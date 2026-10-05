"""Tema Vivienda (código VI): precios frente a salarios, comunidades, Europa y la ficha de los topes al alquiler en Cataluña."""

import datetime as dt
import re
import unicodedata
from collections import defaultdict

from lib import geo, sources
from lib.output import THEMES, chart

THEMES["vivienda"] = {"code": "VI", "title": "Vivienda"}

IPV_TABLE = 79563       # INE, IPV: índices por CCAA, general, nueva y segunda mano (trimestral)
WAGE_TABLE = 6061       # INE, ETCL: coste laboral por trabajador y CCAA (trimestral)
CPI_TABLE = 24077       # INE, IPC: índice general nacional desde 1961 (mensual)

INE_IPV = {"name": "INE, Índice de Precios de Vivienda", "dataset": f"Tabla {IPV_TABLE}",
           "url": f"https://www.ine.es/jaxiT3/Tabla.htm?t={IPV_TABLE}", "license": "Reutilización libre citando la fuente"}
INE_WAGE = {"name": "INE, Encuesta Trimestral de Coste Laboral", "url": f"https://www.ine.es/jaxiT3/Tabla.htm?t={WAGE_TABLE}"}
INE_CPI = {"name": "INE, Índice de Precios de Consumo", "url": f"https://www.ine.es/jaxiT3/Tabla.htm?t={CPI_TABLE}"}


def _norm(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


# Nombres del INE ("Madrid, Comunidad de", "Castilla - La Mancha"...) -> código de comunidad
def ine_ccaa(name: str) -> str | None:
    n = _norm(name)
    if n.startswith("nacional") or n.startswith("total nacional"):
        return "ES"
    keys = {"andalucia": "01", "aragon": "02", "asturias": "03", "balears": "04", "canarias": "05", "cantabria": "06",
            "castilla y leon": "07", "castilla - la mancha": "08", "castilla-la mancha": "08", "cataluna": "09",
            "comunitat valenciana": "10", "extremadura": "11", "galicia": "12", "madrid": "13", "murcia": "14",
            "navarra": "15", "pais vasco": "16", "rioja": "17", "ceuta": "18", "melilla": "19"}
    for k, code in keys.items():
        if n.startswith(k):
            return code
    return None


def _annual(rows: list[dict]) -> dict[int, float]:
    """Media anual de una serie trimestral o mensual, solo con años completos."""
    by_year = defaultdict(list)
    for r in rows:
        by_year[r["year"]].append(r["value"])
    full = 4 if "Q" in rows[0]["period"] else 12
    return {y: sum(v) / len(v) for y, v in by_year.items() if len(v) == full}


def _pct(a: float, b: float) -> float:
    return round(100 * (b / a - 1), 1)


def _es(v: float) -> str:
    return f"{v:.0f}".replace(".", ",")


# ---------- España en el tiempo ----------

def precios_salarios():
    ipv = [r for r in sources.ine_table(IPV_TABLE) if r["series"] == "Nacional. General. Índice"]
    wage_name = ("Total Nacional. Industria, construcción y servicios (excepto actividades de los hogares como empleadores y de "
                 "organizaciones y organismos extraterritoriales). Coste salarial total. Costes laborales. Euros")
    wage = [r for r in sources.ine_table(WAGE_TABLE) if r["series"] == wage_name]
    cpi = [r for r in sources.ine_table(CPI_TABLE) if r["series"].startswith("Índice general. Índice")
           or r["series"].startswith("Nacional. Índice general. Índice")]
    assert ipv and wage and cpi, (len(ipv), len(wage), len(cpi))
    series = {"vivienda": _annual(ipv), "salarios": _annual(wage), "precios": _annual(cpi)}
    years = sorted(set.intersection(*(set(s) for s in series.values())))
    years = [y for y in years if y >= 2008]
    BASE = 2015
    rows = [{"time": str(y), "series": k, "value": round(100 * s[y] / s[BASE], 1)} for k, s in series.items() for y in years]
    last = years[-1]
    h, w, p = (_pct(series[k][BASE], series[k][last]) for k in ("vivienda", "salarios", "precios"))
    return chart(
        id="vit1-precios-salarios",
        lens="tiempo", theme="vivienda",
        title=f"Desde {BASE}, la vivienda ha subido un {_es(h)} % y los salarios, un {_es(w)} %",
        subtitle=f"Índices, {BASE} = 100. Precio de la vivienda, salario medio por trabajador y precios de consumo",
        unit="Índice (2015 = 100)",
        source={**INE_IPV, "also": [INE_WAGE, INE_CPI]},
        notes=[
            "Vivienda: Índice de Precios de Vivienda (compraventas de vivienda nueva y usada), media anual.",
            "Salarios: coste salarial total por trabajador y mes (industria, construcción y servicios), media anual. Incluye pagas extra.",
            f"Precios: IPC general, media anual. Entre {BASE} y {last} subió un {_es(p)} %.",
            "Solo años completos.",
        ],
        rows=rows,
        extra={"dimensions": {"series": {"vivienda": {"es": "Vivienda"}, "salarios": {"es": "Salarios"}, "precios": {"es": "Precios (IPC)"}}},
               "ref_line": {"value": 100, "label": {"es": str(BASE)}}},
    )


# ---------- España por dentro ----------

def comunidades():
    ipv = [r for r in sources.ine_table(IPV_TABLE) if r["series"].endswith("General. Índice")]
    by_geo = defaultdict(list)
    for r in ipv:
        code = ine_ccaa(r["series"])
        if code:
            by_geo[code].append(r)
    BASE = 2015
    out, last = [], None
    for code, rs in by_geo.items():
        a = _annual(rs)
        last = max(a)
        out.append({"geo": code, "time": str(last), "value": _pct(a[BASE], a[last])})
    es = next(r["value"] for r in out if r["geo"] == "ES")
    # Ceuta y Melilla tienen muy pocas compraventas y un índice muy volátil: no protagonizan el titular
    main = [r for r in out if r["geo"] not in ("ES", "18", "19")]
    top = max(main, key=lambda r: r["value"])
    low = min(main, key=lambda r: r["value"])
    return chart(
        id="vid1-comunidades",
        lens="dentro", theme="vivienda",
        title=f"La vivienda ha subido un {_es(es)} % desde {BASE}: del {_es(top['value'])} % de {geo.CCAA[top['geo']]} "
              f"al {_es(low['value'])} % de {geo.CCAA[low['geo']]}",
        subtitle=f"Subida del precio de la vivienda entre {BASE} y {last}, en %",
        unit="% de subida",
        source=INE_IPV,
        notes=["Índice de Precios de Vivienda, medias anuales. Precios nominales, sin descontar la inflación.",
               "Ceuta y Melilla tienen pocas compraventas, así que su índice varía mucho de un año a otro."],
        rows=sorted(out, key=lambda r: r["geo"]),
        geos=geo.ccaa_table(r["geo"] for r in out),
    )


# ---------- Ficha de política: topes al alquiler en Cataluña ----------

RENT_DATASET = "qww9-bvhh"     # Generalitat: renta media y número de contratos por municipio (fianzas en el INCASÒL)
ZONES_DATASET = "fftm-v9b6"    # Generalitat: áreas de referencia de política de vivienda (zonas tensionadas)
QUARTERS = {"gener-març": 1, "abril-juny": 2, "juliol-setembre": 3, "octubre-desembre": 4}
CAT_SOURCE = {
    "name": "Generalitat de Catalunya, fianzas de alquiler depositadas en el INCASÒL",
    "dataset": f"{RENT_DATASET} y {ZONES_DATASET}",
    "url": f"https://analisi.transparenciacatalunya.cat/d/{RENT_DATASET}",
    "license": "Llicència oberta d'ús d'informació (Catalunya)",
    "also": [{"name": "Zonas de mercado residencial tensionado", "url": f"https://analisi.transparenciacatalunya.cat/d/{ZONES_DATASET}"}],
}
GROUPS = {
    "zmrt1": {"es": "Con tope desde marzo de 2024 (140 municipios)"},
    "zmrt2": {"es": "Con tope desde octubre de 2024 (131 municipios)"},
    "sin": {"es": "Sin tope"},
}
SHORT = {"zmrt1": "Tope mar. 2024", "zmrt2": "Tope oct. 2024", "sin": "Sin tope"}
INDEX_YEAR = 2023  # último año completo antes de los topes


def _cataluna_groups():
    zones = sources.socrata_cat(ZONES_DATASET)
    group = {}
    for z in zones:
        code = z["codmuni"]
        tag = z.get("zona_de_mercat_residencial_tensat", "NA")
        group[code] = "zmrt1" if tag == "ZMRT 1" else "zmrt2" if tag == "ZMRT 2" else "sin"
    counts = defaultdict(int)
    for g in group.values():
        counts[g] += 1
    assert counts["zmrt1"] == 140 and counts["zmrt2"] == 131, dict(counts)

    rows = sources.socrata_cat(RENT_DATASET, ambit_territorial="Municipi")
    agg = defaultdict(lambda: {"n": 0, "rent": 0.0})
    for r in rows:
        q = QUARTERS.get(r.get("periode"))
        if not q or not r.get("habitatges") or not r.get("renda"):
            continue
        year = int(r["any"])
        if year < 2019:
            continue
        g = group.get(r["codi_territorial"][:5])
        if g is None:
            continue
        n = int(r["habitatges"])
        a = agg[(g, year, q)]
        a["n"] += n
        a["rent"] += n * float(r["renda"])
    return agg


def _qtime(year: int, q: int) -> float:
    return round(year + (q - 1) / 4, 2)


def cataluna_topes():
    agg = _cataluna_groups()
    base = {g: [v for (gg, y, q), v in agg.items() if gg == g and y == INDEX_YEAR] for g in GROUPS}
    base_rent = {g: sum(v["rent"] for v in vs) / sum(v["n"] for v in vs) for g, vs in base.items()}
    base_n = {g: sum(v["n"] for v in vs) / 4 for g, vs in base.items()}
    rent_rows, n_rows = [], []
    for (g, y, q), v in sorted(agg.items()):
        rent = v["rent"] / v["n"]
        rent_rows.append({"time": _qtime(y, q), "series": g, "value": round(100 * rent / base_rent[g], 1), "euros": round(rent)})
        n_rows.append({"time": _qtime(y, q), "series": g, "value": round(100 * v["n"] / base_n[g], 1), "contracts": v["n"]})
    last = max(r["time"] for r in rent_rows)
    lq = next((y, q) for (g, y, q) in agg if _qtime(y, q) == last)

    def last_year(rows, g):
        """Media de los últimos cuatro trimestres: evita que un trimestre suelto (y la estacionalidad) marque el titular."""
        rs = sorted((r for r in rows if r["series"] == g), key=lambda r: r["time"])[-4:]
        return round(sum(r["value"] for r in rs) / 4, 1)

    lv = {g: last_year(rent_rows, g) for g in GROUPS}
    ln = {g: last_year(n_rows, g) for g in GROUPS}
    period = f"{['primer', 'segundo', 'tercer', 'cuarto'][lq[1] - 1]} trimestre de {lq[0]}"
    # Posición en el eje: año + fracción del año (los trimestres van en año + (t - 1) / 4)
    events = [
        {"time": 2020.72, "label": {"es": "Ley catalana de contención de rentas (septiembre de 2020)"}},
        {"time": 2022.19, "label": {"es": "El Constitucional la anula (marzo de 2022)"}},
        {"time": 2024.2, "label": {"es": "Tope en los primeros 140 municipios (marzo de 2024)"}},
        {"time": 2024.77, "label": {"es": "Tope en 131 municipios más (octubre de 2024)"}},
    ]
    common_notes = [
        "Contratos de alquiler de vivienda habitual con fianza depositada en el INCASÒL. No incluye los alquileres de temporada "
        "ni los contratos sin fianza depositada.",
        "Titular: media de los últimos cuatro trimestres frente a la de 2023. «Con tope»: municipios con tope desde marzo de 2024.",
        f"Índice: {INDEX_YEAR} = 100 en cada grupo (último año completo antes de los topes). Los grupos parten de niveles distintos: "
        "importa cómo cambian, no su nivel.",
        "Es una comparación descriptiva: los municipios con tope son más urbanos y caros que los demás, así que la diferencia "
        "no se puede atribuir solo a la norma.",
    ]
    rent = chart(
        id="vid2-cataluna-rentas",
        lens="dentro", theme="vivienda",
        title=f"Con tope, la renta de los nuevos alquileres está un {_es(lv['zmrt1'] - 100)} % por encima de {INDEX_YEAR}; "
              f"sin tope, un {_es(lv['sin'] - 100)} %",
        subtitle=f"Renta media de los contratos firmados cada trimestre, índice {INDEX_YEAR} = 100, hasta el {period}",
        unit=f"Índice ({INDEX_YEAR} = 100)",
        source=CAT_SOURCE,
        notes=common_notes + ["Renta media ponderada por el número de contratos de cada municipio: si cambia el tipo de vivienda "
                              "que se alquila (más pequeña, por ejemplo), cambia la media aunque no cambien los precios."],
        rows=rent_rows,
        extra={"dimensions": {"series": GROUPS}, "short_labels": SHORT, "events": events, "quarterly": True,
               "ref_line": {"value": 100, "label": {"es": str(INDEX_YEAR)}}},
    )
    contracts = chart(
        id="vid3-cataluna-contratos",
        lens="dentro", theme="vivienda",
        title=f"Con tope, se firman un {_es(100 - ln['zmrt1'])} % menos de contratos de alquiler que en {INDEX_YEAR}; "
              f"sin tope, un {_es(100 - ln['sin'])} % menos",
        subtitle=f"Contratos de alquiler registrados cada trimestre, índice {INDEX_YEAR} = 100 (media trimestral), hasta el {period}",
        unit=f"Índice ({INDEX_YEAR} = 100)",
        source=CAT_SOURCE,
        notes=common_notes + ["Menos contratos nuevos puede significar menos oferta, pero también que los inquilinos se mudan menos. "
                              "Este dato no permite distinguirlo."],
        rows=n_rows,
        extra={"dimensions": {"series": GROUPS}, "short_labels": SHORT, "events": events, "quarterly": True,
               "ref_line": {"value": 100, "label": {"es": str(INDEX_YEAR)}}},
    )
    return rent, contracts


# ---------- España frente a Europa ----------

def europa_precios():
    BASE, LAST = "2015", None
    raw = sources.eurostat("prc_hpi_a", purchase="TOTAL", unit="I15_A_AVG")
    years = sorted({r["time"] for r in raw if geo.from_eurostat(r["geo"]) == "EU27"})
    LAST = years[-1]
    out = []
    for r in raw:
        c = geo.from_eurostat(r["geo"])
        if r["time"] == LAST and c and (c == "EU27" or geo.COUNTRIES.get(c, (0, 0, 0, False))[3]):
            out.append({"geo": c, "time": LAST, "value": round(r["value"] - 100, 1)})
    es = next(r["value"] for r in out if r["geo"] == "ESP")
    eu = next(r["value"] for r in out if r["geo"] == "EU27")
    rank = sorted((r for r in out if r["geo"] != "EU27"), key=lambda r: -r["value"]).index(next(r for r in out if r["geo"] == "ESP")) + 1
    return chart(
        id="vie1-europa-precios",
        lens="europa", theme="vivienda",
        title=f"La vivienda ha subido un {_es(es)} % en España desde {BASE}, frente al {_es(eu)} % de la UE",
        subtitle=f"Subida del precio de la vivienda entre {BASE} y {LAST}, en %. España es el {rank}.º de {len(out) - 1} países",
        unit="% de subida",
        source={"name": "Eurostat", "dataset": "prc_hpi_a", "url": "https://ec.europa.eu/eurostat/databrowser/view/prc_hpi_a/default/table",
                "license": "CC BY 4.0"},
        notes=["Índice de precios de la vivienda de Eurostat: compraventas de vivienda nueva y usada. Precios nominales.",
               "Para España, Eurostat usa el índice del INE."],
        rows=sorted(out, key=lambda r: r["geo"]),
        geos=geo.country_table(r["geo"] for r in out),
    )


def europa_sobrecarga():
    raw = sources.eurostat("ilc_lvho07c", tenure="RENT_MKT", unit="PC")
    years = sorted({r["time"] for r in raw if geo.from_eurostat(r["geo"]) == "EU27"})
    LAST = years[-1]
    out = []
    for r in raw:
        c = geo.from_eurostat(r["geo"])
        if r["time"] == LAST and c and (c == "EU27" or geo.COUNTRIES.get(c, (0, 0, 0, False))[3]):
            out.append({"geo": c, "time": LAST, "value": round(r["value"], 1)})
    es = next(r["value"] for r in out if r["geo"] == "ESP")
    eu = next(r["value"] for r in out if r["geo"] == "EU27")
    rank = sorted((r for r in out if r["geo"] != "EU27"), key=lambda r: -r["value"]).index(next(r for r in out if r["geo"] == "ESP")) + 1
    return chart(
        id="vie2-europa-sobrecarga",
        lens="europa", theme="vivienda",
        title=f"El {_es(es)} % de los inquilinos que pagan alquiler de mercado en España dedica más del 40 % de su renta a la vivienda; "
              f"en la UE, el {_es(eu)} %",
        subtitle=f"Inquilinos a precio de mercado con sobrecarga de gastos de vivienda, {LAST}, en %. España es el {rank}.º de {len(out) - 1}",
        unit="% de inquilinos",
        source={"name": "Eurostat", "dataset": "ilc_lvho07c", "url": "https://ec.europa.eu/eurostat/databrowser/view/ilc_lvho07c/default/table",
                "license": "CC BY 4.0"},
        notes=["Sobrecarga: los gastos de vivienda (alquiler, suministros, comunidad) superan el 40 % de la renta disponible del hogar, "
               "descontadas las ayudas a la vivienda. Encuesta de Condiciones de Vida (EU-SILC)."],
        rows=sorted(out, key=lambda r: r["geo"]),
        geos=geo.country_table(r["geo"] for r in out),
    )


def cataluna():
    return list(cataluna_topes())


BUILDERS = [precios_salarios, comunidades, cataluna, europa_precios, europa_sobrecarga]
