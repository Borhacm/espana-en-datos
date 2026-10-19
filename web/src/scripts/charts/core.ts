import type { ChartConfig } from "../../lib/charts-config";
import { EXTRA_DIMENSIONS } from "../../lib/charts-config";

export type Lang = "es";
export type Row = Record<string, any> & { value: number };
export type Bi = { es: string };

export interface Chart {
  id: string;
  title: Bi;
  unit: Bi;
  geos: Record<string, Bi & { eu: boolean; aggregate: boolean }>;
  dimensions?: Record<string, Record<string, Bi>>;
  rows: Row[];
  [k: string]: any;
}

export interface RenderContext {
  chart: Chart;
  cfg: ChartConfig;
  lang: Lang;
  state: Record<string, string>;
  focus: string | null;
  plot: HTMLElement;
  legend: HTMLElement;
  width: number;
}

const SVG_NS = "http://www.w3.org/2000/svg";

export function svg<K extends keyof SVGElementTagNameMap>(
  tag: K,
  attrs: Record<string, string | number | undefined> = {},
  parent?: Element,
): SVGElementTagNameMap[K] {
  const el = document.createElementNS(SVG_NS, tag);
  for (const [k, v] of Object.entries(attrs)) if (v !== undefined) el.setAttribute(k, String(v));
  parent?.appendChild(el);
  return el;
}

export function cssVar(name: string): string {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

const BLOC_VAR: Record<string, string> = { ES: "--es", ESP: "--es", EU27: "--eu" };

/** Color de cada partido. Los que no tienen color propio van en gris («Otros»). */
export const PARTY_VAR: Record<string, string> = {
  PP: "--p-pp", PSOE: "--p-psoe", Vox: "--p-vox", Sumar: "--p-sumar", Podemos: "--p-podemos", SALF: "--p-salf",
  PNV: "--p-pnv", "EH Bildu": "--p-bildu", UPN: "--p-upn", Junts: "--p-junts", ERC: "--p-erc", BNG: "--p-bng", CC: "--p-cc",
  // Mismo espacio político que Junts (lo indica la sigla en el tooltip)
  CiU: "--p-junts", PDeCAT: "--p-junts", JxCat: "--p-junts",
};
export const partyColor = (party: string) => cssVar(PARTY_VAR[party] ?? "--p-other");

/** Nombre visible de cada partido cuando no coincide con su clave en los datos. Frente Amplio sustituye a Sumar desde
 *  septiembre de 2026 y sigue su serie (ver la nota de datasets/encuestas.py). */
export const PARTY_LABEL: Record<string, string> = { Sumar: "Sumar/FA" };
export const partyLabel = (party: string) => PARTY_LABEL[party] ?? party;

/** El color sigue a la entidad, nunca a su posición. */
export function colorFor(geo: string, focus: string | null): string {
  if (geo === focus) return cssVar("--focus");
  return cssVar(BLOC_VAR[geo] ?? "--context");
}

export function isHighlighted(geo: string, focus: string | null): boolean {
  return geo === "EU27" || geo === "ES" || geo === focus || geo in BLOC_VAR;
}

export function nf(lang: Lang, digits = 1) {
  const f = new Intl.NumberFormat("es-ES", { maximumFractionDigits: digits });
  return (v: number) => f.format(v);
}

export function geoName(chart: Chart, geo: string, lang: Lang): string {
  // Con datos de V-Dem, la UE es la mediana de los 27: se dice en la etiqueta
  return chart.geos[geo]?.[lang] ?? chart.rows.find((r) => r.geo === geo)?.name ?? geo;
}

export function dimLabel(chart: Chart, dim: string, key: string, lang: Lang): string {
  return chart.dimensions?.[dim]?.[key]?.[lang] ?? EXTRA_DIMENSIONS[dim]?.[key]?.[lang] ?? key;
}

/** Filtra por el estado de los controles y los filtros fijos. */
export function slice(ctx: RenderContext, skip: string[] = []): Row[] {
  const filters = { ...(ctx.cfg.fixed ?? {}), ...ctx.state };
  const valueKey = ctx.cfg.valueFrom ? ctx.cfg.valueFrom.map[ctx.state[ctx.cfg.valueFrom.control]] : "value";
  const out: Row[] = [];
  for (const r of ctx.chart.rows) {
    let ok = true;
    for (const [k, v] of Object.entries(filters)) {
      if (skip.includes(k) || k === ctx.cfg.valueFrom?.control) continue;
      if (r[k] !== undefined && r[k] !== v) { ok = false; break; }
    }
    if (!ok) continue;
    const value = r[valueKey];
    if (typeof value === "number") out.push({ ...r, value });
  }
  return out;
}

// ---------- Tooltip ----------

export function tooltip(plot: HTMLElement) {
  let tip = plot.querySelector<HTMLDivElement>(".tip");
  if (!tip) {
    tip = document.createElement("div");
    tip.className = "tip";
    tip.setAttribute("role", "status");
    plot.appendChild(tip);
  }
  const el = tip;
  return {
    show(x: number, y: number, html: string) {
      el.innerHTML = html;
      el.style.display = "block";
      const w = el.offsetWidth;
      let left = x + 14;
      if (left + w > plot.clientWidth) left = x - w - 14;
      el.style.left = `${Math.max(left, 0)}px`;
      el.style.top = `${Math.max(y - el.offsetHeight - 10, 0)}px`;
    },
    hide() { el.style.display = "none"; },
  };
}

export function tipRow(color: string, label: string, value: string, strong = false): string {
  return `<div class="tip-row${strong ? " strong" : ""}"><span class="key" style="background:${color}"></span><span>${label}</span><span class="v">${value}</span></div>`;
}

// ---------- Leyenda ----------

export function legend(el: HTMLElement, items: { color: string; label: string; kind?: "line" | "dot" | "swatch" }[]) {
  el.innerHTML = "";
  for (const it of items) {
    const span = document.createElement("span");
    span.className = `lg lg-${it.kind ?? "line"}`;
    span.innerHTML = `<span class="key" style="background:${it.color}"></span>${it.label}`;
    el.appendChild(span);
  }
}

// ---------- Ejes ----------

export function niceTicks(max: number, min = 0, count = 5): number[] {
  const span = max - min;
  const step0 = span / count;
  const mag = 10 ** Math.floor(Math.log10(step0));
  const step = [1, 2, 2.5, 5, 10].map((m) => m * mag).find((s) => span / s <= count) ?? step0;
  const ticks: number[] = [];
  for (let v = Math.floor(min / step) * step; v < max + step - 1e-9; v += step) ticks.push(+v.toFixed(10));
  return ticks;
}
