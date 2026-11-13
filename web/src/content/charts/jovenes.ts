// Tema Jóvenes: cómo se dibuja cada gráfico. Ver ChartConfig en lib/charts-config.ts.
import type { ChartConfig } from "../../lib/charts-config";

const charts: Record<string, ChartConfig> = {
  "joe1-europa-edad": {
    renderer: "rank",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  // Cada fila es una situación (trabaja, paro, estudia...). Punto hueco: UE; punto lleno: España
  "joe2-europa-trabajan": {
    renderer: "dumbbell",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "jod1-comunidades-ninis": {
    renderer: "rank",
    usesFocus: true,
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  // Cada fila es una comunidad. Punto hueco: estudios superiores; punto lleno: como mucho la ESO
  "jod2-comunidades-paro-estudios": {
    renderer: "dumbbell",
    usesFocus: true,
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "jot1-con-padres": {
    renderer: "line",
    series: ["ue", "espana"],
    seriesColors: { espana: "--es", ue: "--eu" },
    table: { rows: "series", cols: "time", lastCols: 8 },
    digits: 1,
  },
  "jot2-tenencia": {
    renderer: "line",
    series: ["cesion", "reducido", "mercado", "propiedad"],
    seriesColors: { propiedad: "--es", mercado: "--focus", reducido: "--context-strong", cesion: "--eu" },
    table: { rows: "series", cols: "time", lastCols: 8 },
    digits: 1,
    domainMin: 0,
  },
};

export default charts;
