// Fuentes de los gráficos en inglés. El pipeline escribe el nombre, la tabla y la licencia de cada fuente en español;
// en la versión inglesa se traducen las descripciones y las licencias. Un nombre que no esté aquí se muestra tal cual:
// el nombre oficial de una estadística sigue siendo una cita válida.
import type { Lang } from "./i18n";

const EXACT: Record<string, string> = {
  // Nombres
  "Banco de España, Boletín Estadístico": "Bank of Spain, Statistical Bulletin",
  "Congreso de los Diputados, datos abiertos de votaciones": "Congress of Deputies, open data on votes",
  "Eurostat, Encuesta de Población Activa de la UE": "Eurostat, EU Labour Force Survey",
  "Eurostat, cuentas nacionales": "Eurostat, national accounts",
  "Eurostat, cuentas de las administraciones públicas": "Eurostat, government finance statistics",
  "Eurostat, encuesta de condiciones de vida (EU-SILC)": "Eurostat, Survey on Income and Living Conditions (EU-SILC)",
  "Eurostat, salarios mínimos mensuales": "Eurostat, monthly minimum wages",
  "Eurostat, sistema europeo de estadísticas de protección social (SEEPROS)": "Eurostat, European system of integrated social protection statistics (ESSPROS)",
  "Eurostat, SEEPROS": "Eurostat, ESSPROS",
  "Generalitat de Catalunya, fianzas de alquiler depositadas en el INCASÒL": "Catalan government, rental deposits lodged with INCASÒL",
  "INE, Encuesta Trimestral de Coste Laboral": "INE, Quarterly Labour Cost Survey",
  "INE, Encuesta de Población Activa": "INE, Labour Force Survey (EPA)",
  "INE, Estadística Continua de Población": "INE, Continuous Population Statistics",
  "INE, Indicadores Demográficos Básicos": "INE, Basic Demographic Indicators",
  "INE, cifras oficiales de población (revisión del padrón)": "INE, official population figures (municipal register)",
  "INE, Índice de Precios de Vivienda": "INE, House Price Index",
  "INE, Índice de Precios de Consumo": "INE, Consumer Price Index",
  "INE, Proyecciones de Población 2026-2075": "INE, Population Projections 2026-2075",
  "Ministerio del Interior, Infoelectoral": "Ministry of the Interior, Infoelectoral",
  "Ministerio de Sanidad, Sistema de Información sobre Listas de Espera del SNS (SISLE-SNS)": "Ministry of Health, National Health System Waiting List Information System (SISLE-SNS)",
  "Ministerio de Sanidad, Estadística de Gasto Sanitario Público": "Ministry of Health, Public Health Expenditure Statistics",
  "Resultados de 2023: Ministerio del Interior": "2023 results: Ministry of the Interior",
  "Presidentes del Gobierno (La Moncloa)": "Prime ministers (La Moncloa)",
  "Sector público": "Public sector",
  "Senado, cuadro de gobiernos autonómicos": "Senate, table of regional governments",
  "Zonas de mercado residencial tensionado": "Stressed residential market areas",
  "IGN, vía es-atlas (geometrías)": "IGN (National Geographic Institute), via es-atlas (boundaries)",
  "BOE, Real Decreto 806/2026 de convocatoria (diputados por circunscripción)": "BOE (official gazette), Royal Decree 806/2026 calling the election (deputies per constituency)",
  "BOE, Real Decreto 126/2026 (salario mínimo de 2026: 1.221 euros al mes en 14 pagas)": "BOE (official gazette), Royal Decree 126/2026 (2026 minimum wage: 1,221 euros a month in 14 payments)",
  // Conjuntos de datos
  "Cifras oficiales de población a 1 de enero de 2025": "Official population figures on 1 January 2025",
  "Convalidación o derogación de reales decretos-leyes": "Validation or repeal of royal decree-laws",
  "Encuestas recopiladas con su enlace original": "Polls collected with a link to the original",
  "Estudios sobre la Economía Española 2026/24, cuadro 9": "Estudios sobre la Economía Española 2026/24, table 9",
  "Ficheros MUNI 02202307": "MUNI 02202307 files",
  "Presidencias autonómicas": "Regional presidencies",
  "Indicadores resumen, situación a 31 de diciembre de cada año": "Summary indicators, position on 31 December each year",
  "Serie 2002-2024, gasto real (devengo)": "2002-2024 series, actual spending (accrual basis)",
  "Votaciones nominales del Pleno, XV legislatura": "Roll-call votes in the plenary, 15th parliament",
  "Votaciones nominales del Pleno, legislaturas X a XV": "Roll-call votes in the plenary, 10th to 15th parliaments",
  // Licencias
  "Reutilización libre citando la fuente": "Free reuse with attribution",
  "Cita de un estudio publicado": "Citation of a published study",
  "Reutilización libre citando la fuente (Ley 37/2007)": "Free reuse with attribution (Law 37/2007)",
  "Reutilización libre citando la fuente (aviso legal del Congreso)": "Free reuse with attribution (Congress legal notice)",
  "Llicència oberta d'ús d'informació (Catalunya)": "Open information use licence (Catalonia)",
};

const RULES: [RegExp, (...m: string[]) => string][] = [
  [/^Tabla (\d+)$/, (_, n) => `Table ${n}`],
  [/^Cuadro (\S+)$/, (_, n) => `Table ${n}`],
  [/^Tablas (.+)$/, (_, list) => `Tables ${list.replace(/ y /g, " and ")}`],
  [/^RDL (\S+) \(derogado el (\S+)\)$/, (_, d, date) => `RDL ${d} (struck down on ${date})`],
  [/^(\S+) y (\S+)$/, (_, a, b) => `${a} and ${b}`],
];

/** Texto de una fuente (nombre, tabla o licencia) en el idioma de la página */
export function srcText(s: string | undefined, lang: Lang): string {
  if (!s || lang === "es") return s ?? "";
  if (s in EXACT) return EXACT[s];
  for (const [re, f] of RULES) {
    const m = s.match(re);
    if (m) return f(...m);
  }
  return s;
}
