"""Registro de gráficos. Cada tema es un módulo (charts/<tema>.py) con BUILDERS; añádelo aquí.
Las notas (charts/notas/) se registran solas."""

from . import elecciones, notas, vivienda

BUILDERS = [*elecciones.BUILDERS, *vivienda.BUILDERS, *notas.BUILDERS]
