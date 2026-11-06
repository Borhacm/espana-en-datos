// Tema Energía: cómo se dibuja cada gráfico. Ver ChartConfig en lib/charts-config.ts.
import type { ChartConfig } from "../../lib/charts-config";

const charts: Record<string, ChartConfig> = {
  "ene1-europa-precio": {
    renderer: "rank",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  // Cada fila es un componente del precio. Punto hueco: media de la UE; punto lleno: España
  "ene2-europa-componentes": {
    renderer: "dumbbell",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "ene3-europa-frio": {
    renderer: "rank",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "end1-comunidades-frio": {
    renderer: "rank",
    usesFocus: true,
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "end2-comunidades-gasto": {
    renderer: "rank",
    usesFocus: true,
    digits: 0,
    table: { rows: "geo", cols: "time" },
  },
  "ent1-generacion": {
    renderer: "line",
    series: ["solar", "eolica", "gas", "nuclear", "carbon"],
    seriesColors: { solar: "--focus", eolica: "--es", gas: "--eu", nuclear: "--context-strong", carbon: "--context" },
    table: { rows: "series", cols: "time", lastCols: 8 },
    digits: 1,
    domainMin: 0,
  },
  "ent2-precio": {
    renderer: "line",
    series: ["espana", "ue"],
    seriesColors: { espana: "--es", ue: "--eu" },
    table: { rows: "series", cols: "time", lastCols: 8 },
    digits: 1,
  },
  "ent3-dependencia": {
    renderer: "line",
    series: ["espana", "ue"],
    seriesColors: { espana: "--es", ue: "--eu" },
    table: { rows: "series", cols: "time", lastCols: 8 },
    digits: 1,
  },
};

export default charts;
