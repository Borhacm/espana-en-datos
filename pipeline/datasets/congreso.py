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
PAGE_LEG = BASE + "/es/opendata/votaciones?p_p_id=votaciones&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&targetLegislatura={leg}"
PAGE = PAGE_LEG.format(leg="XV")
CURRENT = "XV"

# Legislaturas con votaciones en datos abiertos
LEGISLATURES = {
    "X": "X (2011-2015)", "XI": "XI (2016)", "XII": "XII (2016-2019)",
    "XIII": "XIII (2019)", "XIV": "XIV (2019-2023)", "XV": "XV (2023-2026)",
}
SOURCE = {
    "name": "Congreso de los Diputados, datos abiertos de votaciones",
    "url": "https://www.congreso.es/es/opendata/votaciones",
    "license": "Reutilización libre citando la fuente (aviso legal del Congreso)",
}

# Grupo parlamentario (código de los datos) -> nombre corto. El mismo nombre en varias legislaturas permite sumarlas.
GROUPS = {
    "GP": "PP", "GS": "PSOE", "GVOX": "Vox", "GSUMAR": "Sumar", "GR": "ERC", "GER": "ERC", "GJxCAT": "Junts",
    "GEH Bildu": "EH Bildu", "GV": "PNV", "GV (EAJ-PNV)": "PNV", "GMx": "Mixto", "GCs": "Ciudadanos",
    # Grupo de Podemos y sus confluencias: XI Podemos-En Comú Podem-En Marea, XII Unidos Podemos, XIV Unidas Podemos
    "GP-EC-EM": "Unidas Podemos", "GCUP-EC-EM": "Unidas Podemos", "GCUP-EC-GC": "Unidas Podemos",
    "GC-DL": "Democràcia i Llibertat", "GPlu": "Grupo Plural",
    "GC-CiU": "CiU", "GIP": "Izquierda Plural", "GUPyD": "UPyD",
}
# Notas para los grupos que reúnen varios partidos o cambian de nombre
BLOC_NOTES = {
    "Grupo Mixto": "Grupo Mixto: reúne partidos distintos en cada legislatura; su voto es el de la mayoría de sus miembros.",
    "Grupo Plural": "Grupo Plural (XIV): Junts, Más País, Compromís, BNG y otros.",
    "Unidas Podemos": "Unidas Podemos: el grupo de Podemos y sus confluencias en la XI, XII y XIV legislaturas.",
    "Mixto (otros)": "Mixto (otros), XV legislatura: diputados del Grupo Mixto que no son de Podemos, BNG, CC, UPN ni Compromís "
                     "(por ejemplo, quienes dejaron su grupo); su voto es el de la mayoría de ellos.",
    "Podemos": "Podemos (XV): en el grupo de Sumar hasta diciembre de 2023 y después en el Mixto.",
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


def _days(leg: str = CURRENT) -> list[str]:
    # La lista de días cambia cuando hay plenos nuevos: se pide una vez al día (la fecha forma parte de la clave de la
    # caché). Las páginas de cada día y sus zips no cambian, así que salen de la caché y no se vuelven a descargar.
    page = PAGE_LEG.format(leg=leg)
    url = f"{page}&_dia={dt.date.today().isoformat()}" if leg == CURRENT else page
    html = fetch(url, ".html").read_text(encoding="utf-8", errors="ignore")
    days = re.search(r"var diasVotaciones = \[([^\]]*)\]", html).group(1)
    return sorted(d.strip() for d in days.split(",") if d.strip())


def _day_html(day: str, leg: str) -> str:
    d = f"{day[6:8]}/{day[4:6]}/{day[:4]}"
    return fetch(f"{PAGE_LEG.format(leg=leg)}&targetDate={d}", ".html").read_text(encoding="utf-8", errors="ignore")


def _zips(day: str, leg: str = CURRENT) -> list[str]:
    return sorted(set(re.findall(r"/webpublica/opendata/votaciones/[^\"]*?\.zip", _day_html(day, leg))))


def _day_files(day: str, leg: str):
    """JSON de cada votación de un día: del zip de la sesión o, si el zip no existe en el portal (pasa en la X y la XII),
    de los JSON sueltos que enlaza la página del día."""
    html = _day_html(day, leg)
    for z in sorted(set(re.findall(r"/webpublica/opendata/votaciones/[^\"]*?\.zip", html))):
        try:
            zf = zipfile.ZipFile(io.BytesIO(fetch(BASE + z, ".zip").read_bytes()))
        except Exception:
            prefix = z.rsplit("/", 1)[0]
            for j in sorted(set(re.findall(r"/webpublica/opendata/votaciones/[^\"]*?\.json", html))):
                if j.startswith(prefix):
                    try:
                        yield json.loads(fetch(BASE + j, ".json").read_text(encoding="utf-8"))
                    except Exception:
                        continue
            continue
        for name in sorted(n for n in zf.namelist() if n.endswith(".json")):
            yield json.loads(zf.read(name).decode("utf-8"))


def _bloc(v: dict, leg: str = CURRENT) -> str:
    # Al inicio de cada legislatura algún voto figura sin grupo (aún no asignado)
    if not v["grupo"]:
        return "Sin grupo"
    if v["grupo"] not in GROUPS:
        raise ValueError(f"{leg}: grupo desconocido: {v['grupo']}")
    g = GROUPS[v["grupo"]]
    if g == "Mixto":
        # En la legislatura actual el Mixto se separa por partido; en las anteriores, cuenta como grupo
        return MIXTO_PARTY.get(v["diputado"], "Mixto (otros)") if leg == CURRENT else "Grupo Mixto"
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


def kind(title: str, text: str) -> str:
    """Tipo de votación a partir del epígrafe del orden del día."""
    t, x = title.lower(), text.lower()
    if "presupuestos generales del estado" in t:
        return "presupuestos"
    if "decreto" in t or x.startswith("real decreto-ley"):
        return "decreto"
    if any(k in t for k in ("moción", "mocion", "proposiciones no de ley", "proposición no de ley")):
        return "mocion"
    if any(k in t for k in ("iniciativas legislativas", "enmiendas del senado", "proposiciones de ley", "proposición de ley",
                            "proyecto de ley", "proyectos de ley", "lectura única", "convenios internacionales",
                            "reforma del reglamento", "estatuto", "orgánica")):
        return "ley"
    return "otra"


def votes(leg: str = CURRENT) -> tuple[list[dict], dict]:
    out, deputies = [], defaultdict(lambda: {"bloc": None, "votes": 0, "breaks": 0})
    seen_mixto, seen = set(), set()
    for day in _days(leg):
        for d in _day_files(day, leg):
            info, tot = d["informacion"], d["totales"]
            key = (info["sesion"], info["numeroVotacion"])
            if key in seen or tot.get("asentimiento") == "Sí" or not d.get("votaciones"):
                continue
            seen.add(key)
            by_bloc = defaultdict(list)
            for v in d["votaciones"]:
                b = _bloc(v, leg)
                if v["grupo"] == "GMx":
                    seen_mixto.add(v["diputado"])
                by_bloc[b].append(VOTE.get(v["voto"]))
            pos = {b: _position(vs) for b, vs in by_bloc.items() if b != "Sin grupo"}
            # Disciplina: votos de cada diputado distintos de la posición de su grupo (sin contar «No vota»)
            for v in d["votaciones"]:
                b, mine = _bloc(v, leg), VOTE.get(v["voto"])
                dep = deputies[v["diputado"]]
                dep["bloc"] = b
                if mine and pos.get(b):
                    dep["votes"] += 1
                    dep["breaks"] += mine != pos[b]
            title = info.get("titulo", "").strip()
            text = (info.get("textoExpediente") or "").strip()
            out.append({
                "id": f"{info['sesion']}-{info['numeroVotacion']}",
                "date": "-".join(reversed([p.zfill(2) for p in info["fecha"].split("/")])),
                "title": title,
                "text": text,
                "kind": kind(title, text),
                "sub": " ".join(x for x in (info.get("tituloSubGrupo"), info.get("textoSubGrupo")) if x).strip(),
                "yes": tot["afavor"], "no": tot["enContra"], "abst": tot["abstenciones"], "present": tot["presentes"],
                "positions": pos,
            })
    if leg == CURRENT:
        missing = sorted(set(MIXTO_PARTY) - seen_mixto)
        assert not missing, f"diputados de MIXTO_PARTY que no aparecen en el Mixto: {missing}"
    out.sort(key=lambda r: (r["date"], int(r["id"].split("-")[0]), int(r["id"].split("-")[1])))
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


# Orden de los partidos en el explorador: los estatales primero, después el resto por orden alfabético
EXPLORER_ORDER = ["PP", "PSOE", "Vox", "Sumar", "Unidas Podemos", "Podemos", "Ciudadanos", "Izquierda Plural", "UPyD",
                  "ERC", "Junts", "CiU", "Democràcia i Llibertat", "EH Bildu", "PNV", "BNG", "CC", "UPN", "Compromís",
                  "Grupo Plural", "Grupo Mixto", "Mixto (otros)"]
KINDS = {"ley": "Leyes", "presupuestos": "Presupuestos", "decreto": "Decretos-ley",
         "mocion": "Mociones y proposiciones no de ley", "otra": "Otras"}


def build_explorer() -> dict:
    """Todas las legislaturas en formato compacto para el explorador de la web."""
    legs, rows = [], []
    by_leg = {leg: votes(leg)[0] for leg in LEGISLATURES}
    blocs = sorted({b for rs in by_leg.values() for r in rs for b in r["positions"]},
                   key=lambda b: (EXPLORER_ORDER.index(b) if b in EXPLORER_ORDER else 99, b))
    code = {"si": "s", "no": "n", "abst": "a", None: "."}
    for i, (leg, rs) in enumerate(by_leg.items()):
        legs.append({"id": leg, "label": LEGISLATURES[leg], "from": rs[0]["date"], "to": rs[-1]["date"], "n": len(rs)})
        for r in rs:
            rows.append([i, r["date"].replace("-", ""), r["kind"], int(r["yes"] > r["no"]),
                         "".join(code[r["positions"].get(b)] for b in blocs)])
    return {
        "id": "congreso-explorador",
        "title": "Votaciones nominales del Pleno del Congreso, legislaturas X a XV",
        "source": SOURCE,
        "notes": [
            "Cada votación: legislatura, fecha (AAAAMMDD), tipo, aprobada (1) o no (0) por mayoría simple y la posición de cada "
            "partido en el orden de «blocs»: s (sí), n (no), a (abstención), . (sin posición).",
            "Algunas sesiones de la X y la XII no tienen zip en el portal; se leen de los JSON de cada votación.",
        ],
        "legislatures": legs,
        "blocs": blocs,
        "bloc_notes": {b: BLOC_NOTES[b] for b in blocs if b in BLOC_NOTES},
        "types": KINDS,
        "votes": rows,
    }
