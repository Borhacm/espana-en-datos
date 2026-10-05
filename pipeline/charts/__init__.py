"""Registro de gráficos: cada módulo expone BUILDERS."""

from . import elecciones, vivienda

BUILDERS = [*elecciones.BUILDERS, *vivienda.BUILDERS]
