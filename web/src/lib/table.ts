import type { ChartData } from "./data";
import { CHARTS, EXTRA_DIMENSIONS } from "./charts-config";
import { formatNumber, locale, type Lang } from "./i18n";

export interface Pivot {
  rowHeader: string;
  cols: { key: string; label: string }[];
  rows: { key: string; label: string; cells: (string | null)[] }[];
}

const EU_STATS = {
  median: { es: "UE (mediana de los 27)", en: "EU (median of the 27)" },
  min: { es: "País de la UE con el valor más bajo", en: "EU country with the lowest value" },
};

const TXT = {
  es: {
    inOffice: "en el cargo", series: "Serie",
    poll: "Encuesta", avgAt: "Media a", election2023: "Elecciones del 23 de julio de 2023",
    presidency: "Presidencia", party: "Partido", from: "Desde", to: "Hasta", acting: " (en funciones)",
    vote: { si: "A favor", no: "En contra", abst: "Abstención" } as Record<string, string>,
    decree: "Decreto-ley", government: "Gobierno",
    province: "Provincia", winner: "Ganador", winnerPct: "% del ganador", second: "Segundo", margin: "Ventaja (puntos)", turnout: "Participación %",
  },
  en: {
    inOffice: "in office", series: "Series",
    poll: "Poll", avgAt: "Average on", election2023: "Election of 23 July 2023",
    presidency: "Presidency", party: "Party", from: "From", to: "To", acting: " (acting)",
    vote: { si: "Yes", no: "No", abst: "Abstention" } as Record<string, string>,
    decree: "Decree-law", government: "Government",
    province: "Province", winner: "Winner", winnerPct: "Winner's %", second: "Second", margin: "Lead (points)", turnout: "Turnout %",
  },
};

/** 2025.25 -> "T2 2025" / "Q2 2025" (series trimestrales: time = año + (trimestre - 1) / 4). */
const quarterLabel = (t: number, lang: Lang) => `${lang === "es" ? "T" : "Q"}${Math.round((t % 1) * 4) + 1} ${Math.floor(t)}`;

function helpers(lang: Lang) {
  const T = TXT[lang];
  const n = (v: number | null | undefined, d = 1) => (v === null || v === undefined ? null : formatNumber(v, lang, d));
  const day = (iso: string | null) => (iso ? new Intl.DateTimeFormat(locale(lang), { dateStyle: "medium" }).format(new Date(iso)) : T.inOffice);
  return { T, n, day };
}

/** Tablas de gráficos que no son una matriz fila x columna. */
const CUSTOM: Record<string, (chart: ChartData, lang: Lang) => Pivot> = {
  polls(chart, lang) {
    const { n, day, T } = helpers(lang);
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
      rowHeader: T.poll,
      cols: parties.map((p) => ({ key: p, label: p })),
      rows: [
        { key: "avg", label: `${T.avgAt} ${day(lastDay)}`, cells: parties.map((p) => n(mean[p])) },
        ...recent.map((r) => ({
          key: `${r.date}${r.who}`,
          label: `${day(r.date)}. ${r.who}${r.kind !== "poll" ? " *" : ""}`,
          cells: parties.map((p) => n(r.v[p])),
        })),
        { key: "2023", label: T.election2023, cells: parties.map((p) => n(res[p])) },
      ],
    };
  },
  govtimeline(chart, lang) {
    const { day, T } = helpers(lang);
    const rows = [...chart.rows].sort((a, b) => (a.ccaa === "ES" ? -1 : 0) - (b.ccaa === "ES" ? -1 : 0) || chart.geos[a.ccaa][lang].localeCompare(chart.geos[b.ccaa][lang], lang) || a.start.localeCompare(b.start));
    return {
      rowHeader: T.presidency,
      cols: [{ key: "party", label: T.party }, { key: "start", label: T.from }, { key: "end", label: T.to }],
      rows: rows.map((r) => ({
        key: `${r.ccaa}${r.start}`,
        label: `${chart.geos[r.ccaa][lang]}: ${lang === "en" && r.party === "Art. 155" ? "Direct rule by the Spanish government (art. 155)" : r.president}${r.acting ? T.acting : ""}`,
        cells: [r.party_label, day(r.start), day(r.end)],
      })),
    };
  },
  matrix(chart, lang) {
    const { n, T } = helpers(lang);
    const cols: string[] = chart.blocs;
    const votes = chart.rows.some((r) => r.vote);
    const VOTE = T.vote;
    const rowKeys: string[] = chart.row_keys ?? (votes ? [...new Set(chart.rows.map((r) => r.row as string))] : cols);
    const cell = new Map(chart.rows.map((r) => [`${r.row}|${r.col}`, r]));
    return {
      rowHeader: votes ? T.decree : chart.row_keys ? T.government : T.party,
      cols: cols.map((c) => ({ key: c, label: c })),
      rows: rowKeys.map((rk) => ({
        key: rk,
        label: votes ? `RDL ${rk} (${cell.get(`${rk}|${cols[0]}`)?.date ?? ""})` : rk,
        cells: cols.map((c) => {
          const r = cell.get(`${rk}|${c}`);
          if (!r) return votes ? "–" : rk === c ? "–" : null;
          return votes ? VOTE[r.vote] : n(r.value);
        }),
      })),
    };
  },
  spainmap(chart, lang) {
    const { n, T } = helpers(lang);
    const rows = chart.rows.filter((r) => r.level === "provincia").sort((a, b) => a.name.localeCompare(b.name, "es"));
    return {
      rowHeader: T.province,
      cols: [
        { key: "winner", label: T.winner }, { key: "value", label: T.winnerPct }, { key: "second", label: T.second },
        { key: "margin", label: T.margin }, { key: "turnout", label: T.turnout },
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
  if (cfg.customTable) return CUSTOM[cfg.customTable](chart, lang);
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
    rowHeader: rowDim === "geo" ? headers.country : TXT[lang].series,
    cols: colKeys.map((k) => ({ key: k, label: colDim === "time" ? (chart.time_labels?.[k]?.[lang] ?? (chart.quarterly ? quarterLabel(+k, lang) : k)) : label(chart, colDim, k, lang) })),
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
