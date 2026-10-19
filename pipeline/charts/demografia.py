"""Tema Demografía y pensiones (código DE): gasto en pensiones y tasa de sustitución frente a la UE, años de jubilación,
envejecimiento y ocupados por cada mayor en cada comunidad, fecundidad, descomposición del gasto y proyecciones hasta 2075.

Revisado el 19 de octubre de 2026: cada gráfico responde a una pregunta del guion (editorial/registro/a03.md) y ningún
hallazgo se repite en dos miradas."""

from collections import defaultdict

from lib import geo, sources
from lib.output import THEMES, chart

import math
import re

from .common import annual, ine_ccaa
from .legislatura import CPI_TABLE, INE_CPI, _eu_rank, _place, es1

THEMES["demografia"] = {"code": "DE", "title": "Demografía y pensiones: un país que envejece"}

DEP_TABLE = 1455        # INE, Indicadores Demográficos Básicos: tasa de dependencia de los mayores de 64 por comunidad (anual)
ICF_TABLE = 1441        # INE, IDB: indicador coyuntural de fecundidad por comunidad y nacionalidad de la madre (anual)
LIFE_TABLE = 1414       # INE, IDB: esperanza de vida al nacimiento según sexo (anual)
EPA_OCC_TABLE = 65302   # INE, EPA: ocupados por grupo de edad, sexo y comunidad (trimestral, miles)
EPA_POP_TABLE = 65285   # INE, EPA: población por grupo de edad, sexo y comunidad (trimestral, miles)
PROJ_TABLE = 36652      # INE, Proyecciones de Población 2026-2075: población por escenario, sexo, edad y año
START = 1975            # primer año de las series del INE
BASE = 2008             # año de referencia de la descomposición del gasto y de los ocupados por mayor

INE = {"license": "Reutilización libre citando la fuente"}
INE_DEP = {"name": "INE, Indicadores Demográficos Básicos", "dataset": f"Tabla {DEP_TABLE}",
           "url": f"https://www.ine.es/jaxiT3/Tabla.htm?t={DEP_TABLE}", **INE}
INE_ICF = {"name": "INE, Indicadores Demográficos Básicos", "dataset": f"Tabla {ICF_TABLE}",
           "url": f"https://www.ine.es/jaxiT3/Tabla.htm?t={ICF_TABLE}", **INE}
INE_EPA = {"name": "INE, Encuesta de Población Activa", "dataset": f"Tablas {EPA_OCC_TABLE} y {EPA_POP_TABLE}",
           "url": f"https://www.ine.es/jaxiT3/Tabla.htm?t={EPA_OCC_TABLE}", **INE}
INE_PROJ = {"name": "INE, Proyecciones de Población 2026-2075", "dataset": f"Tabla {PROJ_TABLE}",
            "url": f"https://www.ine.es/jaxiT3/Tabla.htm?t={PROJ_TABLE}", **INE}
EUROSTAT_LICENSE = {"license": "CC BY 4.0"}
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

def _eu_last(raw: list[dict], digits: int) -> tuple[list[dict], str]:
    """Filas de un ranking UE con el último año que tiene dato de la media de la UE."""
    last = max(r["time"] for r in raw if geo.from_eurostat(r["geo"]) == "EU27")
    out = []
    for r in raw:
        c = geo.from_eurostat(r["geo"])
        if r["time"] == last and c and (c == "EU27" or geo.COUNTRIES.get(c, (0, 0, 0, False))[3]):
            out.append({"geo": c, "time": last, "value": round(r["value"], digits)})
    return sorted(out, key=lambda r: r["geo"]), last


def europa_sustitucion():
    raw = sources.eurostat("ilc_pnp3", sex="T")
    # Eurostat da la ratio (0,81): se pasa a porcentaje
    raw = [{**r, "value": 100 * r["value"]} for r in raw]
    out, last = _eu_last(raw, 0)
    es = next(r for r in out if r["geo"] == "ESP")
    eu = next(r for r in out if r["geo"] == "EU27")
    ranked = sorted((r for r in out if r["geo"] != "EU27"), key=lambda r: -r["value"])
    above = [geo.COUNTRIES[r["geo"]][1] for r in ranked if r["value"] > es["value"]]
    es_hist = {r["time"]: r["value"] for r in raw if r["geo"] == "ES"}
    first = min(es_hist)
    return chart(
        id="dee3-europa-sustitucion",
        lens="europa", theme="demografia",
        title=f"La pensión mediana de los jubilados españoles equivale al {es['value']:.0f} % del salario mediano de quienes "
              f"están a punto de jubilarse; en la UE, al {eu['value']:.0f} %",
        subtitle=f"Tasa de sustitución agregada, {last}: pensión mediana de 65 a 74 años en % de la renta del trabajo mediana de "
                 "50 a 59 años, en bruto",
        unit="%",
        source={"name": "Eurostat, encuesta de condiciones de vida (EU-SILC)", "dataset": "ilc_pnp3",
                "url": "https://ec.europa.eu/eurostat/databrowser/view/ilc_pnp3/default/table", **EUROSTAT_LICENSE},
        notes=["Compara dos grupos distintos en el mismo año: las pensiones individuales de las personas de 65 a 74 años y las rentas "
               "del trabajo de las de 50 a 59. No es la pensión que cobrará cada trabajador sobre su último sueldo.",
               "Cantidades brutas, sin descontar impuestos. Solo pensiones; no incluye otras prestaciones sociales.",
               "Países con una tasa más alta que España: " + (", ".join(above) if above else "ninguno") + ".",
               f"España, {first}: {es_hist[first]:.0f} %."],
        rows=out,
        geos=geo.country_table(r["geo"] for r in out),
    )


def europa_vida65():
    raw = sources.eurostat("demo_mlexpec", sex="T", age="Y65")
    out, last = _eu_last(raw, 1)
    es = next(r for r in out if r["geo"] == "ESP")
    eu = next(r for r in out if r["geo"] == "EU27")
    top = max(r["value"] for r in out if r["geo"] != "EU27")
    tied = sorted(geo.COUNTRIES[r["geo"]][1] for r in out if r["geo"] not in ("EU27", "ESP") and r["value"] == top)
    es_hist = {r["time"]: r["value"] for r in raw if r["geo"] == "ES"}
    assert es["value"] == top, (es, top)
    title = (f"A los 65 años, a un español le quedan de media {es1(es['value'])} años de vida, "
             + (f"igual que en {', '.join(tied)} y más que en ningún otro país de la UE" if tied else "más que en ningún otro país de la UE")
             + f" (media: {es1(eu['value'])})")
    return chart(
        id="dee4-europa-vida65",
        lens="europa", theme="demografia",
        title=title,
        subtitle=f"Esperanza de vida a los 65 años, ambos sexos, {last}, en años",
        unit="Años",
        source={"name": "Eurostat", "dataset": "demo_mlexpec",
                "url": "https://ec.europa.eu/eurostat/databrowser/view/demo_mlexpec/default/table", **EUROSTAT_LICENSE},
        notes=["Años que viviría de media una persona que cumple 65 años si se mantuvieran las tasas de mortalidad por edad de ese año.",
               f"España: {es1(es_hist['1975'])} años en 1975, {es1(es_hist[str(BASE)])} en {BASE}.",
               "Datos de la UE estimados o provisionales por Eurostat."],
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

def _epa_avg(table: int, kind: str, periods: list[str]) -> dict[str, float]:
    """Media de los trimestres indicados, por comunidad, de una serie de la EPA en miles."""
    by = defaultdict(list)
    for r in sources.ine_table(table):
        parts = r["series"].split(". ")
        if r["period"] in periods and parts[0] == "Ambos sexos" and kind in r["series"]:
            code = ine_ccaa(parts[1])
            if code:
                by[code].append(r["value"])
    assert all(len(v) == len(periods) for v in by.values()), {k: len(v) for k, v in by.items()}
    out = {c: sum(v) / len(v) for c, v in by.items()}
    # La tabla de ocupados no trae el total nacional con el mismo nombre: es la suma de las comunidades y ciudades autónomas
    if "ES" not in out:
        out["ES"] = sum(v for c, v in out.items())
    return out


def ocupados_mayores():
    periods = sorted({r["period"] for r in sources.ine_table(EPA_POP_TABLE, last=4)})
    assert len(periods) == 4
    base = [f"{BASE}Q{q}" for q in range(1, 5)]
    occ, old = _epa_avg(EPA_OCC_TABLE, "Ocupados. Total", periods), _epa_avg(EPA_POP_TABLE, "65 y más años", periods)
    occ0, old0 = _epa_avg(EPA_OCC_TABLE, "Ocupados. Total", base), _epa_avg(EPA_POP_TABLE, "65 y más años", base)
    out = [{"geo": c, "time": periods[-1][:4], "value": round(occ[c] / old[c], 2), "prev": round(occ0[c] / old0[c], 2)}
           for c in sorted(occ)]
    assert len(out) == 20
    es = next(r for r in out if r["geo"] == "ES")
    main = [r for r in out if r["geo"] not in ("ES", "18", "19")]
    top = max(main, key=lambda r: r["value"])
    low = min(main, key=lambda r: r["value"])
    fell = sum(r["value"] < r["prev"] for r in main)
    g_occ, g_old = 100 * (occ["ES"] / occ0["ES"] - 1), 100 * (old["ES"] / old0["ES"] - 1)
    p0, p1 = periods[0], periods[-1]
    q = lambda p: f"{['primer', 'segundo', 'tercer', 'cuarto'][int(p[-1]) - 1]} trimestre de {p[:4]}"
    return chart(
        id="ded3-ocupados-mayores",
        lens="dentro", theme="demografia",
        title=(f"Hay menos ocupados por cada mayor de 64 que en {BASE} en {'las' if fell == len(main) else str(fell) + ' de las'} "
               f"{len(main)} comunidades: en España, {es2(es['value'])} frente a {es2(es['prev'])}"),
        subtitle=f"Ocupados de todas las edades por cada persona de 65 años o más, media del {q(p0)} al {q(p1)}",
        unit="Ocupados por cada mayor de 64",
        source=INE_EPA,
        notes=["Ocupados de 16 años y más (también los mayores de 64 que trabajan) divididos por la población de 65 años y más, "
               "las dos de la EPA y en medias de cuatro trimestres.",
               "No es la ratio de afiliados por pensión de la Seguridad Social: no todos los ocupados cotizan al mismo régimen, "
               "no todos los mayores de 64 cobran pensión y hay pensionistas menores de 65 (incapacidad, viudedad, jubilación anticipada).",
               f"«prev» en la descarga: media de los cuatro trimestres de {BASE}. Desde entonces, en España los ocupados han "
               f"crecido un {es1(g_occ)} % y los mayores de 64, un {es1(g_old)} %.",
               f"Extremos del último año (sin Ceuta ni Melilla): {geo.CCAA[top['geo']]}, {es2(top['value'])}; "
               f"{geo.CCAA[low['geo']]}, {es2(low['value'])}.",
               "La EPA es una encuesta: en las comunidades pequeñas tiene más margen de error. Ceuta y Melilla no protagonizan el titular."],
        rows=out,
        geos=geo.ccaa_table(r["geo"] for r in out),
    )



# ---------- España en el tiempo ----------

def fecundidad_tiempo():
    es = _fecundidad()["ES"]
    years = sorted(es)
    last = years[-1]
    low_y = min(years, key=lambda y: (es[y], -y))
    # Contexto europeo para las notas (Eurostat redondea distinto que el INE: solo se usa el puesto y la media de la UE)
    eu_raw = sources.eurostat("demo_find", indic_de="TOTFERRT")
    eu_rows, eu_last = _eu_last(eu_raw, 2)
    eu = next(r["value"] for r in eu_rows if r["geo"] == "EU27")
    ranked = sorted((r for r in eu_rows if r["geo"] != "EU27"), key=lambda r: r["value"])
    lower = [geo.COUNTRIES[r["geo"]][1] for r in ranked if r["value"] < next(x["value"] for x in ranked if x["geo"] == "ESP")]
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
               "Línea de referencia: 2,1 hijos por mujer, el nivel con el que una población se mantiene sin migraciones.",
               f"En la UE ({eu_last}, Eurostat): media de {es2(eu)} hijos por mujer; con menos que España, "
               + (", ".join(lower) if lower else "ningún país") + f". Ningún país de la UE llega a 2,1."
               if all(r["value"] < 2.1 for r in ranked) else f"En la UE ({eu_last}, Eurostat): media de {es2(eu)}."],
        rows=[{"time": str(y), "series": "fecundidad", "value": round(es[y], 2)} for y in years],
        extra={"dimensions": {"series": {"fecundidad": {"es": "Hijos por mujer"}}},
               "ref_line": {"value": 2.1, "label": {"es": "2,1"}}},
    )


def gasto_descomposicion():
    exp = {int(r["time"]): r["value"] for r in sources.eurostat("spr_exp_pens", spdepb="TOTAL", spdepm="TOTAL",
                                                                 unit="MIO_EUR", geo="ES")}
    ben = {int(r["time"]): r["value"] for r in sources.eurostat("spr_pns_ben", geo="ES")
           if r["spdepb"] == "TOTAL" and r["sex"] == "T" and r["spscheme"] == "TOTAL" and r["spdepm"] == "TOTAL"}
    cpi = annual([r for r in sources.ine_table(CPI_TABLE) if r["series"].startswith("Índice general. Índice")
                  or r["series"].startswith("Nacional. Índice general. Índice")])
    years = [y for y in sorted(set(exp) & set(ben) & set(cpi)) if y >= BASE]
    assert years[0] == BASE, years
    series = {"gasto": {y: exp[y] / cpi[y] for y in years}, "pensionistas": {y: ben[y] for y in years},
              "media": {y: exp[y] / ben[y] / cpi[y] for y in years}}
    idx = {k: {y: 100 * v[y] / v[BASE] for y in years} for k, v in series.items()}
    rows = [{"time": str(y), "series": k, "value": round(v[y], 1)} for k, v in idx.items() for y in years]
    last = years[-1]
    g, n, m = (round(idx[k][last] - 100, 1) for k in ("gasto", "pensionistas", "media"))
    share_n = 100 * math.log(idx["pensionistas"][last] / 100) / math.log(idx["gasto"][last] / 100)
    return chart(
        id="det4-gasto-descomposicion",
        lens="tiempo", theme="demografia",
        title=f"Entre {BASE} y {last}, el gasto real en pensiones sube un {es1(g)} %: hay un {es1(n)} % más de pensionistas "
              f"y cada uno cobra de media un {es1(m)} % más, descontada la inflación",
        subtitle=f"Gasto en pensiones descontada la inflación, número de pensionistas y gasto real por pensionista. Índices, {BASE} = 100, {BASE}-{last}",
        unit=f"Índice ({BASE} = 100)",
        source={"name": "Eurostat, SEEPROS", "dataset": "spr_exp_pens y spr_pns_ben",
                "url": "https://ec.europa.eu/eurostat/databrowser/view/spr_pns_ben/default/table", **EUROSTAT_LICENSE,
                "also": [INE_CPI]},
        notes=["Gasto: todas las pensiones de la definición europea (jubilación, viudedad, orfandad, incapacidad; públicas y de "
               "funcionarios), en euros, deflactado con el IPC medio de cada año.",
               "Pensionistas: personas que cobran al menos una pensión, contadas una sola vez aunque cobren dos.",
               f"El gasto real crece porque crecen las dos cosas: {es1(100 + n)} x {es1(100 + m)} / 100 = {es1(100 + g)}. "
               f"En escala logarítmica, el número de pensionistas explica el {share_n:.0f} % de la subida y la pensión media, el resto.",
               "La pensión media sube también porque los nuevos jubilados tuvieron salarios y carreras de cotización mayores que "
               "quienes fallecen (efecto sustitución), no solo por la revalorización de las pensiones ya existentes."],
        rows=rows,
        extra={"dimensions": {"series": {"gasto": {"es": "Gasto real"}, "pensionistas": {"es": "Pensionistas"},
                                         "media": {"es": "Por pensionista"}}},
               "ref_line": {"value": 100, "label": {"es": str(BASE)}}},
    )


def _proyeccion() -> dict[str, dict[int, float]]:
    """Tasa de dependencia de los mayores de 64 (65+ / 16-64, por 100) por escenario de las proyecciones del INE."""
    pop = defaultdict(lambda: defaultdict(float))
    for r in sources.ine_table(PROJ_TABLE):
        parts = r["series"].split(". ")
        m = re.match(r"(\d+)", parts[4])
        if parts[1] != "Total" or not m:
            continue
        age = int(m.group(1))
        if 16 <= age <= 64:
            pop[(parts[0], r["year"])]["w"] += r["value"]
        elif age >= 65:
            pop[(parts[0], r["year"])]["o"] += r["value"]
    by = defaultdict(dict)
    for (sc, y), v in pop.items():
        by[sc][y] = 100 * v["o"] / v["w"]
    return by


def dependencia_proyeccion():
    hist = _dependencia()["ES"]
    proj = _proyeccion()
    central, nulo = proj["Central"], proj["Saldo migratorio nulo"]
    h1 = max(hist)
    end = 2075
    years = [y for y in sorted(central) if h1 < y <= end]
    rows = ([{"time": str(y), "series": "historico", "value": round(hist[y], 1)} for y in sorted(hist)]
            # El último dato observado abre las dos proyecciones para que las líneas empiecen en el mismo punto
            + [{"time": str(y), "series": k, "value": round(hist[h1] if y == h1 else s[y], 1)}
               for k, s in (("central", central), ("nulo", nulo)) for y in [h1] + years])
    y50 = 2050
    mid = [y for y in years if y <= 2060]
    peak_y = max(mid, key=lambda y: central[y])
    trough_y = min((y for y in years if y > peak_y), key=lambda y: central[y])
    return chart(
        id="det5-dependencia-proyeccion",
        lens="tiempo", theme="demografia",
        title=f"El INE proyecta {es1(central[y50])} mayores de 64 por cada 100 personas de 16 a 64 años en {y50}; "
              f"sin migración, serían {es1(nulo[y50])}",
        subtitle=f"Tasa de dependencia de los mayores de 64: observada, {START}-{h1}, y proyectada, {years[0]}-{end}, en dos escenarios del INE",
        unit="Mayores de 64 por cada 100 personas de 16 a 64",
        source={**INE_DEP, "also": [INE_PROJ]},
        notes=["Población de 65 años o más dividida por la población de 16 a 64 años, por 100.",
               "Escenario central del INE: fecundidad, esperanza de vida y saldo migratorio según las tendencias recientes. "
               "Escenario de saldo migratorio nulo: tantas entradas como salidas de población cada año.",
               f"En el escenario central, la tasa calculada con la población proyectada coincide con la que publica el INE (tabla 36670). "
               f"Sube hasta {es1(central[peak_y])} en {peak_y}, baja hasta {es1(central[trough_y])} en {trough_y} "
               f"y vuelve a subir hasta {es1(central[end])} en {end}. Sin migración, llega a {es1(nulo[end])} en {end}.",
               f"Otros escenarios del INE en {y50} y {end}: fecundidad alta, {es1(proj['Fecundidad alta'][y50])} y "
               f"{es1(proj['Fecundidad alta'][end])}; fecundidad baja, {es1(proj['Fecundidad baja'][y50])} y {es1(proj['Fecundidad baja'][end])}; "
               f"saldo migratorio alto, {es1(proj['Saldo migratorio alto'][y50])} y {es1(proj['Saldo migratorio alto'][end])}; "
               f"saldo migratorio bajo, {es1(proj['Saldo migratorio bajo'][y50])} y {es1(proj['Saldo migratorio bajo'][end])}.",
               "Una proyección no es una predicción: muestra qué pasaría si se cumplieran sus supuestos.",
               f"La serie observada es del 1 de enero de cada año; la proyectada empieza en {years[0]}."],
        rows=rows,
        extra={"dimensions": {"series": {"historico": {"es": "Observada"}, "central": {"es": "Central"},
                                         "nulo": {"es": "Sin migración"}}}},
    )



BUILDERS = [europa_pensiones, europa_sustitucion, europa_vida65, dependencia_comunidades, ocupados_mayores, fecundidad_tiempo,
            gasto_descomposicion, dependencia_proyeccion]
