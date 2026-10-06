// Copia la salida del pipeline (../data) a public/data para que el navegador pueda leerla.
import { cpSync, existsSync, mkdirSync, rmSync } from "node:fs";

const src = new URL("../../data/", import.meta.url);
const dest = new URL("../public/data/", import.meta.url);
rmSync(dest, { recursive: true, force: true });
mkdirSync(dest, { recursive: true });
for (const part of ["base", "charts", "geo"]) {
  if (!existsSync(new URL(part, src))) continue;
  cpSync(new URL(part, src), new URL(part, dest), { recursive: true });
}
// Veda electoral (LOREG art. 69.7, ver src/lib/veda.ts): las encuestas no se publican ni se pueden descargar
const now = process.env.VEDA_TEST_NOW ? new Date(process.env.VEDA_TEST_NOW) : new Date();
if (now >= new Date("2026-11-24T00:00:00+01:00") && now < new Date("2026-11-29T21:00:00+01:00")) {
  for (const f of ["base/encuestas.json", "charts/el1-encuestas.json"]) rmSync(new URL(f, dest), { force: true });
  console.log("veda electoral: datos de encuestas retirados de public/data");
}
console.log("datos sincronizados en public/data");
