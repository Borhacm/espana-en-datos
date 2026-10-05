// Modelo del simulador de escaños. Sin DOM: se puede comprobar en Node (scripts/check-simulator.mjs).
//
// 1. Para cada provincia, el voto de 2023 de cada partido se multiplica por (voto nacional elegido / voto nacional
//    de 2023). Es un «swing proporcional»: un partido que sube un 10 % sube un 10 % en todas partes.
// 2. Podemos se presentó dentro de Sumar en 2023: reparte su voto con la misma distribución territorial que Sumar.
// 3. SALF no se presentó: su voto se reparte igual en todas las provincias.
// 4. Los partidos que solo concurren en algunas provincias (ERC, Junts, PNV...) mantienen su voto de 2023.
// 5. En cada provincia, D'Hondt entre las candidaturas con al menos el 3 % del voto válido (LOREG, art. 163).

export interface SimProvince { geo: string; name: string; seats: number; seats_2023: number; share_2023: Record<string, number> }
export interface SimData {
  parties: string[];
  regional: string[];
  national_2023: Record<string, number>;
  defaults: Record<string, number>;
  threshold: number;
  provinces: SimProvince[];
}

/** Voto provincial estimado (% del voto válido) a partir del voto nacional elegido. */
export function provinceShares(p: SimProvince, input: Record<string, number>, data: SimData): Record<string, number> {
  const n23 = data.national_2023;
  const s23 = p.share_2023;
  const out: Record<string, number> = {};
  for (const party of data.parties) {
    const v = input[party] ?? 0;
    if (!v) continue;
    if (party === "Podemos") out[party] = (s23.Sumar ?? 0) * v / n23.Sumar;
    else if (party === "SALF") out[party] = v;
    else if (s23[party] && n23[party]) out[party] = s23[party] * v / n23[party];
  }
  for (const party of data.regional) if (s23[party]) out[party] = s23[party];

  // Si el total pasa del 99 % (queda al menos un 1 % para blanco y otros), se recortan los partidos estatales
  const regional = data.regional.reduce((a, k) => a + (out[k] ?? 0), 0);
  const statewide = data.parties.reduce((a, k) => a + (out[k] ?? 0), 0);
  const room = 99 - regional;
  if (statewide > room) for (const k of data.parties) if (out[k]) out[k] *= room / statewide;
  return out;
}

/** D'Hondt: cada escaño va al cociente más alto (votos / (escaños ya ganados + 1)). Empate: más votos. */
export function dhondt(shares: Record<string, number>, seats: number, threshold: number): Record<string, number> {
  const eligible = Object.entries(shares).filter(([, v]) => v >= threshold);
  const won: Record<string, number> = Object.fromEntries(eligible.map(([k]) => [k, 0]));
  for (let i = 0; i < seats; i++) {
    let best = "", bestQ = -1, bestV = -1;
    for (const [k, v] of eligible) {
      const q = v / (won[k] + 1);
      if (q > bestQ || (q === bestQ && v > bestV)) { best = k; bestQ = q; bestV = v; }
    }
    if (!best) break;
    won[best]++;
  }
  return Object.fromEntries(Object.entries(won).filter(([, n]) => n > 0));
}

export function simulate(input: Record<string, number>, data: SimData, useSeats: "seats" | "seats_2023" = "seats") {
  const total: Record<string, number> = {};
  const byProvince: { geo: string; name: string; won: Record<string, number> }[] = [];
  for (const p of data.provinces) {
    const won = dhondt(provinceShares(p, input, data), p[useSeats], data.threshold);
    byProvince.push({ geo: p.geo, name: p.name, won });
    for (const [k, n] of Object.entries(won)) total[k] = (total[k] ?? 0) + n;
  }
  return { total, byProvince };
}
