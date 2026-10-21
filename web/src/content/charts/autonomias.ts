// Tema Autonomías: cómo se dibuja cada gráfico. Ver ChartConfig en lib/charts-config.ts.
import type { ChartConfig } from "../../lib/charts-config";

const charts: Record<string, ChartConfig> = {
  "aue1-europa-gasto": {
    renderer: "rank",
    digits: 0,
    table: { rows: "geo", cols: "time" },
  },
  "aue2-europa-deuda": {
    renderer: "rank",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "aud1-deuda-comunidades": {
    renderer: "rank",
    usesFocus: true,
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  // Punto hueco: lo que reúne cada comunidad con sus impuestos; punto lleno: lo que tiene tras el reparto
  "aud2-financiacion": {
    renderer: "dumbbell",
    digits: 0,
    table: { rows: "geo", cols: "stage" },
  },
  "aut1-deuda": {
    renderer: "line",
    series: ["deuda"],
    seriesColors: { deuda: "--es" },
    table: { rows: "series", cols: "time", lastCols: 8 },
    digits: 1,
  },
  "aut2-acreedores": {
    renderer: "line",
    series: ["resto", "estado"],
    seriesColors: { estado: "--es", resto: "--eu" },
    table: { rows: "series", cols: "time", lastCols: 8 },
    digits: 0,
  },
};

export default charts;
