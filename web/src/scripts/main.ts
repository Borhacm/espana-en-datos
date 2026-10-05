import { CHARTS } from "../lib/charts-config";
import { dimLabel, type Chart, type Lang, type RenderContext } from "./charts/core";
import { renderLine } from "./charts/line";
import { renderRank, renderPaired, renderDumbbell } from "./charts/bars";
import { renderStack } from "./charts/stack";
import { renderMap } from "./charts/map";
import { renderPolls, inVeda } from "./charts/polls";
import { renderGovTimeline } from "./charts/govtimeline";
import { renderSpainMap } from "./charts/spainmap";

const RENDERERS = {
  line: renderLine,
  rank: renderRank,
  paired: renderPaired,
  dumbbell: renderDumbbell,
  stack: renderStack,
  map: renderMap,
  polls: renderPolls,
  govtimeline: renderGovTimeline,
  spainmap: renderSpainMap,
} as const;

// ---------- Comunidad destacada (preferencia del lector, solo en este navegador) ----------

const FOCUS_KEY = "ead-focus";
const DEFAULT_FOCUS = "";

function readFocus(): string | null {
  try {
    const v = localStorage.getItem(FOCUS_KEY);
    return v === null ? DEFAULT_FOCUS : v || null;
  } catch {
    return DEFAULT_FOCUS;
  }
}

function writeFocus(v: string | null) {
  try { localStorage.setItem(FOCUS_KEY, v ?? ""); } catch { /* sin almacenamiento: se usa el valor por defecto */ }
}

let focus = readFocus();
const redraws: (() => void)[] = [];

for (const sel of document.querySelectorAll<HTMLSelectElement>("select[data-focus-select]")) {
  sel.value = focus ?? "";
  sel.addEventListener("change", () => {
    focus = sel.value || null;
    writeFocus(focus);
    document.querySelectorAll<HTMLSelectElement>("select[data-focus-select]").forEach((s) => (s.value = sel.value));
    redraws.forEach((r) => r());
  });
}

// ---------- Montaje de cada figura ----------

const dataCache = new Map<string, Promise<Chart>>();
function load(id: string): Promise<Chart> {
  if (!dataCache.has(id)) dataCache.set(id, fetch(`/data/charts/${id}.json`).then((r) => {
    if (!r.ok) throw new Error(`${id}: ${r.status}`);
    return r.json();
  }));
  return dataCache.get(id)!;
}

function buildControls(el: HTMLElement, chart: Chart, id: string, lang: Lang, state: Record<string, string>, onChange: () => void) {
  const cfg = CHARTS[id];
  el.innerHTML = "";
  for (const c of cfg.controls ?? []) {
    const options = c.options ?? Object.keys(chart.dimensions?.[c.dim] ?? {});
    if (options.length < 2) continue;
    const group = document.createElement("div");
    group.className = "seg";
    group.setAttribute("role", "radiogroup");
    group.setAttribute("aria-label", c.dim);
    for (const opt of options) {
      const b = document.createElement("button");
      b.type = "button";
      b.setAttribute("role", "radio");
      b.setAttribute("aria-checked", String(state[c.dim] === opt));
      b.textContent = dimLabel(chart, c.dim, opt, lang);
      b.addEventListener("click", () => {
        state[c.dim] = opt;
        group.querySelectorAll("button").forEach((x) => x.setAttribute("aria-checked", String(x === b)));
        onChange();
      });
      group.appendChild(b);
    }
    el.appendChild(group);
  }
}

async function mount(fig: HTMLElement) {
  const id = fig.dataset.chart!;
  const lang = (fig.dataset.lang ?? "es") as Lang;
  const cfg = CHARTS[id];
  const plot = fig.querySelector<HTMLElement>("[data-plot]")!;
  const legendEl = fig.querySelector<HTMLElement>("[data-legend]")!;
  const controls = fig.querySelector<HTMLElement>("[data-controls]")!;
  const status = fig.querySelector<HTMLElement>("[data-status]");

  let chart: Chart;
  try {
    chart = await load(id);
  } catch {
    if (status) status.textContent = fig.dataset.error ?? "Error";
    return;
  }
  // Veda electoral: el gráfico de encuestas no se muestra (LOREG art. 69.7)
  if (inVeda(chart.veda)) {
    fig.classList.add("veda");
    const note = document.createElement("p");
    note.className = "veda-note";
    note.textContent = "La ley electoral prohíbe publicar encuestas durante los cinco días anteriores a la votación. Este gráfico volverá a mostrarse cuando cierren los colegios electorales.";
    fig.querySelector(".fig-head")?.after(note);
    return;
  }
  const state: Record<string, string> = {};
  for (const c of cfg.controls ?? []) state[c.dim] = c.default;

  let lastWidth = 0;
  const draw = async () => {
    const width = Math.floor(plot.clientWidth);
    if (!width) return;
    lastWidth = width;
    const ctx: RenderContext = { chart, cfg, lang, state, focus, plot, legend: legendEl, width };
    plot.querySelectorAll("svg.chart-svg").forEach((n) => n.remove());
    plot.querySelector(".tip")?.remove();
    status?.remove();
    await RENDERERS[cfg.renderer](ctx);
    plot.dataset.ready = "true";
  };

  buildControls(controls, chart, id, lang, state, draw);
  redraws.push(draw);
  await draw();
  new ResizeObserver(() => {
    if (Math.abs(Math.floor(plot.clientWidth) - lastWidth) > 4) draw();
  }).observe(plot);
}

// Redibujar si cambia el tema del sistema (los colores se leen de los tokens)
matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => redraws.forEach((r) => r()));

const figures = [...document.querySelectorAll<HTMLElement>("figure[data-chart]")];
const io = new IntersectionObserver((entries) => {
  for (const e of entries) {
    if (!e.isIntersecting) continue;
    io.unobserve(e.target);
    mount(e.target as HTMLElement);
  }
}, { rootMargin: "400px 0px" });
figures.forEach((f) => io.observe(f));

// Barra de secciones: pestaña activa al hacer scroll y desplazamiento lateral cuando no caben
const sectionNav = document.querySelector<HTMLElement>(".sectionbar nav");
const lensLinks = [...document.querySelectorAll<HTMLAnchorElement>(".sectionbar a[href^='#']")];
if (sectionNav && lensLinks.length) {
  const updateEdges = () => {
    const { scrollLeft, scrollWidth, clientWidth } = sectionNav;
    sectionNav.classList.toggle("more-left", scrollLeft > 2);
    sectionNav.classList.toggle("more-right", scrollLeft + clientWidth < scrollWidth - 2);
  };
  sectionNav.addEventListener("scroll", updateEdges, { passive: true });
  new ResizeObserver(updateEdges).observe(sectionNav);
  updateEdges();

  const sections = lensLinks.map((a) => document.getElementById(a.hash.slice(1))).filter((s): s is HTMLElement => !!s);
  const spy = new IntersectionObserver((entries) => {
    for (const e of entries) {
      if (!e.isIntersecting) continue;
      for (const a of lensLinks) {
        const active = a.hash === `#${e.target.id}`;
        a.classList.toggle("active", active);
        if (active) {
          a.setAttribute("aria-current", "location");
          // Centra la pestaña activa dentro de la barra (sin mover la página)
          const left = a.offsetLeft - (sectionNav.clientWidth - a.offsetWidth) / 2;
          sectionNav.scrollTo({ left, behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" });
        } else {
          a.removeAttribute("aria-current");
        }
      }
    }
  }, { rootMargin: "-40% 0px -55% 0px" });
  sections.forEach((s) => spy.observe(s));
}
