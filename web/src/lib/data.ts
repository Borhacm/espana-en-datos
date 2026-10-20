// Lectura de los JSON del pipeline en tiempo de build (tablas y textos renderizados en el servidor).
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

export type Bi = { es: string; en: string };

export interface ChartData {
  id: string;
  lens: "europa" | "dentro" | "tiempo";
  theme: string;
  title: Bi;
  subtitle: Bi;
  unit: Bi;
  source: { name: string; dataset: string; url: string; license: string; also?: { name: string; url: string }[] };
  notes: { es: string[]; en: string[] };
  retrieved: string;
  geos: Record<string, Bi & { eu?: boolean; aggregate?: boolean }>;
  dimensions?: Record<string, Record<string, Bi>>;
  rows: Record<string, any>[];
  [key: string]: any;
}

// Copia sincronizada por scripts/sync-data.mjs (el build se ejecuta desde web/)
const DATA_DIR = resolve(process.cwd(), "public/data/charts");

export function loadChart(id: string): ChartData {
  return JSON.parse(readFileSync(resolve(DATA_DIR, `${id}.json`), "utf-8"));
}

/** Datasets base (gobiernos, encuestas, elecciones), leídos en el build. */
const BASE_DIR = resolve(process.cwd(), "public/data/base");
export function loadBase<T = any>(id: string): T {
  return JSON.parse(readFileSync(resolve(BASE_DIR, `${id}.json`), "utf-8"));
}
