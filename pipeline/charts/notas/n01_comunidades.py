"""N01. Quién gobierna dónde y qué se juega cada comunidad el 29N.

Datos: escaños de 2026 por provincia (datasets/escanos.py, contrastado con el Real Decreto 806/2026), presidentes
autonómicos en el cargo (datasets/gobiernos.py) y escaños de 2023 (datasets/elecciones.py). Se suman las provincias
de cada comunidad.
"""

from collections import Counter

from datasets import elecciones, escanos, gobiernos
from lib import geo
from lib.output import chart

from ..common import bi


SEATS_SOURCE = {**escanos.SOURCE, "dataset": "Cifras oficiales de población a 1 de enero de 2025",
                "also": [{"name": "BOE, Real Decreto 806/2026 de convocatoria (diputados por circunscripción)",
                          "url": "https://www.boe.es/buscar/doc.php?id=BOE-A-2026-20742"}]}


# Nombres cortos: el ranking corta las etiquetas de más de 14 caracteres en móvil
SHORT = {"07": "C. y León", "08": "C.-La Mancha", "10": "C. Valenciana"}
SHORT_EN = {"04": "Balearic Is.", "05": "Canary Is.", "07": "Castile-León", "08": "C.-La Mancha", "10": "Valencian C."}


def _geos(codes) -> dict:
    return {c: {"es": "España" if c == "ES" else SHORT.get(c, geo.CCAA[c]),
                "en": "Spain" if c == "ES" else SHORT_EN.get(c, geo.CCAA_EN[c]), "ccaa": c != "ES", "aggregate": c == "ES"}
            for c in sorted(set(codes))}


def _thousands(n: int) -> str:
    return f"{n:,}"


def _miles(n: int) -> str:
    return f"{n:,}".replace(",", ".")


def _by_ccaa():
    """Escaños de 2026, de 2023 y población por comunidad."""
    base = escanos.build()
    seats, pop = Counter(), Counter()
    for r in base["rows"]:
        c = geo.PROVINCIAS[r["geo"]][1]
        seats[c] += r["seats"]
        pop[c] += r["population"]
    seats_2023 = Counter()
    for p in elecciones.build("202307")["provinces"]:
        if p["geo"] != "ES":
            seats_2023[geo.PROVINCIAS[p["geo"]][1]] += sum(p["won"].values())
    assert sum(seats.values()) == sum(seats_2023.values()) == 350
    return seats, seats_2023, pop, base["population_year"]


def _governing():
    return {r["ccaa"]: r for r in gobiernos.build()["rows"] if r["end"] is None and r["ccaa"] != "ES"}


def escanos_ccaa():
    seats, seats_2023, _, _ = _by_ccaa()
    gov = _governing()
    rows = [{"geo": c, "time": "2026", "value": v, "seats_2023": seats_2023[c], "party": gov[c]["party"]}
            for c, v in seats.items()]
    top = sorted(rows, key=lambda r: -r["value"])[:3]
    top_sum = sum(r["value"] for r in top)
    names = [geo.CCAA[r["geo"]] for r in top]
    names_en = [geo.CCAA_EN[r["geo"]] for r in top]
    changed = [f"{geo.CCAA[c]} pasa de {seats_2023[c]} a {seats[c]}" for c in sorted(seats) if seats[c] != seats_2023[c]]
    changed_en = [f"{geo.CCAA_EN[c]} goes from {seats_2023[c]} to {seats[c]}" for c in sorted(seats) if seats[c] != seats_2023[c]]
    prov_2023 = {p["geo"]: sum(p["won"].values()) for p in elecciones.build("202307")["provinces"] if p["geo"] != "ES"}
    prov = [f"{r['name']} ({prov_2023[r['geo']]} a {r['seats']})" for r in escanos.build()["rows"] if r["seats"] != prov_2023[r["geo"]]]
    prov_en = [f"{r['name']} ({prov_2023[r['geo']]} to {r['seats']})" for r in escanos.build()["rows"] if r["seats"] != prov_2023[r["geo"]]]
    return chart(
        id="n01-escanos-ccaa",
        lens="dentro", theme="elecciones",
        title=bi(f"{names[0]}, {names[1]} y {names[2]} eligen {top_sum} de los 350 diputados",
                 f"{names_en[0]}, {names_en[1]} and {names_en[2]} elect {top_sum} of the 350 deputies"),
        subtitle=bi("Diputados que elige cada comunidad el 29 de noviembre de 2026", "Deputies each region elects on 29 November 2026"),
        unit=bi("Diputados", "Deputies"),
        source={**SEATS_SOURCE, "also": SEATS_SOURCE["also"] + [{"name": gobiernos.SOURCE["name"], "url": gobiernos.SOURCE["url"]}]},
        notes={"es": [
            "Los escaños se reparten por provincias (LOREG, art. 162): 2 fijos por provincia, 1 en Ceuta y en Melilla, y los 248 restantes según la población.",
            "Cambios respecto a 2023: " + "; ".join(changed) + ". Por provincias: " + ", ".join(prov) + ".",
            "En los datos, party es el partido del presidente o presidenta autonómico hoy (el PSC cuenta como PSOE), no de sus socios de coalición.",
        ], "en": [
            "Seats are allocated by province (LOREG, art. 162): 2 fixed per province, 1 in Ceuta and in Melilla, and the remaining 248 by population.",
            "Changes from 2023: " + "; ".join(changed_en) + ". By province: " + ", ".join(prov_en) + ".",
            "In the data, party is the party of the current regional president (the PSC counts as PSOE), not of their coalition partners.",
        ]},
        rows=sorted(rows, key=lambda r: r["geo"]),
        geos=_geos(seats),
    )


def habitantes_escano():
    seats, _, pop, year = _by_ccaa()
    rows = [{"geo": c, "time": "2026", "value": round(pop[c] / seats[c]), "population": pop[c], "seats": seats[c]} for c in seats]
    rows.append({"geo": "ES", "time": "2026", "value": round(sum(pop.values()) / 350), "population": sum(pop.values()), "seats": 350})
    peninsula = [r for r in rows if r["geo"] not in ("ES", "18", "19")]
    lo = min(peninsula, key=lambda r: r["value"])
    hi = max(peninsula, key=lambda r: r["value"])
    return chart(
        id="n01-habitantes-escano",
        lens="dentro", theme="elecciones",
        title=bi(f"Cada diputado de {geo.CCAA[lo['geo']]} representa a {_miles(lo['value'])} habitantes; "
                 f"cada uno de {geo.CCAA[hi['geo']]}, a {_miles(hi['value'])}",
                 f"Each deputy from {geo.CCAA_EN[lo['geo']]} represents {_thousands(lo['value'])} people; "
                 f"each one from {geo.CCAA_EN[hi['geo']]}, {_thousands(hi['value'])}"),
        subtitle=bi(f"Habitantes por diputado en cada comunidad, con la población oficial a 1 de enero de {year} y el reparto de 2026",
                    f"Inhabitants per deputy in each region, with the official population on 1 January {year} and the 2026 allocation"),
        unit=bi("Habitantes por diputado", "Inhabitants per deputy"),
        source=SEATS_SOURCE,
        notes={"es": [
            "Población total empadronada, de todas las edades y nacionalidades, no censo electoral.",
            "La diferencia viene de la ley electoral: cada provincia tiene 2 escaños fijos, así que las provincias poco pobladas eligen "
            "más diputados por habitante. Por provincias, el extremo es Soria y el contrario, Madrid.",
            "Ceuta y Melilla eligen un diputado cada una.",
        ], "en": [
            "Total registered population, of all ages and nationalities, not the electoral roll.",
            "The difference comes from the electoral law: each province has 2 fixed seats, so sparsely populated provinces elect "
            "more deputies per inhabitant. By province, the extreme is Soria and the opposite, Madrid.",
            "Ceuta and Melilla elect one deputy each.",
        ]},
        rows=sorted(rows, key=lambda r: r["geo"]),
        geos=_geos(r["geo"] for r in rows),
    )


BUILDERS = [escanos_ccaa, habitantes_escano]
