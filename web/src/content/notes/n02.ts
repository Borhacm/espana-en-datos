import { p, type Note } from "../../lib/content-types";

// Cifras comprobadas contra data/charts/n02-*.json (INE, ETCL e IPC; Eurostat, earn_mw_cur) y el Real Decreto 126/2026.
// Tabla de verificación: editorial/registro/n02.md.
const note: Note = {
  id: "n02",
  code: "N02",
  slug: { es: "salarios-reales-salario-minimo", en: "real-wages-minimum-wage" },
  title: { es: "Descontada la inflación, el salario medio está un 3,7 % por debajo de 2008 y el salario mínimo, un 43,9 % por encima", en: "Adjusted for inflation, the average wage is 3.7% below 2008 and the minimum wage 43.9% above" },
  dek: {
    es: "Entre 2008 y 2025 el salario medio sube un 32,0 % y los precios, un 37,1 %. El salario mínimo casi se duplica y pasa del 38,9 % al 58,1 % del salario medio.",
    en: "Between 2008 and 2025 the average wage rises 32.0% and prices 37.1%. The minimum wage almost doubles and goes from 38.9% to 58.1% of the average wage.",
  },
  published: "2026-10-19",
  lens: "tiempo",
  theme: "empleo",
  body: [
    p("Los salarios y el salario mínimo, que el Gobierno fija cada año por real decreto, son dos de los asuntos económicos que llegan a las elecciones del 29 de noviembre. Los datos del INE permiten ver cómo han evolucionado desde 2008 una vez descontada la inflación.", "Wages and the minimum wage, which the government sets each year by royal decree, are two of the economic issues going into the 29 November election. INE data shows how they have changed since 2008 once inflation is stripped out."),
    p("El salario medio por trabajador pasa de 1.800 euros al mes en 2008 a 2.377 en 2025, con las pagas extra repartidas en doce meses: un 32,0 % más. Los precios suben en ese tiempo un 37,1 %. Descontada la inflación, el salario medio de 2025 es un 3,7 % menor que el de 2008. El punto más bajo de la serie es 2022, cuando los precios subieron más deprisa que los sueldos, y desde 2012 no ha vuelto al nivel de 2008.", "The average wage per worker goes from 1,800 euros a month in 2008 to 2,377 in 2025, with extra payments spread over twelve months: 32.0% more. Prices rise 37.1% over that time. Adjusted for inflation, the average wage in 2025 is 3.7% lower than in 2008. The lowest point in the series is 2022, when prices rose faster than wages, and since 2012 it has not returned to its 2008 level."),
    p("El salario mínimo sigue otro camino. En doce pagas, pasa de 700 euros en 2008 a 1.381 en 2025, un 97,3 % más; descontada la inflación, un 43,9 %. La mayor subida fue la de 2019, un 22,2 %. En 2026 es de 1.221 euros en catorce pagas, según el Real Decreto 126/2026.", "The minimum wage follows another path. In twelve payments, it goes from 700 euros in 2008 to 1,381 in 2025, 97.3% more; adjusted for inflation, 43.9%. The largest rise was in 2019, 22.2%. In 2026 it is 1,221 euros in fourteen payments, under Royal Decree 126/2026."),
    { fig: "n02-salario-real", code: "1" },
    p("El resultado es que el salario mínimo se acerca al medio: era el 38,9 % del salario medio en 2008 y el 58,1 % en 2025.", "The result is that the minimum wage is closing in on the average: it was 38.9% of the average wage in 2008 and 58.1% in 2025."),
    { fig: "n02-smi-salario-medio", code: "2" },
    p("Un aviso sobre las medias. El salario medio también cambia según quién trabaja: cuando se pierde sobre todo empleo de sueldo bajo, como en la crisis que empezó en 2008, la media sube aunque ningún salario lo haga. Por eso la caída real desde 2008 no quiere decir que cada trabajador cobre hoy un 3,7 % menos. Los efectos del salario mínimo sobre el empleo quedan fuera de esta nota.", "A word of warning about averages. The average wage also changes with who is working: when mostly low-wage jobs are lost, as in the crisis that began in 2008, the average rises even if no wage does. So the real fall since 2008 does not mean that each worker earns 3.7% less today. The effects of the minimum wage on employment are outside the scope of this note."),
    { see: { es: "Empleo: la reforma laboral, tres años después", en: "Jobs: the labour reform, three years on" }, href: "/empleo/" },
  ],
  sources: [
    { name: { es: "BOE, Real Decreto 126/2026, por el que se fija el salario mínimo interprofesional para 2026", en: "BOE (official gazette), Royal Decree 126/2026 setting the 2026 minimum wage" }, url: "https://www.boe.es/eli/es/rd/2026/02/18/126/con" },
  ],
};

export default note;
