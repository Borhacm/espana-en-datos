import { p, type Theme } from "../../lib/content-types";

// Cifras comprobadas contra data/charts/te*.json (INE y Eurostat, descargados el 25 de noviembre de 2026) y data/base/escanos-2026.json.
// Tabla de verificación en editorial/registro/a15.md.
// Estudios citados: Banco de España, Informe Anual 2020, capítulo 4; Gutiérrez, Moral-Benito y Ramos, Documentos Ocasionales 2027 (2020) y 2206 (2022).
const theme: Theme = {
  id: "territorio",
  code: "TE",
  slug: { es: "territorio", en: "territory" },
  title: {
    es: "Territorio: la España que se vacía y la que crece",
    en: "Territory: the Spain that is emptying and the Spain that is growing",
  },
  status: "published",
  published: "2026-11-25",
  order: 13,
  dek: {
    es: "España ha ganado un 19,5 % de habitantes desde 2001, pero seis de cada diez municipios y 14 provincias del interior y del noroeste tienen hoy menos población. No crecen las grandes ciudades, sino los municipios medianos de su alrededor y de la costa. En el campo mueren casi tres personas por cada una que nace, y es la llegada de población la que ha frenado la pérdida en los últimos años. Las 14 provincias que han perdido habitantes eligen el 29N 54 de los 350 diputados.",
    en: "Spain has gained 19.5% more inhabitants since 2001, yet six in ten municipalities and 14 provinces in the interior and the north-west have fewer people today. It is not the big cities that are growing, but the medium-sized towns around them and on the coast. In the countryside almost three people die for every one born, and it is the arrival of newcomers that has slowed the loss in recent years. The 14 provinces that have lost inhabitants elect 54 of the 350 deputies on 29 November.",
  },
  lenses: {
    europa: {
      lede: {
        es: "España no está poco poblada en conjunto, pero tiene algunas de las zonas más vacías de la UE fuera de los países nórdicos, y en ellas faltan nacimientos más que en el resto de Europa.",
        en: "Spain as a whole is not sparsely populated, but it has some of the emptiest areas in the EU outside the Nordic countries, and in them births fall short more than in the rest of Europe.",
      },
      body: [
        p(
          "Dónde vive la gente importa el 29N: los escaños se reparten por provincias, y eso hace que el voto del interior pese más que su población. Con 97,2 habitantes por km² en 2024, España está algo por debajo de la media de la UE (109,7), pero su población está muy concentrada. Solo 16 regiones de la UE de nivel provincial bajan de 12,5 habitantes por km², el umbral con el que las normas europeas de ayudas regionales definen una zona escasamente poblada. Diez están en Suecia y Finlandia. De las otras seis, tres son provincias españolas: Soria (8,8), Teruel (9,2) y Cuenca (11,7). Les siguen Huesca (14,8) y Zamora (15,9).",
          "Where people live matters on 29 November: seats are allocated by province, which means that a vote in the interior weighs more than its population. With 97.2 inhabitants per km² in 2024, Spain is somewhat below the EU average (109.7), but its population is highly concentrated. Only 16 EU regions at provincial level fall below 12.5 inhabitants per km², the threshold that EU regional aid rules use to define a sparsely populated area. Ten are in Sweden and Finland. Of the other six, three are Spanish provinces: Soria (8.8), Teruel (9.2) and Cuenca (11.7). Huesca (14.8) and Zamora (15.9) come next.",
        ),
        { fig: "tee1-europa-densidad", code: "E1" },
        p(
          "La comparación por provincias se queda corta, porque una provincia grande mezcla ciudades y comarcas vacías. El Banco de España la hizo por municipios: en su Informe Anual de 2020 contó 3.403 municipios en riesgo de despoblación (con menos población en 2018 que en 2001, más defunciones que nacimientos desde 2001 y menos de 12,5 habitantes por km²). Eran el 42 % de los municipios españoles, con el 2,3 % de la población, alrededor de un millón de personas. En el conjunto de la zona del euro eran el 10 %; en Alemania, el 1 %; en Francia, el 7 %, y en Italia, el 4 %. Solo Estonia, Finlandia y Letonia, con porcentajes en torno al 50 %, se parecían a España.",
          "A comparison by province falls short, because a large province mixes cities with empty districts. The Bank of Spain did it by municipality: in its 2020 Annual Report it counted 3,403 municipalities at risk of depopulation (with fewer inhabitants in 2018 than in 2001, more deaths than births since 2001 and fewer than 12.5 inhabitants per km²). They made up 42% of Spanish municipalities and held 2.3% of the population, about 1 million people. In the euro area as a whole the share was 10%; in Germany, 1%; in France, 7%, and in Italy, 4%. Only Estonia, Finland and Latvia, with shares of around 50%, resembled Spain.",
        ),
        p(
          "Como explica el Banco de España en otro estudio, lo que vacía hoy esas zonas no es tanto que la gente se vaya como que se fue durante décadas: quedan pocos jóvenes y muchos mayores, y hay más defunciones que nacimientos. Entre 2022 y 2024, en las provincias que Eurostat clasifica como predominantemente rurales hubo cada año 9,3 defunciones más que nacimientos por cada 1.000 habitantes, casi el doble que en las regiones rurales de la UE (4,7). Lo compensó, y con creces, la llegada de población: 11,8 personas más de las que se fueron por cada 1.000 habitantes, frente a 5,1 en la UE. En las regiones urbanas españolas las llegadas netas fueron todavía mayores (15,4, frente a 7,8 en la UE).",
          "As the Bank of Spain explains in another study, what empties these areas today is not so much that people are leaving as that they left over decades: few young people remain and many older ones do, and there are more deaths than births. Between 2022 and 2024, in the provinces that Eurostat classifies as predominantly rural there were 9.3 more deaths than births each year per 1,000 inhabitants, almost double the figure in the EU's rural regions (4.7). It was more than offset by newcomers: 11.8 more people arrived than left per 1,000 inhabitants, against 5.1 in the EU. In Spain's urban regions net arrivals were even higher (15.4, against 7.8 in the EU).",
        ),
        { fig: "tee2-europa-balance", code: "E2" },
        { see: { es: "Demografía y pensiones: un país que envejece", en: "Demographics and pensions: an ageing country" }, href: "/demografia/" },
      ],
    },
    dentro: {
      lede: {
        es: "La línea que separa la España que pierde habitantes de la que gana no pasa entre comunidades, sino entre el interior y la costa, y entre los pueblos pequeños y los municipios medianos.",
        en: "The line between the Spain that is losing inhabitants and the Spain that is gaining them does not run between regions, but between the interior and the coast, and between small villages and medium-sized towns.",
      },
      body: [
        p(
          "Entre el 1 de enero de 2001 y el de 2025, la población empadronada en España pasó de 41,1 a 49,1 millones. En 14 de las 52 provincias, en cambio, hay hoy menos habitantes que entonces: Zamora ha perdido el 18,3 %; Ourense, el 11,3 %; León, el 10,6 %, y Lugo y Palencia, el 10,5 %. La lista la completan Salamanca, Asturias, Cáceres, Jaén, Ávila, Cuenca, Soria, Badajoz y Teruel, que tiene 36 habitantes menos que en 2001. En el otro extremo, Guadalajara, pegada a Madrid, ha crecido un 66,4 %, seguida de Almería (45,1 %), Girona (43,5 %), Tarragona (42,9 %) y Baleares (40,8 %). Si se cuenta desde 2011, cuando la población tocó techo antes de la crisis, son 22 las provincias que han perdido habitantes.",
          "Between 1 January 2001 and 1 January 2025, Spain's registered population rose from 41.1 to 49.1 million. In 14 of the 52 provinces, however, there are fewer inhabitants today than then: Zamora has lost 18.3%; Ourense, 11.3%; León, 10.6%, and Lugo and Palencia, 10.5%. The list is completed by Salamanca, Asturias, Cáceres, Jaén, Ávila, Cuenca, Soria, Badajoz and Teruel, which has 36 fewer inhabitants than in 2001. At the other end, Guadalajara, next to Madrid, has grown by 66.4%, followed by Almería (45.1%), Girona (43.5%), Tarragona (42.9%) and the Balearic Islands (40.8%). Counting from 2011, when the population peaked before the crisis, 22 provinces have lost inhabitants.",
        ),
        { fig: "ted1-provincias", code: "D1" },
        p(
          "Esas 14 provincias suman 5,0 millones de habitantes y, según el reparto por población de 2025, eligen 54 de los 350 diputados el 29N. Como cada provincia tiene al menos dos escaños, el voto de las menos pobladas pesa más, algo que explicamos en las notas sobre el coste de un escaño y sobre cómo se convierten los votos en escaños.",
          "Those 14 provinces have 5.0 million inhabitants between them and, under the allocation based on 2025 population, elect 54 of the 350 deputies on 29 November. Because every province has at least two seats, votes in the least populated provinces carry more weight, as we explain in the notes on the cost of a seat and on how votes become seats.",
        ),
        { see: { es: "Nota: cómo se convierten los votos en escaños", en: "Note: how votes become seats" }, href: "/notas/como-se-convierten-votos-en-escanos/" },
        p(
          "Dentro de cada provincia, lo que más distingue a los municipios que pierden de los que ganan es su tamaño. De los 8.103 municipios que existían en 2001 y siguen existiendo, 4.956 (el 61,2 %) tienen hoy menos habitantes; en ellos viven 8,0 millones de personas, el 16,4 % de la población. Los de 500 habitantes o menos han perdido población en conjunto, y los de 501 a 1.000 apenas han crecido (1,8 %). Pero no son las grandes ciudades las que más ganan: las de más de 100.000 habitantes han crecido menos que la media (19,3 % en estos municipios), y por encima de ella están todos los tramos de 2.001 a 100.000 habitantes. El tamaño no lo explica todo: influyen la cercanía a una ciudad, la costa, el precio de la vivienda y la llegada de inmigrantes, y estos datos no permiten separar cada factor.",
          "Within each province, what most distinguishes the municipalities that lose from those that gain is their size. Of the 8,103 municipalities that existed in 2001 and still exist, 4,956 (61.2%) have fewer inhabitants today; 8.0 million people live in them, 16.4% of the population. Those with 500 inhabitants or fewer have lost population as a group, and those with 501 to 1,000 have barely grown (1.8%). But it is not the big cities that gain most: those with over 100,000 inhabitants have grown less than the average (19.3% across these municipalities), and every size band from 2,001 to 100,000 inhabitants is above it. Size does not explain everything: proximity to a city, the coast, house prices and the arrival of immigrants all play a part, and this data cannot separate each factor.",
        ),
        { fig: "ted2-tamano-municipio", code: "D2" },
        p(
          "Vivir en un pueblo pequeño es también vivir más lejos de los servicios. Según el Informe Anual de 2020 del Banco de España, con datos de entre 2011 y 2020, el habitante medio de un municipio en riesgo de despoblación tenía el colegio, el centro de salud, la gasolinera o el polideportivo más cercanos a más de 30 km, frente a 14 km en el resto de los municipios rurales y 2 km en los urbanos. El 79 % de esos municipios no tenía sucursal bancaria, y solo el 5 % de sus hogares tenía cobertura de banda ancha de 100 megas, frente al 83 % en los municipios urbanos. Algunas de estas cifras han podido cambiar desde entonces, sobre todo la de banda ancha.",
          "Living in a small village also means living further from services. According to the Bank of Spain's 2020 Annual Report, with data from between 2011 and 2020, the average resident of a municipality at risk of depopulation had the nearest school, health centre, petrol station or sports centre more than 30 km away, against 14 km in other rural municipalities and 2 km in urban ones. 79% of those municipalities had no bank branch, and only 5% of their households had 100-megabit broadband coverage, against 83% in urban municipalities. Some of these figures may have changed since then, especially the broadband one.",
        ),
      ],
    },
    tiempo: {
      lede: {
        es: "Cada vez hay más pueblos casi vacíos, pero desde 2020 la mitad de los municipios gana población cada año, como antes de la crisis de 2008.",
        en: "There are ever more almost empty villages, but since 2020 half of municipalities have gained population each year, as before the 2008 crisis.",
      },
      body: [
        p(
          "El número de municipios con 100 habitantes o menos no ha dejado de crecer: eran 850 en 1996 y son 1.426 en 2025, el máximo de la serie. Las provincias con más son Guadalajara (177), Burgos (171), Soria (118) y Ávila (106): Guadalajara es a la vez la provincia que más ha crecido y la que tiene más pueblos casi vacíos. Aun así, son una parte pequeña de un mapa municipal muy fragmentado: de los 8.132 municipios españoles, 4.981 tienen 1.000 habitantes o menos, un número parecido al de 1996 (4.902).",
          "The number of municipalities with 100 inhabitants or fewer has kept rising: there were 850 in 1996 and there are 1,426 in 2025, the highest in the series. The provinces with the most are Guadalajara (177), Burgos (171), Soria (118) and Ávila (106): Guadalajara is both the fastest-growing province and the one with the most almost empty villages. Even so, they are a small part of a highly fragmented municipal map: of Spain's 8,132 municipalities, 4,981 have 1,000 inhabitants or fewer, a similar number to 1996 (4,902).",
        ),
        { fig: "tet1-micromunicipios", code: "T1" },
        p(
          "La tendencia de fondo no es una línea recta: depende del ciclo económico y, sobre todo, de la inmigración. En los años del auge inmobiliario, más de la mitad de los municipios ganaba población cada año (el 53,7 % en 2007). Con la crisis la proporción se hundió hasta el 25,4 % en 2015, cuando siete de cada diez municipios perdieron habitantes. Desde 2020 ha vuelto a rondar la mitad, entre el 47,9 % y el 53,7 %, mientras la población nacida en el extranjero seguía creciendo hasta el 20,2 % de los residentes en 2026. El Banco de España estudió el primero de esos años: en 2020 la población rural creció un 0,7 %, sobre todo porque se fue menos gente de los pueblos, y no tanto porque llegara más. Sus autores advertían de que era un año excepcional y de que no se podía saber si el cambio iba a durar.",
          "The underlying trend is not a straight line: it depends on the economic cycle and, above all, on immigration. In the years of the property boom, more than half of municipalities gained population each year (53.7% in 2007). With the crisis the share collapsed to 25.4% in 2015, when seven in ten municipalities lost inhabitants. Since 2020 it has returned to around half, between 47.9% and 53.7%, while the foreign-born population kept growing, to 20.2% of residents in 2026. The Bank of Spain studied the first of those years: in 2020 the rural population grew by 0.7%, mainly because fewer people left the villages, rather than because more arrived. Its authors warned that it was an exceptional year and that it was impossible to know whether the change would last.",
        ),
        { fig: "tet2-municipios-crecen", code: "T2" },
        { see: { es: "Inmigración en datos", en: "Immigration in data" }, href: "/inmigracion/" },

        { h: { es: "Qué dice la evidencia sobre las políticas contra la despoblación", en: "What the evidence says about policies against depopulation" }, id: "evidencia-despoblacion" },
        p(
          "Las políticas contra la despoblación son de dos tipos, según el Banco de España: las de adaptación, que intentan mantener servicios mínimos para quien vive en los pueblos, y las de mitigación, que intentan frenar la pérdida de población con inversiones, subvenciones o rebajas de impuestos. Sobre las segundas, su Informe Anual de 2020 concluye que la evidencia disponible sobre los incentivos fiscales a las empresas y sobre el traslado de instituciones públicas a zonas despobladas no es concluyente, y advierte de que abaratar el transporte con nuevas infraestructuras puede incluso concentrar más la actividad en las regiones más productivas. Sí encuentra efectos en los servicios: el cierre de sucursales bancarias en municipios rurales redujo la inversión y la supervivencia de las pequeñas empresas de esos municipios.",
          "Policies against depopulation are of two kinds, according to the Bank of Spain: adaptation policies, which try to maintain minimum services for those who live in villages, and mitigation policies, which try to halt population loss through investment, subsidies or tax cuts. On the latter, its 2020 Annual Report concludes that the available evidence on tax incentives for firms and on relocating public institutions to depopulated areas is not conclusive, and warns that making transport cheaper with new infrastructure can even concentrate activity further in the most productive regions. It does find effects from services: the closure of bank branches in rural municipalities reduced investment and survival among small firms in those municipalities.",
        ),
        p(
          "Un segundo estudio de los mismos autores, sobre los cambios de población de 2020, encontró que los municipios con mejor acceso a servicios físicos y digitales, más segundas residencias y más cerca de la capital de provincia tuvieron un saldo migratorio más favorable durante la pandemia. Es una asociación, no la prueba de que mejorar los servicios atraiga población, y se refiere a un año muy particular.",
          "A second study by the same authors, on population changes in 2020, found that municipalities with better access to physical and digital services, more second homes and closer to the provincial capital had a more favourable migration balance during the pandemic. That is an association, not proof that improving services attracts population, and it refers to a very unusual year.",
        ),
        p(
          "Lo que no dicen estos datos. El padrón cuenta a los empadronados, no a quien vive en un pueblo parte del año ni a quien está empadronado en él sin vivir allí, así que puede sobrestimar o subestimar la población real de los municipios pequeños. Las comparaciones europeas usan regiones de tamaños muy distintos: las provincias españolas son grandes y esconden comarcas casi vacías, y por eso solo el 2,6 % de los españoles vive en provincias que Eurostat clasifica como rurales, frente al 19,2 % en la UE. Los gráficos por tamaño de municipio no distinguen si los que crecen lo hacen por nacimientos, por llegadas desde otras partes de España o desde el extranjero. Y nada de esto permite atribuir la pérdida o la ganancia de población de una provincia a un gobierno: el éxodo rural empezó a mediados del siglo pasado y ha seguido con gobiernos de distinto color en Madrid y en las comunidades.",
          "What this data does not say. The municipal register counts registered residents, not people who live in a village for part of the year or those registered there without living there, so it can overstate or understate the real population of small municipalities. European comparisons use regions of very different sizes: Spanish provinces are large and hide almost empty districts, which is why only 2.6% of Spaniards live in provinces that Eurostat classifies as rural, against 19.2% in the EU. The charts by size of municipality do not show whether those that grow do so through births, arrivals from elsewhere in Spain or arrivals from abroad. And none of this allows a province's loss or gain of population to be attributed to a government: the rural exodus began in the middle of the last century and has continued under governments of different parties in Madrid and in the regions.",
        ),
        { see: { es: "Vivienda: por qué es el tema de estas elecciones", en: "Housing: why it is the issue of this election" }, href: "/vivienda/" },
      ],
    },
  },
  sources: [
    { name: "Banco de España, Informe Anual 2020, capítulo 4: La distribución espacial de la población en España y sus implicaciones económicas", url: "https://www.bde.es/f/webbde/SES/Secciones/Publicaciones/PublicacionesAnuales/InformesAnuales/20/Fich/InfAnual_2020-Cap4.pdf" },
    { name: "Gutiérrez, Moral-Benito y Ramos, Tendencias recientes de la población en las áreas rurales y urbanas de España (Banco de España, Documentos Ocasionales 2027, 2020)", url: "https://www.bde.es/f/webbde/SES/Secciones/Publicaciones/PublicacionesSeriadas/DocumentosOcasionales/20/Fich/do2027.pdf" },
    { name: "Gutiérrez, Moral-Benito y Ramos, Dinámicas de población durante el COVID-19 (Banco de España, Documentos Ocasionales 2206, 2022)", url: "https://www.bde.es/f/webbde/SES/Secciones/Publicaciones/PublicacionesSeriadas/DocumentosOcasionales/22/Fich/do2206.pdf" },
    { name: { es: "Escaños por provincia en 2026: cálculo según el artículo 162 de la LOREG con el padrón de 2025", en: "Seats per province in 2026: calculation under article 162 of the electoral law (LOREG) with the 2025 register" }, url: "/elecciones-29n/" },
  ],
};

export default theme;
