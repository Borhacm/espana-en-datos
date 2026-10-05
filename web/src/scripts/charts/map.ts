import { geoAzimuthalEqualArea, geoPath, type GeoPermissibleObjects } from "d3-geo";
import { scaleLinear } from "d3-scale";
import { interpolateLab } from "d3-interpolate";
import { feature } from "topojson-client";
import type { Topology, GeometryCollection } from "topojson-specification";
import { svg, cssVar, nf, geoName, tooltip, tipRow, niceTicks, type RenderContext } from "./core";

type Feat = GeoJSON.Feature<GeoJSON.Geometry, { NUTS_ID: string; CNTR_CODE: string; NAME_LATN: string }>;

const cache = new Map<string, Promise<Feat[]>>();
function loadLevel(level: number): Promise<Feat[]> {
  if (!cache.has(String(level))) {
    cache.set(String(level), fetch(`/data/geo/nuts${level}.json`).then((r) => r.json()).then((topo: Topology) => {
      const obj = Object.values(topo.objects)[0] as GeometryCollection;
      return (feature(topo, obj) as unknown as GeoJSON.FeatureCollection).features as Feat[];
    }));
  }
  return cache.get(String(level))!;
}

// Marco de Europa continental (Canarias va en un recuadro aparte)
const FRAME: GeoJSON.MultiPoint = { type: "MultiPoint", coordinates: [[-10.5, 35], [34.5, 34.5], [31, 70.5], [-9, 64]] };
const isCanarias = (id: string) => id.startsWith("ES7");

export async function renderMap(ctx: RenderContext) {
  const { chart, lang, plot, focus, width } = ctx;
  const fmt = nf(lang, 1);
  const latest: string = chart.latest;
  const best: Record<string, number> = chart.best_level;
  const rows = chart.rows.filter((r) => r.time === latest && r.level === best[r.country]);
  const byId = new Map(rows.map((r) => [r.geo as string, r]));
  // Código NUTS de país (Eurostat y GISCO usan EL para Grecia), a partir de todas las filas de nivel 0
  const countryCode = new Map(chart.rows.filter((r) => r.level === 0).map((r) => [r.country as string, r.geo as string]));
  const focusCode = focus ? countryCode.get(focus) : undefined;

  const [l0, l1, l2] = await Promise.all([loadLevel(0), loadLevel(1), loadLevel(2)]);
  const levels = [l0, l1, l2];
  const shown: Feat[] = [];
  for (const r of rows) {
    const f = levels[r.level].find((q) => q.properties.NUTS_ID === r.geo);
    if (f) shown.push(f);
  }

  const height = Math.round(Math.min(Math.max(width * 0.82, 380), 700));
  const legendH = 44;
  const proj = geoAzimuthalEqualArea().rotate([-10, -52]).fitExtent([[4, legendH + 4], [width - 4, height - 4]], FRAME);
  const path = geoPath(proj);
  const insetW = Math.max(width * 0.2, 90), insetH = insetW * 0.55;
  // Arriba a la izquierda: en esta proyección es océano a cualquier ancho
  const insetBox: [[number, number], [number, number]] = [[8, legendH + 12], [8 + insetW, legendH + 12 + insetH]];
  const canarias = shown.filter((f) => isCanarias(f.properties.NUTS_ID));
  const insetProj = geoAzimuthalEqualArea().rotate([15.5, -28.3]).fitExtent(
    [[insetBox[0][0] + 6, insetBox[0][1] + 6], [insetBox[1][0] - 6, insetBox[1][1] - 6]],
    { type: "FeatureCollection", features: canarias } as GeoPermissibleObjects,
  );
  const insetPath = geoPath(insetProj);

  // Tope opcional de la escala (map_max): los valores por encima toman el color más intenso
  const cap: number | undefined = chart.map_max;
  const max = Math.min(Math.max(...rows.map((r) => r.value)), cap ?? Infinity);
  const ticks = niceTicks(max, 0, 4);
  const top = cap ?? Math.max(ticks[ticks.length - 1], max);
  const color = scaleLinear<string>().domain([0, top]).range([cssVar("--seq-0"), cssVar("--seq-1")]).interpolate(interpolateLab).clamp(true);

  const root = svg("svg", { width, height, viewBox: `0 0 ${width} ${height}`, class: "chart-svg map" });
  plot.appendChild(root);
  const clipId = `clip-${chart.id}`;
  const defs = svg("defs", {}, root);
  const clip = svg("clipPath", { id: clipId }, defs);
  svg("rect", { x: 0, y: legendH, width, height: height - legendH }, clip);

  // Fondo: países sin dato
  const base = svg("g", { "clip-path": `url(#${clipId})` }, root);
  for (const f of l0) {
    const d = path(f);
    if (d) svg("path", { d, class: "land-nodata" }, base);
  }

  const tip = tooltip(plot);
  const layer = svg("g", { "clip-path": `url(#${clipId})` }, root);
  const draw = (f: Feat, p: typeof path, g: SVGGElement) => {
    const r = byId.get(f.properties.NUTS_ID)!;
    const d = p(f);
    if (!d) return;
    const el = svg("path", { d, fill: color(r.value), class: "region" }, g);
    el.addEventListener("pointermove", (e) => {
      const rect = plot.getBoundingClientRect();
      const region = r.level === 0 ? geoName(chart, r.country, lang) : `${r.name}`;
      const sub = r.level === 0 ? "" : `<div class="tip-note">${geoName(chart, r.country, lang)}</div>`;
      tip.show(e.clientX - rect.left, e.clientY - rect.top, `<div class="tip-title">${region}</div>${sub}${tipRow(color(r.value), latest, `${fmt(r.value)} %`, true)}`);
    });
    el.addEventListener("pointerleave", () => tip.hide());
  };
  for (const f of shown) if (!isCanarias(f.properties.NUTS_ID)) draw(f, path, layer);

  // Contorno del país destacado
  if (focusCode) {
    const f = l0.find((q) => q.properties.NUTS_ID === focusCode);
    const d = f && path(f);
    if (d) svg("path", { d, class: "focus-outline", "clip-path": `url(#${clipId})` }, root);
  }

  // Recuadro de Canarias
  if (canarias.length) {
    const inset = svg("g", {}, root);
    svg("rect", { x: insetBox[0][0], y: insetBox[0][1], width: insetW, height: insetH, class: "inset-box" }, inset);
    for (const f of canarias) draw(f, insetPath, inset);
  }

  // Leyenda de escala continua
  const lw = Math.min(260, width - 110);
  const gradId = `grad-${chart.id}`;
  const grad = svg("linearGradient", { id: gradId }, defs);
  for (let i = 0; i <= 10; i++) svg("stop", { offset: `${i * 10}%`, "stop-color": color((top * i) / 10) }, grad);
  const lg = svg("g", { transform: "translate(8, 6)" }, root);
  const caption = svg("text", { x: 0, y: 10, class: "tick" }, lg);
  caption.textContent = `${chart.unit[lang]}, ${latest}`;
  svg("rect", { x: 0, y: 16, width: lw, height: 10, fill: `url(#${gradId})` }, lg);
  const lx = scaleLinear().domain([0, top]).range([0, lw]);
  for (const t of ticks) {
    const txt = svg("text", { x: lx(t), y: 38, class: "tick", "text-anchor": t === 0 ? "start" : "middle" }, lg);
    txt.textContent = cap !== undefined && t === top ? `≥ ${fmt(t)}` : fmt(t);
  }
  svg("rect", { x: lw + 16, y: 16, width: 10, height: 10, class: "land-nodata" }, lg);
  const nd = svg("text", { x: lw + 30, y: 25, class: "tick" }, lg);
  nd.textContent = lang === "es" ? "Sin datos" : "No data";

  ctx.legend.innerHTML = "";
  if (focus && !focusCode) return;
  if (focus && focusCode) {
    const lgd = document.createElement("span");
    lgd.className = "lg lg-outline";
    lgd.innerHTML = `<span class="key"></span>${geoName(chart, focus, lang)}`;
    ctx.legend.appendChild(lgd);
  }
}
