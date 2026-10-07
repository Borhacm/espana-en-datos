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

from .common import es_num

THEMES["congreso"] = {"code": "CG", "title": "El Congreso en datos"}

# Orden de los partidos: por votos en las generales de 2023 (los del Grupo Mixto, después)
BLOCS = ["PP", "PSOE", "Vox", "Sumar", "ERC", "Junts", "EH Bildu", "PNV", "Podemos", "BNG", "CC", "UPN"]
DECREE_TITLE = "Convalidación o derogación de Reales Decretos-leyes."

# Votaciones con empate que se repitieron fuera de los datos abiertos: resultado oficial
OUTCOMES = {
    "8/2023": {"result": "convalidado", "note": "Empate a 171 en la primera votación; convalidado en la segunda por 172 a 171.",
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
        title=f"PP y PSOE votaron lo mismo en el {_es(pp_psoe)} % de las votaciones de la legislatura",
        subtitle=f"Porcentaje de votaciones nominales del Pleno en que dos partidos votaron igual "
                 f"({f'{len(rows):,}'.replace(',', '.')} votaciones, del {_fecha(first)} al {_fecha(last)})",
        unit="% de votaciones con el mismo voto",
        source={**congreso.SOURCE, "dataset": "Votaciones nominales del Pleno, XV legislatura"},
        notes=[
            "Voto de un partido: la opción (sí, no o abstención) que eligió la mayoría de sus diputados presentes.",
            "Cuentan las votaciones en las que los dos partidos votaron. Todas pesan igual: una moción pesa lo mismo que una ley.",
            "Podemos formó parte del grupo de Sumar hasta diciembre de 2023: hasta entonces cuenta como Sumar.",
            "BNG, CC, UPN y Podemos están en el Grupo Mixto: se separan por diputado.",
        ],
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
        title=f"El PSOE ha quedado en el lado ganador en el {_es(tot['PSOE'])} % de las votaciones; el PP, en el {_es(tot['PP'])} %",
        subtitle="Porcentaje de votaciones en las que cada partido votó lo mismo que el resultado final, por trimestre",
        unit="% de votaciones",
        source={**congreso.SOURCE, "dataset": "Votaciones nominales del Pleno, XV legislatura"},
        notes=[
            "Gana quien vota sí y la votación sale adelante, o vota no y no sale. Las abstenciones no cuentan.",
            "Resultado por mayoría simple (más síes que noes). Las leyes orgánicas necesitan mayoría absoluta en la votación final; "
            "aquí se tratan igual, así que el dato es aproximado en esas votaciones.",
            "Trimestres con al menos 10 votaciones.",
        ],
        rows=out,
        extra={"quarterly": True, "short_labels": {"PSOE": "PSOE", "PP": "PP"},
               "ref_line": {"value": 50, "label": {"es": "50 %"}}},
    )


# ---------- 3. Los decretos que cayeron ----------

def decretos():
    rows = [v for v in _rows() if v["title"] == DECREE_TITLE and not v["text"].startswith("Tramitación")]
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
        title=f"El Congreso ha tumbado {n_der} decretos-ley del Gobierno esta legislatura",
        subtitle=f"Voto de cada partido en los decretos-ley derogados ({len(derogated)} con votación publicada en los datos abiertos)",
        unit="Voto",
        source={**congreso.SOURCE, "dataset": "Convalidación o derogación de reales decretos-leyes",
                "also": [{"name": f"RDL {d['decree']} (derogado el {d['date']})", "url": d["url"]} for d in LATE_DECREES]},
        notes=[
            f"De {total} decretos-ley votados con datos publicados, {len(derogated)} fueron derogados. "
            f"Se suman {len(LATE_DECREES)} derogados el 2 de octubre de 2026 cuya votación aún no está en los datos abiertos.",
            "Un decreto-ley se convalida si tiene más votos a favor que en contra.",
            OUTCOMES["8/2023"]["note"] + " No figura entre los derogados.",
            "Celda vacía: ese partido no tuvo posición (no votó o sus diputados se dividieron a partes iguales).",
        ],
        rows=out,
        extra={"blocs": BLOCS, "labels": labels, "late": LATE_DECREES},
    )


BUILDERS = [coincidencias, lado_ganador, decretos]
