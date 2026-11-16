"""N06. Qué preocupa a los españoles: los problemas según el CIS.

Datos: pregunta de los barómetros mensuales del CIS sobre los tres principales problemas de España (respuesta
espontánea), desde enero de 2023, guardada en data/base/cis-problemas.json (dataset «cis-problemas»).
"""

from collections import defaultdict

from datasets import cis
from lib.output import chart

from ..common import bi
from ..elecciones import _base
from ..legislatura import en1, es1

MONTHS = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
MONTHS_EN = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# Categorías del CIS -> clave y nombre corto (el ranking corta en móvil las etiquetas largas)
SHORT = {
    "La vivienda": ("vivienda", "Vivienda", "Housing"),
    "La inmigración": ("inmigracion", "Inmigración", "Immigration"),
    "La crisis económica, los problemas de índole económica": ("economia", "Economía", "Economy"),
    "Los problemas relacionados con la calidad del empleo": ("calidad-empleo", "Calidad del empleo", "Job quality"),
    "El Gobierno y partidos o políticos/as concretos/as": ("gobierno", "Gobierno y partidos", "Gov. and parties"),
    "Los problemas políticos en general": ("politica", "Política en general", "Politics in general"),
    "La sanidad": ("sanidad", "Sanidad", "Healthcare"),
    "El paro": ("paro", "Paro", "Unemployment"),
    "La corrupción y el fraude": ("corrupcion", "Corrupción", "Corruption"),
    "El mal comportamiento de los/as políticos/as": ("comportamiento", "Conducta de políticos", "Politicians' conduct"),
    "Los extremismos": ("extremismos", "Extremismos", "Extremism"),
    "La educación": ("educacion", "Educación", "Education"),
}
LINE = ["vivienda", "economia", "paro", "inmigracion"]
RANK_N = 10
DEF_ES = ("Pregunta: «¿Cuál es, a su juicio, el principal problema que existe actualmente en España? ¿Y el segundo? ¿Y el "
          "tercero?». Respuesta espontánea (sin lista de opciones), recodificada por el CIS en categorías. El porcentaje suma "
          "a cada entrevistado que cita el problema en cualquiera de los tres lugares, así que el total pasa de 100.")
DEF_EN = ("Question: 'In your opinion, what is the main problem currently facing Spain? And the second? And the third?'. "
          "Spontaneous answer (no list of options), coded into categories by the CIS (Spain's public polling institute). The "
          "percentage counts every respondent who names the problem in any of the three places, so the total exceeds 100.")


def _data():
    base = _base("cis-problemas", cis.build)
    s = defaultdict(dict)
    for r in base["rows"]:
        if r["question"] == "espana" and r["problem"] in SHORT:
            s[SHORT[r["problem"]][0]][r["time"]] = r["total"]
    times = sorted(base["studies"])
    assert all(len(s[k]) == len(times) for k in LINE), {k: len(s[k]) for k in LINE}
    return base, s, times


def _time(t: str) -> str:
    """'2024-03' -> '2024.167' (eje numérico)."""
    y, m = int(t[:4]), int(t[5:])
    return str(round(y + (m - 1) / 12, 3)).removesuffix(".0")


def _month(t: str, lang: str) -> str:
    y, m = int(t[:4]), int(t[5:])
    return f"{MONTHS[m - 1]} de {y}" if lang == "es" else f"{MONTHS_EN[m - 1]} {y}"


def _missing(base, times) -> tuple[list[str], list[str]]:
    first, last = times[0], times[-1]
    y, m = int(first[:4]), int(first[5:])
    out = []
    while f"{y}-{m:02d}" <= last:
        t = f"{y}-{m:02d}"
        if m != 8 and t not in base["studies"]:
            out.append(t)
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return [_month(t, "es") for t in out], [_month(t, "en") for t in out]


def problemas_tiempo():
    base, s, times = _data()
    labels = {v[0]: bi(v[1], v[2]) for v in SHORT.values()}
    rows = [{"time": _time(t), "series": k, "value": s[k][t], "month": t} for k in LINE for t in times]
    # Primer problema de cada barómetro, entre todas las categorías del CIS
    allp = defaultdict(dict)
    for r in base["rows"]:
        if r["question"] == "espana":
            allp[r["problem"]][r["time"]] = r["total"]
    top = {t: max(allp, key=lambda p: allp[p].get(t, 0)) for t in times}
    since = next(t for t in times if all(top[u] == "La vivienda" for u in times if u >= t))
    streak = sum(t >= since for t in times)
    y23 = [t for t in times if t < "2024"]
    v23 = round(sum(s["vivienda"][t] for t in y23) / len(y23), 1)
    miss_es, miss_en = _missing(base, times)
    ns = [base["studies"][t]["n"] for t in times]
    n_es = f"entre {min(ns):,} y {max(ns):,}".replace(",", ".")
    n_en = f"between {min(ns):,} and {max(ns):,}"
    return chart(
        id="n06-problemas-tiempo",
        lens="tiempo", theme="elecciones",
        title=bi(f"La vivienda es el problema más citado en los {streak} barómetros del CIS desde {_month(since, 'es')}; "
                 f"en 2023 la mencionaba de media un {es1(v23)} %",
                 f"Housing is the most-cited problem in the {streak} CIS barometers since {_month(since, 'en')}; "
                 f"in 2023 an average of {en1(v23)}% mentioned it"),
        subtitle=bi(f"Porcentaje de entrevistados que citan cada problema entre los tres principales de España, barómetros mensuales, "
                    f"{_month(times[0], 'es')}-{_month(times[-1], 'es')}",
                    f"Share of respondents who name each problem among Spain's three main problems, monthly barometers, "
                    f"{_month(times[0], 'en')}-{_month(times[-1], 'en')}"),
        unit=bi("% de entrevistados", "% of respondents"),
        source=cis.SOURCE,
        notes={"es": ["Respuesta espontánea, hasta tres problemas por entrevistado (ver el texto).",
                      "«Economía»: la categoría del CIS «la crisis económica, los problemas de índole económica».",
                      f"El CIS no hace barómetro en agosto. Faltan además: {', '.join(miss_es)} (sin barómetro ese mes o con "
                      "la tabla publicada en otro formato); la línea une los meses de alrededor.",
                      f"Cada barómetro entrevista a {n_es} personas: diferencias de un mes a otro de uno o dos "
                      "puntos pueden deberse al azar de la muestra."],
               "en": ["Spontaneous answer, up to three problems per respondent (see the text).",
                      "'Economy': the CIS category 'the economic crisis, economic problems'.",
                      f"The CIS does not run a barometer in August. Also missing: {', '.join(miss_en)} (no barometer that month "
                      "or the table published in another format); the line joins the months either side.",
                      f"Each barometer interviews {n_en} people: month-to-month differences of one or two points "
                      "may be down to sampling chance."]},
        rows=rows,
        extra={"dimensions": {"series": {k: labels[k] for k in LINE}},
               "time_labels": {_time(t): bi(_month(t, "es").capitalize(), _month(t, "en")) for t in times}},
    )


def problemas_ranking():
    base, s, times = _data()
    last3 = times[-3:]
    avg = {k: round(sum(v[t] for t in last3) / 3, 1) for k, v in s.items() if all(t in v for t in last3)}
    order = sorted(avg, key=lambda k: -avg[k])[:RANK_N]
    names = {v[0]: (v[1], v[2]) for v in SHORT.values()}
    rows = [{"geo": k, "time": f"{last3[0]}/{last3[-1]}", "value": avg[k]} for k in order]
    a, b = order[0], order[1]
    ratio = avg[a] / avg[b]
    assert a == "vivienda" and ratio > 2, (a, ratio)
    # Todas las categorías del CIS, no solo las del gráfico: el gráfico enseña las diez primeras
    allavg = defaultdict(float)
    for r in base["rows"]:
        if r["question"] == "espana" and r["time"] in last3:
            allavg[r["problem"]] += r["total"] / 3
    top_all = sorted(allavg, key=lambda p: -allavg[p])[:RANK_N]
    assert all(p in SHORT for p in top_all) and [SHORT[p][0] for p in top_all] == order, f"faltan categorías en SHORT: {top_all}"
    assert b == "inmigracion", b
    span_es = f"{_month(last3[0], 'es')}, {_month(last3[1], 'es')} y {_month(last3[2], 'es')}"
    span_en = f"{_month(last3[0], 'en')}, {_month(last3[1], 'en')} and {_month(last3[2], 'en')}"
    return chart(
        id="n06-problemas-ranking",
        lens="tiempo", theme="elecciones",
        title=bi(f"En los tres últimos barómetros, el {es1(avg[a])} % cita la vivienda entre los problemas de España, "
                 f"más del doble que el segundo, la inmigración ({es1(avg[b])} %)",
                 f"In the last three barometers, {en1(avg[a])}% name housing among Spain's problems, more than twice "
                 f"the second, immigration ({en1(avg[b])}%)"),
        subtitle=bi(f"Porcentaje de entrevistados que citan cada problema entre los tres principales de España. Media de los "
                    f"barómetros de {span_es}. Los {RANK_N} más citados",
                    f"Share of respondents who name each problem among Spain's three main problems. Average of the "
                    f"{span_en} barometers. The {RANK_N} most cited"),
        unit=bi("% de entrevistados", "% of respondents"),
        source=cis.SOURCE,
        notes={"es": ["Media simple de los tres barómetros; cada uno pesa lo mismo.",
                      "Nombres abreviados. «Gobierno y partidos»: «el Gobierno y partidos o políticos concretos»; «Política en "
                      "general»: «los problemas políticos en general»; «Conducta de políticos»: «el mal comportamiento de los "
                      "políticos». Son categorías distintas del CIS y no se pueden sumar: un mismo entrevistado puede citar varias."],
               "en": ["Simple average of the three barometers; each one carries the same weight.",
                      "Shortened names. 'Gov. and parties': 'the government and specific parties or politicians'; 'Politics in "
                      "general': 'political problems in general'; 'Politicians' conduct': 'the bad behaviour of politicians'. They "
                      "are separate CIS categories and cannot be added up: the same respondent can name several."]},
        rows=rows,
        geos={k: {**bi(*names[k]), "ccaa": True} for k in order},
    )


BUILDERS = [problemas_tiempo, problemas_ranking]
