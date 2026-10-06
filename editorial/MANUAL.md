# Manual de publicación de España en datos

Procedimiento para preparar y publicar una **nota** o un **artículo** del [calendario](calendario.yaml). Lo sigue la rutina «espana-publicacion» (lunes, miércoles y viernes) y sirve igual para hacerlo a mano.

**La publicación es automática: nadie revisa antes.** Por eso las comprobaciones de este manual no son opcionales. Si algo falla o tienes una duda seria sobre un dato o sobre la neutralidad de un texto, **no publiques**: deja el trabajo en una rama y explica el problema en el resumen final.

## Reglas que no se rompen

1. **Cada cifra y cada afirmación de un título o de un texto sale de un JSON generado o de una fuente citada.** Cuenta, ordena y divide antes de escribir "casi todos", "más que nunca", "el doble" o "uno de cada tres". Si la historia prevista no se sostiene, cuenta la que dicen los datos.
2. **Neutralidad política.** Mismo formato y misma exigencia para todos los partidos. Describimos, no atribuimos: que una comunidad gobernada por un partido tenga un dato mejor o peor no prueba que sea por ese partido (influyen la renta, la demografía, el ciclo y quién tiene la competencia). Nunca pidas el voto ni califiques a un partido. Si valoras una política, compárala con un grupo de control y cita evaluaciones independientes (AIReF, Banco de España, Fedea, EsadeEcPol, IVIE, artículos académicos), y di cuándo la evidencia no es concluyente.
3. **Veda electoral (LOREG, art. 69.7): del 24 al 28 de noviembre de 2026**, ninguna pieza muestra, cita ni resume encuestas de intención de voto, y no se actualizan las encuestas (paso 2). El sábado **28 de noviembre (jornada de reflexión) no se publica nada**.
4. Nunca regeneres datos ajenos a tu pieza: ejecuta el pipeline siempre con `--only`. Solo usa `--refresh` en el paso 2 (encuestas).
5. No cambies la configuración de Vercel ni el dominio. No borres archivos ajenos a tu pieza.
6. Español de España. **Nunca uses la raya (—)**: usa punto, coma o dos puntos. Coma decimal y espacio antes de %: "12,5 %". Títulos en frase normal que afirman el hallazgo.

## 1. Preparar el repositorio

```bash
cd /Users/bcm/espana-en-datos
git status --short          # debe estar vacío; si no, para y explica qué hay
git checkout main
```

El repositorio es local (sin GitHub). La web se publica con la CLI de Vercel desde `web/` (paso 9).

## 2. Actualizar las encuestas (cada ejecución, salvo en veda)

Si la fecha y hora actuales **no** están entre el 24 de noviembre de 2026 a las 00.00 y el 29 de noviembre a las 21.00:

```bash
cd pipeline
uv run run.py --refresh --only encuestas
uv run run.py --only charts.elecciones
```

Comprueba que `data/base/encuestas.json` no ha perdido encuestas (el número de filas no baja) y que el título de `data/charts/el1-encuestas.json` tiene sentido. Si la página de Wikipedia ha cambiado de formato y el lector falla, no toques las encuestas en esta ejecución y dilo en el resumen.

## 3. Elegir la entrada

Lee `editorial/calendario.yaml` y toma la **primera** entrada con `estado` distinto de `hecha` cuya `fecha` sea **hoy o anterior**. Si hoy es 28 de noviembre, no publiques. Si no queda ninguna entrada para hoy, publica solo la actualización de encuestas (pasos 8 a 10) y termina.

## 4. Buscar y comprobar los datos

- Empieza por la `idea` del calendario, pero compruébala: que la fuente existe, qué dimensiones tiene y cuál es el último periodo completo.
- Lectores en `pipeline/lib/sources.py`: `ine_table` (API del INE: busca tablas con `https://servicios.ine.es/wstempus/js/ES/TABLAS_OPERACION/<id>`), `eurostat`, `oecd`, `worldbank`, `socrata_cat` (datos abiertos de Cataluña), `wikipedia`. Resultados electorales: `pipeline/datasets/elecciones.py` (Infoelectoral, ficheros MUNI; necesita la cabecera de navegador de `lib/http.py`). Gobiernos autonómicos: `datasets/gobiernos.py`. Escaños 2026: `datasets/escanos.py`.
- Geografía (`pipeline/lib/geo.py`): comunidades con código INE (`"01"`... `"19"`) y `"ES"` para el total; provincias `"01"`... `"52"`; países en ISO3 (`"ESP"`, `"DEU"`) y `"EU27"`. `geo.ccaa_table()` y `geo.country_table()` dan los nombres para el JSON.
- Utilidades comunes en `pipeline/charts/common.py`: `ine_ccaa` (nombre del INE a código), `annual` (media anual con años completos), `pct`, `es_num`.

## 5. Escribir los gráficos (pipeline)

Ejemplo completo: `pipeline/charts/vivienda.py` (artículo con seis gráficos, incluida una ficha de política).

- **Artículo:** un módulo `pipeline/charts/<tema>.py` con `THEMES["<tema>"] = {"code": "XX", "title": "..."}` y `BUILDERS`; regístralo en `pipeline/charts/__init__.py`. **Dos gráficos por mirada** si los datos lo permiten (como mínimo uno): `europa` (España frente a la UE y países comparables), `dentro` (comunidades o provincias), `tiempo` (evolución).
- **Nota:** un archivo `pipeline/charts/notas/<id>_<palabra>.py` con `BUILDERS` (se registra solo). Uno o dos gráficos.
- Identificador de cada gráfico: `<código del tema en minúsculas><e|d|t><n>-<palabras>` (por ejemplo `vid2-cataluna-rentas`); en notas, `<id>-<palabras>` (por ejemplo `n02-salario-real`).
- Cada gráfico: título (el hallazgo), subtítulo (qué se mide, unidad, periodo), unidad, fuente con licencia, notas metodológicas (qué mide, qué falta, qué no se puede comparar) y filas. Para titulares con datos trimestrales, usa medias de cuatro trimestres, no un trimestre suelto.

```bash
cd pipeline && uv run run.py --only charts.<tema>      # o --only charts.notas
```

## 6. Verificar cada afirmación

Abre los JSON y calcula todo lo que vas a escribir. Para cada número del texto, anota su valor exacto y su gráfico en `editorial/registro/<id>.md` (tabla de verificación: cifra del texto, valor en el JSON, gráfico). Comprueba cuantificadores, récords ("el más alto": revisa toda la serie), proporciones, rankings y periodos. Si mezclas fuentes o definiciones, dilo en las notas del gráfico. Si un territorio pequeño (Ceuta, Melilla) es un extremo por volatilidad, no lo pongas en el titular y explícalo en una nota.

## 7. Escribir la web

- **Configuración de los gráficos:** `web/src/content/charts/<tema o id>.ts`. Renderizadores probados en este proyecto: `line` (series temporales; admite `series`, `seriesColors`, datos trimestrales con `quarterly`, fechas clave con `events`, etiquetas cortas con `short_labels`, línea de referencia con `ref_line`), `rank` (ranking de países de la UE o de comunidades; España se destaca sola), `spainmap` (mapa por provincia o municipio, preparado para resultados electorales), `govtimeline` y `polls` (solo del especial). `stack`, `paired`, `dumbbell` y `map` vienen de Europa en datos y no se han probado aquí: si los usas, comprueba que se ven bien. Opciones en `web/src/lib/charts-config.ts`. Colores: usa tokens de `web/src/styles/global.css` (`--es` España, `--eu` UE, `--focus`, `--context`, y los de partido `--p-*` solo para partidos).
- **Artículo:** `web/src/content/themes/<tema>.ts` (si ya existe como `status: "upcoming"`, sustitúyelo) con `code`, `slug`, `title`, `status: "published"`, `published` (fecha de hoy), `dek`, `lenses` (`europa`, `dentro`, `tiempo`: entradilla y cuerpo con párrafos `p("...")` y gráficos `{ fig, code: "E1" }`) y `sources` (fuentes de lo que no sale de los gráficos). Modelo: `web/src/content/themes/vivienda.ts`. Explica en la entradilla o el primer párrafo por qué el tema importa el 29N.
- **Nota:** `web/src/content/notes/<id>.ts` con `id`, `code` (`N01`...), `slug`, `title`, `dek`, `published` (hoy), `lens`, `theme` (un tema publicado; las notas electorales van al tema `elecciones`) y `body`. Unas 250 palabras.
- Las piezas aparecen solas en la portada, los índices, la metodología y en «Análisis de campaña» del especial.

### Piezas sobre los programas electorales (a12, a13, a14)

- Solo los programas oficiales publicados en la web de cada partido (enlaza el PDF). Incluye a todos los partidos con grupo propio en el Congreso de 2023 y a los que tengan al menos un 3 % en la media de encuestas, con las mismas preguntas para todos y en el mismo orden (el de votos de 2023).
- Para cada medida: qué propone cada partido (en una frase, con sus palabras resumidas, sin adjetivos) y qué dicen los datos sobre el problema. No pongas notas ni veredictos ("falso", "inviable"). No estimes costes que no publique una fuente independiente.
- Si un partido no ha publicado su programa, dilo y no lo sustituyas por declaraciones.

## 8. Comprobar

```bash
cd web && npm run build && npm run check
```

`npm run check` dibuja todos los gráficos en un navegador sin interfaz y prueba el simulador. Tiene que terminar sin errores. `git status` solo debe mostrar archivos de tu pieza, los datos de encuestas del paso 2 y el calendario.

## 9. Publicar

1. Marca la entrada como `estado: hecha` en `editorial/calendario.yaml`.
2. Commit en `main`: `git add -A && git commit -m "<Nota|Artículo> <id>: <título>"` y, en una línea aparte al final del mensaje, `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. Si solo has actualizado encuestas: `Encuestas: actualización del <fecha>`.
3. Publica desde `web/` (el build sincroniza `../data`, por eso no se compila en remoto):

```bash
cd /Users/bcm/espana-en-datos/web
vercel build --prod --scope bocalma && vercel deploy --prebuilt --prod --scope bocalma
```

Comprueba que `vercel build` termina sin error **antes** de desplegar: si falla, `deploy --prebuilt` publicaría una versión vieja.

## 10. Comprobar la web real

- `curl -s -o /dev/null -w "%{http_code}" https://espanaendatos.bocal.online/<slug>/` (artículo) o `/notas/<slug>/` (nota) debe dar 200, y también `/data/charts/<id de un gráfico>.json`.
- `https://espanaendatos.bocal.online/elecciones-29n/` debe dar 200.

## 11. Terminar

Resumen breve en español: qué has publicado, el enlace, si se actualizaron las encuestas (y el nuevo titular de la media) y cualquier límite o duda que Borja deba conocer. Si no has publicado, di por qué y en qué paso te detuviste.
