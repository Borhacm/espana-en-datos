"""Tema Educación (código ED): abandono temprano, PISA y nivel de estudios frente a Europa, comunidades, evolución y la ficha de la ley de FP."""

import statistics

from lib import geo, sources
from lib.output import THEMES, chart

from .common import bi, dec, ordinal_en

THEMES["educacion"] = {"code": "ED", "title": "Educación"}

EUROSTAT = {"name": "Eurostat", "license": "CC BY 4.0"}


def _src(dataset: str, label: str | None = None) -> dict:
    return {**EUROSTAT, "dataset": label or dataset, "url": f"https://ec.europa.eu/eurostat/databrowser/view/{dataset}/default/table"}


# Regiones NUTS 2 de Eurostat -> código de comunidad del INE
NUTS2 = {"ES61": "01", "ES24": "02", "ES12": "03", "ES53": "04", "ES70": "05", "ES13": "06", "ES41": "07", "ES42": "08",
         "ES51": "09", "ES52": "10", "ES43": "11", "ES11": "12", "ES30": "13", "ES62": "14", "ES22": "15", "ES21": "16",
         "ES23": "17", "ES63": "18", "ES64": "19", "ES": "ES"}
REGION_YEARS = ("2023", "2024", "2025")   # media de tres años: la muestra regional de la EPA es pequeña
SMALL = ("18", "19")                       # Ceuta y Melilla: muestra muy pequeña, no protagonizan titulares


def _eu_rows(raw: list[dict], year: str | None = None) -> tuple[list[dict], str]:
    """Una fila por país de la UE y otra para la media, en el último año con dato de la UE (o el pedido)."""
    year = year or sorted({r["time"] for r in raw if geo.from_eurostat(r["geo"]) == "EU27"})[-1]
    out = []
    for r in raw:
        c = geo.from_eurostat(r["geo"])
        if r["time"] == year and c and (c == "EU27" or geo.COUNTRIES.get(c, (0, 0, 0, False))[3]):
            out.append({"geo": c, "time": year, "value": round(r["value"], 1)})
    return sorted(out, key=lambda r: r["geo"]), year


def _rank(rows: list[dict], code: str = "ESP") -> int:
    ranked = sorted((r for r in rows if r["geo"] != "EU27"), key=lambda r: -r["value"])
    return [r["geo"] for r in ranked].index(code) + 1


def _val(rows: list[dict], code: str) -> float:
    return next(r["value"] for r in rows if r["geo"] == code)


def _regions(raw: list[dict]) -> list[dict]:
    """Media 2023-2025 de cada comunidad (con los años que haya) y del total de España."""
    by = {}
    for r in raw:
        code = NUTS2.get(r["geo"])
        if code and r["time"] in REGION_YEARS:
            by.setdefault(code, []).append(r["value"])
    return [{"geo": c, "time": f"{REGION_YEARS[0]}-{REGION_YEARS[-1]}", "value": round(sum(v) / len(v), 1), "years": len(v)}
            for c, v in sorted(by.items())]


def _name(code: str, lang: str) -> str:
    """Nombre de la comunidad con artículo cuando lo lleva en una frase («el País Vasco», «the Basque Country»)."""
    n = geo.ccaa_name(code, lang)
    if lang == "es":
        return "el " + n if code == "16" else n
    return "the " + n if code in ("04", "05", "16") else n


def _abandono() -> list[dict]:
    return sources.eurostat("edat_lfse_14", sex="T", wstatus="POP", age="Y18-24")


ABANDONO_NOTE = {
    "es": "Abandono temprano: jóvenes de 18 a 24 años que como mucho han terminado la ESO y no siguen estudiando ni formándose "
          "(Encuesta de Población Activa).",
    "en": "Early leavers: people aged 18 to 24 who have at most completed lower secondary education (ESO in Spain) and are not "
          "in education or training (Labour Force Survey).",
}


# ---------- España frente a Europa ----------

def europa_abandono():
    raw = _abandono()
    rows, year = _eu_rows(raw)
    es, eu = _val(rows, "ESP"), _val(rows, "EU27")
    n, rank = len(rows) - 1, _rank(rows)
    above = [geo.country_name(r["geo"], "es") for r in sorted(rows, key=lambda r: -r["value"]) if r["geo"] not in ("EU27", "ESP")][:rank - 1]
    above_en = [geo.country_name(r["geo"], "en") for r in sorted(rows, key=lambda r: -r["value"]) if r["geo"] not in ("EU27", "ESP")][:rank - 1]
    # Qué hacen los que abandonan: trabajan o no
    work = sources.eurostat("edat_lfse_14", sex="T", wstatus=["EMP", "NEMP"], age="Y18-24")
    w = {(geo.from_eurostat(r["geo"]), r["wstatus"]): r["value"] for r in work if r["time"] == year}
    return chart(
        id="ede1-europa-abandono",
        lens="europa", theme="educacion",
        title=bi(f"El {dec(es, 'es')} % de los jóvenes españoles deja los estudios sin pasar de la ESO; en la UE, el {dec(eu, 'es')} %",
                 f"{dec(es, 'en')}% of young Spaniards leave education with no more than lower secondary; in the EU, {dec(eu, 'en')}%"),
        subtitle=bi(f"Abandono temprano de la educación y la formación, jóvenes de 18 a 24 años, {year}, en %. "
                    f"España es el {rank}.º de {n} países",
                    f"Early leavers from education and training, aged 18 to 24, {year}, in %. Spain ranks {ordinal_en(rank)} of {n} countries"),
        unit=bi("% de los jóvenes de 18 a 24 años", "% of people aged 18 to 24"),
        source=_src("edat_lfse_14"),
        notes={"es": [ABANDONO_NOTE["es"],
                      f"En España, el {dec(w[('ESP', 'EMP')], 'es')} % de los jóvenes de 18 a 24 años ha abandonado y trabaja, y el "
                      f"{dec(w[('ESP', 'NEMP')], 'es')} % ha abandonado y no trabaja; en la UE, el {dec(w[('EU27', 'EMP')], 'es')} % y el "
                      f"{dec(w[('EU27', 'NEMP')], 'es')} %.",
                      "Eurostat advierte de que la definición de España y Francia difiere ligeramente de la común."],
               "en": [ABANDONO_NOTE["en"],
                      f"In Spain, {dec(w[('ESP', 'EMP')], 'en')}% of people aged 18 to 24 have left early and are working, and "
                      f"{dec(w[('ESP', 'NEMP')], 'en')}% have left early and are not working; in the EU, {dec(w[('EU27', 'EMP')], 'en')}% "
                      f"and {dec(w[('EU27', 'NEMP')], 'en')}%.",
                      "Eurostat notes that the definition used for Spain and France differs slightly from the common one."]},
        rows=rows,
        geos=geo.country_table(r["geo"] for r in rows),
        extra={"countries_above": bi(", ".join(above), ", ".join(above_en))},
    )


def europa_pisa():
    raw = sources.eurostat("sdg_04_40", sex="T", field=["EF461", "READ", "SCI"])
    maths = [r for r in raw if r["field"] == "EF461"]
    rows, year = _eu_rows(maths)
    es, eu = _val(rows, "ESP"), _val(rows, "EU27")
    n, rank = len(rows) - 1, _rank(rows)
    other = {f: {geo.from_eurostat(r["geo"]): r["value"] for r in raw if r["field"] == f and r["time"] == year} for f in ("READ", "SCI")}
    return chart(
        id="ede2-europa-pisa",
        lens="europa", theme="educacion",
        title=bi(f"En PISA {year}, uno de cada tres alumnos de 15 años no llega al nivel básico de matemáticas: "
                 f"el {dec(es, 'es')} % en España y el {dec(eu, 'es')} % en la UE",
                 f"In PISA {year}, one in three 15-year-olds falls short of the basic level in mathematics: "
                 f"{dec(es, 'en')}% in Spain and {dec(eu, 'en')}% in the EU"),
        subtitle=bi(f"Alumnos de 15 años por debajo del nivel 2 de PISA en matemáticas, {year}, en %. España es el {rank}.º de {n} países",
                    f"15-year-old pupils below PISA level 2 in mathematics, {year}, in %. Spain ranks {ordinal_en(rank)} of {n} countries"),
        unit=bi("% de los alumnos de 15 años", "% of 15-year-old pupils"),
        source=_src("sdg_04_40", "sdg_04_40 (PISA)"),
        notes={"es": ["PISA (OCDE) evalúa a alumnos de 15 años, estén en el curso que estén. El nivel 2 es el que la OCDE considera "
                      "básico para desenvolverse; por debajo, el alumno no resuelve problemas sencillos fuera de un contexto conocido.",
                      f"En lectura, por debajo del nivel 2 está el {dec(other['READ']['ESP'], 'es')} % en España y el "
                      f"{dec(other['READ']['EU27'], 'es')} % en la UE; en ciencias, el {dec(other['SCI']['ESP'], 'es')} % y el "
                      f"{dec(other['SCI']['EU27'], 'es')} %.",
                      "Es una muestra de alumnos: las diferencias pequeñas entre países no son significativas."],
               "en": ["PISA (OECD) tests 15-year-old pupils, whatever school year they are in. Level 2 is what the OECD considers the "
                      "baseline; below it, pupils cannot solve simple problems outside a familiar context.",
                      f"In reading, {dec(other['READ']['ESP'], 'en')}% are below level 2 in Spain and "
                      f"{dec(other['READ']['EU27'], 'en')}% in the EU; in science, {dec(other['SCI']['ESP'], 'en')}% and "
                      f"{dec(other['SCI']['EU27'], 'en')}%.",
                      "It is a sample of pupils: small differences between countries are not significant."]},
        rows=rows,
        geos=geo.country_table(r["geo"] for r in rows),
    )


def europa_nivel():
    raw = sources.eurostat("edat_lfse_03", sex="T", age="Y25-34", isced11=["ED0-2", "ED3_4", "ED35_45", "ED5-8"])
    by = {k: [r for r in raw if r["isced11"] == k] for k in ("ED0-2", "ED3_4", "ED35_45", "ED5-8")}
    rows, year = _eu_rows(by["ED3_4"])
    lv = {k: {r["geo"]: r["value"] for r in _eu_rows(v, year)[0]} for k, v in by.items()}
    es, eu = lv["ED3_4"]["ESP"], lv["ED3_4"]["EU27"]
    n, rank = len(rows) - 1, _rank(rows)
    low_rank = n + 1 - rank
    return chart(
        id="ede3-europa-nivel",
        lens="europa", theme="educacion",
        title=bi(f"Solo para el {dec(es, 'es')} % de los españoles de 25 a 34 años el título más alto es el bachillerato o la FP de grado medio; "
                 f"en la UE, el {dec(eu, 'es')} %",
                 f"Only {dec(es, 'en')}% of Spaniards aged 25 to 34 have upper secondary (bachillerato or intermediate vocational "
                 f"training) as their highest qualification; in the EU, {dec(eu, 'en')}%"),
        subtitle=bi(f"Población de 25 a 34 años cuyo nivel más alto es el medio, {year}, en %. "
                    + ("España es la última de la UE" if low_rank == 1 else f"España es la {low_rank}.ª por la cola de {n}"),
                    f"Population aged 25 to 34 whose highest level is upper secondary, {year}, in %. "
                    + ("Spain is last in the EU" if low_rank == 1 else f"Spain is {ordinal_en(low_rank)} from the bottom of {n}")),
        unit=bi("% de la población de 25 a 34 años", "% of population aged 25 to 34"),
        source=_src("edat_lfse_03"),
        notes={"es": [f"El resto se reparte entre los dos extremos. Como mucho la ESO: {dec(lv['ED0-2']['ESP'], 'es')} % en España y "
                      f"{dec(lv['ED0-2']['EU27'], 'es')} % en la UE. Estudios superiores: {dec(lv['ED5-8']['ESP'], 'es')} % y "
                      f"{dec(lv['ED5-8']['EU27'], 'es')} %.",
                      "Nivel medio: bachillerato, FP de grado medio y estudios postsecundarios no superiores. La FP de grado superior "
                      "cuenta como estudios superiores."],
               "en": [f"The rest is split between the two extremes. Lower secondary at most: {dec(lv['ED0-2']['ESP'], 'en')}% in Spain and "
                      f"{dec(lv['ED0-2']['EU27'], 'en')}% in the EU. Tertiary education: {dec(lv['ED5-8']['ESP'], 'en')}% and "
                      f"{dec(lv['ED5-8']['EU27'], 'en')}%.",
                      "Upper secondary level: bachillerato, intermediate vocational training and post-secondary non-tertiary studies. "
                      "Higher vocational training counts as tertiary education."]},
        rows=rows,
        geos=geo.country_table(r["geo"] for r in rows),
        extra={"levels": {k: {"ESP": v["ESP"], "EU27": v["EU27"]} for k, v in lv.items()}},
    )


# ---------- España por dentro ----------

def comunidades():
    ab = _regions(sources.eurostat("edat_lfse_16", sex="T", age="Y18-24"))
    sup = _regions(sources.eurostat("edat_lfse_04", sex="T", age="Y25-34", isced11="ED5-8"))
    period = f"{REGION_YEARS[0]}-{REGION_YEARS[-1]}"
    region_note = {
        "es": f"Media de {REGION_YEARS[0]} a {REGION_YEARS[-1]}: la muestra de la EPA en cada comunidad es pequeña y el dato de un "
              "solo año varía mucho. Ceuta y Melilla tienen muy pocas observaciones; en algún año Eurostat no publica su dato.",
        "en": f"Average from {REGION_YEARS[0]} to {REGION_YEARS[-1]}: the Labour Force Survey sample in each region is small and a "
              "single year's figure varies a lot. Ceuta and Melilla have very few observations; in some years Eurostat does not "
              "publish their figure.",
    }
    main_ab = [r for r in ab if r["geo"] not in ("ES", *SMALL)]
    top, low = max(main_ab, key=lambda r: r["value"]), min(main_ab, key=lambda r: r["value"])
    es_ab = _val(ab, "ES")
    d1 = chart(
        id="edd1-comunidades-abandono",
        lens="dentro", theme="educacion",
        title=bi(f"El abandono temprano va del {dec(low['value'], 'es')} % en {_name(low['geo'], 'es')} al "
                 f"{dec(top['value'], 'es')} % en {_name(top['geo'], 'es')}",
                 f"Early school leaving ranges from {dec(low['value'], 'en')}% in {_name(low['geo'], 'en')} to "
                 f"{dec(top['value'], 'en')}% in {_name(top['geo'], 'en')}"),
        subtitle=bi(f"Abandono temprano de la educación y la formación, 18 a 24 años, media {period}, en %. España: {dec(es_ab, 'es')} %",
                    f"Early leavers from education and training, aged 18 to 24, {period} average, in %. Spain: {dec(es_ab, 'en')}%"),
        unit=bi("% de los jóvenes de 18 a 24 años", "% of people aged 18 to 24"),
        source=_src("edat_lfse_16"),
        notes={"es": [ABANDONO_NOTE["es"], region_note["es"],
                      "Se cuenta a los jóvenes donde viven, no donde estudiaron."],
               "en": [ABANDONO_NOTE["en"], region_note["en"],
                      "Young people are counted where they live, not where they studied."]},
        rows=ab,
        geos=geo.ccaa_table(r["geo"] for r in ab),
    )
    main_sup = [r for r in sup if r["geo"] not in ("ES", *SMALL)]
    stop, slow = max(main_sup, key=lambda r: r["value"]), min(main_sup, key=lambda r: r["value"])
    es_sup = _val(sup, "ES")
    # Relación entre las dos variables en las 17 comunidades
    sv = {r["geo"]: r["value"] for r in main_sup}
    pairs = [(r["value"], sv[r["geo"]]) for r in main_ab if r["geo"] in sv]
    corr = statistics.correlation([a for a, _ in pairs], [b for _, b in pairs])
    d2 = chart(
        id="edd2-comunidades-superiores",
        lens="dentro", theme="educacion",
        title=bi(f"En {_name(stop['geo'], 'es')}, el {dec(stop['value'], 'es')} % de los adultos jóvenes tiene estudios superiores; "
                 f"en {_name(slow['geo'], 'es')}, el {dec(slow['value'], 'es')} %",
                 f"In {_name(stop['geo'], 'en')}, {dec(stop['value'], 'en')}% of young adults have a tertiary qualification; "
                 f"in {_name(slow['geo'], 'en')}, {dec(slow['value'], 'en')}%"),
        subtitle=bi(f"Población de 25 a 34 años con estudios superiores (universidad o FP de grado superior), media {period}, en %. "
                    f"España: {dec(es_sup, 'es')} %",
                    f"Population aged 25 to 34 with tertiary education (university or higher vocational training), {period} average, "
                    f"in %. Spain: {dec(es_sup, 'en')}%"),
        unit=bi("% de la población de 25 a 34 años", "% of population aged 25 to 34"),
        source=_src("edat_lfse_04"),
        notes={"es": [region_note["es"],
                      "Se cuenta a las personas donde viven, no donde estudiaron: las comunidades que atraen a titulados de otras salen "
                      "con una tasa más alta."],
               "en": [region_note["en"],
                      "People are counted where they live, not where they studied: regions that attract graduates from elsewhere show "
                      "a higher rate."]},
        rows=sup,
        geos=geo.ccaa_table(r["geo"] for r in sup),
        extra={"correlation_abandono": round(corr, 3)},
    )
    return [d1, d2]


# ---------- España en el tiempo ----------

def tiempo_abandono():
    raw = _abandono()
    FIRST = 2002   # primer año con media de la UE
    s = {k: {int(r["time"]): r["value"] for r in raw if geo.from_eurostat(r["geo"]) == c and int(r["time"]) >= FIRST}
         for k, c in (("espana", "ESP"), ("ue", "EU27"))}
    years = sorted(set(s["espana"]) & set(s["ue"]))
    last = years[-1]
    peak = max(years, key=lambda y: s["espana"][y])
    gap_peak, gap_last = s["espana"][peak] - s["ue"][peak], s["espana"][last] - s["ue"][last]
    rows = [{"time": str(y), "series": k, "value": s[k][y]} for k in ("espana", "ue") for y in years]
    first_all = min(int(r["time"]) for r in raw if r["geo"] == "ES")
    v_first = next(r["value"] for r in raw if r["geo"] == "ES" and int(r["time"]) == first_all)
    breaks = [r["time"] for r in sorted(raw, key=lambda r: r["time"]) if r["geo"] == "ES" and "b" in r["flag"] and int(r["time"]) >= FIRST]
    br_es = ", ".join(breaks[:-1]) + " y " + breaks[-1] if len(breaks) > 1 else "".join(breaks)
    br_en = ", ".join(breaks[:-1]) + " and " + breaks[-1] if len(breaks) > 1 else "".join(breaks)
    return chart(
        id="edt1-abandono",
        lens="tiempo", theme="educacion",
        title=bi(f"El abandono temprano ha caído a menos de la mitad desde {peak} y la distancia con la UE se ha reducido de "
                 f"{dec(gap_peak, 'es')} a {dec(gap_last, 'es')} puntos",
                 f"Early school leaving has fallen by more than half since {peak} and the gap with the EU has narrowed from "
                 f"{dec(gap_peak, 'en')} to {dec(gap_last, 'en')} points"),
        subtitle=bi(f"Abandono temprano de la educación y la formación, 18 a 24 años, {FIRST}-{last}, en %",
                    f"Early leavers from education and training, aged 18 to 24, {FIRST}-{last}, in %"),
        unit=bi("% de los jóvenes de 18 a 24 años", "% of people aged 18 to 24"),
        source=_src("edat_lfse_14"),
        notes={"es": [ABANDONO_NOTE["es"],
                      f"La serie de España empieza en {first_all}, con un {dec(v_first, 'es')} %; la media de la UE, en {FIRST}.",
                      f"Eurostat marca rupturas de serie en España en {br_es} por cambios en la encuesta."],
               "en": [ABANDONO_NOTE["en"],
                      f"The series for Spain starts in {first_all}, at {dec(v_first, 'en')}%; the EU average, in {FIRST}.",
                      f"Eurostat flags breaks in the series for Spain in {br_en} owing to changes in the survey."]},
        rows=rows,
        extra={"dimensions": {"series": {"espana": bi("España", "Spain"), "ue": bi("UE", "EU")}},
               "peak": {"year": peak, "espana": s["espana"][peak], "ue": s["ue"][peak]}},
    )


def tiempo_origen():
    raw = sources.eurostat("edat_lfse_02", sex="T", wstatus="POP", age="Y18-24", c_birth=["NAT", "FOR", "TOTAL"])
    s = {k: {int(r["time"]): r["value"] for r in raw if r["geo"] == "ES" and r["c_birth"] == k} for k in ("NAT", "FOR", "TOTAL")}
    years = sorted(set(s["NAT"]) & set(s["FOR"]) & set(s["TOTAL"]))
    first, last = years[0], years[-1]

    def share(y):
        """Peso de los nacidos fuera entre los jóvenes de 18 a 24 años, deducido de las tres tasas: total = p·fuera + (1 - p)·España."""
        return (s["TOTAL"][y] - s["NAT"][y]) / (s["FOR"][y] - s["NAT"][y])

    p0, p1 = share(first), share(last)
    # Si el peso de los nacidos fuera no hubiera cambiado, con las tasas de hoy
    fixed = p0 * s["FOR"][last] + (1 - p0) * s["NAT"][last]
    rows = [{"time": str(y), "series": k.lower(), "value": s[k][y]} for k in ("NAT", "FOR") for y in years]
    n, f = s["NAT"], s["FOR"]
    return chart(
        id="edt2-abandono-origen",
        lens="tiempo", theme="educacion",
        title=bi(f"Desde {first}, el abandono baja del {dec(n[first], 'es')} % al {dec(n[last], 'es')} % entre los nacidos en España "
                 f"y del {dec(f[first], 'es')} % al {dec(f[last], 'es')} % entre los nacidos fuera",
                 f"Since {first}, early leaving has fallen from {dec(n[first], 'en')}% to {dec(n[last], 'en')}% among those born in Spain "
                 f"and from {dec(f[first], 'en')}% to {dec(f[last], 'en')}% among those born abroad"),
        subtitle=bi(f"Abandono temprano de la educación y la formación, 18 a 24 años, por lugar de nacimiento, {first}-{last}, en %",
                    f"Early leavers from education and training, aged 18 to 24, by country of birth, {first}-{last}, in %"),
        unit=bi("% de los jóvenes de 18 a 24 años", "% of people aged 18 to 24"),
        source=_src("edat_lfse_02"),
        notes={"es": ["El peso de los nacidos fuera entre los jóvenes de 18 a 24 años se deduce de las tres tasas publicadas: la total "
                      "es la media de las otras dos ponderada por ese peso. Es una aproximación: las tasas están redondeadas.",
                      "Nacidos fuera incluye a quienes llegaron de niños y estudiaron en España y a quienes llegaron ya con 18 años o más.",
                      "La muestra de nacidos fuera es más pequeña y su tasa varía más de un año a otro."],
               "en": ["The share of people born abroad among those aged 18 to 24 is derived from the three published rates: the total "
                      "is the average of the other two weighted by that share. It is an approximation: the rates are rounded.",
                      "Born abroad includes those who arrived as children and went to school in Spain and those who arrived aged 18 "
                      "or older.",
                      "The sample of people born abroad is smaller and their rate varies more from year to year."]},
        rows=rows,
        extra={"dimensions": {"series": {"nat": bi("Nacidos en España", "Born in Spain"), "for": bi("Nacidos fuera", "Born abroad")}},
               "short_labels": {"nat": bi("Nativos", "Natives"), "for": bi("Fuera", "Abroad")},
               "foreign_share": {str(first): round(p0, 3), str(last): round(p1, 3)}, "fixed_mix_total": round(fixed, 1)},
    )


def tiempo_fp_dual():
    raw = sources.eurostat("educ_uoe_enrs04", sex="T", sector="TOT_SEC", worktime="TOTAL", isced11=["ED35", "ED3SW"])
    FIRST = 2015   # primer año con dato de la UE
    v = {(geo.from_eurostat(r["geo"]), r["isced11"], int(r["time"])): r["value"] for r in raw}
    rows = []
    for k, c in (("espana", "ESP"), ("ue", "EU27")):
        for y in sorted({y for (cc, i, y) in v if cc == c and i == "ED3SW" and y >= FIRST}):
            if (c, "ED35", y) in v:
                rows.append({"time": str(y), "series": k, "value": round(100 * v[(c, "ED3SW", y)] / v[(c, "ED35", y)], 1)})
    last = max(int(r["time"]) for r in rows if r["series"] == "espana")
    es = next(r["value"] for r in rows if r["series"] == "espana" and r["time"] == str(last))
    eu = next(r["value"] for r in rows if r["series"] == "ue" and r["time"] == str(last))
    course = f"{last}-{last + 1}"
    return chart(
        id="edt3-fp-dual",
        lens="tiempo", theme="educacion",
        title=bi(f"En el curso {course}, solo el {dec(es, 'es')} % de los alumnos de FP de grado básico y medio estudiaba en programas que "
                 f"combinan centro y empresa; en la UE, el {dec(eu, 'es')} %",
                 f"In the {course} school year, only {dec(es, 'en')}% of basic and intermediate vocational students were in programmes "
                 f"combining school and workplace; in the EU, {dec(eu, 'en')}%"),
        subtitle=bi(f"Alumnos de FP de secundaria superior en programas combinados de centro y empresa, en % de los alumnos de FP de ese "
                    f"nivel. Cursos {FIRST}-{FIRST + 1} a {course}",
                    f"Upper-secondary vocational students in combined school- and work-based programmes, as % of vocational students "
                    f"at that level. School years {FIRST}-{FIRST + 1} to {course}"),
        unit=bi("% de los alumnos de FP", "% of vocational students"),
        source=_src("educ_uoe_enrs04"),
        notes={"es": ["Programas combinados: los que reparten la formación entre el centro y la empresa, como la FP dual o el aprendizaje. "
                      "Cada país decide qué programas clasifica así.",
                      "FP de secundaria superior: en España, sobre todo la FP de grado básico y de grado medio. La FP de grado superior "
                      "no está incluida.",
                      "Eurostat fecha cada curso por el año en que empieza."],
               "en": ["Combined programmes: those that split training between the school and the workplace, such as dual vocational "
                      "training or apprenticeships. Each country decides which programmes it classifies this way.",
                      "Upper-secondary vocational training: in Spain, mainly basic and intermediate vocational training. Higher "
                      "vocational training is not included.",
                      "Eurostat dates each school year by the year in which it starts."]},
        rows=rows,
        extra={"dimensions": {"series": {"espana": bi("España", "Spain"), "ue": bi("UE", "EU")}}},
    )


BUILDERS = [europa_abandono, europa_pisa, europa_nivel, comunidades, tiempo_abandono, tiempo_origen, tiempo_fp_dual]
