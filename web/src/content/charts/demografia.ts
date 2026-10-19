// Tema Demografía y pensiones: cómo se dibuja cada gráfico. Ver ChartConfig en lib/charts-config.ts.
import type { ChartConfig } from "../../lib/charts-config";

const charts: Record<string, ChartConfig> = {
  "dee2-europa-pensiones": {
    renderer: "rank",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "dee3-europa-sustitucion": {
    renderer: "rank",
    digits: 0,
    table: { rows: "geo", cols: "time" },
  },
  "dee4-europa-vida65": {
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
  "ded3-ocupados-mayores": {
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
  "det4-gasto-descomposicion": {
    renderer: "line",
    series: ["pensionistas", "media", "gasto"],
    seriesColors: { gasto: "--es", media: "--focus", pensionistas: "--context-strong" },
    table: { rows: "series", cols: "time", lastCols: 8 },
    digits: 1,
  },
  "det5-dependencia-proyeccion": {
    renderer: "line",
    series: ["nulo", "central", "historico"],
    seriesColors: { historico: "--es", central: "--focus", nulo: "--context-strong" },
    table: { rows: "series", cols: "time", lastCols: 8 },
    digits: 1,
  },
};

export default charts;
