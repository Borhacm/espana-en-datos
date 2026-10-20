import { p, type Theme } from "../../lib/content-types";

// El Congreso en datos. Página propia (views/Congress.astro). Cifras comprobadas contra data/charts/cg*.json
// (votaciones nominales del Pleno de la XV legislatura, datos abiertos del Congreso, descargados el 7 de octubre de 2026).
const theme: Theme = {
  id: "congreso",
  code: "CG",
  slug: { es: "congreso", en: "congress" },
  title: { es: "El Congreso en datos", en: "Congress in data" },
  status: "published",
  hub: true,
  published: "2026-10-07",
  dek: {
    es: "Cómo han votado los partidos en las 2.173 votaciones nominales de la legislatura: quién coincide con quién, quién gana las votaciones y qué decretos del Gobierno cayeron.",
    en: "How the parties have voted in the 2,173 roll-call votes of this parliament: who votes with whom, who wins the votes and which government decrees fell.",
  },
  lenses: {
    tiempo: {
      lede: { es: "Tres años de votaciones, con los datos abiertos del propio Congreso.", en: "Three years of votes, using Congress's own open data." },
      body: [
        { h: { es: "Quién vota con quién", en: "Who votes with whom" }, id: "coincidencias" },
        p("Si dos partidos votan lo mismo casi siempre, son aliados estables; si casi nunca, están en bloques opuestos. PP y PSOE han votado lo mismo en el 39 % de las votaciones. Las parejas que más coinciden son PP y UPN (91 %), ERC y EH Bildu (85 %) y PSOE y Sumar (83 %).", "If two parties almost always vote the same way, they are stable allies; if almost never, they are in opposing blocs. PP and PSOE have voted the same way in 39% of the votes. The pairs that agree most are PP and UPN (91%), ERC and EH Bildu (85%) and PSOE and Sumar (83%)."),
        p("Los socios de la investidura de 2023 no votan como un bloque. El PSOE coincide con el PNV en el 75 % de las votaciones y con Junts en el 62 %. Y PP y Vox, los dos mayores partidos de la oposición, han votado lo mismo en el 63 % de las ocasiones.", "The partners who backed the 2023 investiture do not vote as a bloc. The PSOE agrees with the PNV in 75% of the votes and with Junts in 62%. And PP and Vox, the two largest opposition parties, have voted the same way 63% of the time."),
        { fig: "cg1-coincidencias", code: "1" },

        { h: { es: "Quién gana las votaciones", en: "Who wins the votes" }, id: "lado-ganador" },
        p("El PSOE, partido del Gobierno, ha quedado en el lado ganador en el 84 % de las votaciones de la legislatura, y el PP, primer partido de la oposición, en el 68 %. La distancia se ha estrechado: en 2024 el PSOE ganó entre el 84 % y el 94 % de las votaciones de cada trimestre, y en 2026, entre el 71 % y el 81 %. El PP ha pasado de entre el 58 % y el 74 % en 2024 a entre el 75 % y el 80 % en 2026.", "The PSOE, the governing party, has been on the winning side in 84% of the votes of this parliament, and the PP, the main opposition party, in 68%. The gap has narrowed: in 2024 the PSOE won between 84% and 94% of the votes each quarter, and in 2026, between 71% and 81%. The PP has gone from between 58% and 74% in 2024 to between 75% and 80% in 2026."),
        { fig: "cg2-lado-ganador", code: "2" },

        { h: { es: "Los decretos que cayeron", en: "The decrees that fell" }, id: "decretos" },
        p("Un decreto-ley entra en vigor al aprobarlo el Gobierno, pero el Congreso tiene que convalidarlo en un mes. Esta legislatura ha derogado 13: los 11 que ya figuran en los datos abiertos y los dos decretos de alquiler derogados el 2 de octubre de 2026, tres días antes de que se convocaran las elecciones.", "A decree-law comes into force when the government approves it, but Congress has to validate it within a month. This parliament has struck down 13: the 11 already in the open data and the two rental decrees struck down on 2 October 2026, three days before the election was called."),
        p("En los 11 con votación publicada, PP y Vox votaron siempre en contra, y Junts en 10 de ellos. PSOE, Sumar, ERC y EH Bildu votaron siempre a favor. Un decreto más, el 8/2023, empató a 171 votos y se salvó en la repetición, que no figura en los datos abiertos.", "In the 11 with a published vote, PP and Vox always voted against, and Junts in 10 of them. PSOE, Sumar, ERC and EH Bildu always voted in favour. One more decree, 8/2023, tied at 171 votes and was saved in the repeat vote, which is not in the open data."),
        { fig: "cg3-decretos-derogados", code: "3" },
        p("Estas cifras cuentan todas las votaciones por igual: una moción sin efectos legales pesa lo mismo que una ley. Sirven para ver alianzas y tendencias, no para medir la importancia de lo que se votó.", "These figures count every vote equally: a motion with no legal effect weighs the same as a law. They show alliances and trends, not the importance of what was voted on."),
      ],
    },
    europa: { lede: { es: "", en: "" }, body: [] },
    dentro: { lede: { es: "", en: "" }, body: [] },
  },
  sources: [
    { name: { es: "Congreso de los Diputados, datos abiertos de votaciones", en: "Congress of Deputies, open data on votes" }, url: "https://www.congreso.es/es/opendata/votaciones" },
    { name: { es: "Ministerio de la Presidencia: convalidación del Real Decreto-ley 8/2023 (10 de enero de 2024)", en: "Ministry of the Presidency: validation of Royal Decree-law 8/2023 (10 January 2024)" }, url: "https://www.mpr.gob.es/prencom/notas/Paginas/2024/100124-aprobados-decretos-leyes-prorroga-medidas.aspx" },
    { name: { es: "BOE: derogación del Real Decreto-ley 26/2026", en: "BOE (official gazette): repeal of Royal Decree-law 26/2026" }, url: "https://www.boe.es/buscar/doc.php?id=BOE-A-2026-20526" },
  ],
};

export default theme;
