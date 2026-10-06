// Eventos de Google Analytics (propiedad común de bocal.online). gtag ya respeta el consentimiento
// (Consent Mode v2, ver components/Consent.astro): sin consentimiento solo se envían pings sin cookies.
//
//   chart_control     cambio en un control de un gráfico (chart_id, control_value)
//   chart_table_open  abre la tabla de datos de un gráfico (chart_id)
//   data_download     descarga el JSON de un gráfico (chart_id)
//   source_click      sigue el enlace a una fuente (chart_id, link_domain)
//   focus_region      elige una comunidad para destacar (region)
//   simulator_use     primera interacción con el simulador en la página (action)
//   simulator_preset  pulsa «Media de encuestas» o «Resultado de 2023» (preset)

type Params = Record<string, string | number | undefined>;

function send(name: string, params: Params = {}) {
  const gtag = (window as any).gtag;
  if (typeof gtag === "function") gtag("event", name, params);
}

const chartOf = (el: Element) => el.closest<HTMLElement>("figure[id]")?.id;

document.addEventListener("click", (e) => {
  const t = e.target as Element;
  const control = t.closest<HTMLButtonElement>("figure .controls [role=radio]");
  if (control) send("chart_control", { chart_id: chartOf(control), control_value: control.textContent ?? "" });

  const download = t.closest<HTMLAnchorElement>("figure a.download");
  if (download) send("data_download", { chart_id: chartOf(download) });

  const source = t.closest<HTMLAnchorElement>("figure .source a, .sources a, .src a");
  if (source) send("source_click", { chart_id: chartOf(source), link_domain: new URL(source.href).hostname });

  const preset = t.closest<HTMLButtonElement>("[data-sim] [data-preset]");
  if (preset) send("simulator_preset", { preset: preset.dataset.preset });
});

// <details> no emite click fiable al abrirse con teclado: se escucha «toggle» (no burbujea, por eso en captura)
document.addEventListener("toggle", (e) => {
  const d = e.target as HTMLDetailsElement;
  if (d.matches?.("figure details.table-view") && d.open) send("chart_table_open", { chart_id: chartOf(d) });
}, true);

document.addEventListener("change", (e) => {
  const sel = e.target as HTMLSelectElement;
  if (sel.matches?.("select[data-focus-select]") && sel.value) {
    send("focus_region", { region: sel.options[sel.selectedIndex]?.text ?? sel.value });
  }
});

// Simulador: solo la primera interacción por página (mover un deslizador emite decenas de eventos «input»)
let simUsed = false;
document.addEventListener("input", (e) => {
  if (simUsed || !(e.target as Element).closest?.("[data-sim]")) return;
  simUsed = true;
  send("simulator_use", { action: "slider" });
});
