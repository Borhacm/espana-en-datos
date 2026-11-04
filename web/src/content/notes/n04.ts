import { p, type Note } from "../../lib/content-types";

// Cifras comprobadas contra data/charts/n04-*.json y data/base/generales-escanos.json (Wikipedia, comprobado con la
// leyenda de escaños de cada artículo y, en 2023, con Infoelectoral). Tabla de verificación: editorial/registro/n04.md.
const note: Note = {
  id: "n04",
  code: "N04",
  slug: { es: "congreso-fragmentado", en: "fragmented-congress" },
  title: {
    es: "El Congreso tuvo menos de tres partidos efectivos hasta 2011 y entre 3,4 y 4,9 desde 2015",
    en: "Congress had fewer than three effective parties until 2011 and between 3.4 and 4.9 since 2015",
  },
  dek: {
    es: "Entre 1977 y 2011 los dos partidos con más escaños sumaron siempre más del 80 % del Congreso y hubo cuatro mayorías absolutas. Desde 2015 ningún partido ha pasado de 137 diputados y los dos mayores se han quedado entre el 54,0 % y el 73,7 % de los escaños.",
    en: "Between 1977 and 2011 the two parties with most seats always held more than 80% of Congress, and there were four absolute majorities. Since 2015 no party has gone above 137 deputies and the two largest have held between 54.0% and 73.7% of the seats.",
  },
  published: "2026-11-04",
  lens: "tiempo",
  theme: "elecciones",
  body: [
    p("Para formar gobierno tras el 29 de noviembre, el candidato a la presidencia necesita 176 de los 350 diputados en la primera votación de investidura o, en la segunda, más votos a favor que en contra (artículo 99 de la Constitución). Cuántos partidos se reparten el Congreso decide con cuántos hay que pactar.", "To form a government after 29 November, the candidate for prime minister needs 176 of the 350 deputies in the first investiture vote or, in the second, more votes in favour than against (Article 99 of the Constitution). How many parties share Congress decides how many have to strike a deal."),
    p("El número efectivo de partidos resume ese reparto en una cifra: vale 2 si dos partidos tienen la mitad de los escaños cada uno, y sube cuanto más repartidos están. Entre 1977 y 2011 osciló entre 2,3 (1982 y 2008) y 2,9 (1977). En 2015 saltó a 4,5, con la entrada de Podemos (42 escaños) y Ciudadanos (40), y en abril de 2019 llegó al máximo de la serie, 4,9. En 2023 bajó a 3,4: la cifra más baja desde 2015, pero más alta que la de cualquier elección anterior.", "The effective number of parties sums up that split in a single figure: it equals 2 if two parties have half the seats each, and rises the more spread out they are. Between 1977 and 2011 it ranged between 2.3 (1982 and 2008) and 2.9 (1977). In 2015 it jumped to 4.5, with the arrival of Podemos (42 seats) and Ciudadanos (40), and in April 2019 it reached the highest value in the series, 4.9. In 2023 it fell to 3.4: the lowest figure since 2015, but higher than in any earlier election."),
    { fig: "n04-partidos-efectivos", code: "1" },
    p("La otra cara es el peso de los dos mayores. Hasta 2011 nunca bajaron del 80 % de los escaños (el mínimo fue el 80,6 % de 1989) y el tercer partido nunca tuvo más de 23 diputados; desde 2015, el tercero no ha bajado de 33. En las 11 generales entre 1977 y 2011 hubo cuatro mayorías absolutas: 1982, 1986, 2000 y 2011. Desde 2015 el partido con más escaños no ha pasado de 137, 39 menos de los 176 de la mayoría absoluta, y hubo dos repeticiones electorales, en 2016 y en noviembre de 2019.", "The other side is the weight of the two largest parties. Until 2011 they never fell below 80% of the seats (the lowest was 80.6% in 1989) and the third party never had more than 23 deputies; since 2015 the third has not fallen below 33. In the 11 general elections between 1977 and 2011 there were four absolute majorities: 1982, 1986, 2000 and 2011. Since 2015 the party with most seats has not gone above 137, 39 short of the 176 for an absolute majority, and there were two repeat elections, in 2016 and in November 2019."),
    { fig: "n04-dos-mayores", code: "2" },
    p("Con más partidos, cada votación depende de más socios. Cómo ha votado cada grupo en esta legislatura, y quién coincide con quién, está en la sección del Congreso.", "With more parties, every vote depends on more partners. How each group has voted in this parliament, and who votes with whom, is in the Congress section."),
    p("Lo que no dicen estos datos. Cuentan escaños, no votos: con circunscripciones provinciales, el reparto favorece a los partidos grandes, y en votos el Congreso de 2023 tendría 4,1 partidos efectivos en lugar de 3,4. Además, las candidaturas se cuentan como se presentaron: las confluencias de Podemos en Cataluña, Galicia y la Comunidad Valenciana de 2015 y 2016 van aparte; contadas con Podemos, el índice de esos años bajaría a 4,1 y 3,8, todavía por encima de cualquier elección hasta 2011.", "What this data does not say. It counts seats, not votes: with provincial constituencies, the allocation favours large parties, and in votes the 2023 Congress would have 4.1 effective parties instead of 3.4. Also, lists are counted as they stood: the Podemos alliances in Catalonia, Galicia and the Valencian Community in 2015 and 2016 are counted separately; counted with Podemos, the index for those years would fall to 4.1 and 3.8, still above any election up to 2011."),
    { see: { es: "El Congreso en datos", en: "Congress in data" }, href: "/congreso/" },
    { see: { es: "Elecciones generales del 29N", en: "29 November general election" }, href: "/elecciones-29n/" },
  ],
  sources: [
    { name: { es: "Constitución Española, artículo 99 (investidura del presidente del Gobierno)", en: "Spanish Constitution, Article 99 (investiture of the prime minister)" }, url: "https://www.boe.es/buscar/act.php?id=BOE-A-1978-31229#a99" },
    { name: { es: "Ministerio del Interior, Infoelectoral: resultados de las elecciones al Congreso de julio de 2023 (votos por candidatura)", en: "Ministry of the Interior, Infoelectoral: results of the July 2023 election to Congress (votes by list)" }, url: "https://infoelectoral.interior.gob.es/opencms/es/elecciones-celebradas/area-de-descargas/" },
  ],
};

export default note;
