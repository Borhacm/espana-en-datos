import { p, type Note } from "../../lib/content-types";

// Cifras comprobadas contra data/charts/n03-*.json, data/base/participacion.json (Infoelectoral) e INE, PERE (tabla 71106).
// Tabla de verificación: editorial/registro/n03.md.
const note: Note = {
  id: "n03",
  code: "N03",
  slug: { es: "participacion-generales-1977", en: "general-election-turnout-1977" },
  title: { es: "La participación de 2023, del 66,6 %, es la tercera más baja en unas generales desde 1977", en: "Turnout in 2023, at 66.6%, is the third lowest in a general election since 1977" },
  dek: {
    es: "En las 16 generales desde 1977 la participación ha ido del 80,0 % de 1982 al 66,2 % de noviembre de 2019. Por comunidades, en 2023 hubo 14,8 puntos entre Castilla-La Mancha y Canarias, y una parte de la diferencia viene de los electores que viven en el extranjero.",
    en: "In the 16 general elections since 1977, turnout has ranged from 80.0% in 1982 to 66.2% in November 2019. By region, in 2023 there were 14.8 points between Castile-La Mancha and the Canary Islands, and part of the gap comes from voters who live abroad.",
  },
  published: "2026-10-26",
  lens: "tiempo",
  theme: "elecciones",
  body: [
    p("En las generales de julio de 2023 votaron 24,95 millones de personas de un censo de 37,47 millones: 12,5 millones no votaron. La participación será una de las cifras del 29 de noviembre, y los datos del Ministerio del Interior permiten ver cómo ha cambiado desde 1977.", "In the July 2023 general election, 24.95 million people voted out of an electoral roll of 37.47 million: 12.5 million did not vote. Turnout will be one of the figures of 29 November, and Ministry of the Interior data shows how it has changed since 1977."),
    p("El máximo de la serie es 1982, con un 80,0 %. Desde entonces la participación solo ha superado el 75 % en 1993, 1996 y 2004. Las tres generales con menos participación son, en orden: noviembre de 2019 (66,2 %), 2016 (66,5 %) y 2023 (66,6 %). Dos de ellas fueron repeticiones convocadas unos seis meses después de las anteriores, y en ambas la participación bajó: 3,2 puntos en 2016 y 5,5 en noviembre de 2019.", "The highest value in the series is 1982, at 80.0%. Since then turnout has only gone above 75% in 1993, 1996 and 2004. The three general elections with the lowest turnout are, in order: November 2019 (66.2%), 2016 (66.5%) and 2023 (66.6%). Two of them were repeat elections called about six months after the previous one, and in both turnout fell: 3.2 points in 2016 and 5.5 in November 2019."),
    { fig: "n03-participacion", code: "1" },
    p("Un aviso sobre la comparación. La cifra oficial se calcula sobre todo el censo, que incluye a los españoles que viven en el extranjero, y estos votan mucho menos. Entre 2011 y 2019 tuvieron que pedir el voto antes de cada elección (el voto rogado), y en 2023, tras la Ley Orgánica 12/2022, ya no. Los ficheros de resultados no separan su voto, así que no se puede saber cuánto de la caída desde 2011 se debe a ellos.", "A word of caution about the comparison. The official figure is calculated on the whole roll, which includes Spaniards living abroad, and they vote much less. Between 2011 and 2019 they had to apply for a postal vote before each election (the 'voto rogado'), and in 2023, after Organic Law 12/2022, they no longer did. The results files do not separate their vote, so it is not possible to tell how much of the fall since 2011 is due to them."),
    p("Por comunidades, en 2023 la que más votó fue Castilla-La Mancha, que también tiene la media más alta de las 16 generales (77,2 %), y la que menos, sin contar Ceuta y Melilla, Canarias. El voto exterior pesa en esa diferencia: en Galicia hay 19,6 españoles inscritos en el padrón de residentes en el extranjero por cada 100 personas del censo, en Asturias 14,4 y en Canarias 10,4, frente a 7,4 en el conjunto de España y 2,8 en Castilla-La Mancha. Pero no lo explica todo: Baleares (61,3 %) y Cataluña (62,7 %) votaron poco con menos residentes fuera que la media (5,2 y 6,4 por cada 100). Cataluña, además, bajó 6,7 puntos respecto a noviembre de 2019, la mayor caída de las 17 comunidades.", "By region, in 2023 the one that voted most was Castile-La Mancha, which also has the highest average over the 16 general elections (77.2%), and the one that voted least, leaving aside Ceuta and Melilla, was the Canary Islands. The vote from abroad weighs on that gap: in Galicia there are 19.6 Spaniards in INE's register of residents abroad for every 100 people on the roll, in Asturias 14.4 and in the Canary Islands 10.4, compared with 7.4 for Spain as a whole and 2.8 in Castile-La Mancha. But it does not explain everything: the Balearic Islands (61.3%) and Catalonia (62.7%) voted little with fewer residents abroad than average (5.2 and 6.4 per 100). Catalonia also fell 6.7 points from November 2019, the largest drop of the 17 regions."),
    { fig: "n03-participacion-ccaa", code: "2" },
    p("Lo que no dicen estos datos. Son totales por provincia: no dicen quién vota por edad, renta o estudios, que solo se puede estimar con encuestas, ni por qué la participación sube o baja en cada elección.", "What this data does not say. These are provincial totals: they do not say who votes by age, income or education, which can only be estimated with surveys, nor why turnout rises or falls in each election."),
    { see: { es: "Elecciones generales del 29N", en: "29 November general election" }, href: "/elecciones-29n/" },
  ],
  sources: [
    { name: "Ley Orgánica 12/2022, de 30 de septiembre, de reforma de la Ley Orgánica 5/1985, de 19 de junio, del Régimen Electoral General, para la regulación del ejercicio del voto por los españoles que viven en el extranjero", url: "https://www.boe.es/eli/es/lo/2022/09/30/12" },
    { name: { es: "INE, Padrón de Españoles Residentes en el Extranjero a 1 de enero de 2023 (tabla 71106)", en: "INE, Register of Spaniards Resident Abroad on 1 January 2023 (table 71106)" }, url: "https://www.ine.es/jaxiT3/Tabla.htm?t=71106" },
  ],
};

export default note;
