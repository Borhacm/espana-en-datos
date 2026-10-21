"""Lectores de cada fuente. Todos devuelven una lista de dicts planos, una fila por observación."""

import csv
import json
import urllib.parse

from .http import fetch

EUROSTAT_API = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"
OECD_API = "https://sdmx.oecd.org/public/rest/data"
WORLDBANK_API = "https://api.worldbank.org/v2"
WIKI_API = "https://{lang}.wikipedia.org/w/api.php"


def eurostat(dataset: str, **filters) -> list[dict]:
    """Dataset de Eurostat en JSON-stat. Los filtros aceptan un valor o una lista de valores."""
    params = [("lang", "en")]
    for dim, val in filters.items():
        for v in val if isinstance(val, (list, tuple)) else [val]:
            params.append((dim, v))
    url = f"{EUROSTAT_API}/{dataset}?{urllib.parse.urlencode(params)}"
    d = json.loads(fetch(url, ".json").read_text())
    if "error" in d:
        raise RuntimeError(f"Eurostat {dataset}: {d['error']}")

    ids, sizes = d["id"], d["size"]
    by_pos = {k: {i: code for code, i in d["dimension"][k]["category"]["index"].items()} for k in ids}
    labels = d["dimension"].get("geo", {}).get("category", {}).get("label", {})
    status = d.get("status", {})

    rows = []
    for flat, value in d["value"].items():
        rest, coords = int(flat), []
        for size in reversed(sizes):
            coords.append(rest % size)
            rest //= size
        row = {k: by_pos[k][c] for k, c in zip(ids, reversed(coords))}
        row["value"] = value
        row["geo_label"] = labels.get(row.get("geo"), "")
        row["flag"] = status.get(flat, "")
        rows.append(row)
    return rows


def oecd(flow: str, key: str, start: str | None = None) -> list[dict]:
    """Dataflow SDMX de la OCDE, p. ej. flow='OECD.STI.STP,DSD_MSTI@DF_MSTI,1.3'."""
    url = f"{OECD_API}/{flow}/{key}?format=csvfilewithlabels"
    if start:
        url += f"&startPeriod={start}"
    path = fetch(url, ".csv")
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def worldbank(indicator: str, countries: list[str], start: int, end: int) -> list[dict]:
    url = (f"{WORLDBANK_API}/country/{';'.join(countries)}/indicator/{indicator}"
           f"?format=json&date={start}:{end}&per_page=2000")
    payload = json.loads(fetch(url, ".json").read_text())
    return [
        {"iso3": x["countryiso3code"], "time": x["date"], "value": x["value"]}
        for x in payload[1] if x["value"] is not None
    ]




def wikipedia(page: str, lang: str = "es", prop: str = "wikitext") -> str:
    """Wikitexto (o HTML con prop='text') de una página de Wikipedia (CC BY-SA 4.0)."""
    params = {"action": "parse", "page": page, "prop": prop, "format": "json", "formatversion": "2", "redirects": "1"}
    url = f"{WIKI_API.format(lang=lang)}?{urllib.parse.urlencode(params)}"
    d = json.loads(fetch(url, ".json").read_text())
    if "error" in d:
        raise RuntimeError(f"Wikipedia {page}: {d['error']}")
    return d["parse"][prop]


INE_API = "https://servicios.ine.es/wstempus/js/ES"
# FK_Periodo del INE: meses 1-12, trimestres 19-22, año 28
INE_QUARTER = {19: 1, 20: 2, 21: 3, 22: 4}


def ine_table(table: int, last: int | None = None) -> list[dict]:
    """Tabla del INE (API JSON Tempus). Una fila por observación: serie, año, periodo y valor.

    'period' es "2026Q2", "2026-09" o "2026" según la periodicidad.
    """
    url = f"{INE_API}/DATOS_TABLA/{table}" + (f"?nult={last}" if last else "")
    series = json.loads(fetch(url, ".json").read_text())
    out = []
    for s in series:
        for d in s["Data"]:
            if d.get("Valor") is None or d.get("Secreto"):
                continue
            fk, year = d["FK_Periodo"], d["Anyo"]
            if fk in INE_QUARTER:
                period = f"{year}Q{INE_QUARTER[fk]}"
            elif 1 <= fk <= 12:
                period = f"{year}-{fk:02d}"
            else:
                period = str(year)
            out.append({"series": s["Nombre"].strip().rstrip("."), "period": period, "year": year, "value": d["Valor"]})
    return out


SOCRATA = "https://analisi.transparenciacatalunya.cat/resource/{id}.json"


def socrata_cat(dataset: str, **params) -> list[dict]:
    """Conjunto de datos del portal de transparencia de Cataluña (API Socrata), todas las filas."""
    out, offset, page = [], 0, 50000
    while True:
        q = {"$limit": page, "$offset": offset, **params}
        rows = json.loads(fetch(f"{SOCRATA.format(id=dataset)}?{urllib.parse.urlencode(q)}", ".json").read_text())
        out += rows
        if len(rows) < page:
            return out
        offset += page


BDE_CSV = "https://www.bde.es/webbe/es/estadisticas/compartido/datos/csv/be{table}.csv"
BDE_MONTHS = {"MAR": 1, "JUN": 2, "SEP": 3, "DIC": 4}


def bde(table: str) -> list[dict]:
    """Cuadro del Boletín Estadístico del Banco de España (p. ej. '1310' para el 13.10), trimestral.

    Una fila por observación: código y descripción de la serie, año, trimestre y valor. Los huecos ("_") se omiten.
    """
    path = fetch(BDE_CSV.format(table=table), ".csv")
    rows = list(csv.reader(path.read_text(encoding="latin-1").splitlines()))
    codes, names = rows[0], rows[3]
    out = []
    for r in rows:
        if not r or len(r[0].split()) != 2 or r[0].split()[0] not in BDE_MONTHS:
            continue
        month, year = r[0].split()
        for code, name, v in zip(codes[1:], names[1:], r[1:]):
            if v in ("_", ""):
                continue
            out.append({"code": code, "series": name, "year": int(year), "q": BDE_MONTHS[month], "value": float(v)})
    return out
