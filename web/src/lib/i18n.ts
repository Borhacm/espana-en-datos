// Textos fijos de la interfaz y rutas. La web está solo en español; los contenidos usan el tipo Bi
// ({ es }) para poder añadir otro idioma más adelante sin tocar cada archivo.
export type Lang = "es";
export const LANGS: Lang[] = ["es"];

export const ui = {
  es: {
    siteName: "España en datos",
    siteDescription:
      "España contada con datos abiertos: economía, vivienda, empleo, política y territorio, comparados con Europa y entre comunidades.",
    navElections: "Elecciones 29N",
    navThemes: "Temas",
    navNotes: "Notas",
    navLenses: "Miradas",
    navMethod: "Metodología",
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
    comingSoon: "En preparación",
    table: { country: "Territorio", year: "Año", value: "Valor" },
  },
} as const;

export type Bi = { es: string };

export const paths = {
  home: { es: "/" },
  elections: { es: "/elecciones-29n/" },
  themes: { es: "/temas/" },
  notes: { es: "/notas/" },
  lenses: { es: "/miradas/" },
  method: { es: "/metodologia/" },
} as const;

export type Section = "home" | "elections" | "themes" | "notes" | "lenses" | "method";

/** Rutas de un tema, una mirada o una nota a partir de su slug. */
export const themePath = (slug: Bi): Bi => ({ es: `/${slug.es}/` });
export const lensPath = (slug: Bi): Bi => ({ es: `/miradas/${slug.es}/` });
export const notePath = (slug: Bi): Bi => ({ es: `/notas/${slug.es}/` });

export function formatNumber(value: number, _lang: Lang = "es", digits = 1): string {
  return new Intl.NumberFormat("es-ES", { maximumFractionDigits: digits }).format(value);
}

export function formatDate(iso: string, _lang: Lang = "es"): string {
  return new Intl.DateTimeFormat("es-ES", { day: "numeric", month: "long", year: "numeric" }).format(new Date(iso));
}
