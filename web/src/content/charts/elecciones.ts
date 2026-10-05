// Especial elecciones 29N: cómo se dibuja cada gráfico. Ver ChartConfig en lib/charts-config.ts.
import type { ChartConfig } from "../../lib/charts-config";

const charts: Record<string, ChartConfig> = {
  "el1-encuestas": {
    renderer: "polls",
    controls: [{ dim: "range", default: "all", options: ["all", "year", "quarter"] }],
    table: { rows: "party", cols: "date" },
    customTable: "polls",
  },
  "el2-gobiernos": {
    renderer: "govtimeline",
    usesFocus: true,
    table: { rows: "ccaa", cols: "start" },
    customTable: "govtimeline",
  },
  "el3-mapa-2023": {
    renderer: "spainmap",
    controls: [{ dim: "level", default: "provincia", options: ["provincia", "municipio"] }],
    table: { rows: "geo", cols: "winner" },
    customTable: "spainmap",
  },
};

export default charts;
