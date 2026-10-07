// Matriz fila x columna. Dos usos:
//  - "heat": porcentaje (0-100) con rampa secuencial de un solo tono (coincidencias entre partidos).
//  - "votes": voto de cada partido (si / no / abst) en cada fila (decretos derogados).
import { interpolateLab } from "d3-interpolate";
import { svg, cssVar, nf, tooltip, tipRow, legend, type RenderContext, type Row } from "./core";

const VOTE_LABEL: Record<string, string> = { si: "A favor", no: "En contra", abst: "Abstención" };
const VOTE_VAR: Record<string, string> = { si: "--vote-yes", no: "--vote-no", abst: "--vote-abst" };

/** Texto en tinta oscura sobre fondos claros y en blanco sobre los oscuros (sirve en modo claro y oscuro). */
function textOn(rgb: string): string {
  const [r, g, b] = (rgb.match(/\d+/g) ?? ["0", "0", "0"]).slice(0, 3).map((x) => +x / 255)
    .map((c) => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4));
  return 0.2126 * r + 0.7152 * g + 0.0722 * b > 0.22 ? "#151826" : "#ffffff";
}

export function renderMatrix(ctx: RenderContext) {
  const { chart, plot, width, cfg } = ctx;
  const mode = cfg.matrixMode ?? "heat";
  const fmt = nf("es", 0);
  const cols: string[] = chart.blocs;
  const rowKeys: string[] = mode === "heat" ? chart.blocs : [...new Set(chart.rows.map((r: Row) => r.row as string))];
  const cell = new Map<string, Row>(chart.rows.map((r: Row) => [`${r.row}|${r.col}`, r]));

  const narrow = width < 560;
  const left = mode === "heat" ? (narrow ? 76 : 84) : (narrow ? 78 : 104);
  const top = narrow ? 64 : 76;
  const size = Math.max(Math.min(Math.floor((width - left - 4) / cols.length), mode === "heat" ? 54 : 46), 18);
  const rowH = mode === "heat" ? size : Math.min(size, 30);
  const w = left + cols.length * size;
  const h = top + rowKeys.length * (rowH + 2);
  const showText = size >= 30;

  const root = svg("svg", { width: Math.max(w, width), height: h, viewBox: `0 0 ${Math.max(w, width)} ${h}`, class: "chart-svg matrix" });
  plot.appendChild(root);

  // Cabeceras de columna, giradas
  cols.forEach((c, j) => {
    const x = left + j * size + size / 2;
    svg("text", { x, y: top - 8, class: "row-name", transform: `rotate(-45 ${x} ${top - 8})`, "text-anchor": "start" }, root).textContent = c;
  });

  const lo = cssVar("--seq-0"), hi = cssVar("--seq-1");
  const tip = tooltip(plot);
  rowKeys.forEach((rk, i) => {
    const y = top + i * (rowH + 2);
    const label = mode === "heat" ? rk : `RDL ${rk}`;
    svg("text", { x: left - 8, y: y + rowH / 2 + 4, class: "row-name", "text-anchor": "end" }, root).textContent = label;
    cols.forEach((c, j) => {
      const r = cell.get(`${rk}|${c}`);
      const x = left + j * size;
      if (mode === "heat" && rk === c) {
        svg("rect", { x: x + 1, y, width: size - 2, height: rowH, class: "matrix-diag" }, root);
        return;
      }
      if (!r) {
        svg("rect", { x: x + 1, y, width: size - 2, height: rowH, class: "matrix-empty" }, root);
        return;
      }
      const t = mode === "heat" ? Math.max(0, Math.min(1, r.value / 100)) : 0;
      const fill = mode === "heat" ? interpolateLab(lo, hi)(t) : cssVar(VOTE_VAR[r.vote]);
      const g = svg("g", { tabindex: 0, class: "matrix-cell" }, root);
      svg("rect", { x: x + 1, y, width: size - 2, height: rowH, rx: 2, fill }, g);
      if (mode === "heat" && showText) {
        // Texto claro sobre las celdas oscuras de la rampa
        svg("text", { x: x + size / 2, y: y + rowH / 2 + 4, "text-anchor": "middle", class: "matrix-val", fill: textOn(fill) }, g)
          .textContent = fmt(r.value);
      }
      const html = mode === "heat"
        ? `<div class="tip-title">${rk} y ${c}</div><div>Votaron lo mismo en el <strong>${fmt(r.value)} %</strong> de ${r.n.toLocaleString("es-ES")} votaciones</div>`
        : `<div class="tip-title">RDL ${rk}</div><div class="tip-note">${chart.labels?.[rk] ?? ""}</div>` +
          `<div class="tip-note">Votación del ${r.date}: ${r.yes} a favor, ${r.no} en contra</div>` +
          tipRow(fill, c, VOTE_LABEL[r.vote], true);
      const show = (cx: number, cy: number) => tip.show(cx, cy, html);
      g.addEventListener("pointermove", (e) => {
        const rect = root.getBoundingClientRect();
        show(e.clientX - rect.left, e.clientY - rect.top);
      });
      g.addEventListener("focus", () => show(x + size / 2, y));
      g.addEventListener("pointerleave", () => tip.hide());
      g.addEventListener("blur", () => tip.hide());
    });
  });

  if (mode === "votes") {
    legend(ctx.legend, Object.entries(VOTE_LABEL).map(([k, label]) => ({ color: cssVar(VOTE_VAR[k]), label, kind: "swatch" as const })));
  } else {
    legend(ctx.legend, [
      { color: lo, label: "0 %: nunca votan igual", kind: "swatch" as const },
      { color: hi, label: "100 %: siempre votan igual", kind: "swatch" as const },
    ]);
  }
}
