// Tema Impuestos y gasto público: cómo se dibuja cada gráfico. Ver ChartConfig en lib/charts-config.ts.
import type { ChartConfig } from "../../lib/charts-config";

const charts: Record<string, ChartConfig> = {
  "fie1-europa-presion": {
    renderer: "rank",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  // Cada fila es un tipo de impuesto (o una función del gasto). Punto hueco: media de la UE; punto lleno: España
  "fie2-europa-impuestos": {
    renderer: "dumbbell",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "fie3-europa-gasto": {
    renderer: "dumbbell",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "fid1-comunidades-saldo": {
    renderer: "rank",
    usesFocus: true,
    digits: 0,
    table: { rows: "geo", cols: "time" },
  },
  // Punto hueco: renta antes de impuestos y prestaciones; punto lleno: renta disponible
  "fid2-comunidades-renta": {
    renderer: "dumbbell",
    digits: 1,
    table: { rows: "geo", cols: "stage" },
  },
  "fit1-presion": {
    renderer: "line",
    series: ["espana", "ue"],
    seriesColors: { espana: "--es", ue: "--eu" },
    table: { rows: "series", cols: "time", lastCols: 8 },
    digits: 1,
  },
  "fit2-impuestos": {
    renderer: "line",
    series: ["irpf", "sociedades", "iva", "cotizaciones"],
    seriesColors: { irpf: "--es", sociedades: "--focus", iva: "--eu", cotizaciones: "--context-strong" },
    table: { rows: "series", cols: "time", lastCols: 8 },
    digits: 1,
    domainMin: 0,
  },
};

export default charts;
