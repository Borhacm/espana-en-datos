"""Registro de gráficos. Cada tema es un módulo (charts/<tema>.py) con BUILDERS; añádelo aquí.
Las notas (charts/notas/) se registran solas."""

from . import congreso, demografia, elecciones, empleo, inmigracion, legislatura, notas, vivienda

BUILDERS = [*elecciones.BUILDERS, *congreso.BUILDERS, *vivienda.BUILDERS, *legislatura.BUILDERS, *empleo.BUILDERS, *demografia.BUILDERS, *inmigracion.BUILDERS, *notas.BUILDERS]
