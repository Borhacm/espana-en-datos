"""Tema La legislatura en datos (código LE): paro, empleo, salarios, precios, deuda y déficit desde las generales de julio de 2023.

Balance descriptivo: compara el último periodo disponible con 2023, el año de las últimas generales. No atribuye mérito ni culpa.
"""

from collections import defaultdict

from lib import geo, sources
from lib.output import THEMES, chart

from .common import annual, ine_ccaa, pct

THEMES["legislatura"] = {"code": "LE", "title": "La legislatura en datos"}

START = 2023            # año de las últimas generales (23 de julio de 2023)
PARO_TABLE = 65334      # INE, EPA: tasas de paro por edad, sexo y comunidad (trimestral)
OCUP_TABLE = 65302      # INE, EPA: ocupados por edad, sexo y comunidad, miles (trimestral)
WAGE_TABLE = 6061       # INE, ETCL: coste salarial por trabajador y comunidad (trimestral)
CPI_TABLE = 24077       # INE, IPC: índice general nacional (mensual)

INE_EPA = {"name": "INE, Encuesta de Población Activa", "dataset": f"Tablas {PARO_TABLE} y {OCUP_TABLE}",
           "url": f"https://www.ine.es/jaxiT3/Tabla.htm?t={PARO_TABLE}", "license": "Reutilización libre citando la fuente"}
INE_WAGE = {"name": "INE, Encuesta Trimestral de Coste Laboral", "dataset": f"Tabla {WAGE_TABLE}",
            "url": f"https://www.ine.es/jaxiT3/Tabla.htm?t={WAGE_TABLE}", "license": "Reutilización libre citando la fuente"}
INE_CPI = {"name": "INE, Índice de Precios de Consumo", "url": f"https://www.ine.es/jaxiT3/Tabla.htm?t={CPI_TABLE}"}
ORDINAL = ["primer", "segundo", "tercer", "cuarto"]


def es1(v: float) -> str:
    """Un decimal con coma: 10,3."""
    return f"{v:.1f}".replace(".", ",")


def de(code: str) -> str:
    """«de Asturias», «del País Vasco», «de la Comunidad Valenciana»."""
    name = geo.CCAA[code]
    return {"País Vasco": "del País Vasco", "Comunidad Valenciana": "de la Comunidad Valenciana"}.get(name, f"de {name}")


def _qtime(period: str) -> float:
    y, q = period.split("Q")
    return round(int(y) + (int(q) - 1) / 4, 2)


def _qlabel(period: str) -> str:
    y, q = period.split("Q")
    return f"{ORDINAL[int(q) - 1]} trimestre de {y}"


def _last4(rs: list[dict]) -> tuple[float, str, str]:
    """Media de los cuatro últimos trimestres y su primer y último trimestre."""
    rs = sorted(rs, key=lambda r: r["period"])[-4:]
    return sum(r["value"] for r in rs) / 4, rs[0]["period"], rs[-1]["period"]


def _eu_rank(raw: list[dict], year: str, prev: str) -> list[dict]:
    """Filas de un ranking UE: valor del último año y del año de referencia."""
    by = defaultdict(dict)
    for r in raw:
        c = geo.from_eurostat(r["geo"])
        if c and (c == "EU27" or geo.COUNTRIES.get(c, (0, 0, 0, False))[3]):
            by[c][r["time"]] = r["value"]
    return [{"geo": c, "time": year, "value": round(v[year], 1), "prev": round(v[prev], 1)}
            for c, v in sorted(by.items()) if year in v and prev in v]


def _place(out: list[dict], code: str, reverse: bool = True) -> int:
    ranked = sorted((r for r in out if r["geo"] != "EU27"), key=lambda r: -r["value"] if reverse else r["value"])
    return [r["geo"] for r in ranked].index(code) + 1


# ---------- España frente a Europa ----------

def europa_paro():
    raw = sources.eurostat("une_rt_a", age="Y15-74", sex="T", unit="PC_ACT")
    last = max(r["time"] for r in raw if geo.from_eurostat(r["geo"]) == "EU27")
    out = _eu_rank(raw, last, str(START))
    es = next(r for r in out if r["geo"] == "ESP")
    eu = next(r for r in out if r["geo"] == "EU27")
    place = _place(out, "ESP")
    n = len(out) - 1
    first = "la más alta de la UE" if place == 1 else f"la {place}.ª más alta de la UE"
    return chart(
        id="lee1-europa-paro",
        lens="europa", theme="legislatura",
        title=f"La tasa de paro de España baja del {es1(es['prev'])} % al {es1(es['value'])} % entre {START} y {last}, "
              f"pero sigue siendo {first}",
        subtitle=f"Tasa de paro de 15 a 74 años, {last}, en % de la población activa. Media de la UE: {es1(eu['value'])} %",
        unit="% de la población activa",
        source={"name": "Eurostat", "dataset": "une_rt_a", "url": "https://ec.europa.eu/eurostat/databrowser/view/une_rt_a/default/table",
                "license": "CC BY 4.0"},
        notes=[f"Medias anuales de la Encuesta de Población Activa armonizada (para España, la EPA del INE). Compara {last} con {START}, "
               "el año de las últimas generales.",
               f"«prev» en la descarga: tasa de {START}. En {START} España también tenía la tasa más alta de los {n} países."
               if _place([{**r, "value": r["prev"]} for r in out], "ESP") == 1 else f"«prev» en la descarga: tasa de {START}."],
        rows=out,
        geos=geo.country_table(r["geo"] for r in out),
    )


def europa_deuda():
    raw = sources.eurostat("gov_10dd_edpt1", na_item="GD", sector="S13", unit="PC_GDP")
    last = max(r["time"] for r in raw if geo.from_eurostat(r["geo"]) == "EU27")
    out = _eu_rank(raw, last, str(START))
    es = next(r for r in out if r["geo"] == "ESP")
    eu = next(r for r in out if r["geo"] == "EU27")
    place = _place(out, "ESP")
    return chart(
        id="lee2-europa-deuda",
        lens="europa", theme="legislatura",
        title=f"La deuda pública baja del {es1(es['prev'])} % al {es1(es['value'])} % del PIB entre {START} y {last}; "
              f"en la UE pasa del {es1(eu['prev'])} % al {es1(eu['value'])} %",
        subtitle=f"Deuda de las administraciones públicas, {last}, en % del PIB. España es la {place}.ª más alta de {len(out) - 1}",
        unit="% del PIB",
        source={"name": "Eurostat", "dataset": "gov_10dd_edpt1",
                "url": "https://ec.europa.eu/eurostat/databrowser/view/gov_10dd_edpt1/default/table", "license": "CC BY 4.0"},
        notes=["Deuda según el Protocolo de Déficit Excesivo (criterio de Maastricht): Estado, comunidades, ayuntamientos y "
               "Seguridad Social, a valor nominal y consolidada.",
               "La ratio baja si la deuda crece menos que el PIB nominal: en euros, la deuda de España ha seguido subiendo.",
               f"«prev» en la descarga: deuda de {START}."],
        rows=out,
        geos=geo.country_table(r["geo"] for r in out),
    )


# ---------- España por dentro ----------

def _paro_rows():
    rows = [r for r in sources.ine_table(PARO_TABLE)
            if r["series"].startswith("Tasa de paro de la población. Ambos sexos.") and r["series"].endswith(". Total")]
    by = defaultdict(list)
    for r in rows:
        code = ine_ccaa(r["series"].split(". ")[2])
        if code:
            by[code].append(r)
    assert len(by) == 20, sorted(by)
    return by


def paro_comunidades():
    by = _paro_rows()
    out, p0, p1 = [], None, None
    for code, rs in by.items():
        v, p0, p1 = _last4(rs)
        prev = annual(rs)[START]
        out.append({"geo": code, "time": p1, "value": round(v, 1), "prev": round(prev, 1), "change": round(v - prev, 1)})
    es = next(r for r in out if r["geo"] == "ES")
    main = [r for r in out if r["geo"] not in ("ES", "18", "19")]
    down = [r for r in main if r["change"] < 0]
    top = max(main, key=lambda r: r["value"])
    low = min(main, key=lambda r: r["value"])
    who = "las 17 comunidades" if len(down) == 17 else f"{len(down)} de las 17 comunidades"
    return chart(
        id="led1-paro-comunidades",
        lens="dentro", theme="legislatura",
        title=f"El paro ha bajado desde {START} en {who}, pero va del {es1(low['value'])} % {de(low['geo'])} "
              f"al {es1(top['value'])} % {de(top['geo'])}",
        subtitle=f"Tasa de paro, media de los cuatro trimestres del {_qlabel(p0)} al {_qlabel(p1)}, en %. "
                 f"España: {es1(es['value'])} % ({es1(es['prev'])} % en {START})",
        unit="% de la población activa",
        source=INE_EPA,
        notes=["Encuesta de Población Activa, población de 16 años y más. Media de los últimos cuatro trimestres para evitar la "
               "estacionalidad (el paro sube en invierno y baja en verano).",
               f"«prev» en la descarga: media de {START}; «change»: diferencia en puntos.",
               "Ceuta y Melilla tienen muestras pequeñas en la EPA y sus tasas varían mucho de un trimestre a otro."],
        rows=sorted(out, key=lambda r: r["geo"]),
        geos=geo.ccaa_table(r["geo"] for r in out),
    )


def empleo_comunidades():
    rows = sources.ine_table(OCUP_TABLE)
    by = defaultdict(list)
    for r in rows:
        s = r["series"]
        if s == "Total Nacional. Ambos sexos. Total. Ocupados. Valor absoluto":
            by["ES"].append(r)
        elif s.startswith("Ambos sexos. ") and s.endswith(". Ocupados. Total. Valor absoluto"):
            code = ine_ccaa(s.split(". ")[1])
            if code and code != "ES":
                by[code].append(r)
    assert len(by) == 20, sorted(by)
    out, p0, p1 = [], None, None
    for code, rs in by.items():
        v, p0, p1 = _last4(rs)
        prev = annual(rs)[START]
        out.append({"geo": code, "time": p1, "value": pct(prev, v), "thousands": round(v, 1), "prev_thousands": round(prev, 1)})
    es = next(r for r in out if r["geo"] == "ES")
    main = [r for r in out if r["geo"] not in ("ES", "18", "19")]
    top = max(main, key=lambda r: r["value"])
    low = min(main, key=lambda r: r["value"])
    gain_txt = es1((es["thousands"] - es["prev_thousands"]) / 1000)
    return chart(
        id="led2-empleo-comunidades",
        lens="dentro", theme="legislatura",
        title=f"El número de ocupados ha crecido un {es1(es['value'])} % desde {START}: del {es1(top['value'])} % "
              f"{de(top['geo'])} al {es1(low['value'])} % {de(low['geo'])}",
        subtitle=f"Variación de los ocupados entre la media de {START} y la de los cuatro trimestres del {_qlabel(p0)} al "
                 f"{_qlabel(p1)}, en %. España: {gain_txt} millones de ocupados más",
        unit="% de variación",
        source=INE_EPA,
        notes=["Encuesta de Población Activa: personas de 16 años y más que trabajaron al menos una hora en la semana de referencia. "
               "Cuenta personas, no contratos ni afiliaciones a la Seguridad Social.",
               "Media de los últimos cuatro trimestres frente a la media de 2023. «thousands» y «prev_thousands» en la descarga: "
               "ocupados en miles.",
               "Parte de la diferencia entre comunidades se debe a cuánto crece su población: este dato no es una tasa.",
               "La EPA es una encuesta: en las comunidades menos pobladas el error de muestreo es mayor, así que las diferencias "
               "pequeñas entre ellas no son significativas. Ceuta y Melilla tienen muestras muy pequeñas."],
        rows=sorted(out, key=lambda r: r["geo"]),
        geos=geo.ccaa_table(r["geo"] for r in out),
    )


# ---------- España en el tiempo ----------

def paro_tiempo():
    es = sorted(_paro_rows()["ES"], key=lambda r: r["period"])
    rows = [{"time": _qtime(r["period"]), "series": "paro", "value": round(r["value"], 2)} for r in es if r["year"] >= 2008]
    roll = [(es[i]["period"], sum(x["value"] for x in es[i - 3:i + 1]) / 4) for i in range(3, len(es))]
    last_p, last_v = roll[-1]
    # Último periodo de cuatro trimestres con un paro igual o más bajo que el actual
    since = max((p for p, v in roll[:-1] if v <= last_v), default=None)
    since_year = since[:4] if since else None
    prev = annual(es)[START]
    return chart(
        id="let1-paro",
        lens="tiempo", theme="legislatura",
        title=f"El paro, en el {es1(last_v)} % en el último año, está en su nivel más bajo desde {since_year}",
        subtitle=f"Tasa de paro trimestral desde 2008, en % de la población activa, hasta el {_qlabel(last_p)}",
        unit="% de la población activa",
        source=INE_EPA,
        notes=["Encuesta de Población Activa, población de 16 años y más. Datos trimestrales sin desestacionalizar: el paro sube "
               "cada primer trimestre y baja en verano.",
               f"Titular: media de los cuatro últimos trimestres ({es1(last_v)} %), frente a la media de {START} ({es1(prev)} %). "
               f"La última vez que esa media estuvo igual o más baja fue en el periodo que acaba en el {_qlabel(since)}."],
        rows=rows,
        extra={"dimensions": {"series": {"paro": {"es": "Tasa de paro"}}}, "quarterly": True,
               "events": [{"time": 2023.5, "label": {"es": "Elecciones generales (23 de julio de 2023)"}}]},
    )


def salarios_precios():
    wage_name = ("Total Nacional. Industria, construcción y servicios (excepto actividades de los hogares como empleadores y de "
                 "organizaciones y organismos extraterritoriales). Coste salarial total. Costes laborales. Euros")
    wage = [r for r in sources.ine_table(WAGE_TABLE) if r["series"] == wage_name]
    cpi = [r for r in sources.ine_table(CPI_TABLE) if r["series"].startswith("Índice general. Índice")
           or r["series"].startswith("Nacional. Índice general. Índice")]
    assert wage and cpi, (len(wage), len(cpi))
    series = {"salarios": annual(wage), "precios": annual(cpi)}
    years = [y for y in sorted(set(series["salarios"]) & set(series["precios"])) if y >= 2015]
    rows = [{"time": str(y), "series": k, "value": round(100 * s[y] / s[START], 1)} for k, s in series.items() for y in years]
    last = years[-1]
    w, p = pct(series["salarios"][START], series["salarios"][last]), pct(series["precios"][START], series["precios"][last])
    real = pct(series["salarios"][START] / series["precios"][START], series["salarios"][last] / series["precios"][last])
    return chart(
        id="let2-salarios-precios",
        lens="tiempo", theme="legislatura",
        title=f"Entre {START} y {last}, el salario medio sube un {es1(w)} % y los precios, un {es1(p)} %",
        subtitle=f"Índices, {START} = 100. Salario medio por trabajador y precios de consumo, medias anuales desde 2015",
        unit=f"Índice ({START} = 100)",
        source={**INE_WAGE, "also": [INE_CPI]},
        notes=["Salario: coste salarial total por trabajador y mes (industria, construcción y servicios), media anual. "
               "Incluye pagas extra. Es una media: no dice cómo le ha ido al salario de cada persona.",
               "Precios: IPC general, media anual.",
               f"Descontada la inflación, el salario medio de {last} es un {es1(real)} % más alto que el de {START}.",
               "Solo años completos."],
        rows=rows,
        extra={"dimensions": {"series": {"salarios": {"es": "Salario medio"}, "precios": {"es": "Precios (IPC)"}}},
               "ref_line": {"value": 100, "label": {"es": str(START)}}},
    )


def deficit_tiempo():
    raw = sources.eurostat("gov_10dd_edpt1", na_item="B9", sector="S13", unit="PC_GDP", geo=["ES", "EU27_2020"])
    key = {"ES": "espana", "EU27_2020": "ue"}
    # Déficit en positivo: saldo con el signo cambiado (un superávit sale negativo)
    rows = [{"time": r["time"], "series": key[r["geo"]], "value": round(-r["value"], 1)}
            for r in raw if r["geo"] in key and int(r["time"]) >= 2008]
    val = {(r["series"], r["time"]): r["value"] for r in rows}
    years = sorted({r["time"] for r in rows if ("espana", r["time"]) in val and ("ue", r["time"]) in val})
    last = years[-1]
    es, eu = val[("espana", last)], val[("ue", last)]
    below = [y for y in years if val[("espana", y)] < val[("ue", y)]]
    lowest_since = max((y for y in years[:-1] if val[("espana", y)] <= es), default=None)
    title = (f"El déficit público baja al {es1(es)} % del PIB en {last}, por debajo de la media de la UE ({es1(eu)} %)"
             if es < eu else f"El déficit público es del {es1(es)} % del PIB en {last}; en la UE, del {es1(eu)} %")
    return chart(
        id="let3-deficit",
        lens="tiempo", theme="legislatura",
        title=title,
        subtitle=f"Déficit de las administraciones públicas, en % del PIB, 2008-{last}",
        unit="% del PIB",
        source={"name": "Eurostat", "dataset": "gov_10dd_edpt1",
                "url": "https://ec.europa.eu/eurostat/databrowser/view/gov_10dd_edpt1/default/table", "license": "CC BY 4.0"},
        notes=["Necesidad de financiación de las administraciones públicas (Estado, comunidades, ayuntamientos y Seguridad Social), "
               "según el Protocolo de Déficit Excesivo. Un valor negativo sería superávit.",
               f"Años con un déficit de España menor que el de la media de la UE: {', '.join(below) or 'ninguno'}.",
               f"Último año anterior con un déficit igual o menor que el de {last}: {lowest_since}." if lowest_since
               else f"El déficit de {last} es el más bajo de España desde 2008, el primer año del gráfico."],
        rows=rows,
        extra={"dimensions": {"series": {"espana": {"es": "España"}, "ue": {"es": "UE"}}},
               "ref_line": {"value": 3, "label": {"es": "Referencia UE: 3 %"}}},
    )


BUILDERS = [europa_paro, europa_deuda, paro_comunidades, empleo_comunidades, paro_tiempo, salarios_precios, deficit_tiempo]
