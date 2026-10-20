// Tipos de los contenidos (temas y notas). Los archivos de content/ importan de aquí.

/** Texto en los dos idiomas de la web. Una pieza no se publica sin su versión inglesa. */
export type Bi = { es: string; en: string };
/** Fuente citada: el nombre puede quedarse en el idioma original (títulos de leyes o informes) o traducirse */
export type Source = { name: string | Bi; url: string };
export type LensId = "europa" | "dentro" | "tiempo";
export type Block =
  | { p: Bi }
  /** Gráfico. `code` corto ("1") se prefija con el código de la pieza; uno completo ("N02-1") se muestra tal cual */
  | { fig: string; code: string }
  /** Subtítulo de sección (los análisis generan el índice con ellos) */
  | { h: Bi; id: string }
  /** Lista de puntos */
  | { list: Bi[] }
  /** Pasos numerados, para procedimientos */
  | { steps: { title: Bi; text: Bi }[] }
  /** Cita breve atribuida, con su fuente */
  | { quote: Bi; who: Bi; url: string }
  /** Cronología */
  | { timeline: { date: Bi; text: Bi }[] }
  /** Enlace a otra pieza publicada («Ver también») */
  | { see: Bi; href: string };

export interface Lens {
  id: LensId;
  slug: Bi;
  name: Bi;
  short: Bi;
  about: Bi;
}

export interface ThemeLens {
  lede: Bi;
  body: Block[];
}

export interface Theme {
  id: string;
  /** Prefijo de los códigos de gráfico (IA-G1, CO-G1...): identificador único y citable */
  code: string;
  slug: Bi;
  title: Bi;
  status: "published" | "upcoming";
  /** Especial con página propia (no usa la plantilla de tema ni la ruta /[tema]/) */
  hub?: boolean;
  dek?: Bi;
  published?: string;
  /** Fecha de la última revisión de una pieza publicada (se muestra junto a la de publicación) */
  updated?: string;
  /** Desempate si dos temas se publican el mismo día (menor = antes) */
  order?: number;
  lenses?: Record<LensId, ThemeLens>;
  /** Notas de otros temas que adelantaron este (se listan en la página del tema) */
  notes?: string[];
  /** Fuentes de las afirmaciones del texto que no salen de los gráficos (leyes, informes...) */
  sources?: Source[];
}

export interface Note {
  /** Identificador del calendario editorial, en minúsculas: "n01" */
  id: string;
  /** "analisis": pieza larga con secciones e índice. Por defecto, nota breve */
  kind?: "nota" | "analisis";
  /** Código visible y citable: "N01". Los gráficos se numeran N01-1, N01-2... */
  code: string;
  slug: Bi;
  title: Bi;
  dek: Bi;
  published: string;
  /** Mirada desde la que se cuenta */
  lens: LensId;
  /** Tema al que pertenece (id de un tema publicado) */
  theme: string;
  body: Block[];
  /** Fuentes de las afirmaciones del texto que no salen de los gráficos (leyes, informes...) */
  sources?: Source[];
}

/** Atajo para párrafos: primero el español, después el inglés */
export const p = (es: string, en: string): Block => ({ p: { es, en } });

/** Nombre de una fuente en el idioma de la página */
export const sourceName = (s: Source, lang: "es" | "en") => (typeof s.name === "string" ? s.name : s.name[lang]);
