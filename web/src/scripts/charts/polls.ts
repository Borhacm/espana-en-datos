// Seguimiento de encuestas: un punto por encuesta y la media como línea, con los resultados de 2023 de referencia
// y la fecha de las elecciones marcada al final del eje.
import { scaleLinear, scaleTime } from "d3-scale";
import { line as d3line, curveMonotoneX } from "d3-shape";
import { svg, cssVar, nf, partyColor, tooltip, tipRow, legend, niceTicks, type RenderContext, type Row } from "./core";

const ELECTION = new Date("2026-11-29");
const RANGES: Record<string, number | null> = { all: null, year: 365, quarter: 92 };
const MONTHS = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"];
const MIN_LABEL_GAP = 16;

const d = (iso: string) => new Date(iso + "T00:00:00");
const fmtDay = (dt: Date) => `${dt.getDate()} ${MONTHS[dt.getMonth()]} ${dt.getFullYear()}`;
const KIND_NOTE: Record<string, string> = {
  panel: "Panel online: no entra en la media",
  partisan: "Encuesta de partido: no entra en la media",
  reestimate: "Reestimación del CIS: no entra en la media",
};

/** Periodo de veda (LOREG art. 69.7): no se pueden publicar encuestas. */
export function inVeda(veda?: { from: string; to: string }, now = new Date()): boolean {
  if (!veda) return false;
  return now >= new Date(veda.from + "T00:00:00+01:00") && now < new Date(veda.to);
}

export function renderPolls(ctx: RenderContext) {
  const { chart, plot, width } = ctx;
  const fmt = nf("es", 1);
  const parties: string[] = chart.parties;
  const lastPoll = d(chart.last_poll);
  const days = RANGES[ctx.state.range ?? "all"];
  const from = days ? new Date(lastPoll.getTime() - days * 864e5) : d(chart.election_2023);

  const rows = chart.rows.filter((r: Row) => d(r.date) >= from);
  const polls = rows.filter((r: Row) => r.series === "poll");
  const avg = rows.filter((r: Row) => r.series === "avg");

  const narrow = width < 560;
  const height = Math.round(Math.min(Math.max(width * 0.55, 320), 480));
  const m = { top: 24, right: narrow ? 14 : 120, bottom: 30, left: 4 };
  const x = scaleTime().domain([from, ELECTION]).range([m.left, width - m.right]);
  const yMax = Math.max(...rows.map((r: Row) => r.value), ...chart.results_2023.map((r: Row) => r.value));
  const ticks = niceTicks(yMax, 0, narrow ? 4 : 5);
  const y = scaleLinear().domain([0, ticks[ticks.length - 1]]).range([height - m.bottom, m.top]);

  const root = svg("svg", { width, height, viewBox: `0 0 ${width} ${height}`, class: "chart-svg" });
  plot.appendChild(root);

  // Rejilla
  const grid = svg("g", { class: "grid" }, root);
  for (const t of ticks) {
    svg("line", { x1: m.left, x2: width - m.right, y1: y(t), y2: y(t), class: t === 0 ? "baseline" : "gridline" }, grid);
    svg("text", { x: m.left, y: y(t) - 5, class: "tick" }, grid).textContent = `${fmt(t)} %`;
  }
  for (const t of x.ticks(narrow ? 4 : 7)) {
    const lbl = svg("text", { x: x(t), y: height - 8, class: "tick", "text-anchor": "middle" }, grid);
    lbl.textContent = days && days <= 92 ? `${t.getDate()} ${MONTHS[t.getMonth()]}` : `${MONTHS[t.getMonth()]} ${String(t.getFullYear()).slice(2)}`;
  }

  // Tramo hasta las elecciones y marca del 29N
  const xe = x(ELECTION), xl = x(lastPoll);
  svg("rect", { x: xl, y: m.top, width: Math.max(xe - xl, 0), height: height - m.top - m.bottom, class: "future" }, root);
  svg("line", { x1: xe, x2: xe, y1: m.top - 8, y2: height - m.bottom, class: "election-line" }, root);
  svg("text", { x: xe, y: m.top - 12, class: "election-label", "text-anchor": "end" }, root).textContent = "29N";

  // Resultados de 2023 (solo si el inicio del eje es la elección)
  if (!days) {
    const x0 = x(d(chart.election_2023));
    for (const r of chart.results_2023) {
      svg("rect", { x: x0 - 1, y: y(r.value) - 5, width: 10, height: 10, class: "result-mark", fill: partyColor(r.party), transform: `rotate(45 ${x0 + 4} ${y(r.value)})` }, root);
    }
  }

  // Puntos de cada encuesta, debajo de las medias
  const dots = svg("g", { class: "poll-dots" }, root);
  for (const r of polls) {
    const hollow = r.kind !== "poll";
    svg("circle", {
      cx: x(d(r.date)), cy: y(r.value), r: narrow ? 2 : 2.6,
      fill: hollow ? "none" : partyColor(r.party), stroke: hollow ? partyColor(r.party) : "none",
      "stroke-width": hollow ? 1 : 0, class: "poll-dot",
    }, dots);
  }

  // Medias
  const byParty = new Map<string, { x: Date; y: number }[]>();
  for (const r of avg) {
    if (!byParty.has(r.party)) byParty.set(r.party, []);
    byParty.get(r.party)!.push({ x: d(r.date), y: r.value });
  }
  const path = d3line<{ x: Date; y: number }>().x((p) => x(p.x)).y((p) => y(p.y)).curve(curveMonotoneX);
  const ends: { party: string; y: number; v: number }[] = [];
  for (const party of [...parties].reverse()) {
    const pts = byParty.get(party);
    if (!pts?.length) continue;
    pts.sort((a, b) => +a.x - +b.x);
    svg("path", { d: path(pts) ?? "", stroke: cssVar("--paper"), class: "line", "stroke-width": 5 }, root);
    svg("path", { d: path(pts) ?? "", stroke: partyColor(party), class: "line", "stroke-width": 2.25 }, root);
    const last = pts[pts.length - 1];
    svg("circle", { cx: x(last.x), cy: y(last.y), r: 4.5, fill: partyColor(party), stroke: cssVar("--paper"), "stroke-width": 2 }, root);
    ends.push({ party, y: y(last.y), v: last.y });
  }

  // Etiquetas directas: siempre (los colores de Vox y SALF necesitan etiqueta por contraste)
  ends.sort((a, b) => a.y - b.y);
  let prev = -Infinity;
  const lx = narrow ? null : xl + 10;
  for (const e of ends) {
    const yy = Math.max(e.y, prev + MIN_LABEL_GAP);
    prev = yy;
    if (lx === null) continue;
    const t = svg("text", { x: lx, y: yy + 4, class: "end-label" }, root);
    t.innerHTML = `<tspan class="end-name">${e.party}</tspan> <tspan class="end-value">${fmt(e.v)}</tspan>`;
  }

  legend(ctx.legend, [
    ...parties.filter((p) => byParty.has(p)).map((p) => ({ color: partyColor(p), label: p })),
    ...(!days ? [{ color: cssVar("--ink-3"), label: "◆ Resultado de 2023", kind: "dot" as const }] : []),
    { color: cssVar("--ink-3"), label: "○ No entra en la media", kind: "dot" as const },
  ]);

  // Tooltip: media en la fecha más cercana y encuestas de esa semana
  const tip = tooltip(plot);
  const dates = [...new Set(avg.map((r: Row) => r.date as string))].sort();
  const hover = svg("g", { class: "hover", style: "display:none" }, root);
  const vline = svg("line", { y1: m.top, y2: height - m.bottom, class: "crosshair" }, hover);
  const overlay = svg("rect", { x: m.left, y: 0, width: Math.max(xl - m.left, 1), height, fill: "transparent", tabindex: 0, class: "overlay" }, root);
  // Debajo de los puntos: así los puntos reciben su propio tooltip y el resto del área, el de la media
  root.insertBefore(overlay, dots);
  let idx = dates.length - 1;
  const showAt = (i: number) => {
    idx = Math.max(0, Math.min(dates.length - 1, i));
    const day = dates[idx];
    const xx = x(d(day));
    hover.style.display = "";
    vline.setAttribute("x1", String(xx));
    vline.setAttribute("x2", String(xx));
    const vals = avg.filter((r: Row) => r.date === day).sort((a: Row, b: Row) => b.value - a.value);
    const week = polls.filter((r: Row) => Math.abs(+d(r.date) - +d(day)) <= 3.5 * 864e5);
    const firms = [...new Set(week.map((r: Row) => r.pollster))];
    const note = firms.length ? `<div class="tip-note">Encuestas de esa semana: ${firms.slice(0, 5).join(", ")}${firms.length > 5 ? "…" : ""}</div>` : "";
    tip.show(xx, m.top + 10, `<div class="tip-title">Media a ${fmtDay(d(day))}</div>${note}${vals.map((r: Row) => tipRow(partyColor(r.party), r.party, `${fmt(r.value)} %`)).join("")}`);
  };
  const hide = () => { hover.style.display = "none"; tip.hide(); };
  overlay.addEventListener("pointermove", (e) => {
    const rect = root.getBoundingClientRect();
    const t = +x.invert(e.clientX - rect.left);
    let best = 0;
    dates.forEach((dd, i) => { if (Math.abs(+d(dd) - t) < Math.abs(+d(dates[best]) - t)) best = i; });
    showAt(best);
  });
  overlay.addEventListener("pointerleave", hide);
  overlay.addEventListener("focus", () => showAt(idx));
  overlay.addEventListener("blur", hide);
  overlay.addEventListener("keydown", (e) => {
    if (e.key === "ArrowLeft") { showAt(idx - 1); e.preventDefault(); }
    if (e.key === "ArrowRight") { showAt(idx + 1); e.preventDefault(); }
  });

  // Las encuestas individuales, accesibles al pasar por encima de un punto
  dots.addEventListener("pointermove", (e) => {
    const t = e.target as SVGCircleElement;
    if (t.tagName !== "circle") return;
    const i = [...dots.children].indexOf(t);
    const r = polls[i];
    if (!r) return;
    const who = r.commissioner ? `${r.pollster} para ${r.commissioner}` : r.pollster;
    const extra = KIND_NOTE[r.kind] ? `<div class="tip-note">${KIND_NOTE[r.kind]}</div>` : "";
    const rect = root.getBoundingClientRect();
    tip.show(e.clientX - rect.left, e.clientY - rect.top, `<div class="tip-title">${who}</div><div class="tip-note">${fmtDay(d(r.date))}${r.sample ? `. ${r.sample.toLocaleString("es-ES")} entrevistas` : ""}</div>${extra}${tipRow(partyColor(r.party), r.party, `${fmt(r.value)} %`, true)}`);
    e.stopPropagation();
  });
  dots.addEventListener("pointerleave", () => tip.hide());
}
