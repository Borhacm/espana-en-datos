"""N05. Cuánto cuesta un escaño en cada provincia.

Datos: resultados de las generales de julio de 2023 por provincia (dataset «congreso-202307», Infoelectoral), guardados
en data/base: no se vuelven a descargar. Los habitantes por escaño de 2026 ya están en la nota n01.
"""

from datasets import elecciones
from lib.output import chart

from ..common import bi
from ..elecciones import _base

# El ranking corta las etiquetas largas en móvil
SHORT = {"38": ("S.C. Tenerife", "S.C. Tenerife"), "07": ("Baleares", "Balearic Is.")}

GROUPS = [(2, 3), (10, 99)]


def es0(v: float) -> str:
    return f"{round(v):,}".replace(",", ".")


def en0(v: float) -> str:
    return f"{round(v):,}"


def es1(v: float) -> str:
    return f"{v:.1f}".replace(".", ",")


def en1(v: float) -> str:
    return f"{v:.1f}"


def _results():
    return _base("congreso-202307", lambda: elecciones.build("202307"))


def _valid(p: dict) -> int:
    return sum(p["votes"].values()) + p["blank"]


def _lost(p: dict) -> int:
    """Votos a candidaturas que no obtuvieron escaño en esa provincia."""
    return sum(v for k, v in p["votes"].items() if k not in p["won"])


def group_share(provs: list[dict], lo: int, hi: int) -> tuple[int, float]:
    g = [p for p in provs if lo <= p["seats"] <= hi]
    return len(g), 100 * sum(_lost(p) for p in g) / sum(_valid(p) for p in g)


def votos_sin_escano():
    base = _results()
    provs = [p for p in base["provinces"] if p["geo"] != "ES"]
    nat = next(p for p in base["provinces"] if p["geo"] == "ES")
    assert len(provs) == 52 and sum(p["seats"] for p in provs) == 350
    (n_s, small), (n_b, big) = (group_share(provs, lo, hi) for lo, hi in GROUPS)
    rows = [{"geo": p["geo"], "time": "2023", "value": round(100 * _lost(p) / _valid(p), 1), "seats": p["seats"],
             "lost": _lost(p), "valid": _valid(p)} for p in provs]
    lost_es = sum(_lost(p) for p in provs)
    rows.append({"geo": "ES", "time": "2023", "value": round(100 * lost_es / _valid(nat), 1), "seats": 350, "lost": lost_es,
                 "valid": _valid(nat)})
    geos = {p["geo"]: {"es": SHORT.get(p["geo"], (p["name"], p["name"]))[0],
                       "en": SHORT.get(p["geo"], (p["name"], p["name"]))[1], "rank": True} for p in provs}
    geos["ES"] = {"es": "España", "en": "Spain", "aggregate": True}
    lo, hi = GROUPS[0]
    return chart(
        id="n05-votos-sin-escano",
        lens="dentro", theme="elecciones",
        title=bi(f"En las provincias que eligen {lo} o {hi} diputados, el {es1(small)} % del voto fue a candidaturas sin "
                 f"escaño; en las que eligen {GROUPS[1][0]} o más, el {es1(big)} %",
                 f"In provinces that elect {lo} or {hi} deputies, {en1(small)}% of the vote went to lists that won no seat; "
                 f"in those that elect {GROUPS[1][0]} or more, {en1(big)}%"),
        subtitle=bi("Votos a candidaturas que no obtuvieron escaño en la provincia, % del voto válido, generales de julio "
                    "de 2023",
                    "Votes for lists that won no seat in the province, % of the valid vote, July 2023 general election"),
        unit=bi("% del voto válido", "% of valid vote"),
        source=base["source"],
        notes={"es": ["El voto válido incluye el voto en blanco, que nunca da escaño pero no se cuenta aquí como voto sin "
                      "escaño. Incluye el voto exterior (CERA).",
                      "Ceuta y Melilla eligen un solo diputado: todo el voto que no va al ganador se queda sin escaño."],
               "en": ["The valid vote includes blank ballots, which never win a seat but are not counted here as votes "
                      "without a seat. It includes the vote from abroad (CERA).",
                      "Ceuta and Melilla elect a single deputy: every vote not cast for the winner is left without a seat."]},
        rows=rows, geos=geos,
        extra={"groups": {f"{lo}-{hi}": {"provinces": n_s, "share": round(small, 1)},
                          f"{GROUPS[1][0]}+": {"provinces": n_b, "share": round(big, 1)}}},
    )


def votos_escano_partido():
    base = _results()
    nat = next(p for p in base["provinces"] if p["geo"] == "ES")
    assert sum(nat["won"].values()) == 350
    vals = {k: nat["votes"][k] / s for k, s in nat["won"].items()}
    big4 = sorted(nat["won"], key=lambda k: -nat["won"][k])[:4]
    two, next2 = big4[:2], big4[2:]
    assert max(vals[k] for k in two) < min(vals[k] for k in next2), "la historia del titular no se sostiene"
    cap = (int(max(vals[k] for k in two)) // 5000 + 1) * 5000   # 65.000
    floor = int(min(vals[k] for k in next2)) // 10000 * 10000    # 90.000
    rows = [{"geo": k, "time": "2023", "value": round(v), "votes": nat["votes"][k], "seats": nat["won"][k]} for k, v in vals.items()]
    geos = {k: {"es": k, "en": k, "rank": True, "party": True} for k in vals}
    return chart(
        id="n05-votos-escano",
        lens="dentro", theme="elecciones",
        title=bi(f"En 2023 el {two[0]} y el {two[1]} lograron un escaño por menos de {es0(cap)} votos; {next2[0]} y "
                 f"{next2[1]} necesitaron más de {es0(floor)}",
                 f"In 2023 the {two[0]} and the {two[1]} won a seat for fewer than {en0(cap)} votes; {next2[0]} and "
                 f"{next2[1]} needed more than {en0(floor)}"),
        subtitle=bi("Votos por escaño obtenido de cada candidatura con diputados en las generales de julio de 2023, "
                    "en toda España",
                    "Votes per seat won by each list with deputies at the July 2023 general election, across Spain"),
        unit=bi("votos por escaño", "votes per seat"),
        source=base["source"],
        notes={"es": ["Votos de la candidatura en todas las provincias divididos entre los escaños que obtuvo. Los votos "
                      "se agrupan por la candidatura cabecera nacional (por ejemplo, el PSC cuenta como PSOE).",
                      "Los escaños se reparten provincia a provincia con la regla D'Hondt y un mínimo del 3 % del voto "
                      "válido de la provincia."],
               "en": ["Votes for the list in every province divided by the seats it won. Votes are grouped by the national "
                      "head list (for example, the PSC counts as PSOE).",
                      "Seats are allocated province by province with the D'Hondt rule and a minimum of 3% of the valid "
                      "vote in the province."]},
        rows=rows, geos=geos,
    )


BUILDERS = [votos_sin_escano, votos_escano_partido]
