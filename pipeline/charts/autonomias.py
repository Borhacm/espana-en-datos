"""Tema Autonomías (código AU): cuánto gastan y deben las comunidades, cómo se reparte su financiación y a quién deben."""

from lib import geo, sources
from lib.output import THEMES, chart

from .common import bi, dec, es_num, ordinal_en

THEMES["autonomias"] = {"code": "AU", "title": "Autonomías"}

BDE = {"name": "Banco de España, Boletín Estadístico", "license": "Reutilización libre citando la fuente"}
BDE_URL = "https://www.bde.es/wbe/es/estadisticas/temas/administraciones-publicas/"
EUROSTAT_GOV = {"name": "Eurostat, cuentas de las administraciones públicas", "license": "CC BY 4.0"}

# Cuadro 13.10: deuda PDE de cada comunidad en % de su PIB. Sufijo del código de serie -> código de comunidad
BDE_CCAA = {"ACS": "ES", "ACS_AAN": "01", "ACS_AAR": "02", "ACS_AAS": "03", "ACS_ABA": "04", "ACS_ACA": "05", "ACS_ACB": "06",
            "ACS_ACO": "07", "ACS_ACL": "08", "ACS_ACT": "09", "ACS_AVA": "10", "ACS_AEX": "11", "ACS_AGA": "12", "ACS_AMA": "13",
            "ACS_AMU": "14", "ACS_ANA": "15", "ACS_APV": "16", "ACS_ALR": "17"}
QUARTER_ES = ["marzo", "junio", "septiembre", "diciembre"]
QUARTER_EN = ["March", "June", "September", "December"]


def _qtime(year: int, q: int) -> float:
    return round(year + (q - 1) / 4, 2)


def _eu_rows(raw, value, last):
    """Filas de los países de la UE (y la media) para el año `last`, con `value(dict de sectores)`."""
    by = {}
    for r in raw:
        c = geo.from_eurostat(r["geo"])
        if r["time"] == last and c and (c == "EU27" or geo.COUNTRIES.get(c, (0, 0, 0, False))[3]):
            by.setdefault(c, {})[r["sector"]] = r["value"]
    return [{"geo": c, "time": last, **value(d)} for c, d in by.items() if "S13" in d]


def _with_article(code: str, lang: str = "es") -> str:
    """Nombre de la comunidad tal como va tras una preposición: «en la Comunidad Valenciana», «in the Balearic Islands»."""
    name = geo.ccaa_name(code, lang)
    if lang == "es":
        return f"la {name}" if code == "10" else name
    return f"the {name}" if code in ("04", "05", "10", "16") else name


def _rank(out, code="ESP"):
    ranked = sorted((r for r in out if r["geo"] != "EU27"), key=lambda r: -r["value"])
    return ranked.index(next(r for r in out if r["geo"] == code)) + 1, len(ranked)


# ---------- España frente a Europa ----------

def europa_gasto():
    raw = sources.eurostat("gov_10a_main", na_item="TE", unit="PC_GDP", sector=["S13", "S1312", "S1313"])
    last = max(r["time"] for r in raw if r["geo"] == "EU27_2020" and r["sector"] == "S13")

    def share(d):
        reg, loc = d.get("S1312") or 0, d.get("S1313") or 0
        return {"value": round(100 * (reg + loc) / d["S13"], 1), "regional": reg, "local": loc, "total": d["S13"]}

    out = _eu_rows(raw, share, last)
    es = next(r for r in out if r["geo"] == "ESP")
    eu = next(r for r in out if r["geo"] == "EU27")
    rank, n = _rank(out)
    return chart(
        id="aue1-europa-gasto",
        lens="europa", theme="autonomias",
        title=bi(f"Comunidades y ayuntamientos gastan el {es_num(es['value'])} % del dinero público en España; en la UE, el {es_num(eu['value'])} %",
                 f"Regions and municipalities spend {es_num(es['value'])}% of public money in Spain; in the EU, {es_num(eu['value'])}%"),
        subtitle=bi(f"Gasto de los gobiernos regionales y locales sobre el gasto de todas las administraciones, {last}, en %. "
                    f"España es el {rank}.º de {n} países",
                    f"Spending by regional and local governments as a share of all government spending, {last}, in %. "
                    f"Spain ranks {ordinal_en(rank)} of {n} countries"),
        unit=bi("% del gasto público", "% of public spending"),
        source={**EUROSTAT_GOV, "dataset": "gov_10a_main", "url": "https://ec.europa.eu/eurostat/databrowser/view/gov_10a_main/default/table"},
        notes={
            "es": [
                "Gasto total de cada nivel de gobierno en las cuentas nacionales (SEC 2010). Se suman sin descontar las transferencias "
                "entre ellos, así que el porcentaje puede estar algo sobrestimado.",
                "Solo Alemania, Austria, Bélgica y España tienen un nivel regional propio en estas cuentas. En el resto de países, "
                "las regiones que existen (por ejemplo, en Italia o Francia) se cuentan dentro del nivel local.",
                f"España, {last}: comunidades autónomas, {dec(es['regional'], 'es')} % del PIB; corporaciones locales, "
                f"{dec(es['local'], 'es')} % del PIB.",
            ],
            "en": [
                "Total spending by each level of government in the national accounts (ESA 2010). The levels are added up without "
                "netting out transfers between them, so the share may be somewhat overstated.",
                "Only Germany, Austria, Belgium and Spain have a separate regional level in these accounts. In the other countries, "
                "existing regions (in Italy or France, for example) are counted within the local level.",
                f"Spain, {last}: regional governments, {dec(es['regional'], 'en')}% of GDP; local governments, "
                f"{dec(es['local'], 'en')}% of GDP.",
            ],
        },
        rows=sorted(out, key=lambda r: r["geo"]),
        geos=geo.country_table(r["geo"] for r in out),
    )


def europa_deuda():
    raw = sources.eurostat("gov_10dd_edpt1", na_item="GD", unit="PC_GDP", sector=["S13", "S1312", "S1313"])
    last = max(r["time"] for r in raw if r["geo"] == "EU27_2020" and r["sector"] == "S13")

    def debt(d):
        reg, loc = d.get("S1312") or 0, d.get("S1313") or 0
        return {"value": round(reg + loc, 1), "regional": reg, "local": loc}

    out = _eu_rows(raw, debt, last)
    es = next(r for r in out if r["geo"] == "ESP")
    eu = next(r for r in out if r["geo"] == "EU27")
    rank, n = _rank(out)
    ahead = [geo.country_name(r["geo"], "es") for r in sorted(out, key=lambda r: -r["value"]) if r["geo"] not in ("EU27",)][:rank - 1]
    ahead_en = [geo.country_name(r["geo"], "en") for r in sorted(out, key=lambda r: -r["value"]) if r["geo"] not in ("EU27",)][:rank - 1]
    assert rank == 2, (rank, ahead)  # el titular dice «solo por detrás de»
    return chart(
        id="aue2-europa-deuda",
        lens="europa", theme="autonomias",
        title=bi(f"La deuda de comunidades y ayuntamientos llega al {dec(es['value'], 'es')} % del PIB, solo por detrás de {ahead[0]} en la UE",
                 f"Regional and local government debt reaches {dec(es['value'], 'en')}% of GDP, second only to {ahead_en[0]} in the EU"),
        subtitle=bi(f"Deuda de los gobiernos regionales y locales, {last}, en % del PIB. Media de la UE: {dec(eu['value'], 'es')} %",
                    f"Debt of regional and local governments, {last}, as % of GDP. EU average: {dec(eu['value'], 'en')}%"),
        unit=bi("% del PIB", "% of GDP"),
        source={**EUROSTAT_GOV, "dataset": "gov_10dd_edpt1", "url": "https://ec.europa.eu/eurostat/databrowser/view/gov_10dd_edpt1/default/table"},
        notes={
            "es": [
                "Deuda según el protocolo de déficit excesivo (PDE), a fin de año. Incluye lo que cada nivel debe a otras "
                "administraciones; en España, sobre todo los préstamos del Estado a las comunidades.",
                "Solo Alemania, Austria, Bélgica y España tienen un nivel regional propio en estas cuentas; en el resto, el dato es solo local.",
                f"España, {last}: comunidades autónomas, {dec(es['regional'], 'es')} % del PIB; corporaciones locales, "
                f"{dec(es['local'], 'es')} % del PIB.",
            ],
            "en": [
                "Debt under the excessive deficit procedure (EDP), at year end. It includes what each level owes to other "
                "parts of government; in Spain, mainly central government loans to the regions.",
                "Only Germany, Austria, Belgium and Spain have a separate regional level in these accounts; elsewhere, the figure is local only.",
                f"Spain, {last}: regional governments, {dec(es['regional'], 'en')}% of GDP; local governments, "
                f"{dec(es['local'], 'en')}% of GDP.",
            ],
        },
        rows=sorted(out, key=lambda r: r["geo"]),
        geos=geo.country_table(r["geo"] for r in out),
    )


# ---------- España por dentro ----------

def deuda_comunidades():
    raw = [r for r in sources.bde("1310") if r["code"].startswith("DTNPDE2010_P0000P_PS_")]
    by_code = {}
    for r in raw:
        by_code.setdefault(r["code"].removeprefix("DTNPDE2010_P0000P_PS_"), []).append(r)
    last = max((r["year"], r["q"]) for r in raw)
    out = []
    for suffix, code in BDE_CCAA.items():
        r = next(x for x in by_code[suffix] if (x["year"], x["q"]) == last)
        out.append({"geo": code, "time": f"{last[0]}T{last[1]}", "value": r["value"]})
    es = next(r["value"] for r in out if r["geo"] == "ES")
    # El titular compara comunidades de régimen común: las forales (País Vasco y Navarra) se financian de otra forma
    common = [r for r in out if r["geo"] not in ("ES", "15", "16")]
    top, low = max(common, key=lambda r: r["value"]), min(common, key=lambda r: r["value"])
    period, period_en = f"{QUARTER_ES[last[1] - 1]} de {last[0]}", f"{QUARTER_EN[last[1] - 1]} {last[0]}"
    return chart(
        id="aud1-deuda-comunidades",
        lens="dentro", theme="autonomias",
        title=bi(f"La deuda equivale al {dec(top['value'], 'es')} % del PIB en {_with_article(top['geo'])} y al "
                 f"{dec(low['value'], 'es')} % en {_with_article(low['geo'])}",
                 f"Debt equals {dec(top['value'], 'en')}% of GDP in {_with_article(top['geo'], 'en')} and "
                 f"{dec(low['value'], 'en')}% in {_with_article(low['geo'], 'en')}"),
        subtitle=bi(f"Deuda de cada comunidad en % de su PIB, {period}. Todas las comunidades: {dec(es, 'es')} % del PIB de España",
                    f"Debt of each region as % of its GDP, {period_en}. All regions: {dec(es, 'en')}% of Spain's GDP"),
        unit=bi("% del PIB regional", "% of regional GDP"),
        source={**BDE, "dataset": "Cuadro 13.10", "url": BDE_URL},
        notes={
            "es": [
                "Deuda según el protocolo de déficit excesivo (PDE) de cada comunidad y sus organismos, incluida la que debe al Estado. "
                "PIB de los últimos cuatro trimestres.",
                "El Banco de España no publica este dato para Ceuta y Melilla, que son ciudades autónomas.",
                "El País Vasco y Navarra tienen un régimen foral: recaudan casi todos sus impuestos y no participan en el sistema "
                "de financiación común. Por eso el titular compara solo las comunidades de régimen común.",
            ],
            "en": [
                "Debt under the excessive deficit procedure (EDP) of each region and its agencies, including what it owes to "
                "central government. GDP over the last four quarters.",
                "The Bank of Spain does not publish this figure for Ceuta and Melilla, which are autonomous cities.",
                "The Basque Country and Navarre have a foral regime: they collect almost all their own taxes and are not part of "
                "the common financing system. That is why the headline compares only the common-regime regions.",
            ],
        },
        rows=sorted(out, key=lambda r: r["geo"]),
        geos=geo.ccaa_table(r["geo"] for r in out),
    )


# Fedea (A. de la Fuente), «La liquidación de 2024 del sistema de financiación de las comunidades autónomas de régimen común»,
# Estudios sobre la Economía Española 2026/24, cuadro 9: componentes del índice de financiación efectiva a competencias
# homogéneas por habitante ajustado (media de las comunidades de régimen común = 100), 2024.
# Columnas: ingresos tributarios homogéneos, transferencia de garantía, Fondo de Suficiencia, Fondo de Cooperación,
# Fondo de Competitividad y DA3, total.
FEDEA_2024 = {
    "09": (110.6, -5.9, -7.6, 0.0, 5.4, 102.6),
    "12": (75.6, 17.8, 4.1, 4.8, 0.0, 102.3),
    "01": (75.1, 19.4, -1.7, 2.1, 0.0, 94.7),
    "03": (81.1, 13.5, 3.3, 4.8, 0.0, 102.7),
    "06": (87.7, 5.8, 20.1, 5.0, 0.0, 118.6),
    "17": (86.8, 10.2, 14.0, 1.3, 0.0, 112.2),
    "14": (72.9, 19.1, -5.0, 1.9, 3.1, 92.0),
    "10": (85.0, 10.1, -11.5, 1.8, 7.3, 92.8),
    "02": (89.3, 6.4, 4.4, 1.1, 0.0, 101.3),
    "08": (69.4, 22.4, 1.1, 1.8, 0.0, 94.7),
    "05": (55.1, 44.8, -3.6, 1.9, 10.1, 108.4),
    "11": (64.3, 27.3, 13.8, 5.2, 0.0, 110.6),
    "04": (118.5, -7.7, -22.2, 0.0, 20.6, 109.2),
    "13": (135.3, -25.7, -10.0, 0.0, 0.7, 100.3),
    "07": (81.3, 14.1, 5.6, 4.6, 0.0, 105.7),
}
FEDEA_SOURCE = {
    "name": "Fedea, A. de la Fuente, La liquidación de 2024 del sistema de financiación de las comunidades autónomas de régimen común",
    "dataset": "Estudios sobre la Economía Española 2026/24, cuadro 9",
    "url": "https://documentos.fedea.net/pubs/eee/2026/eee2026-24.pdf",
    "license": "Cita de un estudio publicado",
}
STAGES = {"antes": bi("Sus impuestos", "Its own taxes"), "despues": bi("Financiación final", "Final funding")}


def financiacion():
    # Comprobaciones de la transcripción: cada fila suma su total (±0,2: Fedea redondea cada columna)
    for code, (*parts, total) in FEDEA_2024.items():
        assert abs(sum(parts) - total) <= 0.25, (code, sum(parts), total)
    rows = []
    for code, v in FEDEA_2024.items():
        rows.append({"geo": code, "time": "antes", "stage": "antes", "value": v[0]})
        rows.append({"geo": code, "time": "despues", "stage": "despues", "value": v[5]})
    m, c = FEDEA_2024["13"], FEDEA_2024["05"]
    return chart(
        id="aud2-financiacion",
        lens="dentro", theme="autonomias",
        title=bi(f"Con sus impuestos, Madrid reúne {es_num(m[0])} por habitante ajustado y Canarias, {es_num(c[0])}; "
                 f"tras el reparto, {es_num(m[5])} y {es_num(c[5])}",
                 f"With its own taxes, Madrid raises {es_num(m[0])} per adjusted inhabitant and the Canary Islands {es_num(c[0])}; "
                 f"after redistribution, {es_num(m[5])} and {es_num(c[5])}"),
        subtitle=bi("Ingresos tributarios y financiación final por habitante ajustado, 2024. Índice: financiación media de las "
                    "comunidades de régimen común = 100",
                    "Tax revenue and final funding per adjusted inhabitant, 2024. Index: average funding of the common-regime "
                    "regions = 100"),
        unit=bi("Índice (media = 100)", "Index (average = 100)"),
        source=FEDEA_SOURCE,
        notes={
            "es": [
                "Población ajustada: la población corregida por lo que el sistema estima que cuesta prestar los servicios en cada "
                "territorio (edad, dispersión, superficie, insularidad).",
                "Cálculos de Fedea sobre la liquidación oficial de Hacienda, a competencias homogéneas e igual esfuerzo fiscal: "
                "como si todas cobraran los mismos impuestos y tuvieran las mismas competencias.",
                "«Sus impuestos»: tributos cedidos a cada comunidad, incluido el régimen económico y fiscal de Canarias. "
                "«Financiación final»: después del Fondo de Garantía y de los fondos de Suficiencia, Cooperación y Competitividad.",
                "Solo las 15 comunidades de régimen común: el País Vasco y Navarra tienen régimen foral, y Ceuta y Melilla, uno propio.",
            ],
            "en": [
                "Adjusted population: population corrected for what the system estimates it costs to provide services in each "
                "territory (age, dispersion, area, insularity).",
                "Fedea calculations on the official Finance Ministry settlement, with the same powers and the same tax effort: "
                "as if every region levied the same taxes and had the same responsibilities.",
                "«Its own taxes»: taxes ceded to each region, including the Canary Islands' special tax regime. «Final funding»: "
                "after the Guarantee Fund and the Sufficiency, Cooperation and Competitiveness funds.",
                "Only the 15 common-regime regions: the Basque Country and Navarre have a foral regime, and Ceuta and Melilla their own.",
            ],
        },
        rows=sorted(rows, key=lambda r: (r["geo"], r["time"])),
        geos=geo.ccaa_table(FEDEA_2024),
        extra={"dimensions": {"time": STAGES, "stage": STAGES}},
    )


# ---------- España en el tiempo ----------

def deuda_tiempo():
    raw = [r for r in sources.bde("1310") if r["code"] == "DTNPDE2010_P0000P_PS_ACS"]
    rows = [{"time": _qtime(r["year"], r["q"]), "series": "deuda", "value": r["value"]} for r in raw]
    by_q = {(r["year"], r["q"]): r["value"] for r in raw}
    pre = (2007, 4)                                   # final de 2007, antes de la crisis financiera
    peak = max(by_q, key=lambda k: by_q[k])
    last = max(by_q)
    when = lambda k, lang: (f"{QUARTER_ES[k[1] - 1]} de {k[0]}" if lang == "es" else f"{QUARTER_EN[k[1] - 1]} {k[0]}")
    return chart(
        id="aut1-deuda",
        lens="tiempo", theme="autonomias",
        title=bi(f"La deuda de las comunidades pasó del {dec(by_q[pre], 'es')} % del PIB a finales de {pre[0]} al "
                 f"{dec(by_q[peak], 'es')} % en {when(peak, 'es')}; en {when(last, 'es')}, el {dec(by_q[last], 'es')} %",
                 f"Regional debt went from {dec(by_q[pre], 'en')}% of GDP at the end of {pre[0]} to "
                 f"{dec(by_q[peak], 'en')}% in {when(peak, 'en')}; in {when(last, 'en')}, {dec(by_q[last], 'en')}%"),
        subtitle=bi(f"Deuda del conjunto de las comunidades autónomas, en % del PIB, trimestral desde {raw[0]['year']}",
                    f"Debt of all regional governments, as % of GDP, quarterly since {raw[0]['year']}"),
        unit=bi("% del PIB", "% of GDP"),
        source={**BDE, "dataset": "Cuadro 13.10", "url": BDE_URL},
        notes={
            "es": ["Deuda PDE a final de cada trimestre sobre el PIB de los últimos cuatro trimestres.",
                   "En 2020 y principios de 2021 el PIB cayó por la pandemia: el porcentaje subió también porque bajó el denominador."],
            "en": ["EDP debt at the end of each quarter over GDP for the last four quarters.",
                   "In 2020 and early 2021 GDP fell because of the pandemic: the ratio also rose because the denominator shrank."],
        },
        rows=rows,
        extra={"dimensions": {"series": {"deuda": bi("Deuda de las comunidades", "Regional debt")}}, "quarterly": True,
               "events": [{"time": 2012.5, "label": bi("El Estado crea el Fondo de Liquidez Autonómico (julio de 2012)",
                                                        "Central government creates the Regional Liquidity Fund (July 2012)")}]},
    )


def acreedores():
    raw = sources.bde("1307")
    total = {(r["year"], r["q"]): r["value"] for r in raw if r["code"] == "DTNPDE2010_P00000_PS_ACS"}
    state = {(r["year"], r["q"]): r["value"] for r in raw if r["code"] == "DTNPDE2010_F42116_PS_ACS"}
    START = 2008
    rows = []
    for k in sorted(total):
        if k[0] < START:
            continue
        s = state.get(k, 0)
        t = _qtime(*k)
        rows.append({"time": t, "series": "estado", "value": round(s / 1e6, 1)})
        rows.append({"time": t, "series": "resto", "value": round((total[k] - s) / 1e6, 1)})
    last = max(total)
    share = 100 * state[last] / total[last]
    first_state = min(k for k, v in state.items() if v > 0)
    period, period_en = f"{QUARTER_ES[last[1] - 1]} de {last[0]}", f"{QUARTER_EN[last[1] - 1]} {last[0]}"
    return chart(
        id="aut2-acreedores",
        lens="tiempo", theme="autonomias",
        title=bi(f"El Estado es el acreedor de {es_num(share)} de cada 100 euros que deben las comunidades",
                 f"Central government is the creditor for {es_num(share)} of every 100 euros the regions owe"),
        subtitle=bi(f"Deuda de las comunidades según a quién se debe, en miles de millones de euros, trimestral, {START} a {period}",
                    f"Regional debt by creditor, in billions of euros, quarterly, {START} to {period_en}"),
        unit=bi("Miles de millones de euros", "Billions of euros"),
        source={**BDE, "dataset": "Cuadro 13.7", "url": BDE_URL},
        notes={
            "es": [
                "«Préstamos del Estado»: préstamos de los fondos de financiación de la Administración central a las comunidades "
                f"(pago a proveedores, Fondo de Liquidez Autonómico y sus sucesores). Aparecen en {first_state[0]}.",
                "«Bonos, bancos y otros»: deuda emitida en los mercados, préstamos de entidades financieras y otros pasivos.",
                f"Titular: a {period}.",
            ],
            "en": [
                "«Central government loans»: loans from central government financing funds to the regions (supplier payments, "
                f"the Regional Liquidity Fund and its successors). They first appear in {first_state[0]}.",
                "«Bonds, banks and other»: debt issued on the markets, loans from financial institutions and other liabilities.",
                f"Headline: as of {period_en}.",
            ],
        },
        rows=rows,
        extra={"dimensions": {"series": {"estado": bi("Préstamos del Estado", "Central government loans"),
                                         "resto": bi("Bonos, bancos y otros", "Bonds, banks and other")}},
               "quarterly": True},
    )


BUILDERS = [europa_gasto, europa_deuda, deuda_comunidades, financiacion, deuda_tiempo, acreedores]
