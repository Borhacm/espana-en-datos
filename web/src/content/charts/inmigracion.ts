// Tema Inmigración: cómo se dibuja cada gráfico. Ver ChartConfig en lib/charts-config.ts.
import type { ChartConfig } from "../../lib/charts-config";

const charts: Record<string, ChartConfig> = {
  "ine1-europa-nacidos-fuera": {
    renderer: "rank",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "ine2-europa-empleo": {
    renderer: "rank",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "ind1-comunidades-nacidos-fuera": {
    renderer: "rank",
    usesFocus: true,
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "ind2-comunidades-paro": {
    renderer: "rank",
    usesFocus: true,
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "int1-poblacion": {
    renderer: "line",
    series: ["extranjeros", "nacidos"],
    seriesColors: { nacidos: "--es", extranjeros: "--eu" },
    table: { rows: "series", cols: "time", lastCols: 8 },
    digits: 1,
  },
  "int2-paro": {
    renderer: "line",
    series: ["espanoles", "extranjeros"],
    seriesColors: { extranjeros: "--es", espanoles: "--eu" },
    table: { rows: "series", cols: "time", lastCols: 8 },
    digits: 1,
  },
};

export default charts;
