"""Registro de gráficos. Cada tema es un módulo (charts/<tema>.py) con BUILDERS; añádelo aquí.
Las notas (charts/notas/) se registran solas."""

from . import congreso, elecciones, empleo, legislatura, notas, vivienda

BUILDERS = [*elecciones.BUILDERS, *congreso.BUILDERS, *vivienda.BUILDERS, *legislatura.BUILDERS, *empleo.BUILDERS, *notas.BUILDERS]
