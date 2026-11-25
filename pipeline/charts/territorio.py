"""Tema Territorio (código TE): regiones casi vacías y balance demográfico rural frente a Europa, población por provincia y
por tamaño de municipio, y evolución de los municipios más pequeños y de los que ganan población cada año."""

import json

from lib import geo, sources
from lib.http import fetch
from lib.output import BASE_DIR, THEMES, chart

from .common import bi, dec, pct

THEMES["territorio"] = {"code": "TE", "title": "Territorio"}

EUROSTAT = {"name": "Eurostat", "license": "CC BY 4.0"}


def _src(dataset: str) -> dict:
    return {**EUROSTAT, "dataset": dataset, "url": f"https://ec.europa.eu/eurostat/databrowser/view/{dataset}/default/table"}


PADRON_TABLE = 29005   # INE, cifras oficiales de población de los municipios españoles (revisión del padrón)
PADRON_URL = f"https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/{PADRON_TABLE}?tv=18:451&nult=40&tip=AM"
INE_PADRON = {"name": "INE, cifras oficiales de población (revisión del padrón)",
              "dataset": f"Tabla {PADRON_TABLE}", "url": f"https://www.ine.es/jaxiT3/Tabla.htm?t={PADRON_TABLE}",
              "license": "Reutilización libre citando la fuente"}
PADRON_NOTE = {
    "es": "Cifras oficiales del padrón municipal a 1 de enero de cada año (no hay cifras de 1997). Cuenta a los empadronados, "
          "no a quien vive allí solo una parte del año.",
    "en": "Official municipal register (padrón) figures at 1 January each year (there are no figures for 1997). It counts "
          "registered residents, not people who live there for only part of the year.",
}
BASE_YEAR = 2001   # primer censo del siglo; el padrón de ese año coincide con el total oficial


def _th(n: int, lang: str) -> str:
    """Entero con separador de miles: 1.426 en español, 1,426 en inglés."""
    return f"{n:,}".replace(",", "." if lang == "es" else ",")


def _padron() -> dict[str, dict[int, float]]:
    """Población de cada municipio (código INE de 5 cifras) por año."""
    series = json.loads(fetch(PADRON_URL, ".json").read_text())
    out = {}
    for s in series:
        meta = {m["T3_Variable"]: m for m in s["MetaData"]}
        assert meta["Sexo"]["Nombre"] == "Total", s["Nombre"]
        code = meta["Municipios"]["Codigo"]
        assert len(code) == 5, code
        out[code] = {d["Anyo"]: d["Valor"] for d in s["Data"] if d.get("Valor") is not None}
    assert len(out) > 8100, len(out)
    return out


# ---------- España frente a Europa ----------

# Nombres más cortos o con forma española (el resto, como los da Eurostat, sin «län» ni «županija»)
NUTS3_NAMES = {"FRY30": bi("Guayana Francesa", "French Guiana"), "HR032": bi("Lika-Senj", "Lika-Senj")}
SPARSE = 12.5   # habitantes por km²: umbral de «zona escasamente poblada» de las normas de ayudas regionales de la UE


def europa_densidad():
    raw = sources.eurostat("demo_r_d3dens")
    d = json.loads(fetch(f"{sources.EUROSTAT_API}/demo_r_d3dens?lang=en", ".json").read_text())
    labels = d["dimension"]["geo"]["category"]["label"]
    eu2 = {c[0] for c in geo.COUNTRIES.values() if c[0] and c[3]}
    nuts3 = [r for r in raw if len(r["geo"]) == 5 and r["geo"][:2] in eu2]
    year = max(r["time"] for r in nuts3 if r["geo"] == "ES417")
    cur = [r for r in nuts3 if r["time"] == year]
    sparse = sorted((r for r in cur if r["value"] < SPARSE), key=lambda r: r["value"])
    country = {c[0]: iso3 for iso3, c in geo.COUNTRIES.items() if c[0]}
    es = [r for r in sparse if r["geo"].startswith("ES")]
    nordic = [r for r in sparse if r["geo"][:2] in ("SE", "FI")]
    rest = [r for r in sparse if r["geo"][:2] not in ("SE", "FI")]
    assert len(es) == 3, es
    es_all = sorted((r for r in cur if r["geo"].startswith("ES") and r["geo"][:4] not in ("ES53", "ES70", "ES63", "ES64")),
                    key=lambda r: r["value"])
    rows = [{"geo": r["geo"], "time": year, "value": round(r["value"], 1)} for r in sparse]
    names = {}
    for r in sparse:
        iso = country[r["geo"][:2]]
        lab = labels[r["geo"]].split("/")[0].replace(" län", "").strip()
        lab = NUTS3_NAMES.get(r["geo"], {"es": lab, "en": lab})
        names[r["geo"]] = {"es": f"{lab['es']} ({geo.country_name(iso, 'es')})", "en": f"{lab['en']} ({geo.country_name(iso, 'en')})",
                           "rank": True}
    n_es = len(es)
    return chart(
        id="tee1-europa-densidad",
        lens="europa", theme="territorio",
        title=bi(f"Solo {len(sparse)} regiones de la UE tienen menos de 12,5 habitantes por km²; fuera de Suecia y Finlandia "
                 f"son {len(rest)}, y {n_es} de ellas son Soria, Teruel y Cuenca",
                 f"Only {len(sparse)} EU regions have fewer than 12.5 inhabitants per km²; outside Sweden and Finland there are "
                 f"{len(rest)}, and {n_es} of them are Soria, Teruel and Cuenca"),
        subtitle=bi(f"Regiones de nivel provincial (NUTS 3) de la UE con menos de 12,5 habitantes por km², {year}, en "
                    f"habitantes por km²",
                    f"EU regions at provincial level (NUTS 3) with fewer than 12.5 inhabitants per km², {year}, in inhabitants "
                    f"per km²"),
        unit=bi("habitantes por km²", "inhabitants per km²"),
        source=_src("demo_r_d3dens"),
        notes={"es": ["12,5 habitantes por km² es el umbral con el que las normas de ayudas regionales de la UE definen las "
                      "zonas escasamente pobladas.",
                      "Las regiones NUTS 3 tienen tamaños muy distintos según el país: en España son las provincias; en Alemania, "
                      "comarcas mucho más pequeñas. Una región grande puede esconder zonas casi vacías y una pequeña, no.",
                      "Guayana Francesa es una región ultraperiférica de Francia, en Sudamérica."],
               "en": ["12.5 inhabitants per km² is the threshold that EU regional aid rules use to define sparsely populated "
                      "areas.",
                      "NUTS 3 regions vary greatly in size from country to country: in Spain they are the provinces; in Germany, "
                      "much smaller districts. A large region can hide almost empty areas and a small one cannot.",
                      "French Guiana is an outermost region of France, in South America."]},
        rows=rows,
        geos=names,
        extra={"year": year, "sparse": [r["geo"] for r in sparse], "nordic": len(nordic), "outside_nordic": [r["geo"] for r in rest],
               "spain_lowest": [{"geo": r["geo"], "name": labels[r["geo"]], "value": round(r["value"], 1)} for r in es_all[:8]],
               "spain_total": round(next(r["value"] for r in raw if r["geo"] == "ES" and r["time"] == year), 1),
               "eu_total": round(next(r["value"] for r in raw if r["geo"] == "EU27_2020" and r["time"] == year), 1)},
    )


BALANCE = {
    "LBIRTH": bi("nacimientos", "births"),
    "DEATH": bi("defunciones", "deaths"),
    "CNMIGRAT": bi("llegadas netas", "net arrivals"),
}
TYPO = {"RUR": bi("Rurales", "Rural"), "URB": bi("Urbanas", "Urban")}
BAL_YEARS = ("2022", "2023", "2024")


def europa_balance():
    """Nacimientos, defunciones y saldo migratorio por cada 1.000 habitantes en las regiones rurales y urbanas, España y UE."""
    raw = sources.eurostat("urt_gind3", geo=["ES", "EU27_2020"], terrtypo=[*TYPO, "INT"], indic_de=[*BALANCE, "JAN"])
    v = {(geo.from_eurostat(r["geo"]), r["terrtypo"], r["indic_de"], r["time"]): r["value"] for r in raw}
    rate = {}
    for g in ("ESP", "EU27"):
        for t in TYPO:
            for i in BALANCE:
                vals = [1000 * v[(g, t, i, y)] / ((v[(g, t, "JAN", y)] + v[(g, t, "JAN", str(int(y) + 1))]) / 2)
                        for y in BAL_YEARS]
                rate[(g, t, i)] = round(sum(vals) / len(vals), 1)
    share = {g: {t: round(100 * v[(g, t, "JAN", "2025")] / sum(v[(g, x, "JAN", "2025")] for x in ("URB", "INT", "RUR")), 1)
                 for t in TYPO} for g in ("ESP", "EU27")}
    pop_rur = int(v[("ESP", "RUR", "JAN", "2025")])
    rows = [{"geo": f"{t}-{i}", "time": tt, "value": rate[(g, t, i)]}
            for t in TYPO for i in BALANCE for tt, g in (("0-ue", "EU27"), ("1-espana", "ESP"))]
    geos = {f"{t}-{i}": {"es": f"{TYPO[t]['es']}: {BALANCE[i]['es']}", "en": f"{TYPO[t]['en']}: {BALANCE[i]['en']}",
                         "aggregate": True} for t in TYPO for i in BALANCE}
    r = lambda g, i, t="RUR": rate[(g, t, i)]
    assert 2.5 <= r("ESP", "DEATH") / r("ESP", "LBIRTH") < 3, "el titular dice «casi tres»"
    eu_ratio = round(r("EU27", "DEATH") / r("EU27", "LBIRTH"), 1)
    natural = {g: round(r(g, "LBIRTH") - r(g, "DEATH"), 1) for g in ("ESP", "EU27")}
    period = f"{BAL_YEARS[0]}-{BAL_YEARS[-1]}"
    return chart(
        id="tee2-europa-balance",
        lens="europa", theme="territorio",
        title=bi(f"En las provincias rurales de España mueren casi tres personas por cada una que nace: "
                 f"{dec(r('ESP', 'DEATH'), 'es')} defunciones y {dec(r('ESP', 'LBIRTH'), 'es')} nacimientos al año por cada "
                 f"1.000 habitantes; en las regiones rurales de la UE, {dec(eu_ratio, 'es')} defunciones por cada nacimiento",
                 f"In Spain's rural provinces almost three people die for every one born: {dec(r('ESP', 'DEATH'), 'en')} deaths "
                 f"and {dec(r('ESP', 'LBIRTH'), 'en')} births a year per 1,000 inhabitants; in the EU's rural regions, "
                 f"{dec(eu_ratio, 'en')} deaths for every birth"),
        subtitle=bi(f"Nacimientos, defunciones y saldo migratorio en las regiones predominantemente rurales y urbanas, media "
                    f"{period}, por cada 1.000 habitantes. Punto hueco: UE; punto lleno: España",
                    f"Births, deaths and net migration in predominantly rural and urban regions, {period} average, per 1,000 "
                    f"inhabitants. Hollow dot: EU; solid dot: Spain"),
        unit=bi("por cada 1.000 habitantes", "per 1,000 inhabitants"),
        source=_src("urt_gind3"),
        notes={"es": ["Tipología urbano-rural de Eurostat: clasifica cada región NUTS 3 (en España, cada provincia) según la parte "
                      "de su población que vive en zonas rurales. Las regiones intermedias no se muestran.",
                      f"Como las provincias españolas son grandes, pocas cuentan como predominantemente rurales: en 2025 vivía en "
                      f"ellas el {dec(share['ESP']['RUR'], 'es')} % de la población, frente al {dec(share['EU27']['RUR'], 'es')} % "
                      f"en la UE.",
                      "Saldo migratorio: llegadas menos salidas, desde otras partes del país y desde el extranjero, más los ajustes "
                      "estadísticos. Tasas calculadas sobre la población media de cada año."],
               "en": ["Eurostat urban-rural typology: it classifies each NUTS 3 region (in Spain, each province) by the share of "
                      "its population living in rural areas. Intermediate regions are not shown.",
                      f"Because Spanish provinces are large, few count as predominantly rural: in 2025 they were home to "
                      f"{dec(share['ESP']['RUR'], 'en')}% of the population, against {dec(share['EU27']['RUR'], 'en')}% in the EU.",
                      "Net migration: arrivals minus departures, from elsewhere in the country and from abroad, plus statistical "
                      "adjustments. Rates calculated on each year's average population."]},
        rows=rows,
        geos=geos,
        extra={"dimensions": {"time": {"0-ue": bi("UE", "EU"), "1-espana": bi("España", "Spain")}},
               "period": period, "rates": {f"{g}-{t}-{i}": x for (g, t, i), x in rate.items()},
               "natural_rural": natural, "eu_deaths_per_birth": eu_ratio,
               "es_deaths_per_birth": round(r("ESP", "DEATH") / r("ESP", "LBIRTH"), 2), "share_2025": share, "rural_population_2025": pop_rur},
    )


# ---------- España por dentro ----------

def provincias():
    m = _padron()
    last = max(y for v in m.values() for y in v)
    prov = {}
    for code, v in m.items():
        p = prov.setdefault(code[:2], {})
        for y, x in v.items():
            p[y] = p.get(y, 0) + x
    total = {y: sum(p.get(y, 0) for p in prov.values()) for y in (BASE_YEAR, 2011, last)}
    es = pct(total[BASE_YEAR], total[last])
    ch = {p: pct(v[BASE_YEAR], v[last]) for p, v in prov.items()}
    ch11 = {p: pct(v[2011], v[last]) for p, v in prov.items()}
    lost = sorted((p for p, v in prov.items() if v[last] < v[BASE_YEAR]), key=lambda p: ch[p])
    lost11 = sorted(p for p, v in prov.items() if v[last] < v[2011])
    top = sorted(ch, key=lambda p: -ch[p])[:5]
    rows = [{"geo": p, "time": f"{BASE_YEAR}-{last}", "value": ch[p], "pop": int(prov[p][last])} for p in sorted(prov)]
    rows.append({"geo": "ES", "time": f"{BASE_YEAR}-{last}", "value": es, "pop": int(total[last])})
    geos = {p: {"es": geo.PROVINCIAS[p][0], "en": geo.PROVINCIAS[p][0], "rank": True} for p in prov}
    geos["ES"] = {"es": "España", "en": "Spain", "aggregate": True}
    # Diputados que eligen en 2026 las provincias que han perdido población
    seats = {r["geo"]: r["seats"] for r in json.loads((BASE_DIR / "escanos-2026.json").read_text())["rows"]}
    worst = lost[0]
    return chart(
        id="ted1-provincias",
        lens="dentro", theme="territorio",
        title=bi(f"{len(lost)} de las 52 provincias tienen hoy menos habitantes que en {BASE_YEAR}, mientras España ha ganado un "
                 f"{dec(es, 'es')} %; {geo.PROVINCIAS[worst][0]} ha perdido el {dec(-ch[worst], 'es')} %",
                 f"{len(lost)} of the 52 provinces have fewer inhabitants today than in {BASE_YEAR}, while Spain has grown by "
                 f"{dec(es, 'en')}%; {geo.PROVINCIAS[worst][0]} has lost {dec(-ch[worst], 'en')}%"),
        subtitle=bi(f"Variación de la población de cada provincia entre el 1 de enero de {BASE_YEAR} y el de {last}, en %",
                    f"Change in each province's population between 1 January {BASE_YEAR} and 1 January {last}, in %"),
        unit=bi("% de variación", "% change"),
        source=INE_PADRON,
        notes={"es": [PADRON_NOTE["es"],
                      f"Desde 2011, el último máximo de población antes de la crisis, han perdido habitantes {len(lost11)} "
                      f"provincias."],
               "en": [PADRON_NOTE["en"],
                      f"Since 2011, the last population peak before the crisis, {len(lost11)} provinces have lost inhabitants."]},
        rows=rows,
        geos=geos,
        extra={"last": last, "spain": es, "lost": lost, "lost_since_2011": lost11, "top": [(p, ch[p]) for p in top],
               "seats_lost_provinces": sum(seats[p] for p in lost), "pop_lost_provinces": int(sum(prov[p][last] for p in lost)),
               "abs": {p: [int(prov[p][BASE_YEAR]), int(prov[p][last])] for p in lost}, "total": {str(k): int(x) for k, x in total.items()}},
    )


SIZES = [(0, 100), (101, 500), (501, 1000), (1001, 2000), (2001, 5000), (5001, 10000), (10001, 20000), (20001, 50000),
         (50001, 100000), (100001, None)]


def _size_label(lo, hi, lang):
    th = "." if lang == "es" else ","
    f = lambda n: f"{n:,}".replace(",", th)
    if lo == 0:
        return f"Hasta {hi}" if lang == "es" else f"Up to {hi}"
    if hi is None:
        return f"Más de {f(lo - 1)}" if lang == "es" else f"Over {f(lo - 1)}"
    return f"{f(lo)} a {f(hi)}" if lang == "es" else f"{f(lo)} to {f(hi)}"


def tamano():
    """Crecimiento de la población por tamaño del municipio en el año base (municipios con dato en los dos años)."""
    m = _padron()
    last = max(y for v in m.values() for y in v)
    rows, info = [], {}
    for lo, hi in SIZES:
        g = [v for v in m.values() if BASE_YEAR in v and last in v and lo <= v[BASE_YEAR] <= (hi or 10 ** 9)]
        a, b = sum(v[BASE_YEAR] for v in g), sum(v[last] for v in g)
        key = f"s{lo}"
        rows.append({"geo": key, "time": f"{BASE_YEAR}-{last}", "value": pct(a, b), "municipios": len(g),
                     "lost": sum(1 for v in g if v[last] < v[BASE_YEAR]), "pop_base": int(a), "pop_last": int(b)})
        info[key] = {"es": _size_label(lo, hi, "es"), "en": _size_label(lo, hi, "en"), "rank": True}
    both = [v for v in m.values() if BASE_YEAR in v and last in v]
    lost = [v for v in both if v[last] < v[BASE_YEAR]]
    tot = pct(sum(v[BASE_YEAR] for v in both), sum(v[last] for v in both))
    by = {r["geo"]: r for r in rows}
    best = max(rows, key=lambda r: r["value"])
    return chart(
        id="ted2-tamano-municipio",
        lens="dentro", theme="territorio",
        title=bi(f"Desde {BASE_YEAR}, los municipios de {info[best['geo']]['es'].lower()} habitantes han crecido un "
                 f"{dec(best['value'], 'es')} %; los de 101 a 500 han perdido el {dec(-by['s101']['value'], 'es')} % y las "
                 f"ciudades de más de 100.000 solo han ganado un {dec(by['s100001']['value'], 'es')} %",
                 f"Since {BASE_YEAR}, municipalities of {info[best['geo']]['en'].lower()} inhabitants have grown by "
                 f"{dec(best['value'], 'en')}%; those of 101 to 500 have lost {dec(-by['s101']['value'], 'en')}% and cities of "
                 f"over 100,000 have grown by only {dec(by['s100001']['value'], 'en')}%"),
        subtitle=bi(f"Variación de la población entre {BASE_YEAR} y {last} según el tamaño del municipio en {BASE_YEAR}, en %",
                    f"Population change between {BASE_YEAR} and {last} by size of municipality in {BASE_YEAR}, in %"),
        unit=bi("% de variación", "% change"),
        source=INE_PADRON,
        notes={"es": [PADRON_NOTE["es"],
                      f"Cada municipio se clasifica por su población en {BASE_YEAR} y se sigue hasta {last}, aunque haya cambiado "
                      f"de tamaño. Se excluyen los pocos municipios creados o fusionados en el periodo.",
                      "Los tramos agrupan municipios por su tamaño, no por su situación: no distinguen si están cerca de una "
                      "ciudad, en la costa o en el interior."],
               "en": [PADRON_NOTE["en"],
                      f"Each municipality is classified by its population in {BASE_YEAR} and followed to {last}, even if its "
                      f"size has changed. The few municipalities created or merged during the period are excluded.",
                      "The bands group municipalities by size, not by location: they do not distinguish whether they are near a "
                      "city, on the coast or inland."]},
        rows=rows,
        geos=info,
        extra={"last": last, "municipios": len(both), "lost": len(lost), "lost_pct": round(100 * len(lost) / len(both), 1),
               "pop_in_lost": int(sum(v[last] for v in lost)),
               "pop_in_lost_pct": round(100 * sum(v[last] for v in lost) / sum(v[last] for v in both), 1),
               "total_change": tot},
    )


# ---------- España en el tiempo ----------

def micro():
    m = _padron()
    years = sorted({y for v in m.values() for y in v})
    count = {y: sum(1 for v in m.values() if y in v and v[y] <= 100) for y in years}
    total = {y: sum(1 for v in m.values() if y in v) for y in years}
    upto1000 = {y: sum(1 for v in m.values() if y in v and v[y] <= 1000) for y in years}
    rows = [{"time": str(y), "series": "micro", "value": count[y]} for y in years]
    first, last = years[0], years[-1]
    by_prov = {}
    for code, v in m.items():
        if v.get(last, 10 ** 9) <= 100:
            by_prov[code[:2]] = by_prov.get(code[:2], 0) + 1
    top_prov = sorted(by_prov.items(), key=lambda kv: -kv[1])[:6]
    peak = max(years, key=lambda y: count[y])
    return chart(
        id="tet1-micromunicipios",
        lens="tiempo", theme="territorio",
        title=bi(f"Hay {_th(count[last], 'es')} municipios con 100 habitantes o menos, frente a {count[first]} en {first}",
                 f"There are {_th(count[last], 'en')} municipalities with 100 inhabitants or fewer, against {count[first]} in {first}"),
        subtitle=bi(f"Municipios con 100 habitantes o menos, {first}-{last}",
                    f"Municipalities with 100 inhabitants or fewer, {first}-{last}"),
        unit=bi("municipios", "municipalities"),
        source=INE_PADRON,
        notes={"es": [PADRON_NOTE["es"],
                      f"En {last} hay {_th(total[last], 'es')} municipios; {_th(upto1000[last], 'es')} tienen 1.000 habitantes "
                      f"o menos."],
               "en": [PADRON_NOTE["en"],
                      f"In {last} there are {_th(total[last], 'en')} municipalities; {_th(upto1000[last], 'en')} have 1,000 inhabitants or fewer."]},
        rows=rows,
        extra={"dimensions": {"series": {"micro": bi("Municipios de 100 habitantes o menos", "Municipalities of 100 inhabitants or fewer")}},
               "short_labels": {"micro": bi("Hasta 100 hab.", "Up to 100")},
               "count": {str(y): count[y] for y in years}, "upto1000": {str(y): upto1000[y] for y in years},
               "total": {str(y): total[y] for y in years}, "peak": peak,
               "top_provinces": [{"geo": p, "name": geo.PROVINCIAS[p][0], "n": n} for p, n in top_prov]},
    )


def crecen():
    """Porcentaje de municipios que ganan población cada año (de un 1 de enero al siguiente)."""
    m = _padron()
    years = sorted({y for v in m.values() for y in v})
    rows, info = [], {}
    for y in years:
        if y - 1 not in years:
            continue
        both = [(v[y - 1], v[y]) for v in m.values() if y - 1 in v and y in v]
        up = round(100 * sum(1 for a, b in both if b > a) / len(both), 1)
        down = round(100 * sum(1 for a, b in both if b < a) / len(both), 1)
        # El cambio entre el 1 de enero de y-1 y el de y ocurre durante el año y-1
        rows.append({"time": str(y - 1), "series": "crecen", "value": up})
        info[str(y - 1)] = {"up": up, "down": down, "n": len(both)}
    vals = {r["time"]: r["value"] for r in rows}
    low = min(vals, key=vals.get)
    high = max(vals, key=vals.get)
    last = max(vals)
    crisis = [t for t in vals if 2012 <= int(t) <= 2016]
    crisis_max = max(vals[t] for t in crisis)
    recent = [t for t in vals if int(t) >= 2020]
    recent_min = min(vals[t] for t in recent)
    return chart(
        id="tet2-municipios-crecen",
        lens="tiempo", theme="territorio",
        title=bi(f"Desde 2020, cerca de la mitad de los municipios gana población cada año (el {dec(vals[last], 'es')} % en "
                 f"{last}); entre 2012 y 2016, como mucho el {dec(crisis_max, 'es')} %",
                 f"Since 2020, around half of municipalities have gained population each year ({dec(vals[last], 'en')}% in "
                 f"{last}); between 2012 and 2016, at most {dec(crisis_max, 'en')}%"),
        subtitle=bi(f"Municipios cuya población aumenta durante el año, {min(vals)}-{last}, en % del total",
                    f"Municipalities whose population increases during the year, {min(vals)}-{last}, as % of the total"),
        unit=bi("% de los municipios", "% of municipalities"),
        source=INE_PADRON,
        notes={"es": [PADRON_NOTE["es"],
                      "Cada año compara el padrón del 1 de enero con el del 1 de enero siguiente: «2024» es el cambio entre "
                      "enero de 2024 y enero de 2025. En los municipios muy pequeños, unas pocas altas o bajas bastan para "
                      "pasar de ganar a perder."],
               "en": [PADRON_NOTE["en"],
                      "Each year compares the register at 1 January with that at the following 1 January: «2024» is the change "
                      "between January 2024 and January 2025. In very small municipalities, a handful of registrations or "
                      "departures is enough to switch from gaining to losing."]},
        rows=rows,
        extra={"dimensions": {"series": {"crecen": bi("Municipios que ganan población", "Municipalities gaining population")}},
               "short_labels": {"crecen": bi("Ganan", "Gaining")},
               "years": info, "low": low, "high": high, "crisis_max": crisis_max, "recent_min": recent_min},
    )


BUILDERS = [europa_densidad, europa_balance, provincias, tamano, micro, crecen]
