// AN01. Quince años en el Congreso: cómo se dibuja cada gráfico.
import type { ChartConfig } from "../../lib/charts-config";

const charts: Record<string, ChartConfig> = {
  "an01-pp-psoe": {
    renderer: "line",
    series: ["pp-psoe"],
    seriesColors: { "pp-psoe": "--es" },
    table: { rows: "series", cols: "time" },
    digits: 0,
    domainMin: 0,
  },
  "an01-gobierno-gana": {
    renderer: "line",
    series: ["PP", "PSOE"],
    seriesColors: { PP: "--p-pp", PSOE: "--p-psoe" },
    table: { rows: "series", cols: "time" },
    digits: 0,
    domainMin: 0,
  },
  "an01-decretos": {
    renderer: "rank",
    digits: 0,
    table: { rows: "geo", cols: "time" },
  },
  "an01-socios": {
    renderer: "matrix",
    matrixMode: "heat",
    table: { rows: "row", cols: "col" },
    customTable: "matrix",
  },
};

export default charts;
