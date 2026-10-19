import { p, type Note } from "../../lib/content-types";

// Cifras comprobadas contra data/charts/n02-*.json (INE, ETCL e IPC; Eurostat, earn_mw_cur) y el Real Decreto 126/2026.
// Tabla de verificación: editorial/registro/n02.md.
const note: Note = {
  id: "n02",
  code: "N02",
  slug: { es: "salarios-reales-salario-minimo" },
  title: { es: "Descontada la inflación, el salario medio está un 3,7 % por debajo de 2008 y el salario mínimo, un 43,9 % por encima" },
  dek: {
    es: "Entre 2008 y 2025 el salario medio sube un 32,0 % y los precios, un 37,1 %. El salario mínimo casi se duplica y pasa del 38,9 % al 58,1 % del salario medio.",
  },
  published: "2026-10-19",
  lens: "tiempo",
  theme: "empleo",
  body: [
    p("Los salarios y el salario mínimo, que el Gobierno fija cada año por real decreto, son dos de los asuntos económicos que llegan a las elecciones del 29 de noviembre. Los datos del INE permiten ver cómo han evolucionado desde 2008 una vez descontada la inflación."),
    p("El salario medio por trabajador pasa de 1.800 euros al mes en 2008 a 2.377 en 2025, con las pagas extra repartidas en doce meses: un 32,0 % más. Los precios suben en ese tiempo un 37,1 %. Descontada la inflación, el salario medio de 2025 es un 3,7 % menor que el de 2008. El punto más bajo de la serie es 2022, cuando los precios subieron más deprisa que los sueldos, y desde 2012 no ha vuelto al nivel de 2008."),
    p("El salario mínimo sigue otro camino. En doce pagas, pasa de 700 euros en 2008 a 1.381 en 2025, un 97,3 % más; descontada la inflación, un 43,9 %. La mayor subida fue la de 2019, un 22,2 %. En 2026 es de 1.221 euros en catorce pagas, según el Real Decreto 126/2026."),
    { fig: "n02-salario-real", code: "1" },
    p("El resultado es que el salario mínimo se acerca al medio: era el 38,9 % del salario medio en 2008 y el 58,1 % en 2025."),
    { fig: "n02-smi-salario-medio", code: "2" },
    p("Un aviso sobre las medias. El salario medio también cambia según quién trabaja: cuando se pierde sobre todo empleo de sueldo bajo, como en la crisis que empezó en 2008, la media sube aunque ningún salario lo haga. Por eso la caída real desde 2008 no quiere decir que cada trabajador cobre hoy un 3,7 % menos. Los efectos del salario mínimo sobre el empleo quedan fuera de esta nota."),
  ],
  sources: [
    { name: "BOE, Real Decreto 126/2026, por el que se fija el salario mínimo interprofesional para 2026", url: "https://www.boe.es/eli/es/rd/2026/02/18/126/con" },
  ],
};

export default note;
