"""Tema Productividad y empresa (código PR): PIB por habitante y productividad por hora frente a la UE, de dónde sale la
distancia (productividad u horas trabajadas), el tamaño de las empresas, las diferencias entre comunidades, la convergencia
desde 1995 y el gasto en I+D."""

from lib import geo, sources
from lib.output import THEMES, chart

from .common import bi, dec, ine_ccaa
from .educacion import NUTS2

THEMES["productividad"] = {"code": "PR", "title": "Productividad y empresa"}

EUROSTAT_NA = {"name": "Eurostat, cuentas nacionales", "license": "CC BY 4.0"}
EUROSTAT_SBS = {"name": "Eurostat, estadísticas estructurales de empresas", "license": "CC BY 4.0"}
EUROSTAT_RD = {"name": "Eurostat, estadísticas de I+D", "license": "CC BY 4.0"}
INE_CRE = {"name": "INE, Contabilidad Regional de España", "license": "Reutilización libre citando la fuente",
           "dataset": "Tablas 82284, 82285 y 82002", "url": "https://www.ine.es/dyngs/INEbase/operacion.htm?c=Estadistica_C&cid=1254736167628&menu=resultados&idp=1254735576581"}
SMALL = ("18", "19")   # Ceuta y Melilla: no protagonizan titulares

PPS_NOTE = {
    "es": "En paridad de poder de compra (PPA): corrige las diferencias de nivel de precios entre países, de modo que un euro "
          "compra lo mismo en todos.",
    "en": "In purchasing power standards (PPS): corrects for differences in price levels between countries, so that a euro buys "
          "the same everywhere.",
}


def _src(dataset: str, base: dict) -> dict:
    return {**base, "dataset": dataset, "url": f"https://ec.europa.eu/eurostat/databrowser/view/{dataset}/default/table"}


def _is_eu(c: str | None) -> bool:
    return bool(c) and (c == "EU27" or geo.COUNTRIES.get(c, (0, 0, 0, False))[3])


def _int(v: float, lang: str) -> str:
    """Entero con separador de miles: 34.237 en español, 34,237 en inglés."""
    s = f"{round(v):,}"
    return s.replace(",", ".") if lang == "es" else s


def _es(code: str) -> str:
    """Nombre español de una comunidad con artículo cuando lo lleva (el País Vasco)."""
    name = geo.ccaa_name(code, "es")
    return f"el {name}" if code == "16" else name


def _en(code: str) -> str:
    """Nombre inglés de una comunidad con artículo cuando lo lleva (the Basque Country)."""
    name = geo.ccaa_name(code, "en")
    return f"the {name}" if code in ("04", "05", "10", "16") else name


# ---------- España frente a Europa ----------

def _gdp_pc() -> dict:
    """PIB por habitante en PPA, índice UE = 100, por país y año (con la marca de provisional)."""
    raw = sources.eurostat("nama_10_pc", unit="PC_EU27_2020_HAB_MPPS_CP", na_item="B1GQ")
    return {(geo.from_eurostat(r["geo"]), int(r["time"])): (r["value"], r["flag"]) for r in raw if _is_eu(geo.from_eurostat(r["geo"]))}


def europa_pib():
    v = _gdp_pc()
    year = max(y for (c, y) in v if c == "ESP" and ("EU27", y) in v)
    rows = sorted(({"geo": c, "time": str(y), "value": val[0]} for (c, y), val in v.items() if y == year), key=lambda r: r["geo"])
    es = v[("ESP", year)][0]
    others = [r for r in rows if r["geo"] not in ("EU27", "ESP")]
    above = sorted((r["geo"] for r in others if r["value"] > es), key=lambda c: -v[(c, year)][0])
    n = len(others) + 1
    provisional = v[("ESP", year)][1] == "p"
    return chart(
        id="pre1-europa-pib",
        lens="europa", theme="productividad",
        title=bi(f"El PIB por habitante de España es el {dec(es, 'es')} % de la media de la UE, una vez descontadas las diferencias "
                 f"de precios: {len(above)} de los otros {n - 1} países están por encima",
                 f"Spain's GDP per person is {dec(es, 'en')}% of the EU average once price differences are taken into account: "
                 f"{len(above)} of the other {n - 1} countries are above it"),
        subtitle=bi(f"PIB por habitante en paridad de poder de compra, {year}. Índice: media de la UE = 100",
                    f"GDP per person in purchasing power standards, {year}. Index: EU average = 100"),
        unit=bi("índice, UE = 100", "index, EU = 100"),
        source=_src("nama_10_pc", EUROSTAT_NA),
        notes={"es": [PPS_NOTE["es"],
                      "En Irlanda y Luxemburgo, el PIB por habitante está inflado por los beneficios de multinacionales y por los "
                      "trabajadores que viven en otros países.",
                      *([f"Los datos de {year} son provisionales."] if provisional else [])],
               "en": [PPS_NOTE["en"],
                      "In Ireland and Luxembourg, GDP per person is inflated by multinational profits and by workers who live in "
                      "other countries.",
                      *([f"{year} data are provisional."] if provisional else [])]},
        rows=rows,
        geos=geo.country_table(r["geo"] for r in rows),
        extra={"year": year, "countries_above": above},
    )


GAP_ITEMS = {   # etiquetas cortas: el nombre de cada fila tiene unos 150 píxeles
    "pib": bi("PIB por habitante", "GDP per person"),
    "hora": bi("PIB por hora", "GDP per hour"),
    "horas": bi("Horas por persona", "Hours per person"),
    "ocupados": bi("Ocupados", "Workers"),
    "jornada": bi("Horas por ocupado", "Hours per worker"),
}


def _lp() -> dict:
    raw = sources.eurostat("nama_10_lp_ulc", geo=["ES", "EU27_2020"],
                           na_item=["NLPR_HW", "HW_HAB", "HW_EMP", "EMP_HAB", "RLPR_HW"],
                           unit=["PC_EU27_2020_MPPS_CP", "HW", "PC_EU27_2020", "I10"])
    return {(geo.from_eurostat(r["geo"]), r["na_item"], r["unit"], int(r["time"])): r["value"] for r in raw}


def europa_brecha():
    v = _lp()
    pc = _gdp_pc()
    year = max(y for (c, i, u, y) in v if c == "ESP" and i == "NLPR_HW" and u == "PC_EU27_2020_MPPS_CP" and ("ESP", y) in pc)
    es = {
        "pib": pc[("ESP", year)][0],
        "hora": v[("ESP", "NLPR_HW", "PC_EU27_2020_MPPS_CP", year)],
        "horas": round(100 * v[("ESP", "HW_HAB", "HW", year)] / v[("EU27", "HW_HAB", "HW", year)], 1),
        "ocupados": v[("ESP", "EMP_HAB", "PC_EU27_2020", year)],
        "jornada": round(100 * v[("ESP", "HW_EMP", "HW", year)] / v[("EU27", "HW_EMP", "HW", year)], 1),
    }
    # El PIB por habitante es la productividad por hora por las horas por habitante: el producto de los índices tiene que cuadrar
    assert abs(es["hora"] * es["horas"] / 100 - es["pib"]) < 0.3, es
    hours = {c: {"per_person": v[(c, "HW_HAB", "HW", year)], "per_worker": v[(c, "HW_EMP", "HW", year)]} for c in ("ESP", "EU27")}
    rows = [{"geo": k, "time": t, "value": val} for k in GAP_ITEMS for t, val in (("0-ue", 100.0), ("1-espana", es[k]))]
    less_h, less_hh = round(100 - es["hora"], 1), round(100 - es["horas"], 1)
    return chart(
        id="pre2-europa-brecha",
        lens="europa", theme="productividad",
        title=bi(f"La distancia con la UE se reparte casi a partes iguales: España produce un {dec(less_h, 'es')} % menos por hora "
                 f"trabajada y trabaja un {dec(less_hh, 'es')} % menos horas por habitante, porque hay menos ocupados",
                 f"The gap with the EU is split almost evenly: Spain produces {dec(less_h, 'en')}% less per hour worked and works "
                 f"{dec(less_hh, 'en')}% fewer hours per person, because fewer people are in work"),
        subtitle=bi(f"España frente a la media de la UE (= 100), {year}: PIB por habitante y por hora trabajada, horas trabajadas por "
                    f"habitante, ocupados por habitante y horas por ocupado. Punto hueco: UE; punto lleno: España",
                    f"Spain compared with the EU average (= 100), {year}: GDP per person and per hour worked, hours worked per "
                    f"person, workers per person and hours per worker. Hollow dot: EU; solid dot: Spain"),
        unit=bi("índice, UE = 100", "index, EU = 100"),
        source=_src("nama_10_lp_ulc", EUROSTAT_NA),
        notes={"es": ["El PIB por habitante es igual a la productividad por hora multiplicada por las horas trabajadas por habitante; "
                      "y estas, a los ocupados por habitante multiplicados por las horas de cada ocupado. Los índices cumplen esas "
                      "igualdades salvo por el redondeo.",
                      "Productividad: PIB por hora trabajada en paridad de poder de compra. Ocupados y horas, de la contabilidad "
                      "nacional (incluye a los autónomos)."],
               "en": ["GDP per person equals productivity per hour multiplied by hours worked per person; and the latter equals "
                      "workers per person multiplied by hours per worker. The indices satisfy these identities except for rounding.",
                      "Productivity: GDP per hour worked in purchasing power standards. Workers and hours from the national "
                      "accounts (self-employed included)."]},
        rows=rows,
        geos={k: {**label, "aggregate": True} for k, label in GAP_ITEMS.items()},
        extra={"dimensions": {"time": {"0-ue": bi("Media de la UE", "EU average"), "1-espana": bi("España", "Spain")}},
               "year": year, "spain": es, "hours": hours},
    )


SIZES = {
    "0-9": bi("De 0 a 9 personas", "0 to 9 people"),
    "10-19": bi("De 10 a 19", "10 to 19"),
    "20-49": bi("De 20 a 49", "20 to 49"),
    "50-249": bi("De 50 a 249", "50 to 249"),
    "GE250": bi("250 o más", "250 or more"),
}


def europa_tamano():
    raw = sources.eurostat("sbs_sc_ovw", nace_r2="B-S_X_O_S94", indic_sbs=["EMP_NR", "LABPRY_TEUR"], geo=["ES", "EU27_2020"],
                           size_emp=["TOTAL", *SIZES])
    v = {(geo.from_eurostat(r["geo"]), r["indic_sbs"], r["size_emp"], int(r["time"])): r["value"] for r in raw}
    # Último año con todos los tamaños en España y en la UE (la UE publica algunos tamaños con un año de retraso)
    year = max(y for (c, i, s, y) in v
               if all((g, ind, sz, y) in v for g in ("ESP", "EU27") for ind in ("EMP_NR", "LABPRY_TEUR") for sz in ("TOTAL", *SIZES)))
    share = {c: {s: v[(c, "EMP_NR", s, year)] / v[(c, "EMP_NR", "TOTAL", year)] for s in SIZES} for c in ("ESP", "EU27")}
    prod = {c: {s: v[(c, "LABPRY_TEUR", s, year)] for s in SIZES} for c in ("ESP", "EU27")}
    total = {c: v[(c, "LABPRY_TEUR", "TOTAL", year)] for c in ("ESP", "EU27")}
    # Productividad de España con el reparto del empleo por tamaños de la UE (y la de cada tamaño en España)
    with_eu_sizes = sum(share["EU27"][s] * prod["ESP"][s] for s in SIZES)
    as_published = sum(share["ESP"][s] * prod["ESP"][s] for s in SIZES)
    assert abs(as_published - total["ESP"]) < 0.5, (as_published, total["ESP"])
    gap = total["EU27"] - total["ESP"]
    explained = round(100 * (with_eu_sizes - as_published) / gap, 1)
    assert all(prod["ESP"][s] < prod["EU27"][s] for s in SIZES), "el titular dice que en todos los tamaños"
    rows = [{"geo": s, "time": t, "value": round(prod[c][s], 1)} for s in SIZES for t, c in (("0-ue", "EU27"), ("1-espana", "ESP"))]
    return chart(
        id="pre3-europa-tamano",
        lens="europa", theme="productividad",
        title=bi(f"Las empresas españolas producen menos por persona que las europeas de su mismo tamaño; si el empleo se repartiera "
                 f"por tamaños como en la UE, la distancia solo se reduciría un {dec(explained, 'es', 0)} %",
                 f"Spanish firms produce less per person than European firms of the same size; if employment were spread across "
                 f"firm sizes as in the EU, the gap would shrink by only {dec(explained, 'en', 0)}%"),
        subtitle=bi(f"Valor añadido por persona ocupada según el tamaño de la empresa, {year}, miles de euros. Punto hueco: media de "
                    f"la UE; punto lleno: España",
                    f"Value added per person employed by firm size, {year}, thousand euros. Hollow dot: EU average; solid dot: Spain"),
        unit=bi("miles de euros por ocupado", "thousand euros per person employed"),
        source=_src("sbs_sc_ovw", EUROSTAT_SBS),
        notes={"es": ["Empresas de la industria, la construcción y los servicios de mercado. No incluye la agricultura, las "
                      "administraciones públicas, la educación ni la sanidad públicas, ni las finanzas.",
                      "En euros corrientes, sin corregir por el nivel de precios: en paridad de poder de compra la distancia con la "
                      "UE es menor, pero la parte que explica el tamaño no cambia, porque la corrección afecta igual a todos los "
                      "tamaños.",
                      "Tamaño: personas ocupadas en la empresa, incluidos los propietarios que trabajan en ella.",
                      f"Se usa {year}, el último año en que la UE publica todos los tamaños."],
               "en": ["Firms in industry, construction and market services. Excludes agriculture, public administration, public "
                      "education and health, and finance.",
                      "In current euros, not corrected for price levels: in purchasing power standards the gap with the EU is "
                      "smaller, but the share explained by firm size does not change, because the correction affects all sizes "
                      "equally.",
                      "Size: people employed in the firm, including working owners.",
                      f"{year} is used, the latest year in which the EU publishes all size classes."]},
        rows=rows,
        geos={k: {**label, "aggregate": True} for k, label in SIZES.items()},
        extra={"dimensions": {"time": {"0-ue": bi("Media de la UE", "EU average"), "1-espana": bi("España", "Spain")}},
               "year": year,
               "employment_share": {c: {s: round(100 * share[c][s], 1) for s in SIZES} for c in share},
               "total": {c: round(total[c], 1) for c in total},
               "with_eu_sizes": round(with_eu_sizes, 1), "gap": round(gap, 1), "explained_pct": explained},
    )


# ---------- España por dentro ----------

def _cre() -> tuple[dict, dict, dict]:
    """PIB (miles de euros), PIB por habitante (euros) y horas trabajadas (miles) por comunidad y año."""
    pib, pc, hours = {}, {}, {}
    for table, out in ((82284, pib), (82285, pc)):
        for r in sources.ine_table(table):
            if "Dato base" in r["series"]:
                c = ine_ccaa(r["series"].split(".")[0])
                if c:
                    out[(c, r["year"])] = r["value"]
    for r in sources.ine_table(82002):
        c = ine_ccaa(r["series"].split(".")[0])
        if c:
            hours[(c, r["year"])] = r["value"]
    return pib, pc, hours


def comunidades_pib():
    pib, pc, hours = _cre()
    year = max(y for (c, y) in pc if c == "ES")
    vals = {c: pc[(c, y)] for (c, y) in pc if y == year}
    rows = [{"geo": c, "time": str(year), "value": vals[c]} for c in sorted(vals)]
    main = [c for c in vals if c not in ("ES", *SMALL)]
    top, low = max(main, key=vals.get), min(main, key=vals.get)
    ratio = vals[top] / vals[low]
    return chart(
        id="prd1-comunidades-pib",
        lens="dentro", theme="productividad",
        title=bi(f"El PIB por habitante de {geo.ccaa_name(top, 'es')} ({_int(vals[top], 'es')} euros) es "
                 f"{dec(ratio, 'es', 2)} veces el de {geo.ccaa_name(low, 'es')} ({_int(vals[low], 'es')})",
                 f"GDP per person in {_en(top)} ({_int(vals[top], 'en')} euros) is {dec(ratio, 'en', 2)} times that of "
                 f"{_en(low)} ({_int(vals[low], 'en')})"),
        subtitle=bi(f"PIB por habitante, {year}, euros corrientes. España: {_int(vals['ES'], 'es')} euros",
                    f"GDP per person, {year}, current euros. Spain: {_int(vals['ES'], 'en')} euros"),
        unit=bi("euros por habitante", "euros per person"),
        source=INE_CRE,
        notes={"es": [f"Primera estimación del INE para {year}: se revisará.",
                      "El PIB se mide donde se produce y la población donde reside: las comunidades con muchos trabajadores que "
                      "viven en otra (Madrid) salen favorecidas, y las vecinas (Castilla-La Mancha), perjudicadas.",
                      "No corrige las diferencias de precios entre comunidades."],
               "en": [f"INE's first estimate for {year}: it will be revised.",
                      "GDP is measured where it is produced and population where people live: regions with many workers who live "
                      "in another region (Madrid) come out higher, and neighbouring ones (Castile-La Mancha) lower.",
                      "It does not correct for price differences between regions."]},
        rows=rows,
        geos=geo.ccaa_table(vals),
        extra={"year": year, "ratio": round(ratio, 2)},
    )


def comunidades_hora():
    pib, pc, hours = _cre()
    year = max(y for (c, y) in hours if c == "ES" and ("ES", y) in pib)
    cs = [c for (c, y) in hours if y == year and (c, y) in pib and (c, y) in pc]
    prod = {c: round(pib[(c, year)] / hours[(c, year)], 1) for c in cs}   # miles de euros / miles de horas = euros por hora
    pop = {c: pib[(c, year)] / pc[(c, year)] for c in cs}                  # miles de habitantes
    hpc = {c: hours[(c, year)] / pop[c] for c in cs}                       # horas por habitante
    # Índices España = 100: PIB por habitante = productividad por hora x horas por habitante
    idx = {c: {"pib": round(100 * pc[(c, year)] / pc[("ES", year)], 1), "hora": round(100 * prod[c] / prod["ES"], 1),
               "horas": round(100 * hpc[c] / hpc["ES"], 1)} for c in cs}
    rows = [{"geo": c, "time": str(year), "value": prod[c]} for c in sorted(cs)]
    main = [c for c in cs if c not in ("ES", *SMALL)]
    top, low = max(main, key=prod.get), min(main, key=prod.get)
    top_pc = max(main, key=lambda c: pc[(c, year)])
    low_pc = min(main, key=lambda c: pc[(c, year)])
    ratio_h = prod[top] / prod[low]
    ratio_pc = pc[(top_pc, year)] / pc[(low_pc, year)]
    assert ratio_h < ratio_pc, "el titular dice que la distancia es menor por hora"
    return chart(
        id="prd2-comunidades-hora",
        lens="dentro", theme="productividad",
        title=bi(f"Por hora trabajada, las diferencias son menores: {_es(top)} produce {dec(prod[top], 'es')} euros, "
                 f"{dec(ratio_h, 'es', 2)} veces lo que {geo.ccaa_name(low, 'es')} ({dec(prod[low], 'es')})",
                 f"Per hour worked, the differences are smaller: {_en(top)} produces {dec(prod[top], 'en')} euros, "
                 f"{dec(ratio_h, 'en', 2)} times as much as {_en(low)} ({dec(prod[low], 'en')})"),
        subtitle=bi(f"PIB por hora trabajada, {year}, euros corrientes. España: {dec(prod['ES'], 'es')} euros",
                    f"GDP per hour worked, {year}, current euros. Spain: {dec(prod['ES'], 'en')} euros"),
        unit=bi("euros por hora", "euros per hour"),
        source=INE_CRE,
        notes={"es": ["PIB de cada comunidad dividido entre las horas trabajadas en ella, de la Contabilidad Regional del INE.",
                      "El PIB por habitante es la productividad por hora multiplicada por las horas trabajadas por habitante: "
                      "«index» en la descarga da los tres índices de cada comunidad (España = 100).",
                      f"Primera estimación del INE para {year}: se revisará."],
               "en": ["Each region's GDP divided by the hours worked in it, from INE's Regional Accounts.",
                      "GDP per person equals productivity per hour multiplied by hours worked per person: «index» in the download "
                      "gives the three indices for each region (Spain = 100).",
                      f"INE's first estimate for {year}: it will be revised."]},
        rows=rows,
        geos=geo.ccaa_table(cs),
        extra={"year": year, "ratio_hour": round(ratio_h, 2), "ratio_pc": round(ratio_pc, 2),
               "hours_per_person": {c: round(hpc[c], 1) for c in cs},
               "index": idx},
    )


# ---------- España en el tiempo ----------

def tiempo_convergencia():
    pc = _gdp_pc()
    v = _lp()
    years = sorted(y for (c, y) in pc if c == "ESP" and ("ESP", "NLPR_HW", "PC_EU27_2020_MPPS_CP", y) in v)
    last = years[-1]
    gdp = {y: pc[("ESP", y)][0] for y in years}
    hour = {y: v[("ESP", "NLPR_HW", "PC_EU27_2020_MPPS_CP", y)] for y in years}
    rows = [{"time": str(y), "series": k, "value": d[y]} for k, d in (("pib", gdp), ("hora", hour)) for y in years]
    above = [y for y in years if gdp[y] > 100]
    assert above == list(range(above[0], above[-1] + 1)), "el titular habla de un único periodo por encima de la UE"
    peak = max(years, key=lambda y: gdp[y])
    since = above[-1] + 2
    top_since = max(gdp[y] for y in years if y >= since)
    # Crecimiento real de la productividad por hora (índice 2010 = 100, sin efecto de los precios)
    real = {c: {y: v[(c, "RLPR_HW", "I10", y)] for y in years if (c, "RLPR_HW", "I10", y) in v} for c in ("ESP", "EU27")}
    base = 2000
    growth = {c: round(100 * (real[c][last] / real[c][base] - 1), 1) for c in real}
    growth19 = {c: round(100 * (real[c][last] / real[c][2019] - 1), 1) for c in real}
    return chart(
        id="prt1-convergencia",
        lens="tiempo", theme="productividad",
        title=bi(f"El PIB por habitante de España superó la media de la UE entre {above[0]} y {above[-1]}, con un máximo del "
                 f"{dec(gdp[peak], 'es')} % en {peak}; desde {since} no ha pasado del {dec(top_since, 'es')} %",
                 f"Spain's GDP per person was above the EU average between {above[0]} and {above[-1]}, peaking at "
                 f"{dec(gdp[peak], 'en')}% in {peak}; since {since} it has not exceeded {dec(top_since, 'en')}%"),
        subtitle=bi(f"PIB por habitante y PIB por hora trabajada de España en paridad de poder de compra, {years[0]}-{last}. "
                    f"Índice: media de la UE = 100",
                    f"Spain's GDP per person and GDP per hour worked in purchasing power standards, {years[0]}-{last}. "
                    f"Index: EU average = 100"),
        unit=bi("índice, UE = 100", "index, EU = 100"),
        source={**_src("nama_10_pc", EUROSTAT_NA), "dataset": "nama_10_pc y nama_10_lp_ulc"},
        notes={"es": [PPS_NOTE["es"] + " Sirve para comparar países en cada año; la evolución en el tiempo es orientativa.",
                      "UE: los 27 países actuales en toda la serie.",
                      "«real_growth» en la descarga: crecimiento de la productividad por hora en volumen (sin el efecto de los "
                      f"precios) desde {base} y desde 2019, en España y en la UE."],
               "en": [PPS_NOTE["en"] + " It is designed to compare countries in each year; changes over time are indicative.",
                      "EU: the current 27 countries throughout the series.",
                      "«real_growth» in the download: growth in productivity per hour in volume terms (without the effect of "
                      f"prices) since {base} and since 2019, in Spain and the EU."]},
        rows=rows,
        extra={"dimensions": {"series": {"pib": bi("PIB por habitante", "GDP per person"),
                                         "hora": bi("PIB por hora trabajada", "GDP per hour worked")}},
               "short_labels": {"pib": bi("Por habitante", "Per person"), "hora": bi("Por hora", "Per hour")},
               "ref_line": {"value": 100, "label": bi("Media de la UE", "EU average")},
               "above_eu": above, "peak": {"year": peak, "value": gdp[peak]}, "max_since": {"year": since, "value": top_since},
               "workers_per_person": {str(y): v[("ESP", "EMP_HAB", "PC_EU27_2020", y)] for y in years
                                      if ("ESP", "EMP_HAB", "PC_EU27_2020", y) in v},
               "real_growth": {"since": base, "ESP": growth["ESP"], "EU27": growth["EU27"],
                               "since_2019": {"ESP": growth19["ESP"], "EU27": growth19["EU27"]}}},
    )


def tiempo_id():
    raw = sources.eurostat("rd_e_gerdfund", geo=["ES", "EU27_2020"], unit="PC_GDP", sectperf="TOTAL", sectfund=["TOTAL", "GOV", "BES"])
    v = {(geo.from_eurostat(r["geo"]), r["sectfund"], int(r["time"])): r["value"] for r in raw}
    years = sorted(y for (c, f, y) in v if c == "ESP" and f == "TOTAL" and ("EU27", "TOTAL", y) in v and y >= 2000)
    last = years[-1]
    series = {"espana": ("ESP", "TOTAL"), "ue": ("EU27", "TOTAL"), "publica": ("ESP", "GOV")}
    rows = [{"time": str(y), "series": k, "value": v[(c, f, y)]} for k, (c, f) in series.items() for y in years if (c, f, y) in v]
    es, eu = v[("ESP", "TOTAL", last)], v[("EU27", "TOTAL", last)]
    pub = {y: v[("ESP", "GOV", y)] for y in years if ("ESP", "GOV", y) in v}
    eu_bes_year = max(y for (c, f, y) in v if c == "EU27" and f == "BES")
    # Ranking de la UE en el último año
    tot = sources.eurostat("rd_e_gerdtot", unit="PC_GDP", sectperf="TOTAL", time=str(last))
    rank = {geo.from_eurostat(r["geo"]): r["value"] for r in tot if _is_eu(geo.from_eurostat(r["geo"]))}
    above = sorted((c for c in rank if c not in ("EU27", "ESP") and rank[c] > rank["ESP"]), key=lambda c: -rank[c])
    reg = sources.eurostat("rd_e_gerdreg", unit="PC_GDP", sectperf="TOTAL", geo=list(NUTS2), time=str(last))
    regions = {NUTS2[r["geo"]]: r["value"] for r in reg}
    perf = sources.eurostat("rd_e_gerdtot", unit="PC_GDP", sectperf=["TOTAL", "BES"], geo=["ES", "EU27_2020"], time=str(last))
    bes = {geo.from_eurostat(r["geo"]): r["value"] for r in perf if r["sectperf"] == "BES"}
    bes_share = round(100 * (bes["EU27"] - bes["ESP"]) / (eu - es), 1)
    assert 0.6 <= es / eu <= 0.7 and bes_share >= 80, (es / eu, bes_share)   # «dos tercios» y «casi toda»
    peak08 = max((y for y in years if y <= 2012), key=lambda y: v[("ESP", "TOTAL", y)])
    low = min((y for y in years if y > peak08), key=lambda y: v[("ESP", "TOTAL", y)])
    return chart(
        id="prt2-id",
        lens="tiempo", theme="productividad",
        title=bi(f"España dedica a I+D el {dec(es, 'es', 2)} % del PIB, dos tercios de lo que dedica la UE ({dec(eu, 'es', 2)} %); "
                 f"casi toda la diferencia está en el gasto de las empresas",
                 f"Spain spends {dec(es, 'en', 2)}% of GDP on R&D, two thirds of the EU figure ({dec(eu, 'en', 2)}%); almost all of "
                 f"the difference lies in business spending"),
        subtitle=bi(f"Gasto en I+D en % del PIB, {years[0]}-{last}. España y UE: gasto total; financiación pública: la parte que "
                    f"pagan las administraciones en España",
                    f"R&D spending as % of GDP, {years[0]}-{last}. Spain and EU: total spending; public funding: the share paid by "
                    f"government in Spain"),
        unit=bi("% del PIB", "% of GDP"),
        source={**_src("rd_e_gerdfund", EUROSTAT_RD), "dataset": "rd_e_gerdfund, rd_e_gerdtot y rd_e_gerdreg"},
        notes={"es": ["Gasto en I+D ejecutado en el país por empresas, administraciones, universidades e instituciones sin fines de "
                      "lucro, según quién lo realiza; la financiación pública es la parte de ese gasto que pagan las "
                      "administraciones, la ejecute quien la ejecute.",
                      "No incluye las deducciones fiscales por I+D ni la financiación pública de I+D hecha en el extranjero.",
                      "UE: estimaciones de Eurostat. «regions» en la descarga: gasto en I+D por comunidad en el último año."],
               "en": ["R&D spending carried out in the country by businesses, government, universities and non-profit institutions, "
                      "by who performs it; public funding is the part of that spending paid for by government, whoever carries it "
                      "out.",
                      "It does not include R&D tax credits or publicly funded R&D carried out abroad.",
                      "EU: Eurostat estimates. «regions» in the download: R&D spending by region in the latest year."]},
        rows=rows,
        extra={"dimensions": {"series": {"espana": bi("España", "Spain"), "ue": bi("UE", "EU"),
                                         "publica": bi("España, financiación pública", "Spain, public funding")}},
               "short_labels": {"espana": bi("España", "Spain"), "ue": bi("UE", "EU"),
                                "publica": bi("Financiación pública", "Public funding")},
               "year": last, "countries_above": above, "n": len(rank) - 1,
               "public": {str(y): pub[y] for y in years if y >= 2019 and y in pub},
               "business_funded": {"ESP": v.get(("ESP", "BES", last)), "EU27": v.get(("EU27", "BES", eu_bes_year)),
                                   "EU27_year": eu_bes_year},
               "public_eu": {"year": max(y for (c, f, y) in v if c == "EU27" and f == "GOV"),
                             "value": v[("EU27", "GOV", max(y for (c, f, y) in v if c == "EU27" and f == "GOV"))]},
               "business_performed": {"ESP": bes["ESP"], "EU27": bes["EU27"], "share_of_gap": bes_share},
               "peak_2008": {"year": peak08, "value": v[("ESP", "TOTAL", peak08)]},
               "low": {"year": low, "value": v[("ESP", "TOTAL", low)]},
               "regions": dict(sorted(regions.items()))},
    )


BUILDERS = [europa_pib, europa_brecha, europa_tamano, comunidades_pib, comunidades_hora, tiempo_convergencia, tiempo_id]
