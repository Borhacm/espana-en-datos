// Tema La legislatura en datos: cómo se dibuja cada gráfico. Ver ChartConfig en lib/charts-config.ts.
import type { ChartConfig } from "../../lib/charts-config";

const charts: Record<string, ChartConfig> = {
  "lee1-europa-paro": {
    renderer: "rank",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "lee2-europa-deuda": {
    renderer: "rank",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "led1-paro-comunidades": {
    renderer: "rank",
    usesFocus: true,
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "led2-empleo-comunidades": {
    renderer: "rank",
    usesFocus: true,
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "let1-paro": {
    renderer: "line",
    series: ["paro"],
    seriesColors: { paro: "--es" },
    table: { rows: "series", cols: "time", lastCols: 8 },
    digits: 1,
  },
  "let2-salarios-precios": {
    renderer: "line",
    series: ["precios", "salarios"],
    seriesColors: { salarios: "--es", precios: "--context-strong" },
    table: { rows: "series", cols: "time", lastCols: 8 },
    digits: 1,
  },
  "let3-deficit": {
    renderer: "line",
    series: ["ue", "espana"],
    seriesColors: { espana: "--es", ue: "--eu" },
    table: { rows: "series", cols: "time", lastCols: 8 },
    digits: 1,
  },
};

export default charts;
