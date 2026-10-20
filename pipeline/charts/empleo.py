"""Tema Empleo (código EM): temporalidad, fijos discontinuos, paro juvenil y de larga duración, y la ficha de la reforma laboral de 2021.

Referencia: 2021, el último año completo antes de la reforma (Real Decreto-ley 32/2021; los cambios de contratos rigen desde el
30 de marzo de 2022). Grupo de comparación de la ficha: el sector público, al que la reforma de los contratos afecta mucho menos.
"""

from collections import defaultdict

from lib import geo, sources
from lib.output import THEMES, chart

from .common import annual, bi, ine_ccaa, ordinal_en
from .legislatura import _eu_rank, _last4, _place, _qlabel, _qlabel_en, _qtime, de, en1, es1, nm

THEMES["empleo"] = {"code": "EM", "title": "Empleo: la reforma laboral, tres años después"}

BASE = 2021             # último año completo antes de la reforma
PRIV_TABLE = 65195      # INE, EPA: asalariados del sector privado por tipo de contrato (trimestral)
PUB_TABLE = 65196       # INE, EPA: asalariados del sector público por tipo de contrato (trimestral)
CCAA_TABLE = 65329      # INE, EPA: asalariados del sector privado por tipo de contrato y comunidad (trimestral)
LTU_TABLE = 65340       # INE, EPA: parados por tiempo de búsqueda de empleo y comunidad, % (trimestral)

INE_EPA = {"name": "INE, Encuesta de Población Activa", "dataset": f"Tablas {PRIV_TABLE} y {PUB_TABLE}",
           "url": f"https://www.ine.es/jaxiT3/Tabla.htm?t={PRIV_TABLE}", "license": "Reutilización libre citando la fuente",
           "also": [{"name": "Sector público", "url": f"https://www.ine.es/jaxiT3/Tabla.htm?t={PUB_TABLE}"}]}
EVENTS = [
    {"time": 2022.0, "label": bi("Reforma laboral: Real Decreto-ley 32/2021 (diciembre de 2021)",
                                 "Labour reform: Royal Decree-law 32/2021 (December 2021)")},
    {"time": 2022.23, "label": bi("Rigen los nuevos contratos (30 de marzo de 2022)", "The new contract rules apply (30 March 2022)")},
]


def _eu_countries(rows: list[dict]) -> list[dict]:
    return [r for r in rows if r["geo"] == "EU27" or geo.COUNTRIES.get(r["geo"], (0, 0, 0, False))[3]]


def _ordinal(n: int) -> str:
    return "el más alto" if n == 1 else f"el {n}.º más alto"


def _ordinal_en(n: int) -> str:
    return "the highest" if n == 1 else f"the {ordinal_en(n)} highest"


# ---------- España frente a Europa ----------

def europa_temporalidad():
    raw = sources.eurostat("lfsi_pt_a", wstatus="EMP_TEMP", sex="T", age="Y15-64", unit="PC_SAL")
    last = max(r["time"] for r in raw if geo.from_eurostat(r["geo"]) == "EU27")
    out = _eu_rank(raw, last, str(BASE))
    es = next(r for r in out if r["geo"] == "ESP")
    eu = next(r for r in out if r["geo"] == "EU27")
    place = _place(out, "ESP")
    prev_place = _place([{**r, "value": r["prev"]} for r in out], "ESP")
    n = len(out) - 1
    return chart(
        id="eme1-europa-temporalidad",
        lens="europa", theme="empleo",
        title=bi(f"Los asalariados temporales bajan del {es1(es['prev'])} % al {es1(es['value'])} % en España entre {BASE} y {last}; "
                 f"en la UE, del {es1(eu['prev'])} % al {es1(eu['value'])} %",
                 f"Temporary employees fall from {en1(es['prev'])}% to {en1(es['value'])}% in Spain between {BASE} and {last}; "
                 f"in the EU, from {en1(eu['prev'])}% to {en1(eu['value'])}%"),
        subtitle=bi(f"Asalariados con contrato temporal, de 15 a 64 años, {last}, en % de los asalariados. "
                    f"España tenía en {BASE} el {prev_place}.º porcentaje más alto de {n} países; ahora, el {place}.º",
                    f"Employees on temporary contracts, aged 15 to 64, {last}, as % of employees. "
                    f"In {BASE} Spain had the {ordinal_en(prev_place)} highest share of {n} countries; now, the {ordinal_en(place)}"),
        unit=bi("% de los asalariados", "% of employees"),
        source={"name": "Eurostat", "dataset": "lfsi_pt_a", "url": "https://ec.europa.eu/eurostat/databrowser/view/lfsi_pt_a/default/table",
                "license": "CC BY 4.0"},
        notes={"es": ["Encuesta de Población Activa armonizada (para España, la EPA del INE), medias anuales.",
                      "Los fijos discontinuos cuentan como contratos indefinidos, no como temporales.",
                      f"«prev» en la descarga: porcentaje de {BASE}, el último año completo antes de la reforma laboral."],
               "en": ["Harmonised Labour Force Survey (for Spain, INE's EPA), annual averages.",
                      "Fijos discontinuos (permanent seasonal contracts) count as permanent contracts, not temporary ones.",
                      f"«prev» in the download: share in {BASE}, the last full year before the labour reform."]},
        rows=out,
        geos=geo.country_table(r["geo"] for r in out),
    )


def europa_paro_juvenil():
    raw = sources.eurostat("une_rt_a", age="Y15-24", sex="T", unit="PC_ACT")
    last = max(r["time"] for r in raw if geo.from_eurostat(r["geo"]) == "EU27")
    out = _eu_rank(raw, last, str(BASE))
    es = next(r for r in out if r["geo"] == "ESP")
    eu = next(r for r in out if r["geo"] == "EU27")
    place = _place(out, "ESP")
    n = len(out) - 1
    missing = sorted(c for c, v in geo.COUNTRIES.items() if v[3] and c not in {r["geo"] for r in out})
    return chart(
        id="eme2-europa-paro-juvenil",
        lens="europa", theme="empleo",
        title=bi(f"El paro de los menores de 25 años baja del {es1(es['prev'])} % al {es1(es['value'])} % entre {BASE} y {last}, "
                 f"el doble que en la UE ({es1(eu['value'])} %)" if es["value"] / eu["value"] >= 1.95 else
                 f"El paro de los menores de 25 años baja del {es1(es['prev'])} % al {es1(es['value'])} % entre {BASE} y {last}; "
                 f"en la UE es del {es1(eu['value'])} %",
                 f"Unemployment among under-25s falls from {en1(es['prev'])}% to {en1(es['value'])}% between {BASE} and {last}, "
                 f"twice the EU rate ({en1(eu['value'])}%)" if es["value"] / eu["value"] >= 1.95 else
                 f"Unemployment among under-25s falls from {en1(es['prev'])}% to {en1(es['value'])}% between {BASE} and {last}; "
                 f"in the EU it is {en1(eu['value'])}%"),
        subtitle=bi(f"Tasa de paro de 15 a 24 años, {last}, en % de la población activa de esa edad. "
                    f"España es {_ordinal(place)} de {n} países",
                    f"Unemployment rate aged 15 to 24, {last}, as % of the labour force of that age. "
                    f"Spain is {_ordinal_en(place)} of {n} countries"),
        unit=bi("% de la población activa de 15 a 24 años", "% of the labour force aged 15 to 24"),
        source={"name": "Eurostat", "dataset": "une_rt_a", "url": "https://ec.europa.eu/eurostat/databrowser/view/une_rt_a/default/table",
                "license": "CC BY 4.0"},
        notes={"es": ["Medias anuales de la Encuesta de Población Activa armonizada. La tasa se calcula sobre los jóvenes que trabajan o "
                      "buscan empleo, no sobre todos los jóvenes: muchos estudian y no cuentan como activos.",
                      f"«prev» en la descarga: tasa de {BASE}."]
                     + ([f"Sin dato de {last} para: {', '.join(geo.COUNTRIES[c][1] for c in missing)}."] if missing else []),
               "en": ["Annual averages of the harmonised Labour Force Survey. The rate is calculated over young people who work or "
                      "are looking for work, not over all young people: many are studying and do not count as active.",
                      f"«prev» in the download: rate in {BASE}."]
                     + ([f"No {last} data for: {', '.join(geo.COUNTRIES[c][2] for c in missing)}."] if missing else [])},
        rows=out,
        geos=geo.country_table(r["geo"] for r in out),
    )


# ---------- España por dentro ----------

def temporalidad_comunidades():
    rows = sources.ine_table(CCAA_TABLE)
    by = defaultdict(list)
    for r in rows:
        parts = r["series"].split(". ")
        # «Asalariado sector privado. Total. <comunidad>. Temporal: Total. Porcentaje»
        if len(parts) == 5 and parts[1] == "Total" and parts[3] == "Temporal: Total" and parts[4] == "Porcentaje":
            code = ine_ccaa(parts[2])
            if code:
                by[code].append(r)
    assert len(by) == 20, sorted(by)
    out, p0, p1 = [], None, None
    for code, rs in by.items():
        v, p0, p1 = _last4(rs)
        prev = annual(rs)[BASE]
        out.append({"geo": code, "time": p1, "value": round(v, 1), "prev": round(prev, 1), "change": round(v - prev, 1)})
    es = next(r for r in out if r["geo"] == "ES")
    main = [r for r in out if r["geo"] not in ("ES", "18", "19")]
    down = [r for r in main if r["change"] < 0]
    top = max(main, key=lambda r: r["value"])
    low = min(main, key=lambda r: r["value"])
    who = "las 17 comunidades" if len(down) == 17 else f"{len(down)} de las 17 comunidades"
    who_en = "all 17 regions" if len(down) == 17 else f"{len(down)} of the 17 regions"
    return chart(
        id="emd1-temporalidad-comunidades",
        lens="dentro", theme="empleo",
        title=bi(f"En el sector privado, la temporalidad ha bajado desde {BASE} en {who}: hoy va del {es1(low['value'])} % "
                 f"{de(low['geo'])} al {es1(top['value'])} % {de(top['geo'])}",
                 f"In the private sector, the temporary employment rate has fallen since {BASE} in {who_en}: it now ranges from "
                 f"{en1(low['value'])}% in {nm(low['geo'])} to {en1(top['value'])}% in {nm(top['geo'])}"),
        subtitle=bi(f"Asalariados del sector privado con contrato temporal, media de los cuatro trimestres del {_qlabel(p0)} al "
                    f"{_qlabel(p1)}, en %. España: {es1(es['value'])} % ({es1(es['prev'])} % en {BASE})",
                    f"Private-sector employees on temporary contracts, average of the four quarters from {_qlabel_en(p0)} to "
                    f"{_qlabel_en(p1)}, in %. Spain: {en1(es['value'])}% ({en1(es['prev'])}% in {BASE})"),
        unit=bi("% de los asalariados del sector privado", "% of private-sector employees"),
        source={"name": "INE, Encuesta de Población Activa", "dataset": f"Tabla {CCAA_TABLE}",
                "url": f"https://www.ine.es/jaxiT3/Tabla.htm?t={CCAA_TABLE}", "license": "Reutilización libre citando la fuente"},
        notes={"es": ["Encuesta de Población Activa. Media de los últimos cuatro trimestres para evitar la estacionalidad (los contratos "
                      "temporales suben en verano).",
                      f"«prev» en la descarga: media de {BASE}; «change»: diferencia en puntos.",
                      "Los fijos discontinuos cuentan como contratos indefinidos.",
                      "La temporalidad depende mucho de la estructura productiva de cada comunidad (agricultura, turismo, industria).",
                      "Ceuta y Melilla tienen muestras pequeñas en la EPA y sus porcentajes varían mucho de un trimestre a otro."],
               "en": ["Labour Force Survey (EPA). Average of the last four quarters to avoid seasonality (temporary contracts "
                      "rise in summer).",
                      f"«prev» in the download: {BASE} average; «change»: difference in points.",
                      "Fijos discontinuos (permanent seasonal contracts) count as permanent contracts.",
                      "Temporary employment depends heavily on each region's economic structure (agriculture, tourism, industry).",
                      "Ceuta and Melilla have small samples in the EPA and their shares vary a lot from one quarter to the next."]},
        rows=sorted(out, key=lambda r: r["geo"]),
        geos=geo.ccaa_table(r["geo"] for r in out),
    )


def paro_larga_comunidades():
    rows = sources.ine_table(LTU_TABLE)
    LONG = ("De 1 año a menos de 2 años", "2 años o más")
    parts_by = defaultdict(lambda: defaultdict(float))
    for r in rows:
        parts = r["series"].split(". ")
        # «Parados. Ambos sexos. <comunidad>. <tiempo>. Porcentaje» o «Parados. Total Nacional. Ambos sexos. <tiempo>. Porcentaje»
        if len(parts) != 5 or parts[4] != "Porcentaje":
            continue
        if parts[1] == "Ambos sexos":
            name, dur = parts[2], parts[3]
        elif parts[1] == "Total Nacional" and parts[2] == "Ambos sexos":
            name, dur = "Total Nacional", parts[3]
        else:
            continue
        code = ine_ccaa(name)
        if code and dur in LONG:
            parts_by[code][(r["period"], r["year"])] += r["value"]
    by = {code: [{"period": p, "year": y, "value": v} for (p, y), v in d.items()] for code, d in parts_by.items()}
    assert len(by) == 20, sorted(by)
    out, p0, p1 = [], None, None
    for code, rs in by.items():
        v, p0, p1 = _last4(rs)
        prev = annual(rs)[BASE]
        out.append({"geo": code, "time": p1, "value": round(v, 1), "prev": round(prev, 1), "change": round(v - prev, 1)})
    es = next(r for r in out if r["geo"] == "ES")
    main = [r for r in out if r["geo"] not in ("ES", "18", "19")]
    top = max(main, key=lambda r: r["value"])
    low = min(main, key=lambda r: r["value"])
    return chart(
        id="emd2-paro-larga-comunidades",
        lens="dentro", theme="empleo",
        title=bi(f"El {es1(es['value'])} % de los parados lleva un año o más buscando empleo: del {es1(low['value'])} % "
                 f"{de(low['geo'])} al {es1(top['value'])} % {de(top['geo'])}",
                 f"{en1(es['value'])}% of the unemployed have been looking for work for a year or more: from {en1(low['value'])}% "
                 f"in {nm(low['geo'])} to {en1(top['value'])}% in {nm(top['geo'])}"),
        subtitle=bi(f"Parados que llevan un año o más buscando empleo, media de los cuatro trimestres del {_qlabel(p0)} al "
                    f"{_qlabel(p1)}, en % de los parados. España: {es1(es['prev'])} % en {BASE}",
                    f"Unemployed people looking for work for a year or more, average of the four quarters from {_qlabel_en(p0)} to "
                    f"{_qlabel_en(p1)}, as % of the unemployed. Spain: {en1(es['prev'])}% in {BASE}"),
        unit=bi("% de los parados", "% of the unemployed"),
        source={"name": "INE, Encuesta de Población Activa", "dataset": f"Tabla {LTU_TABLE}",
                "url": f"https://www.ine.es/jaxiT3/Tabla.htm?t={LTU_TABLE}", "license": "Reutilización libre citando la fuente"},
        notes={"es": ["Suma de los parados que llevan de uno a dos años buscando empleo y de los que llevan dos años o más, sobre el total "
                      "de parados de cada comunidad. Es un porcentaje de los parados, no de la población activa.",
                      f"«prev» en la descarga: media de {BASE}; «change»: diferencia en puntos.",
                      f"En {BASE} todavía pesaban los parados que perdieron el empleo con la pandemia de 2020: parte de la bajada desde "
                      "entonces es la salida de esa crisis.",
                      "Ceuta y Melilla tienen muestras pequeñas en la EPA y sus porcentajes varían mucho de un trimestre a otro."],
               "en": ["Sum of the unemployed who have been looking for work for one to two years and for two years or more, over all "
                      "the unemployed in each region. It is a share of the unemployed, not of the labour force.",
                      f"«prev» in the download: {BASE} average; «change»: difference in points.",
                      f"In {BASE} the people who lost their jobs in the 2020 pandemic still weighed heavily: part of the fall since "
                      "then is the recovery from that crisis.",
                      "Ceuta and Melilla have small samples in the EPA and their shares vary a lot from one quarter to the next."]},
        rows=sorted(out, key=lambda r: r["geo"]),
        geos=geo.ccaa_table(r["geo"] for r in out),
    )


# ---------- España en el tiempo (y ficha de la reforma) ----------

def _series(table: int, prefix: str, kind: str) -> list[dict]:
    rs = [r for r in sources.ine_table(table) if r["series"] == f"{prefix}. Total Nacional. Ambos sexos. {kind}. Porcentaje"]
    assert rs, (table, kind)
    return sorted(rs, key=lambda r: r["period"])


def temporalidad_sectores():
    priv = _series(PRIV_TABLE, "Asalariado sector privado", "Temporal: Total")
    pub = _series(PUB_TABLE, "Asalariado sector público", "Temporal: Total")
    rows = [{"time": _qtime(r["period"]), "series": k, "value": r["value"]}
            for k, rs in (("privado", priv), ("publico", pub)) for r in rs if r["year"] >= 2008]
    v_priv, p0, p1 = _last4(priv)
    v_pub, _, _ = _last4(pub)
    b_priv, b_pub = annual(priv)[BASE], annual(pub)[BASE]
    return chart(
        id="emt1-temporalidad-sectores",
        lens="tiempo", theme="empleo",
        title=bi(f"Entre {BASE} y el último año, la temporalidad del sector privado baja del {es1(b_priv)} % al {es1(v_priv)} %; "
                 f"en el público, del {es1(b_pub)} % al {es1(v_pub)} %",
                 f"Between {BASE} and the last year, the private sector's temporary employment rate falls from {en1(b_priv)}% to {en1(v_priv)}%; "
                 f"in the public sector, from {en1(b_pub)}% to {en1(v_pub)}%"),
        subtitle=bi(f"Asalariados con contrato temporal, en % de los asalariados de cada sector, trimestral desde 2008 hasta el {_qlabel(p1)}",
                    f"Employees on temporary contracts, as % of each sector's employees, quarterly from 2008 to {_qlabel_en(p1)}"),
        unit=bi("% de los asalariados", "% of employees"),
        source=INE_EPA,
        notes={"es": ["Encuesta de Población Activa, asalariados de 16 años y más. Datos trimestrales sin desestacionalizar.",
                      f"Titular: media de {BASE} frente a la media de los cuatro trimestres del {_qlabel(p0)} al {_qlabel(p1)}.",
                      "Los cambios de contratos de la reforma rigen para todos los empleadores, pero el empleo público temporal (interinos) "
                      "sigue sobre todo sus propias normas: la Ley 20/2021 de estabilización del empleo público se aprobó a la vez. "
                      "Por eso el sector público sirve de comparación, aunque imperfecta.",
                      "Los fijos discontinuos cuentan como contratos indefinidos."],
               "en": ["Labour Force Survey (EPA), employees aged 16 and over. Quarterly data, not seasonally adjusted.",
                      f"Headline: {BASE} average against the average of the four quarters from {_qlabel_en(p0)} to {_qlabel_en(p1)}.",
                      "The reform's contract rules apply to all employers, but temporary public employment (interim staff) "
                      "mostly follows its own rules: Law 20/2021 on stabilising public employment was passed at the same time. "
                      "That is why the public sector works as a comparison, if an imperfect one.",
                      "Fijos discontinuos (permanent seasonal contracts) count as permanent contracts."]},
        rows=rows,
        extra={"dimensions": {"series": {"privado": bi("Sector privado", "Private sector"), "publico": bi("Sector público", "Public sector")}},
               "quarterly": True, "events": EVENTS},
    )


def fijos_discontinuos():
    temp = _series(PRIV_TABLE, "Asalariado sector privado", "Temporal: Total")
    disc = _series(PRIV_TABLE, "Asalariado sector privado", "De duración indefinida: Discontinuo")
    by_p = {r["period"]: r for r in temp}
    both = [{"period": r["period"], "year": r["year"], "value": round(r["value"] + by_p[r["period"]]["value"], 1)}
            for r in disc if r["period"] in by_p]
    rows = [{"time": _qtime(r["period"]), "series": k, "value": r["value"]}
            for k, rs in (("temporal", temp), ("discontinuo", disc), ("suma", both)) for r in rs if r["year"] >= 2008]
    v = {k: _last4(rs)[0] for k, rs in (("temporal", temp), ("discontinuo", disc), ("suma", both))}
    b = {k: annual(rs)[BASE] for k, rs in (("temporal", temp), ("discontinuo", disc), ("suma", both))}
    _, p0, p1 = _last4(disc)
    return chart(
        id="emt2-fijos-discontinuos",
        lens="tiempo", theme="empleo",
        title=bi(f"Los fijos discontinuos pasan del {es1(b['discontinuo'])} % al {es1(v['discontinuo'])} % de los asalariados privados; "
                 f"sumados a los temporales, bajan del {es1(b['suma'])} % al {es1(v['suma'])} %",
                 f"Permanent seasonal workers rise from {en1(b['discontinuo'])}% to {en1(v['discontinuo'])}% of private employees; "
                 f"added to temporary workers, they fall from {en1(b['suma'])}% to {en1(v['suma'])}%"),
        subtitle=bi(f"Asalariados del sector privado con contrato temporal o fijo discontinuo, en %, trimestral desde 2008 hasta el {_qlabel(p1)}",
                    f"Private-sector employees on temporary or permanent seasonal contracts, in %, quarterly from 2008 to {_qlabel_en(p1)}"),
        unit=bi("% de los asalariados del sector privado", "% of private-sector employees"),
        source={**INE_EPA, "dataset": f"Tabla {PRIV_TABLE}", "also": []},
        notes={"es": ["Fijo discontinuo: contrato indefinido para trabajos de temporada o intermitentes. Entre periodos de actividad el "
                      "trabajador no cobra salario, pero conserva el contrato. Cuenta como indefinido.",
                      "La EPA pregunta a las personas por su contrato en la semana de referencia: un fijo discontinuo en un periodo sin "
                      "actividad puede aparecer como ocupado ausente o como parado según su situación, de ahí parte de la estacionalidad.",
                      f"Titular: media de {BASE} frente a la media de los cuatro trimestres del {_qlabel(p0)} al {_qlabel(p1)}.",
                      "«suma»: temporales más fijos discontinuos, para ver cuánto de la caída de la temporalidad se explica por el paso a "
                      "fijos discontinuos."],
               "en": ["Fijo discontinuo (permanent seasonal contract): a permanent contract for seasonal or intermittent work. Between "
                      "periods of activity the worker earns no wage but keeps the contract. It counts as permanent.",
                      "The EPA asks people about their contract in the reference week: a permanent seasonal worker in a period without "
                      "activity may appear as employed but absent or as unemployed depending on their situation, hence part of the seasonality.",
                      f"Headline: {BASE} average against the average of the four quarters from {_qlabel_en(p0)} to {_qlabel_en(p1)}.",
                      "«suma»: temporary plus permanent seasonal workers, to see how much of the fall in temporary employment is explained "
                      "by the shift to permanent seasonal contracts."]},
        rows=rows,
        extra={"dimensions": {"series": {"temporal": bi("Temporales", "Temporary"), "discontinuo": bi("Fijos discontinuos", "Permanent seasonal"),
                                         "suma": bi("Temporales + fijos discontinuos", "Temporary + permanent seasonal")}},
               "short_labels": {"temporal": bi("Temporales", "Temporary"), "discontinuo": bi("Fijos disc.", "Perm. seasonal"),
                                "suma": bi("Suma", "Sum")},
               "quarterly": True, "events": EVENTS},
    )


BUILDERS = [europa_temporalidad, europa_paro_juvenil, temporalidad_comunidades, paro_larga_comunidades,
            temporalidad_sectores, fijos_discontinuos]
