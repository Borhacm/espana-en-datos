import { p, type Theme } from "../../lib/content-types";

// Cifras comprobadas contra data/charts/in*.json (INE y Eurostat, descargados el 16 de octubre de 2026).
// Tabla de verificación: editorial/registro/a04.md.
const theme: Theme = {
  id: "inmigracion",
  code: "IN",
  slug: { es: "inmigracion" },
  title: { es: "Inmigración en datos" },
  status: "published",
  published: "2026-10-16",
  order: 5,
  dek: {
    es: "El 20,2 % de quienes viven en España nació en otro país, frente al 5,7 % de 2002. Es más que la media de la UE. Los nacidos fuera tienen una tasa de empleo algo más baja que los nacidos aquí, y el paro de los extranjeros es más alto que el de los españoles en todas las comunidades. Antes del 29N conviene partir de las cifras oficiales: desde 2013, la población nacida en España ha bajado y todo el aumento de la población se debe a los nacidos fuera.",
  },
  lenses: {
    europa: {
      lede: { es: "En España vive más población nacida fuera que en la media de la UE, y la distancia de empleo con los nacidos en el país es menor que en el conjunto de la Unión." },
      body: [
        p("Hay dos formas de contar la inmigración. Una cuenta a las personas nacidas en otro país, tengan o no la nacionalidad española. La otra, a las personas de nacionalidad extranjera, hayan nacido donde hayan nacido. Este artículo usa sobre todo la primera: permite comparar países y no cambia cuando alguien obtiene la nacionalidad. Solo usamos fuentes oficiales: el INE y Eurostat."),
        p("El 1 de enero de 2025, el 19,3 % de los residentes en España había nacido en otro país, frente al 14,4 % de la media de la UE. Es el noveno porcentaje más alto de los 26 países con datos (Portugal no ha publicado el de 2025). Por delante están Luxemburgo (51,5 %), Malta, Chipre, Irlanda, Austria, Suecia, Alemania (20,5 %) y Bélgica. Francia (14,0 %) e Italia (11,8 %) están por debajo."),
        p("En 2015, la proporción era del 12,7 % en España y del 10,0 % en la UE. La subida española, de 6,6 puntos, es la quinta mayor de la Unión, después de las de Malta, Alemania, Luxemburgo e Irlanda."),
        { fig: "ine1-europa-nacidos-fuera", code: "E1" },
        p("En 2025 tenía empleo el 69,6 % de los nacidos en el extranjero de 20 a 64 años, frente al 73,3 % de los nacidos en España: 3,7 puntos de diferencia. En el conjunto de la UE la diferencia es de 6,4 puntos (70,8 % frente a 77,2 %), y en Alemania y Francia supera los 11 puntos (11,5 y 12,4)."),
        p("La tasa de empleo de los nacidos fuera ha subido 10,9 puntos en España desde 2015, cuando era del 58,7 %. Aun así, España es el 19.º de 26 países por esa tasa. También la de los nacidos en España está por debajo de la media europea."),
        { fig: "ine2-europa-empleo", code: "E2" },
      ],
    },
    dentro: {
      lede: { es: "En Baleares, más de uno de cada cuatro residentes nació fuera; en Extremadura, menos de uno de cada quince." },
      body: [
        p("El 1 de enero de 2026 vivían en España 10,0 millones de personas nacidas en otro país, el 20,2 % de la población, según el dato provisional del INE. El reparto es muy desigual. Baleares (29,3 %), Cataluña (26,1 %), Madrid (25,7 %), la Comunidad Valenciana (25,5 %) y Canarias (24,1 %) están por encima del 24 %. En el otro extremo están Extremadura (6,6 %), Asturias (12,6 %) y Castilla y León (12,9 %)."),
        p("En números absolutos, Cataluña (2,1 millones), Madrid (1,8), la Comunidad Valenciana (1,4) y Andalucía (1,2) reúnen a casi dos de cada tres nacidos fuera (el 66 %)."),
        { fig: "ind1-comunidades-nacidos-fuera", code: "D1" },
        p("El paro de las personas de nacionalidad extranjera es más alto que el de las de nacionalidad española en todas las comunidades. En el último año con datos (del tercer trimestre de 2025 al segundo de 2026), fue del 15,3 % en el conjunto de España, frente al 9,2 % de los españoles. Va del 21,0 % de Andalucía y el 20,5 % de Extremadura al 10,7 % de Madrid. Donde menos se distancia del de los españoles es en Canarias (13,1 % frente a 12,4 %)."),
        p("En este gráfico la medida es la nacionalidad, no el lugar de nacimiento: quien ha obtenido la nacionalidad española cuenta como español. Y la Encuesta de Población Activa es una encuesta: en las comunidades pequeñas, la muestra de extranjeros es reducida y el dato tiene más margen de error. Navarra, por ejemplo, aparece con un 20,0 %, frente al 5,9 % de los españoles."),
        { fig: "ind2-comunidades-paro", code: "D2" },
      ],
    },
    tiempo: {
      lede: { es: "En 2002 había nacido fuera el 5,7 % de los residentes en España; en 2026, el 20,2 %, uno de cada cinco." },
      body: [
        p("La llegada no ha sido constante. Entre 2002 y 2009, los nacidos fuera pasaron del 5,7 % al 13,5 % de la población. Con la crisis, la cifra se estancó y después bajó un poco: en 2015 y 2016 era del 12,7 %. Desde 2017 vuelve a subir, y más deprisa desde 2023: 17,1 % ese año y 20,2 % en 2026."),
        p("La población de nacionalidad extranjera sigue la misma curva, más abajo: del 4,2 % en 2002 a un máximo del 11,6 % en 2009 y 2010, un mínimo del 9,5 % en 2016 y 2017 y el 14,6 % en 2026. La distancia entre las dos líneas corresponde a las personas nacidas fuera que tienen la nacionalidad española, descontados los extranjeros nacidos en España."),
        p("Este crecimiento es el que hace aumentar la población de España. La nacida en España llegó a su máximo en 2013, con 40,5 millones de personas, y ha bajado todos los años desde entonces, hasta 39,6 millones en 2026. En el mismo periodo, la nacida fuera pasó de 6,2 a 10,0 millones. Los hijos de inmigrantes que nacen en España cuentan como nacidos en España."),
        { fig: "int1-poblacion", code: "T1" },
        p("El paro de los extranjeros subió mucho más que el de los españoles con la crisis. En 2007 rondaba el 12 %, frente a menos del 8 % de los españoles. En el primer trimestre de 2013 llegó al 39,2 %, frente al 25,0 %. En el último año con datos ha sido del 15,3 % y del 9,2 %."),
        { fig: "int2-paro", code: "T2" },
      ],
    },
  },
};

export default theme;
