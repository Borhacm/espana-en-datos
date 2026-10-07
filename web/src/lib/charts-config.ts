// Cómo se dibuja cada gráfico. Lo comparten el servidor (tabla accesible) y el navegador (gráfico).

export type Renderer = "line" | "rank" | "paired" | "dumbbell" | "stack" | "map" | "polls" | "govtimeline" | "spainmap" | "matrix";

export interface Control {
  dim: string;
  default: string;
  /** Solo estas opciones, en este orden (por defecto: todas las de `dimensions`) */
  options?: string[];
}

export interface ChartConfig {
  renderer: Renderer;
  controls?: Control[];
  /** Filtro fijo, además de los controles */
  fixed?: Record<string, string>;
  /** Series en color, en orden fijo. El resto se dibuja como contexto gris (o se oculta). */
  series?: string[];
  showContext?: boolean;
  /** Solo estos países como contexto gris (si no se indica y showContext es true: todos los demás) */
  context?: string[];
  /** Usa el país elegido por el lector ("Destacar un país") */
  usesFocus?: boolean;
  /** Tabla accesible: pivot de filas x columnas */
  table: { rows: string; cols: string; lastCols?: number };
  /** Tabla propia (ver lib/table.ts) para gráficos cuyos datos no son una matriz fila x columna */
  customTable?: "polls" | "govtimeline" | "spainmap" | "matrix";
  /** Matriz: porcentajes con rampa secuencial ("heat") o votos sí/no/abstención ("votes") */
  matrixMode?: "heat" | "votes";
  /** Dimensión alternativa del valor (p. ej. per_million) según un control */
  valueFrom?: { control: string; map: Record<string, string> };
  yLabel?: { es: string; en: string };
  /** Decimales en etiquetas y tooltips (por defecto: 1) */
  digits?: number;
  /** Color (variable CSS) de series que no son países, p. ej. { hora: "--eu" } */
  seriesColors?: Record<string, string>;
  /** Países de fuera de la UE que se incluyen en los rankings, p. ej. ["USA"] */
  extraGeos?: string[];
  domainMin?: number;
}

// Cada tema y cada nota tiene su archivo en content/charts/: así un tema nuevo solo añade archivos
const modules = import.meta.glob<{ default: Record<string, ChartConfig> }>("../content/charts/*.ts", { eager: true });
export const CHARTS: Record<string, ChartConfig> = Object.assign({}, ...Object.values(modules).map((m) => m.default));

/** Etiquetas de los controles que no vienen en el JSON */
export const EXTRA_DIMENSIONS: Record<string, Record<string, { es: string }>> = {
  range: {
    all: { es: "Desde 2023" },
    year: { es: "Último año" },
    quarter: { es: "Últimos tres meses" },
  },
  level: {
    provincia: { es: "Provincias" },
    municipio: { es: "Municipios" },
  },
};
