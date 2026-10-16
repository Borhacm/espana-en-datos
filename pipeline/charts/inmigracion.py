"""Tema Inmigración (código IN): población nacida en el extranjero y de nacionalidad extranjera, empleo y paro por
nacionalidad, España frente a la UE. Solo fuentes oficiales (INE y Eurostat)."""

from collections import defaultdict

from lib import geo, sources
from lib.output import THEMES, chart

from .common import ine_ccaa
from .legislatura import _place, es1

THEMES["inmigracion"] = {"code": "IN", "title": "Inmigración en datos"}

# INE, Estadística Continua de Población (ECP). Las series definitivas llegan al 1 de enero de 2025; desde el 1 de abril
# de 2025, tablas nuevas (provisionales). El INE fecha cada dato el primer día del trimestre: «2026Q1» es el 1 de enero.
BIRTH_HIST = 56937      # población por país de nacimiento, total nacional, 2002-2025
NAT_HIST = 56936        # población por nacionalidad, total nacional, 2002-2025
BIRTH_NEW = 59586       # población por lugar de nacimiento (España/extranjero), total nacional, desde 2025
NAT_NEW = 59585         # población por nacionalidad (española/extranjera), total nacional, desde 2025
BIRTH_CCAA = 59588      # población por lugar de nacimiento (España/extranjero) y comunidad, desde 2025
UNEMP_TABLE = 65336     # INE, EPA: tasas de paro por nacionalidad, sexo y comunidad (trimestral)

INE = {"license": "Reutilización libre citando la fuente"}


def _ine_src(table: int, name: str) -> dict:
    return {"name": name, "dataset": f"Tabla {table}", "url": f"https://www.ine.es/jaxiT3/Tabla.htm?t={table}", **INE}


ECP = "INE, Estadística Continua de Población"
EPA = "INE, Encuesta de Población Activa"


def _ecp(table: int) -> dict[tuple[str, str], dict[str, float]]:
    """(territorio, grupo) -> {periodo: personas}, todas las edades y ambos sexos.
    Grupo: «Total», «España»/«Española» o «Extranjero»/«Extranjera». El orden de las partes cambia según la tabla."""
    out = defaultdict(dict)
    for r in sources.ine_table(table):
        parts = r["series"].split(". ")
        if "Todas las edades" not in parts:
            continue
        rest = [x for x in parts[1:] if x not in ("Todas las edades", "Población", "Número")]
        if len(rest) != 2 or rest[1] != "Total":
            continue
        out[(parts[0], rest[0])][r["period"]] = r["value"]
    return out


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


def _date(period: str) -> str:
    """«2026Q1» -> «1 de enero de 2026» (la ECP fecha cada dato el primer día del trimestre)."""
    y, q = period.split("Q")
    return f"1 de {['enero', 'abril', 'julio', 'octubre'][int(q) - 1]} de {y}"


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
        notes=["Personas residentes nacidas fuera del país, sea cual sea su nacionalidad: incluye a quienes han obtenido la nacionalidad "
               "del país donde viven y a los nacidos en otro país de la UE.",
               "En la UE, los nacidos en otro país de la Unión también cuentan como nacidos en el extranjero.",
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
    out = []
    ranked, missing = _rank(born, last, PREV)
    for r in ranked:
        code = "EU27_2020" if r["geo"] == "EU27" else geo.COUNTRIES[r["geo"]][0]
        nat = native.get((code, last))
        if nat is not None:
            out.append({**r, "native": round(nat, 1)})
    es = next(r for r in out if r["geo"] == "ESP")
    eu = next(r for r in out if r["geo"] == "EU27")
    place = _place(out, "ESP")
    n = len(out) - 1
    unreliable = sorted(geo.COUNTRIES[geo.from_eurostat(r["geo"])][1] for r in born
                        if r["time"] == last and "u" in r["flag"] and geo.from_eurostat(r["geo"]) in {o["geo"] for o in out})
    diff = sorted({geo.COUNTRIES[geo.from_eurostat(r["geo"])][1] for r in raw
                   if r["time"] == last and "d" in r["flag"] and geo.from_eurostat(r["geo"]) in geo.COUNTRIES})
    return chart(
        id="ine2-europa-empleo",
        lens="europa", theme="inmigracion",
        title=f"En España trabaja el {es1(es['value'])} % de los nacidos en el extranjero de 20 a 64 años, "
              f"frente al {es1(es['native'])} % de los nacidos en España",
        subtitle=f"Tasa de empleo de la población nacida en el extranjero de 20 a 64 años, {last}, en %. En la UE: "
                 f"{es1(eu['value'])} % de los nacidos fuera y {es1(eu['native'])} % de los nacidos en el país",
        unit="% de la población de 20 a 64 años",
        source={"name": "Eurostat, Encuesta de Población Activa de la UE", "dataset": "lfsa_ergacob",
                "url": "https://ec.europa.eu/eurostat/databrowser/view/lfsa_ergacob/default/table", "license": "CC BY 4.0"},
        notes=["Personas ocupadas de 20 a 64 años nacidas fuera del país, en % de toda la población nacida fuera de esa edad.",
               "«native» en la descarga: tasa de empleo de los nacidos en el propio país, el mismo año. "
               f"«prev»: tasa de los nacidos en el extranjero en {PREV}.",
               f"España es el {place}.º de {n} países por la tasa de los nacidos fuera."]
              + ([f"Dato poco fiable por tamaño de muestra en {last}: {', '.join(unreliable)}."] if unreliable else [])
              + ([f"Eurostat marca los datos de {last} de {' y '.join(diff)} como «definición distinta» de la armonizada."] if diff else [])
              + _missing_note(missing, last),
        rows=out,
        geos=geo.country_table(r["geo"] for r in out),
    )


# ---------- España por dentro ----------

def comunidades_nacidos_fuera():
    ecp = _ecp(BIRTH_CCAA)
    periods = sorted({p for (g, b), s in ecp.items() if b == "Total" for p in s})
    jan = max(p for p in periods if p.endswith("Q1"))
    out = []
    for (name, b), s in ecp.items():
        if b != "Extranjero":
            continue
        code = ine_ccaa(name)
        if code and jan in s:
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
        title=f"El {es1(es['value'])} % de los residentes en España nació fuera: del {es1(top['value'])} % de {geo.CCAA[top['geo']]} "
              f"al {es1(low['value'])} % de {geo.CCAA[low['geo']]}",
        subtitle=f"Población nacida en el extranjero, {_date(jan)}, en % de la población de cada comunidad",
        unit="% de la población",
        source=_ine_src(BIRTH_CCAA, ECP),
        notes=["Nacidos fuera de España, tengan o no la nacionalidad española. Incluye, por ejemplo, a los hijos de emigrantes "
               "españoles nacidos en otro país.",
               "Dato provisional. «people» en la descarga: número de personas.",
               "Ceuta y Melilla tienen poblaciones pequeñas y no protagonizan el titular."],
        rows=sorted(out, key=lambda r: r["geo"]),
        geos=geo.ccaa_table(r["geo"] for r in out),
    )


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


def _last4(s: dict[str, float]) -> tuple[float, list[str]]:
    qs = sorted(s)[-4:]
    return sum(s[q] for q in qs) / 4, qs


QWORDS = ["primer", "segundo", "tercer", "cuarto"]


def _qlabel(p: str) -> str:
    """«2013Q1» -> «primer trimestre de 2013»."""
    return f"{QWORDS[int(p[-1]) - 1]} trimestre de {p[:4]}"


def _quarters(qs: list[str]) -> str:
    a, b = qs[0], qs[-1]
    return f"del {_qlabel(a)} al {QWORDS[int(b[-1]) - 1]} de {b[:4]}"


FOREIGN, SPANISH = "Extranjera: Total", "Española"


def comunidades_paro():
    by = _paro()
    out, qs = [], None
    for (code, nat), s in by.items():
        if nat != FOREIGN:
            continue
        v, qs_ = _last4(s)
        qs = qs or qs_
        assert qs_ == qs, (code, qs_)
        sp, _ = _last4(by[(code, SPANISH)])
        out.append({"geo": code, "time": qs[-1][:4], "value": round(v, 1), "spanish": round(sp, 1)})
    es = next(r for r in out if r["geo"] == "ES")
    main = [r for r in out if r["geo"] not in ("ES", "18", "19")]
    top = max(main, key=lambda r: r["value"])
    low = min(main, key=lambda r: r["value"])
    higher = sum(1 for r in main if r["value"] > r["spanish"])
    return chart(
        id="ind2-comunidades-paro",
        lens="dentro", theme="inmigracion",
        title=f"El paro de los extranjeros va del {es1(top['value'])} % de {geo.CCAA[top['geo']]} al {es1(low['value'])} % de "
              f"{geo.CCAA[low['geo']]}; en España, {es1(es['value'])} %, frente al {es1(es['spanish'])} % de los españoles",
        subtitle=f"Tasa de paro de la población de nacionalidad extranjera, media {_quarters(qs)}, en %",
        unit="% de la población activa",
        source=_ine_src(UNEMP_TABLE, EPA),
        notes=["Parados en % de los activos (personas que trabajan o buscan empleo) de 16 años o más con nacionalidad extranjera. "
               "Las personas nacidas fuera que tienen la nacionalidad española cuentan como españolas.",
               "Media de los últimos cuatro trimestres publicados. «spanish» en la descarga: la tasa de los españoles en la misma comunidad.",
               f"En {higher} de las 17 comunidades el paro de los extranjeros es más alto que el de los españoles.",
               "La EPA es una encuesta: en las comunidades pequeñas, la muestra de extranjeros es reducida y el dato tiene más error. "
               "Ceuta y Melilla no protagonizan el titular."],
        rows=sorted(out, key=lambda r: r["geo"]),
        geos=geo.ccaa_table(r["geo"] for r in out),
    )


# ---------- España en el tiempo ----------

def poblacion_tiempo():
    born_h, nat_h = _ecp(BIRTH_HIST), _ecp(NAT_HIST)
    born_n, nat_n = _ecp(BIRTH_NEW), _ecp(NAT_NEW)
    N = "Total Nacional"

    def jan(*tables_keys):
        out = {}
        for table, key in tables_keys:
            for p, v in table[(N, key)].items():
                if p.endswith("Q1"):
                    out.setdefault(int(p[:4]), v)
        return out

    total = jan((born_h, "Total"), (born_n, "Total"))
    born = jan((born_h, "Extranjero"), (born_n, "Extranjero"))
    foreign = jan((nat_h, "Extranjera"), (nat_n, "Extranjera"))
    years = sorted(set(total) & set(born) & set(foreign))
    assert years[0] == 2002 and years[-1] >= 2026, years
    first, last = years[0], years[-1]
    sb = {y: 100 * born[y] / total[y] for y in years}
    sf = {y: 100 * foreign[y] / total[y] for y in years}
    rows = ([{"time": str(y), "series": "nacidos", "value": round(sb[y], 1), "people": round(born[y]), "total": round(total[y])}
             for y in years]
            + [{"time": str(y), "series": "extranjeros", "value": round(sf[y], 1), "people": round(foreign[y])} for y in years])
    # Pico de la población extranjera antes de la crisis
    native = {y: total[y] - born[y] for y in years}
    npeak = max(years, key=lambda y: native[y])
    mill = lambda v: es1(v / 1e6)
    peak = max((y for y in years if y <= 2015), key=lambda y: sf[y])
    low = min((y for y in years if y >= peak), key=lambda y: sf[y])
    return chart(
        id="int1-poblacion",
        lens="tiempo", theme="inmigracion",
        title=f"Los nacidos en el extranjero han pasado del {es1(sb[first])} % de la población en {first} al {es1(sb[last])} % en {last}",
        subtitle=f"Población nacida en el extranjero y población de nacionalidad extranjera, 1 de enero de cada año, {first}-{last}, "
                 "en % de la población residente",
        unit="% de la población",
        source={**_ine_src(BIRTH_HIST, ECP),
                "also": [_ine_src(NAT_HIST, ECP), _ine_src(BIRTH_NEW, ECP), _ine_src(NAT_NEW, ECP)]},
        notes=["Nacidos en el extranjero: personas nacidas fuera de España, tengan o no la nacionalidad española. "
               "Extranjeros: personas sin nacionalidad española, hayan nacido donde hayan nacido.",
               "La distancia entre las dos líneas corresponde a las personas nacidas fuera con nacionalidad española, "
               "descontadas las de nacionalidad extranjera nacidas en España.",
               f"La población extranjera tocó techo en {peak} ({es1(sf[peak])} %) y bajó hasta {low} ({es1(sf[low])} %).",
               f"La población nacida en España llegó a su máximo en {npeak} ({mill(native[npeak])} millones) y en {last} era de "
               f"{mill(native[last])} millones. Entre {npeak} y {last}, la nacida fuera pasó de {mill(born[npeak])} a {mill(born[last])} millones.",
               f"Hasta {min(2025, last)}, cifras definitivas de la Estadística Continua de Población; después, provisionales. "
               "«people» en la descarga: número de personas; «total»: población residente."],
        rows=rows,
        extra={"dimensions": {"series": {"nacidos": {"es": "Nacidos en el extranjero"}, "extranjeros": {"es": "Nacionalidad extranjera"}}}},
    )


def paro_tiempo():
    by = _paro()
    rows = []
    for key, series in ((SPANISH, "espanoles"), (FOREIGN, "extranjeros")):
        for p, v in sorted(by[("ES", key)].items()):
            y, q = int(p[:4]), int(p[-1])
            rows.append({"time": round(y + (q - 1) / 4, 2), "series": series, "value": round(v, 1)})
    fs, ss = by[("ES", FOREIGN)], by[("ES", SPANISH)]
    f4, qs = _last4(fs)
    s4, _ = _last4(ss)
    peak = max(fs, key=lambda p: fs[p])
    return chart(
        id="int2-paro",
        lens="tiempo", theme="inmigracion",
        title=f"El paro de los extranjeros es del {es1(f4)} % y el de los españoles, del {es1(s4)} %: "
              f"en {peak[:4]} llegó al {es1(fs[peak])} % y al {es1(ss[peak])} %",
        subtitle=f"Tasa de paro por nacionalidad, trimestral, {min(fs)[:4]}-{qs[-1][:4]}, en %. Titular: media {_quarters(qs)}",
        unit="% de la población activa",
        source=_ine_src(UNEMP_TABLE, EPA),
        notes=["Parados en % de los activos de 16 años o más. Las personas nacidas fuera que tienen la nacionalidad española "
               "cuentan como españolas.",
               f"Máximo de la serie de los extranjeros: {_qlabel(peak)} ({es1(fs[peak])} %; españoles, {es1(ss[peak])} %).",
               "Datos trimestrales sin desestacionalizar: el primer trimestre suele tener más paro."],
        rows=rows,
        extra={"dimensions": {"series": {"espanoles": {"es": "Españoles"}, "extranjeros": {"es": "Extranjeros"}}},
               "quarterly": True},
    )


BUILDERS = [europa_nacidos_fuera, europa_empleo, comunidades_nacidos_fuera, comunidades_paro, poblacion_tiempo, paro_tiempo]
