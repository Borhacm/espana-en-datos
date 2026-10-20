import { p, type Note } from "../../lib/content-types";

// Cifras comprobadas contra data/charts/n01-*.json, data/charts/el2-gobiernos.json, data/charts/el3-mapa-2023.json y data/base/escanos-2026.json.
// Tabla de verificación: editorial/registro/n01.md.
const note: Note = {
  id: "n01",
  code: "N01",
  slug: { es: "quien-gobierna-donde-29n", en: "who-governs-where-29-november" },
  title: { es: "Andalucía, Cataluña y Madrid eligen 146 de los 350 diputados: quién gobierna dónde y cuánto pesa cada comunidad", en: "Andalusia, Catalonia and Madrid elect 146 of the 350 deputies: who governs where and how much each region weighs" },
  dek: {
    es: "El 29N se reparten 350 escaños por provincias. Tres comunidades eligen el 41,7 % del Congreso, el PP preside 11 de las 17 y un diputado de Castilla y León representa a menos de la mitad de habitantes que uno de Madrid.",
    en: "On 29 November, 350 seats are allocated by province. Three regions elect 41.7% of Congress, the PP holds the presidency of 11 of the 17, and a deputy from Castile and León represents fewer than half as many people as one from Madrid.",
  },
  published: "2026-10-12",
  lens: "dentro",
  theme: "elecciones",
  body: [
    p("El 29 de noviembre se eligen 350 diputados, repartidos por provincias. Sumados por comunidades, Andalucía elige 60, Cataluña 48 y Madrid 38: 146 en total, el 41,7 % del Congreso. En el otro extremo, La Rioja elige 4, y Ceuta y Melilla, uno cada una. Respecto a 2023 solo cambia un escaño, según el decreto de convocatoria: Cádiz pasa de 9 a 8 y Madrid, de 37 a 38.", "On 29 November, 350 deputies are elected, allocated by province. Added up by region, Andalusia elects 60, Catalonia 48 and Madrid 38: 146 in total, 41.7% of Congress. At the other end, La Rioja elects 4, and Ceuta and Melilla one each. Compared with 2023 only one seat changes, according to the decree calling the election: Cádiz goes from 9 to 8 and Madrid from 37 to 38."),
    { fig: "n01-escanos-ccaa", code: "1" },
    p("Hoy el PP preside 11 de las 17 comunidades, además de Ceuta y Melilla; el PSOE, 3, y el PSC, Cataluña; el PNV, el País Vasco, y Coalición Canaria, Canarias. Las comunidades presididas por el PP eligen 234 diputados; las del PSOE y el PSC, 81; el País Vasco, 18, y Canarias, 15. Son elecciones distintas: quién gobierna una comunidad no dice cómo votarán sus electores en las generales.", "Today the PP holds the presidency of 11 of the 17 regions, as well as Ceuta and Melilla; the PSOE, 3, and the PSC, Catalonia; the PNV, the Basque Country; and Coalición Canaria, the Canary Islands. The regions with a PP president elect 234 deputies; those of the PSOE and the PSC, 81; the Basque Country, 18; and the Canary Islands, 15. These are different elections: who governs a region does not say how its voters will vote in the general election."),
    { fig: "el2-gobiernos", code: "EL-3" },
    p("En 2023, el PP fue el partido con más escaños en 9 comunidades y el PSOE en 2, Cataluña y Navarra. PP y PSOE empataron en 5 (Baleares, Canarias, Cantabria, Extremadura y La Rioja), y en el País Vasco EH Bildu, PNV y PSOE sacaron 5 escaños cada uno.", "In 2023, the PP was the party with the most seats in 9 regions and the PSOE in 2, Catalonia and Navarre. PP and PSOE tied in 5 (the Balearic Islands, the Canary Islands, Cantabria, Extremadura and La Rioja), and in the Basque Country EH Bildu, PNV and PSOE won 5 seats each."),
    p("No todos los escaños cuestan lo mismo. Cada provincia tiene dos fijos, así que las menos pobladas eligen más diputados por habitante: en Castilla y León hay uno por cada 77.371 habitantes y en Madrid, uno por cada 187.817, 2,4 veces más. La media de España es de 140.327. Por provincias, el extremo es Soria, con un diputado por cada 45.117 habitantes.", "Not every seat costs the same. Each province has two fixed seats, so the least populated ones elect more deputies per inhabitant: in Castile and León there is one for every 77,371 inhabitants and in Madrid one for every 187,817, 2.4 times more. The Spanish average is 140,327. By province, the extreme is Soria, with one deputy for every 45,117 inhabitants."),
    { fig: "n01-habitantes-escano", code: "2" },
    p("Qué se juega en el mapa. Los datos dibujan tres frentes para cualquier partido. Las tres grandes comunidades reparten 146 escaños en circunscripciones grandes, donde el resultado se parece más al porcentaje de voto. En el extremo contrario, 29 de las 52 circunscripciones eligen 5 diputados o menos: suman 108 escaños, el 30,9 % del Congreso, con el 20,7 % de la población. Ahí el reparto favorece a los partidos más votados y pocos votos pueden mover un escaño. Y las 5 comunidades donde PP y PSOE empataron en 2023 eligen 41 diputados: es el terreno donde un cambio pequeño se nota más en el recuento final.", "What is at stake on the map. The data sketches three fronts for any party. The three big regions share out 146 seats in large constituencies, where the result tracks the vote share more closely. At the other end, 29 of the 52 constituencies elect 5 deputies or fewer: together they have 108 seats, 30.9% of Congress, with 20.7% of the population. There the allocation favours the parties with the most votes and a few votes can move a seat. And the 5 regions where PP and PSOE tied in 2023 elect 41 deputies: that is where a small shift shows most in the final count."),
    p("En el especial de las elecciones se puede ver quién ha gobernado cada comunidad desde 1980 y probar el reparto de escaños con el simulador.", "In the election special you can see who has governed each region since 1980 and try out the seat allocation with the simulator."),
  ],
  sources: [
    { name: { es: "BOE, Real Decreto 806/2026 de convocatoria de elecciones (diputados por circunscripción)", en: "BOE (official gazette), Royal Decree 806/2026 calling the election (deputies per constituency)" }, url: "https://www.boe.es/buscar/doc.php?id=BOE-A-2026-20742" },
    { name: { es: "Ministerio del Interior, resultados de las elecciones al Congreso de 2023", en: "Ministry of the Interior, results of the 2023 Congress election" }, url: "https://infoelectoral.interior.gob.es/opencms/es/elecciones-celebradas/area-de-descargas/" },
  ],
};

export default note;
