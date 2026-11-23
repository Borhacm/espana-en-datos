import { p, type Note } from "../../lib/content-types";

// Cifras comprobadas contra data/charts/n07-*.json y data/base/congreso-202307.json (Infoelectoral).
// Tabla de verificación: editorial/registro/n07.md.
const note: Note = {
  id: "n07",
  code: "N07",
  slug: { es: "como-se-convierten-votos-en-escanos", en: "how-votes-become-seats" },
  title: {
    es: "La barrera real para entrar en el Congreso no es el 3 %, sino el tamaño de la provincia",
    en: "The real hurdle to enter Congress is not the 3% threshold but the size of the province",
  },
  dek: {
    es: "Con los votos de 2023, el mínimo legal del 3 % no cambió ningún escaño. Lo que decide cuántos votos hacen falta es cuántos diputados elige cada provincia: en Soria, una candidatura con el 19,1 % se quedó fuera; en Madrid, el último escaño se repartió con el equivalente al 2,5 % del voto.",
    en: "With the 2023 votes, the legal minimum of 3% did not change a single seat. What decides how many votes it takes is how many deputies each province elects: in Soria, a list with 19.1% was left out; in Madrid, the last seat went for the equivalent of 2.5% of the vote.",
  },
  published: "2026-11-23",
  lens: "dentro",
  theme: "elecciones",
  body: [
    p("La regla D'Hondt es una división. En cada provincia, los votos de cada candidatura que supera el 3 % del voto válido se dividen entre 1, 2, 3 y así hasta el número de diputados en juego, y los escaños van a los cocientes más altos. Cada provincia elige al menos dos diputados, Ceuta y Melilla uno cada una, y el resto se reparte según la población (artículos 162 y 163 de la LOREG). Aplicada a los votos de julio de 2023, esta regla reproduce los 350 escaños oficiales en las 52 circunscripciones.", "The D'Hondt rule is a division. In each province, the votes of every list that passes 3% of the valid vote are divided by 1, 2, 3 and so on up to the number of deputies at stake, and the seats go to the highest quotients. Each province elects at least two deputies, Ceuta and Melilla one each, and the rest are shared out by population (Articles 162 and 163 of the electoral law, LOREG). Applied to the July 2023 votes, this rule reproduces the 350 official seats in all 52 constituencies."),
    p("El 3 % solo puede pesar donde se elige a muchos diputados. En Madrid, el último de los 37 escaños se adjudicó con un cociente equivalente al 2,5 % del voto válido, y en Barcelona, al 2,8 %; en Valencia, la tercera provincia más grande, ya hacía falta el 5,6 %. En 2023 ninguna candidatura quedó entre esas cifras y el 3 %: sin el mínimo legal, el reparto habría sido el mismo en todas las provincias.", "The 3% only matters where many deputies are elected. In Madrid, the last of the 37 seats was awarded with a quotient equivalent to 2.5% of the valid vote, and in Barcelona to 2.8%; in Valencia, the third-largest province, 5.6% was already needed. In 2023 no list fell between those figures and 3%: without the legal minimum, the allocation would have been the same in every province."),
    { fig: "n07-barrera-real", code: "1" },
    p("El tamaño de la provincia también decide cuánto se parece el reparto a los votos. En las 9 provincias que eligieron 2 o 3 diputados, las candidaturas más votadas en cada una sumaron el 40,2 % de los votos y se llevaron el 61,5 % de los escaños; en Madrid, Barcelona y Valencia, el 37,6 % de los votos y el 41,2 % de los escaños. En el conjunto de España, el índice de desproporcionalidad de Gallagher, que valdría 0 si los escaños siguieran exactamente a los votos, fue de 5,8.", "Province size also decides how closely the allocation resembles the votes. In the 9 provinces that elected 2 or 3 deputies, the lists that came first in each one had 40.2% of the votes between them and took 61.5% of the seats; in Madrid, Barcelona and Valencia, 37.6% of the votes and 41.2% of the seats. Across Spain as a whole, the Gallagher disproportionality index, which would be 0 if seats followed votes exactly, was 5.8."),
    { fig: "n07-desproporcion", code: "2" },
    p("Lo que no dicen estos datos. Recalcular el reparto con otras reglas no dice qué habría pasado: con otro sistema, votantes y partidos se comportan de otra manera. El 29 de noviembre el reparto cambia un poco: Madrid elige 38 diputados y Cádiz 8, uno más y uno menos que en 2023. Cuántos votos costó cada escaño a cada partido está en la nota sobre el coste de un escaño.", "What this data does not say. Recalculating the allocation with other rules does not say what would have happened: under another system, voters and parties behave differently. On 29 November the allocation changes slightly: Madrid elects 38 deputies and Cádiz 8, one more and one fewer than in 2023. How many votes each seat cost each party is in the note on the cost of a seat."),
    { see: { es: "En 2023 un escaño costó menos de 65.000 votos al PP y al PSOE y más de 90.000 a Vox y a Sumar", en: "In 2023 a seat cost the PP and the PSOE fewer than 65,000 votes and Vox and Sumar more than 90,000" }, href: "/notas/cuanto-cuesta-un-escano/" },
    { see: { es: "Elecciones generales del 29N", en: "29 November general election" }, href: "/elecciones-29n/" },
  ],
  sources: [
    { name: { es: "Ley Orgánica 5/1985, del Régimen Electoral General, artículos 162 y 163 (reparto de escaños)", en: "Organic Law 5/1985 on the General Electoral System, Articles 162 and 163 (seat allocation)" }, url: "https://www.boe.es/buscar/act.php?id=BOE-A-1985-11672" },
  ],
};

export default note;
