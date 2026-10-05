import { scaleLinear } from "d3-scale";
import { line as d3line } from "d3-shape";
import {
  svg, colorFor, cssVar, nf, geoName, dimLabel, slice, tooltip, tipRow, legend, niceTicks,
  type RenderContext, type Row,
} from "./core";

interface Series { key: string; label: string; color: string; points: { x: number; y: number }[]; context: boolean }

const MIN_LABEL_GAP = 15;

export function renderLine(ctx: RenderContext) {
  const { chart, cfg, lang, plot, focus } = ctx;
  const digits = cfg.digits ?? (ctx.state.scale === "total" ? 0 : 1);
  const fmt = nf(lang, digits);
  // El año en curso (incompleto) no se dibuja: parecería una caída. Sigue en la tabla y en la descarga.
  const partial = chart.partial_year ? String(chart.partial_year) : null;
  const rows = slice(ctx).filter((r) => r.time !== partial);

  // Qué series se dibujan: bloques en color, país destacado en oro, contexto en gris
  const byKey = new Map<string, Row[]>();
  // Una serie es un país o bloque; en algunos gráficos es una medida de un mismo bloque (dimensión "series")
  const hasMedian = rows.some((r) => r.stat === "median");
  for (const r of rows) {
    const key = r.stat === "min" ? "EU27_min" : (r.series ?? r.geo);
    if (!byKey.has(key)) byKey.set(key, []);
    byKey.get(key)!.push(r);
  }
  const main = cfg.series ?? [];
  const series: Series[] = [];
  const add = (key: string, context: boolean) => {
    const rs = byKey.get(key);
    if (!rs) return;
    const label = key === "EU27_min"
      ? (lang === "es" ? "País de la UE con el valor más bajo" : "EU country with the lowest value")
      : key === "EU27" && hasMedian
        ? (lang === "es" ? "UE (mediana de los 27)" : "EU (median of the 27)")
        : chart.dimensions?.series?.[key] ? dimLabel(chart, "series", key, lang) : geoName(chart, key, lang);
    const seriesVar = cfg.seriesColors?.[key];
    series.push({
      key, label, context,
      color: key === "EU27_min" ? cssVar("--context-strong") : seriesVar ? cssVar(seriesVar) : colorFor(key, focus),
      points: rs.map((r) => ({ x: +r.time, y: r.value })).sort((a, b) => a.x - b.x),
    });
  };
  const isContext = (k: string) => k === "EU27_min" || (cfg.context ? cfg.context.includes(k) : !!cfg.showContext);
  for (const k of byKey.keys()) if (!main.includes(k) && k !== focus && isContext(k)) add(k, true);
  if (focus && !main.includes(focus)) add(focus, false);
  for (const k of main) add(k, false);
  if (!series.length) return;

  // Dimensiones
  const width = ctx.width;
  const narrow = width < 560;
  const height = Math.round(Math.min(Math.max(width * 0.48, 280), 420));
  const m = { top: 20, right: narrow ? 12 : 150, bottom: 30, left: 4 };
  const xs = series.flatMap((s) => s.points.map((p) => p.x));
  const ys = series.flatMap((s) => s.points.map((p) => p.y));
  const ref: { value: number; label: { es: string; en: string } } | undefined = chart.ref_line;
  if (ref) ys.push(ref.value);
  const yMin = cfg.domainMin ?? Math.min(...ys);
  const yMaxRaw = Math.max(...ys);
  const ticks = niceTicks(yMaxRaw, Math.min(yMin, Math.min(...ys)), narrow ? 4 : 5);
  const x = scaleLinear().domain([Math.min(...xs), Math.max(...xs)]).range([m.left, width - m.right]);
  const y = scaleLinear().domain([ticks[0], Math.max(ticks[ticks.length - 1], yMaxRaw)]).range([height - m.bottom, m.top]);

  const root = svg("svg", { width, height, viewBox: `0 0 ${width} ${height}`, class: "chart-svg" });
  plot.appendChild(root);

  // Rejilla y etiquetas del eje Y sobre la línea (ahorra margen izquierdo)
  const grid = svg("g", { class: "grid" }, root);
  for (const t of ticks) {
    svg("line", { x1: m.left, x2: width - m.right, y1: y(t), y2: y(t), class: t === 0 ? "baseline" : "gridline" }, grid);
    const txt = svg("text", { x: m.left, y: y(t) - 5, class: "tick" }, grid);
    txt.textContent = fmt(t);
  }
  // Línea de referencia (p. ej. 100 = EE. UU. o nivel de 1990)
  if (ref) {
    svg("line", { x1: m.left, x2: width - m.right, y1: y(ref.value), y2: y(ref.value), class: "refline" }, grid);
    const lbl = svg("text", { x: width - m.right, y: y(ref.value) - 6, class: "ref-label", "text-anchor": "end" }, grid);
    lbl.textContent = ref.label[lang];
  }
  const [x0, x1] = x.domain();
  const step = Math.max(1, Math.ceil((x1 - x0) / (narrow ? 4 : 8)));
  for (let v = x1; v >= x0; v -= step) {
    const txt = svg("text", { x: x(v), y: height - 8, class: "tick", "text-anchor": v === x0 ? "start" : "middle" }, grid);
    txt.textContent = String(v);
  }

  // Líneas: contexto debajo, después las principales
  const path = d3line<{ x: number; y: number }>().x((p) => x(p.x)).y((p) => y(p.y));
  for (const s of series) {
    const g = svg("g", { class: s.context ? "series context" : "series" }, root);
    svg("path", { d: path(s.points) ?? "", stroke: s.color, class: "line", "stroke-width": s.context ? 1.5 : 2 }, g);
    const last = s.points[s.points.length - 1];
    if (!s.context) {
      svg("circle", {
        cx: x(last.x), cy: y(last.y), r: 4.5, fill: s.color, stroke: cssVar("--paper"), "stroke-width": 2,
      }, g);
    }
  }

  // Etiquetas directas al final (solo series principales, sin apilar etiquetas que chocan)
  if (!narrow) {
    const labels = series.filter((s) => !s.context).map((s) => {
      const last = s.points[s.points.length - 1];
      return { s, y: y(last.y), x: x(last.x), value: last.y };
    }).sort((a, b) => a.y - b.y);
    let prev = -Infinity;
    for (const l of labels) {
      if (l.y - prev < MIN_LABEL_GAP) continue; // la leyenda y el tooltip cubren la etiqueta omitida
      prev = l.y;
      const txt = svg("text", { x: l.x + 10, y: l.y + 4, class: "end-label" }, root);
      txt.innerHTML = `<tspan class="end-name">${l.s.label}</tspan> <tspan class="end-value">${fmt(l.value)}</tspan>`;
    }
  }

  // Leyenda: siempre con dos o más series
  legend(ctx.legend, [...series].reverse().map((s) => ({ color: s.color, label: s.label })));

  // Crosshair y tooltip
  const tip = tooltip(plot);
  const hover = svg("g", { class: "hover", style: "display:none" }, root);
  const vline = svg("line", { y1: m.top, y2: height - m.bottom, class: "crosshair" }, hover);
  const dots = series.filter((s) => !s.context || s.key === "EU27_min").map((s) =>
    ({ s, dot: svg("circle", { r: 4.5, fill: s.color, stroke: cssVar("--paper"), "stroke-width": 2 }, hover) }));
  const years = [...new Set(xs)].sort((a, b) => a - b);

  const overlay = svg("rect", { x: m.left, y: 0, width: width - m.left - m.right, height, fill: "transparent", tabindex: 0, class: "overlay" }, root);
  let idx = years.length - 1;
  const showAt = (i: number) => {
    idx = Math.max(0, Math.min(years.length - 1, i));
    const yr = years[idx];
    hover.style.display = "";
    vline.setAttribute("x1", String(x(yr)));
    vline.setAttribute("x2", String(x(yr)));
    const lines: { color: string; label: string; v: number }[] = [];
    for (const { s, dot } of dots) {
      const p = s.points.find((q) => q.x === yr);
      if (!p) { dot.style.display = "none"; continue; }
      dot.style.display = "";
      dot.setAttribute("cx", String(x(yr)));
      dot.setAttribute("cy", String(y(p.y)));
      lines.push({ color: s.color, label: s.label, v: p.y });
    }
    lines.sort((a, b) => b.v - a.v);
    tip.show(x(yr), m.top + 10, `<div class="tip-title">${yr}</div>${lines.map((l) => tipRow(l.color, l.label, fmt(l.v))).join("")}`);
  };
  const hide = () => { hover.style.display = "none"; tip.hide(); };
  overlay.addEventListener("pointermove", (e) => {
    const rect = root.getBoundingClientRect();
    const px = x.invert(e.clientX - rect.left);
    let best = 0;
    years.forEach((yr, i) => { if (Math.abs(yr - px) < Math.abs(years[best] - px)) best = i; });
    showAt(best);
  });
  overlay.addEventListener("pointerleave", hide);
  overlay.addEventListener("focus", () => showAt(idx));
  overlay.addEventListener("blur", hide);
  overlay.addEventListener("keydown", (e) => {
    if (e.key === "ArrowLeft") { showAt(idx - 1); e.preventDefault(); }
    if (e.key === "ArrowRight") { showAt(idx + 1); e.preventDefault(); }
  });
}
