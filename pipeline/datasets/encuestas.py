"""Encuestas de intención de voto al Congreso publicadas desde las generales del 23 de julio de 2023.

Fuente: Wikipedia, «Opinion polling for the 2026 Spanish general election» (CC BY-SA 4.0), que
recopila cada encuesta con su referencia original. Cada fila conserva el enlace a la publicación.
"""

import datetime as dt
import re

from lib import sources

PAGE = "Opinion_polling_for_the_2026_Spanish_general_election"
SOURCE = {
    "name": "Wikipedia, Opinion polling for the 2026 Spanish general election",
    "url": "https://en.wikipedia.org/wiki/Opinion_polling_for_the_2026_Spanish_general_election",
    "license": "CC BY-SA 4.0",
}

MONTHS = {m: i for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}

# Paneles online sin muestreo probabilístico ni ficha técnica completa: se publican, pero no entran en la media
PANELS = ("Electomanía", "ElectoPanel")

# Encuestas encargadas o hechas por un partido
PARTIES_AS_POLLSTERS = {"Sumar", "PSOE", "PP", "Vox", "Podemos"}

# Nombres de columna de Wikipedia -> siglas que usamos.
# Frente Amplio (FA) sustituye a la alianza Sumar desde septiembre de 2026 (IU, Movimiento Sumar, Más Madrid y Comuns, entre
# otros): sigue la misma serie, con la clave «Sumar», para que la media no empiece de cero con dos encuestas. Compromís–Front
# Valencià (FV), con Compromís, Podemos y EUPV en la Comunidad Valenciana, va aparte. Ver la nota en build().
PARTY_ALIASES = {"CCa": "CC", "Aliança.cat": "AC", "Adelante Andalucía (2021)": "AA", "FA": "Sumar"}


def _clean(cell: str) -> str:
    cell = re.sub(r"<ref[^>]*/>|<ref[^>]*>.*?</ref>", "", cell, flags=re.S)
    cell = re.sub(r"\{\{Party shading/[^}]*\}\}\s*\|", "", cell)
    cell = re.sub(r"^\s*(?:style|colspan|rowspan|class)=[^|]*\|", "", cell)
    return cell.strip()


def _refs(cell: str) -> list[str]:
    return re.findall(r"\|\s*url\s*=\s*([^|}\s]+)", cell)


def _parties(header: str) -> list[str]:
    out = []
    for line in header.split("\n"):
        if not line.startswith("!") or "rowspan" in line:
            continue
        m = re.search(r"\[\[([^\]]+)\]\]", line)
        if not m:
            continue
        parts = m.group(1).split("|")
        name = parts[-1] if not parts[-1].startswith("link=") else parts[-1][5:]
        if name.endswith("px"):
            name = next(p[5:] for p in parts if p.startswith("link="))
        out.append(PARTY_ALIASES.get(name, name))
    return out


def _fieldwork_end(text: str, year: int) -> str | None:
    """'2–3 Oct' -> fecha del último día; '28 Sep–3 Oct' -> 3 Oct; '28 Dec 2025–2 Jan' -> 2 Jan."""
    last = re.split(r"[–-]", text)[-1].strip()
    m = re.match(r"(\d{1,2}) (\w{3})(?: (\d{4}))?", last)
    if not m:
        return None
    d, mon, y = m.groups()
    return dt.date(int(y or year), MONTHS[mon], int(d)).isoformat()


def _value(cell: str) -> tuple[float | None, int | None]:
    cell = _clean(cell)
    pct = re.match(r"'*\s*(\d+(?:\.\d+)?)", cell)
    seats = re.search(r"text=(\d+)(?:[/–-](\d+))?\}\}", cell)
    seat = None
    if seats:
        lo, hi = seats.groups()
        seat = (int(lo) + int(hi)) / 2 if hi else int(lo)
    return (float(pct.group(1)) if pct else None), seat


def polls() -> list[dict]:
    text = sources.wikipedia(PAGE, lang="en")
    estimates = text[text.index("====Voting intention estimates===="): text.index("====Voting preferences====")]
    out = []
    # Secciones por año; desde octubre de 2026, «2026 (after Broad Front)» y «2026 (before Broad Front)»
    for section in re.split(r"\n=====(\d{4})[^=\n]*=====\n", estimates)[1:]:
        if re.fullmatch(r"\d{4}", section):
            year = int(section)
            continue
        table = section[section.index("{|"):]
        head, _, body = table.partition("\n|-\n|")
        parties = _parties(head)
        width = 4 + len(parties)
        # Celdas con rowspan (Wikipedia escribe una sola vez la fecha y la muestra que comparten, por ejemplo, el CIS y
        # una reestimación de sus datos): se arrastran a las filas siguientes. Sin esto se perdían esas filas.
        carry: dict[int, list] = {}
        for row in ("|" + body).split("\n|-"):
            raw = [c for c in re.split(r"\n\|(?!\})", "\n" + row.strip()) if c.strip()]
            cells, k = [], 0
            for col in range(width + 1):
                if col in carry and carry[col][0] > 0:
                    carry[col][0] -= 1
                    cells.append(carry[col][1])
                    continue
                if k >= len(raw):
                    break
                cell = raw[k]
                k += 1
                m = re.match(r"\s*[^|\[]*?rowspan=\"?(\d+)", cell)
                if m and int(m.group(1)) > 1:
                    carry[col] = [int(m.group(1)) - 1, cell]
                cells.append(cell)
            if len(cells) < width:
                continue
            firm_raw = cells[0]
            firm = re.sub(r"\[\[(?:[^]|]*\|)?([^]]+)\]\]", r"\1", _clean(firm_raw)).strip()
            if "election" in firm.lower():
                continue  # fila de resultados electorales, no es una encuesta
            end = _fieldwork_end(_clean(cells[1]), year)
            if not end:
                continue
            sample = re.sub(r"[^\d]", "", _clean(cells[2]))
            values = {}
            seats = {}
            for party, cell in zip(parties, cells[4: 4 + len(parties)]):
                v, s = _value(cell)
                if v is not None:
                    values[party] = v
                if s is not None:
                    seats[party] = s
            if len(values) < 3:
                continue
            # Reestimaciones de los microdatos del CIS hechas por otras empresas: «CIS {{smaller|(Logoslab)}}»
            alt = re.search(r"\{\{smaller\|\(([^)]+)\)\}\}", firm)
            firm = re.sub(r"\{\{[^}]*\}\}", "", firm).strip()
            pollster, _, commissioner = firm.partition("/")
            out.append({
                "pollster": pollster.strip(),
                "commissioner": commissioner.strip() or None,
                "fieldwork": _clean(cells[1]),
                "date": end,
                "sample": int(sample) if sample else None,
                "panel": any(p in firm_raw for p in PANELS),
                # Misma muestra que el CIS, otra estimación: no cuenta como encuesta independiente
                "reestimate": alt.group(1) if alt else None,
                "partisan": pollster.strip() in PARTIES_AS_POLLSTERS,
                "url": (_refs(firm_raw) or [None])[0],
                "values": values,
                "seats": seats or None,
            })
    return out


def _dedupe(rows: list[dict]) -> list[dict]:
    """Una misma encuesta publicada con varios escenarios (por ejemplo, con y sin un partido) aparece varias veces con el
    mismo enlace: se queda la primera, que es el escenario principal."""
    seen, out = set(), []
    for r in rows:
        key = (r["pollster"], r["commissioner"], r["date"], r["reestimate"], r["url"])
        if r["url"] and key in seen:
            continue
        seen.add(key)
        out.append(r)
    return out


def build() -> dict:
    rows = sorted(_dedupe(polls()), key=lambda r: (r["date"], r["pollster"]))
    return {
        "id": "encuestas",
        "title": "Encuestas de intención de voto al Congreso desde julio de 2023",
        "source": SOURCE,
        "notes": [
            "Porcentaje sobre voto válido estimado por cada empresa. Escaños, cuando la empresa los publica (si da un rango, se usa el punto medio).",
            "La fecha es el último día del trabajo de campo.",
            "panel = true: panel online sin muestreo probabilístico. Se muestra, pero no entra en la media.",
            "reestimate: otra empresa reestima los microdatos de un barómetro del CIS. No cuenta como encuesta independiente.",
            "partisan = true: encuesta de un partido. No entra en la media.",
            "Sumar: desde las encuestas posteriores a su creación (septiembre de 2026), la columna es la de Frente Amplio, la alianza "
            "que sustituye a Sumar. No es exactamente el mismo espacio: en la Comunidad Valenciana, Compromís concurre con Podemos y "
            "EUPV en Compromís–Front Valencià (FV), que tiene su propia clave. Por eso, desde ese cambio, Sumar/FA y Podemos no "
            "incluyen el voto de esa candidatura.",
        ],
        "rows": rows,
    }
