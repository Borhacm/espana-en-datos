import { p, type Note } from "../../lib/content-types";

// Cifras comprobadas contra data/charts/n06-*.json y data/base/cis-problemas.json (barómetros del CIS).
// Tabla de verificación: editorial/registro/n06.md.
const note: Note = {
  id: "n06",
  code: "N06",
  slug: { es: "que-preocupa-cis", en: "what-worries-spaniards" },
  title: {
    es: "La vivienda es el problema más citado en el CIS desde enero de 2025; en 2023 lo eran la economía y el paro",
    en: "Housing has been the most-cited problem in the CIS since January 2025; in 2023 it was the economy and unemployment",
  },
  dek: {
    es: "En enero de 2023, el 3,4 % de los entrevistados por el CIS citaba la vivienda entre los tres principales problemas de España. En octubre de 2026 fue el 55,7 %. En el mismo tiempo han perdido peso la economía y el paro, los problemas más citados en 2023.",
    en: "In January 2023, 3.4% of those interviewed by the CIS named housing among Spain's three main problems. In October 2026 it was 55.7%. Over the same period the economy and unemployment, the most-cited problems in 2023, have lost ground.",
  },
  published: "2026-11-16",
  lens: "tiempo",
  theme: "elecciones",
  body: [
    p("Los partidos hacen campaña sobre lo que creen que preocupa a los votantes. Cada mes, el CIS pregunta a varios miles de personas cuáles son, a su juicio, los tres principales problemas de España, sin leerles ninguna lista, y agrupa las respuestas en categorías. Como cada entrevistado puede citar tres, los porcentajes suman más de 100.", "Parties campaign on what they think worries voters. Every month the CIS, Spain's public polling institute, asks several thousand people what in their opinion are Spain's three main problems, without reading them any list, and groups the answers into categories. As each respondent can name three, the percentages add up to more than 100."),
    p("En enero de 2023 citaba la vivienda el 3,4 %; en octubre de 2026, el 55,7 %, el valor más alto de los 38 barómetros analizados desde enero de 2023, y el 29,9 % la puso en primer lugar. En 2023 los más citados eran la economía (38,2 % de media) y el paro (28,6 %). La inmigración fue el problema más citado en septiembre y octubre de 2024 (30,4 % y 28,1 %).", "In January 2023, 3.4% named housing; in October 2026, 55.7%, the highest value in the 38 barometers analysed since January 2023, and 29.9% put it first. In 2023 the most cited were the economy (38.2% on average) and unemployment (28.6%). Immigration was the most-cited problem in September and October 2024 (30.4% and 28.1%)."),
    { fig: "n06-problemas-tiempo", code: "1" },
    p("En los tres últimos barómetros, la economía se queda en el 19,7 % y el paro en el 10,7 %. Entre los diez problemas más citados, cuatro tienen que ver con la política: el Gobierno y los partidos, la política en general, la corrupción y la conducta de los políticos.", "In the last three barometers, the economy stands at 19.7% and unemployment at 10.7%. Of the ten most-cited problems, four have to do with politics: the government and the parties, politics in general, corruption and politicians' conduct."),
    { fig: "n06-problemas-ranking", code: "2" },
    p("El orden cambia cuando el CIS pregunta por el problema que a cada uno le afecta personalmente. En esos tres barómetros, la vivienda (29,5 %) y la economía (28,8 %) casi empatan, la sanidad sube al 21,4 % y la inmigración baja al 11,6 %, frente al 21,3 % que la cita como problema de España.", "The order changes when the CIS asks about the problem that affects each person personally. In those three barometers, housing (29.5%) and the economy (28.8%) are almost level, healthcare rises to 21.4% and immigration falls to 11.6%, compared with the 21.3% who name it as a problem for Spain."),
    p("Lo que no dicen estos datos. Miden qué se menciona sin preguntar por nada concreto, no cuánto pesa cada problema en el voto ni qué solución prefiere cada uno. Las respuestas espontáneas pueden seguir lo que ocupa los medios ese mes, y diferencias de uno o dos puntos entre barómetros pueden deberse al azar de la muestra. Qué ha pasado con los precios y los alquileres está en el tema de vivienda.", "What this data does not say. It measures what people mention without being asked about anything specific, not how much each problem weighs in their vote or which solution each person prefers. Spontaneous answers may follow what fills the media that month, and differences of one or two points between barometers may be down to sampling chance. What has happened to prices and rents is in the housing topic."),
    { see: { es: "Vivienda: por qué es el tema de estas elecciones", en: "Housing: why it is the issue of this election" }, href: "/vivienda/" },
    { see: { es: "Elecciones generales del 29N", en: "29 November general election" }, href: "/elecciones-29n/" },
  ],
  sources: [
    { name: { es: "CIS, barómetro de octubre de 2026 (estudio 3582), marginales", en: "CIS, October 2026 barometer (study 3582), results tables" }, url: "https://www.cis.es/estudios/barometro-de-octubre-2026" },
  ],
};

export default note;
