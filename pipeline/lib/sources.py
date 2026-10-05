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
