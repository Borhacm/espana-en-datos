"""El Congreso en datos (código CG): cómo han votado los partidos en la XV legislatura.

Datos: datasets/congreso.py (votaciones nominales del Pleno). El resultado de cada votación se calcula por mayoría
simple (más síes que noes); los empates y las votaciones que no están en los datos abiertos se corrigen con
fuentes oficiales en OUTCOMES y LATE_DECREES.
"""

import json
import re
from collections import defaultdict

from datasets import congreso
from lib.output import BASE_DIR, THEMES, chart

from .common import bi, es_num

THEMES["congreso"] = {"code": "CG", "title": "El Congreso en datos"}

# Orden de los partidos: por votos en las generales de 2023 (los del Grupo Mixto, después)
BLOCS = ["PP", "PSOE", "Vox", "Sumar", "ERC", "Junts", "EH Bildu", "PNV", "Podemos", "BNG", "CC", "UPN"]
DECREE_TITLE = "Convalidación o derogación de Reales Decretos-leyes."

# Votaciones con empate que se repitieron fuera de los datos abiertos: resultado oficial
OUTCOMES = {  # ver también congreso.DECREE_OUTCOMES (todas las legislaturas)
    "8/2023": {"result": "convalidado", "note": "Empate a 171 en la primera votación; convalidado en la segunda por 172 a 171.",
               "note_en": "RDL 8/2023: tied at 171 in the first vote; validated in the second by 172 to 171.",
               "url": "https://www.mpr.gob.es/prencom/notas/Paginas/2024/100124-aprobados-decretos-leyes-prorroga-medidas.aspx"},
}
# Decretos derogados cuya votación todavía no está en los datos abiertos
LATE_DECREES = [
    {"decree": "26/2026", "date": "2026-10-02", "text": "Real Decreto-ley 26/2026, de 29 de septiembre, de medidas urgentes para la protección de la función social de la vivienda",
     "url": "https://www.boe.es/buscar/doc.php?id=BOE-A-2026-20526"},
    {"decree": "27/2026", "date": "2026-10-02", "text": "Real Decreto-ley 27/2026 (contratos de alquiler: prórrogas e indemnizaciones)",
     "url": "https://www.ocu.org/fincas-y-casas/gestion/alquiler/analisis/2026/10/derogados-los-decretos-de-alquileres"},
]


def _rows():
    """Lee el dataset base ya generado (uv run run.py --only congreso-xv); si no existe, lo construye."""
    path = BASE_DIR / "congreso-xv.json"
    return json.loads(path.read_text())["rows"] if path.exists() else congreso.build()["rows"]


def _passed(v: dict) -> bool:
    return v["yes"] > v["no"]


MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def _fecha(iso: str) -> str:
    y, m, d = iso.split("-")
    return f"{int(d)} de {MESES[int(m) - 1]} de {y}"


def _es(x: float) -> str:
    return es_num(x)


MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def _date_en(iso: str) -> str:
    y, m, d = iso.split("-")
    return f"{int(d)} {MONTHS[int(m) - 1]} {y}"


# ---------- 1. Matriz de coincidencias ----------

def coincidencias():
    rows = _rows()
    out = []
    pair = {}
    for a in BLOCS:
        for b in BLOCS:
            both = [v for v in rows if v["positions"].get(a) and v["positions"].get(b)]
            if not both:
                continue
            same = sum(v["positions"][a] == v["positions"][b] for v in both)
            pct = round(100 * same / len(both), 1)
            out.append({"row": a, "col": b, "value": pct, "n": len(both)})
            pair[(a, b)] = pct
    # Titular: la pareja que más coincide y el apoyo del PSOE con PP frente a sus socios de investidura
    pairs = sorted(((v, a, b) for (a, b), v in pair.items() if a < b), reverse=True)
    pp_psoe = pair[("PP", "PSOE")]
    first = rows[0]["date"]
    last = rows[-1]["date"]
    return chart(
        id="cg1-coincidencias",
        lens="tiempo", theme="congreso",
        title=bi(f"PP y PSOE votaron lo mismo en el {_es(pp_psoe)} % de las votaciones de la legislatura",
                 f"PP and PSOE voted the same way in {_es(pp_psoe)}% of the votes in this parliament"),
        subtitle=bi(f"Porcentaje de votaciones nominales del Pleno en que dos partidos votaron igual "
                    f"({f'{len(rows):,}'.replace(',', '.')} votaciones, del {_fecha(first)} al {_fecha(last)})",
                    f"Share of roll-call votes in the plenary in which two parties voted the same way "
                    f"({len(rows):,} votes, from {_date_en(first)} to {_date_en(last)})"),
        unit=bi("% de votaciones con el mismo voto", "% of votes with the same vote"),
        source={**congreso.SOURCE, "dataset": "Votaciones nominales del Pleno, XV legislatura"},
        notes={"es": [
            "Voto de un partido: la opción (sí, no o abstención) que eligió la mayoría de sus diputados presentes.",
            "Cuentan las votaciones en las que los dos partidos votaron. Todas pesan igual: una moción pesa lo mismo que una ley.",
            "Podemos formó parte del grupo de Sumar hasta diciembre de 2023: hasta entonces cuenta como Sumar.",
            "BNG, CC, UPN y Podemos están en el Grupo Mixto: se separan por diputado.",
        ], "en": [
            "A party's vote: the option (yes, no or abstention) chosen by the majority of its deputies present.",
            "Only votes in which both parties voted count. They all carry the same weight: a motion weighs the same as a law.",
            "Podemos was part of the Sumar group until December 2023: until then it counts as Sumar.",
            "BNG, CC, UPN and Podemos sit in the Mixed Group: they are split by deputy.",
        ]},
        rows=out,
        extra={"blocs": BLOCS, "most": [{"a": a, "b": b, "value": v} for v, a, b in pairs[:3]]},
    )


# ---------- 2. Quién gana las votaciones ----------

def lado_ganador():
    rows = _rows()
    by_q = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    for v in rows:
        y, m = int(v["date"][:4]), int(v["date"][5:7])
        q = y + (m - 1) // 3 / 4
        for party in ("PSOE", "PP"):
            p = v["positions"].get(party)
            if p not in ("si", "no"):
                continue  # abstención: ni gana ni pierde
            won = (p == "si") == _passed(v)
            by_q[q][party][0] += won
            by_q[q][party][1] += 1
    out = []
    for q in sorted(by_q):
        for party, (w, n) in by_q[q].items():
            if n >= 10:
                out.append({"time": q, "series": party, "value": round(100 * w / n, 1), "n": n})
    # Titular: legislatura completa
    tot = {}
    for party in ("PSOE", "PP"):
        w = sum(by_q[q][party][0] for q in by_q)
        n = sum(by_q[q][party][1] for q in by_q)
        tot[party] = round(100 * w / n, 1)
    return chart(
        id="cg2-lado-ganador",
        lens="tiempo", theme="congreso",
        title=bi(f"El PSOE ha quedado en el lado ganador en el {_es(tot['PSOE'])} % de las votaciones; el PP, en el {_es(tot['PP'])} %",
                 f"The PSOE has been on the winning side in {_es(tot['PSOE'])}% of the votes; the PP, in {_es(tot['PP'])}%"),
        subtitle=bi("Porcentaje de votaciones en las que cada partido votó lo mismo que el resultado final, por trimestre",
                    "Share of votes in which each party voted the same way as the final result, by quarter"),
        unit=bi("% de votaciones", "% of votes"),
        source={**congreso.SOURCE, "dataset": "Votaciones nominales del Pleno, XV legislatura"},
        notes={"es": [
            "Gana quien vota sí y la votación sale adelante, o vota no y no sale. Las abstenciones no cuentan.",
            "Resultado por mayoría simple (más síes que noes). Las leyes orgánicas necesitan mayoría absoluta en la votación final; "
            "aquí se tratan igual, así que el dato es aproximado en esas votaciones.",
            "Trimestres con al menos 10 votaciones.",
        ], "en": [
            "A party wins if it votes yes and the motion passes, or votes no and it fails. Abstentions do not count.",
            "Outcome by simple majority (more yes than no votes). Organic laws need an absolute majority in the final vote; "
            "here they are treated the same, so the figure is approximate for those votes.",
            "Quarters with at least 10 votes.",
        ]},
        rows=out,
        extra={"quarterly": True, "short_labels": {"PSOE": bi("PSOE", "PSOE"), "PP": bi("PP", "PP")},
               "ref_line": {"value": 50, "label": bi("50 %", "50%")}},
    )


# ---------- 3. Los decretos que cayeron ----------

def decretos():
    rows = [v for v in _rows() if v["title"] == DECREE_TITLE and re.match(r"Real Decreto-[Ll]ey", v["text"])]
    out, total, derogated = [], 0, []
    for v in rows:
        m = re.match(r"Real Decreto-ley (\d+/\d{4})", v["text"])
        num = m.group(1) if m else v["id"]
        total += 1
        fix = OUTCOMES.get(num)
        result = fix["result"] if fix else ("convalidado" if _passed(v) else "derogado")
        if result != "derogado":
            continue
        derogated.append(num)
        for b in BLOCS:
            pos = v["positions"].get(b)
            if pos:
                out.append({"row": num, "col": b, "value": {"si": 1, "abst": 0, "no": -1}[pos], "vote": pos,
                            "date": v["date"], "yes": v["yes"], "no": v["no"]})
    labels = {}
    for v in rows:
        m = re.match(r"Real Decreto-ley (\d+/\d{4}), de [^,]+, (.*)", v["text"])
        if m and m.group(1) in derogated:
            labels[m.group(1)] = m.group(2)[:140]
    n_der = len(derogated) + len(LATE_DECREES)
    return chart(
        id="cg3-decretos-derogados",
        lens="tiempo", theme="congreso",
        title=bi(f"El Congreso ha tumbado {n_der} decretos-ley del Gobierno esta legislatura",
                 f"Congress has struck down {n_der} government decree-laws in this parliament"),
        subtitle=bi(f"Voto de cada partido en los decretos-ley derogados ({len(derogated)} con votación publicada en los datos abiertos)",
                    f"Each party's vote on the decree-laws struck down ({len(derogated)} with the vote published in the open data)"),
        unit=bi("Voto", "Vote"),
        source={**congreso.SOURCE, "dataset": "Convalidación o derogación de reales decretos-leyes",
                "also": [{"name": f"RDL {d['decree']} (derogado el {d['date']})", "url": d["url"]} for d in LATE_DECREES]},
        notes={"es": [
            f"De {total} decretos-ley votados con datos publicados, {len(derogated)} fueron derogados. "
            f"Se suman {len(LATE_DECREES)} derogados el 2 de octubre de 2026 cuya votación aún no está en los datos abiertos.",
            "Un decreto-ley se convalida si tiene más votos a favor que en contra.",
            OUTCOMES["8/2023"]["note"] + " No figura entre los derogados.",
            "Celda vacía: ese partido no tuvo posición (no votó o sus diputados se dividieron a partes iguales).",
        ], "en": [
            f"Of {total} decree-laws voted on with published data, {len(derogated)} were struck down. "
            f"Added to them are {len(LATE_DECREES)} struck down on 2 October 2026 whose vote is not yet in the open data.",
            "A decree-law is validated if it has more votes in favour than against.",
            OUTCOMES["8/2023"]["note_en"] + " It is not among those struck down.",
            "Empty cell: that party had no position (it did not vote or its deputies split evenly).",
        ]},
        rows=out,
        extra={"blocs": BLOCS, "labels": labels, "late": LATE_DECREES},
    )


BUILDERS = [coincidencias, lado_ganador, decretos]
