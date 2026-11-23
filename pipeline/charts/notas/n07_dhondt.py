"""N07. Cómo se convierten los votos en escaños.

Datos: resultados de las generales de julio de 2023 por provincia (dataset «congreso-202307», Infoelectoral), guardados
en data/base: no se vuelven a descargar. El reparto D'Hondt con un mínimo del 3 % (LOREG, arts. 162 y 163) se recalcula
aquí y se comprueba que reproduce los escaños oficiales de las 52 circunscripciones.
"""

from lib.output import chart

from ..common import bi
from .n05_escanos import SHORT, _lost, _results, _valid, en1, es1

# Grupos de provincias por número de diputados (2023)
GROUPS = [(1, 1), (2, 3), (4, 4), (5, 5), (6, 7), (8, 12), (16, 37)]


def dhondt(votes: dict[str, int], seats: int, valid: int, threshold: float = 3.0) -> dict[str, int]:
    """Reparto D'Hondt: cada candidatura con al menos `threshold` % del voto válido divide sus votos entre 1, 2, 3...
    y los escaños van a los cocientes más altos."""
    ok = {k: v for k, v in votes.items() if 100 * v / valid >= threshold}
    q = sorted(((v / i, v, k) for k, v in ok.items() for i in range(1, seats + 1)), reverse=True)[:seats]
    out: dict[str, int] = {}
    for _, _, k in q:
        out[k] = out.get(k, 0) + 1
    return out


def _provs() -> list[dict]:
    base = _results()
    provs = [p for p in base["provinces"] if p["geo"] != "ES"]
    assert len(provs) == 52 and sum(p["seats"] for p in provs) == 350
    for p in provs:
        assert dhondt(p["votes"], p["seats"], _valid(p)) == p["won"], f"D'Hondt no reproduce {p['name']}"
    return provs


def threshold_changes() -> list[str]:
    """Provincias en las que el mínimo del 3 % cambió algún escaño en 2023."""
    return [p["name"] for p in _provs()
            if dhondt(p["votes"], p["seats"], _valid(p), 0) != p["won"]]


def max_lost(p: dict) -> tuple[float, str]:
    """Mayor porcentaje del voto válido de una candidatura que no obtuvo escaño en la provincia."""
    lost = [(100 * v / _valid(p), k) for k, v in p["votes"].items() if k not in p["won"]]
    return max(lost) if lost else (0.0, "")


def gallagher(groups: list[dict]) -> float:
    """Índice de mínimos cuadrados de Gallagher sobre el conjunto de provincias."""
    V = sum(_valid(p) for p in groups)
    S = sum(p["seats"] for p in groups)
    parties = {k for p in groups for k in p["votes"]}
    return (0.5 * sum((100 * sum(p["votes"].get(k, 0) for p in groups) / V
                       - 100 * sum(p["won"].get(k, 0) for p in groups) / S) ** 2 for k in parties)) ** 0.5


def barrera_real():
    base = _results()
    provs = _provs()
    assert not threshold_changes(), "el 3 % cambió escaños: revisar el texto"
    small = [p for p in provs if 2 <= p["seats"] <= 3]
    big = [p for p in provs if p["seats"] >= 30]
    s_val, s_party = max(max_lost(p) for p in small)
    s_prov = next(p for p in small if max_lost(p) == (s_val, s_party))
    b_val = max(max_lost(p)[0] for p in big)
    rows = []
    for p in provs:
        v, k = max_lost(p)
        rows.append({"geo": p["geo"], "time": "2023", "value": round(v, 1), "list": k, "seats": p["seats"],
                     "min_won": round(min(100 * p["votes"][w] / _valid(p) for w in p["won"]), 1)})
    geos = {p["geo"]: {"es": SHORT.get(p["geo"], (p["name"], p["name"]))[0],
                       "en": SHORT.get(p["geo"], (p["name"], p["name"]))[1], "rank": True} for p in provs}
    return chart(
        id="n07-barrera-real",
        lens="dentro", theme="elecciones",
        title=bi(f"En las provincias que eligen 2 o 3 diputados, candidaturas con hasta el {es1(s_val)} % del voto se "
                 f"quedaron sin escaño; en Madrid y Barcelona, ninguna con más del {es1(b_val)} %",
                 f"In provinces that elect 2 or 3 deputies, lists with up to {en1(s_val)}% of the vote won no seat; in "
                 f"Madrid and Barcelona, none with more than {en1(b_val)}%"),
        subtitle=bi("Porcentaje del voto válido de la candidatura más votada que no obtuvo escaño en cada provincia, "
                    "generales de julio de 2023",
                    "Share of the valid vote of the most-voted list that won no seat in each province, July 2023 general "
                    "election"),
        unit=bi("% del voto válido", "% of valid vote"),
        source=base["source"],
        notes={"es": ["Voto válido: votos a candidaturas más voto en blanco. Votos agrupados por candidatura cabecera "
                      "nacional, como en la nota sobre el coste de un escaño.",
                      "Ceuta y Melilla eligen un solo diputado: la segunda candidatura, con más de un cuarto del voto, "
                      "se queda sin escaño."],
               "en": ["Valid vote: votes for lists plus blank ballots. Votes grouped by national head list, as in the note "
                      "on the cost of a seat.",
                      "Ceuta and Melilla elect a single deputy: the runner-up, with more than a quarter of the vote, wins "
                      "no seat."]},
        rows=rows, geos=geos,
        extra={"small_max": {"province": s_prov["name"], "list": s_party, "share": round(s_val, 1)},
               "big_max": round(b_val, 1), "threshold_changes": 0},
    )


def _glabel(lo: int, hi: int, lang: str) -> str:
    if lo == hi:
        return f"{lo} {'escaño' if lo == 1 else 'escaños'}" if lang == "es" else f"{lo} {'seat' if lo == 1 else 'seats'}"
    if hi - lo == 1:
        return f"{lo} o {hi} escaños" if lang == "es" else f"{lo} or {hi} seats"
    return f"De {lo} a {hi} escaños" if lang == "es" else f"{lo} to {hi} seats"


def desproporcion():
    base = _results()
    provs = _provs()
    nat = next(p for p in base["provinces"] if p["geo"] == "ES")
    rows, geos, vals = [], {}, {}
    for lo, hi in GROUPS:
        g = [p for p in provs if lo <= p["seats"] <= hi]
        key = f"M{lo}-{hi}"
        vals[key] = gallagher(g)
        rows.append({"geo": key, "time": "2023", "value": round(vals[key], 1), "provinces": len(g),
                     "seats": sum(p["seats"] for p in g)})
        geos[key] = {"es": _glabel(lo, hi, "es"), "en": _glabel(lo, hi, "en"), "rank": True}
    g_es = gallagher([nat])
    rows.append({"geo": "ES", "time": "2023", "value": round(g_es, 1), "seats": 350})
    geos["ES"] = {"es": "España", "en": "Spain", "aggregate": True}
    small, big = vals["M2-3"], vals["M16-37"]
    seq = [vals[f"M{lo}-{hi}"] for lo, hi in GROUPS[1:]]
    assert all(a >= b - 0.05 for a, b in zip(seq, seq[1:])), "la desproporción no baja con el tamaño"
    return chart(
        id="n07-desproporcion",
        lens="dentro", theme="elecciones",
        title=bi(f"El reparto se aleja más de los votos cuantos menos diputados elige la provincia: índice de {es1(small)} "
                 f"con 2 o 3 escaños y de {es1(big)} en Madrid, Barcelona y Valencia",
                 f"The allocation strays further from the votes the fewer deputies a province elects: an index of "
                 f"{en1(small)} with 2 or 3 seats and {en1(big)} in Madrid, Barcelona and Valencia"),
        subtitle=bi("Índice de desproporcionalidad de Gallagher por grupos de provincias según los diputados que eligen, "
                    "generales de julio de 2023 (0 = escaños en la misma proporción que los votos)",
                    "Gallagher disproportionality index by groups of provinces according to the deputies they elect, July "
                    "2023 general election (0 = seats in the same proportion as votes)"),
        unit=bi("índice de Gallagher", "Gallagher index"),
        source=base["source"],
        notes={"es": ["Índice de Gallagher: raíz cuadrada de la mitad de la suma de los cuadrados de la diferencia, en "
                      "puntos, entre el porcentaje de votos y el de escaños de cada candidatura, calculado sobre el "
                      "conjunto de provincias de cada grupo.",
                      "El dato de España compara votos y escaños de cada candidatura en todo el país."],
               "en": ["Gallagher index: square root of half the sum of the squared differences, in points, between each "
                      "list's share of votes and of seats, computed over all the provinces in each group.",
                      "The figure for Spain compares each list's votes and seats across the whole country."]},
        rows=rows, geos=geos,
    )


BUILDERS = [barrera_real, desproporcion]
