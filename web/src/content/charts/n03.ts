// N03. Quién vota y quién no: la participación desde 1977: cómo se dibuja cada gráfico.
import type { ChartConfig } from "../../lib/charts-config";

const charts: Record<string, ChartConfig> = {
  "n03-participacion": {
    renderer: "line",
    series: ["ES"],
    seriesColors: { ES: "--es" },
    table: { rows: "series", cols: "time" },
    digits: 1,
  },
  "n03-participacion-ccaa": {
    renderer: "rank",
    usesFocus: true,
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
};

export default charts;
