"""Registro de gráficos. Cada tema es un módulo (charts/<tema>.py) con BUILDERS; añádelo aquí.
Las notas (charts/notas/) se registran solas."""

from . import autonomias, congreso, demografia, educacion, elecciones, empleo, energia, fiscalidad, inmigracion, legislatura, notas, sanidad, vivienda

BUILDERS = [*elecciones.BUILDERS, *congreso.BUILDERS, *vivienda.BUILDERS, *legislatura.BUILDERS, *empleo.BUILDERS, *demografia.BUILDERS, *inmigracion.BUILDERS, *autonomias.BUILDERS, *sanidad.BUILDERS, *educacion.BUILDERS, *fiscalidad.BUILDERS, *energia.BUILDERS, *notas.BUILDERS]
