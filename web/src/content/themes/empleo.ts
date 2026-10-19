import { p, type Theme } from "../../lib/content-types";

// Cifras comprobadas contra data/charts/em*.json (INE y Eurostat, descargados el 9 de octubre de 2026).
// Tabla de verificación: editorial/registro/a02.md.
// Evaluaciones citadas: AIReF, Documento técnico 8/25 (22 de septiembre de 2025), y Banco de España, Informe Anual 2023,
// capítulo 3, recuadro 3.1.
const theme: Theme = {
  id: "empleo",
  code: "EM",
  slug: { es: "empleo" },
  title: { es: "Empleo: la reforma laboral, tres años después" },
  status: "published",
  published: "2026-10-09",
  updated: "2026-10-19",
  order: 3,
  dek: {
    es: "La reforma laboral de diciembre de 2021 cambió los contratos de trabajo. Desde entonces, los asalariados temporales del sector privado han pasado del 23,7 % al 12,4 %. Parte de ese cambio se ha ido a los fijos discontinuos, y el paro juvenil sigue entre los más altos de la UE.",
  },
  lenses: {
    europa: {
      lede: { es: "España ha dejado de ser una excepción en temporalidad. En paro juvenil, todavía no." },
      body: [
        p("El empleo será uno de los temas de la campaña del 29N, y la reforma laboral de 2021 es el cambio en los contratos de trabajo más importante de los últimos años. Su objetivo principal era reducir la temporalidad, uno de los rasgos que más distinguían al mercado de trabajo español del europeo."),
        p("En 2021, el 25,4 % de los asalariados españoles de 15 a 64 años tenía un contrato temporal, el segundo porcentaje más alto de la UE, solo por detrás de los Países Bajos. En 2025 era el 15,4 %. La media europea también bajó, pero mucho menos: del 14,0 % al 12,6 %. La distancia con la UE ha pasado de 11,4 a 2,8 puntos. España es ahora la tercera, por detrás de los Países Bajos (25,5 %) y Polonia (15,7 %), y casi igual que Francia y Portugal (15,2 %)."),
        { fig: "eme1-europa-temporalidad", code: "E1" },
        p("El paro de los jóvenes también ha bajado, pero sigue lejos de la media. En 2021, el 35,0 % de los menores de 25 años que querían trabajar no encontraba empleo; en 2025, el 24,9 %. En la UE, el 15,2 %. España tiene la segunda tasa más alta de los 26 países con datos, tras Rumanía (26,1 %). Grecia, que en 2021 tenía una tasa parecida (35,5 %), ha bajado al 19,1 %, e Italia, del 29,7 % al 20,6 %."),
        { fig: "eme2-europa-paro-juvenil", code: "E2" },
      ],
    },
    dentro: {
      lede: { es: "La temporalidad ha bajado en todas las comunidades, y más donde era más alta." },
      body: [
        p("En el sector privado, el porcentaje de asalariados con contrato temporal ha bajado en las 17 comunidades entre 2021 y el último año (del tercer trimestre de 2025 al segundo de 2026). Las mayores bajadas están, en general, donde la temporalidad era más alta: Andalucía (del 35,3 % al 18,1 %), Extremadura (15,4 puntos menos), Murcia (15,1) y Canarias (14,1). Las menores, en Navarra (6,4 puntos) y el País Vasco (6,8)."),
        p("Las diferencias se han estrechado, pero siguen ahí. Andalucía (18,1 %), Extremadura (17,2 %) y Murcia (15,2 %) tienen los porcentajes más altos; Madrid (9,3 %), Cataluña (10,2 %) y Galicia (10,3 %), los más bajos."),
        { fig: "emd1-temporalidad-comunidades", code: "D1" },
        p("El otro problema persistente es el paro de larga duración. En el último año, el 35,4 % de los parados llevaba un año o más buscando empleo, frente al 47,8 % de 2021, cuando todavía pesaban los despidos de la pandemia. Canarias (45,2 %) y Castilla-La Mancha (40,6 %) tienen los porcentajes más altos. Baleares, con el 19,3 %, el más bajo, y también la mayor bajada desde 2021 (24,7 puntos)."),
        { fig: "emd2-paro-larga-comunidades", code: "D2" },
      ],
    },
    tiempo: {
      lede: { es: "La temporalidad del sector privado está en su nivel más bajo desde, al menos, 2008. La del sector público ha bajado mucho menos." },
      body: [
        { h: { es: "La ficha: la reforma laboral de 2021" }, id: "ficha-reforma" },
        { steps: [
          { title: { es: "Qué es." }, text: { es: "El Real Decreto-ley 32/2021, de 28 de diciembre, pactado por el Gobierno con los sindicatos y las organizaciones empresariales. Eliminó el contrato de obra y servicio, limitó los contratos temporales a causas concretas y de duración corta, endureció el encadenamiento de contratos y amplió el uso del contrato fijo discontinuo." } },
          { title: { es: "Cuándo." }, text: { es: "Entró en vigor el 31 de diciembre de 2021, pero los cambios en los contratos rigen desde el 30 de marzo de 2022." } },
          { title: { es: "Qué debería pasar." }, text: { es: "Menos contratos temporales y empleos más estables. El riesgo que señalaban sus críticos era que los temporales se convirtieran en indefinidos igual de inestables, en especial fijos discontinuos." } },
          { title: { es: "Con qué lo comparamos." }, text: { es: "Con el sector público, que contrata sobre todo con sus propias normas. No es una comparación perfecta: a la vez se aprobó la Ley 20/2021 para reducir la temporalidad de los interinos." } },
        ] },
        p("Entre 2008 y 2021, la temporalidad del sector privado subía y bajaba con el ciclo, pero no bajó del 21 % en ningún trimestre. En 2021, la media fue del 23,7 %. Desde que rigen los nuevos contratos ha caído con rapidez, y en el último año fue del 12,4 %, el nivel más bajo de la serie, que empieza en 2008. En el sector público, la temporalidad siguió subiendo hasta superar el 32 % en el año que acaba en el segundo trimestre de 2022, y desde entonces ha bajado al 27,0 %, un nivel parecido al de 2019. Entre 2021 y el último año, la temporalidad ha bajado 11,3 puntos en el sector privado y 4,2 en el público."),
        { fig: "emt1-temporalidad-sectores", code: "T1" },
        p("Una parte del cambio ha ido a los fijos discontinuos, un contrato indefinido para trabajos de temporada o intermitentes en el que no se cobra entre un periodo de actividad y el siguiente. Eran el 2,5 % de los asalariados del sector privado en 2021 y el 4,1 % en el último año. Si se suman a los temporales, el porcentaje baja del 26,2 % al 16,5 %: casi 10 puntos, menos que la temporalidad sola, pero una caída grande."),
        { fig: "emt2-fijos-discontinuos", code: "T2" },
        p("Lo que dicen las evaluaciones independientes. El Banco de España (Informe Anual 2023) concluyó que la estabilidad del empleo en su conjunto había aumentado ligeramente, porque pesan mucho más los contratos indefinidos, aunque los nuevos indefinidos, y en especial los fijos discontinuos, duran algo menos que antes. De los contratos firmados en marzo de 2022, el 16,1 % seguía activo un año después, frente al 11 % de los firmados en marzo de 2017 y 2018. Advierte de que la comparación no es causal."),
        p("La AIReF (documento técnico de septiembre de 2025) compara los sectores y ocupaciones más expuestos a la temporalidad con los demás. Encuentra que la reforma redujo un poco la probabilidad de perder el empleo y mejoró algo la de encontrarlo, y que aumentó el paso de contratos temporales a fijos discontinuos, pero no encuentra un efecto claro en el paso a indefinidos ordinarios ni en el crecimiento del empleo total. Pide cautela: son efectos medios, en pocos años y con muchos otros cambios a la vez."),
        p("En resumen: la temporalidad ha bajado mucho más en el sector privado que en el público y que en Europa, y las dos evaluaciones relacionan esa caída con la reforma. Lo que sigue en discusión es cuánto más estable es el empleo que la ha sustituido."),
        p("Lo que no dicen estos datos. La EPA es una encuesta de personas, no un registro de contratos: dice cuántos asalariados tienen un contrato temporal, pero no cuántos contratos se firman ni cuánto duran. Para eso hacen falta los registros de afiliación a la Seguridad Social, que son los que usan el Banco de España y la AIReF. El sector público no es un grupo de comparación perfecto, porque a la vez tuvo su propia ley contra la temporalidad. Y la tasa de paro juvenil se calcula sobre los jóvenes que buscan trabajo, no sobre todos: muchos menores de 25 años estudian y no cuentan como activos."),
        { see: { es: "Nota: salarios reales y salario mínimo desde 2008" }, href: "/notas/salarios-reales-salario-minimo/" },
        { see: { es: "La legislatura en datos: paro, crecimiento y tasa de empleo desde 2023" }, href: "/la-legislatura-en-datos/" },
      ],
    },
  },
  sources: [
    { name: "BOE: Real Decreto-ley 32/2021, de medidas urgentes para la reforma laboral", url: "https://www.boe.es/buscar/act.php?id=BOE-A-2021-21788" },
    { name: "BOE: Ley 20/2021, de medidas urgentes para la reducción de la temporalidad en el empleo público", url: "https://www.boe.es/buscar/act.php?id=BOE-A-2021-21651" },
    { name: "AIReF: Documento técnico sobre el análisis del mercado laboral y el impacto de las medidas de reforma implementadas (DT 8/25)", url: "https://www.airef.es/wp-content/uploads/2025/09/Documentos-tecnicos-macro-opinion-sostenibilidad/250922_DT_Analisis_mercado_laboral.pdf" },
    { name: "Banco de España: Informe Anual 2023, capítulo 3 (recuadro 3.1)", url: "https://www.bde.es/f/webbe/SES/Secciones/Publicaciones/PublicacionesAnuales/InformesAnuales/23/Fich/InfAnual_2023_Cap3.pdf" },
  ],
};

export default theme;
