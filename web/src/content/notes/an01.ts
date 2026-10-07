import { p, type Note } from "../../lib/content-types";

// Cifras comprobadas contra data/charts/an01-*.json (votaciones nominales del Pleno, legislaturas X a XV, sin Presupuestos).
// Tabla de verificación: editorial/registro/an01.md.
const note: Note = {
  id: "an01",
  kind: "analisis",
  code: "AN01",
  slug: { es: "quince-anos-en-el-congreso" },
  title: { es: "Quince años en el Congreso: de la mayoría absoluta a los decretos que caen" },
  dek: {
    es: "Hemos analizado todas las votaciones nominales del Pleno desde 2012. Con mayoría absoluta, el PP ganó todas; el PSOE ha pasado de ganar el 99 % en 2021 al 76 % en 2026, y esta legislatura concentra 13 de los 16 decretos-ley derogados desde 2011.",
  },
  published: "2026-10-07",
  lens: "tiempo",
  theme: "congreso",
  body: [
    p("El Congreso vota miles de veces en cada legislatura: leyes, enmiendas, decretos, mociones. Cada votación nominal queda registrada con el voto de cada diputado. Con esos datos, que el Congreso publica en abierto desde la legislatura que empezó en 2011, se puede ver cómo ha cambiado la forma de gobernar. Para que no pesen más que todo lo demás, dejamos fuera las votaciones de Presupuestos, que en algunos años son miles de enmiendas."),

    { h: { es: "Del rodillo a la geometría variable" }, id: "gobierno" },
    p("Entre 2012 y 2015, con mayoría absoluta, el PP ganó todas las votaciones del Pleno: lo que votaba salía. En la legislatura siguiente, ya en minoría, ganó el 82 % en 2016, el 73 % en 2017 y el 58 % en los primeros meses de 2018, hasta la moción de censura de junio."),
    p("El PSOE, en coalición y con apoyos externos, ganó entre el 97 % y el 99 % de las votaciones de cada año entre 2020 y 2023. En esta legislatura la cifra ha caído cada año: el 88 % en 2024, el 84 % en 2025 y el 76 % en lo que va de 2026."),
    { fig: "an01-gobierno-gana", code: "1" },

    { h: { es: "Los decretos que caen" }, id: "decretos" },
    p("Un decreto-ley necesita que el Congreso lo convalide en un mes. Desde 2011 se han derogado 16. Ninguno entre 2011 y 2015, con 71 decretos convalidados; 2 en la legislatura de 2016 a 2019 y 1 en la de 2019 a 2023, que votó 96. En la que ahora termina se han derogado 13 de 56, contando los dos decretos de alquiler del 2 de octubre de 2026."),
    { fig: "an01-decretos", code: "2" },

    { h: { es: "PP y PSOE: menos acuerdo que nunca desde 2015" }, id: "pp-psoe" },
    p("PP y PSOE han votado lo mismo en el 30 % de las votaciones de 2013 y 2014, el mínimo de la serie, y en el 61 % de las de 2016, el máximo, un año de Gobierno en funciones y elecciones repetidas. Desde 2024 coinciden en torno al 38 % y el 39 % de las votaciones de cada año: el nivel más bajo desde 2015."),
    { fig: "an01-pp-psoe", code: "3" },

    { h: { es: "Con quién vota cada Gobierno" }, id: "socios" },
    p("Con mayoría absoluta, el PP no necesitaba socios, y ningún grupo votó con él en más del 36 % de las votaciones (UPyD fue el que más). En minoría, entre 2016 y 2018, su apoyo principal fue Ciudadanos (66 %), seguido del PNV (47 %)."),
    p("El PSOE de 2020 a 2023 tuvo en Unidas Podemos, su socio de coalición, a quien más coincidía con él (86 %), y después al PNV (57 %) y EH Bildu (52 %). En esta legislatura, Sumar ha votado con el PSOE en el 83 % de las votaciones, el PNV y Coalición Canaria en el 75 %. En esta legislatura el Grupo Mixto se separa por partido; la columna «Mixto (otros)» reúne a los pocos diputados del Mixto que no son de Podemos, BNG, CC, UPN ni Compromís, y no es comparable con un partido."),
    { fig: "an01-socios", code: "4" },

    { h: { es: "Lo que estos datos no dicen" }, id: "limites" },
    { list: [
      { es: "Cada votación pesa lo mismo: una moción sin efectos legales cuenta igual que una ley. Sirven para ver tendencias, no para medir la importancia de lo que se votó." },
      { es: "Ganar una votación no es aprobar una ley: también gana quien vota no a algo que no sale adelante." },
      { es: "Los grupos Mixto y Plural reúnen partidos distintos; fuera de esta legislatura cuentan como un solo grupo." },
      { es: "Las legislaturas de 2016 y 2019 fueron muy breves y apenas tienen votaciones." },
    ] },
    p("Todos los datos se pueden explorar por legislatura, tipo de votación y partido en El Congreso en datos."),
  ],
  sources: [
    { name: "Congreso de los Diputados, datos abiertos de votaciones", url: "https://www.congreso.es/es/opendata/votaciones" },
    { name: "BOE: convalidación del Real Decreto-ley 14/2021 (empate repetido)", url: "https://www.boe.es/buscar/doc.php?id=BOE-A-2021-12605" },
    { name: "Ministerio de la Presidencia: convalidación del Real Decreto-ley 8/2023 (empate repetido)", url: "https://www.mpr.gob.es/prencom/notas/Paginas/2024/100124-aprobados-decretos-leyes-prorroga-medidas.aspx" },
    { name: "El Congreso en datos: explorador de votaciones", url: "/congreso/#explorador" },
  ],
};

export default note;
