"""Registro de gráficos. Cada tema es un módulo (charts/<tema>.py) con BUILDERS; añádelo aquí.
Las notas (charts/notas/) se registran solas."""

from . import autonomias, clima, congreso, demografia, educacion, elecciones, empleo, energia, fiscalidad, inmigracion, jovenes, legislatura, notas, productividad, sanidad, territorio, vivienda

BUILDERS = [*elecciones.BUILDERS, *congreso.BUILDERS, *vivienda.BUILDERS, *legislatura.BUILDERS, *empleo.BUILDERS, *demografia.BUILDERS, *inmigracion.BUILDERS, *autonomias.BUILDERS, *sanidad.BUILDERS, *educacion.BUILDERS, *fiscalidad.BUILDERS, *energia.BUILDERS, *productividad.BUILDERS, *jovenes.BUILDERS, *territorio.BUILDERS, *clima.BUILDERS, *notas.BUILDERS]
