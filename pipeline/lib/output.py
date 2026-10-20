"""Formato común de salida.

- data/base/<id>.json: datasets fundacionales (gobiernos, encuestas, elecciones) que reutilizan varios gráficos.
- data/charts/<id>.json: un JSON por gráfico.
"""

import datetime as dt
import json
import math
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
BASE_DIR = DATA_DIR / "base"
CHARTS_DIR = DATA_DIR / "charts"

LENSES = {
    "europa": {"es": "España frente a Europa", "en": "Spain and Europe"},
    "dentro": {"es": "España por dentro", "en": "Spain from within"},
    "tiempo": {"es": "España en el tiempo", "en": "Spain over time"},
}
LANGS = ("es", "en")


def _check_bilingual(v, where: str) -> None:
    """Todo texto de la web va en los dos idiomas: cualquier diccionario con "es" tiene que tener "en" (y al revés)."""
    if isinstance(v, dict):
        if "es" in v or "en" in v:
            missing = [l for l in LANGS if l not in v or v[l] in (None, "")]
            assert not missing, f"{where}: falta el texto en {missing}: {v}"
        for k, x in v.items():
            _check_bilingual(x, f"{where}.{k}")
    elif isinstance(v, list):
        for i, x in enumerate(v):
            _check_bilingual(x, f"{where}[{i}]")
# Se rellena al importar charts/: cada paquete de tema declara su THEME
THEMES: dict[str, dict] = {}


def chart(*, id, lens, theme, title, subtitle, unit, source, rows, geos=None, notes=None, extra=None) -> dict:
    """Valida y empaqueta un gráfico. `rows` es una lista de observaciones con al menos 'value'."""
    assert lens in LENSES and theme in THEMES, id
    assert rows, f"{id}: sin datos"
    for r in rows:
        v = r["value"]
        assert isinstance(v, (int, float)) and not math.isnan(v), f"{id}: valor no numérico {r}"
    # Textos en los dos idiomas de la web: {"es": ..., "en": ...}. Las notas, {"es": [...], "en": [...]} con el mismo número.
    for name, v in (("title", title), ("subtitle", subtitle), ("unit", unit)):
        assert isinstance(v, dict) and set(v) == set(LANGS), f"{id}: {name} tiene que ser {{'es', 'en'}}: {v!r}"
    notes = notes or {"es": [], "en": []}
    assert isinstance(notes, dict) and set(notes) == set(LANGS) and len(notes["es"]) == len(notes["en"]), \
        f"{id}: las notas tienen que ir en es y en, con el mismo número"
    out = {
        "id": id,
        "lens": lens,
        "theme": theme,
        "title": title,
        "subtitle": subtitle,
        "unit": unit,
        "source": source,
        "notes": notes,
        "retrieved": dt.date.today().isoformat(),
        "geos": geos or {},
        **(extra or {}),
        "rows": rows,
    }
    _check_bilingual({k: v for k, v in out.items() if k not in ("rows", "source", "notes")}, id)
    return out


def write(charts: list[dict]) -> None:
    """Escribe solo los gráficos generados: una ejecución parcial no toca los demás."""
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    for c in charts:
        # Si los datos no han cambiado (p. ej., al regenerar textos desde la caché), se conserva la fecha de descarga real
        path = CHARTS_DIR / f"{c['id']}.json"
        if path.exists():
            old = json.loads(path.read_text())
            if old.get("rows") == c["rows"] and old.get("retrieved"):
                c["retrieved"] = old["retrieved"]
        # Los gráficos con muchas filas (encuestas, mapas municipales) se escriben compactos
        indent = 1 if len(c["rows"]) < 2000 else None
        sep = None if indent else (",", ":")
        (CHARTS_DIR / f"{c['id']}.json").write_text(json.dumps(c, ensure_ascii=False, indent=indent, separators=sep))


def write_base(d: dict, compact: bool = False) -> Path:
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    d = {**d, "retrieved": dt.date.today().isoformat()}
    path = BASE_DIR / f"{d['id']}.json"
    path.write_text(json.dumps(d, ensure_ascii=False, separators=(",", ":")) if compact else json.dumps(d, ensure_ascii=False, indent=1))
    return path
