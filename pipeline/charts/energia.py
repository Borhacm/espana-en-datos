"""Tema Energía (código EN): precio de la luz de los hogares frente a la UE y de qué se compone, hogares que no pueden
calentar su vivienda, gasto en energía por comunidad, cómo ha cambiado la generación eléctrica y la dependencia energética."""

from collections import defaultdict

from lib import geo, sources
from lib.output import THEMES, chart

from .common import bi, dec, ine_ccaa

THEMES["energia"] = {"code": "EN", "title": "Energía"}

EUROSTAT_PRICES = {"name": "Eurostat, precios de la electricidad para los hogares", "license": "CC BY 4.0"}
EUROSTAT_SILC = {"name": "Eurostat, encuesta de condiciones de vida (EU-SILC)", "license": "CC BY 4.0"}
EUROSTAT_BAL = {"name": "Eurostat, balances energéticos", "license": "CC BY 4.0"}
INE_LICENSE = "Reutilización libre citando la fuente"
SMALL = ("18", "19")   # Ceuta y Melilla: muestras muy pequeñas, no protagonizan titulares

BAND = "KWH2500-4999"   # consumo anual de 2.500 a 5.000 kWh: el hogar tipo de Eurostat


def _src(dataset: str, base: dict) -> dict:
    return {**base, "dataset": dataset, "url": f"https://ec.europa.eu/eurostat/databrowser/view/{dataset}/default/table"}


def _int(v: float, lang: str) -> str:
    """Entero con separador de miles: 1.563 en español, 1,563 en inglés."""
    s = f"{round(v):,}"
    return s.replace(",", ".") if lang == "es" else s


def _en(code: str) -> str:
    """Nombre inglés de una comunidad con artículo cuando lo lleva (the Canary Islands)."""
    name = geo.ccaa_name(code, "en")
    return f"the {name}" if code in ("04", "05", "10", "16") else name


def _is_eu(c: str) -> bool:
    return c == "EU27" or geo.COUNTRIES.get(c, (0, 0, 0, False))[3]


def _sem_time(s: str) -> float:
    """'2025-S2' -> 2025.5; '2025-S1' -> 2025."""
    y, h = s.split("-S")
    return int(y) + (0.5 if h == "2" else 0)


def _tkey(t: float) -> str:
    """Clave de tiempo tal como la escribe el navegador (String(2025) = "2025", String(2025.5) = "2025.5")."""
    return str(int(t)) if t == int(t) else str(t)


def _sem_label(s: str) -> dict:
    y, h = s.split("-S")
    return bi(f"{'Primer' if h == '1' else 'Segundo'} semestre de {y}", f"H{h} {y}")


PRICE_NOTE = {
    "es": "Precio medio de la electricidad para los hogares con un consumo de 2.500 a 5.000 kWh al año (la banda de consumo "
          "más habitual en la UE), con todos los impuestos. Incluye la parte fija (potencia) y la variable (energía) de la factura.",
    "en": "Average electricity price for households consuming 2,500 to 5,000 kWh a year (the most common consumption band in "
          "the EU), including all taxes. It includes the fixed (capacity) and variable (energy) parts of the bill.",
}


def _prices():
    raw = sources.eurostat("nrg_pc_204", nrg_cons=BAND, unit="KWH", tax="I_TAX", currency=["EUR", "PPS"])
    return {(geo.from_eurostat(r["geo"]), r["currency"], r["time"]): r["value"] for r in raw if geo.from_eurostat(r["geo"])}


# ---------- España frente a Europa ----------

def europa_precio():
    v = _prices()
    sems = sorted({t for (c, cur, t) in v if c == "EU27" and cur == "EUR" and ("ESP", "EUR", t) in v})
    last2 = sems[-2:]

    def mean(c, cur):
        return round(100 * sum(v[(c, cur, t)] for t in last2) / 2, 1)   # céntimos de euro

    eur = {c: mean(c, "EUR") for (c, cur, t) in v if cur == "EUR" and _is_eu(c) and all((c, "EUR", s) in v for s in last2)}
    pps = {c: mean(c, "PPS") for (c, cur, t) in v if cur == "PPS" and _is_eu(c) and all((c, "PPS", s) in v for s in last2)}
    rows = [{"geo": c, "time": "ultimo", "value": eur[c]} for c in sorted(eur)]
    ranked = sorted((c for c in eur if c != "EU27"), key=lambda c: -eur[c])
    n = len(ranked)
    above = [c for c in ranked if eur[c] > eur["ESP"]]
    ranked_pps = sorted((c for c in pps if c != "EU27"), key=lambda c: -pps[c])
    above_pps = [c for c in ranked_pps if pps[c] > pps["ESP"]]
    period = bi(f"{_sem_label(last2[0])['es'].lower()} y {_sem_label(last2[1])['es'].lower()}",
                f"{_sem_label(last2[0])['en']} and {_sem_label(last2[1])['en']}")
    es, eu = eur["ESP"], eur["EU27"]
    return chart(
        id="ene1-europa-precio",
        lens="europa", theme="energia",
        title=bi(f"Los hogares españoles pagan la luz a {dec(es, 'es')} céntimos el kWh, por debajo de la media de la UE "
                 f"({dec(eu, 'es')}): {len(above)} de los {n} países la pagan más cara",
                 f"Spanish households pay {dec(es, 'en')} cents per kWh for electricity, below the EU average ({dec(eu, 'en')}): "
                 f"{len(above)} of the {n} countries pay more"),
        subtitle=bi(f"Precio de la electricidad para los hogares con todos los impuestos, céntimos de euro por kWh. Media del "
                    f"{period['es']}",
                    f"Household electricity price including all taxes, euro cents per kWh. Average of {period['en']}"),
        unit=bi("céntimos por kWh", "cents per kWh"),
        source=_src("nrg_pc_204", EUROSTAT_PRICES),
        notes={"es": [PRICE_NOTE["es"],
                      "Media de los dos últimos semestres publicados, para no depender de la estación del año.",
                      "En euros no se tiene en cuenta que el nivel de precios y de salarios es distinto en cada país. En paridad de "
                      "poder de compra (PPA), que lo corrige, España queda prácticamente en la media de la UE."],
               "en": [PRICE_NOTE["en"],
                      "Average of the last two half-years published, so as not to depend on the season.",
                      "Figures in euros do not take into account that price and wage levels differ between countries. In "
                      "purchasing power standards (PPS), which correct for this, Spain is practically at the EU average."]},
        rows=rows,
        geos=geo.country_table(eur),
        extra={"dimensions": {"time": {"ultimo": bi("Último año", "Last year")}},
               "semesters": last2, "countries_above": above,
               "pps": {"ESP": pps["ESP"], "EU27": pps["EU27"], "countries_above": above_pps, "n": len(ranked_pps)}},
    )


COMPONENTS = {
    "energia": bi("Energía y suministro", "Energy and supply"),
    "redes": bi("Redes", "Networks"),
    "impuestos": bi("Impuestos sin IVA", "Taxes excl. VAT"),
    "iva": bi("IVA", "VAT"),
}
TAX_PARTS = ["TAX_CAP", "TAX_ENV", "TAX_RNW", "TAX_NUC", "OTH"]


def europa_componentes():
    items = ["NRG_SUP", "NETC", "TAX_FEE_LEV_CHRG", "VAT", *TAX_PARTS]
    raw = sources.eurostat("nrg_pc_204_c", nrg_cons=BAND, currency="EUR", geo=["ES", "EU27_2020"], nrg_prc=items)
    v = {(geo.from_eurostat(r["geo"]), r["nrg_prc"], int(r["time"])): r["value"] for r in raw}
    year = max(y for (c, i, y) in v if c == "EU27" and i == "NRG_SUP" and ("ESP", "NRG_SUP", y) in v)
    g = {}
    for c in ("ESP", "EU27"):
        taxes = v[(c, "TAX_FEE_LEV_CHRG", year)]
        # «Impuestos, tasas y cargos» de Eurostat incluye el IVA: es la suma de sus partidas
        assert abs(taxes - v[(c, "VAT", year)] - sum(v.get((c, i, year), 0) for i in TAX_PARTS)) < 0.0005, (c, taxes)
        g[c] = {"energia": v[(c, "NRG_SUP", year)], "redes": v[(c, "NETC", year)],
                "impuestos": taxes - v[(c, "VAT", year)], "iva": v[(c, "VAT", year)]}
    cents = {c: {k: round(100 * x, 1) for k, x in g[c].items()} for c in g}
    total = {c: round(100 * sum(g[c].values()), 1) for c in g}
    gap = {k: round(100 * (g["EU27"][k] - g["ESP"][k]), 1) + 0.0 for k in COMPONENTS}
    rows = [{"geo": k, "time": t, "value": cents[c][k]} for k in COMPONENTS for t, c in (("0-ue", "EU27"), ("1-espana", "ESP"))]
    return chart(
        id="ene2-europa-componentes",
        lens="europa", theme="energia",
        title=bi(f"La luz es más barata en España por la energía ({dec(cents['ESP']['energia'], 'es')} céntimos el kWh frente a "
                 f"{dec(cents['EU27']['energia'], 'es')}) y por las redes; en impuestos, los hogares pagan casi lo mismo que en la UE",
                 f"Electricity is cheaper in Spain because of energy ({dec(cents['ESP']['energia'], 'en')} cents per kWh against "
                 f"{dec(cents['EU27']['energia'], 'en')}) and networks; in taxes, households pay almost the same as in the EU"),
        subtitle=bi(f"Precio de la electricidad para los hogares por componentes, {year}, céntimos de euro por kWh. Punto hueco: "
                    f"media de la UE; punto lleno: España",
                    f"Household electricity price by component, {year}, euro cents per kWh. Hollow dot: EU average; "
                    f"solid dot: Spain"),
        unit=bi("céntimos por kWh", "cents per kWh"),
        source=_src("nrg_pc_204_c", EUROSTAT_PRICES),
        notes={"es": ["Hogares con un consumo de 2.500 a 5.000 kWh al año. Datos anuales.",
                      "Energía y suministro: lo que cuesta producir o comprar la electricidad y comercializarla. Redes: transporte y "
                      "distribución. Impuestos sin IVA: impuesto sobre la electricidad y otros tributos y cargos regulados.",
                      "Las partidas de Eurostat no coinciden exactamente con las de la factura española (peajes, cargos, impuesto "
                      "especial e IVA): cada país asigna sus cargos regulados a una u otra partida.",
                      "Las partidas están redondeadas a un decimal y su suma puede no coincidir con el total."],
               "en": ["Households consuming 2,500 to 5,000 kWh a year. Annual data.",
                      "Energy and supply: the cost of producing or buying electricity and selling it on. Networks: transmission and "
                      "distribution. Taxes excl. VAT: electricity tax and other taxes, levies and regulated charges.",
                      "Eurostat's components do not match the Spanish bill exactly (network tolls, regulated charges, electricity tax "
                      "and VAT): each country assigns its regulated charges to one component or another.",
                      "Components are rounded to one decimal place and may not add up to the total."]},
        rows=rows,
        geos={k: {**label, "aggregate": True} for k, label in COMPONENTS.items()},
        extra={"dimensions": {"time": {"0-ue": bi("Media de la UE", "EU average"), "1-espana": bi("España", "Spain")}},
               "year": year, "components": cents, "total": total, "gap": gap, "gap_total": round(total["EU27"] - total["ESP"], 1)},
    )


COLD_NOTE = {
    "es": "Hogares que declaran que no pueden permitirse mantener la vivienda a una temperatura adecuada en invierno. Es una "
          "respuesta a una encuesta, no una medida de temperatura ni de gasto.",
    "en": "Households reporting that they cannot afford to keep their home adequately warm in winter. It is a survey answer, "
          "not a measure of temperature or spending.",
}


def europa_frio():
    raw = sources.eurostat("ilc_mdes01", hhcomp="TOTAL", rskpovth="TOTAL", unit="PC")
    v = {(geo.from_eurostat(r["geo"]), int(r["time"])): r["value"] for r in raw if geo.from_eurostat(r["geo"])}
    year = max(y for (c, y) in v if c == "EU27" and ("ESP", y) in v)
    rows = sorted(({"geo": c, "time": str(y), "value": val} for (c, y), val in v.items() if y == year and _is_eu(c)),
                  key=lambda r: r["geo"])
    ranked = sorted((r for r in rows if r["geo"] != "EU27"), key=lambda r: -r["value"])
    es, eu = v[("ESP", year)], v[("EU27", year)]
    above = [r["geo"] for r in ranked if r["value"] > es]
    n = len(ranked)
    base = 2019
    return chart(
        id="ene3-europa-frio",
        lens="europa", theme="energia",
        title=bi(f"El {dec(es, 'es')} % de los españoles vive en hogares que no pueden mantener la casa caliente, frente al "
                 f"{dec(eu, 'es')} % en la UE: solo {len(above)} de los {n} países tienen un porcentaje más alto",
                 f"{dec(es, 'en')}% of Spaniards live in households that cannot keep their home warm, against {dec(eu, 'en')}% in "
                 f"the EU: only {len(above)} of the {n} countries have a higher share"),
        subtitle=bi(f"Población que vive en hogares que no pueden permitirse mantener la vivienda a una temperatura adecuada, {year}, en %",
                    f"Population living in households that cannot afford to keep their home adequately warm, {year}, in %"),
        unit=bi("% de la población", "% of population"),
        source=_src("ilc_mdes01", EUROSTAT_SILC),
        notes={"es": [COLD_NOTE["es"],
                      "Porcentaje de personas, no de hogares. La encuesta se hace a lo largo del año y pregunta por la situación del "
                      "hogar en ese momento."],
               "en": [COLD_NOTE["en"],
                      "Share of people, not of households. The survey is carried out throughout the year and asks about the "
                      "household's situation at that time."]},
        rows=rows,
        geos=geo.country_table(r["geo"] for r in rows),
        extra={"countries_above": above,
               "history": {str(y): {"ESP": v[("ESP", y)], "EU27": v[("EU27", y)]} for y in range(base, year + 1)
                           if ("ESP", y) in v and ("EU27", y) in v}},
    )


# ---------- España por dentro ----------

COLD_TABLE = 9975   # INE, ECV: hogares con carencia material por comunidad autónoma
EPF_TABLE3 = 73992  # INE, EPF: gasto por subgrupos (3 dígitos) y comunidad
EPF_TABLE4 = 73993  # INE, EPF: gasto por códigos (4 dígitos) y comunidad


def comunidades_frio():
    t = defaultdict(dict)
    for r in sources.ine_table(COLD_TABLE):
        if "temperatura adecuada" in r["series"]:
            c = ine_ccaa(r["series"].split(". ")[-1])
            if c:
                t[c][r["year"]] = r["value"]
    last = max(t["ES"])
    years = [last - 2, last - 1, last]
    avg = {c: round(sum(t[c][y] for y in years) / 3, 1) for c in t if all(y in t[c] for y in years)}
    rows = [{"geo": c, "time": f"{years[0]}-{last}", "value": avg[c]} for c in sorted(avg)]
    main = [c for c in avg if c not in ("ES", *SMALL)]
    top, low = max(main, key=lambda c: avg[c]), min(main, key=lambda c: avg[c])
    period = f"{years[0]}-{last}"
    return chart(
        id="end1-comunidades-frio",
        lens="dentro", theme="energia",
        title=bi(f"En {geo.ccaa_name(top, 'es')}, el {dec(avg[top], 'es')} % de los hogares no puede mantener la casa caliente; "
                 f"en {geo.ccaa_name(low, 'es')}, el {dec(avg[low], 'es')} %",
                 f"In {_en(top)}, {dec(avg[top], 'en')}% of households cannot keep their home warm; in "
                 f"{_en(low)}, {dec(avg[low], 'en')}%"),
        subtitle=bi(f"Hogares que no pueden permitirse mantener la vivienda a una temperatura adecuada, media {period}, en %. "
                    f"España: {dec(avg['ES'], 'es')} %",
                    f"Households that cannot afford to keep their home adequately warm, {period} average, in %. "
                    f"Spain: {dec(avg['ES'], 'en')}%"),
        unit=bi("% de los hogares", "% of households"),
        source={"name": "INE, Encuesta de Condiciones de Vida", "dataset": f"Tabla {COLD_TABLE}",
                "url": f"https://www.ine.es/jaxiT3/Tabla.htm?t={COLD_TABLE}", "license": INE_LICENSE},
        notes={"es": [COLD_NOTE["es"],
                      "Media de los tres últimos años: la muestra de cada comunidad es pequeña y el dato de un solo año varía mucho. "
                      "Ceuta y Melilla tienen muestras aún más pequeñas.",
                      "Porcentaje de hogares (el de Eurostat del gráfico anterior es de personas)."],
               "en": [COLD_NOTE["en"],
                      "Average of the last three years: each region's sample is small and a single year's figure varies a lot. "
                      "Ceuta and Melilla have even smaller samples.",
                      "Share of households (the Eurostat figure in the previous chart is of people)."]},
        rows=rows,
        geos=geo.ccaa_table(avg),
        extra={"dimensions": {"time": {period: bi(f"Media {period}", f"{period} average")}},
               "years": {c: {str(y): t[c][y] for y in years} for c in avg}},
    )


def comunidades_gasto():
    total, share = {}, {}
    for r in sources.ine_table(EPF_TABLE3):
        s = r["series"]
        if "Electricidad, gas y otros combustibles. Dato base" not in s:
            continue
        c = ine_ccaa(s.split(". ")[0])
        if not c:
            continue
        if s.endswith("Gasto medio por hogar"):
            total.setdefault(c, {})[r["year"]] = r["value"]
        elif s.endswith("Distribución porcentual"):
            share.setdefault(c, {})[r["year"]] = r["value"]
    year = max(total["ES"])
    elec = {}
    for r in sources.ine_table(EPF_TABLE4):
        parts = r["series"].split(". ")
        if r["year"] == year and len(parts) > 2 and parts[1] == "Electricidad" and "Gasto medio por hogar" in r["series"]:
            c = ine_ccaa(parts[0])
            if c:
                elec[c] = r["value"]
    codes = sorted(c for c in total if year in total[c])
    tot = {c: round(total[c][year]) for c in codes}
    rows = [{"geo": c, "time": str(year), "value": tot[c]} for c in codes]
    main = [c for c in codes if c not in ("ES", *SMALL)]
    top, low = max(main, key=lambda c: tot[c]), min(main, key=lambda c: tot[c])
    elec_share = {c: round(100 * elec[c] / total[c][year], 1) for c in codes if c in elec}
    budget = {c: share[c][year] for c in codes if year in share.get(c, {})}
    return chart(
        id="end2-comunidades-gasto",
        lens="dentro", theme="energia",
        title=bi(f"Los hogares de {geo.ccaa_name(top, 'es')} gastan {_int(tot[top], 'es')} euros al año en luz, gas y otros "
                 f"combustibles para la vivienda; los de {geo.ccaa_name(low, 'es')}, {_int(tot[low], 'es')}",
                 f"Households in {_en(top)} spend {_int(tot[top], 'en')} euros a year on electricity, gas and "
                 f"other fuels for the home; those in {_en(low)}, {_int(tot[low], 'en')}"),
        subtitle=bi(f"Gasto medio por hogar en electricidad, gas y otros combustibles de la vivienda, {year}, euros. "
                    f"España: {_int(tot['ES'], 'es')} euros",
                    f"Average spending per household on electricity, gas and other household fuels, {year}, euros. "
                    f"Spain: {_int(tot['ES'], 'en')} euros"),
        unit=bi("euros por hogar", "euros per household"),
        source={"name": "INE, Encuesta de Presupuestos Familiares", "dataset": f"Tablas {EPF_TABLE3} y {EPF_TABLE4}",
                "url": f"https://www.ine.es/jaxiT3/Tabla.htm?t={EPF_TABLE3}", "license": INE_LICENSE},
        notes={"es": ["Gasto de los hogares en la electricidad, el gas (natural y butano o propano), el gasóleo y otros combustibles "
                      "de su vivienda principal. No incluye el combustible del coche.",
                      "Gasto por hogar: depende también del tamaño de los hogares y de las viviendas de cada comunidad.",
                      "Las ayudas como el bono social reducen la factura y, por tanto, el gasto que declara el hogar."],
               "en": ["Household spending on electricity, gas (natural gas and butane or propane), heating oil and other fuels for "
                      "their main home. It does not include car fuel.",
                      "Spending per household: it also depends on the size of households and homes in each region.",
                      "Support such as the bono social (Spain's discounted electricity tariff for vulnerable households) reduces "
                      "the bill and therefore the spending households report."]},
        rows=rows,
        geos=geo.ccaa_table(codes),
        extra={"electricity_share": elec_share, "budget_share": budget,
               "electricity": {c: round(elec[c]) for c in elec}},
    )


# ---------- España en el tiempo ----------

TECH = {
    "solar": (["RA410", "RA420"], bi("Solar", "Solar")),
    "eolica": (["RA300"], bi("Eólica", "Wind")),
    "nuclear": (["N900H"], bi("Nuclear", "Nuclear")),
    "gas": (["G3000"], bi("Gas natural", "Natural gas")),
    "carbon": (["C0000X0350-0370"], bi("Carbón", "Coal")),
}


def tiempo_generacion():
    siec = ["TOTAL", "RA000", "RA100", *(s for parts, _ in TECH.values() for s in parts)]
    raw = sources.eurostat("nrg_bal_peh", geo="ES", nrg_bal="GEP", unit="GWH", siec=siec)
    v = {(r["siec"], int(r["time"])): r["value"] for r in raw}
    years = sorted(y for (s, y) in v if s == "TOTAL" and y >= 2000)
    last = years[-1]
    sh = {k: {y: round(100 * sum(v.get((s, y), 0) for s in parts) / v[("TOTAL", y)], 1) for y in years}
          for k, (parts, _) in TECH.items()}
    ren = {y: round(100 * v[("RA000", y)] / v[("TOTAL", y)], 1) for y in years}
    hydro = {y: round(100 * v[("RA100", y)] / v[("TOTAL", y)], 1) for y in years}
    rows = [{"time": str(y), "series": k, "value": sh[k][y]} for k in TECH for y in years]
    base = 2019
    first = years[0]
    leader = max(TECH, key=lambda k: sh[k][last])
    assert max(TECH, key=lambda k: sh[k][first]) == "carbon", "el titular dice que el carbón era la primera fuente"
    ren_raw = sources.eurostat("nrg_ind_ren", geo=["ES", "EU27_2020"], unit="PC", nrg_bal=["REN", "REN_ELC", "REN_TRA", "REN_HEAT_CL"])
    red = {(r["nrg_bal"], geo.from_eurostat(r["geo"]), int(r["time"])): r["value"] for r in ren_raw}
    red_last = max(y for (b, c, y) in red if b == "REN" and c == "ESP")
    return chart(
        id="ent1-generacion",
        lens="tiempo", theme="energia",
        title=bi(f"La solar ha pasado del {dec(sh['solar'][base], 'es')} % de la electricidad generada en {base} al "
                 f"{dec(sh['solar'][last], 'es')} % en {last}; el carbón, que era la primera fuente en {first} "
                 f"({dec(sh['carbon'][first], 'es')} %), ha caído al {dec(sh['carbon'][last], 'es')} %",
                 f"Solar has risen from {dec(sh['solar'][base], 'en')}% of electricity generated in {base} to "
                 f"{dec(sh['solar'][last], 'en')}% in {last}; coal, the leading source in {first} "
                 f"({dec(sh['carbon'][first], 'en')}%), has fallen to {dec(sh['carbon'][last], 'en')}%"),
        subtitle=bi(f"Producción bruta de electricidad por fuente, en % del total, {first}-{last}",
                    f"Gross electricity production by source, as % of the total, {first}-{last}"),
        unit=bi("% de la producción", "% of production"),
        source=_src("nrg_bal_peh", EUROSTAT_BAL),
        notes={"es": ["Producción bruta: incluye la de las centrales, la de las instalaciones de autoconsumo que se miden y la del "
                      "bombeo. Por eso los porcentajes pueden diferir algo de los de Red Eléctrica.",
                      "Solar: fotovoltaica y termosolar. No se muestran la hidráulica, que varía mucho de un año a otro según la lluvia, "
                      "el petróleo (sobre todo en las islas), la biomasa, los residuos ni la cogeneración con otros combustibles."],
               "en": ["Gross production: includes power plants, metered self-consumption installations and pumped storage. "
                      "Percentages may therefore differ slightly from those of Red Eléctrica, the grid operator.",
                      "Solar: photovoltaic and solar thermal. Not shown: hydro, which varies a lot from year to year depending on "
                      "rainfall, oil (mainly on the islands), biomass, waste and cogeneration with other fuels."]},
        rows=rows,
        extra={"dimensions": {"series": {k: label for k, (_, label) in TECH.items()}},
               "short_labels": {k: label for k, (_, label) in TECH.items()},
               "leader": leader, "renewable_share": {str(y): ren[y] for y in years},
               "hydro_share": {str(y): hydro[y] for y in years},
               "red_share": {"year": red_last,
                             "final": {str(y): red[("REN", "ESP", y)] for y in range(base, red_last + 1) if ("REN", "ESP", y) in red},
                             "final_eu": red.get(("REN", "EU27", red_last)),
                             "electricity": {"ESP": red.get(("REN_ELC", "ESP", red_last)),
                                             "EU27": red.get(("REN_ELC", "EU27", red_last))},
                             "transport_heating": {b: {str(y): red[(b, "ESP", y)] for y in range(base, red_last + 1)
                                                       if (b, "ESP", y) in red} for b in ("REN_TRA", "REN_HEAT_CL")}}},
    )


def tiempo_precio():
    v = _prices()
    sems = sorted((t for (c, cur, t) in v if c == "ESP" and cur == "EUR" and ("EU27", "EUR", t) in v), key=_sem_time)
    rows = [{"time": _tkey(_sem_time(t)), "series": k, "value": round(100 * v[(c, "EUR", t)], 1)}
            for k, c in (("espana", "ESP"), ("ue", "EU27")) for t in sems]
    es = {t: v[("ESP", "EUR", t)] for t in sems}
    eu = {t: v[("EU27", "EUR", t)] for t in sems}
    # Último tramo continuo con España por encima de la UE y desde cuándo está por debajo
    below_since = None
    for t in reversed(sems):
        if es[t] < eu[t]:
            below_since = t
        else:
            break
    assert below_since.endswith("-S1"), "el titular cuenta años completos por debajo"
    i = sems.index(below_since) - 1
    above_end = sems[i]
    j = i
    while j > 0 and es[sems[j - 1]] >= eu[sems[j - 1]]:
        j -= 1
    above_start = sems[j]
    peak = max(sems, key=lambda t: es[t])
    last = sems[-1]
    half2 = above_start.endswith("-S2")
    start_es = f"la segunda mitad de {above_start[:4]}" if half2 else above_start[:4]
    start_en = f"the second half of {above_start[:4]}" if half2 else above_start[:4]
    lab = {t: _sem_label(t) for t in sems}
    return chart(
        id="ent2-precio",
        lens="tiempo", theme="energia",
        title=bi(f"La luz de los hogares fue más cara en España que en la media de la UE desde {start_es} hasta {above_end[:4]}; "
                 f"desde {below_since[:4]} es más barata",
                 f"Household electricity was more expensive in Spain than the EU average from {start_en} until {above_end[:4]}; "
                 f"since {below_since[:4]} it has been cheaper"),
        subtitle=bi(f"Precio de la electricidad para los hogares con todos los impuestos, céntimos de euro por kWh, por semestres, "
                    f"{lab[sems[0]]['es'].lower()} a {lab[last]['es'].lower()}",
                    f"Household electricity price including all taxes, euro cents per kWh, by half-year, {lab[sems[0]]['en']} to "
                    f"{lab[last]['en']}"),
        unit=bi("céntimos por kWh", "cents per kWh"),
        source=_src("nrg_pc_204", EUROSTAT_PRICES),
        notes={"es": [PRICE_NOTE["es"],
                      "Hasta 2017, Eurostat calculaba estos precios con reglas algo distintas; la comparación entre España y la UE "
                      "en cada momento sí es homogénea.",
                      "UE: los 27 países actuales en toda la serie. Precios corrientes, sin descontar la inflación."],
               "en": [PRICE_NOTE["en"],
                      "Until 2017, Eurostat calculated these prices using slightly different rules; the comparison between Spain "
                      "and the EU at each point in time is consistent.",
                      "EU: the current 27 countries throughout the series. Current prices, not adjusted for inflation."]},
        rows=rows,
        extra={"dimensions": {"series": {"espana": bi("España", "Spain"), "ue": bi("UE", "EU")}},
               "time_labels": {_tkey(_sem_time(t)): lab[t] for t in sems},
               "above": {"start": above_start, "end": above_end}, "below_since": below_since,
               "peak": {"time": peak, "ESP": round(100 * es[peak], 1), "EU27": round(100 * eu[peak], 1)}},
    )


def tiempo_dependencia():
    raw = sources.eurostat("nrg_ind_id", geo=["ES", "EU27_2020"], siec=["TOTAL", "G3000", "O4000XBIO", "C0000X0350-0370"])
    v = {(r["siec"], geo.from_eurostat(r["geo"]), int(r["time"])): r["value"] for r in raw}
    years = sorted(y for (s, c, y) in v if s == "TOTAL" and c == "ESP" and ("TOTAL", "EU27", y) in v and y >= 2000)
    last = years[-1]
    es = {y: round(v[("TOTAL", "ESP", y)], 1) for y in years}
    eu = {y: round(v[("TOTAL", "EU27", y)], 1) for y in years}
    rows = [{"time": str(y), "series": k, "value": d[y]} for k, d in (("espana", es), ("ue", eu)) for y in years]
    peak = max(years, key=lambda y: es[y])
    gap = round(es[last] - eu[last], 1)
    return chart(
        id="ent3-dependencia",
        lens="tiempo", theme="energia",
        title=bi(f"España importó en {last} el {dec(es[last], 'es')} % de la energía que utiliza, frente al {dec(es[peak], 'es')} % "
                 f"de {peak}; sigue {dec(gap, 'es')} puntos por encima de la UE",
                 f"In {last}, Spain imported {dec(es[last], 'en')}% of the energy it uses, down from {dec(es[peak], 'en')}% in {peak}; "
                 f"it remains {dec(gap, 'en')} points above the EU"),
        subtitle=bi(f"Dependencia energética: importaciones netas en % de la energía disponible, {years[0]}-{last}",
                    f"Energy import dependency: net imports as % of available energy, {years[0]}-{last}"),
        unit=bi("% de la energía disponible", "% of available energy"),
        source=_src("nrg_ind_id", EUROSTAT_BAL),
        notes={"es": ["Importaciones menos exportaciones de todos los productos energéticos, en % de la energía bruta disponible "
                      "(producción más importaciones netas y variación de existencias).",
                      "Por convenio estadístico, la energía nuclear cuenta como producción propia aunque el uranio se importe.",
                      "UE: dependencia del conjunto de los 27 frente al resto del mundo, no la media de los países."],
               "en": ["Imports minus exports of all energy products, as % of gross available energy (production plus net imports "
                      "and stock changes).",
                      "By statistical convention, nuclear energy counts as domestic production even though the uranium is imported.",
                      "EU: dependency of the 27 as a whole on the rest of the world, not the average of the countries."]},
        rows=rows,
        extra={"dimensions": {"series": {"espana": bi("España", "Spain"), "ue": bi("UE", "EU")}},
               "peak": {"year": peak, "value": es[peak]}, "gap": gap,
               "by_fuel": {s: {"ESP": round(v[(s, "ESP", last)], 1), "EU27": round(v[(s, "EU27", last)], 1)}
                           for s in ("G3000", "O4000XBIO", "C0000X0350-0370") if (s, "ESP", last) in v}},
    )


BUILDERS = [europa_precio, europa_componentes, europa_frio, comunidades_frio, comunidades_gasto,
            tiempo_generacion, tiempo_precio, tiempo_dependencia]
