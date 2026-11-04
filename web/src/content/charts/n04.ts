// N04. Un Congreso cada vez más fragmentado: cómo se dibuja cada gráfico.
import type { ChartConfig } from "../../lib/charts-config";

const charts: Record<string, ChartConfig> = {
  "n04-partidos-efectivos": {
    renderer: "line",
    series: ["ES"],
    seriesColors: { ES: "--es" },
    table: { rows: "series", cols: "time" },
    digits: 1,
  },
  "n04-dos-mayores": {
    renderer: "line",
    series: ["ES"],
    seriesColors: { ES: "--es" },
    table: { rows: "series", cols: "time" },
    digits: 1,
  },
};

export default charts;
