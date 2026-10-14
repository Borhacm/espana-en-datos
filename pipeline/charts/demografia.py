"""Tema Demografía y pensiones (código DE): fecundidad, esperanza de vida, envejecimiento por comunidades y gasto en pensiones
frente a la UE."""

from collections import defaultdict

from lib import geo, sources
from lib.output import THEMES, chart

from .common import ine_ccaa
from .legislatura import _eu_rank, _place, es1

THEMES["demografia"] = {"code": "DE", "title": "Demografía y pensiones: un país que envejece"}

DEP_TABLE = 1455        # INE, Indicadores Demográficos Básicos: tasa de dependencia de los mayores de 64 por comunidad (anual)
ICF_TABLE = 1441        # INE, IDB: indicador coyuntural de fecundidad por comunidad y nacionalidad de la madre (anual)
LIFE_TABLE = 1414       # INE, IDB: esperanza de vida al nacimiento según sexo (anual)
START = 1975            # primer año de las series del INE

INE = {"license": "Reutilización libre citando la fuente"}
INE_DEP = {"name": "INE, Indicadores Demográficos Básicos", "dataset": f"Tabla {DEP_TABLE}",
           "url": f"https://www.ine.es/jaxiT3/Tabla.htm?t={DEP_TABLE}", **INE}
INE_ICF = {"name": "INE, Indicadores Demográficos Básicos", "dataset": f"Tabla {ICF_TABLE}",
           "url": f"https://www.ine.es/jaxiT3/Tabla.htm?t={ICF_TABLE}", **INE}
INE_LIFE = {"name": "INE, Indicadores Demográficos Básicos", "dataset": f"Tabla {LIFE_TABLE}",
            "url": f"https://www.ine.es/jaxiT3/Tabla.htm?t={LIFE_TABLE}", **INE}


def es2(v: float) -> str:
    """Dos decimales con coma: 1,10."""
    return f"{v:.2f}".replace(".", ",")


def _ordinal(n: int, high: bool = True) -> str:
    word = "más alto" if high else "más bajo"
    return f"el {word}" if n == 1 else f"el {n}.º {word}"


def _dependencia() -> dict[str, dict[int, float]]:
    """Tasa de dependencia de los mayores de 64 por comunidad y año."""
    by = defaultdict(dict)
    for r in sources.ine_table(DEP_TABLE):
        # «Indicadores de crecimiento y estructura de la población. <comunidad>»
        code = ine_ccaa(r["series"].split(". ", 1)[1])
        if code:
            by[code][int(r["period"])] = r["value"]
    assert len(by) == 20, sorted(by)
    return by


def _fecundidad() -> dict[str, dict[int, float]]:
    """Indicador coyuntural de fecundidad (hijos por mujer), madres de todas las nacionalidades, por comunidad y año."""
    by = defaultdict(dict)
    for r in sources.ine_table(ICF_TABLE):
        parts = r["series"].split(". ")
        # «Fecundidad. <comunidad>. Ambas nacionalidades»
        if len(parts) == 3 and parts[0] == "Fecundidad" and parts[2] == "Ambas nacionalidades":
            code = ine_ccaa(parts[1])
            if code:
                by[code][int(r["period"])] = r["value"]
    assert len(by) == 20, sorted(by)
    return by


# ---------- España frente a Europa ----------

def europa_fecundidad():
    raw = sources.eurostat("demo_find", indic_de="TOTFERRT")
    last = max(r["time"] for r in raw if geo.from_eurostat(r["geo"]) == "EU27")
    PREV = "2008"
    # _eu_rank redondea a un decimal: los hijos por mujer se dan con dos
    vals = defaultdict(dict)
    for r in raw:
        c = geo.from_eurostat(r["geo"])
        if c:
            vals[c][r["time"]] = r["value"]
    out = [{**r, "value": round(vals[r["geo"]][last], 2), "prev": round(vals[r["geo"]][PREV], 2)} for r in _eu_rank(raw, last, PREV)]
    es = next(r for r in out if r["geo"] == "ESP")
    eu = next(r for r in out if r["geo"] == "EU27")
    place = _place(out, "ESP", reverse=False)
    n = len(out) - 1
    return chart(
        id="dee1-europa-fecundidad",
        lens="europa", theme="demografia",
        title=f"En España nacen {es2(es['value'])} hijos por mujer, frente a {es2(eu['value'])} en la UE: "
              f"{_ordinal(place, high=False)} de {n} países",
        subtitle=f"Indicador coyuntural de fecundidad, {last}: hijos por mujer si se mantuvieran las tasas de ese año",
        unit="Hijos por mujer",
        source={"name": "Eurostat", "dataset": "demo_find", "url": "https://ec.europa.eu/eurostat/databrowser/view/demo_find/default/table",
                "license": "CC BY 4.0"},
        notes=["Número medio de hijos que tendría una mujer a lo largo de su vida si se mantuvieran las tasas de fecundidad por edad de ese año.",
               "Se considera que hacen falta unos 2,1 hijos por mujer para que una población se mantenga sin migraciones.",
               f"«prev» en la descarga: dato de {PREV}, último año antes de la crisis financiera. "
               f"España tenía entonces {es2(es['prev'])} hijos por mujer y la UE, {es2(eu['prev'])}."],
        rows=out,
        geos=geo.country_table(r["geo"] for r in out),
    )


def europa_pensiones():
    raw = sources.eurostat("spr_exp_pens", spdepb="TOTAL", spdepm="TOTAL", unit="PC_GDP")
    last = max(r["time"] for r in raw if geo.from_eurostat(r["geo"]) == "EU27")
    PREV = "2008"
    out = _eu_rank(raw, last, PREV)
    es = next(r for r in out if r["geo"] == "ESP")
    eu = next(r for r in out if r["geo"] == "EU27")
    place = _place(out, "ESP")
    n = len(out) - 1
    provisional = sorted(geo.COUNTRIES[geo.from_eurostat(r["geo"])][1] if geo.from_eurostat(r["geo"]) != "EU27" else "la UE"
                         for r in raw if r["time"] == last and "p" in r["flag"]
                         and geo.from_eurostat(r["geo"]) in {o["geo"] for o in out})
    return chart(
        id="dee2-europa-pensiones",
        lens="europa", theme="demografia",
        title=f"España dedica a pensiones el {es1(es['value'])} % del PIB, frente al {es1(eu['value'])} % de la UE: "
              f"{_ordinal(place)} de {n} países",
        subtitle=f"Gasto en pensiones, {last}, en % del PIB. En {PREV}, España dedicaba el {es1(es['prev'])} % y la UE, el {es1(eu['prev'])} %",
        unit="% del PIB",
        source={"name": "Eurostat, sistema europeo de estadísticas de protección social (SEEPROS)", "dataset": "spr_exp_pens",
                "url": "https://ec.europa.eu/eurostat/databrowser/view/spr_exp_pens/default/table", "license": "CC BY 4.0"},
        notes=["Pensiones de jubilación, de jubilación anticipada, de viudedad y orfandad, de incapacidad y parciales, públicas y privadas "
               "obligatorias, con y sin cotización previa. Incluye las de clases pasivas de los funcionarios.",
               "No es igual que el gasto del sistema de Seguridad Social que publica el Gobierno: la definición europea es más amplia "
               "y sirve para comparar países.",
               f"«prev» en la descarga: dato de {PREV}."]
              + ([f"Datos provisionales de {last}: {', '.join(provisional)}."] if provisional else []),
        rows=out,
        geos=geo.country_table(r["geo"] for r in out),
    )


# ---------- España por dentro ----------

def dependencia_comunidades():
    by = _dependencia()
    last = max(by["ES"])
    out = [{"geo": c, "time": str(last), "value": round(v[last], 1), "prev": round(v[START], 1)} for c, v in by.items()]
    es = next(r for r in out if r["geo"] == "ES")
    main = [r for r in out if r["geo"] not in ("ES", "18", "19")]
    top = max(main, key=lambda r: r["value"])
    low = min(main, key=lambda r: r["value"])
    return chart(
        id="ded1-dependencia-comunidades",
        lens="dentro", theme="demografia",
        title=f"Por cada 100 personas de 16 a 64 años hay {es1(es['value'])} mayores de 64: "
              f"{es1(top['value'])} en {geo.CCAA[top['geo']]} y {es1(low['value'])} en {geo.CCAA[low['geo']]}",
        subtitle=f"Tasa de dependencia de la población mayor de 64 años, 1 de enero de {last}. En {START}, España tenía {es1(es['prev'])}",
        unit="Mayores de 64 por cada 100 personas de 16 a 64",
        source=INE_DEP,
        notes=["Población de 65 años o más dividida por la población de 16 a 64 años, por 100. Es una medida demográfica: no tiene "
               "en cuenta cuántas personas de 16 a 64 años trabajan ni cuántas de 65 o más siguen trabajando.",
               f"«prev» en la descarga: dato de {START}.",
               "Ceuta y Melilla tienen poblaciones pequeñas y muy jóvenes."],
        rows=sorted(out, key=lambda r: r["geo"]),
        geos=geo.ccaa_table(r["geo"] for r in out),
    )


def fecundidad_comunidades():
    by = _fecundidad()
    last = max(by["ES"])
    out = [{"geo": c, "time": str(last), "value": round(v[last], 2)} for c, v in by.items()]
    es = next(r for r in out if r["geo"] == "ES")
    main = [r for r in out if r["geo"] not in ("ES", "18", "19")]
    top = max(main, key=lambda r: r["value"])
    low = min(main, key=lambda r: r["value"])
    return chart(
        id="ded2-fecundidad-comunidades",
        lens="dentro", theme="demografia",
        title=f"La fecundidad va de {es2(low['value'])} hijos por mujer en {geo.CCAA[low['geo']]} a {es2(top['value'])} "
              f"en {geo.CCAA[top['geo']]}",
        subtitle=f"Indicador coyuntural de fecundidad, {last}, hijos por mujer. España: {es2(es['value'])}",
        unit="Hijos por mujer",
        source=INE_ICF,
        notes=["Número medio de hijos que tendría una mujer a lo largo de su vida si se mantuvieran las tasas de fecundidad por edad de ese año. "
               "Madres de todas las nacionalidades.",
               "Ceuta y Melilla tienen poblaciones pequeñas y no protagonizan el titular."],
        rows=sorted(out, key=lambda r: r["geo"]),
        geos=geo.ccaa_table(r["geo"] for r in out),
    )


# ---------- España en el tiempo ----------

def fecundidad_tiempo():
    es = _fecundidad()["ES"]
    years = sorted(es)
    last = years[-1]
    low_y = min(years, key=lambda y: (es[y], -y))
    return chart(
        id="det1-fecundidad",
        lens="tiempo", theme="demografia",
        title=f"La fecundidad ha pasado de {es2(es[START])} hijos por mujer en {START} a {es2(es[last])} en {last}",
        subtitle=f"Indicador coyuntural de fecundidad en España, {START}-{last}, hijos por mujer",
        unit="Hijos por mujer",
        source=INE_ICF,
        notes=["Número medio de hijos que tendría una mujer a lo largo de su vida si se mantuvieran las tasas de fecundidad por edad de ese año. "
               "Madres de todas las nacionalidades.",
               f"El dato más bajo de la serie es el de {low_y} ({es2(es[low_y])}).",
               "Línea de referencia: 2,1 hijos por mujer, el nivel con el que una población se mantiene sin migraciones."],
        rows=[{"time": str(y), "series": "fecundidad", "value": round(es[y], 2)} for y in years],
        extra={"dimensions": {"series": {"fecundidad": {"es": "Hijos por mujer"}}},
               "ref_line": {"value": 2.1, "label": {"es": "2,1"}}},
    )


def esperanza_dependencia():
    life = {int(r["period"]): r["value"] for r in sources.ine_table(LIFE_TABLE) if r["series"] == "Mortalidad. Total Nacional. Ambos sexos"}
    dep = _dependencia()["ES"]
    assert life and dep
    ly, dy = max(life), max(dep)
    covid = life.get(2020)
    life_chart = chart(
        id="det2-esperanza-vida",
        lens="tiempo", theme="demografia",
        title=f"La esperanza de vida al nacer ha pasado de {es1(life[START])} años en {START} a {es1(life[ly])} en {ly}",
        subtitle=f"Esperanza de vida al nacimiento en España, ambos sexos, {START}-{ly}, en años",
        unit="Años",
        source=INE_LIFE,
        notes=["Años que viviría de media una persona nacida ese año si se mantuvieran las tasas de mortalidad por edad de ese año."]
              + ([f"En 2020 bajó a {es1(covid)} años por la mortalidad de la covid-19 y se recuperó en los años siguientes."] if covid else []),
        rows=[{"time": str(y), "series": "esperanza", "value": round(life[y], 1)} for y in sorted(life)],
        extra={"dimensions": {"series": {"esperanza": {"es": "Esperanza de vida"}}}},
    )
    dep_chart = chart(
        id="det3-dependencia",
        lens="tiempo", theme="demografia",
        title=f"En {START} había {es1(dep[START])} mayores de 64 por cada 100 personas de 16 a 64 años; en {dy}, {es1(dep[dy])}",
        subtitle=f"Tasa de dependencia de la población mayor de 64 años en España, 1 de enero de cada año, {START}-{dy}",
        unit="Mayores de 64 por cada 100 personas de 16 a 64",
        source=INE_DEP,
        notes=["Población de 65 años o más dividida por la población de 16 a 64 años, por 100. Es una medida demográfica: no tiene "
               "en cuenta cuántas personas trabajan."],
        rows=[{"time": str(y), "series": "dependencia", "value": round(dep[y], 1)} for y in sorted(dep)],
        extra={"dimensions": {"series": {"dependencia": {"es": "Mayores de 64 por cada 100 de 16 a 64"}}}},
    )
    return [life_chart, dep_chart]


BUILDERS = [europa_fecundidad, europa_pensiones, dependencia_comunidades, fecundidad_comunidades, fecundidad_tiempo,
            esperanza_dependencia]
