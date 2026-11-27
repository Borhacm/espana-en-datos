// Tema Clima: cómo se dibuja cada gráfico. Ver ChartConfig en lib/charts-config.ts.
import type { ChartConfig } from "../../lib/charts-config";

const charts: Record<string, ChartConfig> = {
  // Emisiones por habitante: países de la UE y media de la UE
  "cle1-europa-habitante": {
    renderer: "rank",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  // Cada fila es un sector (índice 1990 = 100). Punto hueco: UE; punto lleno: España
  "cle2-europa-sectores": {
    renderer: "dumbbell",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  // Emisiones por habitante de cada comunidad y de España
  "cld1-comunidades-habitante": {
    renderer: "rank",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  // Grados-día de refrigeración. Punto hueco: años ochenta; punto lleno: última década
  "cld2-comunidades-calor": {
    renderer: "dumbbell",
    digits: 0,
    table: { rows: "geo", cols: "time" },
  },
  "clt1-emisiones-1990": {
    renderer: "line",
    series: ["ESP", "EU27"],
    seriesColors: { ESP: "--es", EU27: "--eu" },
    table: { rows: "geo", cols: "time", lastCols: 8 },
    digits: 1,
  },
  "clt2-pib-emisiones": {
    renderer: "line",
    series: ["pib", "emisiones", "intensidad"],
    seriesColors: { pib: "--eu", emisiones: "--es", intensidad: "--context-strong" },
    table: { rows: "series", cols: "time", lastCols: 8 },
    digits: 1,
    domainMin: 0,
  },
  "clt3-embalses": {
    renderer: "line",
    series: ["reserva"],
    seriesColors: { reserva: "--es" },
    table: { rows: "series", cols: "time", lastCols: 12 },
    digits: 1,
    domainMin: 0,
  },
};

export default charts;
