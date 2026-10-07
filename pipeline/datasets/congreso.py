"""Votaciones nominales del Pleno del Congreso en la XV legislatura (desde agosto de 2023).

Fuente: Congreso de los Diputados, datos abiertos de votaciones. La página de cada día con votaciones enlaza un zip
con un JSON por votación (información, totales y el voto de cada diputado con su grupo parlamentario).

Grupos: se usa el grupo parlamentario de cada diputado en cada votación. El Grupo Mixto reúne partidos que votan
distinto, así que sus miembros se separan por partido (MIXTO_PARTY, por nombre del diputado tal como aparece en los
datos). Quien no figura ahí cuenta como «Mixto (otros)».
"""

import datetime as dt
import io
import json
import re
import zipfile
from collections import Counter, defaultdict

from lib.http import fetch

BASE = "https://www.congreso.es"
PAGE = BASE + "/es/opendata/votaciones?p_p_id=votaciones&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&targetLegislatura=XV"
SOURCE = {
    "name": "Congreso de los Diputados, datos abiertos de votaciones",
    "url": "https://www.congreso.es/es/opendata/votaciones",
    "license": "Reutilización libre citando la fuente (aviso legal del Congreso)",
}

# Grupo parlamentario (código de los datos) -> nombre corto
GROUPS = {
    "GP": "PP", "GS": "PSOE", "GVOX": "Vox", "GSUMAR": "Sumar", "GR": "ERC", "GJxCAT": "Junts",
    "GEH Bildu": "EH Bildu", "GV": "PNV", "GV (EAJ-PNV)": "PNV", "GMx": "Mixto",
}

# Diputados del Grupo Mixto por partido. Se comprueba contra los datos: cada nombre tiene que aparecer en el Mixto.
MIXTO_PARTY = {
    "Belarra Urteaga, Ione": "Podemos",
    "Sánchez Serna, Javier": "Podemos",
    "Velarde Gómez, Martina": "Podemos",
    "Santana Perera, Noemí": "Podemos",
    "Rego Candamil, Néstor": "BNG",
    "Valido García, Cristina": "CC",
    "Catalán Higueras, Alberto": "UPN",
    "Micó Micó, Àgueda": "Compromís",
}

VOTE = {"Sí": "si", "No": "no", "Abstención": "abst", "No vota": None}


def _days() -> list[str]:
    # La lista de días cambia cuando hay plenos nuevos: se pide una vez al día (la fecha forma parte de la clave de la
    # caché). Las páginas de cada día y sus zips no cambian, así que salen de la caché y no se vuelven a descargar.
    html = fetch(f"{PAGE}&_dia={dt.date.today().isoformat()}", ".html").read_text(encoding="utf-8", errors="ignore")
    days = re.search(r"var diasVotaciones = \[([^\]]*)\]", html).group(1)
    return sorted(d.strip() for d in days.split(",") if d.strip())


def _zips(day: str) -> list[str]:
    d = f"{day[6:8]}/{day[4:6]}/{day[:4]}"
    html = fetch(f"{PAGE}&targetDate={d}", ".html").read_text(encoding="utf-8", errors="ignore")
    return sorted(set(re.findall(r"/webpublica/opendata/votaciones/[^\"]*?\.zip", html)))


def _bloc(v: dict) -> str:
    # Al inicio de la legislatura algún voto figura sin grupo (aún no asignado)
    if not v["grupo"]:
        return "Sin grupo"
    g = GROUPS.get(v["grupo"], v["grupo"])
    if g == "Mixto":
        return MIXTO_PARTY.get(v["diputado"], "Mixto (otros)")
    return g


def _position(votes: list[str]) -> str | None:
    """Posición de un grupo: la opción más votada por sus miembros presentes (empate: sin posición)."""
    c = Counter(v for v in votes if v)
    if not c:
        return None
    (top, n), *rest = c.most_common()
    if rest and rest[0][1] == n:
        return None
    return top


def votes() -> tuple[list[dict], dict]:
    out, deputies = [], defaultdict(lambda: {"bloc": None, "votes": 0, "breaks": 0})
    seen_mixto = set()
    for day in _days():
        for z in _zips(day):
            zf = zipfile.ZipFile(io.BytesIO(fetch(BASE + z, ".zip").read_bytes()))
            for name in sorted(n for n in zf.namelist() if n.endswith(".json")):
                d = json.loads(zf.read(name).decode("utf-8"))
                info, tot = d["informacion"], d["totales"]
                if tot.get("asentimiento") == "Sí" or not d.get("votaciones"):
                    continue
                by_bloc = defaultdict(list)
                for v in d["votaciones"]:
                    b = _bloc(v)
                    if v["grupo"] and GROUPS.get(v["grupo"]) is None:
                        raise ValueError(f"grupo desconocido: {v['grupo']}")
                    if v["grupo"] == "GMx":
                        seen_mixto.add(v["diputado"])
                    by_bloc[b].append(VOTE.get(v["voto"]))
                pos = {b: _position(vs) for b, vs in by_bloc.items() if b != "Sin grupo"}
                # Disciplina: votos de cada diputado distintos de la posición de su grupo (sin contar «No vota»)
                for v in d["votaciones"]:
                    b, mine = _bloc(v), VOTE.get(v["voto"])
                    dep = deputies[v["diputado"]]
                    dep["bloc"] = b
                    if mine and pos.get(b):
                        dep["votes"] += 1
                        dep["breaks"] += mine != pos[b]
                out.append({
                    "id": f"{info['sesion']}-{info['numeroVotacion']}",
                    "date": "-".join(reversed([p.zfill(2) for p in info["fecha"].split("/")])),
                    "title": info.get("titulo", "").strip(),
                    "text": (info.get("textoExpediente") or "").strip(),
                    "sub": " ".join(x for x in (info.get("tituloSubGrupo"), info.get("textoSubGrupo")) if x).strip(),
                    "yes": tot["afavor"], "no": tot["enContra"], "abst": tot["abstenciones"], "present": tot["presentes"],
                    "positions": pos,
                })
    missing = sorted(set(MIXTO_PARTY) - seen_mixto)
    assert not missing, f"diputados de MIXTO_PARTY que no aparecen en el Mixto: {missing}"
    return out, deputies


def build() -> dict:
    rows, deputies = votes()
    return {
        "id": "congreso-xv",
        "title": "Votaciones nominales del Pleno del Congreso, XV legislatura",
        "source": SOURCE,
        "notes": [
            "Una fila por votación nominal (no se incluyen las de asentimiento).",
            "Posición de cada grupo: la opción más votada por sus diputados presentes; si hay empate, sin posición.",
            "El Grupo Mixto se separa por partido (Podemos, BNG, CC, UPN); el resto de sus miembros, «Mixto (otros)».",
        ],
        "deputies": {k: v for k, v in sorted(deputies.items())},
        "rows": rows,
    }
