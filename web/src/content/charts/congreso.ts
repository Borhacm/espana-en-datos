// El Congreso en datos: cómo se dibuja cada gráfico. Ver ChartConfig en lib/charts-config.ts.
import type { ChartConfig } from "../../lib/charts-config";

const charts: Record<string, ChartConfig> = {
  "cg1-coincidencias": {
    renderer: "matrix",
    matrixMode: "heat",
    table: { rows: "row", cols: "col" },
    customTable: "matrix",
  },
  "cg2-lado-ganador": {
    renderer: "line",
    series: ["PP", "PSOE"],
    seriesColors: { PP: "--p-pp", PSOE: "--p-psoe" },
    table: { rows: "series", cols: "time" },
    digits: 0,
    domainMin: 0,
  },
  "cg3-decretos-derogados": {
    renderer: "matrix",
    matrixMode: "votes",
    table: { rows: "row", cols: "col" },
    customTable: "matrix",
  },
};

export default charts;
