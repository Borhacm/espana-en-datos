// Tema Educación: cómo se dibuja cada gráfico. Ver ChartConfig en lib/charts-config.ts.
import type { ChartConfig } from "../../lib/charts-config";

const charts: Record<string, ChartConfig> = {
  "ede1-europa-abandono": {
    renderer: "rank",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "ede2-europa-pisa": {
    renderer: "rank",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "ede3-europa-nivel": {
    renderer: "rank",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "edd1-comunidades-abandono": {
    renderer: "rank",
    usesFocus: true,
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "edd2-comunidades-superiores": {
    renderer: "rank",
    usesFocus: true,
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "edt1-abandono": {
    renderer: "line",
    series: ["espana", "ue"],
    seriesColors: { espana: "--es", ue: "--eu" },
    table: { rows: "series", cols: "time", lastCols: 8 },
    digits: 1,
  },
  "edt2-abandono-origen": {
    renderer: "line",
    series: ["nat", "for"],
    seriesColors: { nat: "--es", for: "--focus" },
    table: { rows: "series", cols: "time", lastCols: 8 },
    digits: 1,
  },
  "edt3-fp-dual": {
    renderer: "line",
    series: ["espana", "ue"],
    seriesColors: { espana: "--es", ue: "--eu" },
    table: { rows: "series", cols: "time", lastCols: 10 },
    digits: 1,
  },
};

export default charts;
