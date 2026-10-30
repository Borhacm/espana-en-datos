"""Tema Fiscalidad (código FI): presión fiscal, qué impuestos y en qué se gasta frente a la UE, qué pagan y reciben los hogares
de cada comunidad y cómo ha cambiado la recaudación."""

from lib import geo, sources
from lib.output import THEMES, chart

from .common import bi, dec
from .educacion import NUTS2

THEMES["fiscalidad"] = {"code": "FI", "title": "Impuestos y gasto público"}

EUROSTAT = {"name": "Eurostat, cuentas de las administraciones públicas", "license": "CC BY 4.0"}
REGIONAL = {"name": "Eurostat, cuentas nacionales", "license": "CC BY 4.0"}
SMALL = ("18", "19")   # Ceuta y Melilla: economías muy pequeñas, no protagonizan titulares


def _int(v: float, lang: str) -> str:
    """Entero con separador de miles: 5.084 en español, 5,084 en inglés."""
    s = f"{round(v):,}"
    return s.replace(",", ".") if lang == "es" else s


def _src(dataset: str, base: dict = EUROSTAT) -> dict:
    return {**base, "dataset": dataset, "url": f"https://ec.europa.eu/eurostat/databrowser/view/{dataset}/default/table"}


TOTAL = "D2_D5_D91_D61_M_D995"   # impuestos y cotizaciones sociales netas, menos lo que no se espera cobrar


def _taxes(items: list[str]) -> dict:
    """{(partida, país, año): % del PIB} de impuestos y cotizaciones de todas las administraciones y las instituciones de la UE."""
    raw = sources.eurostat("gov_10a_taxag", na_item=items, sector="S13_S212", unit="PC_GDP")
    return {(r["na_item"], geo.from_eurostat(r["geo"]), int(r["time"])): r["value"] for r in raw if geo.from_eurostat(r["geo"])}


def _is_eu(c: str) -> bool:
    return c == "EU27" or geo.COUNTRIES.get(c, (0, 0, 0, False))[3]


PRESION_NOTE = {
    "es": "Presión fiscal: impuestos y cotizaciones sociales que cobran todas las administraciones (y la UE, por los aranceles) "
          "en % del PIB. Incluye las cotizaciones sociales imputadas y descuenta lo que se ha liquidado pero no se espera cobrar.",
    "en": "Tax burden: taxes and social contributions collected by all levels of government (and the EU, through customs duties) "
          "as % of GDP. It includes imputed social contributions and excludes amounts assessed but unlikely to be collected.",
}
PROVISIONAL = {
    "es": "Los datos del último año son provisionales y pueden revisarse.",
    "en": "Figures for the last year are provisional and may be revised.",
}


# ---------- España frente a Europa ----------

def europa_presion():
    v = _taxes([TOTAL])
    year = max(y for (_, c, y) in v if c == "EU27")
    rows = sorted(({"geo": c, "time": str(y), "value": val} for (_, c, y), val in v.items() if y == year and _is_eu(c)),
                  key=lambda r: r["geo"])
    es, eu = v[(TOTAL, "ESP", year)], v[(TOTAL, "EU27", year)]
    ranked = sorted((r for r in rows if r["geo"] != "EU27"), key=lambda r: -r["value"])
    above = [r["geo"] for r in ranked][:[r["geo"] for r in ranked].index("ESP")]
    n = len(ranked)
    return chart(
        id="fie1-europa-presion",
        lens="europa", theme="fiscalidad",
        title=bi(f"España recauda en impuestos y cotizaciones el {dec(es, 'es')} % del PIB: {len(above)} de los {n} países de la UE "
                 f"recaudan más",
                 f"Spain collects {dec(es, 'en')}% of GDP in taxes and social contributions: {len(above)} of the {n} EU countries "
                 f"collect more"),
        subtitle=bi(f"Impuestos y cotizaciones sociales, {year}, en % del PIB. Media de la UE: {dec(eu, 'es')} %",
                    f"Taxes and social contributions, {year}, as % of GDP. EU average: {dec(eu, 'en')}%"),
        unit=bi("% del PIB", "% of GDP"),
        source=_src("gov_10a_taxag"),
        notes={"es": [PRESION_NOTE["es"],
                      "Un porcentaje del PIB más bajo no significa que cada contribuyente pague menos: depende también de cuánta renta "
                      "y cuánto consumo hay, de las exenciones y del fraude.",
                      PROVISIONAL["es"]],
               "en": [PRESION_NOTE["en"],
                      "A lower share of GDP does not mean that each taxpayer pays less: it also depends on how much income and "
                      "consumption there is, on exemptions and on tax evasion.",
                      PROVISIONAL["en"]]},
        rows=rows,
        geos=geo.country_table(r["geo"] for r in rows),
        extra={"countries_above": above},
    )


# Grupos de impuestos: partidas de Eurostat que suman (+) o restan (-)
TAX_GROUPS = {
    "iva": (bi("IVA", "VAT"), {"D211": 1}),
    "produccion": (bi("Otros al consumo", "Other consumption"), {"D2": 1, "D211": -1}),
    "irpf": (bi("IRPF", "Personal income"), {"D51A_C1": 1}),
    "sociedades": (bi("Sociedades", "Corporate profits"), {"D51B_C2": 1}),
    "otros": (bi("Patrimonio y otros", "Wealth and other"),
              {"D5": 1, "D51A_C1": -1, "D51B_C2": -1, "D91": 1}),
    "cotizaciones": (bi("Cotizaciones", "Contributions"), {"D61": 1}),
}
TAX_ITEMS = sorted({i for _, parts in TAX_GROUPS.values() for i in parts} | {TOTAL})


def _group(v: dict, key: str, c: str, y: int) -> float:
    return round(sum(s * v[(i, c, y)] for i, s in TAX_GROUPS[key][1].items()), 1)


def europa_impuestos():
    v = _taxes(TAX_ITEMS)
    year = max(y for (_, c, y) in v if c == "EU27")
    g = {(k, c): _group(v, k, c, year) for k in TAX_GROUPS for c in ("ESP", "EU27")}
    rows = [{"geo": k, "time": t, "value": g[(k, c)]} for k in TAX_GROUPS for t, c in (("0-ue", "EU27"), ("1-espana", "ESP"))]
    consumo = {c: round(g[("iva", c)] + g[("produccion", c)], 1) for c in ("ESP", "EU27")}
    renta = {c: round(g[("irpf", c)] + g[("sociedades", c)], 1) for c in ("ESP", "EU27")}
    gap = round(v[(TOTAL, "EU27", year)] - v[(TOTAL, "ESP", year)], 1)
    return chart(
        id="fie2-europa-impuestos",
        lens="europa", theme="fiscalidad",
        title=bi(f"En impuestos sobre la renta y los beneficios, España ya recauda como la media de la UE; recauda menos en impuestos "
                 f"sobre el consumo ({dec(consumo['ESP'], 'es')} % del PIB frente a {dec(consumo['EU27'], 'es')} %) y en cotizaciones",
                 f"In taxes on income and profits, Spain now collects as much as the EU average; it collects less in taxes on "
                 f"consumption ({dec(consumo['ESP'], 'en')}% of GDP against {dec(consumo['EU27'], 'en')}%) and in social contributions"),
        subtitle=bi(f"Recaudación por tipo de impuesto, {year}, en % del PIB. Punto hueco: media de la UE; punto lleno: España",
                    f"Revenue by type of tax, {year}, as % of GDP. Hollow dot: EU average; solid dot: Spain"),
        unit=bi("% del PIB", "% of GDP"),
        source=_src("gov_10a_taxag"),
        notes={"es": ["Otros al consumo: impuestos especiales (hidrocarburos, tabaco, alcohol, electricidad), "
                      "transmisiones patrimoniales y actos jurídicos, primas de seguros, IBI y otros que pagan las empresas por producir.",
                      "IRPF: sobre todo el IRPF, también el impuesto sobre la renta de no residentes. Sociedades: impuesto sobre los beneficios "
                      "de las empresas. Patrimonio y otros: patrimonio, sucesiones y donaciones, entre otros.",
                      "Cotizaciones: las sociales de empresas y trabajadores, incluidas las imputadas (las que equivalen a las pensiones "
                      "que pagan directamente las administraciones a sus funcionarios).",
                      "Las partidas están redondeadas a un decimal y su suma puede no coincidir con el total.",
                      PROVISIONAL["es"]],
               "en": ["Other consumption: excise duties (fuel, tobacco, alcohol, electricity), property "
                      "transfer and stamp duties, insurance premium tax, property tax (IBI) and other taxes paid by businesses on "
                      "production.",
                      "Personal income: mainly IRPF (Spain's personal income tax), also the non-resident income tax. Corporate profits: "
                      "corporate income tax. Wealth and other: wealth tax and inheritance and gift tax, "
                      "among others.",
                      "Contributions: social contributions paid by employers and workers, including imputed contributions (those equivalent "
                      "to the pensions that government pays directly to its civil servants).",
                      "Items are rounded to one decimal place and may not add up to the total.",
                      PROVISIONAL["en"]]},
        rows=rows,
        geos={k: {**label, "aggregate": True} for k, (label, _) in TAX_GROUPS.items()},
        extra={"dimensions": {"time": {"0-ue": bi("Media de la UE", "EU average"), "1-espana": bi("España", "Spain")}},
               "groups": {k: {"ESP": g[(k, "ESP")], "EU27": g[(k, "EU27")]} for k in TAX_GROUPS},
               "consumo": consumo, "renta": renta, "gap_total": gap},
    )


COFOG = {
    "GF10": bi("Protección social", "Social protection"),
    "GF07": bi("Sanidad", "Health"),
    "GF01": bi("Servicios generales", "General services"),
    "GF04": bi("Asuntos económicos", "Economic affairs"),
    "GF09": bi("Educación", "Education"),
    "GF03": bi("Seguridad", "Public order"),
    "GF08": bi("Cultura y ocio", "Culture, recreation"),
    "GF02": bi("Defensa", "Defence"),
    "GF05": bi("Medio ambiente", "Environment"),
    "GF06": bi("Vivienda", "Housing"),
}
SOCIAL = {"GF1001": "enfermedad", "GF1002": "vejez", "GF1003": "supervivencia", "GF1004": "familia", "GF1005": "desempleo",
          "GF1006": "vivienda", "GF1007": "exclusion"}


def europa_gasto():
    raw = sources.eurostat("gov_10a_exp", cofog99=["TOTAL", *COFOG, *SOCIAL], sector="S13", unit="PC_GDP", na_item="TE")
    v = {(r["cofog99"], geo.from_eurostat(r["geo"]), int(r["time"])): r["value"] for r in raw}
    year = max(y for (f, c, y) in v if c == "EU27" and f == "TOTAL" and ("TOTAL", "ESP", y) in v)
    rows = [{"geo": f, "time": t, "value": v[(f, c, year)]} for f in COFOG for t, c in (("0-ue", "EU27"), ("1-espana", "ESP"))]
    es, eu = v[("TOTAL", "ESP", year)], v[("TOTAL", "EU27", year)]
    diff = {f: round(v[(f, "EU27", year)] - v[(f, "ESP", year)], 1) for f in COFOG}
    biggest = max(diff.values())
    top = [f for f in COFOG if diff[f] == biggest]
    names_es = " y ".join(COFOG[f]["es"].lower() for f in top)
    names_en = " and ".join(COFOG[f]["en"].lower() for f in top)
    social = {k: {"ESP": v[(f, "ESP", year)], "EU27": v[(f, "EU27", year)]} for f, k in SOCIAL.items()}
    return chart(
        id="fie3-europa-gasto",
        lens="europa", theme="fiscalidad",
        title=bi(f"El gasto público equivale al {dec(es, 'es')} % del PIB en España y al {dec(eu, 'es')} % en la UE; donde más se "
                 f"queda por debajo es en {names_es}",
                 f"Public spending is equivalent to {dec(es, 'en')}% of GDP in Spain and {dec(eu, 'en')}% in the EU; it falls furthest "
                 f"below in {names_en}"),
        subtitle=bi(f"Gasto de las administraciones públicas por función, {year}, en % del PIB. Punto hueco: media de la UE; "
                    f"punto lleno: España",
                    f"General government expenditure by function, {year}, as % of GDP. Hollow dot: EU average; solid dot: Spain"),
        unit=bi("% del PIB", "% of GDP"),
        source=_src("gov_10a_exp"),
        notes={"es": ["Clasificación de las funciones de las administraciones públicas (COFOG). Protección social incluye las pensiones "
                      "de jubilación y viudedad, el paro, la incapacidad, la familia y la exclusión social; las pensiones de los "
                      "funcionarios cuentan aquí aunque se paguen sin pasar por la Seguridad Social.",
                      "Sanidad incluye el gasto público en hospitales, atención primaria y medicamentos, no el privado. Servicios "
                      "generales incluye los intereses de la deuda. Seguridad: policía, bomberos, justicia y prisiones. Vivienda: "
                      "vivienda, urbanismo, agua y alumbrado público (las prestaciones de vivienda a los hogares cuentan en protección social).",
                      "Comparar en % del PIB no tiene en cuenta que la población de cada país tiene una edad distinta."],
               "en": ["Classification of the functions of government (COFOG). Social protection includes retirement and survivors' "
                      "pensions, unemployment, disability, family and social exclusion; civil servants' pensions count here even when "
                      "they are not paid through Social Security.",
                      "Health includes public spending on hospitals, primary care and medicines, not private spending. General "
                      "services includes interest on debt. Public order: police, fire services, courts and prisons. Housing: housing, "
                      "urban development, water supply and street lighting (housing benefits paid to households count as social protection).",
                      "Comparing as % of GDP does not take into account that each country's population has a different age profile."]},
        rows=rows,
        geos={f: {**label, "aggregate": True} for f, label in COFOG.items()},
        extra={"dimensions": {"time": {"0-ue": bi("Media de la UE", "EU average"), "1-espana": bi("España", "Spain")}},
               "gap": diff, "social": social},
    )


# ---------- España por dentro ----------

def _households() -> tuple[dict, int, dict]:
    """Cuentas de los hogares por comunidad (millones de euros) y población media (miles), último año con datos."""
    raw = sources.eurostat("nama_10r_2hhinc", unit="MIO_EUR", na_item=["B5N", "B6N", "D5", "D61", "D62"], geo=list(NUTS2))
    v = {(NUTS2[r["geo"]], r["na_item"], r["direct"], int(r["time"])): r["value"] for r in raw}
    year = max(y for (c, i, d, y) in v if c == "13" and i == "B6N")
    pop = {NUTS2[r["geo"]]: r["value"] for r in sources.eurostat("nama_10r_3popgdp", unit="THS", geo=list(NUTS2))
           if int(r["time"]) == year}
    return v, year, pop


HOUSEHOLDS_NOTE = {
    "es": "Cuentas de los hogares de cada comunidad: se cuenta a las personas donde viven. No incluyen el IVA ni los demás "
          "impuestos sobre el consumo, ni el gasto público en sanidad o educación, que se recibe en servicios y no en dinero.",
    "en": "Household accounts for each region: people are counted where they live. They do not include VAT or other taxes on "
          "consumption, nor public spending on health or education, which is received as services rather than cash.",
}


def comunidades():
    v, year, pop = _households()
    codes = sorted(pop)

    def per_hab(c, item, d):
        return 1000 * v[(c, item, d, year)] / pop[c]   # millones / miles = miles de euros por habitante

    saldo = {c: round(per_hab(c, "D5", "PAID") + per_hab(c, "D61", "PAID") - per_hab(c, "D62", "RECV")) for c in codes}
    rows1 = [{"geo": c, "time": str(year), "value": saldo[c]} for c in codes]
    main = [c for c in codes if c not in ("ES", *SMALL)]
    top, low = max(main, key=lambda c: saldo[c]), min(main, key=lambda c: saldo[c])
    negative = [c for c in main if saldo[c] < 0]
    parts = {c: {"impuestos": round(per_hab(c, "D5", "PAID")), "cotizaciones": round(per_hab(c, "D61", "PAID")),
                 "prestaciones": round(per_hab(c, "D62", "RECV"))} for c in codes}
    d1 = chart(
        id="fid1-comunidades-saldo",
        lens="dentro", theme="fiscalidad",
        title=bi(f"Los hogares de {geo.ccaa_name(top, 'es')} pagan en impuestos sobre la renta y cotizaciones {_int(saldo[top], 'es')} "
                 f"euros por habitante más de lo que reciben en pensiones y prestaciones; los de {geo.ccaa_name(low, 'es')} reciben "
                 f"{_int(-saldo[low], 'es')} euros más de lo que pagan",
                 f"Households in {geo.ccaa_name(top, 'en')} pay {_int(saldo[top], 'en')} euros per inhabitant more in income taxes and "
                 f"social contributions than they receive in pensions and benefits; those in {geo.ccaa_name(low, 'en')} receive "
                 f"{_int(-saldo[low], 'en')} euros more than they pay"),
        subtitle=bi(f"Impuestos sobre la renta y el patrimonio y cotizaciones sociales que pagan los hogares menos las prestaciones "
                    f"en dinero que reciben, euros por habitante, {year}. España: {_int(saldo['ES'], 'es')} euros",
                    f"Taxes on income and wealth and social contributions paid by households minus the cash benefits they receive, "
                    f"euros per inhabitant, {year}. Spain: {_int(saldo['ES'], 'en')} euros"),
        unit=bi("euros por habitante", "euros per inhabitant"),
        source=_src("nama_10r_2hhinc", REGIONAL),
        notes={"es": [HOUSEHOLDS_NOTE["es"],
                      "Cotizaciones: las de los trabajadores y también las que pagan las empresas por ellos. Prestaciones: pensiones, "
                      "paro, incapacidad y otras ayudas en dinero, incluidas las de las mutualidades y los planes de empresa.",
                      "Población media del año según Eurostat."],
               "en": [HOUSEHOLDS_NOTE["en"],
                      "Contributions: those paid by workers and also those paid by employers on their behalf. Benefits: pensions, "
                      "unemployment, disability and other cash benefits, including those from mutual societies and company schemes.",
                      "Average population for the year according to Eurostat."]},
        rows=rows1,
        geos=geo.ccaa_table(codes),
        extra={"parts": parts, "negative": negative},
    )

    b5 = {c: per_hab(c, "B5N", "BAL") for c in codes}
    b6 = {c: per_hab(c, "B6N", "BAL") for c in codes}
    rows2 = []
    for c in codes:
        rows2 += [{"geo": c, "time": "antes", "stage": "antes", "value": round(100 * b5[c] / b5["ES"], 1)},
                  {"geo": c, "time": "despues", "stage": "despues", "value": round(100 * b6[c] / b6["ES"], 1)}]
    rich, poor = max(main, key=lambda c: b5[c]), min(main, key=lambda c: b5[c])
    r_before, r_after = b5[rich] / b5[poor], b6[rich] / b6[poor]
    stage = {"antes": bi("Renta antes de impuestos y prestaciones", "Income before taxes and benefits"),
             "despues": bi("Renta disponible", "Disposable income")}
    d2 = chart(
        id="fid2-comunidades-renta",
        lens="dentro", theme="fiscalidad",
        title=bi(f"Antes de impuestos y prestaciones, la renta por habitante de {geo.ccaa_name(rich, 'es')} es {dec(r_before, 'es', 2)} "
                 f"veces la de {geo.ccaa_name(poor, 'es')}; después, {dec(r_after, 'es', 2)} veces",
                 f"Before taxes and benefits, income per inhabitant in {geo.ccaa_name(rich, 'en')} is {dec(r_before, 'en', 2)} times "
                 f"that of {geo.ccaa_name(poor, 'en')}; afterwards, {dec(r_after, 'en', 2)} times"),
        subtitle=bi(f"Renta de los hogares por habitante antes de impuestos y prestaciones (renta primaria) y renta disponible, {year}. "
                    f"Índice: España = 100 en cada una",
                    f"Household income per inhabitant before taxes and benefits (primary income) and disposable income, {year}. "
                    f"Index: Spain = 100 for each"),
        unit=bi("Índice (España = 100)", "Index (Spain = 100)"),
        source=_src("nama_10r_2hhinc", REGIONAL),
        notes={"es": [HOUSEHOLDS_NOTE["es"],
                      "Renta primaria: salarios (con las cotizaciones de la empresa), rentas de los autónomos, alquileres, intereses y "
                      "dividendos. Renta disponible: la primaria menos los impuestos sobre la renta y las cotizaciones, más las "
                      "prestaciones y otras transferencias."],
               "en": [HOUSEHOLDS_NOTE["en"],
                      "Primary income: wages (including employer contributions), self-employment income, rents, interest and "
                      "dividends. Disposable income: primary income minus income taxes and contributions, plus benefits and other "
                      "transfers."]},
        rows=rows2,
        geos=geo.ccaa_table(codes),
        extra={"dimensions": {"time": stage, "stage": stage},
               "ratio": {"rich": rich, "poor": poor, "before": round(r_before, 3), "after": round(r_after, 3)},
               "disposable_share": {c: round(100 * v[(c, "B6N", "BAL", year)] / v[(c, "B5N", "BAL", year)], 1) for c in codes}},
    )
    return [d1, d2]


# ---------- España en el tiempo ----------

def tiempo_presion():
    v = _taxes([TOTAL])
    years = sorted(y for (_, c, y) in v if c == "ESP" and (TOTAL, "EU27", y) in v)
    last = years[-1]
    rows = [{"time": str(y), "series": k, "value": v[(TOTAL, c, y)]} for k, c in (("espana", "ESP"), ("ue", "EU27")) for y in years]
    gap = {y: round(v[(TOTAL, "EU27", y)] - v[(TOTAL, "ESP", y)], 1) for y in years}
    es = {y: v[(TOTAL, "ESP", y)] for y in years}
    min_gap = min(gap.values())
    boom = max((y for y in years if y < 2010), key=lambda y: es[y])
    crisis = min((y for y in years if boom < y < 2015), key=lambda y: es[y])
    return chart(
        id="fit1-presion",
        lens="tiempo", theme="fiscalidad",
        title=bi(f"La distancia con la UE en presión fiscal se ha reducido de {dec(gap[years[0]], 'es')} puntos en {years[0]} a "
                 f"{dec(gap[last], 'es')} en {last}" + (", la menor de la serie" if gap[last] == min_gap else ""),
                 f"The tax-burden gap with the EU has narrowed from {dec(gap[years[0]], 'en')} points in {years[0]} to "
                 f"{dec(gap[last], 'en')} in {last}" + (", the smallest on record" if gap[last] == min_gap else "")),
        subtitle=bi(f"Impuestos y cotizaciones sociales en % del PIB, {years[0]}-{last}",
                    f"Taxes and social contributions as % of GDP, {years[0]}-{last}"),
        unit=bi("% del PIB", "% of GDP"),
        source=_src("gov_10a_taxag"),
        notes={"es": [PRESION_NOTE["es"], "UE: los 27 países actuales en toda la serie.", PROVISIONAL["es"]],
               "en": [PRESION_NOTE["en"], "EU: the current 27 countries throughout the series.", PROVISIONAL["en"]]},
        rows=rows,
        extra={"dimensions": {"series": {"espana": bi("España", "Spain"), "ue": bi("UE", "EU")}},
               "gap": {str(y): gap[y] for y in years}, "boom": {"year": boom, "value": es[boom]},
               "crisis": {"year": crisis, "value": es[crisis]}},
    )


SERIES_T2 = {"irpf": ("D51A_C1", bi("IRPF", "Personal income tax")), "sociedades": ("D51B_C2", bi("Sociedades", "Corporate tax")),
             "iva": ("D211", bi("IVA", "VAT")), "cotizaciones": ("D61", bi("Cotizaciones sociales", "Social contributions"))}


def tiempo_impuestos():
    v = _taxes([TOTAL, *(i for i, _ in SERIES_T2.values())])
    years = sorted(y for (i, c, y) in v if c == "ESP" and i == TOTAL)
    last, base = years[-1], 2019
    rows = [{"time": str(y), "series": k, "value": v[(i, "ESP", y)]} for k, (i, _) in SERIES_T2.items() for y in years]
    s = {k: {y: v[(i, "ESP", y)] for y in years} for k, (i, _) in SERIES_T2.items()}
    total = {y: v[(TOTAL, "ESP", y)] for y in years}
    change = {k: round(s[k][last] - s[k][base], 1) for k in SERIES_T2}
    change_total = round(total[last] - total[base], 1)
    renta = round(change["irpf"] + change["sociedades"], 1)
    rest = {y: round(total[y] - s["irpf"][y] - s["sociedades"][y], 1) for y in (base, last)}
    assert abs(rest[last] - rest[base]) <= 0.2, rest   # si el resto se mueve, el titular deja de valer
    peak_soc = max((y for y in years if y < 2010), key=lambda y: s["sociedades"][y])
    return chart(
        id="fit2-impuestos",
        lens="tiempo", theme="fiscalidad",
        title=bi(f"Desde {base}, el IRPF ha pasado del {dec(s['irpf'][base], 'es')} % al {dec(s['irpf'][last], 'es')} % del PIB y "
                 f"sociedades, del {dec(s['sociedades'][base], 'es')} % al {dec(s['sociedades'][last], 'es')} %; el resto de impuestos y "
                 f"cotizaciones, en conjunto, apenas ha cambiado",
                 f"Since {base}, personal income tax has risen from {dec(s['irpf'][base], 'en')}% to {dec(s['irpf'][last], 'en')}% of GDP "
                 f"and corporate tax from {dec(s['sociedades'][base], 'en')}% to {dec(s['sociedades'][last], 'en')}%; the rest of taxes and "
                 f"contributions, taken together, has barely changed"),
        subtitle=bi(f"Recaudación de los principales impuestos y de las cotizaciones sociales, en % del PIB, {years[0]}-{last}",
                    f"Revenue from the main taxes and from social contributions, as % of GDP, {years[0]}-{last}"),
        unit=bi("% del PIB", "% of GDP"),
        source=_src("gov_10a_taxag"),
        notes={"es": ["IRPF: impuestos sobre la renta de las personas, incluido el de no residentes. Sociedades: impuestos sobre los "
                      "beneficios de las empresas. Cotizaciones sociales: de empresas y trabajadores, incluidas las imputadas.",
                      "Lo que recauda cada impuesto se anota cuando se genera la obligación de pagar, no cuando se ingresa: puede "
                      "diferir de las cifras de caja de la Agencia Tributaria.",
                      PROVISIONAL["es"]],
               "en": ["IRPF: taxes on personal income, including the non-resident income tax. Corporate tax: taxes on company "
                      "profits. Social contributions: paid by employers and workers, including imputed contributions.",
                      "Each tax's revenue is recorded when the obligation to pay arises, not when it is paid in: it may differ from "
                      "the Tax Agency's cash figures.",
                      PROVISIONAL["en"]]},
        rows=rows,
        extra={"dimensions": {"series": {k: label for k, (_, label) in SERIES_T2.items()}},
               "short_labels": {"irpf": bi("IRPF", "PIT"), "sociedades": bi("Sociedades", "CIT"), "iva": bi("IVA", "VAT"),
                                "cotizaciones": bi("Cotizaciones", "Contributions")},
               "change": change, "change_total": change_total, "change_renta": renta, "rest": {str(y): r for y, r in rest.items()},
               "total": {str(base): total[base], str(last): total[last]},
               "peak_sociedades": {"year": peak_soc, "value": s["sociedades"][peak_soc]}},
    )


BUILDERS = [europa_presion, europa_impuestos, europa_gasto, comunidades, tiempo_presion, tiempo_impuestos]
