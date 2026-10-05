# España en datos

España contada con datos abiertos: economía, vivienda, empleo, política y territorio, comparados con Europa, entre comunidades y con el pasado. Sustituye a la antigua web de espanaendatos.bocal.online (FastAPI en Render, archivada en `~/Spain-grpahic`).

Hermano de [Europa en datos](https://europa.bocal.online): misma arquitectura (Astro estático + D3, pipeline en Python que escribe JSON versionado en git), con la piel visual de bocal.online (Bricolage Grotesque + Inter, ink/paper/brand).

## Miradas

- **España frente a Europa**: España con la media de la UE y los países de su tamaño.
- **España por dentro**: diferencias entre comunidades y quién gobierna en cada una.
- **España en el tiempo**: desde 2008, la pandemia y el inicio de la legislatura.

## Especial elecciones del 29N

`/elecciones-29n/`: seguimiento de encuestas con media propia (EL-1), simulador de escaños, mapa de 2023 por provincia y municipio (EL-2) y presidencias autonómicas desde 1980 (EL-3). Metodología completa en `/metodologia/`.

**Veda electoral (LOREG, art. 69.7):** del 24 al 28 de noviembre no se pueden publicar encuestas. El seguimiento y la posición inicial del simulador se ocultan en el navegador esos días. Además, hay que **volver a publicar el 24 de noviembre** sin encuestas nuevas y no actualizar `encuestas` hasta las 21.00 del 29.

## Datos

```
pipeline/
  lib/          descargas con caché, geografía (códigos INE), lectores (Eurostat, OCDE, Wikipedia)
  datasets/     datasets base, reutilizados por varios gráficos:
                gobiernos (presidencias autonómicas), encuestas, elecciones (Infoelectoral),
                escanos (reparto de 2026 por población, LOREG art. 162)
  charts/       un módulo por tema; elecciones.py = especial 29N y datos del simulador
data/base/      salida de datasets/
data/charts/    un JSON por gráfico
data/geo/       geometrías (IGN vía es-atlas)
```

Uso, desde `pipeline/`:

```
uv run run.py                         todo (usa la caché de data/raw)
uv run run.py --refresh               vuelve a descargar todo
uv run run.py --only charts.elecciones  solo el especial
```

## Web

Desde `web/`: `npm run dev`, `npm run build`, `npm run check` (dibuja todos los gráficos sin interfaz con Playwright y comprueba que el simulador reproduce el resultado de 2023).

## Reglas editoriales

- Describir, no atribuir: que una comunidad gobernada por un partido tenga un dato mejor o peor no prueba que sea por ese partido. Las fichas de política comparan con grupo de control y citan evaluaciones independientes.
- Mismo formato y exigencia para todos los partidos.
- Cada cifra del texto, comprobada contra el JSON del gráfico antes de publicar.
- Piezas electorales: **revisión humana antes de publicar** (PR que aprueba Borja).

Proyecto independiente de [Bocal](https://bocal.online).
