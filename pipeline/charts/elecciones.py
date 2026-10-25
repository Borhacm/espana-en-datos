"""Especial elecciones generales del 29 de noviembre de 2026 (código EL).

Gráficos construidos a partir de los datasets base (data/base): encuestas, gobiernos y resultados de 2023.
"""

import datetime as dt
import json
import math
import shutil

from datasets import elecciones, encuestas, gobiernos
from lib import geo
from lib.http import fetch
from lib.output import DATA_DIR, THEMES, chart

from .common import bi, dec

THEMES["elecciones"] = {"code": "EL", "title": "Elecciones generales del 29N"}

ELECTION_2023 = "2023-07-23"


def _base(name: str, build):
    """Dataset base ya guardado en data/base (se versiona con el repositorio); si no existe, se construye.

    Así los gráficos no vuelven a descargar fuentes que no cambian (Infoelectoral, por ejemplo, no responde
    desde algunos entornos en la nube). Los datasets base se regeneran con run.py sin --only o con --only <nombre>."""
    path = DATA_DIR / "base" / f"{name}.json"
    return json.loads(path.read_text()) if path.exists() else build()


def _results_2023() -> dict:
    return _base("congreso-202307", lambda: elecciones.build("202307"))
# Partidos con serie propia en el seguimiento; el resto no tiene datos en todas las encuestas
TRACKED = ["PP", "PSOE", "Vox", "Sumar", "Podemos", "SALF"]

# Media de encuestas: núcleo gaussiano centrado. En la última fecha solo hay encuestas anteriores,
# así que el tramo final equivale a una media hacia atrás.
BANDWIDTH_DAYS = 18
WINDOW_DAYS = 45
MIN_POLLSTERS = 3
# Efecto casa: desviación media de cada empresa respecto a la media, encogida hacia cero
HOUSE_MIN_POLLS = 5
HOUSE_SHRINK = 5


def _weight(days_ago: int, sample: int | None) -> float:
    n = min(sample or 1000, 3000)
    return math.exp(-0.5 * (days_ago / BANDWIDTH_DAYS) ** 2) * math.sqrt(n / 1000)


def _usable(polls: list[dict]) -> list[dict]:
    out = []
    for p in polls:
        if p["panel"] or p["partisan"] or p["reestimate"]:
            continue
        out.append({**p, "_d": dt.date.fromisoformat(p["date"])})
    return out


def _average(usable: list[dict], days: list[dt.date], house: dict | None = None) -> list[dict]:
    """Media ponderada por antigüedad y tamaño muestral. Cada empresa reparte su peso entre sus
    encuestas de la ventana, para que las que publican cada semana no dominen la media."""
    house = house or {}
    out = []
    for day in days:
        window = [p for p in usable if abs((day - p["_d"]).days) <= WINDOW_DAYS]
        per_firm: dict[str, int] = {}
        for p in window:
            per_firm[p["pollster"]] = per_firm.get(p["pollster"], 0) + 1
        if len(per_firm) < MIN_POLLSTERS:
            continue
        for party in TRACKED:
            num = den = 0.0
            for p in window:
                if party not in p["values"]:
                    continue
                w = _weight(abs((day - p["_d"]).days), p["sample"]) / per_firm[p["pollster"]]
                v = p["values"][party] - house.get((p["pollster"], party), 0.0)
                num += w * v
                den += w
            if den:
                out.append({"date": day.isoformat(), "party": party, "value": round(num / den, 1),
                            "series": "avg", "n": len(per_firm)})
    return out


def house_effects(usable: list[dict], first: list[dict]) -> dict:
    """Desviación media de cada empresa respecto a la media del día de cada encuesta, encogida
    hacia cero (n / (n + 5)) y centrada para que el conjunto de empresas sume cero."""
    ref = {(r["date"], r["party"]): r["value"] for r in first}
    days = sorted({r["date"] for r in first})
    import bisect

    def avg_at(date: str, party: str):
        i = bisect.bisect_right(days, date) - 1
        return ref.get((days[i], party)) if i >= 0 else None

    resid: dict[tuple, list[float]] = {}
    for p in usable:
        for party, v in p["values"].items():
            if party in TRACKED and (a := avg_at(p["date"], party)) is not None:
                resid.setdefault((p["pollster"], party), []).append(v - a)
    effects = {}
    for key, rs in resid.items():
        if len(rs) >= HOUSE_MIN_POLLS:
            effects[key] = sum(rs) / len(rs) * len(rs) / (len(rs) + HOUSE_SHRINK)
    for party in TRACKED:
        keys = [k for k in effects if k[1] == party]
        if keys:
            mean = sum(effects[k] for k in keys) / len(keys)
            for k in keys:
                effects[k] -= mean
    return effects


def poll_average(polls: list[dict], start: dt.date, end: dt.date, step: int = 7):
    usable = _usable(polls)
    days = []
    day = start
    while day <= end:
        days.append(day)
        day += dt.timedelta(days=step)
    if days[-1] != end:
        days.append(end)
    first = _average(usable, [d for d in (start + dt.timedelta(days=i) for i in range((end - start).days + 1))][::3] + [end])
    house = house_effects(usable, first)
    return _average(usable, days, house), house


def tracker():
    base = encuestas.build()
    polls = base["rows"]
    last = max(dt.date.fromisoformat(p["date"]) for p in polls)
    avg, house = poll_average(polls, dt.date(2023, 9, 1), last)

    rows = []
    for p in polls:
        for party in TRACKED:
            if party in p["values"]:
                rows.append({
                    "date": p["date"], "party": party, "value": p["values"][party], "series": "poll",
                    "pollster": p["pollster"], "commissioner": p["commissioner"], "sample": p["sample"],
                    "kind": "panel" if p["panel"] else "partisan" if p["partisan"] else "reestimate" if p["reestimate"] else "poll",
                    "url": p["url"],
                })
    result = _results_2023()
    nat = next(p for p in result["provinces"] if p["geo"] == "ES")
    valid = sum(nat["votes"].values()) + nat["blank"]
    results_2023 = [{"party": k, "value": round(100 * v / valid, 1)} for k, v in nat["votes"].items() if k in TRACKED]

    latest = {r["party"]: r["value"] for r in avg if r["date"] == avg[-1]["date"]}
    lead = sorted(latest.items(), key=lambda x: -x[1])
    return chart(
        id="el1-encuestas",
        lens="tiempo", theme="elecciones",
        title=bi(f"El {lead[0][0]} lidera la media de encuestas con un {str(lead[0][1]).replace('.', ',')} %, "
                 f"{str(round(lead[0][1] - lead[1][1], 1)).replace('.', ',')} puntos por delante del {lead[1][0]}",
                 f"The {lead[0][0]} leads the poll average with {lead[0][1]}%, "
                 f"{round(lead[0][1] - lead[1][1], 1)} points ahead of the {lead[1][0]}"),
        subtitle=bi("Intención de voto al Congreso, en % sobre voto válido. Cada punto es una encuesta; la línea, la media.",
                    "Voting intention for Congress, as % of valid votes. Each dot is a poll; the line, the average."),
        unit=bi("% del voto válido", "% of valid votes"),
        source={**encuestas.SOURCE, "dataset": "Encuestas recopiladas con su enlace original",
                "also": [{"name": "Resultados de 2023: Ministerio del Interior", "url": elecciones.SOURCE["url"]}]},
        notes={"es": [
            f"Media semanal suavizada: para cada fecha, las encuestas de {WINDOW_DAYS} días antes y después, ponderadas por distancia "
            f"(núcleo gaussiano de {BANDWIDTH_DAYS} días) y por la raíz del tamaño muestral (tope de 3.000 entrevistas). En el último "
            "tramo solo hay encuestas anteriores, así que la media puede moverse cuando lleguen las siguientes. Cada empresa reparte su "
            "peso entre sus encuestas de la ventana, para que las que publican más a menudo no dominen.",
            f"Antes de promediar se corrige el efecto casa: la desviación media de cada empresa respecto a la media (con al menos "
            f"{HOUSE_MIN_POLLS} encuestas), encogida hacia cero y centrada para que el conjunto de empresas no se desplace. "
            "Los puntos muestran siempre el dato publicado, sin corregir.",
            "No entran en la media los paneles online sin muestreo probabilístico (ElectoPanel), las encuestas de partidos ni las "
            "reestimaciones del CIS hechas por otras empresas. Sí aparecen como puntos.",
            "Sumar/FA: Frente Amplio sustituye desde septiembre de 2026 a la alianza Sumar (IU, Movimiento Sumar, Más Madrid y Comuns, "
            "entre otros) y continúa su serie. Incluye también a Compromís–Front Valencià (Compromís, Podemos y EUPV en la Comunidad "
            "Valenciana), igual que Sumar incluía a Compromís en 2023. Por eso, desde ese cambio, Podemos no incluye su voto en la "
            "Comunidad Valenciana. El resultado de 2023 es el de Sumar.",
            "Resultados de 2023: % sobre voto válido (candidaturas + blanco), con voto exterior.",
            "Por ley (LOREG, art. 69.7), las encuestas no se pueden publicar del 24 al 28 de noviembre. Esos días este gráfico se oculta.",
        ], "en": [
            f"Smoothed weekly average: for each date, the polls from {WINDOW_DAYS} days before and after, weighted by distance "
            f"(a {BANDWIDTH_DAYS}-day Gaussian kernel) and by the square root of the sample size (capped at 3,000 interviews). In the final "
            "stretch there are only earlier polls, so the average may move when the next ones arrive. Each pollster splits its "
            "weight across its polls in the window, so those that publish more often do not dominate.",
            f"Before averaging, house effects are corrected: each pollster's average deviation from the average (with at least "
            f"{HOUSE_MIN_POLLS} polls), shrunk towards zero and centred so that the set of pollsters does not shift. "
            "The dots always show the published figure, uncorrected.",
            "Left out of the average: online panels without probability sampling (ElectoPanel), party polls and re-estimates of "
            "CIS surveys made by other companies. They do appear as dots.",
            "Sumar/FA: since September 2026 Frente Amplio replaces the Sumar alliance (IU, Movimiento Sumar, Más Madrid and Comuns, "
            "among others) and continues its series. It also includes Compromís–Front Valencià (Compromís, Podemos and EUPV in the "
            "Valencian Community), just as Sumar included Compromís in 2023. So since that change, Podemos does not include its vote "
            "in the Valencian Community. The 2023 result is Sumar's.",
            "2023 results: % of valid votes (parties + blank), including votes from abroad.",
            "By law (LOREG, art. 69.7), polls cannot be published from 24 to 28 November. On those days this chart is hidden.",
        ]},
        rows=sorted(rows + avg, key=lambda r: (r["series"], r["party"], r["date"])),
        extra={
            "parties": TRACKED,
            "election_2023": ELECTION_2023,
            "results_2023": results_2023,
            "last_poll": last.isoformat(),
            "veda": {"from": "2026-11-24", "to": "2026-11-29T21:00:00+01:00"},
            "house_effects": [{"pollster": k[0], "party": k[1], "value": round(v, 1)} for k, v in sorted(house.items())],
        },
    )


# Traducción de las notas de datasets/gobiernos.py, en el mismo orden
GOV_NOTES_EN = [
    "The colour is the president's party; it does not show coalition partners.",
    "The PSC counts as PSOE and Alianza Popular as PP. Hovering shows the original party.",
    "Lighter stretches are acting presidencies, included so that there are no gaps.",
]


def gobiernos_timeline():
    base = _base("gobiernos", gobiernos.build)
    assert len(base["notes"]) == len(GOV_NOTES_EN), "Han cambiado las notas de gobiernos: actualiza GOV_NOTES_EN"
    rows = [{**r, "value": 1} for r in base["rows"]]
    current = {r["ccaa"]: r["party"] for r in base["rows"] if r["end"] is None}
    pp = sum(1 for c, p in current.items() if p == "PP" and c not in ("18", "19"))
    return chart(
        id="el2-gobiernos",
        lens="dentro", theme="elecciones",
        title=bi(f"El PP gobierna hoy {pp} de las 17 comunidades autónomas", f"The PP now governs {pp} of the 17 regions"),
        subtitle=bi("Partido del presidente o presidenta de cada comunidad desde 1980",
                    "Party of each region's president since 1980"),
        unit=bi("Partido", "Party"),
        source={**gobiernos.SOURCE, "dataset": "Presidencias autonómicas"},
        notes={"es": base["notes"] + [
                   "Cataluña, de octubre de 2017 a mayo de 2018: gobierno intervenido por el Estado (artículo 155).",
               ],
               "en": GOV_NOTES_EN + [
                   "Catalonia, October 2017 to May 2018: self-government suspended by the State (article 155 of the Constitution).",
               ]},
        rows=rows,
        geos={c: bi(geo.ccaa_name(c, "es") if c != "ES" else "Gobierno de España", geo.ccaa_name(c, "en") if c != "ES" else "Government of Spain")
              for c in [*geo.CCAA, "ES"]},
        extra={"today": dt.date.today().isoformat()},
    )


ATLAS = "https://cdn.jsdelivr.net/npm/es-atlas@0.6.0/es/{name}.json"
ATLAS_SOURCE = {"name": "IGN, vía es-atlas (geometrías)", "url": "https://github.com/martgnz/es-atlas"}


def _geometry():
    geo_dir = DATA_DIR / "geo"
    geo_dir.mkdir(parents=True, exist_ok=True)
    for name in ("provinces", "municipalities"):
        target = geo_dir / f"es-{name}.json"
        if not target.exists():  # las geometrías están en el repositorio: solo se descargan si faltan
            shutil.copy(fetch(ATLAS.format(name=name), ".json"), target)


def _miles(n: int) -> str:
    return f"{n:,}".replace(",", ".")


def _thousands(n: int) -> str:
    return f"{n:,}"


def mapa_2023():
    _geometry()
    result = _results_2023()
    rows = []
    for level, items in (("provincia", result["provinces"]), ("municipio", result["municipalities"])):
        for a in items:
            if a["geo"] == "ES" or not a["votes"]:
                continue
            valid = sum(a["votes"].values())
            (first, v1), *rest = a["votes"].items()
            second = rest[0] if rest else (None, 0)
            rows.append({
                "geo": a["geo"], "level": level, "name": a["name"],
                "winner": first, "value": round(100 * v1 / valid, 1),
                "margin": round(100 * (v1 - second[1]) / valid, 1), "second": second[0],
                "turnout": round(100 * a["voters"] / a["census"], 1) if a["census"] else None,
                **({"seats": a["won"]} if level == "provincia" else {}),
            })
    won = {}
    for r in rows:
        if r["level"] == "municipio":
            won[r["winner"]] = won.get(r["winner"], 0) + 1
    top = sorted(won.items(), key=lambda x: -x[1])
    return chart(
        id="el3-mapa-2023",
        lens="dentro", theme="elecciones",
        title=bi(f"En 2023, el {top[0][0]} ganó en {_miles(top[0][1])} municipios y el {top[1][0]} en {_miles(top[1][1])}",
                 f"In 2023, the {top[0][0]} won in {_thousands(top[0][1])} municipalities and the {top[1][0]} in {_thousands(top[1][1])}"),
        subtitle=bi("Partido más votado en las elecciones al Congreso del 23 de julio de 2023",
                    "Party with the most votes in the Congress election of 23 July 2023"),
        unit=bi("% del voto a candidaturas del ganador", "Winner's % of the vote for parties"),
        source={**elecciones.SOURCE, "dataset": "Ficheros MUNI 02202307", "also": [ATLAS_SOURCE]},
        notes={"es": [
                   "La intensidad del color indica el porcentaje del ganador sobre el voto a candidaturas.",
                   "Los municipios no incluyen el voto exterior.",
               ],
               "en": [
                   "The intensity of the colour shows the winner's share of the vote for parties.",
                   "Municipalities do not include votes cast from abroad.",
               ]},
        rows=rows,
        extra={"geometry": {"provincia": "geo/es-provinces.json", "municipio": "geo/es-municipalities.json"}},
    )


BUILDERS = [tracker, gobiernos_timeline, mapa_2023]


# ---------- Simulador de escaños (dataset base, no es un gráfico) ----------

SIM_PARTIES = ["PP", "PSOE", "Vox", "Sumar", "Podemos", "SALF"]
# Partidos que solo se presentan en algunas provincias: el simulador mantiene su voto de 2023
REGIONAL = ["ERC", "Junts", "EH Bildu", "PNV", "BNG", "CC", "UPN"]


def simulador() -> dict:
    from datasets import escanos

    seats = {r["geo"]: r["seats"] for r in _base("escanos-2026", escanos.build)["rows"]}
    result = _results_2023()
    nat = next(p for p in result["provinces"] if p["geo"] == "ES")
    nat_valid = sum(nat["votes"].values()) + nat["blank"]
    provinces = []
    for p in result["provinces"]:
        if p["geo"] == "ES":
            continue
        valid = sum(p["votes"].values()) + p["blank"]
        share = {k: round(100 * v / valid, 3) for k, v in p["votes"].items() if k in SIM_PARTIES + REGIONAL and v}
        provinces.append({"geo": p["geo"], "name": p["name"], "seats": seats[p["geo"]], "seats_2023": p["seats"], "share_2023": share})
    tracker_rows = json.loads((DATA_DIR / "charts" / "el1-encuestas.json").read_text())["rows"]
    avg = [r for r in tracker_rows if r["series"] == "avg"]
    last = max(r["date"] for r in avg)
    return {
        "id": "simulador",
        "title": "Simulador de escaños: datos de partida",
        "source": {"name": "Ministerio del Interior (resultados de 2023) e INE (población para el reparto de 2026)",
                   "url": elecciones.SOURCE["url"]},
        "parties": SIM_PARTIES,
        "regional": REGIONAL,
        "national_2023": {k: round(100 * v / nat_valid, 2) for k, v in nat["votes"].items() if k in SIM_PARTIES + REGIONAL},
        "defaults": {r["party"]: r["value"] for r in avg if r["date"] == last},
        "defaults_date": last,
        "threshold": 3.0,
        "provinces": provinces,
    }
