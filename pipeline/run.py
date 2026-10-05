"""Genera los datos de la web en data/.

Uso (desde pipeline/):
    uv run run.py                  datasets base y todos los gráficos (usa la caché de data/raw)
    uv run run.py --refresh        vuelve a descargar todo
    uv run run.py --only encuestas solo lo que contenga "encuestas" en su nombre

Una ejecución con --only no modifica lo demás.
"""

import sys
import traceback

from datasets import elecciones, encuestas, gobiernos
from lib import http
from lib.output import write, write_base

# (nombre, función, json compacto)
BASE = [
    ("gobiernos", gobiernos.build, False),
    ("encuestas", encuestas.build, False),
    ("congreso-202307", lambda: elecciones.build("202307"), True),
]


def main(args: list[str]) -> int:
    http.REFRESH = "--refresh" in args
    only = args[args.index("--only") + 1] if "--only" in args else None
    failed = []

    for name, build, compact in BASE:
        if only and only not in name:
            continue
        try:
            d = build()
        except Exception:
            failed.append(name)
            traceback.print_exc()
            continue
        path = write_base(d, compact)
        for w in d.get("warnings", []):
            print(f"AVISO {name}: {w}")
        print(f"ok  base/{path.name:<28} {path.stat().st_size // 1024:>6} KB")

    try:
        from charts import BUILDERS
    except ImportError:
        BUILDERS = []
    built = []
    for build in BUILDERS:
        if only and only not in build.__module__:
            continue
        try:
            c = build()
        except Exception:
            failed.append(f"{build.__module__}.{build.__name__}")
            traceback.print_exc()
            continue
        built.append(c)
        print(f"ok  {c['id']:<32} {len(c['rows']):>6} filas")
    write(built)

    for name in failed:
        print(f"ERR {name}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
