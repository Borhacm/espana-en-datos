// Veda electoral (LOREG, art. 69.7): del 24 al 28 de noviembre de 2026 no se pueden publicar ni difundir encuestas.
// Termina al cerrar los colegios el 29 (21.00 en la península, cuando cierran también en Canarias).
export const VEDA = { from: "2026-11-24T00:00:00+01:00", to: "2026-11-29T21:00:00+01:00" };

/** ¿Estamos en veda? En el build se usa la hora de compilación; en el navegador, la del lector. */
export function inVedaAt(now = testNow() ?? new Date()): boolean {
  return now >= new Date(VEDA.from) && now < new Date(VEDA.to);
}

/** Para probar el build en veda: VEDA_TEST_NOW=2026-11-25T10:00:00+01:00 npm run build */
function testNow(): Date | null {
  const v = typeof process !== "undefined" ? process.env?.VEDA_TEST_NOW : undefined;
  return v ? new Date(v) : null;
}
