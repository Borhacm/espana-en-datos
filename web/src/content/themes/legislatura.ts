import { p, type Theme } from "../../lib/content-types";

// Cifras comprobadas contra data/charts/le*.json (INE y Eurostat, descargados el 7 de octubre de 2026).
// Tabla de verificación: editorial/registro/a01.md.
const theme: Theme = {
  id: "legislatura",
  code: "LE",
  slug: { es: "la-legislatura-en-datos" },
  title: { es: "La legislatura en datos: cómo ha cambiado España desde julio de 2023" },
  status: "published",
  published: "2026-10-07",
  order: 2,
  dek: {
    es: "Las elecciones del 29N cierran la legislatura que empezó con las generales de julio de 2023. Desde entonces, el paro ha bajado del 12,2 % al 10,3 %, hay 1,3 millones más de ocupados y el déficit ha caído al 2,4 % del PIB. Pero España sigue teniendo el paro más alto de la UE y una deuda pública de algo más del 100 % del PIB.",
  },
  lenses: {
    europa: {
      lede: { es: "España ha recortado distancia con la UE en paro y en deuda, pero sigue lejos de la media en los dos." },
      body: [
        p("En 2023, el año de las últimas generales, la tasa de paro de España era del 12,2 %, la más alta de los 27 países de la UE y el doble de la media europea (6,1 %). En 2025 había bajado al 10,5 %, mientras la media de la UE se quedaba en el 6,0 %. La distancia se ha reducido de 6,1 a 4,5 puntos, pero España sigue en el primer puesto. Le siguen Finlandia (9,7 %), donde el paro ha subido, y Grecia (8,9 %), donde ha bajado."),
        { fig: "lee1-europa-paro", code: "E1" },
        p("Con la deuda pública ha pasado algo parecido. Entre 2023 y 2025 bajó del 105,2 % al 100,7 % del PIB, mientras la media de la UE subía del 80,5 % al 81,7 %. España es el quinto país más endeudado, por detrás de Grecia, Italia, Francia y Bélgica. Que la ratio baje no significa que se deba menos dinero: la deuda en euros ha seguido creciendo, pero menos que el PIB nominal."),
        { fig: "lee2-europa-deuda", code: "E2" },
      ],
    },
    dentro: {
      lede: { es: "El paro ha bajado en las 17 comunidades, pero la distancia entre ellas sigue siendo grande." },
      body: [
        p("En el último año (del tercer trimestre de 2025 al segundo de 2026), la tasa de paro media de España fue del 10,3 %, frente al 12,2 % de 2023. Ha bajado en las 17 comunidades. Donde más, en Extremadura (4 puntos), Andalucía y Canarias (3,5 puntos cada una) y Asturias (3,2). Donde menos, en el País Vasco (0,3) y Aragón (0,4), que ya partían de tasas bajas."),
        p("Las diferencias se mantienen: Andalucía (14,8 %), Extremadura (13,4 %) y Canarias (12,6 %) siguen con las tasas más altas, y Cantabria (7,3 %), el País Vasco (7,5 %) y Madrid (7,6 %), con las más bajas."),
        { fig: "led1-paro-comunidades", code: "D1" },
        p("El número de ocupados ha crecido un 6,1 % desde 2023: en el último año hubo de media 22,5 millones de personas trabajando, 1,3 millones más que en 2023. Siete comunidades crecieron por encima de la media: Asturias (10,3 %), Baleares (7,8 %), Andalucía, Madrid y Murcia (7,4 % cada una), la Comunidad Valenciana (7,2 %) y Canarias (7,1 %). En el País Vasco, el empleo apenas ha cambiado (0,9 %)."),
        p("Hay que leer estas diferencias con prudencia. La EPA es una encuesta, y en las comunidades menos pobladas tiene más margen de error. Además, el número de ocupados crece también porque crece la población: no es una tasa."),
        { fig: "led2-empleo-comunidades", code: "D2" },
      ],
    },
    tiempo: {
      lede: { es: "El paro y el déficit están en sus niveles más bajos desde 2008. El salario medio ha ganado algo de poder de compra desde 2023 y está casi igual que en 2019." },
      body: [
        p("La tasa de paro media de los últimos cuatro trimestres, un 10,3 %, es la más baja desde 2008. En el segundo trimestre de 2026 fue del 9,9 %. El máximo de la serie fue el 26,9 % del primer trimestre de 2013."),
        { fig: "let1-paro", code: "T1" },
        p("Entre 2023 y 2025, el salario medio por trabajador subió un 7,2 % y los precios de consumo, un 5,5 %. Descontada la inflación, el salario medio ha ganado un 1,6 % de poder de compra. Esa ganancia llega después de la pérdida de 2022, cuando los precios subieron un 8,4 % y los sueldos, un 4,6 %: si se compara con 2019, antes de la pandemia, el poder de compra del salario medio está prácticamente igual."),
        { fig: "let2-salarios-precios", code: "T2" },
        p("El déficit público, la diferencia entre lo que gastan y lo que ingresan todas las administraciones, bajó del 3,3 % del PIB en 2023 al 2,4 % en 2025. Es el más bajo de toda la serie, que empieza en 2008, y queda por debajo del 3,1 % de la media de la UE y del valor de referencia del 3 % de las reglas fiscales europeas."),
        { fig: "let3-deficit", code: "T3" },
        p("Ninguno de estos datos depende solo del Gobierno central. Influyen el ciclo económico europeo, el crecimiento de la población, los precios de la energía y las decisiones de comunidades y ayuntamientos, que también cuentan en el déficit y la deuda. Este balance describe cómo ha cambiado España en la legislatura, no reparte mérito ni culpa."),
      ],
    },
  },
  sources: [
    { name: "Protocolo (n.º 12) sobre el procedimiento aplicable en caso de déficit excesivo (valor de referencia del 3 % del PIB)", url: "https://eur-lex.europa.eu/legal-content/ES/TXT/HTML/?uri=CELEX:12008M/PRO/12" },
  ],
};

export default theme;
