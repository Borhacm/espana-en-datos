import { p, type Theme } from "../../lib/content-types";

// El Congreso en datos. Página propia (views/Congress.astro). Cifras comprobadas contra data/charts/cg*.json
// (votaciones nominales del Pleno de la XV legislatura, datos abiertos del Congreso, descargados el 7 de octubre de 2026).
const theme: Theme = {
  id: "congreso",
  code: "CG",
  slug: { es: "congreso" },
  title: { es: "El Congreso en datos" },
  status: "published",
  hub: true,
  published: "2026-10-07",
  dek: {
    es: "Cómo han votado los partidos en las 2.173 votaciones nominales de la legislatura: quién coincide con quién, quién gana las votaciones y qué decretos del Gobierno cayeron.",
  },
  lenses: {
    tiempo: {
      lede: { es: "Tres años de votaciones, con los datos abiertos del propio Congreso." },
      body: [
        { h: { es: "Quién vota con quién" }, id: "coincidencias" },
        p("Si dos partidos votan lo mismo casi siempre, son aliados estables; si casi nunca, están en bloques opuestos. PP y PSOE han votado lo mismo en el 39 % de las votaciones. Las parejas que más coinciden son PP y UPN (91 %), ERC y EH Bildu (85 %) y PSOE y Sumar (83 %)."),
        p("Los socios de la investidura de 2023 no votan como un bloque. El PSOE coincide con el PNV en el 75 % de las votaciones y con Junts en el 62 %. Y PP y Vox, los dos mayores partidos de la oposición, han votado lo mismo en el 63 % de las ocasiones."),
        { fig: "cg1-coincidencias", code: "1" },

        { h: { es: "Quién gana las votaciones" }, id: "lado-ganador" },
        p("El PSOE, partido del Gobierno, ha quedado en el lado ganador en el 84 % de las votaciones de la legislatura, y el PP, primer partido de la oposición, en el 68 %. La distancia se ha estrechado: en 2024 el PSOE ganó entre el 84 % y el 94 % de las votaciones de cada trimestre, y en 2026, entre el 71 % y el 81 %. El PP ha pasado de entre el 58 % y el 74 % en 2024 a entre el 75 % y el 80 % en 2026."),
        { fig: "cg2-lado-ganador", code: "2" },

        { h: { es: "Los decretos que cayeron" }, id: "decretos" },
        p("Un decreto-ley entra en vigor al aprobarlo el Gobierno, pero el Congreso tiene que convalidarlo en un mes. Esta legislatura ha derogado 13: los 11 que ya figuran en los datos abiertos y los dos decretos de alquiler derogados el 2 de octubre de 2026, tres días antes de que se convocaran las elecciones."),
        p("En los 11 con votación publicada, PP y Vox votaron siempre en contra, y Junts en 10 de ellos. PSOE, Sumar, ERC y EH Bildu votaron siempre a favor. Un decreto más, el 8/2023, empató a 171 votos y se salvó en la repetición, que no figura en los datos abiertos."),
        { fig: "cg3-decretos-derogados", code: "3" },
        p("Estas cifras cuentan todas las votaciones por igual: una moción sin efectos legales pesa lo mismo que una ley. Sirven para ver alianzas y tendencias, no para medir la importancia de lo que se votó."),
      ],
    },
    europa: { lede: { es: "" }, body: [] },
    dentro: { lede: { es: "" }, body: [] },
  },
  sources: [
    { name: "Congreso de los Diputados, datos abiertos de votaciones", url: "https://www.congreso.es/es/opendata/votaciones" },
    { name: "Ministerio de la Presidencia: convalidación del Real Decreto-ley 8/2023 (10 de enero de 2024)", url: "https://www.mpr.gob.es/prencom/notas/Paginas/2024/100124-aprobados-decretos-leyes-prorroga-medidas.aspx" },
    { name: "BOE: derogación del Real Decreto-ley 26/2026", url: "https://www.boe.es/buscar/doc.php?id=BOE-A-2026-20526" },
  ],
};

export default theme;
