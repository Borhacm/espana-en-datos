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
    "europa": "España frente a Europa",
    "dentro": "España por dentro",
    "tiempo": "España en el tiempo",
}
# Se rellena al importar charts/: cada paquete de tema declara su THEME
THEMES: dict[str, dict] = {}


def chart(*, id, lens, theme, title, subtitle, unit, source, rows, geos=None, notes=None, extra=None) -> dict:
    """Valida y empaqueta un gráfico. `rows` es una lista de observaciones con al menos 'value'."""
    assert lens in LENSES and theme in THEMES, id
    assert rows, f"{id}: sin datos"
    for r in rows:
        v = r["value"]
        assert isinstance(v, (int, float)) and not math.isnan(v), f"{id}: valor no numérico {r}"
    return {
        "id": id,
        "lens": lens,
        "theme": theme,
        "title": title,
        "subtitle": subtitle,
        "unit": unit,
        "source": source,
        "notes": notes or [],
        "retrieved": dt.date.today().isoformat(),
        "geos": geos or {},
        **(extra or {}),
        "rows": rows,
    }


def write(charts: list[dict]) -> None:
    """Escribe solo los gráficos generados: una ejecución parcial no toca los demás."""
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    for c in charts:
        (CHARTS_DIR / f"{c['id']}.json").write_text(json.dumps(c, ensure_ascii=False, indent=1))


def write_base(d: dict, compact: bool = False) -> Path:
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    d = {**d, "retrieved": dt.date.today().isoformat()}
    path = BASE_DIR / f"{d['id']}.json"
    path.write_text(json.dumps(d, ensure_ascii=False, separators=(",", ":")) if compact else json.dumps(d, ensure_ascii=False, indent=1))
    return path
