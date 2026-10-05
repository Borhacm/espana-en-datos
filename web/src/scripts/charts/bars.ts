import { scaleLinear } from "d3-scale";
import {
  svg, colorFor, cssVar, nf, geoName, dimLabel, slice, tooltip, tipRow, legend, niceTicks,
  type RenderContext, type Row,
} from "./core";

const BAR = 14;       // grosor de barra (<= 24px)
const ROW = 24;       // alto de fila
const R = 3;          // extremo redondeado

/** Barra horizontal con el extremo de datos redondeado y el de la base recto (también hacia la izquierda). */
function barPath(x0: number, x1: number, y: number, h: number): string {
  if (x1 < x0) {
    const w = x0 - x1;
    const r = Math.min(R, w, h / 2);
    return `M${x0},${y}H${x1 + r}Q${x1},${y} ${x1},${y + r}V${y + h - r}Q${x1},${y + h} ${x1 + r},${y + h}H${x0}Z`;
  }
  const w = Math.max(x1 - x0, 0);
  const r = Math.min(R, w, h / 2);
  return `M${x0},${y}H${x0 + w - r}Q${x0 + w},${y} ${x0 + w},${y + r}V${y + h - r}Q${x0 + w},${y + h} ${x0 + w - r},${y + h}H${x0}Z`;
}

function nameWidth(width: number) { return width < 520 ? 104 : 150; }

/** Sufijo de unidad para ticks y tooltips: " %" solo si el gráfico se mide en porcentaje. */
function pctSuffix(ctx: RenderContext): string {
  return ctx.chart.unit.es.startsWith("%") ? " %" : "";
}

function euRows(ctx: RenderContext, rows: Row[]): Row[] {
  const extra = ctx.cfg.extraGeos ?? [];
  return rows.filter((r) => ctx.chart.geos[r.geo]?.eu || extra.includes(r.geo));
}

/** Ranking de países: d3 (IA generativa) y d4 (competencias digitales). */
export function renderRank(ctx: RenderContext) {
  const { chart, lang, plot, focus, width } = ctx;
  const fmt = nf(lang, ctx.cfg.digits ?? 1);
  const pct = pctSuffix(ctx);
  const rows = euRows(ctx, slice(ctx)).sort((a, b) => b.value - a.value);
  if (!rows.length) return;

  const targets: { value: number; label: { es: string; en: string } }[] = chart.targets ?? [];
  const left = nameWidth(width);
  // Con línea de objetivo, su etiqueta va en una franja propia bajo las barras
  const m = { top: 28, right: 44, bottom: targets.length ? 26 : 8 };
  const height = m.top + rows.length * ROW + m.bottom;
  const max = Math.max(...rows.map((r) => r.value), ...targets.map((t) => t.value));
  // Si hay valores negativos, el eje empieza justo antes del mínimo (no en el tick redondo anterior)
  const min = Math.min(0, ...rows.map((r) => r.value));
  const domMin = min < 0 ? min - (max - min) * 0.03 : 0;
  const ticks = niceTicks(max, 0, width < 520 ? 3 : 5).filter((t) => t >= domMin);
  const x = scaleLinear().domain([domMin, Math.max(ticks[ticks.length - 1], max)]).range([left, width - m.right]);

  const root = svg("svg", { width, height, viewBox: `0 0 ${width} ${height}`, class: "chart-svg" });
  plot.appendChild(root);
  for (const t of ticks) {
    svg("line", { x1: x(t), x2: x(t), y1: m.top - 6, y2: height - m.bottom, class: t === 0 ? "baseline" : "gridline" }, root);
    const txt = svg("text", { x: x(t), y: m.top - 12, class: "tick", "text-anchor": "middle" }, root);
    txt.textContent = fmt(t);
  }

  // Línea de objetivo por detrás de las barras, para no tachar las etiquetas
  for (const t of targets) {
    svg("line", { x1: x(t.value), x2: x(t.value), y1: m.top - 4, y2: height - m.bottom + 4, class: "target" }, root);
  }

  const tip = tooltip(plot);
  rows.forEach((r, i) => {
    const y = m.top + i * ROW;
    const hl = r.geo === "EU27" || r.geo === focus || (ctx.cfg.extraGeos ?? []).includes(r.geo);
    const g = svg("g", { class: `bar-row${hl ? " hl" : ""}`, tabindex: 0 }, root);
    svg("rect", { x: 0, y, width, height: ROW, fill: "transparent" }, g);
    const name = svg("text", { x: left - 10, y: y + ROW / 2 + 5, class: `row-name${hl ? " strong" : ""}`, "text-anchor": "end" }, g);
    name.textContent = geoName(chart, r.geo, lang);
    svg("path", { d: barPath(x(0), x(r.value), y + (ROW - BAR) / 2, BAR), fill: colorFor(r.geo, focus) }, g);
    const val = svg("text", { x: Math.max(x(r.value), x(0)) + 6, y: y + ROW / 2 + 5, class: `row-value${hl ? " strong" : ""}` }, g);
    val.textContent = fmt(r.value);
    const show = () => tip.show(x(r.value), y, tipRow(colorFor(r.geo, focus), geoName(chart, r.geo, lang), `${fmt(r.value)}${pct}`, true));
    g.addEventListener("pointerenter", show);
    g.addEventListener("focus", show);
    g.addEventListener("pointerleave", () => tip.hide());
    g.addEventListener("blur", () => tip.hide());
  });

  for (const t of targets) {
    const txt = svg("text", { x: x(t.value), y: height - 6, class: "target-label", "text-anchor": "middle" }, root);
    txt.textContent = `${t.label[lang]}: ${fmt(t.value)}${pct}`;
  }
  ctx.legend.innerHTML = "";
}

/** UE frente al país destacado, por categoría (e1). */
export function renderPaired(ctx: RenderContext) {
  const { chart, lang, plot, focus, width } = ctx;
  const fmt = nf(lang, 1);
  const rows = slice(ctx);
  const cats = Object.keys(chart.dimensions?.reason ?? {});
  const geos = ["EU27", ...(focus && focus !== "EU27" && rows.some((r) => r.geo === focus) ? [focus] : [])];
  const value = (g: string, c: string) => rows.find((r) => r.geo === g && r.reason === c)?.value;

  const left = width < 520 ? 130 : 230;
  const group = geos.length * (BAR + 4) + 18;
  const m = { top: 28, right: 44, bottom: 8 };
  const height = m.top + cats.length * group + m.bottom;
  const max = Math.max(...rows.filter((r) => geos.includes(r.geo)).map((r) => r.value));
  const ticks = niceTicks(max, 0, 4);
  const x = scaleLinear().domain([0, Math.max(ticks[ticks.length - 1], max)]).range([left, width - m.right]);

  const root = svg("svg", { width, height, viewBox: `0 0 ${width} ${height}`, class: "chart-svg" });
  plot.appendChild(root);
  for (const t of ticks) {
    svg("line", { x1: x(t), x2: x(t), y1: m.top - 6, y2: height - m.bottom, class: t === 0 ? "baseline" : "gridline" }, root);
    const txt = svg("text", { x: x(t), y: m.top - 12, class: "tick", "text-anchor": "middle" }, root);
    txt.textContent = `${fmt(t)} %`;
  }
  const tip = tooltip(plot);
  cats.forEach((c, i) => {
    const y0 = m.top + i * group + 6;
    const name = svg("text", { x: left - 10, y: y0 + (geos.length * (BAR + 4)) / 2 + 3, class: "row-name", "text-anchor": "end" }, root);
    name.textContent = dimLabel(chart, "reason", c, lang);
    geos.forEach((g, j) => {
      const v = value(g, c);
      if (v === undefined) return;
      const y = y0 + j * (BAR + 4);
      const grp = svg("g", { tabindex: 0 }, root);
      svg("rect", { x: left, y: y - 2, width: width - left, height: BAR + 4, fill: "transparent" }, grp);
      svg("path", { d: barPath(x(0), x(v), y, BAR), fill: colorFor(g, focus) }, grp);
      const val = svg("text", { x: x(v) + 6, y: y + BAR - 2, class: "row-value" }, grp);
      val.textContent = fmt(v);
      const show = () => tip.show(x(v), y, `<div class="tip-title">${dimLabel(chart, "reason", c, lang)}</div>${tipRow(colorFor(g, focus), geoName(chart, g, lang), `${fmt(v)} %`)}`);
      grp.addEventListener("pointerenter", show);
      grp.addEventListener("focus", show);
      grp.addEventListener("pointerleave", () => tip.hide());
      grp.addEventListener("blur", () => tip.hide());
    });
  });
  legend(ctx.legend, geos.map((g) => ({ color: colorFor(g, focus), label: geoName(chart, g, lang), kind: "swatch" as const })));
}

/** Evolución 2021 a último año por país (d1). */
export function renderDumbbell(ctx: RenderContext) {
  const { chart, lang, plot, focus, width } = ctx;
  const fmt = nf(lang, ctx.cfg.digits ?? 1);
  const pct = pctSuffix(ctx);
  const rows = euRows(ctx, slice(ctx));
  const years = [...new Set(rows.map((r) => r.time))].sort();
  const first = years[0], last = years[years.length - 1];
  const geos = [...new Set(rows.map((r) => r.geo))];
  const get = (g: string, t: string) => rows.find((r) => r.geo === g && r.time === t)?.value;
  const data = geos
    .map((g) => ({ g, a: get(g, first), b: get(g, last) }))
    .filter((d): d is { g: string; a: number; b: number } => d.a !== undefined && d.b !== undefined)
    .sort((p, q) => q.b - p.b);

  const left = nameWidth(width);
  const m = { top: 28, right: 44, bottom: 8 };
  const height = m.top + data.length * ROW + m.bottom;
  const max = Math.max(...data.map((d) => d.b), ...data.map((d) => d.a));
  const ticks = niceTicks(max, 0, width < 520 ? 3 : 5);
  const x = scaleLinear().domain([0, Math.max(ticks[ticks.length - 1], max)]).range([left, width - m.right]);

  const root = svg("svg", { width, height, viewBox: `0 0 ${width} ${height}`, class: "chart-svg" });
  plot.appendChild(root);
  for (const t of ticks) {
    svg("line", { x1: x(t), x2: x(t), y1: m.top - 6, y2: height - m.bottom, class: t === 0 ? "baseline" : "gridline" }, root);
    const txt = svg("text", { x: x(t), y: m.top - 12, class: "tick", "text-anchor": "middle" }, root);
    txt.textContent = `${fmt(t)}${pct}`;
  }
  const tip = tooltip(plot);
  const paper = cssVar("--paper");
  data.forEach((d, i) => {
    const cy = m.top + i * ROW + ROW / 2;
    const hl = d.g === "EU27" || d.g === focus;
    const color = colorFor(d.g, focus);
    const g = svg("g", { class: `bar-row${hl ? " hl" : ""}`, tabindex: 0 }, root);
    svg("rect", { x: 0, y: cy - ROW / 2, width, height: ROW, fill: "transparent" }, g);
    const name = svg("text", { x: left - 10, y: cy + 5, class: `row-name${hl ? " strong" : ""}`, "text-anchor": "end" }, g);
    name.textContent = geoName(chart, d.g, lang);
    svg("line", { x1: x(d.a), x2: x(d.b), y1: cy, y2: cy, stroke: hl ? color : cssVar("--context"), "stroke-width": 2 }, g);
    svg("circle", { cx: x(d.a), cy, r: 4, fill: paper, stroke: hl ? color : cssVar("--context-strong"), "stroke-width": 2 }, g);
    svg("circle", { cx: x(d.b), cy, r: 5, fill: hl ? color : cssVar("--context-strong"), stroke: paper, "stroke-width": 2 }, g);
    // La etiqueta va tras el punto más a la derecha, para no pisar el de 2004 si el país ha bajado
    const val = svg("text", { x: Math.max(x(d.a), x(d.b)) + 10, y: cy + 5, class: `row-value${hl ? " strong" : ""}` }, g);
    val.textContent = fmt(d.b);
    const show = () => tip.show(x(d.b), cy - 12,
      `<div class="tip-title">${geoName(chart, d.g, lang)}</div>${tipRow(cssVar("--context"), first, `${fmt(d.a)}${pct}`)}${tipRow(color, last, `${fmt(d.b)}${pct}`, true)}`);
    g.addEventListener("pointerenter", show);
    g.addEventListener("focus", show);
    g.addEventListener("pointerleave", () => tip.hide());
    g.addEventListener("blur", () => tip.hide());
  });
  ctx.legend.innerHTML = `<span class="lg lg-hollow"><span class="key"></span>${first}</span><span class="lg lg-dot"><span class="key"></span>${last}</span>`;
}
