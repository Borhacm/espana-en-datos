// Registro de temas, notas y miradas. Todas las páginas salen de aquí.
// Cada tema vive en content/themes/<id>.ts y cada nota en content/notes/<id>.ts:
// para publicar uno nuevo basta con añadir su archivo.
import type { Lang } from "./i18n";
import type { Bi, Lens, LensId, Note, Theme } from "./content-types";

export type { Bi, Block, Lens, LensId, Note, Theme, ThemeLens } from "./content-types";

export const LENSES: Lens[] = [
  {
    id: "europa",
    slug: { es: "espana-frente-a-europa" },
    name: { es: "España frente a Europa" },
    short: { es: "Dónde estamos respecto a la UE" },
    about: { es: "Cómo se compara España con la media de la Unión Europea y con los países de su tamaño: Alemania, Francia, Italia y Portugal." },
  },
  {
    id: "dentro",
    slug: { es: "espana-por-dentro" },
    name: { es: "España por dentro" },
    short: { es: "Las diferencias entre comunidades" },
    about: { es: "Las diferencias entre comunidades autónomas y provincias que esconde la media nacional, y quién gobierna en cada una." },
  },
  {
    id: "tiempo",
    slug: { es: "espana-en-el-tiempo" },
    name: { es: "España en el tiempo" },
    short: { es: "De dónde venimos" },
    about: { es: "Cómo ha cambiado cada dato desde la crisis de 2008, la pandemia y el inicio de la legislatura en 2023." },
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
