// Tema Territorio: cómo se dibuja cada gráfico. Ver ChartConfig en lib/charts-config.ts.
import type { ChartConfig } from "../../lib/charts-config";

const charts: Record<string, ChartConfig> = {
  // Regiones NUTS 3 de la UE por debajo de 12,5 habitantes por km² (filas `rank`)
  "tee1-europa-densidad": {
    renderer: "rank",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  // Cada fila es un componente del cambio de población en las regiones rurales o urbanas. Punto hueco: UE; punto lleno: España
  "tee2-europa-balance": {
    renderer: "dumbbell",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  // Las 52 provincias (filas `rank`) y el total de España
  "ted1-provincias": {
    renderer: "rank",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  // Tramos de tamaño del municipio en 2001 (filas `rank`)
  "ted2-tamano-municipio": {
    renderer: "rank",
    digits: 1,
    table: { rows: "geo", cols: "time" },
  },
  "tet1-micromunicipios": {
    renderer: "line",
    series: ["micro"],
    seriesColors: { micro: "--es" },
    table: { rows: "series", cols: "time", lastCols: 8 },
    digits: 0,
  },
  "tet2-municipios-crecen": {
    renderer: "line",
    series: ["crecen"],
    seriesColors: { crecen: "--es" },
    table: { rows: "series", cols: "time", lastCols: 8 },
    digits: 1,
    domainMin: 0,
  },
};

export default charts;
