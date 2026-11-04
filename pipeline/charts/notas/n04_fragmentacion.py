"""N04. Un Congreso cada vez más fragmentado.

Datos: escaños de cada candidatura en las 16 elecciones generales desde 1977 (dataset «generales-escanos», de los
artículos de Wikipedia de cada elección, comprobado con la leyenda de escaños de cada artículo y, en 2023, con
Infoelectoral). Se guarda en data/base y no se vuelve a descargar.
"""

from collections import defaultdict

from datasets import generales
from lib.output import chart

from ..common import bi
from ..elecciones import _base
from ..legislatura import en1, es1
from .n03_participacion import _label, _name, _time

ENP_ES = ("Número efectivo de partidos (índice de Laakso y Taagepera): 1 dividido entre la suma de los cuadrados de la "
          "proporción de escaños de cada candidatura. Vale 2 si dos partidos se reparten los escaños a partes iguales.")
ENP_EN = ("Effective number of parties (Laakso-Taagepera index): 1 divided by the sum of the squared share of seats of each "
          "list. It equals 2 if two parties share the seats equally.")
LISTS_ES = ("Candidaturas como las agrupa la tabla de resultados de cada elección: un partido y sus listas asociadas en una "
            "comunidad cuentan juntos (por ejemplo, PSOE con el PSC) y una coalición cuenta como una sola candidatura.")
LISTS_EN = ("Lists as grouped in the results table of each election: a party and its associated lists in a region count "
            "together (for example, PSOE with the PSC) and a coalition counts as a single list.")


def _data() -> dict[str, list[dict]]:
    base = _base("generales-escanos", generales.build)
    by = defaultdict(list)
    for r in base["rows"]:
        by[r["election"]].append(r)
    assert len(by) == len(generales.PAGES), sorted(by)
    for e, rs in by.items():
        assert sum(r["seats"] for r in rs) == generales.SEATS, e
    return dict(sorted(by.items()))


def _source():
    return _base("generales-escanos", generales.build)["source"]


def enp(rows: list[dict]) -> float:
    return 1 / sum((r["seats"] / generales.SEATS) ** 2 for r in rows)


def top2(rows: list[dict]) -> float:
    s = sorted((r["seats"] for r in rows), reverse=True)
    return 100 * (s[0] + s[1]) / generales.SEATS


def partidos_efectivos():
    by = _data()
    els = list(by)
    vals = {e: round(enp(by[e]), 2) for e in els}
    before = [e for e in els if e < "2015"]
    hi_before = max(vals[e] for e in before)
    last = els[-1]
    since = [e for e in els if e >= "2015"]
    assert all(vals[e] > hi_before for e in since), "la historia del titular no se sostiene"
    rows = [{"time": _time(e), "series": "ES", "value": vals[e], "election": e,
             "lists": len(by[e])} for e in els]
    return chart(
        id="n04-partidos-efectivos",
        lens="tiempo", theme="elecciones",
        title=bi(f"Hasta 2011 el Congreso nunca pasó de {es1(hi_before)} partidos efectivos; desde 2015 no ha bajado de "
                 f"{es1(min(vals[e] for e in since))}",
                 f"Until 2011 Congress never went above {en1(hi_before)} effective parties; since 2015 it has not fallen below "
                 f"{en1(min(vals[e] for e in since))}"),
        subtitle=bi(f"Número efectivo de partidos en el Congreso según sus escaños, {els[0][:4]}-{last[:4]}",
                    f"Effective number of parties in Congress by seats, {els[0][:4]}-{last[:4]}"),
        unit=bi("partidos efectivos", "effective parties"),
        source=_source(),
        notes={"es": [ENP_ES, LISTS_ES], "en": [ENP_EN, LISTS_EN]},
        rows=rows,
        extra={"dimensions": {"series": {"ES": bi("Congreso", "Congress")}},
               "time_labels": {_time(e): _label(e) for e in els}},
    )


def dos_mayores():
    by = _data()
    els = list(by)
    vals = {e: round(top2(by[e]), 1) for e in els}
    peak = max(els, key=lambda e: vals[e])
    low = min(els, key=lambda e: vals[e])
    rows = [{"time": _time(e), "series": "ES", "value": vals[e], "election": e,
             "seats": sum(sorted((r["seats"] for r in by[e]), reverse=True)[:2])} for e in els]
    s_peak = rows[els.index(peak)]["seats"]
    s_low = rows[els.index(low)]["seats"]
    return chart(
        id="n04-dos-mayores",
        lens="tiempo", theme="elecciones",
        title=bi(f"Los dos partidos con más escaños sumaron {s_peak} diputados en {_name(peak, 'es')} y {s_low} en "
                 f"{_name(low, 'es')}",
                 f"The two parties with most seats had {s_peak} deputies between them in {_name(peak, 'en')} and {s_low} in "
                 f"{_name(low, 'en')}"),
        subtitle=bi(f"Escaños de las dos candidaturas con más diputados, % de los 350 del Congreso, {els[0][:4]}-{els[-1][:4]}",
                    f"Seats of the two lists with most deputies, % of the 350 in Congress, {els[0][:4]}-{els[-1][:4]}"),
        unit=bi("% de los escaños", "% of seats"),
        source=_source(),
        notes={"es": ["Las dos candidaturas con más escaños en cada elección: UCD y PSOE en 1977 y 1979; PSOE y AP (Coalición "
                      "Popular en 1986) de 1982 a 1986; PSOE y PP desde 1989.", LISTS_ES],
               "en": ["The two lists with most seats in each election: UCD and PSOE in 1977 and 1979; PSOE and AP (Coalición "
                      "Popular in 1986) from 1982 to 1986; PSOE and PP since 1989.", LISTS_EN]},
        rows=rows,
        extra={"dimensions": {"series": {"ES": bi("Dos mayores", "Two largest")}},
               "time_labels": {_time(e): _label(e) for e in els}},
    )


BUILDERS = [partidos_efectivos, dos_mayores]
