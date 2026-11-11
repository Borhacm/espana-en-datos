import { p, type Note } from "../../lib/content-types";

// Cifras comprobadas contra data/charts/n05-*.json y data/base/congreso-202307.json (Infoelectoral).
// Tabla de verificación: editorial/registro/n05.md.
const note: Note = {
  id: "n05",
  code: "N05",
  slug: { es: "cuanto-cuesta-un-escano", en: "cost-of-a-seat" },
  title: {
    es: "En 2023 un escaño costó menos de 65.000 votos al PP y al PSOE y más de 90.000 a Vox y a Sumar",
    en: "In 2023 a seat cost the PP and the PSOE fewer than 65,000 votes and Vox and Sumar more than 90,000",
  },
  dek: {
    es: "El Congreso se elige en 52 circunscripciones, la mayoría pequeñas. En 2023, 1,93 millones de votos, el 7,8 % del voto válido, fueron a candidaturas que no sacaron escaño en su provincia, y el reparto dio a los dos partidos más votados más escaños que su porcentaje de votos.",
    en: "Congress is elected in 52 constituencies, most of them small. In 2023, 1.93 million votes, 7.8% of the valid vote, went to lists that won no seat in their province, and the allocation gave the two parties with most votes more seats than their share of the vote.",
  },
  published: "2026-11-11",
  lens: "dentro",
  theme: "elecciones",
  body: [
    p("El 29 de noviembre no se reparten 350 escaños en toda España, sino unos pocos en cada provincia, con la regla D'Hondt y un mínimo del 3 % del voto válido de la provincia (artículos 162 y 163 de la LOREG). Cuántos diputados elige cada una decide cuántos votos hacen falta para entrar.", "On 29 November, 350 seats are not shared out across Spain as a whole but a few in each province, with the D'Hondt rule and a minimum of 3% of the valid vote in the province (Articles 162 and 163 of the electoral law, LOREG). How many deputies each one elects decides how many votes it takes to get in."),
    p("En julio de 2023, 1.930.424 votos, el 7,8 % del voto válido, fueron a candidaturas que no sacaron ningún escaño en su provincia. En Madrid, que eligió 37 diputados, fue el 1,3 %; en Teruel, con 3, el 35,2 %. En las 9 provincias que eligieron 2 o 3 diputados, casi uno de cada cuatro votos se quedó sin representación.", "In July 2023, 1,930,424 votes, 7.8% of the valid vote, went to lists that won no seat at all in their province. In Madrid, which elected 37 deputies, it was 1.3%; in Teruel, with 3, 35.2%. In the 9 provinces that elected 2 or 3 deputies, almost one vote in four was left unrepresented."),
    { fig: "n05-votos-sin-escano", code: "1" },
    p("Ese voto sin escaño se reparte de forma desigual entre partidos. Vox se quedó sin diputado en 27 provincias y Sumar en 33: allí quedaron el 16,1 % de los votos de Vox y el 19,9 % de los de Sumar. Al PP le pasó en 3 provincias (el 1,1 % de sus votos) y al PSOE en 2 (el 0,2 %). Por eso el PP, con el 33,1 % del voto válido, obtuvo el 39,1 % de los escaños, y el PSOE, con el 31,7 %, el 34,6 %, mientras que Vox (12,4 % de los votos) y Sumar (12,3 %) se quedaron en el 9,4 % y el 8,9 %.", "That vote without a seat is spread unevenly between parties. Vox won no deputy in 27 provinces and Sumar in 33: 16.1% of Vox's votes and 19.9% of Sumar's were cast there. It happened to the PP in 3 provinces (1.1% of its votes) and to the PSOE in 2 (0.2%). That is why the PP, with 33.1% of the valid vote, won 39.1% of the seats, and the PSOE, with 31.7%, won 34.6%, while Vox (12.4% of the votes) and Sumar (12.3%) ended up with 9.4% and 8.9%."),
    { fig: "n05-votos-escano", code: "2" },
    p("Los partidos que solo se presentan donde son fuertes también pagan poco por escaño: PNV, EH Bildu, Junts y UPN, entre 52.188 y 56.490 votos, menos que el PP. Lo contrario les pasó al BNG y a Coalición Canaria, con un diputado cada uno: el BNG lo sacó en A Coruña y sus votos de Lugo, Ourense y Pontevedra no dieron escaño, y Coalición Canaria lo sacó en Santa Cruz de Tenerife, pero no en Las Palmas.", "Parties that only stand where they are strong also pay little per seat: PNV, EH Bildu, Junts and UPN, between 52,188 and 56,490 votes, fewer than the PP. The opposite happened to the BNG and Coalición Canaria, with one deputy each: the BNG won it in A Coruña and its votes in Lugo, Ourense and Pontevedra won no seat, and Coalición Canaria won it in Santa Cruz de Tenerife but not in Las Palmas."),
    p("Lo que no dicen estos datos. No dicen qué habría pasado con otro sistema: con otras reglas, los votantes y los partidos también se habrían comportado de otra manera. Tampoco dicen por qué vota cada elector lo que vota: parte de quienes votaron a una candidatura sin escaño pudieron hacerlo sabiendo que era difícil que lo sacara. Cuántos habitantes representa cada diputado en cada comunidad está en la nota sobre quién gobierna dónde.", "What this data does not say. It does not say what would have happened under another system: with other rules, voters and parties would also have behaved differently. Nor does it say why each voter votes as they do: some of those who voted for a list that won no seat may have done so knowing it was unlikely to win one. How many inhabitants each deputy represents in each region is in the note on who governs where."),
    { see: { es: "Quién gobierna dónde y qué se juega cada comunidad el 29N", en: "Who governs where and what each region has at stake on 29 November" }, href: "/notas/quien-gobierna-donde-29n/" },
    { see: { es: "Elecciones generales del 29N", en: "29 November general election" }, href: "/elecciones-29n/" },
  ],
  sources: [
    { name: { es: "Ley Orgánica 5/1985, del Régimen Electoral General, artículos 162 y 163 (reparto de escaños)", en: "Organic Law 5/1985 on the General Electoral System, Articles 162 and 163 (seat allocation)" }, url: "https://www.boe.es/buscar/act.php?id=BOE-A-1985-11672" },
  ],
};

export default note;
