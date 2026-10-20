"""Tema La legislatura en datos (código LE): paro, crecimiento, deuda, empleo, salarios y cuentas públicas desde las generales
de julio de 2023.

Balance descriptivo: compara el último periodo disponible con 2023, el año de las últimas generales. No atribuye mérito ni culpa.
Revisado el 19 de octubre de 2026: cada gráfico responde a una pregunta del guion (editorial/registro/a01.md), el paro ya no se
repite en las tres miradas y tres gráficos explican el porqué (PIB por habitante, tasa de empleo, ingresos y gastos).
"""

import math
from collections import defaultdict

from lib import geo, sources
from lib.output import THEMES, chart

from .common import annual, bi, ine_ccaa, ordinal_en, pct

THEMES["legislatura"] = {"code": "LE", "title": "La legislatura en datos"}

START = 2023            # año de las últimas generales (23 de julio de 2023)
PARO_TABLE = 65334      # INE, EPA: tasas de paro por edad, sexo y comunidad (trimestral)
OCUP_TABLE = 65302      # INE, EPA: ocupados por edad, sexo y comunidad, miles (trimestral)
EMP_RATE_TABLE = 14508  # INE, EPA: tasas de empleo por grupo de edad, sexo y comunidad (trimestral)
WAGE_TABLE = 6061       # INE, ETCL: coste salarial por trabajador y comunidad (trimestral)
CPI_TABLE = 24077       # INE, IPC: índice general nacional (mensual)

INE_EPA = {"name": "INE, Encuesta de Población Activa", "dataset": f"Tablas {PARO_TABLE} y {OCUP_TABLE}",
           "url": f"https://www.ine.es/jaxiT3/Tabla.htm?t={PARO_TABLE}", "license": "Reutilización libre citando la fuente"}
INE_EMP_RATE = {"name": "INE, Encuesta de Población Activa", "dataset": f"Tablas {EMP_RATE_TABLE} y {OCUP_TABLE}",
                "url": f"https://www.ine.es/jaxiT3/Tabla.htm?t={EMP_RATE_TABLE}", "license": "Reutilización libre citando la fuente"}
EUROSTAT_NA = {"name": "Eurostat, cuentas nacionales", "dataset": "nama_10_gdp y nama_10_pc",
               "url": "https://ec.europa.eu/eurostat/databrowser/view/nama_10_pc/default/table", "license": "CC BY 4.0"}
INE_WAGE = {"name": "INE, Encuesta Trimestral de Coste Laboral", "dataset": f"Tabla {WAGE_TABLE}",
            "url": f"https://www.ine.es/jaxiT3/Tabla.htm?t={WAGE_TABLE}", "license": "Reutilización libre citando la fuente"}
INE_CPI = {"name": "INE, Índice de Precios de Consumo", "url": f"https://www.ine.es/jaxiT3/Tabla.htm?t={CPI_TABLE}"}
ORDINAL = ["primer", "segundo", "tercer", "cuarto"]


def es1(v: float) -> str:
    """Un decimal con coma: 10,3."""
    return f"{v:.1f}".replace(".", ",")


def de(code: str) -> str:
    """«de Asturias», «del País Vasco», «de la Comunidad Valenciana»."""
    name = geo.CCAA[code]
    return {"País Vasco": "del País Vasco", "Comunidad Valenciana": "de la Comunidad Valenciana"}.get(name, f"de {name}")


def en1(v: float) -> str:
    """Un decimal con punto, para el inglés: 10.3."""
    return f"{v:.1f}"


def nm(code: str) -> str:
    """Nombre en inglés de una comunidad (o España)."""
    return geo.ccaa_name(code, "en")


def _qlabel_en(period: str) -> str:
    """«2026Q2» -> «Q2 2026»."""
    y, q = period.split("Q")
    return f"Q{q} {y}"


def _qtime(period: str) -> float:
    y, q = period.split("Q")
    return round(int(y) + (int(q) - 1) / 4, 2)


def _qlabel(period: str) -> str:
    y, q = period.split("Q")
    return f"{ORDINAL[int(q) - 1]} trimestre de {y}"


def _last4(rs: list[dict]) -> tuple[float, str, str]:
    """Media de los cuatro últimos trimestres y su primer y último trimestre."""
    rs = sorted(rs, key=lambda r: r["period"])[-4:]
    return sum(r["value"] for r in rs) / 4, rs[0]["period"], rs[-1]["period"]


def _eu_rank(raw: list[dict], year: str, prev: str) -> list[dict]:
    """Filas de un ranking UE: valor del último año y del año de referencia."""
    by = defaultdict(dict)
    for r in raw:
        c = geo.from_eurostat(r["geo"])
        if c and (c == "EU27" or geo.COUNTRIES.get(c, (0, 0, 0, False))[3]):
            by[c][r["time"]] = r["value"]
    return [{"geo": c, "time": year, "value": round(v[year], 1), "prev": round(v[prev], 1)}
            for c, v in sorted(by.items()) if year in v and prev in v]


def _place(out: list[dict], code: str, reverse: bool = True) -> int:
    ranked = sorted((r for r in out if r["geo"] != "EU27"), key=lambda r: -r["value"] if reverse else r["value"])
    return [r["geo"] for r in ranked].index(code) + 1


# ---------- España frente a Europa ----------

def europa_paro():
    raw = sources.eurostat("une_rt_a", age="Y15-74", sex="T", unit="PC_ACT")
    last = max(r["time"] for r in raw if geo.from_eurostat(r["geo"]) == "EU27")
    out = _eu_rank(raw, last, str(START))
    es = next(r for r in out if r["geo"] == "ESP")
    eu = next(r for r in out if r["geo"] == "EU27")
    place = _place(out, "ESP")
    n = len(out) - 1
    first = "la más alta de la UE" if place == 1 else f"la {place}.ª más alta de la UE"
    first_en = "the highest in the EU" if place == 1 else f"the {ordinal_en(place)} highest in the EU"
    was_first = _place([{**r, "value": r["prev"]} for r in out], "ESP") == 1
    return chart(
        id="lee1-europa-paro",
        lens="europa", theme="legislatura",
        title=bi(f"La tasa de paro de España baja del {es1(es['prev'])} % al {es1(es['value'])} % entre {START} y {last}, "
                 f"pero sigue siendo {first}",
                 f"Spain's unemployment rate falls from {en1(es['prev'])}% to {en1(es['value'])}% between {START} and {last}, "
                 f"but it is still {first_en}"),
        subtitle=bi(f"Tasa de paro de 15 a 74 años, {last}, en % de la población activa. Media de la UE: {es1(eu['value'])} %",
                    f"Unemployment rate aged 15 to 74, {last}, as % of the labour force. EU average: {en1(eu['value'])}%"),
        unit=bi("% de la población activa", "% of the labour force"),
        source={"name": "Eurostat", "dataset": "une_rt_a", "url": "https://ec.europa.eu/eurostat/databrowser/view/une_rt_a/default/table",
                "license": "CC BY 4.0"},
        notes={"es": [f"Medias anuales de la Encuesta de Población Activa armonizada (para España, la EPA del INE). Compara {last} con {START}, "
                      "el año de las últimas generales.",
                      f"«prev» en la descarga: tasa de {START}. En {START} España también tenía la tasa más alta de los {n} países."
                      if was_first else f"«prev» en la descarga: tasa de {START}."],
               "en": [f"Annual averages of the harmonised Labour Force Survey (for Spain, INE's EPA). It compares {last} with {START}, "
                      "the year of the last general election.",
                      f"«prev» in the download: rate in {START}. In {START} Spain also had the highest rate of the {n} countries."
                      if was_first else f"«prev» in the download: rate in {START}."]},
        rows=out,
        geos=geo.country_table(r["geo"] for r in out),
    )

def _gdp() -> tuple[dict, dict]:
    """PIB y PIB por habitante en volumen (euros encadenados de 2010), por país y año."""
    gdp = {(r["geo"], r["time"]): r["value"] for r in sources.eurostat("nama_10_gdp", na_item="B1GQ", unit="CLV10_MEUR")}
    pc = {(r["geo"], r["time"]): r["value"] for r in sources.eurostat("nama_10_pc", na_item="B1GQ", unit="CLV10_EUR_HAB")}
    return gdp, pc


def europa_crecimiento():
    gdp, pc = _gdp()
    last = max(t for g, t in gdp if g == "EU27_2020")
    base = str(START)
    out = []
    for (g, t), v in gdp.items():
        c = geo.from_eurostat(g)
        if t != last or (g, base) not in gdp or (g, last) not in pc or (g, base) not in pc:
            continue
        if c and (c == "EU27" or geo.COUNTRIES.get(c, (0, 0, 0, False))[3]):
            out.append({"geo": c, "time": last, "value": pct(gdp[(g, base)], v),
                        "per_capita": pct(pc[(g, base)], pc[(g, last)]),
                        "population": pct(gdp[(g, base)] / pc[(g, base)], v / pc[(g, last)])})
    es = next(r for r in out if r["geo"] == "ESP")
    eu = next(r for r in out if r["geo"] == "EU27")
    place = _place(out, "ESP")
    place_pc = _place([{**r, "value": r["per_capita"]} for r in out], "ESP")
    n = len(out) - 1
    share_pop = 100 * (1 - math.log(1 + es["per_capita"] / 100) / math.log(1 + es["value"] / 100))
    place_pop = _place([{**r, "value": r["population"]} for r in out], "ESP")
    return chart(
        id="lee3-europa-crecimiento",
        lens="europa", theme="legislatura",
        title=bi(f"El PIB de España crece un {es1(es['value'])} % entre {base} y {last}, el {place}.º de {n} países de la UE; "
                 f"por habitante, un {es1(es['per_capita'])} %, el {place_pc}.º",
                 f"Spain's GDP grows {en1(es['value'])}% between {base} and {last}, {ordinal_en(place)} of {n} EU countries; "
                 f"per person, {en1(es['per_capita'])}%, {ordinal_en(place_pc)}"),
        subtitle=bi(f"Crecimiento del PIB en volumen (descontada la inflación) entre {base} y {last}, en %. Media de la UE: "
                    f"{es1(eu['value'])} % ({es1(eu['per_capita'])} % por habitante)",
                    f"Real GDP growth (adjusted for inflation) between {base} and {last}, in %. EU average: "
                    f"{en1(eu['value'])}% ({en1(eu['per_capita'])}% per person)"),
        unit=bi("% de crecimiento", "% growth"),
        source=EUROSTAT_NA,
        notes={"es": ["PIB en volumen encadenado (euros de 2010): mide cuánto más se produce, sin el efecto de los precios.",
                      f"«per_capita» en la descarga: crecimiento del PIB por habitante en el mismo periodo. En España, el aumento de la "
                      f"población explica en torno al {share_pop:.0f} % del crecimiento del PIB (en escala logarítmica).",
                      f"«population» en la descarga: crecimiento de la población implícita (PIB / PIB por habitante). España: "
                      f"{es1(es['population'])} %, el {place_pop}.º de {n}; UE: {es1(eu['population'])} %.",
                      f"Datos de {last} provisionales en varios países, entre ellos España."],
               "en": ["GDP in chain-linked volumes (2010 euros): it measures how much more is produced, without the effect of prices.",
                      f"«per_capita» in the download: growth of GDP per person over the same period. In Spain, population growth "
                      f"explains around {share_pop:.0f}% of GDP growth (on a logarithmic scale).",
                      f"«population» in the download: growth of the implied population (GDP / GDP per person). Spain: "
                      f"{en1(es['population'])}%, {ordinal_en(place_pop)} of {n}; EU: {en1(eu['population'])}%.",
                      f"{last} data provisional in several countries, including Spain."]},
        rows=sorted(out, key=lambda r: r["geo"]),
        geos=geo.country_table(r["geo"] for r in out),
    )



def europa_deuda():
    raw = sources.eurostat("gov_10dd_edpt1", na_item="GD", sector="S13", unit="PC_GDP")
    last = max(r["time"] for r in raw if geo.from_eurostat(r["geo"]) == "EU27")
    out = _eu_rank(raw, last, str(START))
    es = next(r for r in out if r["geo"] == "ESP")
    eu = next(r for r in out if r["geo"] == "EU27")
    place = _place(out, "ESP")
    return chart(
        id="lee2-europa-deuda",
        lens="europa", theme="legislatura",
        title=bi(f"La deuda pública baja del {es1(es['prev'])} % al {es1(es['value'])} % del PIB entre {START} y {last}; "
                 f"en la UE pasa del {es1(eu['prev'])} % al {es1(eu['value'])} %",
                 f"Public debt falls from {en1(es['prev'])}% to {en1(es['value'])}% of GDP between {START} and {last}; "
                 f"in the EU it goes from {en1(eu['prev'])}% to {en1(eu['value'])}%"),
        subtitle=bi(f"Deuda de las administraciones públicas, {last}, en % del PIB. España es la {place}.ª más alta de {len(out) - 1}",
                    f"General government debt, {last}, as % of GDP. Spain's is the {ordinal_en(place)} highest of {len(out) - 1}"),
        unit=bi("% del PIB", "% of GDP"),
        source={"name": "Eurostat", "dataset": "gov_10dd_edpt1",
                "url": "https://ec.europa.eu/eurostat/databrowser/view/gov_10dd_edpt1/default/table", "license": "CC BY 4.0"},
        notes={"es": ["Deuda según el Protocolo de Déficit Excesivo (criterio de Maastricht): Estado, comunidades, ayuntamientos y "
                      "Seguridad Social, a valor nominal y consolidada.",
                      "La ratio baja si la deuda crece menos que el PIB nominal: en euros, la deuda de España ha seguido subiendo.",
                      f"«prev» en la descarga: deuda de {START}."],
               "en": ["Debt under the Excessive Deficit Procedure (Maastricht criterion): central government, regions, local councils "
                      "and Social Security, at nominal value and consolidated.",
                      "The ratio falls if debt grows less than nominal GDP: in euros, Spain's debt has kept rising.",
                      f"«prev» in the download: debt in {START}."]},
        rows=out,
        geos=geo.country_table(r["geo"] for r in out),
    )


# ---------- España por dentro ----------

def _paro_rows():
    rows = [r for r in sources.ine_table(PARO_TABLE)
            if r["series"].startswith("Tasa de paro de la población. Ambos sexos.") and r["series"].endswith(". Total")]
    by = defaultdict(list)
    for r in rows:
        code = ine_ccaa(r["series"].split(". ")[2])
        if code:
            by[code].append(r)
    assert len(by) == 20, sorted(by)
    return by


def paro_comunidades():
    by = _paro_rows()
    out, p0, p1 = [], None, None
    for code, rs in by.items():
        v, p0, p1 = _last4(rs)
        prev = annual(rs)[START]
        out.append({"geo": code, "time": p1, "value": round(v, 1), "prev": round(prev, 1), "change": round(v - prev, 1)})
    es = next(r for r in out if r["geo"] == "ES")
    main = [r for r in out if r["geo"] not in ("ES", "18", "19")]
    down = [r for r in main if r["change"] < 0]
    top = max(main, key=lambda r: r["value"])
    low = min(main, key=lambda r: r["value"])
    who = "las 17 comunidades" if len(down) == 17 else f"{len(down)} de las 17 comunidades"
    top0 = max(main, key=lambda r: r["prev"])
    low0 = min(main, key=lambda r: r["prev"])
    gap0, gap1 = top0["prev"] - low0["prev"], top["value"] - low["value"]
    # ¿Baja más donde era más alto? Correlación entre el paro de partida y su variación
    n = len(main)
    mx, my = sum(r["prev"] for r in main) / n, sum(r["change"] for r in main) / n
    cov = sum((r["prev"] - mx) * (r["change"] - my) for r in main)
    corr = cov / math.sqrt(sum((r["prev"] - mx) ** 2 for r in main) * sum((r["change"] - my) ** 2 for r in main))
    converge = corr < -0.5 and gap1 < gap0
    who_en = "all 17 regions" if len(down) == 17 else f"{len(down)} of the 17 regions"
    title = bi(f"El paro baja más donde era más alto: la distancia entre la comunidad con más paro y la de menos pasa de "
               f"{es1(gap0)} a {es1(gap1)} puntos" if converge else
               f"El paro va del {es1(low['value'])} % {de(low['geo'])} al {es1(top['value'])} % {de(top['geo'])}",
               f"Unemployment falls most where it was highest: the gap between the region with the most unemployment and the one "
               f"with the least narrows from {en1(gap0)} to {en1(gap1)} points" if converge else
               f"Unemployment ranges from {en1(low['value'])}% in {nm(low['geo'])} to {en1(top['value'])}% in {nm(top['geo'])}")
    return chart(
        id="led1-paro-comunidades",
        lens="dentro", theme="legislatura",
        title=title,
        subtitle=bi(f"Tasa de paro, media de los cuatro trimestres del {_qlabel(p0)} al {_qlabel(p1)}, en %. "
                    f"España: {es1(es['value'])} %",
                    f"Unemployment rate, average of the four quarters from {_qlabel_en(p0)} to {_qlabel_en(p1)}, in %. "
                    f"Spain: {en1(es['value'])}%"),
        unit=bi("% de la población activa", "% of the labour force"),
        source=INE_EPA,
        notes={"es": ["Encuesta de Población Activa, población de 16 años y más. Media de los últimos cuatro trimestres para evitar la "
                      "estacionalidad (el paro sube en invierno y baja en verano).",
                      f"«prev» en la descarga: media de {START}; «change»: diferencia en puntos. El paro ha bajado en {who}.",
                      f"Distancia entre la comunidad con más paro y la de menos (sin Ceuta ni Melilla): {es1(gap0)} puntos en {START} "
                      f"({geo.CCAA[top0['geo']]} y {geo.CCAA[low0['geo']]}) y {es1(gap1)} en el último año ({geo.CCAA[top['geo']]} y "
                      f"{geo.CCAA[low['geo']]}). Correlación entre el paro de {START} y su variación: {es1(corr).replace('-', '−')}.",
                      "Ceuta y Melilla tienen muestras pequeñas en la EPA y sus tasas varían mucho de un trimestre a otro."],
               "en": ["Labour Force Survey (EPA), population aged 16 and over. Average of the last four quarters to avoid "
                      "seasonality (unemployment rises in winter and falls in summer).",
                      f"«prev» in the download: {START} average; «change»: difference in points. Unemployment has fallen in {who_en}.",
                      f"Gap between the region with the most unemployment and the one with the least (excluding Ceuta and Melilla): "
                      f"{en1(gap0)} points in {START} ({nm(top0['geo'])} and {nm(low0['geo'])}) and {en1(gap1)} in the last year "
                      f"({nm(top['geo'])} and {nm(low['geo'])}). Correlation between {START} unemployment and its change: "
                      f"{en1(corr).replace('-', '−')}.",
                      "Ceuta and Melilla have small samples in the EPA and their rates vary a lot from one quarter to the next."]},
        rows=sorted(out, key=lambda r: r["geo"]),
        geos=geo.ccaa_table(r["geo"] for r in out),
    )


def _ocupados_es() -> tuple[float, float]:
    """Ocupados en España (miles): media de 2023 y de los cuatro últimos trimestres."""
    rs = [r for r in sources.ine_table(OCUP_TABLE) if r["series"] == "Total Nacional. Ambos sexos. Total. Ocupados. Valor absoluto"]
    assert rs
    return annual(rs)[START], _last4(rs)[0]


def tasa_empleo_comunidades():
    by = defaultdict(list)
    for r in sources.ine_table(EMP_RATE_TABLE):
        s = r["series"]
        if s == "Total Nacional. Tasa de empleo de la población. Ambos sexos. De 25 a 54 años":
            by["ES"].append(r)
        elif s.startswith("Tasa de empleo de la población. ") and s.endswith(". Ambos sexos. De 25 a 54 años"):
            code = ine_ccaa(s.split(". ")[1])
            if code and code != "ES":
                by[code].append(r)
    assert len(by) == 20, sorted(by)
    out, p0, p1 = [], None, None
    for code, rs in by.items():
        v, p0, p1 = _last4(rs)
        prev = annual(rs)[START]
        out.append({"geo": code, "time": p1, "value": round(v, 1), "prev": round(prev, 1), "change": round(v - prev, 1)})
    es = next(r for r in out if r["geo"] == "ES")
    main = [r for r in out if r["geo"] not in ("ES", "18", "19")]
    up = [r for r in main if r["change"] > 0]
    top = max(main, key=lambda r: r["value"])
    low = min(main, key=lambda r: r["value"])
    most = max(main, key=lambda r: r["change"])
    o0, o1 = _ocupados_es()
    who = "las 17 comunidades" if len(up) == 17 else f"{len(up)} de las 17 comunidades"
    who_en = "all 17 regions" if len(up) == 17 else f"{len(up)} of the 17 regions"
    return chart(
        id="led3-tasa-empleo",
        lens="dentro", theme="legislatura",
        title=bi(f"Trabaja una proporción mayor de la población de 25 a 54 años en {who}: en España, el {es1(es['value'])} %, "
                 f"{es1(es['change'])} puntos más que en {START}",
                 f"A larger share of people aged 25 to 54 are in work in {who_en}: in Spain, {en1(es['value'])}%, "
                 f"{en1(es['change'])} points more than in {START}"),
        subtitle=bi(f"Tasa de empleo de 25 a 54 años, media de los cuatro trimestres del {_qlabel(p0)} al {_qlabel(p1)}, en %",
                    f"Employment rate aged 25 to 54, average of the four quarters from {_qlabel_en(p0)} to {_qlabel_en(p1)}, in %"),
        unit=bi("% de la población de 25 a 54 años", "% of the population aged 25 to 54"),
        source=INE_EMP_RATE,
        notes={"es": ["Ocupados de 25 a 54 años en % de la población de esa edad (EPA). A diferencia del número de ocupados, no sube "
                      "solo porque haya más población, y al dejar fuera a los jóvenes y a los mayores tampoco depende del envejecimiento.",
                      f"«prev» en la descarga: media de {START}; «change»: diferencia en puntos.",
                      f"Número de ocupados de todas las edades en España: {es1(o0 / 1000)} millones de media en {START} y {es1(o1 / 1000)} "
                      f"en el último año ({es1(pct(o0, o1))} %).",
                      f"Extremos (sin Ceuta ni Melilla): {geo.CCAA[top['geo']]}, {es1(top['value'])} %; {geo.CCAA[low['geo']]}, "
                      f"{es1(low['value'])} %. Mayor subida: {geo.CCAA[most['geo']]} ({es1(most['change'])} puntos).",
                      "La EPA es una encuesta: en las comunidades menos pobladas el error de muestreo es mayor y las diferencias pequeñas "
                      "entre ellas no son significativas. Ceuta y Melilla tienen muestras muy pequeñas."],
               "en": ["Employed people aged 25 to 54 as % of the population of that age (EPA). Unlike the number of people in work, "
                      "it does not rise just because the population grows, and by leaving out the young and the old it does not depend "
                      "on ageing either.",
                      f"«prev» in the download: {START} average; «change»: difference in points.",
                      f"Number of people in work of all ages in Spain: {en1(o0 / 1000)} million on average in {START} and {en1(o1 / 1000)} "
                      f"in the last year ({en1(pct(o0, o1))}%).",
                      f"Extremes (excluding Ceuta and Melilla): {nm(top['geo'])}, {en1(top['value'])}%; {nm(low['geo'])}, "
                      f"{en1(low['value'])}%. Largest rise: {nm(most['geo'])} ({en1(most['change'])} points).",
                      "The EPA is a survey: in the less populated regions the sampling error is larger and small differences between "
                      "them are not significant. Ceuta and Melilla have very small samples."]},
        rows=sorted(out, key=lambda r: r["geo"]),
        geos=geo.ccaa_table(r["geo"] for r in out),
    )


# ---------- España en el tiempo ----------

def crecimiento_tiempo():
    gdp, pc = _gdp()
    years = sorted(int(t) for g, t in gdp if g == "ES" and int(t) >= 2015 and ("ES", t) in pc)
    base = 2019
    series = {"pib": {y: gdp[("ES", str(y))] for y in years}, "per_capita": {y: pc[("ES", str(y))] for y in years}}
    series["poblacion"] = {y: series["pib"][y] * 1e6 / series["per_capita"][y] for y in years}
    rows = [{"time": str(y), "series": k, "value": round(100 * v[y] / v[base], 1)} for k, v in series.items() for y in years]
    last = years[-1]
    g = {k: pct(v[base], v[last]) for k, v in series.items()}
    g23 = {k: pct(v[START], v[last]) for k, v in series.items()}
    return chart(
        id="let4-crecimiento",
        lens="tiempo", theme="legislatura",
        title=bi(f"Desde {base}, el PIB ha crecido un {es1(g['pib'])} %: la mitad por la población, que sube un {es1(g['poblacion'])} %, "
                 f"y la otra mitad por el PIB por habitante ({es1(g['per_capita'])} %)"
                 if abs(g["poblacion"] - g["per_capita"]) <= 1 else
                 f"Desde {base}, el PIB ha crecido un {es1(g['pib'])} %; la población, un {es1(g['poblacion'])} %, y el PIB por habitante, "
                 f"un {es1(g['per_capita'])} %",
                 f"Since {base}, GDP has grown {en1(g['pib'])}%: half from population, up {en1(g['poblacion'])}%, "
                 f"and the other half from GDP per person ({en1(g['per_capita'])}%)"
                 if abs(g["poblacion"] - g["per_capita"]) <= 1 else
                 f"Since {base}, GDP has grown {en1(g['pib'])}%; population, {en1(g['poblacion'])}%, and GDP per person, "
                 f"{en1(g['per_capita'])}%"),
        subtitle=bi(f"PIB en volumen, población y PIB por habitante en volumen. Índices, {base} = 100, {years[0]}-{last}",
                    f"Real GDP, population and real GDP per person. Indices, {base} = 100, {years[0]}-{last}"),
        unit=bi(f"Índice ({base} = 100)", f"Index ({base} = 100)"),
        source=EUROSTAT_NA,
        notes={"es": ["PIB y PIB por habitante en volumen encadenado (euros de 2010); la población es el cociente de los dos, la que usa "
                      "Eurostat para el PIB por habitante.",
                      f"Base en {base}, el último año antes de la pandemia: la caída de 2020 y la recuperación posterior distorsionan las "
                      f"comparaciones con años intermedios.",
                      f"Desde {START}, año de las últimas generales: PIB {es1(g23['pib'])} %, población {es1(g23['poblacion'])} %, "
                      f"PIB por habitante {es1(g23['per_capita'])} %.",
                      f"Datos de {last} provisionales."],
               "en": ["GDP and GDP per person in chain-linked volumes (2010 euros); population is the ratio of the two, the one Eurostat "
                      "uses for GDP per person.",
                      f"Base year {base}, the last year before the pandemic: the 2020 fall and the recovery afterwards distort "
                      f"comparisons with the years in between.",
                      f"Since {START}, the year of the last general election: GDP {en1(g23['pib'])}%, population {en1(g23['poblacion'])}%, "
                      f"GDP per person {en1(g23['per_capita'])}%.",
                      f"{last} data provisional."]},
        rows=rows,
        extra={"dimensions": {"series": {"pib": bi("PIB", "GDP"), "poblacion": bi("Población", "Population"),
                                         "per_capita": bi("PIB por habitante", "GDP per person")}},
               "ref_line": {"value": 100, "label": bi(str(base), str(base))},
               "events": [{"time": START + 0.5, "label": bi("Elecciones generales (23 de julio de 2023)", "General election (23 July 2023)")}]},
    )


def salarios_precios():
    wage_name = ("Total Nacional. Industria, construcción y servicios (excepto actividades de los hogares como empleadores y de "
                 "organizaciones y organismos extraterritoriales). Coste salarial total. Costes laborales. Euros")
    wage = [r for r in sources.ine_table(WAGE_TABLE) if r["series"] == wage_name]
    cpi = [r for r in sources.ine_table(CPI_TABLE) if r["series"].startswith("Índice general. Índice")
           or r["series"].startswith("Nacional. Índice general. Índice")]
    assert wage and cpi, (len(wage), len(cpi))
    series = {"salarios": annual(wage), "precios": annual(cpi)}
    years = [y for y in sorted(set(series["salarios"]) & set(series["precios"])) if y >= 2015]
    rows = [{"time": str(y), "series": k, "value": round(100 * s[y] / s[START], 1)} for k, s in series.items() for y in years]
    last = years[-1]
    w, p = pct(series["salarios"][START], series["salarios"][last]), pct(series["precios"][START], series["precios"][last])
    real = pct(series["salarios"][START] / series["precios"][START], series["salarios"][last] / series["precios"][last])
    return chart(
        id="let2-salarios-precios",
        lens="tiempo", theme="legislatura",
        title=bi(f"Entre {START} y {last}, el salario medio sube un {es1(w)} % y los precios, un {es1(p)} %",
                 f"Between {START} and {last}, the average wage rises {en1(w)}% and prices {en1(p)}%"),
        subtitle=bi(f"Índices, {START} = 100. Salario medio por trabajador y precios de consumo, medias anuales desde 2015",
                    f"Indices, {START} = 100. Average wage per worker and consumer prices, annual averages since 2015"),
        unit=bi(f"Índice ({START} = 100)", f"Index ({START} = 100)"),
        source={**INE_WAGE, "also": [INE_CPI]},
        notes={"es": ["Salario: coste salarial total por trabajador y mes (industria, construcción y servicios), media anual. "
                      "Incluye pagas extra. Es una media: no dice cómo le ha ido al salario de cada persona.",
                      "Precios: IPC general, media anual.",
                      f"Descontada la inflación, el salario medio de {last} es un {es1(real)} % más alto que el de {START}.",
                      "Solo años completos."],
               "en": ["Wage: total wage cost per worker per month (industry, construction and services), annual average. "
                      "Includes extra payments. It is an average: it does not say how each person's wage has fared.",
                      "Prices: general CPI, annual average.",
                      f"Adjusted for inflation, the average wage in {last} is {en1(real)}% higher than in {START}.",
                      "Full years only."]},
        rows=rows,
        extra={"dimensions": {"series": {"salarios": bi("Salario medio", "Average wage"), "precios": bi("Precios (IPC)", "Prices (CPI)")}},
               "ref_line": {"value": 100, "label": bi(str(START), str(START))}},
    )


def ingresos_gastos():
    key = {"TR": "ingresos", "TE": "gastos"}
    raw = [r for na in key for r in sources.eurostat("gov_10a_main", na_item=na, sector="S13", unit="PC_GDP", geo="ES")]
    val = {(key[r["na_item"]], int(r["time"])): r["value"] for r in raw}
    years = sorted(y for (k, y) in val if k == "ingresos" and y >= 2008 and ("gastos", y) in val)
    rows = [{"time": str(y), "series": k, "value": round(val[(k, y)], 1)} for k in ("ingresos", "gastos") for y in years]
    last = years[-1]
    ing0, ing1, gas0, gas1 = val[("ingresos", START)], val[("ingresos", last)], val[("gastos", START)], val[("gastos", last)]
    d0, d1 = gas0 - ing0, gas1 - ing1
    lowest = min(years, key=lambda y: (val[("gastos", y)] - val[("ingresos", y)], -y))
    eu = {int(r["time"]): r["value"] for r in sources.eurostat("gov_10dd_edpt1", na_item="B9", sector="S13", unit="PC_GDP", geo="EU27_2020")}
    max_ing = max(years, key=lambda y: val[("ingresos", y)])
    return chart(
        id="let5-ingresos-gastos",
        lens="tiempo", theme="legislatura",
        title=bi(f"El déficit baja del {es1(d0)} % al {es1(d1)} % del PIB entre {START} y {last}: los ingresos suben del "
                 f"{es1(ing0)} % al {es1(ing1)} % y el gasto pasa del {es1(gas0)} % al {es1(gas1)} %",
                 f"The deficit falls from {en1(d0)}% to {en1(d1)}% of GDP between {START} and {last}: revenue rises from "
                 f"{en1(ing0)}% to {en1(ing1)}% and spending goes from {en1(gas0)}% to {en1(gas1)}%"),
        subtitle=bi(f"Ingresos y gastos de las administraciones públicas, en % del PIB, 2008-{last}. El déficit es la distancia entre las dos líneas",
                    f"General government revenue and spending, as % of GDP, 2008-{last}. The deficit is the gap between the two lines"),
        unit=bi("% del PIB", "% of GDP"),
        source={"name": "Eurostat", "dataset": "gov_10a_main", "url": "https://ec.europa.eu/eurostat/databrowser/view/gov_10a_main/default/table",
                "license": "CC BY 4.0"},
        notes={"es": ["Estado, comunidades, ayuntamientos y Seguridad Social, en contabilidad nacional. Ingresos: impuestos, cotizaciones "
                      "y otros ingresos; gastos: todos, también los intereses de la deuda.",
                      f"El déficit de {last} es el más bajo de la serie, que empieza en 2008." if lowest == last else
                      f"El déficit más bajo de la serie es el de {lowest}.",
                      f"Ingresos de {last}: {'el máximo de la serie' if max_ing == last else f'máximo de la serie en {max_ing}'}.",
                      f"Déficit de la media de la UE en {last}: {es1(-eu[last])} % del PIB.",
                      "Que suban los ingresos en % del PIB puede deberse a subidas de impuestos, a más empleo y beneficios o a que la "
                      "inflación eleve lo recaudado; los datos no separan esos efectos."],
               "en": ["Central government, regions, local councils and Social Security, in national accounts. Revenue: taxes, social "
                      "contributions and other revenue; spending: all of it, including interest on the debt.",
                      f"The {last} deficit is the lowest in the series, which starts in 2008." if lowest == last else
                      f"The lowest deficit in the series is that of {lowest}.",
                      f"Revenue in {last}: {'the highest in the series' if max_ing == last else f'highest in the series in {max_ing}'}.",
                      f"EU average deficit in {last}: {en1(-eu[last])}% of GDP.",
                      "Revenue rising as % of GDP can be due to tax rises, more jobs and profits, or inflation lifting tax takings; "
                      "the data does not separate those effects."]},
        rows=rows,
        extra={"dimensions": {"series": {"ingresos": bi("Ingresos", "Revenue"), "gastos": bi("Gastos", "Spending")}},
               "events": [{"time": START + 0.5, "label": bi("Elecciones generales (23 de julio de 2023)", "General election (23 July 2023)")}]},
    )


BUILDERS = [europa_paro, europa_crecimiento, europa_deuda, paro_comunidades, tasa_empleo_comunidades, crecimiento_tiempo,
            salarios_precios, ingresos_gastos]
