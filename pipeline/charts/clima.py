"""Tema Clima (código CL): emisiones de gases de efecto invernadero por habitante y por sector frente a la UE, emisiones por
comunidad, días de calor (grados-día de refrigeración) por comunidad, evolución de las emisiones frente al objetivo de 2030 y
al PIB, y reservas de agua embalsada desde 1988."""

import collections
import zipfile

from lib import geo, sources
from lib.http import RAW_DIR, fetch
from lib.output import THEMES, chart

from .common import bi, dec, pct
from .educacion import NUTS2

THEMES["clima"] = {"code": "CL", "title": "Clima"}

EUROSTAT_GHG = {"name": "Eurostat, inventario de gases de efecto invernadero (AEMA)", "license": "CC BY 4.0"}
EUROSTAT_POP = {"name": "Eurostat, estadísticas de población", "license": "CC BY 4.0"}
EUROSTAT_NA = {"name": "Eurostat, cuentas nacionales", "license": "CC BY 4.0"}
EUROSTAT_DD = {"name": "Eurostat, grados-día de calefacción y refrigeración", "license": "CC BY 4.0"}
MITECO_LICENSE = "Reutilización libre citando la fuente (Ley 37/2007)"
MITECO_CCAA_URL = ("https://www.miteco.gob.es/content/dam/miteco/es/calidad-y-evaluacion-ambiental/temas/"
                   "sistema-espanol-de-inventario-sei-/otra-informacion/emisiones-crt-gei-ccaa-prov-1990-2024.zip")
MITECO_CCAA = {"name": "MITECO, Inventario Nacional de Emisiones de GEI desagregado por comunidades autónomas",
               "dataset": "Edición 2026, serie 1990-2024",
               "url": "https://www.miteco.gob.es/es/calidad-y-evaluacion-ambiental/temas/sistema-espanol-de-inventario-sei-/"
                      "otra-informacion/inv-gei-ccaa.html",
               "license": MITECO_LICENSE}
EMB_URL = ("https://www.miteco.gob.es/content/dam/miteco/es/agua/temas/evaluacion-de-los-recursos-hidricos/"
           "boletin-hidrologico/Historico-de-embalses/BD-Embalses.zip")
MITECO_EMB = {"name": "MITECO, Boletín Hidrológico: histórico de embalses",
              "dataset": "BD-Embalses (reserva semanal de cada embalse)",
              "url": "https://www.miteco.gob.es/es/agua/temas/evaluacion-de-los-recursos-hidricos/boletin-hidrologico.html",
              "license": MITECO_LICENSE}

LAW_CUT = 23     # Ley 7/2021, art. 3.1.a: al menos un 23 % menos que en 1990 en 2030
PNIEC_CUT = 32   # PNIEC 2023-2030 (Real Decreto 986/2024): un 32 % menos que en 1990


def _src(dataset: str, base: dict) -> dict:
    return {**base, "dataset": dataset, "url": f"https://ec.europa.eu/eurostat/databrowser/view/{dataset}/default/table"}


def _en(code: str) -> str:
    """Nombre inglés de una comunidad con artículo cuando lo lleva (the Canary Islands)."""
    name = geo.ccaa_name(code, "en")
    return f"the {name}" if code in ("04", "05", "10", "16") else name


def _th(n: float, lang: str) -> str:
    """Entero con separador de miles: 1.426 en español, 1,426 en inglés."""
    return f"{round(n):,}".replace(",", "." if lang == "es" else ",")


# ---------- Emisiones (Eurostat) ----------

# Grandes sectores a partir de las categorías del inventario (CRF). Lo que no entra en ninguno (emisiones fugitivas,
# disolventes, otros) se calcula como diferencia con el total sin LULUCF.
SECTORS = {
    "energia": (("CRF1A1",), bi("Centrales y refinerías", "Power and refineries")),
    "industria": (("CRF1A2", "CRF2"), bi("Industria", "Industry")),
    "transporte": (("CRF1A3",), bi("Transporte", "Transport")),
    "edificios": (("CRF1A4A", "CRF1A4B"), bi("Edificios", "Buildings")),
    "agricultura": (("CRF3", "CRF1A4C"), bi("Agricultura", "Agriculture")),
    "residuos": (("CRF5",), bi("Residuos", "Waste")),
}
TOTAL = "TOTX4_MEMO"   # total sin LULUCF ni partidas pro memoria (aviación y navegación internacionales)


def _ghg() -> dict:
    codes = [c for cs, _ in SECTORS.values() for c in cs]
    raw = sources.eurostat("env_air_gge", unit="THS_T", airpol="GHG", src_crf=[TOTAL, *codes])
    return {(r["geo"], r["src_crf"], int(r["time"])): r["value"] for r in raw}


def _sector(v: dict, g: str, s: str, y: int) -> float:
    return sum(v.get((g, c, y), 0) for c in SECTORS[s][0])


def europa_habitante():
    v = _ghg()
    pop = {(r["geo"], int(r["time"])): r["value"] for r in sources.eurostat("demo_gind", indic_de="AVG")}
    year = max(y for (g, c, y) in v if g == "ES" and c == TOTAL)
    eu2 = [c[0] for c in geo.COUNTRIES.values() if c[0] and c[3]]
    rows = []
    for g in [*eu2, "EU27_2020"]:
        if (g, TOTAL, year) in v and (g, year) in pop:
            rows.append({"geo": geo.from_eurostat(g), "time": str(year), "value": round(1000 * v[(g, TOTAL, year)] / pop[(g, year)], 1)})
    assert len(rows) == 28, len(rows)
    val = {r["geo"]: r["value"] for r in rows}
    countries = sorted((c for c in val if c != "EU27"), key=lambda c: val[c])
    pos = countries.index("ESP") + 1   # 1 = el que menos emite
    lower = [c for c in countries if val[c] < val["ESP"]]
    es, eu = val["ESP"], val["EU27"]
    big = {c: val[c] for c in ("DEU", "FRA", "ITA", "POL")}
    return chart(
        id="cle1-europa-habitante",
        lens="europa", theme="clima",
        title=bi(f"Cada habitante de España emite {dec(es, 'es')} toneladas de gases de efecto invernadero al año, frente a "
                 f"{dec(eu, 'es')} en la UE; solo {len(lower)} países emiten menos",
                 f"Each person in Spain emits {dec(es, 'en')} tonnes of greenhouse gases a year, against {dec(eu, 'en')} in "
                 f"the EU; only {len(lower)} countries emit less"),
        subtitle=bi(f"Emisiones de gases de efecto invernadero por habitante, {year}, en toneladas de CO₂ equivalente",
                    f"Greenhouse gas emissions per inhabitant, {year}, in tonnes of CO₂ equivalent"),
        unit=bi("toneladas por habitante", "tonnes per inhabitant"),
        source={**_src("env_air_gge", EUROSTAT_GHG), "also": [_src("demo_gind", EUROSTAT_POP)]},
        notes={"es": ["Emisiones dentro de cada país según su inventario oficial, sin contar las absorciones de los bosques y "
                      "los suelos (LULUCF) ni la aviación y la navegación internacionales. No incluye las emisiones de lo que "
                      "se importa.",
                      "CO₂ equivalente: el metano, el óxido nitroso y los gases fluorados se suman al CO₂ según su efecto "
                      "sobre el calentamiento a cien años.",
                      "Población media del año."],
               "en": ["Emissions within each country according to its official inventory, excluding removals by forests and "
                      "soils (LULUCF) and international aviation and shipping. Emissions embodied in imports are not included.",
                      "CO₂ equivalent: methane, nitrous oxide and fluorinated gases are added to CO₂ according to their "
                      "warming effect over a hundred years.",
                      "Average population for the year."]},
        rows=rows,
        geos=geo.country_table(val),
        extra={"year": year, "position_from_lowest": pos, "lower": lower, "big": big,
               "max": countries[-1], "min": countries[0]},
    )


def europa_sectores():
    v = _ghg()
    year = max(y for (g, c, y) in v if g == "ES" and c == TOTAL)
    idx, share, contrib = {}, {}, {}
    for g in ("ES", "EU27_2020"):
        t90, tl = v[(g, TOTAL, 1990)], v[(g, TOTAL, year)]
        for s in SECTORS:
            a, b = _sector(v, g, s, 1990), _sector(v, g, s, year)
            idx[(g, s)] = round(100 * b / a, 1)
            share[(g, s)] = round(100 * b / tl, 1)
            contrib[(g, s)] = round(100 * (b - a) / t90, 1)
    rows = [{"geo": s, "time": t, "value": idx[(g, s)]} for s in SECTORS for t, g in (("0-ue", "EU27_2020"), ("1-espana", "ES"))]
    geos = {s: {**lab, "aggregate": True} for s, (_, lab) in SECTORS.items()}
    i = lambda g, s: idx[(g, s)]
    # El titular: la electricidad baja igual que en la UE; el transporte sube mucho más
    assert abs(i("ES", "energia") - i("EU27_2020", "energia")) < 5
    up_es = [s for s in SECTORS if i("ES", s) > 100]
    up_eu = [s for s in SECTORS if i("EU27_2020", s) > 100]
    assert up_eu == ["transporte"], up_eu
    assert up_es == ["transporte", "edificios", "agricultura", "residuos"], up_es
    assert i("ES", "energia") < 50 and i("EU27_2020", "energia") < 50
    tr = lambda g: round(i(g, "transporte") - 100, 1)
    return chart(
        id="cle2-europa-sectores",
        lens="europa", theme="clima",
        title=bi(f"Las centrales eléctricas y las refinerías emiten menos de la mitad que en 1990, en España y en la UE; pero "
                 f"el transporte español emite un {dec(tr('ES'), 'es')} % más, y también suben los edificios, la agricultura y "
                 f"los residuos",
                 f"Power stations and refineries emit less than half as much as in 1990, in Spain and in the EU; but Spanish "
                 f"transport emits {dec(tr('ES'), 'en')}% more, and buildings, agriculture and waste are also up"),
        subtitle=bi(f"Emisiones de gases de efecto invernadero de cada sector en {year}, índice 1990 = 100. Punto hueco: UE; "
                    f"punto lleno: España",
                    f"Greenhouse gas emissions of each sector in {year}, index 1990 = 100. Hollow dot: EU; solid dot: Spain"),
        unit=bi("índice, 1990 = 100", "index, 1990 = 100"),
        source=_src("env_air_gge", EUROSTAT_GHG),
        notes={"es": ["Por debajo de 100, el sector emite menos que en 1990; por encima, más.",
                      "Centrales y refinerías: centrales eléctricas, refinerías y otras instalaciones energéticas. Edificios: "
                      "calefacción, agua caliente y cocina de hogares, comercios y oficinas.",
                      "Industria: combustibles quemados en fábricas y obras y emisiones de los propios procesos (cemento, "
                      "química, metal) y de los gases fluorados. Agricultura: ganado, abonos y combustible de tractores y "
                      "barcos de pesca. No se muestran las emisiones fugitivas de combustibles y otras menores.",
                      "Sin LULUCF ni aviación y navegación internacionales."],
               "en": ["Below 100, the sector emits less than in 1990; above it, more.",
                      "Power and refineries: power stations, refineries and other energy installations. Buildings: heating, hot "
                      "water and cooking in homes, shops and offices.",
                      "Industry: fuel burned in factories and construction and emissions from the processes themselves (cement, "
                      "chemicals, metals) and from fluorinated gases. Agriculture: livestock, fertilisers and fuel for tractors "
                      "and fishing boats. Fugitive emissions from fuels and other minor sources are not shown.",
                      "Excluding LULUCF and international aviation and shipping."]},
        rows=rows,
        geos=geos,
        extra={"dimensions": {"time": {"0-ue": bi("UE", "EU"), "1-espana": bi("España", "Spain")}},
               "year": year, "index": {f"{g}-{s}": x for (g, s), x in idx.items()},
               "share": {f"{g}-{s}": x for (g, s), x in share.items()},
               "contribution_points": {f"{g}-{s}": x for (g, s), x in contrib.items()},
               "total_change": {g: pct(v[(g, TOTAL, 1990)], v[(g, TOTAL, year)]) for g in ("ES", "EU27_2020")},
               "up_es": up_es},
    )


# ---------- España por dentro ----------

def _miteco_ccaa() -> dict:
    """Emisiones por comunidad, año y categoría CRT de 3 caracteres (kt de CO₂ eq.), sin LULUCF (sector 4)."""
    import openpyxl

    from .common import ine_ccaa

    zpath = fetch(MITECO_CCAA_URL, ".zip")
    out = collections.defaultdict(float)
    with zipfile.ZipFile(zpath) as zf:
        names = [n for n in zf.namelist() if n.lower().endswith(".xlsx")]
        assert len(names) == 19, names
        for n in names:
            with zf.open(n) as f:
                wb = openpyxl.load_workbook(f, read_only=True)
                ws = wb[wb.sheetnames[0]]
                it = ws.iter_rows(values_only=True)
                hdr = next(it)
                assert hdr[0] == "ANNO" and hdr[1] == "CCAA" and hdr[3] == "ACTIVIDAD_CRT" and hdr[10] == "EE_CO2_EQ", hdr
                for r in it:
                    val = r[10]
                    if val in (None, "") or str(r[4]) == "4":
                        continue
                    code = ine_ccaa(r[1])
                    assert code, r[1]
                    out[(code, int(r[0]), str(r[3])[:3])] += float(val)
    return out


GROUPS = {"1A1": "energia", "1A2": "industria", "2": "industria", "1A3": "transporte"}   # resto: "otros"


def _group(a: str) -> str:
    return GROUPS.get(a[:3]) or GROUPS.get(a[:1]) or "otros"


def comunidades():
    m = _miteco_ccaa()
    tot, energy, grp = collections.defaultdict(float), collections.defaultdict(float), collections.defaultdict(float)
    for (c, y, a), x in m.items():
        tot[(c, y)] += x
        grp[(c, y, _group(a))] += x
        if a == "1A1":
            energy[(c, y)] += x
    year = max(y for (_, y) in tot)
    codes = sorted({c for (c, _) in tot})
    assert len(codes) == 19
    raw = sources.eurostat("demo_r_d2jan", sex="T", age="TOTAL", geo=list(NUTS2))
    jan = {(NUTS2[r["geo"]], int(r["time"])): r["value"] for r in raw}
    pop = {c: (jan[(c, year)] + jan[(c, year + 1)]) / 2 for c in codes}
    pc = {c: round(1000 * tot[(c, year)] / pop[c], 1) for c in codes}
    es_tot = sum(tot[(c, year)] for c in codes)
    pc["ES"] = round(1000 * es_tot / sum(pop.values()), 1)
    rows = [{"geo": c, "time": str(year), "value": pc[c]} for c in [*codes, "ES"]]
    big = [c for c in codes if c not in ("18", "19")]
    hi = max(big, key=lambda c: pc[c])
    lo = min(big, key=lambda c: pc[c])
    base = 2005
    es_base = sum(tot[(c, base)] for c in codes)
    ch = {c: pct(tot[(c, base)], tot[(c, year)]) for c in codes}
    en_drop = sum(energy[(c, base)] - energy[(c, year)] for c in codes)
    share_drop_energy = round(100 * en_drop / (es_base - es_tot), 1)
    share_em = {c: round(100 * tot[(c, year)] / es_tot, 1) for c in codes}
    share_pop = {c: round(100 * pop[c] / sum(pop.values()), 1) for c in codes}
    raw_ratio = (tot[(hi, year)] / pop[hi]) / (tot[(lo, year)] / pop[lo])
    assert 4.5 <= raw_ratio < 5, raw_ratio   # «casi cinco veces»
    ratio = round(raw_ratio, 2)
    shares = {c: {g: round(100 * grp[(c, year, g)] / tot[(c, year)], 1) for g in ("energia", "industria", "transporte", "otros")}
              for c in codes}
    hi_ind = round(shares[hi]["energia"] + shares[hi]["industria"], 1)
    assert 66.7 < hi_ind < 75, hi_ind   # «más de dos tercios»
    return chart(
        id="cld1-comunidades-habitante",
        lens="dentro", theme="clima",
        title=bi(f"En {geo.ccaa_name(hi, 'es')} se emiten {dec(pc[hi], 'es')} toneladas por habitante, casi cinco veces más que "
                 f"en {geo.ccaa_name(lo, 'es')} ({dec(pc[lo], 'es')}): más de dos tercios de lo que emite {geo.ccaa_name(hi, 'es')} sale "
                 f"de sus centrales eléctricas y su industria",
                 f"In {_en(hi)} {dec(pc[hi], 'en')} tonnes are emitted per inhabitant, almost five times as much as in "
                 f"{_en(lo)} ({dec(pc[lo], 'en')}): more than two thirds of {_en(hi)}'s emissions come from its power stations and "
                 f"its industry"),
        subtitle=bi(f"Emisiones de gases de efecto invernadero producidas en cada comunidad por habitante, {year}, en toneladas "
                    f"de CO₂ equivalente",
                    f"Greenhouse gas emissions produced in each region per inhabitant, {year}, in tonnes of CO₂ equivalent"),
        unit=bi("toneladas por habitante", "tonnes per inhabitant"),
        source={**MITECO_CCAA, "also": [_src("demo_r_d2jan", EUROSTAT_POP)]},
        notes={"es": ["Las emisiones se asignan a la comunidad donde se producen, no a la que consume: la electricidad de una "
                      "central o el acero de una acería cuentan donde están, aunque se usen en otra parte.",
                      "Centrales eléctricas: incluye refinerías y otras instalaciones energéticas. Industria: combustión en fábricas y obras y emisiones de los "
                      "procesos industriales y del uso de gases fluorados.",
                      "Sin LULUCF. Población media del año (media del 1 de enero de ese año y del siguiente).",
                      "Ceuta y Melilla tienen muy poca población; su dato depende de unas pocas instalaciones."],
               "en": ["Emissions are assigned to the region where they are produced, not where the output is consumed: "
                      "electricity from a power station or steel from a steelworks counts where the plant is, even if it is "
                      "used elsewhere.",
                      "Power stations: includes refineries and other energy installations. Industry: combustion in factories and construction and emissions "
                      "from industrial processes and the use of fluorinated gases.",
                      "Excluding LULUCF. Average population for the year (mean of 1 January of that year and the next).",
                      "Ceuta and Melilla have very small populations; their figure depends on a handful of installations."]},
        rows=rows,
        geos=geo.ccaa_table([*codes, "ES"]),
        extra={"year": year, "ratio_hi_lo": ratio, "shares": shares, "hi_power_industry": hi_ind, "hi": hi, "lo": lo,
               "change_since_2005": ch, "spain_change_since_2005": pct(es_base, es_tot),
               "energy_share_of_drop_since_2005": share_drop_energy,
               "energy_kt": {c: [round(energy[(c, base)]), round(energy[(c, year)])] for c in codes},
               "share_emissions": share_em, "share_population": share_pop,
               "spain_total_mt": round(es_tot / 1000, 1)},
    )


DD_FIRST = (1980, 1989)   # primera década de la serie
DD_LAST_SPAN = 10


def calor():
    raw = sources.eurostat("nrg_chddr2_a", geo=["ES", "EU27_2020", *NUTS2])
    v = {(r["geo"], r["indic_nrg"], int(r["time"])): r["value"] for r in raw}
    last = max(y for (g, i, y) in v if g == "ES")
    span = (last - DD_LAST_SPAN + 1, last)

    def avg(g, i, a, b):
        xs = [v[(g, i, y)] for y in range(a, b + 1)]
        return sum(xs) / len(xs)

    t0, t1 = f"{DD_FIRST[0]}-{DD_FIRST[1]}", f"{span[0]}-{span[1]}"
    rows, val = [], {}
    for g in NUTS2:   # incluye "ES" (total)
        code = NUTS2.get(g, "ES")
        a, b = round(avg(g, "CDD", *DD_FIRST)), round(avg(g, "CDD", *span))
        val[code] = (a, b)
        rows += [{"geo": code, "time": f"0-{t0}", "value": a}, {"geo": code, "time": f"1-{t1}", "value": b}]
    regions = [c for c in NUTS2.values() if c != "ES"]
    big = [c for c in regions if c not in ("18", "19")]
    up = [c for c in regions if val[c][1] > val[c][0]]
    assert len(up) == 19
    top = sorted(big, key=lambda c: -(val[c][1] - val[c][0]))[:4]
    hdd = {c: (round(avg(g, "HDD", *DD_FIRST)), round(avg(g, "HDD", *span))) for g, c in [*NUTS2.items(), ("EU27_2020", "EU27")]}
    eu = (round(avg("EU27_2020", "CDD", *DD_FIRST)), round(avg("EU27_2020", "CDD", *span)))
    es = val["ES"]
    series = {y: round(v[("ES", "CDD", y)]) for y in range(DD_FIRST[0], last + 1)}
    top_years = sorted(series, key=lambda y: -series[y])[:5]
    return chart(
        id="cld2-comunidades-calor",
        lens="dentro", theme="clima",
        title=bi(f"Las necesidades de refrigeración han crecido en todas las comunidades: en España, de {es[0]} grados-día al "
                 f"año en los años ochenta a {es[1]} en la última década; donde más, en {geo.ccaa_name(top[0], 'es')}, "
                 f"{geo.ccaa_name(top[1], 'es')} y {geo.ccaa_name(top[2], 'es')}",
                 f"Cooling needs have grown in every region: in Spain, from {es[0]} degree days a year in the 1980s to "
                 f"{es[1]} in the last decade; most in {_en(top[0])}, {_en(top[1])} and {_en(top[2])}"),
        subtitle=bi(f"Grados-día de refrigeración, media anual de {t0} y de {t1}. Punto hueco: {t0}; punto lleno: {t1}",
                    f"Cooling degree days, annual average for {t0} and {t1}. Hollow dot: {t0}; solid dot: {t1}"),
        unit=bi("grados-día al año", "degree days a year"),
        source=_src("nrg_chddr2_a", EUROSTAT_DD),
        notes={"es": ["Grados-día de refrigeración: cada día con una temperatura media de 24 °C o más suma los grados que "
                      "supera los 21 °C. Miden cuánto calor hay que combatir, no cuánta refrigeración se usa.",
                      "Eurostat los calcula con datos meteorológicos del Centro Común de Investigación de la Comisión Europea "
                      "para cada región y los pondera por población, no por superficie.",
                      "Ceuta y Melilla son territorios muy pequeños, con clima marítimo; su serie es menos precisa."],
               "en": ["Cooling degree days: each day with a mean temperature of 24°C or more adds the degrees by which it "
                      "exceeds 21°C. They measure how much heat has to be countered, not how much cooling is used.",
                      "Eurostat calculates them with meteorological data from the European Commission's Joint Research Centre "
                      "for each region and weights them by population, not by area.",
                      "Ceuta and Melilla are very small territories with a maritime climate; their series is less precise."]},
        rows=rows,
        geos=geo.ccaa_table(val),
        extra={"dimensions": {"time": {f"0-{t0}": bi(t0, t0), f"1-{t1}": bi(t1, t1)}},
               "periods": [t0, t1], "cdd": {c: list(x) for c, x in val.items()}, "eu_cdd": list(eu),
               "hdd": {c: list(x) for c, x in hdd.items()}, "top_increase": top,
               "spain_series": {str(y): x for y, x in series.items()}, "spain_top_years": top_years,
               "spain_ratio": round(es[1] / es[0], 2), "eu_ratio": round(eu[1] / eu[0], 2)},
    )


# ---------- España en el tiempo ----------

def tiempo_emisiones():
    v = _ghg()
    year = max(y for (g, c, y) in v if g == "ES" and c == TOTAL)
    rows, idx = [], {}
    for g in ("ES", "EU27_2020"):
        for y in range(1990, year + 1):
            x = round(100 * v[(g, TOTAL, y)] / v[(g, TOTAL, 1990)], 1)
            idx[(g, y)] = x
            rows.append({"geo": geo.from_eurostat(g), "time": str(y), "value": x})
    es = {y: idx[("ES", y)] for y in range(1990, year + 1)}
    peak = max(es, key=es.get)
    eu_peak = max((idx[("EU27_2020", y)], y) for y in range(1990, year + 1))
    target = 100 - LAW_CUT
    # Avance de 2025 (MITECO, Nota de Avance del Inventario de GEI 2025): -4,8 % respecto a 1990
    return chart(
        id="clt1-emisiones-1990",
        lens="tiempo", theme="clima",
        title=bi(f"España emitió en {year} un {dec(100 - es[year], 'es')} % menos que en 1990, tras subir un "
                 f"{dec(es[peak] - 100, 'es')} % hasta {peak}; la UE, un {dec(100 - idx[('EU27_2020', year)], 'es')} % menos",
                 f"Spain emitted {dec(100 - es[year], 'en')}% less in {year} than in 1990, after rising by "
                 f"{dec(es[peak] - 100, 'en')}% up to {peak}; the EU, {dec(100 - idx[('EU27_2020', year)], 'en')}% less"),
        subtitle=bi(f"Emisiones de gases de efecto invernadero, índice 1990 = 100, 1990-{year}",
                    f"Greenhouse gas emissions, index 1990 = 100, 1990-{year}"),
        unit=bi("índice, 1990 = 100", "index, 1990 = 100"),
        source=_src("env_air_gge", EUROSTAT_GHG),
        notes={"es": ["Sin LULUCF ni aviación y navegación internacionales, como en el objetivo de la ley española.",
                      f"La línea horizontal marca el objetivo de la Ley 7/2021 para 2030 en España: al menos un {LAW_CUT} % "
                      f"menos que en 1990. El de la UE es distinto (un 55 % menos de emisiones netas, con LULUCF) y no se "
                      f"dibuja."],
               "en": ["Excluding LULUCF and international aviation and shipping, as in the Spanish law's target.",
                      f"The horizontal line marks Spain's 2030 target under Law 7/2021: at least {LAW_CUT}% below 1990. The "
                      f"EU's target is different (55% lower net emissions, including LULUCF) and is not drawn."]},
        rows=rows,
        geos=geo.country_table(["ESP", "EU27"]),
        extra={"ref_line": {"value": target, "label": bi(f"Objetivo de la ley para 2030: {target}", f"Law's 2030 target: {target}")},
               "short_labels": {"ESP": bi("España", "Spain"), "EU27": bi("UE", "EU")},
               "year": year, "peak": peak, "peak_value": es[peak], "eu_peak": eu_peak,
               "spain_mt": {str(y): round(v[("ES", TOTAL, y)] / 1000, 1) for y in (1990, peak, year)},
               "law_target_mt": round(v[("ES", TOTAL, 1990)] * target / 100 / 1000, 1),
               "pniec_target_mt": round(v[("ES", TOTAL, 1990)] * (100 - PNIEC_CUT) / 100 / 1000, 1),
               "pace_2019_year": round((es[year] - es[2019]) / (year - 2019), 2), "index_2019": es[2019]},
    )


def tiempo_pib():
    """Emisiones y PIB en volumen, índice con base en el máximo de emisiones (relación entre las dos variables)."""
    v = _ghg()
    year = max(y for (g, c, y) in v if g == "ES" and c == TOTAL)
    gdp = {int(r["time"]): r["value"] for r in sources.eurostat("nama_10_gdp", unit="CLV10_MEUR", na_item="B1GQ", geo="ES")}
    pop = {int(r["time"]): r["value"] for r in sources.eurostat("demo_gind", indic_de="AVG", geo="ES")}
    first = min(gdp)
    em = {y: v[("ES", TOTAL, y)] for y in range(first, year + 1)}
    peak = max(em, key=em.get)
    series = {"pib": gdp, "emisiones": em, "intensidad": {y: em[y] / gdp[y] for y in em}}
    rows = [{"time": str(y), "series": k, "value": round(100 * s[y] / s[first], 1)} for k, s in series.items()
            for y in range(first, year + 1)]
    g_ch = pct(gdp[peak], gdp[year])
    e_ch = pct(em[peak], em[year])
    i_ch = pct(series["intensidad"][first], series["intensidad"][year])
    pc_ch = pct(em[peak] / pop[peak], em[year] / pop[year])
    return chart(
        id="clt2-pib-emisiones",
        lens="tiempo", theme="clima",
        title=bi(f"Hasta {peak}, las emisiones crecían con la economía; desde entonces, el PIB ha crecido un {dec(g_ch, 'es')} % "
                 f"y las emisiones han bajado un {dec(-e_ch, 'es')} %",
                 f"Until {peak}, emissions grew with the economy; since then, GDP has grown by {dec(g_ch, 'en')}% and "
                 f"emissions have fallen by {dec(-e_ch, 'en')}%"),
        subtitle=bi(f"PIB en volumen, emisiones de gases de efecto invernadero y emisiones por euro de PIB, índice {first} = 100, "
                    f"{first}-{year}",
                    f"GDP in volume, greenhouse gas emissions and emissions per euro of GDP, index {first} = 100, {first}-{year}"),
        unit=bi(f"índice, {first} = 100", f"index, {first} = 100"),
        source={**_src("env_air_gge", EUROSTAT_GHG), "also": [_src("nama_10_gdp", EUROSTAT_NA)]},
        notes={"es": [f"PIB a precios constantes (volumen encadenado, referencia 2010). La serie de Eurostat empieza en {first}.",
                      "Emisiones por euro de PIB: emisiones divididas por el PIB en volumen. Sin LULUCF ni aviación y navegación "
                      "internacionales."],
               "en": [f"GDP at constant prices (chain-linked volumes, reference year 2010). Eurostat's series starts in {first}.",
                      "Emissions per euro of GDP: emissions divided by GDP in volume. Excluding LULUCF and international aviation "
                      "and shipping."]},
        rows=rows,
        extra={"dimensions": {"series": {"pib": bi("PIB en volumen", "GDP in volume"),
                                         "emisiones": bi("Emisiones", "Emissions"),
                                         "intensidad": bi("Emisiones por euro de PIB", "Emissions per euro of GDP")}},
               "short_labels": {"pib": bi("PIB", "GDP"), "emisiones": bi("Emisiones", "Emissions"),
                                "intensidad": bi("Por euro", "Per euro")},
               "ref_line": {"value": 100, "label": bi(f"Nivel de {first}", f"{first} level")},
               "first": first, "year": year, "peak": peak, "gdp_change_since_peak": g_ch, "emissions_change_since_peak": e_ch,
               "intensity_change_since_first": i_ch, "per_capita_change_since_peak": pc_ch,
               "gdp_change_first_peak": pct(gdp[first], gdp[peak]), "emissions_change_first_peak": pct(em[first], em[peak])},
    )


MONTHS_ES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre",
             "diciembre"]
MONTHS_EN = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
             "December"]
EMB_FIRST = 1988   # el histórico empieza en octubre de 1987 con muy pocos embalses; desde 1988, todos


def _embalses() -> list[tuple[str, str, float, float]]:
    """(fecha, ámbito, capacidad, reserva) de cada embalse y semana, en hm³."""
    from access_parser import AccessParser

    zpath = fetch(EMB_URL, ".zip")
    mdb = RAW_DIR / (zpath.stem + ".mdb")
    if not mdb.exists() or mdb.stat().st_mtime < zpath.stat().st_mtime:
        with zipfile.ZipFile(zpath) as zf:
            name = next(n for n in zf.namelist() if n.lower().endswith(".mdb"))
            mdb.write_bytes(zf.read(name))
    db = AccessParser(str(mdb))
    t = db.parse_table("T_Datos Embalses 1988-2026")
    num = lambda s: float(str(s).replace(".", "").replace(",", ".")) if s not in (None, "") else None
    out = []
    for fe, amb, cap, act in zip(t["FECHA"], t["AMBITO_NOMBRE"], t["AGUA_TOTAL"], t["AGUA_ACTUAL"]):
        c, a = num(cap), num(act)
        if c is None or a is None:
            continue
        out.append((str(fe)[:10], amb, c, a))
    return out


def _mtime(y: int, m: int) -> str:
    return str(round(y + (m - 1) / 12, 3)).removesuffix(".0")


def embalses():
    data = _embalses()
    cap, act, n = collections.defaultdict(float), collections.defaultdict(float), collections.Counter()
    bcap, bact = collections.defaultdict(float), collections.defaultdict(float)
    for d, amb, c, a in data:
        cap[d] += c
        act[d] += a
        n[d] += 1
        bcap[(amb, d)] += c
        bact[(amb, d)] += a
    days = sorted(d for d in cap if int(d[:4]) >= EMB_FIRST)
    assert min(n[d] for d in days) >= 300, min(n[d] for d in days)
    pctd = {d: 100 * act[d] / cap[d] for d in days}
    mon = collections.defaultdict(list)
    for d in days:
        mon[(int(d[:4]), int(d[5:7]))].append(pctd[d])
    mm = {k: round(sum(x) / len(x), 1) for k, x in mon.items()}
    keys = sorted(mm)
    rows = [{"time": _mtime(y, m), "series": "reserva", "value": mm[(y, m)]} for y, m in keys]
    labels = {_mtime(y, m): bi(f"{MONTHS_ES[m - 1].capitalize()} de {y}", f"{MONTHS_EN[m - 1]} {y}") for y, m in keys}
    last_day = days[-1]
    ly, lm = int(last_day[:4]), int(last_day[5:7])
    # El mes en curso puede estar incompleto: se compara la última semana con la misma semana de cada año
    same_week = {}
    for y in range(EMB_FIRST, ly + 1):
        cand = [d for d in days if d[:4] == str(y) and d[5:7] == last_day[5:7] and abs(int(d[8:]) - int(last_day[8:])) <= 3]
        if cand:
            same_week[y] = round(pctd[cand[0]], 1)
    higher_since = max((y for y in same_week if y < ly and same_week[y] >= same_week[ly]), default=None)
    lows = sorted(mm.items(), key=lambda kv: kv[1])
    low_after_95 = min(((k, x) for k, x in mm.items() if k[0] > 1995), key=lambda kv: kv[1])
    low_95 = min(((k, x) for k, x in mm.items() if k[0] == 1995), key=lambda kv: kv[1])
    # Por ámbito: última semana frente a la media de la misma semana de los diez años anteriores
    basins = sorted({a for a, _ in bcap})
    by_basin = {}
    for b in basins:
        now = 100 * bact[(b, last_day)] / bcap[(b, last_day)]
        prev = []
        for y in range(ly - 10, ly):
            cand = [d for d in days if d[:4] == str(y) and d[5:7] == last_day[5:7] and abs(int(d[8:]) - int(last_day[8:])) <= 3
                    and (b, d) in bcap]
            if cand:
                prev.append(100 * bact[(b, cand[0])] / bcap[(b, cand[0])])
        by_basin[b] = {"now": round(now, 1), "avg10": round(sum(prev) / len(prev), 1), "capacity_hm3": round(bcap[(b, last_day)])}
    hy = {y: mm[(y, 9)] for y in range(EMB_FIRST, ly + 1) if (y, 9) in mm}   # final del año hidrológico (septiembre)
    full = lambda k: (f"{MONTHS_ES[k[1] - 1]} de {k[0]}", f"{MONTHS_EN[k[1] - 1]} {k[0]}")
    return chart(
        id="clt3-embalses",
        lens="tiempo", theme="clima",
        title=bi(f"Los embalses bajaron al {dec(low_after_95[1], 'es')} % en {full(low_after_95[0])[0]}, el mínimo desde la "
                 f"sequía de 1995; a {int(last_day[8:])} de {MONTHS_ES[lm - 1]} de {ly} están al {dec(same_week[ly], 'es')} %, "
                 f"lo más alto en esa semana desde {higher_since}",
                 f"Reservoirs fell to {dec(low_after_95[1], 'en')}% in {full(low_after_95[0])[1]}, the lowest since the 1995 "
                 f"drought; on {int(last_day[8:])} {MONTHS_EN[lm - 1]} {ly} they stood at {dec(same_week[ly], 'en')}%, the "
                 f"highest for that week since {higher_since}"),
        subtitle=bi(f"Agua embalsada en los embalses de la España peninsular, en % de su capacidad, media mensual, "
                    f"enero de {EMB_FIRST}-{MONTHS_ES[lm - 1]} de {ly}. El último dato semanal, del {int(last_day[8:])} de "
                    f"{MONTHS_ES[lm - 1]}, es del {dec(same_week[ly], 'es')} %",
                    f"Water stored in mainland Spain's reservoirs, as % of capacity, monthly average, January {EMB_FIRST}-"
                    f"{MONTHS_EN[lm - 1]} {ly}. The latest weekly figure, for {int(last_day[8:])} {MONTHS_EN[lm - 1]}, is "
                    f"{dec(same_week[ly], 'en')}%"),
        unit=bi("% de la capacidad", "% of capacity"),
        source=MITECO_EMB,
        notes={"es": ["Reserva semanal que publica el Boletín Hidrológico para los embalses de más de 5 hm³, de uso consuntivo "
                      "(abastecimiento y riego) e hidroeléctrico. El número de embalses y la capacidad total han cambiado "
                      "con los años; el porcentaje se calcula sobre la capacidad de los que informan cada semana.",
                      f"El último mes, {MONTHS_ES[lm - 1]} de {ly}, solo tiene datos hasta el {int(last_day[8:])}.",
                      "El nivel de los embalses depende de la lluvia, pero también de cuánta agua se gasta y se desembalsa: no "
                      "es una medida directa de la sequía meteorológica."],
               "en": ["Weekly reserve published by the Hydrological Bulletin for reservoirs over 5 hm³, used for consumption "
                      "(supply and irrigation) and hydropower. The number of reservoirs and total capacity have changed over the "
                      "years; the percentage is calculated on the capacity of those reporting each week.",
                      f"The last month, {MONTHS_EN[lm - 1]} {ly}, only has data up to the {int(last_day[8:])}th.",
                      "Reservoir levels depend on rainfall, but also on how much water is used and released: they are not a "
                      "direct measure of meteorological drought."]},
        rows=rows,
        extra={"dimensions": {"series": {"reserva": bi("Agua embalsada", "Water stored")}},
               "short_labels": {"reserva": bi("Reserva", "Stored")},
               "time_labels": labels,
               "last_day": last_day, "last_week_pct": same_week[ly], "same_week": {str(y): x for y, x in same_week.items()},
               "higher_since": higher_since, "low_after_1995": [f"{low_after_95[0][0]}-{low_after_95[0][1]:02d}", low_after_95[1]],
               "low_1995": [f"{low_95[0][0]}-{low_95[0][1]:02d}", low_95[1]],
               "lowest_months": [[f"{k[0]}-{k[1]:02d}", x] for k, x in lows[:8]],
               "end_hydrological_year": {str(y): x for y, x in hy.items()},
               "capacity_hm3_last": round(cap[last_day]), "stored_hm3_last": round(act[last_day]), "reservoirs_last": n[last_day],
               "basins": by_basin},
    )


BUILDERS = [europa_habitante, europa_sectores, comunidades, calor, tiempo_emisiones, tiempo_pib, embalses]
