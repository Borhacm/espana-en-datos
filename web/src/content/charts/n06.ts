// N06. Qué preocupa a los españoles: cómo se dibuja cada gráfico.
import type { ChartConfig } from "../../lib/charts-config";

const charts: Record<string, ChartConfig> = {
  "n06-problemas-tiempo": {
    renderer: "line",
    series: ["vivienda", "economia", "paro", "inmigracion"],
    seriesColors: { vivienda: "--es", economia: "--eu", paro: "--focus", inmigracion: "--context-strong" },
    table: { rows: "series", cols: "time" },
    digits: 1,
    domainMin: 0,
  },
  "n06-problemas-ranking": {
    renderer: "rank",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
};

export default charts;
