import { p, type Theme } from "../../lib/content-types";

// Cifras comprobadas contra data/charts/de*.json (INE y Eurostat, descargados el 14 de octubre de 2026).
// Tabla de verificación: editorial/registro/a03.md.
const theme: Theme = {
  id: "demografia",
  code: "DE",
  slug: { es: "demografia" },
  title: { es: "Demografía y pensiones: un país que envejece" },
  status: "published",
  published: "2026-10-14",
  order: 4,
  dek: {
    es: "En España nacen 1,10 hijos por mujer, el segundo dato más bajo de la UE, y se vive casi 11 años más que en 1975. Por cada 100 personas de 16 a 64 años ya hay 31,7 mayores de 64, casi el doble que entonces. Es el fondo de uno de los debates del 29N: cómo pagar las pensiones.",
  },
  lenses: {
    europa: {
      lede: { es: "Pocos países europeos tienen menos hijos que España, y pocos gastan más en pensiones." },
      body: [
        p("Las pensiones son una de las preguntas que los partidos tendrán que responder antes del 29N, y la demografía es su punto de partida: cuántos niños nacen, cuánto se vive y cuántas personas en edad de trabajar hay por cada jubilado."),
        p("En 2024, el indicador de fecundidad de España fue de 1,10 hijos por mujer, frente a 1,34 en la media de la UE. Solo Malta tiene un dato más bajo (1,01). Ningún país de la Unión llega a los 2,1 hijos por mujer con los que una población se mantiene sin migraciones: el más alto es Bulgaria (1,72), seguido de Francia (1,61)."),
        { fig: "dee1-europa-fecundidad", code: "E1" },
        p("España dedica a pensiones el 13,2 % del PIB, por encima de la media de la UE (12,6 %, dato provisional) y por debajo de Italia (15,9 %), Austria (15,6 %) y Francia (15,1 %). Es el séptimo porcentaje más alto de los 27. La definición europea incluye las pensiones de jubilación, viudedad, orfandad e incapacidad, también las de los funcionarios."),
        p("En 2008 la situación era la contraria: España gastaba el 9,2 % del PIB, menos que la media europea (11,8 %). Desde entonces, el gasto ha subido unos 4 puntos del PIB, el segundo mayor aumento de la UE después del de Finlandia."),
        { fig: "dee2-europa-pensiones", code: "E2" },
      ],
    },
    dentro: {
      lede: { es: "En Asturias hay casi el doble de mayores por cada persona en edad de trabajar que en Baleares." },
      body: [
        p("El 1 de enero de 2025 había en España 31,7 personas de 65 años o más por cada 100 de 16 a 64 años. La cifra cambia mucho de una comunidad a otra: 46,5 en Asturias, 44,7 en Castilla y León y 43,7 en Galicia, frente a 24,5 en Baleares, 25,7 en Murcia y 26,1 en Canarias."),
        p("No siempre fue así. En 1975, Asturias tenía 17,2 mayores por cada 100 personas en edad de trabajar, menos que Baleares (19,5). Desde entonces, Asturias ha sumado 29,3 puntos, la mayor subida de todas las comunidades, y Baleares, 5,0, la menor. En esa diferencia influyen la fecundidad, la esperanza de vida y las migraciones: la salida de jóvenes y la llegada de nuevos residentes."),
        { fig: "ded1-dependencia-comunidades", code: "D1" },
        p("La fecundidad también varía. En 2024, cuatro comunidades no llegaban a un hijo por mujer: Canarias (0,82), Asturias (0,95), Galicia (0,96) y Cantabria (0,99). Las más altas fueron Murcia (1,32), Navarra (1,20) y Castilla-La Mancha (1,19). Ninguna se acerca a 2,1."),
        { fig: "ded2-fecundidad-comunidades", code: "D2" },
      ],
    },
    tiempo: {
      lede: { es: "En medio siglo, los hijos por mujer se han quedado en menos de la mitad y la esperanza de vida ha subido más de diez años." },
      body: [
        p("En 1975 nacían en España 2,77 hijos por mujer. En 1981 el indicador bajó por primera vez de 2,1 (2,04) y siguió cayendo hasta 1,13 en 1998. Se recuperó hasta 1,44 en 2008 y desde entonces ha vuelto a bajar: 1,10 en 2024, el dato más bajo de la serie."),
        { fig: "det1-fecundidad", code: "T1" },
        p("A la vez, se vive más. La esperanza de vida al nacer ha pasado de 73,4 años en 1975 a 84,0 en 2024. La covid-19 la bajó de 83,5 años en 2019 a 82,3 en 2020, y en 2023 (83,8) ya había superado el nivel anterior a la pandemia."),
        { fig: "det2-esperanza-vida", code: "T2" },
        p("Menos nacimientos y vidas más largas se traducen en una población mayor. En 1975 había 16,8 personas de 65 años o más por cada 100 de 16 a 64 años; en 2025, 31,7, casi el doble. La cifra se mantuvo en torno a 25 durante la primera década de este siglo y ha subido todos los años desde 2008."),
        { fig: "det3-dependencia", code: "T3" },
        p("Sobre este fondo se aprobaron las reformas de las pensiones de 2021 y 2023. La Ley 21/2021 volvió a actualizar las pensiones cada año con la inflación, y el Real Decreto-ley 2/2023 subió las cotizaciones para reforzar los ingresos del sistema. Esta tasa de dependencia es una medida demográfica: cuánto pesan los mayores sobre quienes cotizan depende también de cuántas personas trabajan, a qué edad se jubilan y cuánta población llega de fuera."),
      ],
    },
  },
  sources: [
    { name: "Ley 21/2021, de garantía del poder adquisitivo de las pensiones", url: "https://www.boe.es/buscar/act.php?id=BOE-A-2021-21652" },
    { name: "Real Decreto-ley 2/2023, de ampliación de derechos de los pensionistas y nuevo marco de sostenibilidad del sistema público de pensiones", url: "https://www.boe.es/buscar/act.php?id=BOE-A-2023-6967" },
  ],
};

export default theme;
