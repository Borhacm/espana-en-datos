// Tema Demografía y pensiones: cómo se dibuja cada gráfico. Ver ChartConfig en lib/charts-config.ts.
import type { ChartConfig } from "../../lib/charts-config";

const charts: Record<string, ChartConfig> = {
  "dee1-europa-fecundidad": {
    renderer: "rank",
    digits: 2,
    table: { rows: "geo", cols: "time" },
  },
  "dee2-europa-pensiones": {
    renderer: "rank",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "ded1-dependencia-comunidades": {
    renderer: "rank",
    usesFocus: true,
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "ded2-fecundidad-comunidades": {
    renderer: "rank",
    usesFocus: true,
    digits: 2,
    table: { rows: "geo", cols: "time" },
  },
  "det1-fecundidad": {
    renderer: "line",
    series: ["fecundidad"],
    seriesColors: { fecundidad: "--es" },
    table: { rows: "series", cols: "time", lastCols: 8 },
    digits: 2,
  },
  "det2-esperanza-vida": {
    renderer: "line",
    series: ["esperanza"],
    seriesColors: { esperanza: "--es" },
    table: { rows: "series", cols: "time", lastCols: 8 },
    digits: 1,
  },
  "det3-dependencia": {
    renderer: "line",
    series: ["dependencia"],
    seriesColors: { dependencia: "--es" },
    table: { rows: "series", cols: "time", lastCols: 8 },
    digits: 1,
  },
};

export default charts;
