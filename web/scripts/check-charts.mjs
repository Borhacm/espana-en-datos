// Comprueba que todos los gráficos de la web compilada se dibujan.
// Uso: npm run build && npm run check   (necesita Chromium: npx playwright install chromium)
import { createServer } from "node:http";
import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { extname, join, relative } from "node:path";
import { chromium } from "playwright";

const DIST = new URL("../dist/", import.meta.url).pathname;
const PORT = 4400 + Math.floor(Math.random() * 400);

function pages(dir) {
  return readdirSync(dir).flatMap((name) => {
    const p = join(dir, name);
    if (statSync(p).isDirectory()) return pages(p);
    return name === "index.html" ? ["/" + relative(DIST, dir).replace(/\\/g, "/") + (relative(DIST, dir) ? "/" : "")] : [];
  });
}

// Servidor estático mínimo sobre dist/ (independiente de astro preview, que solo admite uno por proyecto)
const TYPES = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".json": "application/json", ".svg": "image/svg+xml" };
const server = createServer((req, res) => {
  let file = join(DIST, decodeURIComponent(new URL(req.url, "http://x").pathname));
  if (existsSync(file) && statSync(file).isDirectory()) file = join(file, "index.html");
  if (!existsSync(file)) { res.writeHead(404); res.end(); return; }
  res.writeHead(200, { "content-type": TYPES[extname(file)] ?? "application/octet-stream" });
  res.end(readFileSync(file));
}).listen(PORT, "127.0.0.1");
const base = `http://127.0.0.1:${PORT}`;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
const errors = [];
page.on("pageerror", (e) => errors.push(`${page.url()}: ${e.message}`));

let total = 0;
const failed = [];
// La raíz solo redirige a /es/
const paths = pages(DIST).filter((p) => p !== "/").sort();
for (const path of paths) {
  await page.goto(base + path, { waitUntil: "load" });
  const figs = await page.$$("figure[data-chart]");
  for (const f of figs) { await f.scrollIntoViewIfNeeded(); await page.waitForTimeout(150); }
  await page.waitForTimeout(600);
  const states = await page.$$eval("figure[data-chart]", (fs) => fs.map((f) => [f.id, f.querySelector("[data-plot]")?.dataset.ready === "true"]));
  total += states.length;
  for (const [id, ok] of states) if (!ok) failed.push(`${path}#${id}`);
}
await browser.close();
server.close();

console.log(`${total} gráficos comprobados en ${paths.length} páginas`);
for (const e of errors) console.log("ERROR JS", e);
for (const f of failed) console.log("NO SE DIBUJA", f);
process.exit(failed.length || errors.length ? 1 : 0);
