// Tema Productividad y empresa: cómo se dibuja cada gráfico. Ver ChartConfig en lib/charts-config.ts.
import type { ChartConfig } from "../../lib/charts-config";

const charts: Record<string, ChartConfig> = {
  "pre1-europa-pib": {
    renderer: "rank",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  // Cada fila es un factor del PIB por habitante. Punto hueco: UE (= 100); punto lleno: España
  "pre2-europa-brecha": {
    renderer: "dumbbell",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  // Cada fila es un tamaño de empresa. Punto hueco: UE; punto lleno: España
  "pre3-europa-tamano": {
    renderer: "dumbbell",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "prd1-comunidades-pib": {
    renderer: "rank",
    usesFocus: true,
    digits: 0,
    table: { rows: "geo", cols: "time" },
  },
  "prd2-comunidades-hora": {
    renderer: "rank",
    usesFocus: true,
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "prt1-convergencia": {
    renderer: "line",
    series: ["pib", "hora"],
    seriesColors: { pib: "--es", hora: "--focus" },
    table: { rows: "series", cols: "time", lastCols: 8 },
    digits: 1,
  },
  "prt2-id": {
    renderer: "line",
    series: ["espana", "ue", "publica"],
    seriesColors: { espana: "--es", ue: "--eu", publica: "--focus" },
    table: { rows: "series", cols: "time", lastCols: 8 },
    digits: 2,
    domainMin: 0,
  },
};

export default charts;
