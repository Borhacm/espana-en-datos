import { p, type Note } from "../../lib/content-types";

// Cifras comprobadas contra data/charts/an01-*.json (votaciones nominales del Pleno, legislaturas X a XV, sin Presupuestos).
// Tabla de verificación: editorial/registro/an01.md.
const note: Note = {
  id: "an01",
  kind: "analisis",
  code: "AN01",
  slug: { es: "quince-anos-en-el-congreso", en: "fifteen-years-in-congress" },
  title: { es: "Quince años en el Congreso: de la mayoría absoluta a los decretos que caen", en: "Fifteen years in Congress: from an absolute majority to decrees that fall" },
  dek: {
    es: "Hemos analizado todas las votaciones nominales del Pleno desde 2012. Con mayoría absoluta, el PP ganó todas; el PSOE ha pasado de ganar el 99 % en 2021 al 76 % en 2026, y esta legislatura concentra 13 de los 16 decretos-ley derogados desde 2011.",
    en: "We have analysed every roll-call vote in the plenary since 2012. With an absolute majority, the PP won them all; the PSOE has gone from winning 99% in 2021 to 76% in 2026, and this parliament accounts for 13 of the 16 decree-laws struck down since 2011.",
  },
  published: "2026-10-07",
  lens: "tiempo",
  theme: "congreso",
  body: [
    p("El Congreso vota miles de veces en cada legislatura: leyes, enmiendas, decretos, mociones. Cada votación nominal queda registrada con el voto de cada diputado. Con esos datos, que el Congreso publica en abierto desde la legislatura que empezó en 2011, se puede ver cómo ha cambiado la forma de gobernar. Para que no pesen más que todo lo demás, dejamos fuera las votaciones de Presupuestos, que en algunos años son miles de enmiendas.", "Congress votes thousands of times in each parliament: laws, amendments, decrees, motions. Each roll-call vote is recorded with every deputy's vote. With that data, which Congress has published openly since the parliament that began in 2011, you can see how the way of governing has changed. So that they do not outweigh everything else, we leave out the budget votes, which in some years run to thousands of amendments."),

    { h: { es: "Del rodillo a la geometría variable", en: "From steamroller to shifting alliances" }, id: "gobierno" },
    p("Entre 2012 y 2015, con mayoría absoluta, el PP ganó todas las votaciones del Pleno: lo que votaba salía. En la legislatura siguiente, ya en minoría, ganó el 82 % en 2016, el 73 % en 2017 y el 58 % en los primeros meses de 2018, hasta la moción de censura de junio.", "Between 2012 and 2015, with an absolute majority, the PP won every vote in the plenary: whatever it voted for passed. In the next parliament, now in a minority, it won 82% in 2016, 73% in 2017 and 58% in the first months of 2018, until the motion of no confidence in June."),
    p("El PSOE, en coalición y con apoyos externos, ganó entre el 97 % y el 99 % de las votaciones de cada año entre 2020 y 2023. En esta legislatura la cifra ha caído cada año: el 88 % en 2024, el 84 % en 2025 y el 76 % en lo que va de 2026.", "The PSOE, in coalition and with outside support, won between 97% and 99% of the votes each year between 2020 and 2023. In this parliament the figure has fallen every year: 88% in 2024, 84% in 2025 and 76% so far in 2026."),
    { fig: "an01-gobierno-gana", code: "1" },

    { h: { es: "Los decretos que caen", en: "The decrees that fall" }, id: "decretos" },
    p("Un decreto-ley necesita que el Congreso lo convalide en un mes. Desde 2011 se han derogado 16. Ninguno entre 2011 y 2015, con 71 decretos convalidados; 2 en la legislatura de 2016 a 2019 y 1 en la de 2019 a 2023, que votó 96. En la que ahora termina se han derogado 13 de 56, contando los dos decretos de alquiler del 2 de octubre de 2026.", "A decree-law needs Congress to validate it within a month. Since 2011, 16 have been struck down. None between 2011 and 2015, with 71 decrees validated; 2 in the 2016 to 2019 parliament and 1 in the 2019 to 2023 parliament, which voted on 96. In the one now ending, 13 of 56 have been struck down, counting the two rental decrees of 2 October 2026."),
    { fig: "an01-decretos", code: "2" },

    { h: { es: "PP y PSOE: menos acuerdo que nunca desde 2015", en: "PP and PSOE: less agreement than at any time since 2015" }, id: "pp-psoe" },
    p("PP y PSOE han votado lo mismo en el 30 % de las votaciones de 2013 y 2014, el mínimo de la serie, y en el 61 % de las de 2016, el máximo, un año de Gobierno en funciones y elecciones repetidas. Desde 2024 coinciden en torno al 38 % y el 39 % de las votaciones de cada año: el nivel más bajo desde 2015.", "PP and PSOE voted the same way in 30% of the votes in 2013 and 2014, the lowest in the series, and in 61% of those in 2016, the highest, a year of caretaker government and repeat elections. Since 2024 they have agreed in around 38% to 39% of each year's votes: the lowest level since 2015."),
    { fig: "an01-pp-psoe", code: "3" },

    { h: { es: "Con quién vota cada Gobierno", en: "Who each government votes with" }, id: "socios" },
    p("Con mayoría absoluta, el PP no necesitaba socios, y ningún grupo votó con él en más del 36 % de las votaciones (UPyD fue el que más; el PSOE, el 34 %). En minoría, entre 2016 y 2018, su apoyo principal fue Ciudadanos (66 %), seguido del PSOE (51 %) y el PNV (47 %).", "With an absolute majority, the PP did not need partners, and no group voted with it in more than 36% of the votes (UPyD was the one that did most; the PSOE, 34%). In a minority, between 2016 and 2018, its main support was Ciudadanos (66%), followed by the PSOE (51%) and the PNV (47%)."),
    p("El PSOE de 2020 a 2023 tuvo en Unidas Podemos, su socio de coalición, a quien más coincidía con él (86 %), y después al PNV (57 %) y EH Bildu (52 %). En esta legislatura, Sumar ha votado con el PSOE en el 83 % de las votaciones, el PNV y Coalición Canaria en el 75 %. En esta legislatura el Grupo Mixto se separa por partido; la columna «Mixto (otros)» reúne a los pocos diputados del Mixto que no son de Podemos, BNG, CC, UPN ni Compromís, y no es comparable con un partido.", "From 2020 to 2023 the PSOE's closest match was Unidas Podemos, its coalition partner (86%), followed by the PNV (57%) and EH Bildu (52%). In this parliament, Sumar has voted with the PSOE in 83% of the votes, and the PNV and Coalición Canaria in 75%. In this parliament the Mixed Group is split by party; the «Mixto (otros)» column groups the few Mixed Group deputies who do not belong to Podemos, BNG, CC, UPN or Compromís, and it is not comparable with a party."),
    p("Con los gobiernos del PSOE, el PP votó lo mismo que el PSOE en el 45 % de las votaciones de 2018 a 2019, en el 51 % de 2020 a 2023 y en el 39 % de esta legislatura, la cifra más baja de las tres.", "Under PSOE governments, the PP voted the same way as the PSOE in 45% of the votes from 2018 to 2019, in 51% from 2020 to 2023 and in 39% in this parliament, the lowest of the three."),
    { fig: "an01-socios", code: "4" },

    { h: { es: "Lo que estos datos no dicen", en: "What this data does not say" }, id: "limites" },
    { list: [
      { es: "Cada votación pesa lo mismo: una moción sin efectos legales cuenta igual que una ley. Sirven para ver tendencias, no para medir la importancia de lo que se votó.", en: "Every vote carries the same weight: a motion with no legal effect counts the same as a law. The figures show trends, not the importance of what was voted on." },
      { es: "Ganar una votación no es aprobar una ley: también gana quien vota no a algo que no sale adelante.", en: "Winning a vote is not the same as passing a law: a party that votes no to something that fails also wins." },
      { es: "Los grupos Mixto y Plural reúnen partidos distintos; fuera de esta legislatura cuentan como un solo grupo.", en: "The Mixed and Plural groups bring together different parties; outside this parliament they count as a single group." },
      { es: "Las legislaturas de 2016 y 2019 fueron muy breves y apenas tienen votaciones.", en: "The 2016 and 2019 parliaments were very short and have hardly any votes." },
    ] },
    p("Todos los datos se pueden explorar por legislatura, tipo de votación y partido en El Congreso en datos.", "All the data can be explored by parliament, type of vote and party in Congress in data."),
  ],
  sources: [
    { name: { es: "Congreso de los Diputados, datos abiertos de votaciones", en: "Congress of Deputies, open data on votes" }, url: "https://www.congreso.es/es/opendata/votaciones" },
    { name: { es: "BOE: convalidación del Real Decreto-ley 14/2021 (empate repetido)", en: "BOE (official gazette): validation of Royal Decree-law 14/2021 (repeated tie)" }, url: "https://www.boe.es/buscar/doc.php?id=BOE-A-2021-12605" },
    { name: { es: "Ministerio de la Presidencia: convalidación del Real Decreto-ley 8/2023 (empate repetido)", en: "Ministry of the Presidency: validation of Royal Decree-law 8/2023 (repeated tie)" }, url: "https://www.mpr.gob.es/prencom/notas/Paginas/2024/100124-aprobados-decretos-leyes-prorroga-medidas.aspx" },
    { name: { es: "El Congreso en datos: explorador de votaciones", en: "Congress in data: vote explorer" }, url: "/congreso/#explorador" },
  ],
};

export default note;
