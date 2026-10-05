// Mapa de España por provincia o municipio (Canarias en recuadro, proyección cónica conforme de España).
// Color: partido ganador; intensidad: su porcentaje de voto.
import { geoArea, geoPath } from "d3-geo";
import { geoConicConformalSpain } from "d3-composite-projections";
import { interpolateLab } from "d3-interpolate";
import { feature, mesh } from "topojson-client";
import type { Topology, GeometryCollection } from "topojson-specification";
import { svg, cssVar, nf, PARTY_VAR, tooltip, tipRow, legend, type RenderContext, type Row } from "./core";

type Feat = GeoJSON.Feature<GeoJSON.Geometry, { name: string }> & { id: string };

const cache = new Map<string, Promise<Topology>>();
function loadTopo(url: string): Promise<Topology> {
  if (!cache.has(url)) cache.set(url, fetch(`/data/${url}`).then((r) => r.json()));
  return cache.get(url)!;
}

// Intensidad: del 20 % (claro) al 60 % (color pleno) del voto del ganador
const LO = 20, HI = 60;

// Cada partido con color propio (PARTY_VAR); los que no lo tienen, en gris y con su nombre en la leyenda
function winnerColor(party: string): string {
  return cssVar(PARTY_VAR[party] ?? "--p-other");
}

/** d3-geo usa geometría esférica: un polígono con el giro cambiado se dibuja como «todo menos el municipio».
 *  Se comprueba polígono a polígono (no por municipio entero, porque en un multipolígono puede fallar solo uno). */
function fixPolygon(poly: GeoJSON.Position[][]) {
  if (geoArea({ type: "Polygon", coordinates: poly }) > 2 * Math.PI) poly.forEach((ring) => ring.reverse());
}
function rewind(f: Feat) {
  const g = f.geometry as GeoJSON.Polygon | GeoJSON.MultiPolygon;
  if (g.type === "Polygon") fixPolygon(g.coordinates);
  else if (g.type === "MultiPolygon") g.coordinates.forEach(fixPolygon);
}

export async function renderSpainMap(ctx: RenderContext) {
  const { chart, plot, width } = ctx;
  const fmt = nf("es", 1);
  const level = ctx.state.level ?? "provincia";
  const rows = chart.rows.filter((r: Row) => r.level === level);
  const byId = new Map<string, Row>(rows.map((r: Row) => [r.geo, r]));

  const topo = await loadTopo(chart.geometry[level]);
  const objName = level === "provincia" ? "provinces" : "municipalities";
  const feats = (feature(topo, topo.objects[objName] as GeometryCollection) as unknown as GeoJSON.FeatureCollection).features as Feat[];
  feats.forEach(rewind);

  const height = Math.round(Math.min(Math.max(width * 0.78, 300), 640));
  const proj = geoConicConformalSpain().fitExtent([[4, 4], [width - 4, height - 4]], { type: "FeatureCollection", features: feats } as any);
  const path = geoPath(proj);
  const paper = cssVar("--paper");

  const root = svg("svg", { width, height, viewBox: `0 0 ${width} ${height}`, class: "chart-svg map" });
  plot.appendChild(root);
  const g = svg("g", {}, root);
  const tip = tooltip(plot);

  for (const f of feats) {
    const r = byId.get(String(f.id));
    const t = r ? Math.max(0, Math.min(1, (r.value - LO) / (HI - LO))) : 0;
    const fill = r ? interpolateLab(paper, winnerColor(r.winner))(0.4 + 0.6 * t) : cssVar("--wash");
    const p = svg("path", { d: path(f) ?? "", fill, class: r ? "region" : "land-nodata", tabindex: level === "provincia" ? 0 : undefined }, g);
    if (!r) continue;
    const html = () => {
      const seats = r.seats ? Object.entries(r.seats as Record<string, number>).sort((a, b) => b[1] - a[1])
        .map(([k, v]) => `${k} ${v}`).join(", ") : "";
      return `<div class="tip-title">${r.name}</div>` +
        tipRow(winnerColor(r.winner), r.winner, `${fmt(r.value)} %`, true) +
        (r.second ? `<div class="tip-note">Ventaja sobre ${r.second}: ${fmt(r.margin)} puntos</div>` : "") +
        (r.turnout ? `<div class="tip-note">Participación: ${fmt(r.turnout)} %</div>` : "") +
        (seats ? `<div class="tip-note">Escaños: ${seats}</div>` : "");
    };
    p.addEventListener("pointermove", (e) => {
      const rect = root.getBoundingClientRect();
      tip.show(e.clientX - rect.left, e.clientY - rect.top, html());
    });
    p.addEventListener("pointerleave", () => tip.hide());
    p.addEventListener("focus", () => {
      const [cx, cy] = path.centroid(f);
      tip.show(cx, cy, html());
    });
    p.addEventListener("blur", () => tip.hide());
  }

  // Límites provinciales encima del mapa municipal, y el recuadro de Canarias
  if (level === "municipio") {
    const provObj = topo.objects.provinces as GeometryCollection;
    svg("path", { d: path(mesh(topo, provObj, (a, b) => a !== b)) ?? "", class: "prov-mesh" }, root);
  }
  svg("path", { d: (proj as any).getCompositionBorders(), class: "inset-box" }, root);

  // Leyenda: partidos que ganan en algún territorio, de más a menos
  const wins = new Map<string, number>();
  for (const r of rows) wins.set(r.winner, (wins.get(r.winner) ?? 0) + 1);
  const ranked = [...wins.entries()].sort((a, b) => b[1] - a[1]);
  const named = ranked.filter(([p]) => p in PARTY_VAR);
  const other = ranked.filter(([p]) => !(p in PARTY_VAR));
  const list = (xs: [string, number][]) => xs.map(([p, n]) => `${p} ${n.toLocaleString("es-ES")}`).join(", ");
  legend(ctx.legend, [
    ...named.map(([party, n]) => ({ color: winnerColor(party), label: `${party} (${n.toLocaleString("es-ES")})`, kind: "swatch" as const })),
    ...(other.length ? [{ color: cssVar("--p-other"), label: `Otros (${list(other)})`, kind: "swatch" as const }] : []),
  ]);
}
