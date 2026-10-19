// N02. Salarios reales y salario mínimo: cómo se dibuja cada gráfico.
import type { ChartConfig } from "../../lib/charts-config";

const charts: Record<string, ChartConfig> = {
  "n02-salario-real": {
    renderer: "line",
    series: ["salario", "smi"],
    seriesColors: { salario: "--es", smi: "--focus" },
    table: { rows: "series", cols: "time", lastCols: 8 },
    digits: 1,
  },
  "n02-smi-salario-medio": {
    renderer: "line",
    series: ["ratio"],
    seriesColors: { ratio: "--es" },
    table: { rows: "series", cols: "time", lastCols: 8 },
    digits: 1,
  },
};

export default charts;
