import { p, type Theme } from "../../lib/content-types";

// Cifras comprobadas contra data/charts/in*.json (INE y Eurostat, descargados el 16 y el 19 de octubre de 2026).
// Tabla de verificación, guion y autoevaluación: editorial/registro/a04.md.
// Ficha: Real Decreto 316/2026 (BOE-A-2026-8284) y nota del Consejo de Ministros del 14 de abril de 2026.
// Estudios: Elias, Monras y Vázquez-Grenno (Journal of Labor Economics, 2025); Banco de España (Informe Anual 2025 y
// Boletín Económico 2025/T2, Cuadrado y Regil).
const theme: Theme = {
  id: "inmigracion",
  code: "IN",
  slug: { es: "inmigracion" },
  title: { es: "Inmigración en datos" },
  status: "published",
  published: "2026-10-16",
  updated: "2026-10-19",
  order: 5,
  dek: {
    es: "Uno de cada cinco residentes en España nació en otro país, y uno de cada cuatro entre quienes tienen edad de trabajar. Son más jóvenes que la población nacida aquí, trabajan casi en la misma proporción y con más frecuencia por debajo de su formación. Antes del 29N repasamos de dónde vienen, dónde viven, cómo les va en el trabajo, qué dice la evidencia sobre su efecto en la economía y en qué consiste la regularización extraordinaria de 2026.",
  },
  lenses: {
    europa: {
      lede: { es: "España tiene más población nacida fuera que la media de la UE. La diferencia de empleo con los nacidos en el país es menor que en Europa, pero la sobrecualificación es mayor." },
      body: [
        p("Hay dos formas de contar la inmigración. Una cuenta a las personas nacidas en otro país, tengan o no la nacionalidad española; la otra, a las personas de nacionalidad extranjera, hayan nacido donde hayan nacido. Este artículo usa la primera siempre que puede, porque permite comparar países y no cambia cuando alguien se nacionaliza. Algunas estadísticas, como la Encuesta de Población Activa por comunidades o la sobrecualificación de Eurostat, solo existen por nacionalidad; lo indicamos en cada gráfico."),
        p("Por delante de España en población nacida fuera hay ocho países: Luxemburgo (51,5 %), Malta, Chipre, Irlanda, Austria, Suecia, Alemania (20,5 %) y Bélgica. Francia (14,0 %) e Italia (11,8 %) quedan por debajo. Desde 2015, la proporción ha subido 6,6 puntos en España, la quinta mayor subida de la UE, después de Malta, Alemania, Luxemburgo e Irlanda."),
        { fig: "ine1-europa-nacidos-fuera", code: "E1" },
        p("En Alemania y Francia, la tasa de empleo de los nacidos fuera está más de 11 puntos por debajo de la de los nacidos en el país (11,5 y 12,4 puntos). En España la distancia es mucho menor, pero no solo porque a los inmigrantes les vaya mejor: también porque la tasa de empleo de los nacidos en España (73,3 %) es inferior a la media europea de los nativos (77,2 %). La de los nacidos fuera ha subido 10,9 puntos desde 2015, cuando era del 58,7 %."),
        { fig: "ine2-europa-empleo", code: "E2" },
        p("Tener trabajo no significa trabajar en lo que uno ha estudiado. Entre los ocupados con estudios superiores, el 32,7 % de los españoles trabaja en un empleo que no los requiere: es el porcentaje más alto de los 20 países de la UE con datos. Entre los extranjeros, el 46,4 %. La distancia entre unos y otros (13,7 puntos) es algo menor que en la media de la UE (16,9 puntos, con el 36,9 % de los extranjeros y el 20,0 % de los nacionales). Los porcentajes más altos de extranjeros sobrecualificados son los de Grecia (72,9 %), Estonia (56,4 %) e Italia (54,8 %)."),
        { fig: "ine3-europa-sobrecualificacion", code: "E3" },
      ],
    },
    dentro: {
      lede: { es: "En Baleares, Cataluña, Madrid y la Comunidad Valenciana, más de uno de cada cuatro residentes nació fuera. El paro de los extranjeros es más alto que el de los españoles en todas las comunidades, pero la distancia cambia mucho." },
      body: [
        p("El 1 de enero de 2026 vivían en España 10,0 millones de personas nacidas en otro país, según el dato provisional del INE. Cuatro comunidades reúnen casi dos de cada tres (el 66 %): Cataluña (2,1 millones), Madrid (1,8), la Comunidad Valenciana (1,4) y Andalucía (1,2). En proporción, después de Baleares (29,3 %), Cataluña (26,1 %), Madrid (25,7 %) y la Comunidad Valenciana (25,5 %) viene Canarias (24,1 %). En el norte y el oeste los porcentajes son mucho menores: Asturias (12,6 %), Castilla y León (12,9 %) y Galicia (13,2 %)."),
        { fig: "ind1-comunidades-nacidos-fuera", code: "D1" },
        p("En el último año con datos, el paro de las personas de nacionalidad extranjera fue del 15,3 %, frente al 9,2 % de las de nacionalidad española. Donde menos se separan es en Canarias (13,1 % frente a 12,4 %), una comunidad con paro alto para todos. Donde más, sin contar Ceuta y Melilla, en Navarra (20,0 % frente a 5,9 %), Asturias (17,1 % frente a 8,0 %) y el País Vasco (15,3 % frente a 6,3 %). En las comunidades pequeñas la muestra de la encuesta es reducida y estas diferencias tienen un margen de error amplio."),
        { fig: "ind2-comunidades-paro", code: "D2" },
      ],
    },
    tiempo: {
      lede: { es: "En 2002 había nacido fuera el 5,7 % de los residentes; en 2026, el 20,2 %. También han cambiado los orígenes, y los nacidos fuera son mucho más jóvenes que los nacidos en España." },
      body: [
        p("La llegada no ha sido constante. Entre 2002 y 2009, los nacidos fuera pasaron del 5,7 % al 13,5 % de la población. Con la crisis, la cifra se estancó y después bajó un poco, hasta el 12,7 % en 2015 y 2016. Desde 2017 vuelve a subir, y más deprisa desde 2023. La población de nacionalidad extranjera sigue la misma curva, más abajo (14,6 % en 2026). La distancia entre las dos líneas corresponde a las personas nacidas fuera que tienen la nacionalidad española, descontados los extranjeros nacidos en España."),
        p("Todo el aumento de la población de España desde 2013 se debe a los nacidos fuera. La población nacida en España llegó a su máximo ese año, con 40,5 millones de personas, y ha bajado todos los años desde entonces, hasta 39,6 millones en 2026. La nacida fuera ha pasado, en el mismo periodo, de 6,2 a 10,0 millones."),
        { fig: "int1-poblacion", code: "T1" },
        p("También ha cambiado de dónde vienen. Entre 2005 y 2019, el grupo más numeroso eran los nacidos en otros países de Europa, sobre todo de la UE. Desde 2020 lo son los nacidos en Sudamérica: 3,7 millones el 1 de enero de 2025, casi cinco veces más que en 2002 (0,8 millones). Por países, el primero es Marruecos (1,17 millones), seguido de Colombia (0,98), Venezuela (0,69), Rumanía (0,52) y Ecuador (0,47)."),
        { fig: "int2-origen", code: "T2" },
        p("Los nacidos fuera son, sobre todo, personas en edad de trabajar. El 1 de enero de 2026 eran el 25,5 % de la población de 15 a 64 años, frente al 6,8 % en 2002. Entre los nacidos en España hay 38,8 personas de 65 años o más por cada 100 de 15 a 64; entre los nacidos fuera, 11,1. Para toda la población, la cifra es de 31,7. La proporción entre mayores y personas en edad de trabajar es uno de los factores del gasto en pensiones. Pero los inmigrantes también envejecen: entre 2004 y 2026, la tasa de los nacidos fuera ha pasado de 7,0 a 11,1."),
        { fig: "int3-dependencia", code: "T3" },
        { see: { es: "Demografía y pensiones: un país que envejece" }, href: "/demografia/" },

        { h: { es: "La ficha: la regularización extraordinaria de 2026" }, id: "ficha-regularizacion" },
        { steps: [
          { title: { es: "Qué es." }, text: { es: "Una vía excepcional para obtener una autorización de residencia y trabajo de un año, pensada para extranjeros que ya estaban en España antes del 1 de enero de 2026 sin autorización, o que habían pedido protección internacional antes de esa fecha. La regula el Real Decreto 316/2026, que modifica el Reglamento de Extranjería de 2024." } },
          { title: { es: "Quién y cuándo." }, text: { es: "La aprobó el Consejo de Ministros el 14 de abril de 2026 y se publicó en el BOE al día siguiente. Las solicitudes se podían presentar del 16 de abril al 30 de junio. Hacía falta llevar al menos cinco meses seguidos en España y no tener antecedentes penales y, en la vía general, haber trabajado o querer hacerlo, convivir con hijos menores u otros familiares a cargo o estar en situación de vulnerabilidad acreditada. Según el Gobierno, desde 1986 ha habido seis procesos anteriores, con casi 1,3 millones de personas regularizadas." } },
          { title: { es: "Qué debería pasar." }, text: { es: "Que personas que ya viven y trabajan en España pasen a la economía formal, coticen y paguen impuestos. Sus críticos señalan el riesgo de que anime a llegar a más personas en situación irregular, el llamado «efecto llamada»." } },
          { title: { es: "Con qué lo comparamos." }, text: { es: "Todavía no hay datos oficiales de sus resultados. El precedente más estudiado es la regularización de 2005." } },
        ] },
        p("Lo que dice la investigación sobre 2005: Ferran Elias, Joan Monras y Javier Vázquez-Grenno (Journal of Labor Economics, 2025) estudian aquel proceso, en el que casi 600.000 personas obtuvieron permiso de residencia y trabajo. Encuentran que las cotizaciones aumentaron en al menos 4.000 euros al año por cada trabajador regularizado, que subieron los salarios de los trabajadores nativos poco cualificados del sector formal y que no aumentaron los flujos de llegada. También que una parte de los regularizados volvió después a la economía sumergida. Es un solo episodio, en plena expansión económica, y no tiene por qué repetirse igual en 2026."),
        p("Sobre el efecto de la inmigración en la economía, el Banco de España estima en su Informe Anual de 2025 que la llegada de inmigrantes explicaría en torno a la mitad del crecimiento del PIB y más de dos tercios del aumento del empleo de los últimos años. Medido por habitante, el efecto es más pequeño: entre 2022 y 2024, la población extranjera aportó entre 0,4 y 0,7 puntos al crecimiento anual del PIB per cápita, que fue del 2,9 % (Cuadrado y Regil, Boletín Económico, 2025). Son descomposiciones contables, no estimaciones causales, y no dicen cuál será el saldo fiscal a largo plazo, cuando los inmigrantes de hoy cobren sus pensiones."),
        p("Lo que no dicen estos datos. Las cifras de población no distinguen a quienes tienen autorización de residencia de quienes no la tienen, así que no permiten saber cuántas personas están en situación irregular. Las llegadas y salidas de cada año tampoco se pueden seguir en una serie larga: el INE cambió en 2021 la forma de medirlas y, para ese mismo año, la estadística antigua contaba unas 529.000 inmigraciones procedentes del extranjero y la nueva, unas 888.000. Y el paro por comunidades se mide por nacionalidad: no permite saber cuánto de la diferencia con los españoles se debe a la edad, la formación, el sector o el tiempo que llevan en España."),
      ],
    },
  },
  sources: [
    { name: "BOE: Real Decreto 316/2026, de 14 de abril, por el que se modifica el Reglamento de extranjería (regularización extraordinaria)", url: "https://www.boe.es/buscar/doc.php?id=BOE-A-2026-8284" },
    { name: "La Moncloa: el Gobierno aprueba la regularización extraordinaria (14 de abril de 2026)", url: "https://www.lamoncloa.gob.es/consejodeministros/resumenes/paginas/2026/140426-rueda-prensa-ministros.aspx" },
    { name: "BOE: Real Decreto 1155/2024, Reglamento de la Ley Orgánica 4/2000 (texto consolidado)", url: "https://www.boe.es/buscar/act.php?id=BOE-A-2024-24099" },
    { name: "Elias, Monras y Vázquez-Grenno, Understanding the effects of granting work permits to undocumented immigrants (resumen de la UB)", url: "https://www.ub.edu/school-economics/news/understanding-the-effects-of-granting-work-permits-to-undocumented-immigrants/" },
    { name: "Banco de España, Informe Anual 2025 (resumen)", url: "https://www.bde.es/f/webbe/SES/Secciones/Publicaciones/PublicacionesAnuales/InformesAnuales/25/InfAnual_2025_Breve.pdf" },
    { name: "Cuadrado y Regil, Una estimación de la contribución de la población extranjera en España al crecimiento del PIB per cápita en 2022-2024 (Banco de España)", url: "https://www.bde.es/wbe/en/publicaciones/analisis-economico-investigacion/boletin-economico/2025t2-articulo-10-una-estimacion-de-la-contribucion-de-la-poblacion-extranjera-en-espana-al-crecimiento-del-pib-per-capita-en-el-periodo-2022-2024.html" },
    { name: "INE: Estadística de Migraciones (hasta 2021) y Estadística de Migraciones y Cambios de Residencia (desde 2021)", url: "https://www.ine.es/jaxiT3/Tabla.htm?t=24312" },
  ],
};

export default theme;
