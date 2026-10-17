import { p, type Theme } from "../../lib/content-types";

// Especial de las generales del 29N. Tiene página propia (views/Elections.astro), no la plantilla de tema.
// Los textos no repiten cifras que cambian cada semana: esas van en el título de cada gráfico, que genera el pipeline.
// Cifras de 2023 comprobadas contra data/charts/el3-mapa-2023.json (Infoelectoral).
const theme: Theme = {
  id: "elecciones",
  code: "EL",
  slug: { es: "elecciones-29n" },
  title: { es: "Elecciones generales del 29N" },
  status: "published",
  hub: true,
  dek: {
    es: "Encuestas, resultados de 2023 y quién gobierna en cada comunidad, actualizados hasta el día de la votación. Con la metodología a la vista.",
  },
  published: "2026-10-11",
  lenses: {
    tiempo: {
      lede: { es: "Cómo ha cambiado la intención de voto desde las elecciones de julio de 2023." },
      body: [
        p("Cada punto es una encuesta publicada; la línea es nuestra media. La media da más peso a las encuestas recientes y a las de muestra grande, y cuenta cada empresa una sola vez por semana para que las que publican más a menudo no dominen. Los paneles online sin muestreo probabilístico y las encuestas encargadas por partidos aparecen, pero no entran en la media."),
        { fig: "el1-encuestas", code: "1" },
        p("Una encuesta no es una predicción. Mide la intención declarada en unos días concretos, con un margen de error de entre dos y tres puntos para una muestra de mil entrevistas, y cada empresa corrige sus datos con su propio método. Por eso las encuestas difieren entre sí y por eso conviene mirar la media antes que una cifra suelta."),
      ],
    },
    dentro: {
      lede: { es: "De dónde parte cada partido y qué territorio gobierna." },
      body: [
        p("En 2023 el PP fue el más votado en 40 de las 52 provincias. El PSOE ganó en 10: las cuatro catalanas, Badajoz, Cáceres, Sevilla, Las Palmas, Navarra y Álava. El PNV ganó en Bizkaia y EH Bildu, en Gipuzkoa."),
        p("Por municipios el mapa cambia: el PSOE ganó en más municipios que el PP en Andalucía, Extremadura, Cataluña y Asturias, y EH Bildu fue la fuerza más votada en más municipios que nadie en el País Vasco y Navarra. Cambia a la vista por municipios para ver el detalle."),
        { fig: "el3-mapa-2023", code: "2" },
        p("Las generales no eligen a los gobiernos autonómicos, pero el reparto territorial del poder condiciona la campaña: quién gobierna cada comunidad decide buena parte de la sanidad, la educación y la vivienda que los votantes tienen en mente."),
        { fig: "el2-gobiernos", code: "3" },
      ],
    },
    europa: { lede: { es: "" }, body: [] },
  },
  sources: [
    { name: "LOREG, artículo 69 (encuestas electorales)", url: "https://www.boe.es/buscar/act.php?id=BOE-A-1985-11672#a69" },
  ],
};

export default theme;
