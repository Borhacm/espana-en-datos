"""Tema Jóvenes (código JO): emancipación frente a Europa, ninis y paro por estudios en las comunidades, evolución de
la convivencia con los padres y de la tenencia de la vivienda, y la ficha de la ayuda al alquiler para jóvenes."""

from lib import geo, sources
from lib.output import THEMES, chart

from .common import bi, dec
from .educacion import NUTS2, REGION_YEARS, SMALL, _eu_rows, _name, _regions, _src, _val

THEMES["jovenes"] = {"code": "JO", "title": "Jóvenes"}

ECV_TENURE_TABLE = 9994   # INE, ECV: hogares por régimen de tenencia y edad de la persona de referencia
INE_ECV = {"name": "INE, Encuesta de Condiciones de Vida", "dataset": f"Tabla {ECV_TENURE_TABLE}",
           "url": f"https://www.ine.es/jaxiT3/Tabla.htm?t={ECV_TENURE_TABLE}", "license": "Reutilización libre citando la fuente"}

SILC_NOTE = {
    "es": "Encuesta de Condiciones de Vida (EU-SILC). «Vivir con los padres»: residir en el mismo hogar que al menos uno de "
          "ellos, aunque se aporten ingresos al hogar.",
    "en": "EU Survey on Income and Living Conditions (EU-SILC). «Living with parents»: living in the same household as at least "
          "one of them, even if contributing income to the household.",
}


# ---------- España frente a Europa ----------

def europa_edad():
    raw = sources.eurostat("yth_demo_030", sex="T")
    rows, year = _eu_rows(raw)
    es, eu = _val(rows, "ESP"), _val(rows, "EU27")
    n = len(rows) - 1
    above = sorted(r["geo"] for r in rows if r["geo"] not in ("EU27", "ESP") and r["value"] > es)
    tied = sorted(r["geo"] for r in rows if r["geo"] not in ("EU27", "ESP") and r["value"] == es)
    first = {r["time"]: r["value"] for r in raw if r["geo"] == "ES"}
    first_eu = {r["time"]: r["value"] for r in raw if r["geo"] == "EU27_2020"}
    y0 = min(set(first) & set(first_eu))
    return chart(
        id="joe1-europa-edad",
        lens="europa", theme="jovenes",
        title=bi(f"Los jóvenes españoles se van de casa de sus padres a los {dec(es, 'es')} años de media, "
                 f"{dec(es - eu, 'es')} años más tarde que la media de la UE",
                 f"Young Spaniards leave their parents' home at {dec(es, 'en')} on average, "
                 f"{dec(es - eu, 'en')} years later than the EU average"),
        subtitle=bi(f"Edad media estimada a la que los jóvenes dejan el hogar de sus padres, {year}, en años. "
                    f"Solo en {len(above)} países de la UE se van más tarde",
                    f"Estimated average age at which young people leave the parental household, {year}, in years. "
                    f"Only in {len(above)} EU countries do they leave later"),
        unit=bi("años", "years"),
        source=_src("yth_demo_030"),
        notes={"es": ["Estimación de Eurostat a partir de la Encuesta de Población Activa de cada país: edad a la que el 50 % de "
                      "los jóvenes ya no vive en el hogar de sus padres.",
                      f"En {y0}, la edad era de {dec(first[y0], 'es')} años en España y de {dec(first_eu[y0], 'es')} en la UE."],
               "en": ["Eurostat estimate based on each country's Labour Force Survey: the age at which 50% of young people no "
                      "longer live in their parents' household.",
                      f"In {y0}, the age was {dec(first[y0], 'en')} in Spain and {dec(first_eu[y0], 'en')} in the EU."]},
        rows=rows,
        geos=geo.country_table(r["geo"] for r in rows),
        extra={"countries_above": above, "countries_tied": tied, "first_year": y0,
               "first": {"ESP": first[y0], "EU27": first_eu[y0]}},
    )


STATUS = {
    "EMP_FT": bi("Tiempo completo", "Full-time job"),
    "EMP_PT": bi("Tiempo parcial", "Part-time job"),
    "UNE": bi("En paro", "Unemployed"),
    "EDUC": bi("Estudia", "Studying"),
    "INAC_OTH": bi("Otros inactivos", "Other inactive"),
}


def europa_con_padres():
    """Quiénes son los jóvenes de 25 a 34 años que viven con sus padres: composición por situación laboral, España y UE,
    y descomposición de la diferencia en puntos de población entre los que trabajan y los que no."""
    comp = sources.eurostat("ilc_lvps09", geo=["ES", "EU27_2020"], age="Y25-34")
    share = sources.eurostat("ilc_lvps08", geo=["ES", "EU27_2020"], age="Y25-34", sex="T")
    c = {(geo.from_eurostat(r["geo"]), r["wstatus"], r["time"]): r["value"] for r in comp}
    s = {(geo.from_eurostat(r["geo"]), r["time"]): r["value"] for r in share}
    year = max(t for (g, w, t) in c if all((x, ww, t) in c for x in ("ESP", "EU27") for ww in STATUS)
               and ("ESP", t) in s and ("EU27", t) in s)
    total = {g: round(sum(c[(g, w, year)] for w in STATUS), 1) for g in ("ESP", "EU27")}
    assert all(abs(v - 100) < 0.6 for v in total.values()), total   # la composición suma 100
    work = {g: c[(g, "EMP_FT", year)] + c[(g, "EMP_PT", year)] for g in ("ESP", "EU27")}
    # Puntos de población de 25 a 34 años que viven con sus padres y trabajan (o no)
    pop_work = {g: round(s[(g, year)] * work[g] / 100, 1) for g in work}
    pop_nowork = {g: round(s[(g, year)] - pop_work[g], 1) for g in work}
    gap = round(s[("ESP", year)] - s[("EU27", year)], 1)
    gap_work = round(pop_work["ESP"] - pop_work["EU27"], 1)
    rows = [{"geo": w, "time": t, "value": c[(g, w, year)]} for w in STATUS for t, g in (("0-ue", "EU27"), ("1-espana", "ESP"))]
    return chart(
        id="joe2-europa-trabajan",
        lens="europa", theme="jovenes",
        title=bi(f"El {dec(pop_work['ESP'], 'es')} % de los españoles de 25 a 34 años trabaja y sigue viviendo con sus padres; "
                 f"en la UE, el {dec(pop_work['EU27'], 'es')} %",
                 f"{dec(pop_work['ESP'], 'en')}% of Spaniards aged 25 to 34 have a job and still live with their parents; "
                 f"in the EU, {dec(pop_work['EU27'], 'en')}%"),
        subtitle=bi(f"Jóvenes de 25 a 34 años que viven con sus padres según su situación (trabajo a tiempo completo o parcial, "
                    f"paro, estudios u otra), {year}, en % del total de los que viven con sus padres. Punto hueco: media de la UE; punto lleno: España",
                    f"People aged 25 to 34 living with their parents by main activity (full-time or part-time job, "
                    f"unemployment, study or other), {year}, as % of all those living with their parents. Hollow dot: EU average; solid dot: Spain"),
        unit=bi("% de los que viven con sus padres", "% of those living with their parents"),
        source={**_src("ilc_lvps09"), "dataset": "ilc_lvps09 e ilc_lvps08"},
        notes={"es": [SILC_NOTE["es"],
                      "Situación declarada por el propio joven (actividad principal), no la definición de paro de la EPA.",
                      f"Titular: porcentaje de jóvenes de 25 a 34 años que viven con sus padres ({dec(s[('ESP', year)], 'es')} % en "
                      f"España y {dec(s[('EU27', year)], 'es')} % en la UE) por la parte de ellos que trabaja."],
               "en": [SILC_NOTE["en"],
                      "Status as reported by the young person (main activity), not the Labour Force Survey definition of "
                      "unemployment.",
                      f"Headline: share of people aged 25 to 34 living with their parents ({dec(s[('ESP', year)], 'en')}% in Spain "
                      f"and {dec(s[('EU27', year)], 'en')}% in the EU) times the share of them who work."]},
        rows=rows,
        geos={k: {**label, "aggregate": True} for k, label in STATUS.items()},
        extra={"dimensions": {"time": {"0-ue": bi("Media de la UE", "EU average"), "1-espana": bi("España", "Spain")}},
               "year": year,
               "living_with_parents": {g: s[(g, year)] for g in ("ESP", "EU27")},
               "working_share": {g: round(work[g], 1) for g in work},
               "pop_working": pop_work, "pop_not_working": pop_nowork,
               "gap": gap, "gap_working": gap_work, "gap_working_pct": round(100 * gap_work / gap, 1)},
    )


# ---------- España por dentro ----------

def comunidades_ninis():
    raw = sources.eurostat("edat_lfse_22", sex="T", age="Y15-29", time=list(REGION_YEARS))
    rows = _regions(raw)
    es = next(r["value"] for r in rows if r["geo"] == "ES")
    main = [r for r in rows if r["geo"] not in ("ES", *SMALL)]
    top, low = max(main, key=lambda r: r["value"]), min(main, key=lambda r: r["value"])
    eu = [r for r in sources.eurostat("edat_lfse_22", sex="T", age="Y15-29", geo="EU27_2020", time=list(REGION_YEARS))]
    eu_avg = round(sum(r["value"] for r in eu) / len(eu), 1)
    below_eu = sorted(r["geo"] for r in main if r["value"] < eu_avg)
    period = f"{REGION_YEARS[0]}-{REGION_YEARS[-1]}"
    return chart(
        id="jod1-comunidades-ninis",
        lens="dentro", theme="jovenes",
        title=bi(f"Ni estudian ni trabajan el {dec(top['value'], 'es')} % de los jóvenes de {_name(top['geo'], 'es')} y el "
                 f"{dec(low['value'], 'es')} % de los de {_name(low['geo'], 'es')}",
                 f"{dec(top['value'], 'en')}% of young people in {_name(top['geo'], 'en')} are neither in work nor in education, "
                 f"against {dec(low['value'], 'en')}% in {_name(low['geo'], 'en')}"),
        subtitle=bi(f"Jóvenes de 15 a 29 años que no trabajan ni estudian ni se forman, media {period}, en %. "
                    f"España: {dec(es, 'es')} %; UE: {dec(eu_avg, 'es')} %",
                    f"People aged 15 to 29 not in employment, education or training, {period} average, in %. "
                    f"Spain: {dec(es, 'en')}%; EU: {dec(eu_avg, 'en')}%"),
        unit=bi("% de los jóvenes de 15 a 29 años", "% of people aged 15 to 29"),
        source=_src("edat_lfse_22"),
        notes={"es": ["Encuesta de Población Activa. Incluye a los que buscan empleo y a los que no lo buscan (por cuidados, "
                      "enfermedad o desánimo).",
                      "Media de tres años, porque la muestra de cada comunidad es pequeña.",
                      "Ceuta y Melilla tienen una muestra muy pequeña y Eurostat marca su dato como poco fiable."],
               "en": ["Labour Force Survey. Includes those looking for work and those who are not (because of caring "
                      "responsibilities, illness or discouragement).",
                      "Three-year average, because the sample in each region is small.",
                      "Ceuta and Melilla have a very small sample and Eurostat flags their figure as having low reliability."]},
        rows=rows,
        geos=geo.ccaa_table(r["geo"] for r in rows),
        extra={"eu": eu_avg, "below_eu": below_eu},
    )


def comunidades_paro_estudios():
    raw = sources.eurostat("lfst_r_lfu3rt", sex="T", age="Y25-34", isced11=["ED0-2", "ED5-8"], time=list(REGION_YEARS))
    by = {}
    for r in raw:
        code = NUTS2.get(r["geo"])
        if code and code not in SMALL:
            by.setdefault((code, r["isced11"]), []).append(r["value"])
    avg = {k: round(sum(v) / len(v), 1) for k, v in by.items()}
    codes = sorted({c for c, _ in avg})
    rows = [{"geo": c, "time": t, "value": avg[(c, i)]} for c in codes for t, i in (("0-sup", "ED5-8"), ("1-eso", "ED0-2"))
            if (c, i) in avg]
    full = [c for c in codes if (c, "ED0-2") in avg and (c, "ED5-8") in avg]
    ratio = {c: round(avg[(c, "ED0-2")] / avg[(c, "ED5-8")], 2) for c in full}
    assert all(r > 1 for r in ratio.values()), ratio   # el titular dice «en todas las comunidades»
    es = (avg[("ES", "ED0-2")], avg[("ES", "ED5-8")])
    regions = [c for c in full if c != "ES"]
    period = f"{REGION_YEARS[0]}-{REGION_YEARS[-1]}"
    hi, lo = max(regions, key=lambda c: avg[(c, "ED0-2")]), min(regions, key=lambda c: avg[(c, "ED0-2")])
    return chart(
        id="jod2-comunidades-paro-estudios",
        lens="dentro", theme="jovenes",
        title=bi(f"En todas las comunidades, el paro de los jóvenes que no pasaron de la ESO es más alto que el de los "
                 f"que tienen estudios superiores: en España, el {dec(es[0], 'es')} % frente al {dec(es[1], 'es')} %",
                 f"In every region, unemployment among young people with no more than lower secondary education is higher than "
                 f"among those with tertiary education: in Spain, {dec(es[0], 'en')}% against {dec(es[1], 'en')}%"),
        subtitle=bi(f"Tasa de paro de 25 a 34 años según el nivel de estudios, media {period}, en %. Punto hueco: estudios "
                    f"superiores; punto lleno: como mucho la ESO",
                    f"Unemployment rate, aged 25 to 34, by level of education, {period} average, in %. Hollow dot: tertiary "
                    f"education; solid dot: lower secondary at most"),
        unit=bi("% de los activos", "% of the labour force"),
        source=_src("lfst_r_lfu3rt"),
        notes={"es": ["Encuesta de Población Activa. Tasa de paro: parados sobre activos (los que trabajan o buscan empleo) de "
                      "cada nivel de estudios. «Como mucho la ESO»: niveles 0 a 2 de la CINE; «estudios superiores»: niveles 5 a 8 "
                      "(grado superior de FP, grado, máster y doctorado).",
                      "Media de tres años, porque la muestra de cada comunidad es pequeña; Eurostat marca como poco fiables "
                      "algunos datos anuales de las comunidades pequeñas. Sin Ceuta y Melilla, por el tamaño de la muestra."],
               "en": ["Labour Force Survey. Unemployment rate: unemployed over the labour force (those working or looking for "
                      "work) at each level of education. «Lower secondary at most»: ISCED levels 0 to 2; «tertiary»: levels 5 to 8 "
                      "(higher vocational training, bachelor's, master's and doctorate).",
                      "Three-year average, because the sample in each region is small; Eurostat flags some annual figures for "
                      "small regions as having low reliability. Ceuta and Melilla are excluded because of their sample size."]},
        rows=rows,
        geos=geo.ccaa_table(c for c in codes),
        extra={"dimensions": {"time": {"0-sup": bi("Estudios superiores", "Tertiary education"),
                                       "1-eso": bi("Como mucho la ESO", "Lower secondary at most")}},
               "ratio": ratio, "highest_low_educ": hi, "lowest_low_educ": lo},
    )


# ---------- España en el tiempo ----------

def con_padres():
    raw = sources.eurostat("ilc_lvps08", geo=["ES", "EU27_2020"], age="Y25-34", sex="T")
    rows = sorted(({"time": r["time"], "series": "espana" if r["geo"] == "ES" else "ue", "value": r["value"]} for r in raw),
                  key=lambda r: (r["series"], r["time"]))
    es = {r["time"]: r["value"] for r in rows if r["series"] == "espana"}
    eu = {r["time"]: r["value"] for r in rows if r["series"] == "ue"}
    last, first = max(es), min(es)
    # 2008: último año antes de la crisis; el salto de 2004 a 2005 coincide con el arranque de la encuesta
    low_year = "2008"
    is_max = es[last] == max(es.values())
    return chart(
        id="jot1-con-padres",
        lens="tiempo", theme="jovenes",
        title=bi(f"La mitad de los españoles de 25 a 34 años vive con sus padres: el {dec(es[last], 'es')} % en {last}, "
                 f"frente al {dec(es[low_year], 'es')} % en {low_year}",
                 f"Half of Spaniards aged 25 to 34 live with their parents: {dec(es[last], 'en')}% in {last}, against "
                 f"{dec(es[low_year], 'en')}% in {low_year}"),
        subtitle=bi(f"Jóvenes de 25 a 34 años que viven con sus padres, {first}-{last}, en %",
                    f"People aged 25 to 34 living with their parents, {first}-{last}, in %"),
        unit=bi("% de los jóvenes de 25 a 34 años", "% of people aged 25 to 34"),
        source=_src("ilc_lvps08"),
        notes={"es": [SILC_NOTE["es"],
                      f"La media de la UE empieza en {min(eu)} y es una estimación de Eurostat hasta 2019.",
                      "En 2008 y 2013 hubo cambios de método en la encuesta española; en 2021, en la de toda la UE."],
               "en": [SILC_NOTE["en"],
                      f"The EU average starts in {min(eu)} and is a Eurostat estimate until 2019.",
                      "There were methodological changes in the Spanish survey in 2008 and 2013, and in the EU-wide survey in 2021."]},
        rows=rows,
        extra={"dimensions": {"series": {"espana": bi("España", "Spain"), "ue": bi("Media de la UE", "EU average")}},
               "max_is_last": is_max, "low_year": low_year, "eu_last": eu[last], "eu_first": {min(eu): eu[min(eu)]}},
    )


TENURE = {
    "propiedad": ("Propiedad", bi("Propietarios", "Owners")),
    "mercado": ("Alquiler a precio de mercado", bi("Alquiler a precio de mercado", "Market rent")),
    "reducido": ("Alquiler inferior al precio de mercado", bi("Alquiler por debajo del mercado", "Below-market rent")),
    "cesion": ("Cesión", bi("Cesión gratuita", "Rent-free")),
}


def tenencia():
    raw = sources.ine_table(ECV_TENURE_TABLE)
    v = {}
    for key, (name, _) in TENURE.items():
        for age in ("De 16 a 29 años", "De 30 a 44 años"):
            for r in raw:
                if r["series"] == f"Ambos sexos. {age}. Total Nacional. {name}. Hogar":
                    v[(key, age, r["year"])] = r["value"]
    years = sorted({y for (k, a, y) in v if a == "De 16 a 29 años"})
    young = "De 16 a 29 años"
    for y in years:
        assert abs(sum(v[(k, young, y)] for k in TENURE) - 100) < 0.6, y
    rows = [{"time": str(y), "series": k, "value": v[(k, young, y)]} for k in TENURE for y in years]
    # Titular con medias de tres años: la muestra de hogares encabezados por menores de 30 es pequeña
    def avg(k, age, ys):
        return round(sum(v[(k, age, y)] for y in ys) / len(ys), 1)
    early, late = (2006, 2007, 2008), tuple(years[-3:])
    own = (avg("propiedad", young, early), avg("propiedad", young, late))
    rent = (avg("mercado", young, early), avg("mercado", young, late))
    own30 = (avg("propiedad", "De 30 a 44 años", early), avg("propiedad", "De 30 a 44 años", late))
    pe, pl = f"{early[0]}-{early[-1]}", f"{late[0]}-{late[-1]}"
    return chart(
        id="jot2-tenencia",
        lens="tiempo", theme="jovenes",
        title=bi(f"En los hogares de menores de 30 años, los propietarios han pasado del {dec(own[0], 'es', 0)} % al "
                 f"{dec(own[1], 'es', 0)} % y los inquilinos a precio de mercado, del {dec(rent[0], 'es', 0)} % al "
                 f"{dec(rent[1], 'es', 0)} %",
                 f"In households headed by under-30s, owners have fallen from {dec(own[0], 'en', 0)}% to {dec(own[1], 'en', 0)}% "
                 f"and market-rent tenants have risen from {dec(rent[0], 'en', 0)}% to {dec(rent[1], 'en', 0)}%"),
        subtitle=bi(f"Hogares cuya persona de referencia tiene de 16 a 29 años según el régimen de tenencia de la vivienda, "
                    f"{years[0]}-{years[-1]}, en %",
                    f"Households whose reference person is aged 16 to 29 by housing tenure, {years[0]}-{years[-1]}, in %"),
        unit=bi("% de los hogares", "% of households"),
        source=INE_ECV,
        notes={"es": [f"Titular: medias de {pe} y de {pl}, porque la muestra de hogares encabezados por menores de 30 años es "
                      "pequeña y el dato de un año suelto varía mucho.",
                      "Solo cuenta a los jóvenes que ya tienen su propio hogar (o encabezan uno), no a los que viven con sus padres.",
                      "Propietarios: con o sin hipoteca. Cesión: vivienda prestada gratis, a menudo por la familia o la empresa."],
               "en": [f"Headline: averages for {pe} and {pl}, because the sample of households headed by under-30s is small and "
                      "a single year's figure varies a lot.",
                      "It only counts young people who already have (or head) their own household, not those living with their "
                      "parents.",
                      "Owners: with or without a mortgage. Rent-free: a home lent at no cost, often by family or an employer."]},
        rows=rows,
        extra={"dimensions": {"series": {k: label for k, (_, label) in TENURE.items()}},
               "short_labels": {"propiedad": bi("Propietarios", "Owners"), "mercado": bi("Alquiler", "Market rent"),
                                "reducido": bi("Bajo mercado", "Below market"), "cesion": bi("Cesión", "Rent-free")},
               "averages": {"early": pe, "late": pl, "owners": own, "market_rent": rent, "owners_30_44": own30}},
    )


BUILDERS = [europa_edad, europa_con_padres, comunidades_ninis, comunidades_paro_estudios, con_padres, tenencia]
