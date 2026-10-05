// Tema Vivienda: cómo se dibuja cada gráfico. Ver ChartConfig en lib/charts-config.ts.
import type { ChartConfig } from "../../lib/charts-config";

// Grupos de municipios catalanes: violeta (con tope desde marzo de 2024), oro (desde octubre), pizarra (sin tope)
const CAT_COLORS = { zmrt1: "--es", zmrt2: "--focus", sin: "--eu" };

const charts: Record<string, ChartConfig> = {
  "vit1-precios-salarios": {
    renderer: "line",
    series: ["precios", "salarios", "vivienda"],
    seriesColors: { vivienda: "--es", salarios: "--eu", precios: "--context-strong" },
    table: { rows: "series", cols: "time", lastCols: 8 },
    digits: 0,
  },
  "vid1-comunidades": {
    renderer: "rank",
    usesFocus: true,
    digits: 0,
    table: { rows: "geo", cols: "time" },
  },
  "vid2-cataluna-rentas": {
    renderer: "line",
    series: ["sin", "zmrt2", "zmrt1"],
    seriesColors: CAT_COLORS,
    table: { rows: "series", cols: "time", lastCols: 9 },
    digits: 0,
  },
  "vid3-cataluna-contratos": {
    renderer: "line",
    series: ["sin", "zmrt2", "zmrt1"],
    seriesColors: CAT_COLORS,
    table: { rows: "series", cols: "time", lastCols: 9 },
    digits: 0,
  },
  "vie1-europa-precios": {
    renderer: "rank",
    digits: 0,
    table: { rows: "geo", cols: "time" },
  },
  "vie2-europa-sobrecarga": {
    renderer: "rank",
    digits: 0,
    table: { rows: "geo", cols: "time" },
  },
};

export default charts;
