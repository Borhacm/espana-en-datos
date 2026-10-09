// Tema Empleo: cómo se dibuja cada gráfico. Ver ChartConfig en lib/charts-config.ts.
import type { ChartConfig } from "../../lib/charts-config";

const charts: Record<string, ChartConfig> = {
  "eme1-europa-temporalidad": {
    renderer: "rank",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "eme2-europa-paro-juvenil": {
    renderer: "rank",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "emd1-temporalidad-comunidades": {
    renderer: "rank",
    usesFocus: true,
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "emd2-paro-larga-comunidades": {
    renderer: "rank",
    usesFocus: true,
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "emt1-temporalidad-sectores": {
    renderer: "line",
    series: ["publico", "privado"],
    seriesColors: { privado: "--es", publico: "--eu" },
    table: { rows: "series", cols: "time", lastCols: 9 },
    digits: 1,
  },
  "emt2-fijos-discontinuos": {
    renderer: "line",
    series: ["suma", "temporal", "discontinuo"],
    seriesColors: { temporal: "--es", discontinuo: "--focus", suma: "--context-strong" },
    table: { rows: "series", cols: "time", lastCols: 9 },
    digits: 1,
  },
};

export default charts;
