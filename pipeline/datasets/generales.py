"""Escaños de cada candidatura en las elecciones al Congreso desde 1977.

Fuente: Wikipedia en español, artículo de cada elección general («Elecciones generales de España de <año>»,
CC BY-SA 4.0), tabla de resultados del Congreso. Infoelectoral, la fuente oficial, no responde desde los
entornos en la nube, así que este dataset se guarda en data/base y no se vuelve a descargar.

Comprobaciones al construirlo:
- los escaños de cada elección suman 350;
- coinciden, uno a uno, con la leyenda del diagrama de escaños de la ficha del mismo artículo;
- los de 2023 coinciden con los resultados oficiales de Infoelectoral (data/base/congreso-202307.json).

Las candidaturas se toman como las agrupa la tabla: un partido y sus listas asociadas en una comunidad
cuentan juntos (por ejemplo, PSOE con el PSC), y una coalición cuenta como una sola candidatura.
"""

import json
import re
import urllib.parse
from collections import Counter

from lib import sources
from lib.http import RAW_DIR  # noqa: F401  (la caché la gestiona sources.wikipedia)
from lib.output import DATA_DIR

# Elección (año-mes) -> título del artículo
PAGES = {
    "1977-06": "1977", "1979-03": "1979", "1982-10": "1982", "1986-06": "1986", "1989-10": "1989",
    "1993-06": "1993", "1996-03": "1996", "2000-03": "2000", "2004-03": "2004", "2008-03": "2008",
    "2011-11": "2011", "2015-12": "2015", "2016-06": "2016", "2019-04": "abril de 2019",
    "2019-11": "noviembre de 2019", "2023-07": "2023",
}
SEATS = 350

SOURCE = {
    "name": "Wikipedia, artículos de cada elección general al Congreso",
    "dataset": "Tabla de resultados del Congreso de los Diputados, 1977-2023",
    "url": "https://es.wikipedia.org/wiki/Elecciones_generales_de_Espa%C3%B1a",
    "license": "CC BY-SA 4.0",
    "also": [{"name": "Ministerio del Interior, Infoelectoral",
              "url": "https://infoelectoral.interior.gob.es/opencms/es/elecciones-celebradas/area-de-descargas/",
              "license": "Reutilización libre citando la fuente (Ley 37/2007)"}],
}


def page(election: str) -> str:
    return f"Elecciones generales de España de {PAGES[election]}"


def url(election: str) -> str:
    return "https://es.wikipedia.org/wiki/" + urllib.parse.quote(page(election).replace(" ", "_"))


# --- Lectura del wikitexto -------------------------------------------------------------------------

def _strip_templates(s: str) -> str:
    prev = None
    while prev != s:
        prev, s = s, re.sub(r"\{\{[^{}]*\}\}", "", s)
    return s


def _clean(s: str) -> str:
    s = re.sub(r"\{\{(?i:nowrap)\|([^{}]*)\}\}", r"\1", s.strip())
    if s.startswith("{{Renglóndoble|") and s.endswith("}}"):
        s = _split_top(s[len("{{Renglóndoble|"):-2], "|")[0]
    s = re.sub(r"<ref[^>]*/>", "", s)
    s = re.sub(r"<ref[^>]*>.*?</ref>", "", s, flags=re.S)
    s = re.sub(r"<sup>.*?</sup>", "", s, flags=re.S)
    s = re.sub(r"\[\[(?:Archivo|Imagen|File|Image):[^\]]*\]\]", "", s)
    s = _strip_templates(s)
    s = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", s)
    s = re.sub(r"'''?", "", s)
    s = re.sub(r"<[^>]+>", "", s)
    return s.replace("&nbsp;", " ").strip()


_ATTR = re.compile(r"^\s*((?:[\w\-]+\s*=\s*(?:\"[^\"]*\"|'[^']*'|[^\s|]+)\s*)+)\|(?!\|)")


def _split_cell(c: str) -> tuple[int, str]:
    m = _ATTR.match(c)
    attrs, body = (m.group(1), c[m.end():]) if m else ("", c)
    cs = re.search(r"colspan\s*=\s*\"?(\d+)", attrs)
    return (int(cs.group(1)) if cs else 1), body


def _split_top(s: str, sep: str = "||") -> list[str]:
    """Separa celdas por '||' fuera de plantillas {{...}} y enlaces [[...]]."""
    out, depth, cur, i = [], 0, "", 0
    while i < len(s):
        if s.startswith("{{", i) or s.startswith("[[", i):
            depth += 1
            cur += s[i:i + 2]
            i += 2
        elif (s.startswith("}}", i) or s.startswith("]]", i)) and depth:
            depth -= 1
            cur += s[i:i + 2]
            i += 2
        elif depth == 0 and s.startswith(sep, i):
            out.append(cur)
            cur = ""
            i += len(sep)
        else:
            cur += s[i]
            i += 1
    out.append(cur)
    return out


def _tables(t: str) -> list[str]:
    """Tablas wiki ({| ... |}) de primer nivel; solo cuentan las marcas al principio de línea."""
    out, i = [], 0
    while True:
        j = t.find("{|", i)
        if j < 0:
            return out
        depth, k = 0, j
        while k < len(t):
            at_line = k == 0 or t[k - 1] == "\n"
            if at_line and t.startswith("{|", k):
                depth += 1
                k += 2
            elif at_line and t.startswith("|}", k):
                depth -= 1
                k += 2
                if depth == 0:
                    break
            else:
                k += 1
        out.append(t[j:k])
        i = k


def _rows(tab: str) -> list[list[tuple[str, str]]]:
    rows = [[]]
    for line in tab.split("\n")[1:]:
        if line.startswith("|-"):
            rows.append([])
        elif line.startswith("|}"):
            break
        elif line.startswith("|+"):
            continue
        elif line.startswith("!"):
            rows[-1] += [("h", c) for c in line[1:].split("!!")]
        elif line.startswith("|"):
            rows[-1] += [("d", c) for c in _split_top(line[1:])]
        elif rows[-1]:
            k, c = rows[-1][-1]
            rows[-1][-1] = (k, c + "\n" + line)
    return [r for r in rows if r]


def _expand(row):
    out = []
    for k, c in row:
        n, body = _split_cell(c)
        out += [(k, body)] * n
    return out


def results_table(text: str) -> list[tuple[str, int]]:
    """(candidatura, escaños) de la primera tabla con columnas de votos y de escaños que reparte los 350 escaños."""
    for tab in _tables(text):
        rows = _rows(tab)
        for hi, r in enumerate(rows[:4]):
            e = _expand(r)
            heads = [_clean(b) for _, b in e]
            if not any(k == "h" for k, _ in e):
                continue
            seat_cols = [i for i, h in enumerate(heads) if re.match(r"(Escaños|Diputados)$", h)]
            name_cols = [i for i, h in enumerate(heads) if re.search(r"Lista|Partido|Candidatura", h)]
            if not seat_cols or not name_cols or not any(h.startswith(("Votos", "Sufragios")) for h in heads):
                continue
            si, ni = seat_cols[0], name_cols[-1]
            out = []
            for r2 in rows[hi + 1:]:
                e2 = _expand(r2)
                # Las filas con menos celdas que la cabecera son desgloses de una candidatura (celdas con rowspan)
                if len(e2) < len(e) or all(k == "h" for k, _ in e2):
                    continue
                name, seat = _clean(e2[ni][1]), _clean(e2[si][1])
                if re.match(r"(?i)(total|votos|censo|en blanco|blancos|nulos|abstenc|participaci)", name):
                    break
                m = re.match(r"^(\d+)", seat.replace(" ", ""))
                if m and not re.match(r"(?i)otros", name):
                    out.append((name, int(m.group(1))))
            if sum(s for _, s in out) == SEATS:
                return out
            break
    raise ValueError("no se encuentra la tabla de resultados del Congreso")


def legend(text: str) -> list[int]:
    """Escaños de la leyenda del diagrama del Congreso en la ficha del artículo."""
    i = text.find("leyenda1")
    j = text.find("diagrama2", i)
    seg = text[i:j if j > 0 else i + 5000]
    return sorted((int(m) for m in re.findall(r"texto2\s*=\s*(\d+)", seg)), reverse=True)


def _official_2023() -> list[int]:
    d = json.loads((DATA_DIR / "base" / "congreso-202307.json").read_text())
    won = Counter()
    for p in d["provinces"]:
        if p["geo"] != "ES":
            won.update(p["won"])
    return sorted(won.values(), reverse=True)


def build() -> dict:
    rows, warnings = [], []
    for election in PAGES:
        text = sources.wikipedia(page(election))
        res = [(n, s) for n, s in results_table(text) if s > 0]
        seats = sorted((s for _, s in res), reverse=True)
        assert sum(seats) == SEATS, f"{election}: {sum(seats)} escaños"
        leg = legend(text)
        if leg != seats:
            warnings.append(f"{election}: la leyenda de la ficha no coincide con la tabla ({leg} frente a {seats})")
        if election == "2023-07":
            assert seats == _official_2023(), "2023: no coincide con Infoelectoral"
        for n, s in sorted(res, key=lambda x: -x[1]):
            rows.append({"election": election, "year": int(election[:4]), "list": n, "seats": s})
    return {
        "id": "generales-escanos",
        "title": "Escaños de cada candidatura en las elecciones al Congreso, 1977-2023",
        "source": SOURCE,
        "notes": [
            "Tabla de resultados del Congreso del artículo de Wikipedia de cada elección; se comprueba que suma 350 escaños, "
            "que coincide con la leyenda del diagrama de escaños del mismo artículo y, en 2023, con Infoelectoral.",
            "Candidaturas como las agrupa la tabla: un partido y sus listas asociadas en una comunidad cuentan juntos "
            "(por ejemplo, PSOE con el PSC) y una coalición cuenta como una sola candidatura.",
            "Solo candidaturas con escaño.",
        ],
        "pages": {e: url(e) for e in PAGES},
        "warnings": warnings,
        "rows": rows,
    }
