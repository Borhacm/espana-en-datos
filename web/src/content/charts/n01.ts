// N01. Quién gobierna dónde y qué se juega cada comunidad el 29N: cómo se dibuja cada gráfico.
import type { ChartConfig } from "../../lib/charts-config";

const charts: Record<string, ChartConfig> = {
  "n01-escanos-ccaa": {
    renderer: "rank",
    digits: 0,
    table: { rows: "geo", cols: "time" },
  },
  "n01-habitantes-escano": {
    renderer: "rank",
    usesFocus: true,
    digits: 0,
    table: { rows: "geo", cols: "time" },
  },
};

export default charts;
