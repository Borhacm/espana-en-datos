"""Quién gobierna: presidentes autonómicos y del Gobierno de España, con fechas y partido.

Fuente: Wikipedia, «Anexo:Presidencias autonómicas españolas» (CC BY-SA 4.0), contrastada con el
cuadro de gobiernos autonómicos del Senado. El partido es el del presidente: los socios de coalición
van en un archivo aparte, revisado a mano (coaliciones.py).
"""

import re

from lib import geo, sources

PAGE = "Anexo:Presidencias_autonómicas_españolas"
SOURCE = {
    "name": "Wikipedia, Anexo:Presidencias autonómicas españolas",
    "url": "https://es.wikipedia.org/wiki/Anexo:Presidencias_auton%C3%B3micas_espa%C3%B1olas",
    "license": "CC BY-SA 4.0",
    "also": [{"name": "Senado, cuadro de gobiernos autonómicos",
              "url": "https://www.senado.es/web/conocersenado/biblioteca/dossieresareastematicas/detalle/index.html?id=Cuadro_gobiernos_autonomicos"}],
}

# Bandera de cada tabla -> código INE de la comunidad
FLAGS = {
    "Andalucía": "01", "Aragón": "02", "Asturias": "03", "Islas Baleares": "04", "Canarias": "05",
    "Cantabria": "06", "Castilla y León": "07", "Castilla-La Mancha": "08", "Cataluña": "09",
    "Comunidad Valenciana": "10", "Extremadura": "11", "Galicia": "12", "Comunidad de Madrid": "13",
    "Región de Murcia": "14", "Navarra": "15", "País Vasco": "16", "La Rioja": "17", "Ceuta": "18", "Melilla": "19",
}

MONTHS = {m: i for i, m in enumerate(
    ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
     "septiembre", "octubre", "noviembre", "diciembre"], start=1)}
DATE = re.compile(r"(\d{1,2}) de (\w+) de (\d{4})")

# Siglas homogéneas: los federados regionales cuentan como su partido estatal
PARTY = {"PSC": "PSOE", "AP": "PP", "Indep.": "Independiente"}
# Presidentes independientes: cuenta la fuerza que los propuso y con la que gobernaron
INDEPENDENT = {"Quim Torra": "JxCat", "Uxue Barkos": "Geroa Bai"}

# Presidentes del Gobierno de España desde 1977 (mandatos efectivos; los periodos en funciones
# cuentan para el presidente saliente). Fuente: La Moncloa, «Presidentes del Gobierno».
NACIONAL = [
    ("Adolfo Suárez", "UCD", "1976-07-03", "1981-02-26"),
    ("Leopoldo Calvo-Sotelo", "UCD", "1981-02-26", "1982-12-02"),
    ("Felipe González", "PSOE", "1982-12-02", "1996-05-05"),
    ("José María Aznar", "PP", "1996-05-05", "2004-04-17"),
    ("José Luis Rodríguez Zapatero", "PSOE", "2004-04-17", "2011-12-21"),
    ("Mariano Rajoy", "PP", "2011-12-21", "2018-06-02"),
    ("Pedro Sánchez", "PSOE", "2018-06-02", None),
]
NACIONAL_SOURCE = {"name": "La Moncloa, presidentes del Gobierno", "url": "https://www.lamoncloa.gob.es/presidente/presidentes/Paginas/index.aspx"}


def _date(text: str) -> str | None:
    m = DATE.search(text)
    if not m:
        return None
    d, month, y = m.groups()
    return f"{y}-{MONTHS[month.lower()]:02d}-{int(d):02d}"


def _link_text(cell: str) -> str:
    m = re.search(r"\[\[(?:[^]|]*\|)?([^]]+)\]\]", cell)
    return m.group(1).strip() if m else re.sub(r"<[^>]+>|'''?", "", cell).strip()


def _strip_attrs(cell: str) -> str:
    """Quita el prefijo de estilo de una celda: 'bgcolor=#FFE5B4|[[X]]' -> '[[X]]'."""
    m = re.match(r"^\s*(?:[a-z-]+=[^|\[]*\|)", cell)
    return cell[m.end():] if m and "[[" not in cell[: m.end()] else cell


def presidents() -> list[dict]:
    text = sources.wikipedia(PAGE)
    history = text[text.index("== Histórico de presidentes autonómicos =="): text.index("=== Cuadro resumen ===")]
    out = []
    for table in history.split("{|")[1:]:
        flag = re.search(r"\{\{Bandera\|([^}]+)\}\}", table)
        if not flag:
            continue
        code = FLAGS[flag.group(1)]
        prev = None  # filas con rowspan: el segundo mandato hereda nombre y partido
        for row in re.split(r"\n\|-", table)[1:]:
            cells = [_strip_attrs(c[1:]) for c in row.split("\n") if c.startswith("|") and not c.startswith("|}")]
            mandate = next((c for c in cells if DATE.search(c) and "Archivo:" not in c), None)
            name_cell = next((c for c in cells if "<small>" in c and "[[" in c and "Archivo:" not in c and not DATE.search(c)), None)
            if not mandate:
                continue
            if "artículo 155" in mandate:
                # Intervención estatal: gobierna de hecho el Gobierno de España
                dates = [_date(m.group(0)) for m in DATE.finditer(mandate)]
                out.append({"ccaa": code, "president": "Intervención del Gobierno de España (art. 155)",
                            "party_label": "Art. 155", "party": "Art. 155", "start": dates[0], "end": dates[1], "acting": False})
                prev = None
                continue
            if name_cell:
                prev = (_link_text(name_cell), _link_text(cells[-1]), name_cell)
            elif prev is None:
                continue
            name, party, name_cell = prev
            dates = [_date(m.group(0)) for m in DATE.finditer(mandate.split("<br")[0])]
            start = dates[0]
            end = None if "en el cargo" in mandate or len(dates) < 2 else dates[1]
            if end is None and "en el cargo" not in mandate:
                raise ValueError(f"{code}: mandato sin fecha de fin: {mandate[:80]}")
            out.append({
                "ccaa": code,
                "president": name,
                "party_label": party,
                "party": INDEPENDENT.get(name) or PARTY.get(party, party),
                "start": start,
                "end": end,
                "acting": "en funciones" in mandate.lower(),
            })
    return out


def check(rows: list[dict]) -> list[str]:
    """Avisos de continuidad: huecos o solapes de más de 120 días entre mandatos de una comunidad."""
    import datetime as dt

    warnings = []
    for code in geo.CCAA:
        mine = sorted((r for r in rows if r["ccaa"] == code), key=lambda r: r["start"])
        if not mine:
            warnings.append(f"{code} {geo.CCAA[code]}: sin presidentes")
            continue
        if mine[-1]["end"] is not None:
            warnings.append(f"{code} {geo.CCAA[code]}: ningún presidente en el cargo")
        for a, b in zip(mine, mine[1:]):
            gap = (dt.date.fromisoformat(b["start"]) - dt.date.fromisoformat(a["end"])).days
            if abs(gap) > 120:
                warnings.append(f"{code} {geo.CCAA[code]}: {a['president']} -> {b['president']}: {gap} días")
    return warnings


def build() -> dict:
    rows = presidents()
    nacional = [{"ccaa": "ES", "president": n, "party": p, "party_label": p, "start": s, "end": e, "acting": False}
                for n, p, s, e in NACIONAL]
    return {
        "id": "gobiernos",
        "title": "Quién gobierna: presidentes autonómicos y del Gobierno de España",
        "source": SOURCE,
        "also": [NACIONAL_SOURCE],
        "notes": [
            "El color es el partido del presidente o presidenta; no muestra los socios de coalición.",
            "El PSC cuenta como PSOE y Alianza Popular como PP. Al pasar por encima se ve la sigla original.",
            "Los tramos más claros son presidencias en funciones, que se incluyen para que no haya huecos.",
        ],
        "ccaa": geo.CCAA,
        "warnings": check(rows),
        "rows": sorted(nacional + rows, key=lambda r: (r["ccaa"], r["start"])),
    }
