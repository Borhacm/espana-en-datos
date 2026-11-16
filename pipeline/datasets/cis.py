"""Los principales problemas de España según los barómetros mensuales del CIS, desde enero de 2023.

Fuente: Centro de Investigaciones Sociológicas (CIS), barómetros mensuales, documento de marginales (es<estudio>mar.pdf)
de cada estudio. Pregunta: «¿Cuál es, a su juicio, el principal problema que existe actualmente en España? ¿Y el
segundo? ¿Y el tercero?» (respuesta espontánea, hasta tres respuestas, recodificada por el CIS). Se guarda el TOTAL
(porcentaje de entrevistados que citan el problema en cualquiera de los tres lugares) y el porcentaje que lo cita en
primer lugar. Se guarda también la pregunta «el problema que a usted, personalmente, le afecta más».

Lee el PDF con pdftotext (poppler). Se guarda en data/base para no depender de la web del CIS al rehacer los gráficos.
"""

import re
import subprocess

from lib import http

MONTHS = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
          "septiembre", "octubre", "noviembre", "diciembre"]
FIRST = (2023, 1)
PAGE = "https://www.cis.es/estudios/barometro-de-{month}-{year}"
SOURCE = {
    "name": "CIS, barómetros mensuales",
    "dataset": "Pregunta sobre los tres principales problemas de España (marginales de cada barómetro)",
    "url": "https://www.cis.es/estudios/catalogo",
    "license": "Reutilización libre citando la fuente",
}
QUESTIONS = {
    "espana": "principal problema que existe actualmente en España",
    "personal": "problema que a Ud., personalmente, le afecta más",
}
NUM = r"(?:\d{1,3},\d|-)"
ROW = re.compile(rf"^\s{{1,6}}(\S.*?)\s{{2,}}({NUM})\s+({NUM})\s+({NUM})\s+({NUM})\s*$")
SKIP = ("Ninguno", "N.S.", "N.C.", "Otras respuestas")


def _num(s: str) -> float:
    return 0.0 if s == "-" else float(s.replace(",", "."))


def _table(text: str, question: str) -> dict:
    """({problema: (primer lugar, total)}, entrevistados) de la tabla que sigue al enunciado de la pregunta."""
    i = text.find(question)
    assert i >= 0, f"no está la pregunta «{question}»"
    out, last, n = {}, None, None
    for line in text[i:].splitlines()[1:]:
        if line.strip().startswith("(N)"):
            n = int(re.search(r"\(([\d.]+)\)", line.strip()[3:]).group(1).replace(".", ""))
            break
        m = ROW.match(line)
        if m:
            label = m.group(1).strip()
            last = label
            out[label] = (_num(m.group(2)), _num(m.group(5)))
        elif last and line.startswith("   ") and line.strip() and not re.search(r"\d", line) and len(line) - len(line.lstrip()) <= 6:
            # Etiqueta partida en dos líneas: la continuación se pega a la anterior
            full = f"{last} {line.strip()}"
            out[full] = out.pop(last)
            last = full
    out = {k: v for k, v in out.items() if k not in SKIP}
    assert len(out) >= 20 and n, f"tabla demasiado corta ({len(out)} filas) o sin (N) para «{question}»"
    return out, n


def _study(year: int, month: int) -> dict | None:
    url = PAGE.format(month=MONTHS[month - 1], year=year)
    try:
        page = http.fetch(url, ".html").read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None
    m = re.search(r'href="(https://www\.cis\.es/documents/[^"]*/es(\d{4})mar[^"/]*\.pdf[^"]*)"', page)
    if not m:
        return None
    pdf = http.fetch(m.group(1).replace("&amp;", "&"), ".pdf")
    text = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True, check=True).stdout
    assert f"{m.group(2)}" in text, f"{url}: el PDF no es del estudio {m.group(2)}"
    try:
        tables = {k: _table(text, q) for k, q in QUESTIONS.items()}
    except AssertionError:
        # Algunos estudios (mayo de 2023) publican la tabla en horizontal, sin la columna de cada lugar: no se leen
        return None
    return {"time": f"{year}-{month:02d}", "study": int(m.group(2)), "url": url, "n": tables["espana"][1],
            **{k: t[0] for k, t in tables.items()}}


def build() -> dict:
    import datetime as dt

    today = dt.date.today()
    studies, missing = [], []
    y, m = FIRST
    while (y, m) <= (today.year, today.month):
        if m != 8:  # el CIS no hace barómetro en agosto
            s = _study(y, m)
            (studies.append(s) if s else missing.append(f"{y}-{m:02d}"))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    rows = []
    for s in studies:
        for q in QUESTIONS:
            for label, (first, total) in s[q].items():
                rows.append({"time": s["time"], "study": s["study"], "question": q, "problem": label,
                             "first": first, "total": total})
    return {
        "id": "cis-problemas",
        "title": "Principales problemas de España según los barómetros del CIS, desde enero de 2023",
        "source": SOURCE,
        "notes": [
            "question «espana»: «¿Cuál es, a su juicio, el principal problema que existe actualmente en España? ¿Y el segundo? "
            "¿Y el tercero?». question «personal»: «¿Y cuál es el problema que a Ud., personalmente, le afecta más?».",
            "Respuesta espontánea (sin lista), hasta tres respuestas, recodificada por el CIS en categorías.",
            "total: % de entrevistados que citan el problema en cualquiera de los tres lugares (suma más de 100). "
            "first: % que lo citan en primer lugar.",
            "time: mes del barómetro (no hay barómetro en agosto).",
        ],
        "studies": {s["time"]: {"study": s["study"], "url": s["url"], "n": s["n"]} for s in studies},
        "warnings": [f"sin barómetro o sin marginales: {', '.join(missing)}"] if missing else [],
        "rows": rows,
    }
