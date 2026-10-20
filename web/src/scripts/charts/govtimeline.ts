// Quién gobierna: una fila por comunidad (y el Gobierno de España arriba), con un tramo por presidencia
// coloreado por partido. Los partidos sin color propio (regionalistas pequeños, UCD, CDS...) van en gris con su sigla.
import { scaleTime } from "d3-scale";
import { svg, cssVar, PARTY_VAR, tooltip, legend, fmtDay as fmtDate, type Lang, type RenderContext, type Row } from "./core";

// CiU, PDeCAT y Junts comparten color (mismo espacio político): una sola entrada de leyenda
const JUNTS_FAMILY = ["CiU", "PDeCAT", "JxCat"];
const TXT = {
  es: {
    label: { PP: "PP (y AP)", PSOE: "PSOE (y PSC)", JUNTS: "CiU, PDeCAT y Junts", OTHER: "Otros (UCD, CDS, PRC, PAR, independientes...)" } as Record<string, string>,
    acting: ", en funciones", today: "hoy", spain: "España",
  },
  en: {
    label: { PP: "PP (and AP)", PSOE: "PSOE (and PSC)", JUNTS: "CiU, PDeCAT and Junts", OTHER: "Others (UCD, CDS, PRC, PAR, independents...)" } as Record<string, string>,
    acting: ", acting", today: "today", spain: "Spain",
  },
};

const govColor = (party: string) => cssVar(PARTY_VAR[party] ?? "--p-other");

/** Texto en tinta sobre rellenos claros y en blanco sobre los oscuros. */
function labelColor(hex: string): string {
  const m = hex.match(/^#?([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})$/i);
  if (!m) return cssVar("--ink");
  const [r, g, b] = m.slice(1).map((x) => parseInt(x, 16) / 255).map((c) => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4));
  const lum = 0.2126 * r + 0.7152 * g + 0.0722 * b;
  return lum > 0.22 ? "#151826" : "#ffffff";
}

const fmtDay = (lang: Lang, iso: string) => fmtDate(lang, new Date(iso + "T00:00:00"), "long");

export function renderGovTimeline(ctx: RenderContext) {
  const { chart, plot, width, focus, lang } = ctx;
  const T = TXT[lang];
  const today = new Date(chart.today + "T00:00:00");
  const order = ["ES", ...Object.keys(chart.geos).filter((g) => g !== "ES").sort((a, b) => chart.geos[a][lang].localeCompare(chart.geos[b][lang], lang))];

  const narrow = width < 600;
  const rowH = narrow ? 20 : 22, gap = 4;
  const m = { top: 24, right: 8, bottom: 8, left: narrow ? 108 : 160 };
  const height = m.top + order.length * (rowH + gap) + 10 + m.bottom;
  const x = scaleTime().domain([new Date("1980-01-01"), today]).range([m.left, width - m.right]);

  const root = svg("svg", { width, height, viewBox: `0 0 ${width} ${height}`, class: "chart-svg" });
  plot.appendChild(root);

  for (const t of x.ticks(narrow ? 5 : 9)) {
    svg("line", { x1: x(t), x2: x(t), y1: m.top - 4, y2: height - m.bottom, class: "gridline" }, root);
    svg("text", { x: x(t), y: m.top - 10, class: "tick", "text-anchor": "middle" }, root).textContent = String(t.getFullYear());
  }

  const tip = tooltip(plot);
  const bars = svg("g", { class: "gov-bars" }, root);
  const names: SVGTextElement[] = [];
  order.forEach((code, i) => {
    // El Gobierno de España va separado del resto por un hueco
    const y0 = m.top + i * (rowH + gap) + (i > 0 ? 10 : 0);
    const strong = code === "ES" || code === focus;
    const name = svg("text", { x: m.left - 8, y: y0 + rowH / 2 + 4, class: `row-name${strong ? " strong" : ""}`, "text-anchor": "end" }, root);
    name.textContent = narrow && code === "ES" ? T.spain : chart.geos[code][lang];
    names.push(name);
    const mine = chart.rows.filter((r: Row) => r.ccaa === code);
    for (const r of mine) {
      const start = new Date(r.start + "T00:00:00");
      const end = r.end ? new Date(r.end + "T00:00:00") : today;
      const x0 = Math.max(x(start), m.left), x1 = x(end);
      if (x1 <= m.left) continue;
      const w = Math.max(x1 - x0, 1);
      const fill = govColor(r.party);
      const g = svg("g", { tabindex: 0, class: "gov" }, bars);
      svg("rect", { x: x0, y: y0, width: w, height: rowH, fill, class: "gov-bar", opacity: r.acting ? 0.6 : 1 }, g);
      // Sigla dentro del tramo si cabe
      if (w > r.party.length * 7.2 + 8 && r.party !== "Art. 155") {
        svg("text", { x: x0 + 4, y: y0 + rowH / 2 + 4, class: "gov-label", fill: labelColor(fill) }, g).textContent = r.party;
      }
      const who = lang === "en" && r.party === "Art. 155" ? "Direct rule by the Spanish government (art. 155)" : r.president;
      const html = `<div class="tip-title">${who}</div><div class="tip-note">${chart.geos[code][lang]}. ${r.party_label}${r.acting ? T.acting : ""}</div>` +
        `<div>${fmtDay(lang, r.start)} – ${r.end ? fmtDay(lang, r.end) : T.today}</div>`;
      const show = (cx: number, cy: number) => tip.show(cx, cy, html);
      g.addEventListener("pointermove", (e) => {
        const rect = root.getBoundingClientRect();
        show(e.clientX - rect.left, e.clientY - rect.top);
      });
      g.addEventListener("focus", () => show(x0 + w / 2, y0));
      g.addEventListener("pointerleave", () => tip.hide());
      g.addEventListener("blur", () => tip.hide());
    }
  });

  // Leyenda: solo los partidos que aparecen, de más a menos tiempo en el gobierno
  const time = new Map<string, number>();
  for (const r of chart.rows) {
    const key = JUNTS_FAMILY.includes(r.party) ? "JUNTS" : r.party in PARTY_VAR ? r.party : "OTHER";
    const end = r.end ? new Date(r.end) : today;
    time.set(key, (time.get(key) ?? 0) + (+end - +new Date(r.start)));
  }
  legend(ctx.legend, [...time.entries()].sort((a, b) => b[1] - a[1]).map(([k]) => ({
    color: k === "OTHER" ? cssVar("--p-other") : k === "JUNTS" ? cssVar("--p-junts") : govColor(k),
    label: T.label[k] ?? k,
    kind: "swatch" as const,
  })));

  // Entrada animada (GSAP, cargado aparte)
  import("./intros").then(({ introGovTimeline }) => introGovTimeline({
    plot, root, bars, names, x0: m.left, x1: width - m.right, top: m.top, bottom: height - m.bottom,
    year0: 1980, year1: today.getFullYear(),
  }));
}
