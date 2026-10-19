import { p, type Theme } from "../../lib/content-types";

// Cifras comprobadas contra data/charts/le*.json (INE y Eurostat), el Informe Anual 2025 del Banco de España y el informe de la
// AIReF sobre los presupuestos iniciales de 2026. Guion y tabla de verificación: editorial/registro/a01.md.
const theme: Theme = {
  id: "legislatura",
  code: "LE",
  slug: { es: "la-legislatura-en-datos" },
  title: { es: "La legislatura en datos: cómo ha cambiado España desde julio de 2023" },
  status: "published",
  published: "2026-10-07",
  updated: "2026-10-19",
  order: 2,
  dek: {
    es: "Las elecciones del 29N cierran la legislatura que empezó con las generales de julio de 2023. Desde entonces el paro ha bajado del 12,2 % al 10,5 %, aunque sigue siendo el más alto de la UE; el PIB ha crecido un 6,4 %, un tercio por el aumento de la población, y el déficit ha caído al 2,4 % del PIB, sobre todo en 2025 por el menor coste de las medidas de la crisis energética y la DANA, según la AIReF.",
  },
  lenses: {
    europa: {
      lede: { es: "España ha crecido más que la media europea y ha recortado distancia en paro y en deuda, pero sigue lejos de la media en los dos." },
      body: [
        p("En 2023, el año de las últimas generales, la tasa de paro de España era del 12,2 %, la más alta de los 27 países de la UE y el doble de la media europea (6,1 %). En 2025 había bajado al 10,5 %, mientras la media de la UE se quedaba en el 6,0 %. La distancia se ha reducido de 6,1 a 4,5 puntos, pero España sigue en el primer puesto. Le siguen Finlandia (9,7 %), donde el paro ha subido, y Grecia (8,9 %), donde ha bajado."),
        { fig: "lee1-europa-paro", code: "E1" },
        p("Entre 2023 y 2025, el PIB de España creció un 6,4 % descontada la inflación, más del doble que la media de la UE (2,8 %) y el octavo crecimiento de los 27. Pero su población también ha crecido más: un 2,1 %, el sexto aumento de la UE, frente al 0,5 % de la media. Por habitante, el PIB aumentó un 4,2 %, el undécimo de la UE, frente al 2,2 % de la media. Aproximadamente un tercio del crecimiento total se debe a que hay más habitantes."),
        { fig: "lee3-europa-crecimiento", code: "E2" },
        p("La deuda pública bajó del 105,2 % al 100,7 % del PIB entre 2023 y 2025, mientras la media de la UE subía del 80,5 % al 81,7 %. España es el quinto país más endeudado, por detrás de Grecia, Italia, Francia y Bélgica. Que la ratio baje no significa que se deba menos dinero: la deuda en euros ha seguido creciendo, pero menos que el PIB nominal, que sube con el crecimiento y con los precios."),
        { fig: "lee2-europa-deuda", code: "E3" },
      ],
    },
    dentro: {
      lede: { es: "El paro ha bajado más donde era más alto, y trabaja una parte mayor de la población en edad de hacerlo en casi todas las comunidades." },
      body: [
        p("En el último año (del tercer trimestre de 2025 al segundo de 2026), la tasa de paro media de España fue del 10,3 %, frente al 12,2 % de 2023. Ha bajado en las 17 comunidades, y más donde era más alta: en Extremadura, 4 puntos; en Andalucía y Canarias, 3,5, y en Asturias, 3,2. Donde menos, en el País Vasco (0,3) y Aragón (0,4), que ya partían de tasas bajas."),
        p("Así, las comunidades se han acercado. En 2023, entre la que tenía más paro (Andalucía, 18,2 %) y la que menos (el País Vasco, 7,7 %) había 10,5 puntos. En el último año, entre Andalucía (14,8 %) y Cantabria (7,3 %) hay 7,5. La distancia sigue siendo grande: Andalucía tiene el doble de paro que Cantabria."),
        { fig: "led1-paro-comunidades", code: "D1" },
        p("¿Se crea empleo solo porque hay más gente? En España había de media 22,5 millones de personas trabajando en el último año, 1,3 millones más que en 2023 (un 6,1 %). Una parte de ese aumento se debe a que la población crece. Para descontarlo, la tasa de empleo mide qué parte de la población trabaja. Entre las personas de 25 a 54 años, las edades en que más se trabaja, la tasa ha pasado del 78,0 % al 80,0 %."),
        p("Ha subido en 15 de las 17 comunidades. La mayor subida es la de Asturias (5,8 puntos). En el País Vasco ha bajado medio punto y en Aragón apenas ha cambiado, las dos con tasas altas (83,2 %). La más alta es la de Madrid (84,9 %) y la más baja, la de Andalucía (75,0 %). La EPA es una encuesta: en las comunidades menos pobladas tiene más margen de error y las diferencias pequeñas no son significativas."),
        { fig: "led3-tasa-empleo", code: "D2" },
        { see: { es: "Empleo: la reforma laboral, tres años después" }, href: "/empleo/" },
      ],
    },
    tiempo: {
      lede: { es: "Desde 2019, la mitad del crecimiento del PIB viene de una población mayor. Los salarios han recuperado el poder de compra perdido en 2022, y el déficit ha bajado con más ingresos." },
      body: [
        p("Una economía puede crecer porque hay más personas trabajando y consumiendo o porque cada persona produce más. Entre 2019, el último año antes de la pandemia, y 2025, el PIB de España creció un 10,0 %. La población aumentó un 4,8 % y el PIB por habitante, un 5,0 %: la mitad del crecimiento se debe a cada factor. Desde 2023, el PIB por habitante ha crecido más deprisa (un 4,2 %) que la población (un 2,1 %)."),
        p("El Banco de España, en su Informe Anual de 2025, atribuye el aumento del crecimiento potencial de la economía, por encima del 2 %, al dinamismo de la población, a un mayor crecimiento de la productividad y a la inversión. Buena parte del aumento de la población se debe a la inmigración."),
        { fig: "let4-crecimiento", code: "T1" },
        { see: { es: "Inmigración en datos" }, href: "/inmigracion/" },
        p("Entre 2023 y 2025, el salario medio por trabajador subió un 7,2 % y los precios de consumo, un 5,5 %. Descontada la inflación, el salario medio ha ganado un 1,6 % de poder de compra. Esa ganancia llega después de la pérdida de 2022, cuando los precios subieron un 8,4 % y los sueldos, un 4,6 %: si se compara con 2019, antes de la pandemia, el poder de compra del salario medio está prácticamente igual. Con una mirada más larga, desde 2008, el salario medio real está un 3,7 % por debajo."),
        { fig: "let2-salarios-precios", code: "T2" },
        { see: { es: "Nota: salarios reales y salario mínimo desde 2008" }, href: "/notas/salarios-reales-salario-minimo/" },
        p("El déficit público, la diferencia entre lo que gastan y lo que ingresan todas las administraciones, bajó del 3,3 % del PIB en 2023 al 2,4 % en 2025, el más bajo de la serie, que empieza en 2008, y por debajo del 3,1 % de la media de la UE. Los ingresos pasaron del 42,1 % al 42,9 % del PIB, el máximo de la serie, y el gasto, del 45,4 % al 45,3 %: casi toda la mejora está en los ingresos."),
        p("La AIReF (informe sobre los presupuestos iniciales de 2026, de abril de 2026) explica la bajada de 2025, del 3,2 % al 2,4 %: se debe sobre todo al menor coste de las medidas por la crisis energética y la DANA (ocho décimas) y de las operaciones no recurrentes (tres décimas), mientras que el resto de ingresos y gastos empujó el déficit tres décimas al alza. Para 2026, la AIReF prevé que el déficit suba al 2,6 % del PIB, sobre todo por dos paquetes de medidas aprobados ese año: uno por las borrascas y otro por la crisis en Oriente Medio."),
        { fig: "let5-ingresos-gastos", code: "T3" },
        p("Lo que no dicen estos datos. Ninguna de estas cifras depende solo del Gobierno central: influyen el ciclo económico europeo, el crecimiento de la población, los precios de la energía y las decisiones de comunidades y ayuntamientos, que también cuentan en el déficit y la deuda. Que suban los ingresos en proporción del PIB puede deberse a subidas de impuestos, a más empleo y beneficios o a que la inflación eleve lo recaudado, y los datos agregados no separan esos efectos. Los datos de 2025 de Eurostat son provisionales y pueden revisarse. Este balance describe cómo ha cambiado España en la legislatura, no reparte mérito ni culpa."),
      ],
    },
  },
  sources: [
    { name: "Banco de España: presentación del Informe Anual 2025 (18 de junio de 2026)", url: "https://www.bde.es/f/webbe/SES/Secciones/Publicaciones/PublicacionesAnuales/InformesAnuales/25/Fich/IIPP-2026-06-18-lopez-salido-es-or.pdf" },
    { name: "AIReF: Informe sobre los presupuestos iniciales de las administraciones públicas 2026 (15 de abril de 2026)", url: "https://www.airef.es/wp-content/uploads/2026/04/Presupuestos-iniciales-2026/Informe-Presupuestos-Iniciales-2026.pdf" },
    { name: "Protocolo (n.º 12) sobre el procedimiento aplicable en caso de déficit excesivo (valor de referencia del 3 % del PIB)", url: "https://eur-lex.europa.eu/legal-content/ES/TXT/HTML/?uri=CELEX:12008M/PRO/12" },
  ],
};

export default theme;
