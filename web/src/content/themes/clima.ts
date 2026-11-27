import { p, type Theme } from "../../lib/content-types";

// Cifras comprobadas contra data/charts/cl*.json (Eurostat y MITECO, descargados el 27 de noviembre de 2026).
// Tabla de verificación en editorial/registro/a18.md.
// Otras fuentes: Ley 7/2021 (art. 3), Real Decreto 986/2024 (PNIEC 2023-2030), MITECO, Avance del Inventario de GEI 2025,
// y AEMET, Resumen anual climatológico 2025.
const theme: Theme = {
  id: "clima",
  code: "CL",
  slug: { es: "clima", en: "climate" },
  title: {
    es: "Clima: temperaturas, sequía y emisiones",
    en: "Climate: temperatures, drought and emissions",
  },
  status: "published",
  published: "2026-11-27",
  order: 14,
  dek: {
    es: "Por habitante, España emite menos que la media europea, pero ha recortado mucho menos desde 1990, porque el transporte, los edificios y el campo emiten hoy más que entonces. Para cumplir en 2030 el objetivo de la ley de cambio climático, una meta que tendrá que gestionar el Gobierno que salga del 29N, las emisiones tendrían que bajar más deprisa que en los últimos años. Mientras, el calor que hay que combatir en verano casi se ha duplicado desde los años ochenta, y los embalses, tras la sequía de 2022 y 2023, están más llenos que en la misma semana de cualquier año desde 2014.",
    en: "Per inhabitant, Spain emits less than the European average, but it has cut far less since 1990, because transport, buildings and farming emit more today than they did then. To meet the climate change law's 2030 target, a goal that the government formed after 29 November will have to manage, emissions would have to fall faster than in recent years. Meanwhile, the heat that has to be countered in summer has almost doubled since the 1980s, and reservoirs, after the 2022-2023 drought, are fuller than in the same week of any year since 2014.",
  },
  lenses: {
    europa: {
      lede: {
        es: "España emite por habitante menos que la mayoría de la UE, pero ha reducido sus emisiones mucho menos desde 1990, y la diferencia no está en la electricidad.",
        en: "Spain emits less per inhabitant than most of the EU, but it has reduced its emissions far less since 1990, and the difference does not lie in electricity.",
      },
      body: [
        p(
          "El clima llega a estas elecciones por dos caminos: lo que España emite y lo que el calentamiento ya le hace. En emisiones por habitante, España está entre los países de la UE que menos emiten: con 5,5 toneladas de CO₂ equivalente en 2024, queda por debajo de Alemania (7,8) e Italia (6,2) y por encima de Francia (5,3) y Portugal (4,6). Solo Malta, Suecia, Portugal, Rumanía, Letonia y Francia emiten menos. Los que más, Luxemburgo (11,1), Irlanda (10,0) y Polonia (9,3).",
          "Climate enters this election in two ways: what Spain emits and what warming is already doing to it. In emissions per inhabitant, Spain is among the EU countries that emit least: at 5.5 tonnes of CO₂ equivalent in 2024, it is below Germany (7.8) and Italy (6.2) and above France (5.3) and Portugal (4.6). Only Malta, Sweden, Portugal, Romania, Latvia and France emit less. Those that emit most are Luxembourg (11.1), Ireland (10.0) and Poland (9.3).",
        ),
        { fig: "cle1-europa-habitante", code: "E1" },
        p(
          "Pero desde 1990 España ha avanzado mucho menos que el conjunto de la UE: en 2024 emitía un 5,9 % menos que entonces, y la UE, un 38,0 % menos. La diferencia no está en la electricidad. En España, la caída de las emisiones de las centrales eléctricas y las refinerías restó 14,5 puntos al total, y la de la industria, otros 6,9. Pero el transporte sumó 11,2 puntos, y los edificios, la agricultura y los residuos, otros 4,4 entre los tres, mientras en la UE bajaban. Hoy el transporte genera el 33,8 % de las emisiones españolas, frente al 26,7 % en el conjunto de la UE.",
          "But since 1990 Spain has made much less progress than the EU as a whole: in 2024 it emitted 5.9% less than then, and the EU, 38.0% less. The difference does not lie in electricity. In Spain, the fall in emissions from power stations and refineries took 14.5 points off the total, and that of industry another 6.9. But transport added 11.2 points, and buildings, agriculture and waste another 4.4 between them, while in the EU they were falling. Today transport generates 33.8% of Spain's emissions, against 26.7% in the EU as a whole.",
        ),
        { fig: "cle2-europa-sectores", code: "E2" },
        { see: { es: "Energía: precio de la luz, renovables y dependencia", en: "Energy: electricity prices, renewables and dependency" }, href: "/energia/" },
      ],
    },
    dentro: {
      lede: {
        es: "Las emisiones se concentran donde están las centrales y la industria, y el calor ha aumentado en todas las comunidades, sobre todo en el sur y el Mediterráneo.",
        en: "Emissions are concentrated where the power stations and industry are, and heat has increased in every region, above all in the south and along the Mediterranean.",
      },
      body: [
        p(
          "Las emisiones de cada comunidad dicen más de lo que se produce en ella que de cómo viven sus habitantes. Asturias, con el 2,1 % de la población, genera el 6,0 % de las emisiones de España: el 32,7 % de lo que emite sale de las centrales eléctricas y otras instalaciones energéticas, y el 37,5 %, de la industria. En Madrid, la comunidad que menos emite por habitante, casi la mitad de las emisiones (el 49,7 %) sale del transporte. Entre las comunidades, le siguen por abajo la Comunidad Valenciana (4,1 toneladas por habitante) y Andalucía (4,3), y por arriba, tras Asturias, Aragón y Navarra (8,5) y Castilla y León (8,3).",
          "Each region's emissions say more about what is produced there than about how its people live. Asturias, with 2.1% of the population, generates 6.0% of Spain's emissions: 32.7% of what it emits comes from power stations and other energy installations, and 37.5% from industry. In Madrid, the region that emits least per inhabitant, almost half of emissions (49.7%) come from transport. Among the regions, next from the bottom are the Valencian Community (4.1 tonnes per inhabitant) and Andalusia (4.3), and from the top, after Asturias, Aragon and Navarre (8.5) and Castile and León (8.3).",
        ),
        { fig: "cld1-comunidades-habitante", code: "D1" },
        p(
          "Desde 2005, las emisiones de España han bajado un 39,1 %, y algo más de la mitad de esa caída (el 51,1 %) corresponde a las centrales eléctricas y las refinerías. Por eso han bajado más donde más pesaban las centrales: en Castilla y León, las de ese sector pasaron de 17,4 millones de toneladas a 36.000, y en Galicia, de 15,4 a 1,9 millones. Asturias (54,4 % menos), Castilla y León (53,7 %) y Galicia (53,4 %) son las comunidades donde más han caído las emisiones. Murcia es la única donde han subido, un 16,5 %.",
          "Since 2005, Spain's emissions have fallen by 39.1%, and just over half of that fall (51.1%) is due to power stations and refineries. That is why they have fallen most where power stations weighed most: in Castile and León, emissions from that sector went from 17.4 million tonnes to 36,000, and in Galicia from 15.4 to 1.9 million. Asturias (54.4% less), Castile and León (53.7%) and Galicia (53.4%) are the regions where emissions have fallen most. Murcia is the only one where they have risen, by 16.5%.",
        ),
        p(
          "El calor también se reparte de forma desigual. Una forma de medirlo son los grados-día de refrigeración: en cada día de calor, cuántos grados habría que bajar para volver a 21 °C, sumados a lo largo del año. En la UE, con niveles mucho más bajos, han pasado de 47 al año en los años ochenta a 112 en la última década, más del doble. 2025 tuvo el valor más alto de la serie, que empieza en 1980: 387, por delante de 2022 (383). Según la AEMET, 2025 fue un año extremadamente cálido, con 15,0 °C de media en la España peninsular, 1,1 °C más que la media de 1991-2020: el tercero más cálido desde 1961, empatado con 2024 y por detrás de 2022 y 2023. Los once años más cálidos de esa serie son de este siglo. La otra cara es que hace menos frío: los grados-día de calefacción han bajado en España de 2.015 a 1.657 al año.",
          "Heat is also unevenly distributed. One way of measuring it is cooling degree days: on each hot day, how many degrees would have to be removed to get back to 21°C, added up over the year. In the EU, at much lower levels, they have gone from 47 a year in the 1980s to 112 in the last decade, more than double. 2025 had the highest value in the series, which starts in 1980: 387, ahead of 2022 (383). According to AEMET, Spain's state meteorological agency, 2025 was an extremely warm year, with an average of 15.0°C in mainland Spain, 1.1°C above the 1991-2020 average: the third warmest since 1961, tied with 2024 and behind 2022 and 2023. The eleven warmest years in that series all belong to this century. The flip side is that it is less cold: heating degree days in Spain have fallen from 2,015 to 1,657 a year.",
        ),
        { fig: "cld2-comunidades-calor", code: "D2" },
        p(
          "El aumento ha sido mayor donde ya hacía más calor: en Murcia, de 207 a 489 grados-día al año; en Baleares, de 203 a 451, y en Andalucía, de 281 a 517. En la cornisa cantábrica el calor sigue siendo poco (13 en Asturias y 22 en Cantabria en la última década), aunque también ha crecido.",
          "The increase has been greatest where it was already hottest: in Murcia, from 207 to 489 degree days a year; in the Balearic Islands, from 203 to 451, and in Andalusia, from 281 to 517. Along the Cantabrian coast there is still little heat (13 in Asturias and 22 in Cantabria in the last decade), although it has also grown.",
        ),
      ],
    },
    tiempo: {
      lede: {
        es: "Las emisiones se han separado del crecimiento de la economía, pero al ritmo de los últimos años no bastaría para cumplir el objetivo de 2030. La sequía va y viene: los embalses están hoy más llenos que en estas fechas de cualquier año desde 2014.",
        en: "Emissions have decoupled from economic growth, but at the pace of recent years that would not be enough to meet the 2030 target. Drought comes and goes: reservoirs are fuller today than at this time of year in any year since 2014.",
      },
      body: [
        p(
          "En toneladas, las emisiones de España pasaron de 284,4 millones en 1990 a 444,1 en 2007 y a 267,7 en 2024. El avance del inventario que publicó en 2026 el Ministerio para la Transición Ecológica estima que en 2025 subieron un 1,1 %, hasta 270,7 millones, un 4,8 % menos que en 1990. Según el ministerio, crecieron sobre todo las del transporte (un 2,4 %) y las de la generación eléctrica (un 5,5 %), porque las centrales de ciclo combinado de gas funcionaron más tras el apagón del 28 de abril de 2025 para dar estabilidad al sistema.",
          "In tonnes, Spain's emissions went from 284.4 million in 1990 to 444.1 million in 2007 and 267.7 million in 2024. The advance inventory published in 2026 by the Ministry for the Ecological Transition (MITECO) estimates that they rose by 1.1% in 2025, to 270.7 million, 4.8% less than in 1990. According to the ministry, the biggest increases came from transport (2.4%) and electricity generation (5.5%), because combined-cycle gas plants ran more after the blackout of 28 April 2025 to keep the system stable.",
        ),
        { fig: "clt1-emisiones-1990", code: "T1" },
        p(
          "Que las emisiones bajen no quiere decir que la economía se haya parado. Entre 1995 y 2007, el PIB creció un 54,0 % y las emisiones, un 36,9 %: iban casi a la par. Desde entonces se han separado. En 2024, cada euro de PIB se producía con un 53,6 % menos de emisiones que en 1995, y las emisiones por habitante eran un 44,2 % menores que en 2007. Cuánto se debe al cambio en la electricidad, a la crisis de 2008, a la industria que cerró o a la eficiencia no se puede separar con estos datos.",
          "Falling emissions do not mean that the economy has stalled. Between 1995 and 2007, GDP grew by 54.0% and emissions by 36.9%: they moved almost in step. Since then they have decoupled. In 2024, each euro of GDP was produced with 53.6% fewer emissions than in 1995, and emissions per inhabitant were 44.2% lower than in 2007. How much of this is due to the change in electricity, the 2008 crisis, industry that closed or efficiency cannot be separated with this data.",
        ),
        { fig: "clt2-pib-emisiones", code: "T2" },

        { h: { es: "La ficha: el objetivo de emisiones para 2030", en: "Policy file: the 2030 emissions target" }, id: "ficha-objetivo-emisiones" },
        { steps: [
          {
            title: { es: "Qué es.", en: "What it is." },
            text: {
              es: "El artículo 3 de la Ley 7/2021, de cambio climático y transición energética, obliga a que en 2030 las emisiones de gases de efecto invernadero del conjunto de la economía española sean al menos un 23 % menores que en 1990. El Plan Nacional Integrado de Energía y Clima (PNIEC) 2023-2030, aprobado por el Real Decreto 986/2024, eleva esa meta al 32 %.",
              en: "Article 3 of Law 7/2021 on climate change and the energy transition requires greenhouse gas emissions from the Spanish economy as a whole to be at least 23% lower in 2030 than in 1990. The 2023-2030 National Integrated Energy and Climate Plan (PNIEC), approved by Royal Decree 986/2024, raises that goal to 32%.",
            },
          },
          {
            title: { es: "Quién y cuándo.", en: "Who and when." },
            text: {
              es: "La ley la aprobaron las Cortes en mayo de 2021, y el plan, el Consejo de Ministros en septiembre de 2024. La ley solo permite revisar los objetivos al alza y fija la neutralidad climática antes de 2050.",
              en: "Parliament passed the law in May 2021, and the Council of Ministers approved the plan in September 2024. The law only allows the targets to be revised upwards and sets climate neutrality before 2050.",
            },
          },
          {
            title: { es: "Qué debería pasar.", en: "What should happen." },
            text: {
              es: "Que las emisiones bajen de los 284,4 millones de toneladas de 1990 a 219,0 millones o menos en 2030, o a 193,4 millones con la meta del plan.",
              en: "Emissions should fall from 284.4 million tonnes in 1990 to 219.0 million or less in 2030, or to 193.4 million under the plan's goal.",
            },
          },
          {
            title: { es: "Con qué lo comparamos.", en: "What we compare it with." },
            text: {
              es: "Con las emisiones del inventario oficial, el que España comunica a la UE y a la ONU, y con el ritmo al que han bajado desde 2019.",
              en: "With emissions in the official inventory, the one Spain reports to the EU and the UN, and with the pace at which they have fallen since 2019.",
            },
          },
        ] },
        p(
          "En 2025, según el avance, las emisiones estaban un 4,8 % por debajo de las de 1990. Para llegar a un 23 % menos en 2030 tendrían que bajar cada año unos 3,6 puntos (medidos sobre las emisiones de 1990), y para el 32 % del plan, unos 5,4. Entre 2019 y 2024 bajaron 3,0 puntos al año de media, incluida la caída de 2020 por la pandemia, y en 2025 subieron. La ley no precisa si el objetivo se mide con o sin lo que absorben los bosques y los suelos; aquí se usan las emisiones sin descontar esas absorciones, como en el gráfico, así que la comparación es orientativa. Los objetivos de renovables de la misma ley los analizamos en el tema de energía.",
          "In 2025, according to the advance estimate, emissions were 4.8% below 1990. To reach 23% less in 2030 they would have to fall by around 3.6 points a year (measured against 1990 emissions), and by around 5.4 for the plan's 32%. Between 2019 and 2024 they fell by 3.0 points a year on average, including the drop in 2020 due to the pandemic, and in 2025 they rose. The law does not specify whether the target is measured with or without what forests and soils absorb; here emissions are used without deducting those removals, as in the chart, so the comparison is indicative. We analyse the same law's renewables targets in the energy topic.",
        ),
        p(
          "La otra cara del clima es el agua. El nivel de los embalses depende de la lluvia de cada año, y en él no hay una tendencia tan clara como en la temperatura. En la sequía de 1995, la reserva de la España peninsular bajó al 25,5 % en octubre. En la de 2022 y 2023, la reserva media de septiembre, último mes del año hidrológico, fue del 33,8 % en 2022 y del 36,8 % en 2023. Después llovió: según la AEMET, 2025 fue un año húmedo, con el 109 % de la precipitación normal en la España peninsular, y en septiembre de 2026 la reserva media fue del 61,5 %.",
          "The other side of climate is water. Reservoir levels depend on each year's rainfall, and they show no trend as clear as temperature does. In the 1995 drought, mainland Spain's reserve fell to 25.5% in October. In the 2022-2023 drought, the average reserve in September, the last month of the hydrological year, was 33.8% in 2022 and 36.8% in 2023. Then the rain came: according to AEMET, 2025 was a wet year, with 109% of normal rainfall in mainland Spain, and in September 2026 the average reserve was 61.5%.",
        ),
        { fig: "clt3-embalses", code: "T3" },
        p(
          "La media nacional esconde diferencias entre cuencas. El 24 de noviembre de 2026, varias cuencas del sur y del este estaban muy por encima de su media de los diez años anteriores en esa misma semana: el Guadalquivir, al 69,2 % (media, 34,1 %); el Guadiana, al 73,0 % (40,1 %); el Segura, al 45,8 % (24,5 %), y las cuencas internas de Cataluña, al 78,1 % (55,9 %). En el norte ocurre lo contrario: el Ebro está al 47,3 % (54,9 %), el Duero al 44,9 % (49,1 %) y Galicia Costa al 48,5 % (63,5 %).",
          "The national average hides differences between river basins. On 24 November 2026, several basins in the south and east were well above their average for the same week in the previous ten years: the Guadalquivir at 69.2% (average, 34.1%); the Guadiana at 73.0% (40.1%); the Segura at 45.8% (24.5%), and Catalonia's internal basins at 78.1% (55.9%). In the north the opposite is true: the Ebro is at 47.3% (54.9%), the Duero at 44.9% (49.1%) and the Galician coastal basins at 48.5% (63.5%).",
        ),
        p(
          "Lo que no dicen estos datos. Las emisiones se cuentan donde se producen: no incluyen las de los productos que España importa ni las de la aviación y la navegación internacionales, y asignan a Asturias o a Andalucía las de centrales e industrias que abastecen a todo el país. Los grados-día miden el calor, no sus efectos en la salud, en el campo o en la factura de la luz. El nivel de los embalses mezcla la lluvia con la gestión del agua y no mide la sequedad de los suelos ni el estado de los acuíferos. Y nada de esto permite atribuir la caída de las emisiones a un gobierno: coincide con el cambio de la electricidad, con la crisis de 2008 y con normas europeas, y estos datos no permiten separar cada efecto.",
          "What this data does not say. Emissions are counted where they are produced: they do not include those embodied in the goods Spain imports or those from international aviation and shipping, and they assign to Asturias or Andalusia the emissions of power stations and industries that supply the whole country. Degree days measure heat, not its effects on health, on farming or on electricity bills. Reservoir levels combine rainfall with water management and do not measure soil dryness or the state of aquifers. And none of this allows the fall in emissions to be attributed to a government: it coincides with the change in electricity, the 2008 crisis and European rules, and this data cannot separate each effect.",
        ),
        { see: { es: "Territorio: la España que se vacía y la que crece", en: "Territory: the Spain that is emptying and the Spain that is growing" }, href: "/territorio/" },
      ],
    },
  },
  sources: [
    { name: "Ley 7/2021, de 20 de mayo, de cambio climático y transición energética (artículo 3)", url: "https://www.boe.es/buscar/act.php?id=BOE-A-2021-8447" },
    { name: "Real Decreto 986/2024, de 24 de septiembre, por el que se aprueba la actualización del Plan Nacional Integrado de Energía y Clima 2023-2030", url: "https://www.boe.es/diario_boe/txt.php?id=BOE-A-2024-19278" },
    { name: { es: "MITECO, objetivos del PNIEC 2023-2030 (32 % menos de emisiones que en 1990)", en: "MITECO, 2023-2030 PNIEC targets (32% fewer emissions than in 1990)" }, url: "https://www.miteco.gob.es/es/energia/estrategia-normativa/pniec-23-30.html" },
    { name: "MITECO, Avance del Inventario de Emisiones de GEI del año 2025", url: "https://www.miteco.gob.es/content/dam/miteco/es/calidad-y-evaluacion-ambiental/temas/sistema-espanol-de-inventario-sei-/Nota-Avance-GEI-2025.pdf" },
    { name: "AEMET, Resumen anual climatológico 2025", url: "https://www.aemet.es/documentos/es/serviciosclimaticos/vigilancia_clima/resumenes_climat/anuales/res_anual_clim_2025.pdf" },
  ],
};

export default theme;
