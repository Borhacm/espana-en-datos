"""Tema Inmigración (código IN): cuántos residentes han nacido fuera y de dónde vienen, edad, empleo, sobrecualificación
y paro, España frente a la UE. Solo fuentes oficiales (INE y Eurostat)."""

from collections import defaultdict
from functools import lru_cache

from lib import geo, sources
from lib.output import THEMES, chart

from .common import ine_ccaa
from .legislatura import _place, es1

THEMES["inmigracion"] = {"code": "IN", "title": "Inmigración en datos"}

# INE, Estadística Continua de Población (ECP). Las series definitivas llegan al 1 de enero de 2025; desde el 1 de abril
# de 2025, tablas nuevas (provisionales). El INE fecha cada dato el primer día del trimestre: «2026Q1» es el 1 de enero.
BIRTH_HIST = 56937      # población por edad y país de nacimiento, total nacional, 2002-2025
NAT_HIST = 56936        # población por edad y nacionalidad, total nacional, 2002-2025
BIRTH_NEW = 59586       # población por edad y lugar de nacimiento (España/extranjero), total nacional, desde 2025
NAT_NEW = 59585         # población por edad y nacionalidad (española/extranjera), total nacional, desde 2025
BIRTH_CCAA = 59588      # población por edad y lugar de nacimiento (España/extranjero) y comunidad, desde 2025
UNEMP_TABLE = 65336     # INE, EPA: tasas de paro por nacionalidad, sexo y comunidad (trimestral)

ALL_AGES = "Todas las edades"
N = "Total Nacional"
INE = {"license": "Reutilización libre citando la fuente"}
ECP = "INE, Estadística Continua de Población"
EPA = "INE, Encuesta de Población Activa"


def _ine_src(tables: list[int], name: str) -> dict:
    ds = ", ".join(str(t) for t in tables)
    return {"name": name, "dataset": f"Tabla{'s' if len(tables) > 1 else ''} {ds}",
            "url": f"https://www.ine.es/jaxiT3/Tabla.htm?t={tables[0]}", **INE}


@lru_cache(maxsize=None)
def _ecp(table: int, age: str = ALL_AGES) -> dict[tuple[str, str], dict[str, float]]:
    """(territorio, grupo) -> {periodo: personas} para un grupo de edad, ambos sexos.
    Grupo: «Total», «España»/«Española», «Extranjero»/«Extranjera» o una región o país de nacimiento.
    El orden de las partes del nombre de la serie cambia según la tabla."""
    out = defaultdict(dict)
    for r in sources.ine_table(table):
        parts = r["series"].split(". ")
        if age not in parts:
            continue
        rest = [x for x in parts[1:] if x not in (age, "Población", "Número")]
        if len(rest) != 2 or rest[1] != "Total":
            continue
        out[(parts[0], rest[0])][r["period"]] = r["value"]
    return out


def _jan(series: dict[str, float]) -> dict[int, float]:
    """Datos del 1 de enero de cada año."""
    return {int(p[:4]): v for p, v in series.items() if p.endswith("Q1")}


def _rank(raw: list[dict], year: str, prev: str) -> tuple[list[dict], list[str]]:
    """Ranking UE: valor del último año y, si existe, del año de referencia. Devuelve también los países de la UE sin dato."""
    by = defaultdict(dict)
    for r in raw:
        c = geo.from_eurostat(r["geo"])
        if c and (c == "EU27" or geo.COUNTRIES.get(c, (0, 0, 0, False))[3]):
            by[c][r["time"]] = r["value"]
    out = [{"geo": c, "time": year, "value": round(v[year], 1), **({"prev": round(v[prev], 1)} if prev in v else {})}
           for c, v in sorted(by.items()) if year in v]
    have = {r["geo"] for r in out}
    missing = sorted(name for c, (_, name, _, eu) in geo.COUNTRIES.items() if eu and c not in have)
    return out, missing


def _missing_note(missing: list[str], year: str) -> list[str]:
    return [f"Sin dato de {year}: {', '.join(missing)}."] if missing else []


def _eurostat_code(iso3: str) -> str:
    return "EU27_2020" if iso3 == "EU27" else geo.COUNTRIES[iso3][0]


def _date(period: str) -> str:
    """«2026Q1» -> «1 de enero de 2026» (la ECP fecha cada dato el primer día del trimestre)."""
    y, q = period.split("Q")
    return f"1 de {['enero', 'abril', 'julio', 'octubre'][int(q) - 1]} de {y}"


def mill(v: float) -> str:
    return es1(v / 1e6)


# ---------- España frente a Europa ----------

def europa_nacidos_fuera():
    raw = sources.eurostat("migr_pop3ctb", age="TOTAL", sex="T", unit="NR", c_birth=["FOR", "TOTAL"])
    vals = defaultdict(dict)
    for r in raw:
        vals[(r["geo"], r["time"])][r["c_birth"]] = r["value"]
    share = [{"geo": g, "time": t, "value": 100 * v["FOR"] / v["TOTAL"]} for (g, t), v in vals.items() if "FOR" in v and "TOTAL" in v]
    last = max(r["time"] for r in share if geo.from_eurostat(r["geo"]) == "EU27")
    PREV = "2015"
    out, missing = _rank(share, last, PREV)
    es = next(r for r in out if r["geo"] == "ESP")
    eu = next(r for r in out if r["geo"] == "EU27")
    place = _place(out, "ESP")
    n = len(out) - 1
    return chart(
        id="ine1-europa-nacidos-fuera",
        lens="europa", theme="inmigracion",
        title=f"El {es1(es['value'])} % de los residentes en España nació en otro país, frente al {es1(eu['value'])} % de la UE: "
              f"el {place}.º porcentaje más alto de {n}",
        subtitle=f"Población nacida en el extranjero, 1 de enero de {last}, en % de la población. "
                 f"En {PREV}, España tenía el {es1(es['prev'])} % y la UE, el {es1(eu['prev'])} %",
        unit="% de la población",
        source={"name": "Eurostat", "dataset": "migr_pop3ctb", "url": "https://ec.europa.eu/eurostat/databrowser/view/migr_pop3ctb/default/table",
                "license": "CC BY 4.0"},
        notes=["Incluye a quienes han obtenido la nacionalidad del país donde viven y a los nacidos en otro país de la UE.",
               f"«prev» en la descarga: dato de {PREV}."] + _missing_note(missing, last),
        rows=out,
        geos=geo.country_table(r["geo"] for r in out),
    )


def europa_empleo():
    raw = sources.eurostat("lfsa_ergacob", age="Y20-64", sex="T", unit="PC", c_birth=["FOR", "NAT"])
    born = [r for r in raw if r["c_birth"] == "FOR"]
    native = {(r["geo"], r["time"]): r["value"] for r in raw if r["c_birth"] == "NAT"}
    last = max(r["time"] for r in born if geo.from_eurostat(r["geo"]) == "EU27")
    PREV = "2015"
    ranked, missing = _rank(born, last, PREV)
    out = [{**r, "native": round(native[(_eurostat_code(r["geo"]), last)], 1)} for r in ranked
           if (_eurostat_code(r["geo"]), last) in native]
    es = next(r for r in out if r["geo"] == "ESP")
    eu = next(r for r in out if r["geo"] == "EU27")
    gap_es, gap_eu = es["native"] - es["value"], eu["native"] - eu["value"]
    diff = sorted({geo.COUNTRIES[geo.from_eurostat(r["geo"])][1] for r in raw
                   if r["time"] == last and "d" in r["flag"] and geo.from_eurostat(r["geo"]) in geo.COUNTRIES})
    return chart(
        id="ine2-europa-empleo",
        lens="europa", theme="inmigracion",
        title=f"La tasa de empleo de los nacidos fuera está {es1(gap_es)} puntos por debajo de la de los nacidos en España; "
              f"en la UE, {es1(gap_eu)} puntos",
        subtitle=f"Tasa de empleo de la población de 20 a 64 años nacida en el extranjero, {last}, en %. "
                 f"España: {es1(es['value'])} % (nacidos en España: {es1(es['native'])} %). UE: {es1(eu['value'])} % ({es1(eu['native'])} %)",
        unit="% de la población de 20 a 64 años",
        source={"name": "Eurostat, Encuesta de Población Activa de la UE", "dataset": "lfsa_ergacob",
                "url": "https://ec.europa.eu/eurostat/databrowser/view/lfsa_ergacob/default/table", "license": "CC BY 4.0"},
        notes=["Personas ocupadas de 20 a 64 años nacidas fuera del país, en % de toda la población nacida fuera de esa edad.",
               f"«native» en la descarga: tasa de los nacidos en el propio país. «prev»: tasa de los nacidos fuera en {PREV}."]
              + ([f"Eurostat marca los datos de {last} de {' y '.join(diff)} como «definición distinta» de la armonizada."] if diff else [])
              + _missing_note(missing, last),
        rows=out,
        geos=geo.country_table(r["geo"] for r in out),
    )


def europa_sobrecualificacion():
    raw = sources.eurostat("lfsa_eoqgan", age="Y20-64", sex="T", unit="PC", citizen=["FOR", "NAT"])
    foreign = [r for r in raw if r["citizen"] == "FOR"]
    nat = {(r["geo"], r["time"]): r["value"] for r in raw if r["citizen"] == "NAT"}
    last = max(r["time"] for r in foreign if geo.from_eurostat(r["geo"]) == "EU27")
    ranked, missing = _rank(foreign, last, "2015")
    out = [{"geo": r["geo"], "time": r["time"], "value": r["value"], "national": round(nat[(_eurostat_code(r["geo"]), last)], 1)}
           for r in ranked if (_eurostat_code(r["geo"]), last) in nat]
    es = next(r for r in out if r["geo"] == "ESP")
    eu = next(r for r in out if r["geo"] == "EU27")
    place = _place(out, "ESP")
    n = len(out) - 1
    place_nat = _place([{"geo": r["geo"], "value": r["national"]} for r in out], "ESP")
    unreliable = sorted(geo.COUNTRIES[geo.from_eurostat(r["geo"])][1] for r in foreign
                        if r["time"] == last and "u" in r["flag"] and geo.from_eurostat(r["geo"]) in {o["geo"] for o in out})
    return chart(
        id="ine3-europa-sobrecualificacion",
        lens="europa", theme="inmigracion",
        title=f"El {es1(es['value'])} % de los extranjeros con estudios superiores que trabajan en España lo hace en un empleo "
              f"que no los requiere: el {place}.º porcentaje más alto de {n}",
        subtitle=f"Tasa de sobrecualificación de los ocupados de 20 a 64 años con nacionalidad extranjera, {last}, en %. "
                 f"Españoles: {es1(es['national'])} %. UE: {es1(eu['value'])} % de los extranjeros y {es1(eu['national'])} % de los nacionales",
        unit="% de los ocupados con estudios superiores",
        source={"name": "Eurostat, Encuesta de Población Activa de la UE", "dataset": "lfsa_eoqgan",
                "url": "https://ec.europa.eu/eurostat/databrowser/view/lfsa_eoqgan/default/table", "license": "CC BY 4.0"},
        notes=["Ocupados con estudios superiores (CINE 5 a 8) que trabajan en ocupaciones que no los requieren (grupos 4 a 9 de la "
               "clasificación internacional de ocupaciones), en % de todos los ocupados con estudios superiores.",
               "Esta tabla de Eurostat clasifica por nacionalidad, no por lugar de nacimiento.",
               f"«national» en la descarga: tasa de los nacionales del país. Por esa tasa, España es el {place_nat}.º de {n}."]
              + ([f"Dato poco fiable por tamaño de muestra en {last}: {', '.join(unreliable)}."] if unreliable else [])
              + _missing_note(missing, last),
        rows=out,
        geos=geo.country_table(r["geo"] for r in out),
    )


# ---------- España por dentro ----------

def comunidades_nacidos_fuera():
    ecp = _ecp(BIRTH_CCAA)
    jan = max(p for (g, b), s in ecp.items() if b == "Total" for p in s if p.endswith("Q1"))
    out = []
    for (name, b), s in ecp.items():
        code = ine_ccaa(name)
        if b == "Extranjero" and code and jan in s:
            out.append({"geo": code, "time": jan[:4], "value": round(100 * s[jan] / ecp[(name, "Total")][jan], 1),
                        "people": round(s[jan])})
    assert len(out) == 20, len(out)
    es = next(r for r in out if r["geo"] == "ES")
    main = [r for r in out if r["geo"] not in ("ES", "18", "19")]
    top = max(main, key=lambda r: r["value"])
    low = min(main, key=lambda r: r["value"])
    return chart(
        id="ind1-comunidades-nacidos-fuera",
        lens="dentro", theme="inmigracion",
        title=f"Del {es1(top['value'])} % de residentes nacidos fuera en {geo.CCAA[top['geo']]} al {es1(low['value'])} % "
              f"en {geo.CCAA[low['geo']]}",
        subtitle=f"Población nacida en el extranjero, {_date(jan)}, en % de la población de cada comunidad. España: {es1(es['value'])} %",
        unit="% de la población",
        source=_ine_src([BIRTH_CCAA], ECP),
        notes=["Dato provisional. «people» en la descarga: número de personas.",
               "Ceuta y Melilla tienen poblaciones pequeñas y no protagonizan el titular."],
        rows=sorted(out, key=lambda r: r["geo"]),
        geos=geo.ccaa_table(r["geo"] for r in out),
    )


FOREIGN, SPANISH = "Extranjera: Total", "Española"


def _paro() -> dict[tuple[str, str], dict[str, float]]:
    """(comunidad, nacionalidad) -> {trimestre: tasa de paro}, ambos sexos."""
    out = defaultdict(dict)
    for r in sources.ine_table(UNEMP_TABLE):
        parts = r["series"].split(". ")
        # «Tasa de paro de la población. Ambos sexos. <comunidad>. <nacionalidad>»
        if len(parts) == 4 and parts[1] == "Ambos sexos":
            code = ine_ccaa(parts[2])
            if code:
                out[(code, parts[3])][r["period"]] = r["value"]
    return out


QWORDS = ["primer", "segundo", "tercer", "cuarto"]


def _quarters(qs: list[str]) -> str:
    a, b = qs[0], qs[-1]
    return f"del {QWORDS[int(a[-1]) - 1]} trimestre de {a[:4]} al {QWORDS[int(b[-1]) - 1]} de {b[:4]}"


def comunidades_paro():
    by = _paro()
    out, qs = [], None
    for (code, nat), s in by.items():
        if nat != FOREIGN:
            continue
        last4 = sorted(s)[-4:]
        qs = qs or last4
        assert last4 == qs, (code, last4)
        sp = by[(code, SPANISH)]
        out.append({"geo": code, "time": qs[-1][:4], "value": round(sum(s[q] for q in qs) / 4, 1),
                    "spanish": round(sum(sp[q] for q in qs) / 4, 1)})
    es = next(r for r in out if r["geo"] == "ES")
    main = [r for r in out if r["geo"] not in ("ES", "18", "19")]
    top = max(main, key=lambda r: r["value"])
    low = min(main, key=lambda r: r["value"])
    assert all(r["value"] > r["spanish"] for r in out), "el texto dice que es más alto en todas las comunidades"
    return chart(
        id="ind2-comunidades-paro",
        lens="dentro", theme="inmigracion",
        title=f"El paro de los extranjeros es más alto que el de los españoles en todas las comunidades: del {es1(top['value'])} % "
              f"de {geo.CCAA[top['geo']]} al {es1(low['value'])} % de {geo.CCAA[low['geo']]}",
        subtitle=f"Tasa de paro de la población de nacionalidad extranjera, media {_quarters(qs)}, en %. "
                 f"España: {es1(es['value'])} % (españoles: {es1(es['spanish'])} %)",
        unit="% de la población activa",
        source=_ine_src([UNEMP_TABLE], EPA),
        notes=["Parados en % de los activos (personas que trabajan o buscan empleo) de 16 años o más.",
               "«spanish» en la descarga: tasa de los españoles en la misma comunidad.",
               "En las comunidades pequeñas la muestra de extranjeros de la EPA es reducida y el dato tiene más error. "
               "Ceuta y Melilla no protagonizan el titular."],
        rows=sorted(out, key=lambda r: r["geo"]),
        geos=geo.ccaa_table(r["geo"] for r in out),
    )


# ---------- España en el tiempo ----------

def poblacion_tiempo():
    born_h, nat_h = _ecp(BIRTH_HIST), _ecp(NAT_HIST)
    born_n, nat_n = _ecp(BIRTH_NEW), _ecp(NAT_NEW)

    def series(*pairs):
        out = {}
        for table, key in pairs:
            for y, v in _jan(table[(N, key)]).items():
                out.setdefault(y, v)
        return out

    total = series((born_h, "Total"), (born_n, "Total"))
    born = series((born_h, "Extranjero"), (born_n, "Extranjero"))
    foreign = series((nat_h, "Extranjera"), (nat_n, "Extranjera"))
    years = sorted(set(total) & set(born) & set(foreign))
    assert years[0] == 2002 and years[-1] >= 2026, years
    first, last = years[0], years[-1]
    sb = {y: 100 * born[y] / total[y] for y in years}
    sf = {y: 100 * foreign[y] / total[y] for y in years}
    native = {y: total[y] - born[y] for y in years}
    npeak = max(years, key=lambda y: native[y])
    assert all(native[y] < native[y - 1] for y in years if y > npeak), "el texto dice que baja todos los años"
    rows = ([{"time": str(y), "series": "nacidos", "value": round(sb[y], 1), "people": round(born[y]), "total": round(total[y])}
             for y in years]
            + [{"time": str(y), "series": "extranjeros", "value": round(sf[y], 1), "people": round(foreign[y])} for y in years])
    return chart(
        id="int1-poblacion",
        lens="tiempo", theme="inmigracion",
        title=f"Los nacidos en el extranjero han pasado del {es1(sb[first])} % de la población en {first} al {es1(sb[last])} % en {last}",
        subtitle=f"Población nacida en el extranjero y población de nacionalidad extranjera, 1 de enero de cada año, {first}-{last}, "
                 "en % de la población residente",
        unit="% de la población",
        source=_ine_src([BIRTH_HIST, NAT_HIST, BIRTH_NEW, NAT_NEW], ECP),
        notes=[f"Población nacida en España: máximo en {npeak} ({mill(native[npeak])} millones); {mill(native[last])} millones en {last}.",
               f"Hasta {min(2025, last)}, cifras definitivas; después, provisionales.",
               "«people» en la descarga: número de personas; «total»: población residente."],
        rows=rows,
        extra={"dimensions": {"series": {"nacidos": {"es": "Nacidos en el extranjero"}, "extranjeros": {"es": "Nacionalidad extranjera"}}}},
    )


# Regiones de nacimiento de la ECP. Europa (sin España) se suma de dos agrupaciones que cambian en 2021 con el Brexit:
# UE28 y resto de Europa hasta 2020; UE27 y resto de Europa desde 2021. La suma es la misma en ambos casos.
REGIONS = {"Sudamérica": "sudamerica", "África": "africa", "Centro América y Caribe": "centroamerica", "Asia": "asia"}
EUROPE = [("UE28 sin España", "Europa menos UE28"), ("UE27_2020 sin España", "Europa menos UE27_2020")]
REGION_NAMES = {"sudamerica": "Sudamérica", "europa": "Resto de Europa", "africa": "África",
                "centroamerica": "Centroamérica y Caribe", "asia": "Asia"}
NOT_COUNTRIES = {"Total", "España", "Extranjero", "Sudamérica", "África", "Asia", "Oceanía", "América del Norte",
                 "Centro América y Caribe", "UE27_2020 sin España", "UE28 sin España", "Europa menos UE27_2020",
                 "Europa menos UE28", "Otro país de la Unión Europea sin España"}


def origen_tiempo():
    ecp = _ecp(BIRTH_HIST)
    regions = {code: _jan(ecp[(N, name)]) for name, code in REGIONS.items()}
    europe = {}
    for a, b in EUROPE:
        sa_, sb_ = _jan(ecp[(N, a)]), _jan(ecp[(N, b)])
        europe.update({y: sa_[y] + sb_[y] for y in sa_ if y in sb_})
    regions["europa"] = europe
    years = sorted(set.intersection(*(set(s) for s in regions.values())))
    first, last = years[0], years[-1]
    born = _jan(ecp[(N, "Extranjero")])
    shown = {y: sum(s[y] for s in regions.values()) for y in years}
    assert all(born[y] - shown[y] < 0.03 * born[y] for y in years), "faltan regiones"
    rows = [{"time": str(y), "series": code, "value": round(s[y] / 1e6, 3), "people": round(s[y])}
            for code, s in regions.items() for y in years]
    assert max(regions, key=lambda c: regions[c][last]) == "sudamerica"
    assert max(regions, key=lambda c: regions[c][last] - regions[c][first]) == "sudamerica"
    # Principales países de nacimiento en el último año
    countries = {name: _jan(s).get(last) for (g, name), s in ecp.items() if g == N and name not in NOT_COUNTRIES}
    best = sorted(((v, k) for k, v in countries.items() if v), reverse=True)[:6]
    sa = regions["sudamerica"]
    return chart(
        id="int2-origen",
        lens="tiempo", theme="inmigracion",
        title=f"Los nacidos en Sudamérica son el grupo más numeroso y el que más ha crecido: de {mill(sa[first])} millones "
              f"en {first} a {mill(sa[last])} en {last}",
        subtitle=f"Población residente nacida fuera de España por región de nacimiento, 1 de enero de cada año, {first}-{last}, "
                 "en millones de personas",
        unit="Millones de personas",
        source=_ine_src([BIRTH_HIST], ECP),
        notes=[f"Principales países de nacimiento el 1 de enero de {last}: "
               + ", ".join(f"{k} ({round(v):,})".replace(",", ".") for v, k in best) + " personas.",
               "No se muestran América del Norte ni Oceanía (menos del 2 % de los nacidos fuera en 2025). «Resto de Europa»: toda Europa salvo España, dentro y fuera de la UE.",
               "La serie por país de nacimiento llega, por ahora, al 1 de enero de 2025. «people» en la descarga: número de personas."],
        rows=rows,
        extra={"dimensions": {"series": {c: {"es": n} for c, n in REGION_NAMES.items()}}},
    )


OLD_AGES = ["De 65 a 69 años", "De 70 a 74 años", "De 75 a 79 años", "De 80 a 84 años", "De 85 a 89 años", "90 y más años"]
WORK_AGES = [f"De {a} a {a + 4} años" for a in range(15, 65, 5)]


def dependencia_tiempo():
    def by_age(hist, new, key):
        out = defaultdict(float)
        for ages, sign in ((WORK_AGES, "w"), (OLD_AGES, "o")):
            for age in ages:
                h, n = _ecp(hist, age), _ecp(new, age)
                merged = {**_jan(n[(N, key)]), **_jan(h[(N, key)])}
                for y, v in merged.items():
                    out[(y, sign)] += v
        return out

    groups = {"total": "Total", "espana": "España", "fuera": "Extranjero"}
    data = {g: by_age(BIRTH_HIST, BIRTH_NEW, key) for g, key in groups.items()}
    years = sorted({y for (y, s) in data["total"]})
    ratio = {g: {y: 100 * d[(y, "o")] / d[(y, "w")] for y in years} for g, d in data.items()}
    first, last = years[0], years[-1]
    share_work = {y: 100 * data["fuera"][(y, "w")] / data["total"][(y, "w")] for y in years}
    rows = [{"time": str(y), "series": g, "value": round(ratio[g][y], 1)} for g in groups for y in years]
    return chart(
        id="int3-dependencia",
        lens="tiempo", theme="inmigracion",
        title=f"Entre los nacidos en España hay {es1(ratio['espana'][last])} mayores de 64 por cada 100 personas de 15 a 64 años; "
              f"entre los nacidos fuera, {es1(ratio['fuera'][last])}",
        subtitle=f"Personas de 65 años o más por cada 100 de 15 a 64 años, según el lugar de nacimiento, 1 de enero de cada año, "
                 f"{first}-{last}",
        unit="Mayores de 64 por cada 100 personas de 15 a 64",
        source=_ine_src([BIRTH_HIST, BIRTH_NEW], ECP),
        notes=["Usa el grupo de 15 a 64 años (los grupos de edad de la tabla son quinquenales), como Eurostat. El artículo de "
               "demografía usa el indicador del INE, de 16 a 64 años, que da un valor algo distinto.",
               f"Los nacidos fuera eran el {es1(share_work[first])} % de la población de 15 a 64 años en {first} y el "
               f"{es1(share_work[last])} % en {last}.",
               "Los hijos de inmigrantes nacidos en España cuentan como nacidos en España."],
        rows=rows,
        extra={"dimensions": {"series": {"total": {"es": "Toda la población"}, "espana": {"es": "Nacidos en España"},
                                         "fuera": {"es": "Nacidos fuera"}}},
               "share_work": {str(y): round(share_work[y], 1) for y in years}},
    )


BUILDERS = [europa_nacidos_fuera, europa_empleo, europa_sobrecualificacion, comunidades_nacidos_fuera, comunidades_paro,
            poblacion_tiempo, origen_tiempo, dependencia_tiempo]
