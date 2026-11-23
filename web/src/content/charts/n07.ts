// N07. Cómo se convierten los votos en escaños: cómo se dibuja cada gráfico.
import type { ChartConfig } from "../../lib/charts-config";

const charts: Record<string, ChartConfig> = {
  "n07-barrera-real": {
    renderer: "rank",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "n07-desproporcion": {
    renderer: "rank",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
};

export default charts;
