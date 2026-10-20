"""AN01. Quince años en el Congreso: cómo han votado los partidos de la X a la XV legislatura.

Datos: data/base/congreso-explorador.json (datasets/congreso.py, build_explorer) y los presidentes del Gobierno de
datasets/gobiernos.py (qué partido gobernaba en la fecha de cada votación). Las votaciones de Presupuestos (miles de
enmiendas en algunos años) se excluyen para que no pesen más que todo lo demás.
"""

import json
from collections import defaultdict

from datasets import congreso, gobiernos
from lib.output import BASE_DIR, chart

from ..common import bi, es_num

SOURCE = {**congreso.SOURCE, "dataset": "Votaciones nominales del Pleno, legislaturas X a XV"}
MIN_VOTES = 50
# Decretos derogados después de la última votación publicada (ver charts/congreso.py, LATE_DECREES)
LATE_DEROGATED = {"XV": 2}


def _data():
    return json.loads((BASE_DIR / "congreso-explorador.json").read_text())


def _gov_party(date: str) -> str:
    """Partido del presidente del Gobierno en una fecha AAAAMMDD."""
    d = f"{date[:4]}-{date[4:6]}-{date[6:]}"
    for name, party, start, end in gobiernos.NACIONAL:
        if start <= d < (end or "2099-12-31"):
            return party
    raise ValueError(date)


def _votes(d):
    """Votaciones sin Presupuestos, con la posición de cada partido como diccionario."""
    blocs = d["blocs"]
    out = []
    for leg, date, kind, passed, pos in d["votes"]:
        if kind == "presupuestos":
            continue
        out.append({"leg": d["legislatures"][leg]["id"], "date": date, "year": int(date[:4]), "passed": passed,
                    "pos": {blocs[j]: c for j, c in enumerate(pos) if c != "."}})
    return out


def coincidencia_pp_psoe():
    votes = _votes(_data())
    acc = defaultdict(lambda: [0, 0])
    for v in votes:
        a, b = v["pos"].get("PP"), v["pos"].get("PSOE")
        if a and b:
            acc[v["year"]][0] += a == b
            acc[v["year"]][1] += 1
    rows = [{"time": str(y), "series": "pp-psoe", "value": round(100 * s / n, 1), "n": n}
            for y, (s, n) in sorted(acc.items()) if n >= MIN_VOTES]
    lo = min(rows, key=lambda r: r["value"])
    hi = max(rows, key=lambda r: r["value"])
    return chart(
        id="an01-pp-psoe",
        lens="tiempo", theme="congreso",
        title=bi(f"PP y PSOE han votado lo mismo entre el {es_num(lo['value'])} % ({lo['time']}) y el {es_num(hi['value'])} % "
                 f"({hi['time']}) de las votaciones de cada año",
                 f"PP and PSOE have voted the same way in between {es_num(lo['value'])}% ({lo['time']}) and {es_num(hi['value'])}% "
                 f"({hi['time']}) of each year's votes"),
        subtitle=bi("Porcentaje de votaciones nominales del Pleno en que PP y PSOE votaron igual, por año (sin Presupuestos)",
                    "Share of roll-call votes in the plenary in which PP and PSOE voted the same way, by year (excluding budgets)"),
        unit=bi("% de votaciones", "% of votes"),
        source=SOURCE,
        notes={"es": [
            "Voto de un partido: la opción que eligió la mayoría de sus diputados presentes.",
            "Sin las votaciones de Presupuestos Generales, que son miles de enmiendas en algunos años.",
            f"Años con al menos {MIN_VOTES} votaciones. 2016 y 2019 tuvieron legislaturas breves y elecciones repetidas.",
        ], "en": [
            "A party's vote: the option chosen by the majority of its deputies present.",
            "Excluding votes on the General State Budget, which run to thousands of amendments in some years.",
            f"Years with at least {MIN_VOTES} votes. 2016 and 2019 had short parliaments and repeat elections.",
        ]},
        rows=rows,
        extra={"dimensions": {"series": {"pp-psoe": bi("PP y PSOE", "PP and PSOE")}}, "short_labels": {"pp-psoe": bi("PP y PSOE", "PP and PSOE")}},
    )


def gobierno_gana():
    votes = _votes(_data())
    acc = defaultdict(lambda: [0, 0])
    for v in votes:
        g = _gov_party(v["date"])
        p = v["pos"].get(g)
        if p not in ("s", "n"):
            continue
        acc[(g, v["year"])][0] += (p == "s") == bool(v["passed"])
        acc[(g, v["year"])][1] += 1
    rows = [{"time": str(y), "series": g, "value": round(100 * w / n, 1), "n": n}
            for (g, y), (w, n) in sorted(acc.items()) if n >= MIN_VOTES]
    psoe = [r for r in rows if r["series"] == "PSOE"]
    last = psoe[-1]
    peak = max(psoe, key=lambda r: r["value"])
    pp_full = all(r["value"] == 100 for r in rows if r["series"] == "PP" and r["time"] <= "2015")
    return chart(
        id="an01-gobierno-gana",
        lens="tiempo", theme="congreso",
        title=bi((f"Con mayoría absoluta, el PP ganó todas las votaciones de 2012 a 2015; " if pp_full else "")
                 + f"el PSOE ha pasado del {es_num(peak['value'])} % en {peak['time']} al {es_num(last['value'])} % en {last['time']}",
                 (f"With an absolute majority, the PP won every vote from 2012 to 2015; " if pp_full else "")
                 + f"the PSOE has gone from {es_num(peak['value'])}% in {peak['time']} to {es_num(last['value'])}% in {last['time']}"),
        subtitle=bi("Porcentaje de votaciones en las que el partido del presidente del Gobierno votó lo mismo que el resultado final, por año",
                    "Share of votes in which the prime minister's party voted the same way as the final result, by year"),
        unit=bi("% de votaciones", "% of votes"),
        source={**SOURCE, "also": [{"name": "Presidentes del Gobierno (La Moncloa)", "url": gobiernos.NACIONAL_SOURCE["url"]}]},
        notes={"es": [
            "Gana quien vota sí y la votación sale adelante, o vota no y no sale. Las abstenciones no cuentan.",
            "Partido del Gobierno en la fecha de cada votación: PP hasta el 1 de junio de 2018 (moción de censura) y PSOE desde entonces. "
            "En 2018 hay dos puntos, uno por partido.",
            "Resultado por mayoría simple; las leyes orgánicas necesitan mayoría absoluta en la votación final, así que el dato es aproximado en esas votaciones.",
            f"Sin Presupuestos. Años con al menos {MIN_VOTES} votaciones de cada partido.",
        ], "en": [
            "A party wins if it votes yes and the motion passes, or votes no and it fails. Abstentions do not count.",
            "Party in government on the date of each vote: PP until 1 June 2018 (motion of no confidence) and PSOE since then. "
            "In 2018 there are two points, one per party.",
            "Outcome by simple majority; organic laws need an absolute majority in the final vote, so the figure is approximate for those votes.",
            f"Excluding budgets. Years with at least {MIN_VOTES} votes for each party.",
        ]},
        rows=rows,
        extra={"short_labels": {"PP": bi("PP en el Gobierno", "PP in government"), "PSOE": bi("PSOE en el Gobierno", "PSOE in government")}},
    )


def decretos_por_legislatura():
    d = _data()
    rows, total = [], 0
    for leg in d["legislatures"]:
        if not leg["decrees"]:
            continue
        der = sum(x["result"] == "derogado" for x in leg["decrees"]) + LATE_DEROGATED.get(leg["id"], 0)
        total += der
        rows.append({"geo": leg["id"], "time": leg["label"], "value": der, "voted": len(leg["decrees"]) + LATE_DEROGATED.get(leg["id"], 0)})
    xv = next(r for r in rows if r["geo"] == "XV")
    return chart(
        id="an01-decretos",
        lens="tiempo", theme="congreso",
        title=bi(f"De los {total} decretos-ley que el Congreso ha derogado desde 2011, {xv['value']} son de esta legislatura",
                 f"Of the {total} decree-laws Congress has struck down since 2011, {xv['value']} are from this parliament"),
        subtitle=bi("Reales decretos-leyes derogados por el Congreso en cada legislatura",
                    "Royal decree-laws struck down by Congress in each parliament"),
        unit=bi("Decretos-ley derogados", "Decree-laws struck down"),
        source=SOURCE,
        notes={"es": [
            "Un decreto-ley se convalida si tiene más votos a favor que en contra. Los empates repetidos fuera de los datos abiertos se "
            "corrigen con fuentes oficiales (RDL 14/2021 y 8/2023, convalidados).",
            "XV: incluye los RDL 26 y 27/2026, derogados el 2 de octubre de 2026, cuya votación aún no está en los datos abiertos.",
            "Decretos-ley votados: " + "; ".join(f"{r['geo']}: {r['voted']}" for r in rows) + ".",
        ], "en": [
            "A decree-law is validated if it has more votes in favour than against. Ties repeated outside the open data are "
            "corrected with official sources (RDL 14/2021 and 8/2023, validated).",
            "XV: includes RDL 26 and 27/2026, struck down on 2 October 2026, whose vote is not yet in the open data.",
            "Decree-laws voted on: " + "; ".join(f"{r['geo']}: {r['voted']}" for r in rows) + ".",
        ]},
        rows=rows,
        geos={r["geo"]: {**bi(*[next(l["label"] for l in d["legislatures"] if l["id"] == r["geo"])] * 2), "ccaa": True} for r in rows},
    )


def socios():
    d = _data()
    votes = _votes(d)
    # Periodos de Gobierno con suficientes votaciones: legislatura y partido del presidente
    periods = defaultdict(list)
    for v in votes:
        periods[(v["leg"], _gov_party(v["date"]))].append(v)
    order = [(leg["id"], g) for leg in d["legislatures"] for g in ("PP", "PSOE") if len(periods.get((leg["id"], g), [])) >= 300]
    labels = {}
    for leg, g in order:
        vs = periods[(leg, g)]
        y0, y1 = vs[0]["date"][:4], vs[-1]["date"][:4]
        labels[(leg, g)] = f"{leg} · {g} ({y0}-{y1})" if y0 != y1 else f"{leg} · {g} ({y0})"
    # Todas las columnas, también PP y PSOE: cada Gobierno frente al principal partido de la oposición.
    # Solo se deja vacía la celda del propio partido del Gobierno.
    cols = list(d["blocs"])
    rows = []
    for key in order:
        g = key[1]
        for b in cols:
            if b == g:
                continue
            both = [v for v in periods[key] if v["pos"].get(g) and v["pos"].get(b)]
            if len(both) >= 100:
                rows.append({"row": labels[key], "col": b, "value": round(100 * sum(v["pos"][g] == v["pos"][b] for v in both) / len(both), 1),
                             "n": len(both)})
    present = [b for b in cols if any(r["col"] == b for r in rows)]
    return chart(
        id="an01-socios",
        lens="tiempo", theme="congreso",
        title=bi("Con quién ha votado cada Gobierno", "Who each government has voted with"),
        subtitle=bi("Porcentaje de votaciones en que cada partido votó igual que el partido del Gobierno, por legislatura (sin Presupuestos)",
                    "Share of votes in which each party voted the same way as the governing party, by parliament (excluding budgets)"),
        unit=bi("% de votaciones", "% of votes"),
        source=SOURCE,
        notes={"es": [
            "Fila: legislatura y partido del presidente del Gobierno. Columna: el resto de partidos, incluido el principal de la oposición.",
            "Solo celdas con al menos 100 votaciones comparadas; los partidos que no estaban en el Congreso quedan vacíos.",
            "Grupo Mixto y Grupo Plural reúnen partidos distintos: su voto es el de la mayoría de sus miembros.",
        ], "en": [
            "Row: parliament and the prime minister's party. Column: the other parties, including the main opposition party.",
            "Only cells with at least 100 votes compared; parties that were not in Congress are left empty.",
            "Grupo Mixto (Mixed Group) and Grupo Plural bring together different parties: their vote is that of the majority of their members.",
        ]},
        rows=rows,
        extra={"blocs": present, "row_keys": [labels[k] for k in order]},
    )


BUILDERS = [coincidencia_pp_psoe, gobierno_gana, decretos_por_legislatura, socios]
