// Explorador de votaciones del Congreso: el lector elige legislaturas (una o varias, que se suman), el tipo de
// votación y la vista. Los datos (data/base/congreso-explorador.json) llevan una fila por votación con la posición
// de cada partido codificada en una cadena: s (sí), n (no), a (abstención), . (sin posición).
import { renderMatrix } from "./charts/matrix";
import { renderLine } from "./charts/line";
import { cssVar, nf, PARTY_VAR, svg, tooltip, tipRow, type RenderContext } from "./charts/core";

interface Leg { id: string; label: string; from: string; to: string; n: number }
interface Data {
  legislatures: Leg[];
  blocs: string[];
  bloc_notes: Record<string, string>;
  types: Record<string, string>;
  votes: [number, string, string, number, string][]; // legislatura, AAAAMMDD, tipo, aprobada, posiciones
}

const POS: Record<string, string> = { s: "si", n: "no", a: "abst" };
const MIN_POSITIONS = 30; // un partido aparece si tiene posición en al menos 30 votaciones de la selección

const root = document.querySelector<HTMLElement>("[data-explorer]");
if (root) init(root);

async function init(root: HTMLElement) {
  const status = root.querySelector<HTMLElement>("[data-ex-status]")!;
  let data: Data;
  try {
    data = await fetch("/data/base/congreso-explorador.json").then((r) => r.json());
  } catch {
    status.textContent = "No se han podido cargar las votaciones.";
    return;
  }

  // Estado inicial: de la URL (para compartir) o por defecto la última legislatura
  const url = new URLSearchParams(location.search);
  const last = data.legislatures[data.legislatures.length - 1].id;
  const state = {
    legs: new Set((url.get("leg") ?? last).split(",").filter((l) => data.legislatures.some((x) => x.id === l))),
    type: url.get("tipo") && (url.get("tipo") === "todas" || url.get("tipo")! in data.types) ? url.get("tipo")! : "todas",
    view: ["matriz", "partido", "ganador"].includes(url.get("vista") ?? "") ? url.get("vista")! : "matriz",
    party: url.get("partido") ?? "PSOE",
  };
  if (!state.legs.size) state.legs.add(last);

  const legBox = root.querySelector<HTMLElement>("[data-ex-legs]")!;
  legBox.innerHTML = data.legislatures.map((l) =>
    `<label class="chip"><input type="checkbox" value="${l.id}"${state.legs.has(l.id) ? " checked" : ""}><span>${l.label}</span></label>`).join("");
  legBox.addEventListener("change", (e) => {
    const box = e.target as HTMLInputElement;
    if (box.checked) state.legs.add(box.value);
    else if (state.legs.size > 1) state.legs.delete(box.value);
    else box.checked = true; // siempre al menos una
    update();
  });
  root.querySelectorAll<HTMLButtonElement>("[data-ex-all]").forEach((b) => b.addEventListener("click", () => {
    data.legislatures.forEach((l) => state.legs.add(l.id));
    legBox.querySelectorAll("input").forEach((i) => (i.checked = true));
    update();
  }));

  segmented(root.querySelector("[data-ex-type]")!, [["todas", "Todas"], ...Object.entries(data.types)], () => state.type, (v) => { state.type = v; update(); });
  segmented(root.querySelector("[data-ex-view]")!, [["matriz", "Quién vota con quién"], ["partido", "Un partido frente a los demás"], ["ganador", "Quién gana las votaciones"]],
    () => state.view, (v) => { state.view = v; update(); });
  const partySel = root.querySelector<HTMLSelectElement>("[data-ex-party]")!;
  partySel.addEventListener("change", () => { state.party = partySel.value; update(); });

  const plot = root.querySelector<HTMLElement>("[data-ex-plot]")!;
  const legend = root.querySelector<HTMLElement>("[data-ex-legend]")!;
  const summary = root.querySelector<HTMLElement>("[data-ex-summary]")!;
  const table = root.querySelector<HTMLElement>("[data-ex-table]")!;
  const partyWrap = root.querySelector<HTMLElement>("[data-ex-party-wrap]")!;

  function update() {
    // URL compartible sin recargar
    const q = new URLSearchParams({ leg: [...state.legs].join(","), tipo: state.type, vista: state.view, partido: state.party });
    history.replaceState(null, "", `${location.pathname}?${q}`);

    const legIdx = new Set(data.legislatures.map((l, i) => (state.legs.has(l.id) ? i : -1)).filter((i) => i >= 0));
    const votes = data.votes.filter((v) => legIdx.has(v[0]) && (state.type === "todas" || v[2] === state.type));
    const counts = data.blocs.map((_, j) => votes.reduce((n, v) => n + (v[4][j] !== "." ? 1 : 0), 0));
    const present = data.blocs.map((b, j) => ({ b, j })).filter((x) => counts[x.j] >= MIN_POSITIONS);

    const legs = data.legislatures.filter((l) => state.legs.has(l.id));
    const from = votes.length ? fmtDate(votes.reduce((m, v) => (v[1] < m ? v[1] : m), votes[0][1])) : "";
    const to = votes.length ? fmtDate(votes.reduce((m, v) => (v[1] > m ? v[1] : m), votes[0][1])) : "";
    summary.textContent = votes.length
      ? `${votes.length.toLocaleString("es-ES")} votaciones${state.type !== "todas" ? ` (${data.types[state.type].toLowerCase()})` : ""} de ${legs.length === 1 ? `la legislatura ${legs[0].label}` : `${legs.length} legislaturas sumadas`}, del ${from} al ${to}.`
      : "No hay votaciones con esta selección.";

    // Selector de partido: solo los presentes en la selección
    if (!present.some((x) => x.b === state.party) && present.length) state.party = present.find((x) => x.b === "PSOE")?.b ?? present[0].b;
    partySel.innerHTML = present.map((x) => `<option value="${x.b}"${x.b === state.party ? " selected" : ""}>${x.b}</option>`).join("");
    partyWrap.hidden = state.view !== "partido";

    plot.innerHTML = "";
    legend.innerHTML = "";
    plot.parentElement?.querySelectorAll(":scope > .event-list").forEach((n) => n.remove());
    const width = Math.floor(plot.clientWidth);
    if (!votes.length || !width) { table.innerHTML = ""; return; }

    // Coincidencia entre dos partidos sobre las votaciones en que ambos tienen posición
    const pair = (a: number, b: number) => {
      let both = 0, same = 0;
      for (const v of votes) {
        const pa = v[4][a], pb = v[4][b];
        if (pa === "." || pb === ".") continue;
        both++;
        if (pa === pb) same++;
      }
      return { value: both ? Math.round((1000 * same) / both) / 10 : NaN, n: both };
    };

    if (state.view === "matriz") {
      const rows = [];
      for (const a of present) for (const b of present) {
        if (a.b === b.b) continue;
        const p = pair(a.j, b.j);
        if (p.n) rows.push({ row: a.b, col: b.b, value: p.value, n: p.n });
      }
      const ctx = fakeCtx({ blocs: present.map((x) => x.b), rows }, { renderer: "matrix", matrixMode: "heat" }, plot, legend, width);
      renderMatrix(ctx);
      table.innerHTML = matrixTable(present.map((x) => x.b), rows);
    } else if (state.view === "partido") {
      const me = present.find((x) => x.b === state.party);
      if (!me) return;
      const rows = present.filter((x) => x.b !== me.b).map((x) => ({ b: x.b, ...pair(me.j, x.j) })).filter((r) => r.n).sort((a, b) => b.value - a.value);
      bars(plot, rows, me.b, width);
      table.innerHTML = simpleTable(["Partido", `% de votaciones en que votó igual que ${me.b}`, "Votaciones comparadas"], rows.map((r) => [r.b, fmt1(r.value), r.n.toLocaleString("es-ES")]));
    } else {
      // Lado ganador por año (o por trimestre si solo hay una legislatura)
      const quarterly = state.legs.size === 1;
      const key = (d: string) => quarterly ? +d.slice(0, 4) + Math.floor((+d.slice(4, 6) - 1) / 3) / 4 : +d.slice(0, 4);
      const series = present.map((x) => x.b).filter((b) => ["PP", "PSOE"].includes(b) || b === state.party);
      const acc = new Map<string, [number, number]>();
      for (const v of votes) {
        for (const b of series) {
          const p = v[4][data.blocs.indexOf(b)];
          if (p !== "s" && p !== "n") continue;
          const k = `${b}|${key(v[1])}`;
          const a = acc.get(k) ?? [0, 0];
          a[0] += (p === "s") === (v[3] === 1) ? 1 : 0;
          a[1]++;
          acc.set(k, a);
        }
      }
      const rows = [...acc.entries()].filter(([, [, n]]) => n >= 10).map(([k, [w, n]]) => {
        const [series, t] = k.split("|");
        return { series, time: +t, value: Math.round((1000 * w) / n) / 10, n };
      });
      const colors = Object.fromEntries(series.map((b) => [b, PARTY_VAR[b] ?? "--context-strong"]));
      const ctx = fakeCtx({ rows, quarterly, unit: { es: "%" }, ref_line: { value: 50, label: { es: "50 %" } } },
        { renderer: "line", series, seriesColors: colors, digits: 0, domainMin: 0 }, plot, legend, width);
      renderLine(ctx);
      table.innerHTML = simpleTable(["Partido", quarterly ? "Trimestre" : "Año", "% en el lado ganador", "Votaciones"],
        rows.sort((a, b) => a.series.localeCompare(b.series) || a.time - b.time)
          .map((r) => [r.series, quarterly ? `T${Math.round((r.time % 1) * 4) + 1} ${Math.floor(r.time)}` : String(r.time), fmt1(r.value), String(r.n)]));
    }

    // Notas de los grupos que reúnen varios partidos
    const notes = present.map((x) => data.bloc_notes[x.b]).filter(Boolean);
    root.querySelector<HTMLElement>("[data-ex-notes]")!.innerHTML = [...new Set(notes)].map((n) => `<li>${n}</li>`).join("");
  }

  status.remove();
  update();
  let lastW = 0;
  new ResizeObserver(() => { const w = Math.floor(plot.clientWidth); if (Math.abs(w - lastW) > 4) { lastW = w; update(); } }).observe(plot);
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", update);
}

function segmented(el: HTMLElement, options: [string, string][], get: () => string, set: (v: string) => void) {
  el.innerHTML = "";
  el.setAttribute("role", "radiogroup");
  for (const [value, label] of options) {
    const b = document.createElement("button");
    b.type = "button";
    b.setAttribute("role", "radio");
    b.textContent = label;
    b.setAttribute("aria-checked", String(get() === value));
    b.addEventListener("click", () => {
      set(value);
      el.querySelectorAll("button").forEach((x) => x.setAttribute("aria-checked", String(x === b)));
    });
    el.appendChild(b);
  }
}

function fakeCtx(chart: any, cfg: any, plot: HTMLElement, legend: HTMLElement, width: number): RenderContext {
  return { chart: { id: "explorador", title: { es: "" }, unit: { es: "" }, geos: {}, ...chart }, cfg: { table: { rows: "", cols: "" }, ...cfg }, lang: "es", state: {}, focus: null, plot, legend, width };
}

/** Barras horizontales: coincidencia de un partido con cada uno de los demás. */
function bars(plot: HTMLElement, rows: { b: string; value: number; n: number }[], me: string, width: number) {
  const left = width < 520 ? 96 : 130, rowH = 26, bar = 14, top = 26;
  const height = top + rows.length * rowH + 6;
  const x = (v: number) => left + (v / 100) * (width - left - 44);
  const root = svg("svg", { width, height, viewBox: `0 0 ${width} ${height}`, class: "chart-svg" });
  plot.appendChild(root);
  for (const t of [0, 25, 50, 75, 100]) {
    svg("line", { x1: x(t), x2: x(t), y1: top - 6, y2: height, class: t === 0 ? "baseline" : "gridline" }, root);
    svg("text", { x: x(t), y: top - 12, class: "tick", "text-anchor": "middle" }, root).textContent = `${t} %`;
  }
  const tip = tooltip(plot);
  const f = nf("es", 0);
  rows.forEach((r, i) => {
    const y = top + i * rowH;
    const g = svg("g", { tabindex: 0, class: "bar-row" }, root);
    svg("text", { x: left - 10, y: y + rowH / 2 + 5, class: "row-name", "text-anchor": "end" }, g).textContent = r.b;
    const color = cssVar(PARTY_VAR[r.b] ?? "--context-strong");
    svg("rect", { x: x(0), y: y + (rowH - bar) / 2, width: Math.max(x(r.value) - x(0), 1), height: bar, rx: 3, fill: color }, g);
    svg("text", { x: x(r.value) + 6, y: y + rowH / 2 + 5, class: "row-value strong" }, g).textContent = `${f(r.value)} %`;
    const html = `<div class="tip-title">${me} y ${r.b}</div>${tipRow(color, "Votaron igual", `${f(r.value)} %`, true)}<div class="tip-note">${r.n.toLocaleString("es-ES")} votaciones comparadas</div>`;
    g.addEventListener("pointerenter", () => tip.show(x(r.value), y, html));
    g.addEventListener("focus", () => tip.show(x(r.value), y, html));
    g.addEventListener("pointerleave", () => tip.hide());
    g.addEventListener("blur", () => tip.hide());
  });
}

const fmt1 = (v: number) => (Number.isFinite(v) ? v.toLocaleString("es-ES", { maximumFractionDigits: 1 }) : "–");
const fmtDate = (d: string) => new Intl.DateTimeFormat("es-ES", { dateStyle: "long" }).format(new Date(`${d.slice(0, 4)}-${d.slice(4, 6)}-${d.slice(6, 8)}T12:00:00`));

function simpleTable(head: string[], rows: string[][]): string {
  return `<table><thead><tr>${head.map((h, i) => `<th scope="col"${i ? ' class="num"' : ""}>${h}</th>`).join("")}</tr></thead><tbody>${
    rows.map((r) => `<tr><th scope="row">${r[0]}</th>${r.slice(1).map((c) => `<td class="num">${c}</td>`).join("")}</tr>`).join("")}</tbody></table>`;
}

function matrixTable(blocs: string[], rows: { row: string; col: string; value: number }[]): string {
  const m = new Map(rows.map((r) => [`${r.row}|${r.col}`, r.value]));
  return simpleTable(["Partido", ...blocs], blocs.map((a) => [a, ...blocs.map((b) => (a === b ? "–" : fmt1(m.get(`${a}|${b}`) ?? NaN)))]));
}
