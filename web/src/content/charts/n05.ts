// N05. Cuánto cuesta un escaño en cada provincia: cómo se dibuja cada gráfico.
import type { ChartConfig } from "../../lib/charts-config";

const charts: Record<string, ChartConfig> = {
  "n05-votos-sin-escano": {
    renderer: "rank",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "n05-votos-escano": {
    renderer: "rank",
    digits: 0,
    table: { rows: "geo", cols: "time" },
  },
};

export default charts;
