// Entradas animadas de los gráficos (GSAP + ScrollTrigger), cargadas solo donde hay gráficos que las usan.
// Cada gráfico se anima una sola vez por página, al entrar en pantalla; los redibujados posteriores
// (resize, controles) son estáticos. Sin animación si el lector pide menos movimiento.
// Nunca se ata la animación al scroll (scrub): un gráfico no debe quedarse con los datos a medias.
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);
export { gsap };

const played = new WeakSet<Element>();
const pending = new WeakMap<Element, gsap.core.Timeline>();

export const reducedMotion = () => matchMedia("(prefers-reduced-motion: reduce)").matches;

/** Crea la entrada de `host`; `setup` fija el estado inicial y añade los tweens a la línea de tiempo. */
export function intro(host: Element, setup: (tl: gsap.core.Timeline) => void) {
  // Cada redibujado crea un SVG nuevo: la entrada pendiente del anterior ya no vale.
  pending.get(host)?.scrollTrigger?.kill();
  pending.get(host)?.kill();
  pending.delete(host);
  host.removeAttribute("aria-busy");
  if (played.has(host) || reducedMotion()) return;
  const tl = gsap.timeline({
    paused: true,
    scrollTrigger: { trigger: host, start: "top 75%", once: true },
    // Mientras dura, la región se marca ocupada: un lector de pantalla no anuncia las cifras intermedias
    onStart: () => { played.add(host); host.setAttribute("aria-busy", "true"); },
  });
  setup(tl);
  const own = tl.eventCallback("onComplete");
  tl.eventCallback("onComplete", () => { own?.(); host.removeAttribute("aria-busy"); });
  pending.set(host, tl);
}

/** Cuenta de 0 a `v` en el texto de `el`. */
export function countUp(tl: gsap.core.Timeline, el: Element, v: number, fmt: (n: number) => string, at: number, duration = 1.2) {
  const n = { v: 0 };
  tl.call(() => { el.textContent = fmt(0); }, undefined, 0);
  tl.to(n, { v, duration, ease: "power2.out", onUpdate: () => { el.textContent = fmt(n.v); } }, at);
}

// EL-1. Encuestas: las medias se dibujan de izquierda a derecha, cada encuesta aparece cuando la línea
// llega a su fecha y los valores finales cuentan hasta su cifra.
export function introPolls(p: {
  plot: HTMLElement; lines: SVGPathElement[]; dots: SVGCircleElement[]; marks: SVGElement[]; ends: SVGCircleElement[];
  values: { el: SVGTSpanElement; v: number }[]; dotAt: (dot: SVGCircleElement) => number; fmt: (v: number) => string;
}) {
  intro(p.plot, (tl) => {
    const DRAW = 1.6;
    for (const l of p.lines) {
      const len = l.getTotalLength();
      gsap.set(l, { strokeDasharray: len, strokeDashoffset: len });
    }
    gsap.set([...p.dots, ...p.marks], { autoAlpha: 0 });
    gsap.set(p.ends, { scale: 0, transformOrigin: "50% 50%" });
    tl.eventCallback("onComplete", () => gsap.set(p.lines, { clearProps: "strokeDasharray,strokeDashoffset" }));
    tl.to(p.marks, { autoAlpha: 1, duration: 0.3, stagger: 0.04 })
      .to(p.lines, { strokeDashoffset: 0, duration: DRAW, ease: "power1.inOut" }, 0.15)
      .to(p.dots, { autoAlpha: 1, duration: 0.25, stagger: (_i, el) => p.dotAt(el) * DRAW }, 0.15)
      .to(p.ends, { scale: 1, duration: 0.4, ease: "back.out(2.5)", stagger: 0.05 }, 0.15 + DRAW - 0.1);
    for (const { el, v } of p.values) countUp(tl, el, v, p.fmt, 0.15, DRAW);
  });
}

// EL-2. Quién gobierna: un cursor recorre los años desde 1980 y va descubriendo las presidencias.
export function introGovTimeline(p: {
  plot: HTMLElement; root: SVGSVGElement; bars: SVGGElement; names: SVGTextElement[];
  x0: number; x1: number; top: number; bottom: number; year0: number; year1: number;
}) {
  intro(p.plot, (tl) => {
    const NS = "http://www.w3.org/2000/svg";
    const id = `gt-clip-${Math.random().toString(36).slice(2, 8)}`;
    const clip = document.createElementNS(NS, "clipPath");
    clip.id = id;
    const rect = document.createElementNS(NS, "rect");
    Object.entries({ x: 0, y: 0, width: p.x0, height: p.bottom + 10 }).forEach(([k, v]) => rect.setAttribute(k, String(v)));
    clip.appendChild(rect);
    p.root.prepend(clip);
    p.bars.setAttribute("clip-path", `url(#${id})`);

    const cursor = document.createElementNS(NS, "g");
    cursor.setAttribute("class", "year-cursor");
    cursor.innerHTML = `<line y1="${p.top - 4}" y2="${p.bottom}"></line><text y="${p.top - 10}" text-anchor="middle">${p.year0}</text>`;
    p.root.appendChild(cursor);
    const label = cursor.querySelector("text")!;
    gsap.set(cursor, { x: p.x0 });
    gsap.set(p.names, { autoAlpha: 0, x: -8 });

    const SWEEP = 2.2;
    const s = { x: p.x0 };
    tl.eventCallback("onComplete", () => {
      cursor.remove();
      p.bars.removeAttribute("clip-path");
      clip.remove();
    });
    tl.to(p.names, { autoAlpha: 1, x: 0, duration: 0.35, stagger: 0.025 })
      .to(s, {
        x: p.x1, duration: SWEEP, ease: "power1.inOut",
        onUpdate: () => {
          rect.setAttribute("width", String(s.x));
          gsap.set(cursor, { x: s.x });
          label.textContent = String(Math.round(p.year0 + ((s.x - p.x0) / (p.x1 - p.x0)) * (p.year1 - p.year0)));
        },
      }, 0.2)
      .to(cursor, { autoAlpha: 0, duration: 0.3 });
  });
}

// EL-3. Mapa: los territorios aparecen en onda, del centro hacia fuera.
export function introMap(p: { plot: HTMLElement; regions: { el: SVGPathElement; cx: number; cy: number }[]; cx: number; cy: number }) {
  intro(p.plot, (tl) => {
    const dist = p.regions.map((r) => Math.hypot(r.cx - p.cx, r.cy - p.cy));
    const max = Math.max(...dist, 1);
    const els = p.regions.map((r) => r.el);
    gsap.set(els, { autoAlpha: 0, scale: 0.6, transformOrigin: "50% 50%" });
    tl.eventCallback("onComplete", () => gsap.set(els, { clearProps: "transform,opacity,visibility" }));
    tl.to(els, { autoAlpha: 1, scale: 1, duration: 0.5, ease: "back.out(1.6)", stagger: (i) => (dist[i] / max) * 1.1 });
  });
}

// EL-SIM. Simulador: la barra de escaños crece partido a partido, los escaños cuentan y las sumas entran escalonadas.
export function introSimulator(p: { host: HTMLElement; segments: HTMLElement[]; cells: { el: HTMLElement; v: number }[]; combos: HTMLElement[] }) {
  intro(p.host, (tl) => {
    gsap.set(p.segments, { scaleX: 0, transformOrigin: "0% 50%" });
    gsap.set(p.combos, { autoAlpha: 0, y: 10 });
    tl.to(p.segments, { scaleX: 1, duration: 0.5, ease: "power2.out", stagger: 0.08 });
    for (const { el, v } of p.cells) countUp(tl, el, v, (n) => String(Math.round(n)), 0, 1.1);
    tl.to(p.combos, { autoAlpha: 1, y: 0, duration: 0.4, ease: "power2.out", stagger: 0.08 }, 0.6);
  });
}

let glide: gsap.core.Tween | undefined;

/** Desliza unos range inputs hasta sus nuevos valores, llamando a `update` en cada fotograma. */
export function glideInputs(inputs: HTMLInputElement[], target: Record<string, number>, update: () => void) {
  if (reducedMotion()) {
    inputs.forEach((i) => (i.value = String(target[i.name] ?? 0)));
    update();
    return;
  }
  const from = Object.fromEntries(inputs.map((i) => [i.name, +i.value]));
  const s = { t: 0 };
  glide?.kill();
  glide = gsap.to(s, {
    t: 1, duration: 0.7, ease: "power2.inOut",
    onUpdate: () => {
      inputs.forEach((i) => (i.value = String(from[i.name] + ((target[i.name] ?? 0) - from[i.name]) * s.t)));
      update();
    },
  });
}

/** Para el deslizamiento en curso (el lector ha cogido un control). */
export const stopGlide = () => glide?.kill();
