// Comprueba el modelo del simulador: con el voto de 2023 y el reparto de 2023 debe dar el resultado real.
// Uso: npm run check:sim
import { buildSync } from "esbuild";
import { readFileSync, writeFileSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const dir = mkdtempSync(join(tmpdir(), "sim-"));
const out = join(dir, "model.mjs");
buildSync({ entryPoints: [new URL("../src/scripts/simulator-model.ts", import.meta.url).pathname], outfile: out, format: "esm", bundle: true });
const { simulate } = await import(out);
const data = JSON.parse(readFileSync(new URL("../../data/base/simulador.json", import.meta.url)));
const REAL_2023 = { PP: 137, PSOE: 121, Vox: 33, Sumar: 31, ERC: 7, Junts: 7, "EH Bildu": 6, PNV: 5, BNG: 1, CC: 1, UPN: 1 };

const input = Object.fromEntries(data.parties.map((p) => [p, data.national_2023[p] ?? 0]));
const { total } = simulate(input, data, "seats_2023");
const diff = Object.keys({ ...REAL_2023, ...total }).filter((k) => (REAL_2023[k] ?? 0) !== (total[k] ?? 0));
console.log("2023 reproducido:", JSON.stringify(total));
const now = simulate(data.defaults, data).total;
console.log(`Media de encuestas (${data.defaults_date}):`, JSON.stringify(now), "suma", Object.values(now).reduce((a, b) => a + b, 0));
if (diff.length) { console.log("NO COINCIDE con 2023:", diff.map((k) => `${k} ${total[k] ?? 0} vs ${REAL_2023[k] ?? 0}`).join(", ")); process.exit(1); }
writeFileSync(join(dir, "ok"), "");
