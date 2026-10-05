import type { ChartData } from "./data";
import { CHARTS, EXTRA_DIMENSIONS } from "./charts-config";
import { formatNumber, type Lang } from "./i18n";

export interface Pivot {
  rowHeader: string;
  cols: { key: string; label: string }[];
  rows: { key: string; label: string; cells: (string | null)[] }[];
}

const EU_STATS = {
  median: { es: "UE (mediana de los 27)" },
  min: { es: "País de la UE con el valor más bajo" },
};

const n = (v: number | null | undefined, d = 1) => (v === null || v === undefined ? null : formatNumber(v, "es", d));
const day = (iso: string | null) => (iso ? new Intl.DateTimeFormat("es-ES", { dateStyle: "medium" }).format(new Date(iso)) : "en el cargo");

/** Tablas de gráficos que no son una matriz fila x columna. */
const CUSTOM: Record<string, (chart: ChartData) => Pivot> = {
  polls(chart) {
    const parties: string[] = chart.parties;
    const avg = chart.rows.filter((r) => r.series === "avg");
    const lastDay = avg[avg.length - 1]?.date;
    const polls = chart.rows.filter((r) => r.series === "poll");
    const byPoll = new Map<string, Record<string, any>>();
    for (const r of polls) {
      const k = `${r.date}|${r.pollster}|${r.commissioner ?? ""}`;
      if (!byPoll.has(k)) byPoll.set(k, { date: r.date, who: r.commissioner ? `${r.pollster} (${r.commissioner})` : r.pollster, kind: r.kind, v: {} });
      byPoll.get(k)!.v[r.party] = r.value;
    }
    const recent = [...byPoll.values()].sort((a, b) => b.date.localeCompare(a.date)).slice(0, 30);
    const mean = Object.fromEntries(avg.filter((r) => r.date === lastDay).map((r) => [r.party, r.value]));
    const res = Object.fromEntries(chart.results_2023.map((r: any) => [r.party, r.value]));
    return {
      rowHeader: "Encuesta",
      cols: parties.map((p) => ({ key: p, label: p })),
      rows: [
        { key: "avg", label: `Media a ${day(lastDay)}`, cells: parties.map((p) => n(mean[p])) },
        ...recent.map((r) => ({
          key: `${r.date}${r.who}`,
          label: `${day(r.date)}. ${r.who}${r.kind !== "poll" ? " *" : ""}`,
          cells: parties.map((p) => n(r.v[p])),
        })),
        { key: "2023", label: "Elecciones del 23 de julio de 2023", cells: parties.map((p) => n(res[p])) },
      ],
    };
  },
  govtimeline(chart) {
    const rows = [...chart.rows].sort((a, b) => (a.ccaa === "ES" ? -1 : 0) - (b.ccaa === "ES" ? -1 : 0) || chart.geos[a.ccaa].es.localeCompare(chart.geos[b.ccaa].es, "es") || a.start.localeCompare(b.start));
    return {
      rowHeader: "Presidencia",
      cols: [{ key: "party", label: "Partido" }, { key: "start", label: "Desde" }, { key: "end", label: "Hasta" }],
      rows: rows.map((r) => ({
        key: `${r.ccaa}${r.start}`,
        label: `${chart.geos[r.ccaa].es}: ${r.president}${r.acting ? " (en funciones)" : ""}`,
        cells: [r.party_label, day(r.start), day(r.end)],
      })),
    };
  },
  spainmap(chart) {
    const rows = chart.rows.filter((r) => r.level === "provincia").sort((a, b) => a.name.localeCompare(b.name, "es"));
    return {
      rowHeader: "Provincia",
      cols: [
        { key: "winner", label: "Ganador" }, { key: "value", label: "% del ganador" }, { key: "second", label: "Segundo" },
        { key: "margin", label: "Ventaja (puntos)" }, { key: "turnout", label: "Participación %" },
      ],
      rows: rows.map((r) => ({ key: r.geo, label: r.name, cells: [r.winner, n(r.value), r.second, n(r.margin), n(r.turnout)] })),
    };
  },
};

function label(chart: ChartData, dim: string, key: string, lang: Lang): string {
  if (key === "EU27_min") return EU_STATS.min[lang];
  if (key === "EU27" && chart.rows.some((r) => r.stat === "median")) return EU_STATS.median[lang];
  if (dim === "geo") return chart.geos[key]?.[lang] ?? chart.rows.find((r) => r.geo === key)?.name ?? key;
  return chart.dimensions?.[dim]?.[key]?.[lang] ?? EXTRA_DIMENSIONS[dim]?.[key]?.[lang] ?? key;
}

/** Tabla accesible con el estado por defecto de los controles. */
export function pivot(chart: ChartData, lang: Lang, headers: { country: string; year: string }): Pivot {
  const cfg = CHARTS[chart.id];
  if (cfg.customTable) return CUSTOM[cfg.customTable](chart);
  const { rows: rowDim, cols: colDim, lastCols } = cfg.table;
  const filter: Record<string, string> = { ...(cfg.fixed ?? {}) };
  for (const c of cfg.controls ?? []) if (c.dim !== rowDim && c.dim !== colDim && c.dim !== "scale") filter[c.dim] = c.default;

  let data = chart.rows.filter((r) => Object.entries(filter).every(([k, v]) => r[k] === undefined || r[k] === v));
  if (chart.best_level) data = data.filter((r) => r.level === chart.best_level[r.country]);
  // La fila "país con el valor más bajo" va aparte: si compartiera clave con la UE, pisaría la mediana
  data = data.map((r) => (r.stat === "min" ? { ...r, geo: "EU27_min" } : r));

  let colKeys = [...new Set(data.map((r) => String(r[colDim])))].sort();
  if (colDim === "reason" || colDim === "access") colKeys = Object.keys(chart.dimensions?.[colDim] ?? {}).filter((k) => colKeys.includes(k));
  if (lastCols) colKeys = colKeys.slice(-lastCols);

  const rowKeys = [...new Set(data.map((r) => String(r[rowDim])))];
  const rowLabel = (k: string) => label(chart, rowDim, k, lang);
  const first = ["EU27", "EU27_min"];
  rowKeys.sort((a, b) => {
    const ia = first.indexOf(a), ib = first.indexOf(b);
    if (ia !== -1 || ib !== -1) return (ia === -1 ? 9 : ia) - (ib === -1 ? 9 : ib);
    return rowLabel(a).localeCompare(rowLabel(b), lang);
  });

  const index = new Map(data.map((r) => [`${r[rowDim]}|${r[colDim]}`, r.value as number]));
  return {
    rowHeader: rowDim === "geo" ? headers.country : "Serie",
    cols: colKeys.map((k) => ({ key: k, label: colDim === "time" ? k : label(chart, colDim, k, lang) })),
    rows: rowKeys.map((k) => ({
      key: k,
      label: rowLabel(k),
      cells: colKeys.map((c) => {
        const v = index.get(`${k}|${c}`);
        return v === undefined ? null : formatNumber(v, lang, 2);
      }),
    })),
  };
}
