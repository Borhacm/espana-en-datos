// Tema Sanidad: cómo se dibuja cada gráfico. Ver ChartConfig en lib/charts-config.ts.
import type { ChartConfig } from "../../lib/charts-config";

const charts: Record<string, ChartConfig> = {
  "sae1-europa-gasto": {
    renderer: "rank",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "sae2-europa-bolsillo": {
    renderer: "rank",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "sad1-espera-comunidades": {
    renderer: "rank",
    usesFocus: true,
    digits: 0,
    table: { rows: "geo", cols: "time" },
  },
  "sad2-gasto-comunidades": {
    renderer: "rank",
    usesFocus: true,
    digits: 0,
    table: { rows: "geo", cols: "time" },
  },
  "sat1-lista-espera": {
    renderer: "line",
    series: ["tasa"],
    seriesColors: { tasa: "--es" },
    table: { rows: "series", cols: "time" },
    digits: 1,
  },
  "sat2-gasto-funciones": {
    renderer: "line",
    series: ["hospital", "farmacia", "primaria"],
    seriesColors: { hospital: "--es", farmacia: "--eu", primaria: "--focus" },
    table: { rows: "series", cols: "time", lastCols: 8 },
    digits: 1,
  },
};

export default charts;
