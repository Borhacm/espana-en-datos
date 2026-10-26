"""N03. Quién vota y quién no: la participación desde 1977.

Datos: participación en las 16 elecciones generales desde 1977 por provincia (Infoelectoral, ficheros MUNI), guardada
en data/base/participacion.json (dataset «participacion»): no se vuelve a descargar. Las comunidades suman sus
provincias (votantes entre censo de escrutinio).
"""

from collections import defaultdict

from datasets import participacion
from lib import geo
from lib.output import chart

from ..common import bi
from ..elecciones import _base
from ..legislatura import en1, es1

MONTHS = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
MONTHS_EN = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# Nombres cortos: el ranking corta las etiquetas de más de 14 caracteres en móvil (como en n01)
SHORT = {"07": "C. y León", "08": "C.-La Mancha", "10": "C. Valenciana"}
SHORT_EN = {"04": "Balearic Is.", "05": "Canary Is.", "07": "Castile-León", "08": "C.-La Mancha", "10": "Valencian C."}

CERA_ES = ("La participación oficial se calcula sobre el censo de escrutinio, que incluye a los españoles residentes en el "
           "extranjero (CERA), que votan mucho menos. Con el voto rogado (elecciones de 2011 a 2019) votaron todavía menos. "
           "Estos ficheros no separan su voto, así que no se puede descontar.")
CERA_EN = ("Official turnout is calculated on the final electoral roll, which includes Spaniards living abroad (CERA), who vote "
           "much less. Under the 'voto rogado' system (prior application required, elections from 2011 to 2019) even fewer of "
           "them voted. These files do not separate their vote, so it cannot be stripped out.")


PERE = {"name": "INE, Padrón de Españoles Residentes en el Extranjero", "dataset": "Tabla 71106",
        "url": "https://www.ine.es/jaxiT3/Tabla.htm?t=71106", "license": "Reutilización libre citando la fuente"}


def _the(code: str) -> str:
    """Artículo en inglés para los nombres que lo llevan ("the Canary Islands")."""
    return "the " if code in ("04", "05", "10", "16") else ""


def _data():
    base = _base("participacion", participacion.build)
    nat = {r["election"]: r for r in base["rows"] if r["geo"] == "ES"}
    assert len(nat) == len(participacion.ELECTIONS), sorted(nat)
    return base, nat


def _time(election: str) -> str:
    """'2019-11' -> '2019.833': el eje es numérico y hay dos elecciones en 2019."""
    y, m = int(election[:4]), int(election[5:])
    return str(round(y + (m - 1) / 12, 3)).removesuffix(".0")


def _label(election: str) -> dict:
    y, m = int(election[:4]), int(election[5:])
    return bi(f"{MONTHS[m - 1].capitalize()} de {y}", f"{MONTHS_EN[m - 1]} {y}")


def _name(election: str, lang: str) -> str:
    """Año, o mes y año si ese año hubo dos elecciones."""
    y = election[:4]
    twice = sum(e.startswith(y) for e in participacion.ELECTIONS) > 1
    m = int(election[5:])
    if not twice:
        return y
    return f"{MONTHS[m - 1]} de {y}" if lang == "es" else f"{MONTHS_EN[m - 1]} {y}"


def participacion_generales():
    _, nat = _data()
    els = sorted(nat)
    rows = [{"time": _time(e), "series": "ES", "value": nat[e]["turnout"], "election": e} for e in els]
    low = sorted(els, key=lambda e: nat[e]["turnout"])
    lowest3 = sorted(low[:3])
    cut = max(nat[e]["turnout"] for e in lowest3)
    assert nat[low[3]]["turnout"] > cut
    limit = int(cut) + 1  # "por debajo del 67 %"
    names = [_name(e, "es") for e in lowest3]
    names_en = [_name(e, "en") for e in lowest3]
    return chart(
        id="n03-participacion",
        lens="tiempo", theme="elecciones",
        title=bi(f"Las tres generales con menos participación desde 1977 son las de {names[0]}, {names[1]} y {names[2]}, "
                 f"todas por debajo del {limit} %",
                 f"The three general elections with the lowest turnout since 1977 are those of {names_en[0]}, {names_en[1]} "
                 f"and {names_en[2]}, all below {limit}%"),
        subtitle=bi(f"Participación en las elecciones al Congreso, % del censo, {els[0][:4]}-{els[-1][:4]}",
                    f"Turnout in elections to the Congress of Deputies, % of the electoral roll, {els[0][:4]}-{els[-1][:4]}"),
        unit=bi("% del censo", "% of the electoral roll"),
        source=_base("participacion", participacion.build)["source"],
        notes={"es": ["Votantes: votos a candidaturas, en blanco y nulos.", CERA_ES],
               "en": ["Voters: votes for candidates, blank and spoilt ballots.", CERA_EN]},
        rows=rows,
        extra={"dimensions": {"series": {"ES": bi("España", "Spain")}},
               "time_labels": {_time(e): _label(e) for e in els}},
    )


def participacion_ccaa():
    base, nat = _data()
    last = sorted(nat)[-1]
    sums = defaultdict(lambda: [0, 0])
    for r in base["rows"]:
        if r["election"] == last and r["geo"] != "ES":
            s = sums[geo.ccaa_of_province(r["geo"])]
            s[0] += r["voters"]
            s[1] += r["census"]
    rows = [{"geo": c, "time": last[:4], "value": round(100 * v / n, 1), "voters": v, "census": n} for c, (v, n) in sums.items()]
    rows.append({"geo": "ES", "time": last[:4], "value": round(nat[last]["turnout"], 1),
                 "voters": nat[last]["voters"], "census": nat[last]["census"]})
    assert sum(r["voters"] for r in rows if r["geo"] != "ES") == nat[last]["voters"]
    # Ceuta y Melilla son extremos por su tamaño: fuera del titular, explicado en la nota
    regions = [r for r in rows if r["geo"] not in ("ES", "18", "19")]
    hi = max(regions, key=lambda r: r["value"])
    lo = min(regions, key=lambda r: r["value"])
    gap = round(hi["value"] - lo["value"], 1)
    year = last[:4]
    return chart(
        id="n03-participacion-ccaa",
        lens="dentro", theme="elecciones",
        title=bi(f"En {year} votó el {es1(hi['value'])} % del censo en {geo.CCAA[hi['geo']]} y el {es1(lo['value'])} % en "
                 f"{geo.CCAA[lo['geo']]}: {es1(gap)} puntos de diferencia",
                 f"In {year}, {en1(hi['value'])}% of the electoral roll voted in {_the(hi['geo'])}{geo.CCAA_EN[hi['geo']]} and {en1(lo['value'])}% in "
                 f"{_the(lo['geo'])}{geo.CCAA_EN[lo['geo']]}: a gap of {en1(gap)} points"),
        subtitle=bi(f"Participación en las elecciones al Congreso de julio de {year} por comunidad, % del censo",
                    f"Turnout in the July {year} election to the Congress of Deputies by region, % of the electoral roll"),
        unit=bi("% del censo", "% of the electoral roll"),
        source={**base["source"], "also": [PERE]},
        notes={"es": ["Cada comunidad suma los votantes y el censo de sus provincias.",
                      "Los residentes en el extranjero (CERA) cuentan en la provincia donde están inscritos y bajan la participación "
                      "donde son muchos en relación con el censo, como en Galicia, Asturias o Canarias (INE, padrón de españoles residentes en el extranjero). Las de 2023 son las primeras generales sin voto rogado desde 2008 (Ley Orgánica 12/2022).",
                      "Ceuta y Melilla, con un diputado cada una, quedan fuera del titular: sus porcentajes cambian mucho de una elección a otra."],
               "en": ["Each region adds up the voters and the electoral roll of its provinces.",
                      "Residents abroad (CERA) are counted in the province where they are registered and lower turnout where there "
                      "are many of them relative to the roll, as in Galicia, Asturias or the Canary Islands (INE, register of Spaniards living abroad). The 2023 election is the first general election without 'voto rogado' since 2008 (Organic Law 12/2022).",
                      "Ceuta and Melilla, with one deputy each, are left out of the title: their percentages change a lot from one election to the next."]},
        rows=sorted(rows, key=lambda r: r["geo"]),
        geos={c: {"es": "España" if c == "ES" else SHORT.get(c, geo.CCAA[c]),
                  "en": "Spain" if c == "ES" else SHORT_EN.get(c, geo.CCAA_EN[c]), "ccaa": c != "ES", "aggregate": c == "ES"}
              for c in sorted(r["geo"] for r in rows)},
    )


BUILDERS = [participacion_generales, participacion_ccaa]
