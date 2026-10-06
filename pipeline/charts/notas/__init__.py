"""Notas: un archivo por nota (charts/notas/<id>_<palabra>.py) con su lista BUILDERS. Se registran solos."""

import importlib
import pkgutil

BUILDERS = []
for _m in sorted(pkgutil.iter_modules(__path__), key=lambda m: m.name):
    BUILDERS += importlib.import_module(f"{__name__}.{_m.name}").BUILDERS
