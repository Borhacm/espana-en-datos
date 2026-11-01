# Manual de publicación de España en datos

Procedimiento para preparar y publicar una **nota** o un **artículo** del [calendario](calendario.yaml). Lo sigue la rutina «espana-publicacion» (lunes, miércoles y viernes) y sirve igual para hacerlo a mano.

**La publicación es automática: nadie revisa antes.** Por eso las comprobaciones de este manual no son opcionales. Si algo falla o tienes una duda seria sobre un dato o sobre la neutralidad de un texto, **no publiques**: deja el trabajo en una rama y explica el problema en el resumen final.

## Reglas que no se rompen

1. **Cada cifra y cada afirmación de un título o de un texto sale de un JSON generado o de una fuente citada.** Cuenta, ordena y divide antes de escribir "casi todos", "más que nunca", "el doble" o "uno de cada tres". Si la historia prevista no se sostiene, cuenta la que dicen los datos.
2. **Neutralidad política.** Mismo formato y misma exigencia para todos los partidos. Describimos, no atribuimos: que una comunidad gobernada por un partido tenga un dato mejor o peor no prueba que sea por ese partido (influyen la renta, la demografía, el ciclo y quién tiene la competencia). Nunca pidas el voto ni califiques a un partido. Si valoras una política, compárala con un grupo de control y cita evaluaciones independientes (AIReF, Banco de España, Fedea, EsadeEcPol, IVIE, artículos académicos), y di cuándo la evidencia no es concluyente.
3. **Veda electoral (LOREG, art. 69.7): del 24 al 28 de noviembre de 2026**, ninguna pieza muestra, cita ni resume encuestas de intención de voto, y no se actualizan las encuestas (paso 2). El sábado **28 de noviembre (jornada de reflexión) no se publica nada**.
4. Nunca regeneres datos ajenos a tu pieza: ejecuta el pipeline siempre con `--only`. Solo usa `--refresh` en el paso 2 (encuestas).
5. No cambies la configuración de GitHub Pages ni el dominio. No borres archivos ajenos a tu pieza.
6. Español de España. **Nunca uses la raya (—)**: usa punto, coma o dos puntos. Coma decimal y espacio antes de %: "12,5 %". Títulos en frase normal que afirman el hallazgo.
7. **La web es bilingüe: cada pieza se publica a la vez en español y en inglés** (español en la raíz, `/vivienda/`; inglés bajo `/en/`, `/en/housing/`). Primero se escribe y se verifica el español; el inglés es su traducción fiel: mismas cifras, mismos matices y mismas cautelas, sin añadir ni quitar nada. Inglés británico, punto decimal y % pegado ("12.5%"), nombres de comunidades como en `CCAA_EN` (`pipeline/lib/geo.py`), siglas de partidos sin traducir, y una aclaración breve la primera vez que sale una institución española ("INE, Spain's statistics office"; "AIReF, Spain's independent fiscal authority"). Tampoco en inglés se usa la raya. Si falta un texto en inglés, el pipeline o el build fallan: no lo esquives, tradúcelo.

## 1. Preparar el repositorio

```bash
cd <carpeta del repositorio>   # en local, ~/Projects/espana-en-datos; en una rutina en la nube, la que se haya clonado
git status --short          # debe estar vacío; si no, para y explica qué hay
git checkout main && git pull --ff-only
```

El repositorio está en GitHub (`Borhacm/espana-en-datos`, rama `main`). **GitHub Pages publica la web automáticamente cada vez que llega un commit a `main`** (workflow `.github/workflows/pages.yml`, como Europa en datos). Por eso nada que no haya pasado las comprobaciones puede llegar a `main`.

## 2. Actualizar las encuestas (cada ejecución, salvo en veda)

Si la fecha y hora actuales **no** están entre el 24 de noviembre de 2026 a las 00.00 y el 29 de noviembre a las 21.00:

```bash
cd pipeline
uv run run.py --refresh --only encuestas
uv run run.py --only charts.elecciones
```

Los lunes, actualiza también las votaciones del Congreso (solo descarga los plenos nuevos) y su sección:

```bash
uv run run.py --only congreso          # congreso-xv y el explorador (legislaturas X a XV); tarda unos minutos
uv run run.py --only charts.congreso
```

Si hay votaciones nuevas, revisa que los textos de `web/src/content/themes/congreso.ts` siguen cuadrando con los JSON (porcentajes y número de decretos derogados) y corrígelos. Si un decreto que figuraba en `LATE_DECREES` (`pipeline/charts/congreso.py`) ya aparece en los datos abiertos, quítalo de esa lista para no contarlo dos veces.

Comprueba que `data/base/encuestas.json` no ha perdido encuestas (el número de filas no baja) y que el título de `data/charts/el1-encuestas.json` tiene sentido. Si la página de Wikipedia ha cambiado de formato y el lector falla, no toques las encuestas en esta ejecución y dilo en el resumen.

## 3. Elegir la entrada

Lee `editorial/calendario.yaml` y toma la **primera** entrada con `estado` distinto de `hecha` cuya `fecha` sea **hoy o anterior**. Si hoy es 28 de noviembre, no publiques. Si no queda ninguna entrada para hoy, publica solo la actualización de encuestas (pasos 8 a 10) y termina.

## 3b. Guion antes de los datos (artículos)

Antes de abrir ninguna fuente, escribe en `editorial/registro/<id>.md` un **guion**: entre 5 y 7 preguntas que se haría un lector informado sobre el tema (no solo «cuánto» y «dónde», también «quién», «por qué», «qué ha cambiado» y «qué dice la evidencia»). Luego:

- **Inventario de fuentes:** al menos 10 conjuntos de datos candidatos (INE, Eurostat, OCDE, ministerios, Banco de España...) con qué pregunta respondería cada uno. Elige los gráficos por las preguntas, no por lo primero que encuentres.
- **Una pregunta, un gráfico.** Cada gráfico responde a una pregunta distinta del guion. **Un mismo hallazgo no se repite en dos miradas** (si el paro por nacionalidad está en «por dentro», no vuelve como titular en «en el tiempo»). Ningún número de un titular se repite en el titular de otro gráfico.
- **Mínimos de un artículo** (si no se cumplen, no se publica: ver paso 8b):
  1. Seis gráficos o más, dos por mirada.
  2. Al menos dos gráficos **explicativos**: composición (por origen, edad, sector...), descomposición de un cambio o relación entre dos variables. No basta con niveles y rankings.
  3. Una **ficha de política** (como la de vivienda o empleo: qué es, quién y cuándo, qué debería pasar, con qué se compara) sobre una norma vigente relacionada, con su enlace al BOE. Si no hay ninguna relevante, al menos **dos evaluaciones o estudios independientes** citados (AIReF, Banco de España, Fedea, EsadeEcPol, IVIE, artículos académicos), diciendo dónde la evidencia no es concluyente.
  4. Un párrafo de **«lo que no dicen estos datos»**: qué falta, qué no se puede comparar, qué no se puede atribuir.
  5. Un enlace a otro tema publicado cuando estén conectados (por ejemplo, inmigración y demografía).

## 4. Buscar y comprobar los datos

- Empieza por el guion y la `idea` del calendario, pero compruébala: que la fuente existe, qué dimensiones tiene y cuál es el último periodo completo.
- Lectores en `pipeline/lib/sources.py`: `ine_table` (API del INE: busca tablas con `https://servicios.ine.es/wstempus/js/ES/TABLAS_OPERACION/<id>`), `eurostat`, `oecd`, `worldbank`, `socrata_cat` (datos abiertos de Cataluña), `wikipedia`. Resultados electorales: `pipeline/datasets/elecciones.py` (Infoelectoral, ficheros MUNI; necesita la cabecera de navegador de `lib/http.py`). Infoelectoral no responde desde los entornos en la nube: los resultados de 2023 (`data/base/congreso-202307.json`) y la participación de todas las generales desde 1977 por provincia (`data/base/participacion.json`, dataset `participacion`) ya están guardados; léelos de ahí. Gobiernos autonómicos: `datasets/gobiernos.py`. Escaños 2026: `datasets/escanos.py`. Votaciones del Congreso (XV legislatura, voto de cada partido en cada votación nominal): `datasets/congreso.py`, con la sección `/congreso/` (`charts/congreso.py`) y su explorador de todas las legislaturas desde 2011 (`build_explorer`, `data/base/congreso-explorador.json`).
- Geografía (`pipeline/lib/geo.py`): comunidades con código INE (`"01"`... `"19"`) y `"ES"` para el total; provincias `"01"`... `"52"`; países en ISO3 (`"ESP"`, `"DEU"`) y `"EU27"`. `geo.ccaa_table()` y `geo.country_table()` dan los nombres para el JSON.
- Utilidades comunes en `pipeline/charts/common.py`: `ine_ccaa` (nombre del INE a código), `annual` (media anual con años completos), `pct`, `es_num`, `bi(es, en)` (texto en los dos idiomas), `dec(v, lang)` y `ordinal_en`. En `charts/legislatura.py`: `es1`/`en1` (un decimal con coma o con punto), `nm(code)` (nombre de una comunidad en inglés) y `_qlabel`/`_qlabel_en` (trimestres). En `lib/geo.py`: `ccaa_name(code, lang)` y `country_name(code, lang)`.

## 5. Escribir los gráficos (pipeline)

Ejemplo completo: `pipeline/charts/vivienda.py` (artículo con seis gráficos, incluida una ficha de política).

- **Artículo:** un módulo `pipeline/charts/<tema>.py` con `THEMES["<tema>"] = {"code": "XX", "title": "..."}` y `BUILDERS`; regístralo en `pipeline/charts/__init__.py`. **Dos gráficos por mirada** si los datos lo permiten (como mínimo uno): `europa` (España frente a la UE y países comparables), `dentro` (comunidades o provincias), `tiempo` (evolución).
- **Nota:** un archivo `pipeline/charts/notas/<id>_<palabra>.py` con `BUILDERS` (se registra solo). Uno o dos gráficos.
- Identificador de cada gráfico: `<código del tema en minúsculas><e|d|t><n>-<palabras>` (por ejemplo `vid2-cataluna-rentas`); en notas, `<id>-<palabras>` (por ejemplo `n02-salario-real`).
- Cada gráfico: título (el hallazgo), subtítulo (qué se mide, unidad, periodo), unidad, fuente con licencia, notas metodológicas (qué mide, qué falta, qué no se puede comparar) y filas. Para titulares con datos trimestrales, usa medias de cuatro trimestres, no un trimestre suelto.
- **Todo texto va en los dos idiomas:** `title=bi("...", "...")`, igual `subtitle` y `unit`; `notes={"es": [...], "en": [...]}` con el mismo número de notas; las etiquetas de `dimensions`, `events`, `ref_line` y `short_labels`, con `bi(...)`. `chart()` se niega a generar un gráfico al que le falte el inglés. Los números del inglés salen de las mismas variables que los del español, nunca escritos a mano. Modelo: `pipeline/charts/vivienda.py`.
- Los nombres de las fuentes (`source`) se escriben en español; la web traduce los conocidos con `web/src/lib/sources-en.ts`. Si usas una fuente o una licencia nueva, añade allí su traducción.
- **Las notas son metodología, no texto.** No repitas en las notas lo que ya dice el título o el párrafo (posiciones en rankings, máximos que el texto ya cita). Una definición que se aplica a varios gráficos se explica una vez en el texto y, en las notas, en una frase corta.
- Si un gráfico combina varias tablas de la misma operación, cita la fuente una vez con todas las tablas en `dataset` (no repitas el mismo `name` en `also`: la web lo mostraría varias veces).
- Revisa las frases generadas con contadores: nada de «17 de las 17»; escribe «en todas las comunidades».

```bash
cd pipeline && uv run run.py --only charts.<tema>      # o --only charts.notas
```

## 6. Verificar cada afirmación

Abre los JSON y calcula todo lo que vas a escribir. Para cada número del texto, anota su valor exacto y su gráfico en `editorial/registro/<id>.md` (tabla de verificación: cifra del texto, valor en el JSON, gráfico). Comprueba cuantificadores, récords ("el más alto": revisa toda la serie), proporciones, rankings y periodos. Si mezclas fuentes o definiciones, dilo en las notas del gráfico. Si un territorio pequeño (Ceuta, Melilla) es un extremo por volatilidad, no lo pongas en el titular y explícalo en una nota.

## 7. Escribir la web

- **Configuración de los gráficos:** `web/src/content/charts/<tema o id>.ts`. Renderizadores probados en este proyecto: `line` (series temporales; admite `series`, `seriesColors`, datos trimestrales con `quarterly`, fechas clave con `events`, etiquetas cortas con `short_labels`, línea de referencia con `ref_line`), `rank` (ranking de países de la UE o de comunidades; España se destaca sola), `spainmap` (mapa por provincia o municipio, preparado para resultados electorales), `govtimeline` y `polls` (solo del especial), `matrix` (matriz fila x columna: porcentajes con `matrixMode: "heat"` o votos a favor/en contra/abstención con `matrixMode: "votes"`). `stack`, `paired`, `dumbbell` y `map` vienen de Europa en datos y no se han probado aquí: si los usas, comprueba que se ven bien. Opciones en `web/src/lib/charts-config.ts`. Colores: usa tokens de `web/src/styles/global.css` (`--es` España, `--eu` UE, `--focus`, `--context`, y los de partido `--p-*` solo para partidos).
- **Artículo:** `web/src/content/themes/<tema>.ts` (si ya existe como `status: "upcoming"`, sustitúyelo) con `code`, `slug`, `title`, `status: "published"`, `published` (fecha de hoy), `dek`, `lenses` (`europa`, `dentro`, `tiempo`: entradilla y cuerpo con párrafos `p("español", "English")` y gráficos `{ fig, code: "E1" }`) y `sources` (fuentes de lo que no sale de los gráficos). Modelo: `web/src/content/themes/vivienda.ts`. Explica en la entradilla o el primer párrafo por qué el tema importa el 29N.
- **Los dos idiomas en cada texto:** todo lo que es `{ es: "..." }` lleva también `en`: `slug: { es: "vivienda", en: "housing" }` (el slug inglés, corto y en inglés, no puede coincidir con `themes`, `notes`, `lenses`, `methodology`, `congress` ni `general-election`), `title`, `dek`, entradillas, subtítulos, listas, pasos de las fichas y los `see`. En `sources`, `name` puede ser un texto (título original de una ley o un estudio) o `{ es, en }` si es una descripción nuestra. Los enlaces internos (`see`, fuentes) se escriben con la ruta en español (`/vivienda/`, `/notas/<slug>/`): la web los convierte a la ruta inglesa.
- **Nota:** `web/src/content/notes/<id>.ts` con `id`, `code` (`N01`...), `slug`, `title`, `dek`, `published` (hoy), `lens`, `theme` (un tema publicado; las notas electorales van al tema `elecciones`) y `body`, todo en los dos idiomas como los artículos. Unas 250 palabras. Modelo: `web/src/content/notes/n02.ts`.
- Las piezas aparecen solas en la portada, los índices, la metodología y en «Análisis de campaña» del especial.
- **El texto añade lo que el gráfico no enseña:** contexto, comparación, causas posibles con su evidencia, límites. No parafrasees el título del gráfico que viene después. La entradilla (`dek`) cuenta la idea principal del artículo, no la suma de los titulares de los gráficos.
- **Corregir una pieza publicada:** mantén `slug` y `published`, añade `updated` con la fecha y anota los cambios al final de `editorial/registro/<id>.md`.

### Piezas sobre los programas electorales (a12, a13, a14)

- Solo los programas oficiales publicados en la web de cada partido (enlaza el PDF). Incluye a todos los partidos con grupo propio en el Congreso de 2023 y a los que tengan al menos un 3 % en la media de encuestas, con las mismas preguntas para todos y en el mismo orden (el de votos de 2023).
- Para cada medida: qué propone cada partido (en una frase, con sus palabras resumidas, sin adjetivos) y qué dicen los datos sobre el problema. No pongas notas ni veredictos ("falso", "inviable"). No estimes costes que no publique una fuente independiente.
- Si un partido no ha publicado su programa, dilo y no lo sustituyas por declaraciones.

## 8. Comprobar

```bash
cd web && npm run build && npm run check
```

`npm run check` dibuja todos los gráficos en un navegador sin interfaz y prueba el simulador. Tiene que terminar sin errores. Lee también la versión inglesa de tu pieza en `web/dist/en/` (o con `npm run preview`): que no quede texto en español, que las cifras coincidan con las del español y que los enlaces apunten a páginas `/en/`. `git status` solo debe mostrar archivos de tu pieza, los datos de encuestas del paso 2 y el calendario. Si falta el navegador de Playwright, instálalo con `npx playwright install chromium-headless-shell` (desde `web/`).

## 8b. Autoevaluación (artículos)

Antes de publicar, rellena al final de `editorial/registro/<id>.md` esta lista y compárala con `vivienda` y `empleo`, los modelos:

- [ ] Cada pregunta del guion tiene su gráfico o su párrafo con fuente.
- [ ] Ningún hallazgo se repite en dos miradas ni ningún número de titular en dos gráficos.
- [ ] Dos gráficos explicativos o más.
- [ ] Ficha de política o dos estudios independientes citados en `sources`.
- [ ] Párrafo de «lo que no dicen estos datos».
- [ ] Las notas no repiten el texto.
- [ ] Un lector que sigue la prensa aprende al menos tres cosas que no sabía.
- [ ] La versión inglesa dice lo mismo que la española, con las mismas cifras y cautelas.

Si alguna casilla queda sin marcar y no se puede resolver en esta ejecución, **no publiques el artículo**: publica solo la actualización de encuestas, deja la pieza en una rama `borrador/<id>` y explica en el resumen qué falta.

## 9. Publicar

1. Marca la entrada como `estado: hecha` en `editorial/calendario.yaml`.
2. Commit en `main`: `git add -A && git commit -m "<Nota|Artículo> <id>: <título>"` y, en una línea aparte al final del mensaje, `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. Si solo has actualizado encuestas: `Encuestas: actualización del <fecha>`.
3. Publica: `git pull --rebase origin main && git push origin main`. Al llegar a `main`, GitHub Actions compila la web desde `web/` (el build copia `../data`) y la publica. Si el push falla, no se publica nada: dilo en el resumen.
4. Comprueba que el despliegue termina bien: `gh run list --repo Borhacm/espana-en-datos --workflow pages.yml --branch main --limit 1 --json headSha,status,conclusion` debe mostrar el SHA de tu commit con `conclusion` `success` (espera y repite unos minutos si `status` no es `completed`). Si da `failure`, la web sigue con la versión anterior: revisa el error con `gh run view --log-failed`, corrígelo con otro commit y vuelve a comprobar.

## 10. Comprobar la web real

- `curl -s -o /dev/null -w "%{http_code}" https://espanaendatos.bocal.online/<slug>/` (artículo) o `/notas/<slug>/` (nota) debe dar 200, y también `/data/charts/<id de un gráfico>.json`.
- La versión inglesa también debe dar 200: `/en/<slug inglés>/` (artículo) o `/en/notes/<slug inglés>/` (nota).
- `https://espanaendatos.bocal.online/elecciones-29n/` y `https://espanaendatos.bocal.online/en/general-election/` deben dar 200.

## 11. Terminar

Resumen breve en español: qué has publicado, el enlace, si se actualizaron las encuestas (y el nuevo titular de la media) y cualquier límite o duda que Borja deba conocer. Si no has publicado, di por qué y en qué paso te detuviste.
