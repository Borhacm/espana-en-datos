// Registro de temas, notas y miradas. Todas las páginas salen de aquí.
// Cada tema vive en content/themes/<id>.ts y cada nota en content/notes/<id>.ts:
// para publicar uno nuevo basta con añadir su archivo.
import { lensPath, notePath, paths, themePath, type Lang } from "./i18n";
import type { Bi, Lens, LensId, Note, Theme } from "./content-types";

export type { Bi, Block, Lens, LensId, Note, Theme, ThemeLens } from "./content-types";

export const LENSES: Lens[] = [
  {
    id: "europa",
    slug: { es: "espana-frente-a-europa", en: "spain-and-europe" },
    name: { es: "España frente a Europa", en: "Spain and Europe" },
    short: { es: "Dónde estamos respecto a la UE", en: "Where Spain stands in the EU" },
    about: {
      es: "Cómo se compara España con la media de la Unión Europea y con los países de su tamaño: Alemania, Francia, Italia y Portugal.",
      en: "How Spain compares with the European Union average and with countries of its size: Germany, France, Italy and Portugal.",
    },
  },
  {
    id: "dentro",
    slug: { es: "espana-por-dentro", en: "spain-from-within" },
    name: { es: "España por dentro", en: "Spain from within" },
    short: { es: "Las diferencias entre comunidades", en: "The differences between regions" },
    about: {
      es: "Las diferencias entre comunidades autónomas y provincias que esconde la media nacional, y quién gobierna en cada una.",
      en: "The differences between regions and provinces that the national average hides, and who governs each region.",
    },
  },
  {
    id: "tiempo",
    slug: { es: "espana-en-el-tiempo", en: "spain-over-time" },
    name: { es: "España en el tiempo", en: "Spain over time" },
    short: { es: "De dónde venimos", en: "Where we come from" },
    about: {
      es: "Cómo ha cambiado cada dato desde la crisis de 2008, la pandemia y el inicio de la legislatura en 2023.",
      en: "How each figure has changed since the 2008 crisis, the pandemic and the start of the current parliament in 2023.",
    },
  },
];

const byDate = <T extends { published?: string; order?: number; code: string }>(a: T, b: T) =>
  (a.published ?? "").localeCompare(b.published ?? "") || (a.order ?? 0) - (b.order ?? 0) || a.code.localeCompare(b.code);

const themeModules = import.meta.glob<{ default: Theme }>("../content/themes/*.ts", { eager: true });
const noteModules = import.meta.glob<{ default: Note }>("../content/notes/*.ts", { eager: true });

/** Temas en orden de publicación (el más antiguo primero) */
export const THEMES: Theme[] = Object.values(themeModules).map((m) => m.default).sort(byDate);
/** Notas, de la más reciente a la más antigua */
export const NOTES: Note[] = Object.values(noteModules).map((m) => m.default).sort(byDate).reverse();

/** Cada texto de un tema o una nota tiene que ir en los dos idiomas: si falta el inglés, el build falla en vez de publicar
 *  una página a medias. Los textos vacíos (miradas sin contenido de los especiales) se permiten si lo están en los dos. */
function checkBilingual(v: unknown, where: string): void {
  if (Array.isArray(v)) return v.forEach((x, i) => checkBilingual(x, `${where}[${i}]`));
  if (!v || typeof v !== "object") return;
  const o = v as Record<string, unknown>;
  if ("es" in o || "en" in o) {
    if (typeof o.es !== "string" || typeof o.en !== "string" || (o.es.trim() !== "") !== (o.en.trim() !== ""))
      throw new Error(`Falta el texto en inglés (o en español) en ${where}: ${JSON.stringify(o).slice(0, 160)}`);
    return;
  }
  for (const [k, x] of Object.entries(o)) checkBilingual(x, `${where}.${k}`);
}
for (const t of THEMES) checkBilingual(t, `tema ${t.id}`);
for (const n of NOTES) checkBilingual(n, `nota ${n.id}`);

export const published = () => THEMES.filter((t) => t.status === "published");
export const upcoming = () => THEMES.filter((t) => t.status === "upcoming");
export const themeById = (id: string) => THEMES.find((t) => t.id === id);
/** Notas de un tema: las suyas y las que el tema declara como relacionadas */
export const notesOf = (themeId: string) => {
  const extra = themeById(themeId)?.notes ?? [];
  return NOTES.filter((n) => n.theme === themeId || extra.includes(n.id));
};

export function figuresOf(theme: Theme, lens?: LensId) {
  const ids = lens ? [lens] : LENSES.map((l) => l.id);
  return ids.flatMap((id) =>
    (theme.lenses?.[id]?.body ?? []).filter((b): b is { fig: string; code: string } => "fig" in b).map((b) => ({ ...b, code: `${theme.code}-${b.code}`, lens: id })),
  );
}

export function noteFigures(note: Note) {
  return note.body
    .filter((b): b is { fig: string; code: string } => "fig" in b)
    // Un código completo ("N02-1") indica un gráfico reutilizado de otra pieza: no se duplica en la metodología
    .filter((b) => !b.code.includes("-"))
    .map((b) => ({ ...b, code: `${note.code}-${b.code}` }));
}

export const lensById = (id: LensId) => LENSES.find((l) => l.id === id)!;

export const tr = (b: Bi, lang: Lang) => b[lang];

/** Equivalencias de rutas español -> inglés de todas las páginas (secciones, temas, miradas y notas). */
const ROUTES: Map<string, string> = new Map([
  ...Object.values(paths).map((p) => [p.es, p.en] as [string, string]),
  ...THEMES.filter((t) => !t.hub).map((t) => { const p = themePath(t.slug); return [p.es, p.en] as [string, string]; }),
  ...LENSES.map((l) => { const p = lensPath(l.slug); return [p.es, p.en] as [string, string]; }),
  ...NOTES.map((n) => { const p = notePath(n.slug); return [p.es, p.en] as [string, string]; }),
]);

/** Enlace interno escrito en español ("/vivienda/#ficha-topes") en el idioma de la página. Los externos no cambian. */
export function localizeHref(href: string, lang: Lang): string {
  if (lang === "es" || !href.startsWith("/")) return href;
  const m = href.match(/^([^?#]*)(\?[^#]*)?(#.*)?$/)!;
  const en = ROUTES.get(m[1]);
  if (!en) throw new Error(`Enlace interno sin versión inglesa: ${href}`);
  // Las anclas de las miradas dentro de un tema llevan el slug de la mirada, que cambia con el idioma
  const hash = m[3] ? `#${LENSES.find((l) => `#${l.slug.es}` === m[3])?.slug.en ?? m[3].slice(1)}` : "";
  return en + (m[2] ?? "") + hash;
}
