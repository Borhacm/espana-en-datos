import { p, type Note } from "../../lib/content-types";

// Cifras comprobadas contra data/charts/n01-*.json, data/charts/el2-gobiernos.json, data/charts/el3-mapa-2023.json y data/base/escanos-2026.json.
// Tabla de verificación: editorial/registro/n01.md.
const note: Note = {
  id: "n01",
  code: "N01",
  slug: { es: "quien-gobierna-donde-29n" },
  title: { es: "Andalucía, Cataluña y Madrid eligen 146 de los 350 diputados: quién gobierna dónde y cuánto pesa cada comunidad" },
  dek: {
    es: "El 29N se reparten 350 escaños por provincias. Tres comunidades eligen el 41,7 % del Congreso, el PP preside 11 de las 17 y un diputado de Castilla y León representa a menos de la mitad de habitantes que uno de Madrid.",
  },
  published: "2026-10-12",
  lens: "dentro",
  theme: "elecciones",
  body: [
    p("El 29 de noviembre se eligen 350 diputados, repartidos por provincias. Sumados por comunidades, Andalucía elige 60, Cataluña 48 y Madrid 38: 146 en total, el 41,7 % del Congreso. En el otro extremo, La Rioja elige 4, y Ceuta y Melilla, uno cada una. Respecto a 2023 solo cambia un escaño, según el decreto de convocatoria: Cádiz pasa de 9 a 8 y Madrid, de 37 a 38."),
    { fig: "n01-escanos-ccaa", code: "1" },
    p("Hoy el PP preside 11 de las 17 comunidades, además de Ceuta y Melilla; el PSOE, 3, y el PSC, Cataluña; el PNV, el País Vasco, y Coalición Canaria, Canarias. Las comunidades presididas por el PP eligen 234 diputados; las del PSOE y el PSC, 81; el País Vasco, 18, y Canarias, 15. Son elecciones distintas: quién gobierna una comunidad no dice cómo votarán sus electores en las generales."),
    { fig: "el2-gobiernos", code: "EL-3" },
    p("En 2023, el PP fue el partido con más escaños en 9 comunidades y el PSOE en 2, Cataluña y Navarra. PP y PSOE empataron en 5 (Baleares, Canarias, Cantabria, Extremadura y La Rioja), y en el País Vasco EH Bildu, PNV y PSOE sacaron 5 escaños cada uno."),
    p("No todos los escaños cuestan lo mismo. Cada provincia tiene dos fijos, así que las menos pobladas eligen más diputados por habitante: en Castilla y León hay uno por cada 77.371 habitantes y en Madrid, uno por cada 187.817, 2,4 veces más. La media de España es de 140.327. Por provincias, el extremo es Soria, con un diputado por cada 45.117 habitantes."),
    { fig: "n01-habitantes-escano", code: "2" },
    p("En el especial de las elecciones se puede ver quién ha gobernado cada comunidad desde 1980 y probar el reparto de escaños con el simulador."),
  ],
  sources: [
    { name: "BOE, Real Decreto 806/2026 de convocatoria de elecciones (diputados por circunscripción)", url: "https://www.boe.es/buscar/doc.php?id=BOE-A-2026-20742" },
    { name: "Ministerio del Interior, resultados de las elecciones al Congreso de 2023", url: "https://infoelectoral.interior.gob.es/opencms/es/elecciones-celebradas/area-de-descargas/" },
  ],
};

export default note;
