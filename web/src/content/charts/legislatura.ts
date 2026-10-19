// Tema La legislatura en datos: cómo se dibuja cada gráfico. Ver ChartConfig en lib/charts-config.ts.
import type { ChartConfig } from "../../lib/charts-config";

const charts: Record<string, ChartConfig> = {
  "lee1-europa-paro": {
    renderer: "rank",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "lee3-europa-crecimiento": {
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
  "led3-tasa-empleo": {
    renderer: "rank",
    usesFocus: true,
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "let4-crecimiento": {
    renderer: "line",
    series: ["poblacion", "per_capita", "pib"],
    seriesColors: { pib: "--es", per_capita: "--focus", poblacion: "--context-strong" },
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
  "let5-ingresos-gastos": {
    renderer: "line",
    series: ["ingresos", "gastos"],
    seriesColors: { gastos: "--es", ingresos: "--focus" },
    table: { rows: "series", cols: "time", lastCols: 8 },
    digits: 1,
  },
};

export default charts;
