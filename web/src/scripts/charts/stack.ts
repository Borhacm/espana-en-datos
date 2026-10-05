import { scaleLinear } from "d3-scale";
import { svg, cssVar, nf, geoName, dimLabel, slice, tooltip, tipRow, legend, type RenderContext } from "./core";

const ORDER = ["abierto", "api", "cerrado"];
const VAR: Record<string, string> = { abierto: "--ord-3", api: "--ord-2", cerrado: "--ord-1" };
const BAR = 22;

/** Tinta o papel según la luminancia del relleno, para que la etiqueta siempre contraste. */
function labelColor(fill: string): string {
  const [r, g, b] = [1, 3, 5].map((i) => parseInt(fill.slice(i, i + 2), 16) / 255);
  const lum = 0.2126 * r + 0.7152 * g + 0.0722 * b;
  return lum > 0.45 ? "#0e1a33" : "#ffffff";
}
const GAP = 2;

/** Barras apiladas al 100 % por bloque (e3). */
export function renderStack(ctx: RenderContext) {
  const { chart, cfg, lang, plot, width } = ctx;
  const fmt = nf(lang, 0);
  const rows = slice(ctx);
  const blocs = (cfg.series ?? []).filter((g) => rows.some((r) => r.geo === g));
  const left = width < 520 ? 110 : 150;
  const rowH = 58;
  const m = { top: 8, right: 8, bottom: 8 };
  const height = m.top + blocs.length * rowH + m.bottom;
  const x = scaleLinear().domain([0, 100]).range([left, width - m.right]);

  const root = svg("svg", { width, height, viewBox: `0 0 ${width} ${height}`, class: "chart-svg" });
  plot.appendChild(root);
  const tip = tooltip(plot);

  blocs.forEach((g, i) => {
    const y = m.top + i * rowH + 8;
    const total = rows.find((r) => r.geo === g)?.total ?? 0;
    const name = svg("text", { x: left - 10, y: y + BAR / 2 + 1, class: "row-name strong", "text-anchor": "end" }, root);
    name.textContent = geoName(chart, g, lang);
    const n = svg("text", { x: left - 10, y: y + BAR / 2 + 17, class: "row-meta", "text-anchor": "end" }, root);
    n.textContent = lang === "es" ? `${total} modelos` : `${total} models`;

    let acc = 0;
    for (const a of ORDER) {
      const r = rows.find((q) => q.geo === g && q.access === a);
      if (!r || r.value <= 0) continue;
      const x0 = x(acc) + (acc > 0 ? GAP / 2 : 0);
      const x1 = x(acc + r.value) - (acc + r.value < 100 ? GAP / 2 : 0);
      acc += r.value;
      const fill = cssVar(VAR[a]);
      const seg = svg("g", { tabindex: 0 }, root);
      svg("rect", { x: x0, y, width: Math.max(x1 - x0, 0), height: BAR, fill, rx: 0 }, seg);
      const label = `${fmt(r.value)} %`;
      if (x1 - x0 > label.length * 8 + 12) {
        const t = svg("text", { x: x0 + 8, y: y + BAR / 2 + 5, class: "seg-label", fill: labelColor(fill) }, seg);
        t.textContent = label;
      }
      const show = () => tip.show(x0 + (x1 - x0) / 2, y,
        `<div class="tip-title">${geoName(chart, g, lang)}</div>${tipRow(fill, dimLabel(chart, "access", a, lang), `${fmt(r.value)} % (${r.count})`)}`);
      seg.addEventListener("pointerenter", show);
      seg.addEventListener("focus", show);
      seg.addEventListener("pointerleave", () => tip.hide());
      seg.addEventListener("blur", () => tip.hide());
    }
  });
  legend(ctx.legend, ORDER.map((a) => ({ color: cssVar(VAR[a]), label: dimLabel(chart, "access", a, lang), kind: "swatch" as const })));
}
