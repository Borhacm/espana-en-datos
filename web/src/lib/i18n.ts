// Textos fijos de la interfaz y rutas. Español en la raíz (/temas/...) e inglés bajo /en/ (/en/themes/...).
// Los contenidos usan el tipo Bi ({ es, en }): una pieza no se publica sin sus dos versiones.
export type Lang = "es" | "en";
export const LANGS: Lang[] = ["es", "en"];

export const ui = {
  es: {
    siteName: "España en datos",
    siteDescription:
      "España contada con datos abiertos: economía, vivienda, empleo, política y territorio, comparados con Europa y entre comunidades.",
    navElections: "Elecciones 29N",
    navCongress: "Congreso",
    navThemes: "Temas",
    navNotes: "Notas",
    navLenses: "Miradas",
    navMethod: "Metodología",
    navLabel: "Principal",
    otherLang: "English",
    otherLangLabel: "Read this page in English",
    skip: "Saltar al contenido",
    source: "Fuente",
    license: "Licencia",
    notes: "Notas",
    showTable: "Ver los datos en una tabla",
    download: "Descargar los datos (JSON)",
    retrieved: "Datos descargados el",
    yourCountry: "Destacar una comunidad",
    none: "Ninguna",
    lens: "Mirada",
    loading: "Cargando el gráfico",
    loadError: "No se ha podido cargar el gráfico. Los datos siguen disponibles en la tabla.",
    footerIndependent:
      "Proyecto independiente de Bocal. No es una publicación oficial ni está vinculado a ningún partido, administración o empresa demoscópica.",
    footerData: "Datos abiertos del INE, Eurostat, el Ministerio del Interior, el Banco de España, el CIS y otras fuentes citadas en cada gráfico.",
    cookies: "Preferencias de cookies",
    comingSoon: "En preparación",
    seeAlso: "Ver también: ",
    vedaTitle: "Encuestas de intención de voto",
    vedaNote:
      "La ley electoral prohíbe publicar encuestas durante los cinco días anteriores a la votación. Este gráfico volverá a mostrarse cuando cierren los colegios electorales, el 29 de noviembre.",
    table: { country: "Territorio", year: "Año", value: "Valor" },
  },
  en: {
    siteName: "Spain in data",
    siteDescription:
      "Spain told with open data: the economy, housing, jobs, politics and the regions, compared with Europe and across regions.",
    navElections: "29 Nov election",
    navCongress: "Congress",
    navThemes: "Themes",
    navNotes: "Notes",
    navLenses: "Lenses",
    navMethod: "Methodology",
    navLabel: "Main",
    otherLang: "Español",
    otherLangLabel: "Leer esta página en español",
    skip: "Skip to content",
    source: "Source",
    license: "Licence",
    notes: "Notes",
    showTable: "Show the data as a table",
    download: "Download the data (JSON)",
    retrieved: "Data retrieved on",
    yourCountry: "Highlight a region",
    none: "None",
    lens: "Lens",
    loading: "Loading the chart",
    loadError: "The chart could not be loaded. The data is still available in the table.",
    footerIndependent:
      "An independent project by Bocal. Not an official publication, and not linked to any party, public body or polling company.",
    footerData: "Open data from INE (Spain's statistics office), Eurostat, the Ministry of the Interior, the Bank of Spain, the CIS and other sources cited in each chart.",
    cookies: "Cookie preferences",
    comingSoon: "In preparation",
    seeAlso: "See also: ",
    vedaTitle: "Voting intention polls",
    vedaNote:
      "Spanish electoral law bans publishing polls in the five days before the vote. This chart will be back when polling stations close on 29 November.",
    table: { country: "Area", year: "Year", value: "Value" },
  },
} as const;

export type Bi = { es: string; en: string };

export const paths = {
  home: { es: "/", en: "/en/" },
  elections: { es: "/elecciones-29n/", en: "/en/general-election/" },
  congress: { es: "/congreso/", en: "/en/congress/" },
  themes: { es: "/temas/", en: "/en/themes/" },
  notes: { es: "/notas/", en: "/en/notes/" },
  lenses: { es: "/miradas/", en: "/en/lenses/" },
  method: { es: "/metodologia/", en: "/en/methodology/" },
} as const;

export type Section = "home" | "elections" | "congress" | "themes" | "notes" | "lenses" | "method";

/** Rutas de un tema, una mirada o una nota en los dos idiomas, a partir de su slug. */
export const themePath = (slug: Bi): Bi => ({ es: `/${slug.es}/`, en: `/en/${slug.en}/` });
export const lensPath = (slug: Bi): Bi => ({ es: `/miradas/${slug.es}/`, en: `/en/lenses/${slug.en}/` });
export const notePath = (slug: Bi): Bi => ({ es: `/notas/${slug.es}/`, en: `/en/notes/${slug.en}/` });

export const locale = (lang: Lang) => (lang === "es" ? "es-ES" : "en-GB");

export function formatNumber(value: number, lang: Lang = "es", digits = 1): string {
  return new Intl.NumberFormat(locale(lang), { maximumFractionDigits: digits }).format(value);
}

export function formatDate(iso: string, lang: Lang = "es"): string {
  return new Intl.DateTimeFormat(locale(lang), { day: "numeric", month: "long", year: "numeric" }).format(new Date(iso));
}
