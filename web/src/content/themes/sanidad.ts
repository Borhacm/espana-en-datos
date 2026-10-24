import { p, type Theme } from "../../lib/content-types";

// Cifras comprobadas contra data/charts/sa*.json (Eurostat, SISLE-SNS y Estadística de Gasto Sanitario Público, descargados el 24 de octubre de 2026).
// Ficha: Real Decreto 1039/2011 (BOE-A-2011-14190). Procesos garantizados y consultas: informe SISLE-SNS de diciembre de 2025 (rectificado), págs. 4 y 14.
// Gasto por habitante en PPA: Eurostat hlth_sha11_hf (2024). Entradas en lista: informe de diciembre de 2025, pág. 7.
const theme: Theme = {
  id: "sanidad",
  code: "SA",
  slug: { es: "sanidad", en: "health" },
  title: {
    es: "Sanidad: listas de espera y gasto por comunidad",
    en: "Health: waiting lists and spending by region",
  },
  status: "published",
  published: "2026-10-24",
  order: 7,
  dek: {
    es: "Más de 850.000 personas esperan una operación en la sanidad pública, y cuánto esperan depende mucho de dónde vivan. España gasta en sanidad pública menos que la media de la UE y los hogares pagan de su bolsillo una parte mayor. Gastar más por habitante tampoco garantiza esperar menos: entre comunidades, las dos cosas apenas se relacionan.",
    en: "More than 850,000 people are waiting for surgery in the public health system, and how long they wait depends heavily on where they live. Spain spends less on public health care than the EU average, and households pay a larger share out of their own pockets. Spending more per inhabitant does not guarantee shorter waits either: across regions, the two are barely related.",
  },
  lenses: {
    europa: {
      lede: {
        es: "España gasta en sanidad pública menos que la media europea, y una parte mayor de la factura la pagan directamente los hogares.",
        en: "Spain spends less on public health care than the European average, and a larger share of the bill is paid directly by households.",
      },
      body: [
        p(
          "La sanidad es una competencia de las comunidades, pero el Estado fija las reglas comunes: qué servicios cubre el sistema público, los tiempos máximos de espera garantizados y el sistema de financiación de las comunidades. Las tres dependen de leyes y decretos estatales que el Gobierno y las Cortes que salgan del 29N podrán cambiar. En 2024, el gasto público en sanidad equivalió al 6,5 % del PIB, por debajo de la media de la UE y en mitad de la tabla: Austria, Chequia, Croacia o Francia dedican entre el 8,9 % y el 9,5 %. La diferencia también se ve por habitante y sumando lo público y lo privado: medido en estándares de poder adquisitivo (una unidad que corrige las diferencias de precios entre países), España gastó 3.319 por persona, un 19 % menos que la media de la UE (4.075).",
          "Health care is run by the regions, but central government sets the common rules: which services the public system covers, the guaranteed maximum waiting times and the funding system for the regions. All three depend on national laws and decrees that the Government and parliament that emerge from the 29 November election will be able to change. In 2024, public spending on health was equivalent to 6.5% of GDP, below the EU average and in the middle of the table: Austria, Czechia, Croatia or France devote between 8.9% and 9.5%. The gap also shows per inhabitant, adding public and private spending: measured in purchasing power standards (a unit that corrects for price differences between countries), Spain spent 3,319 per person, 19% less than the EU average (4,075).",
        ),
        { fig: "sae1-europa-gasto", code: "E1" },
        p(
          "Lo que no paga el sector público lo pagan, sobre todo, los hogares. En España, las administraciones y la Seguridad Social cubren el 72,2 % del gasto sanitario, ocho puntos menos que en el conjunto de la UE (80,3 %). Los seguros voluntarios pagan el 6,3 %, y los hogares, el 21,5 %, directamente de su bolsillo. Ese pago directo incluye la parte del precio de los medicamentos con receta, pero también servicios que el sistema público apenas cubre, como el dentista o las gafas, y las consultas privadas.",
          "What the public sector does not pay is mostly paid by households. In Spain, government and social security cover 72.2% of health spending, eight points less than in the EU as a whole (80.3%). Voluntary insurance pays 6.3%, and households 21.5%, directly out of their own pockets. That direct payment includes their share of the price of prescription medicines, but also services the public system barely covers, such as the dentist or glasses, and private consultations.",
        ),
        { fig: "sae2-europa-bolsillo", code: "E2" },
      ],
    },
    dentro: {
      lede: {
        es: "La espera para operarse va de menos de dos meses a casi seis según la comunidad, y no sigue al gasto por habitante.",
        en: "The wait for surgery ranges from under two months to almost six depending on the region, and it does not follow spending per inhabitant.",
      },
      body: [
        p(
          "A 31 de diciembre de 2025 había 853.740 pacientes esperando una operación no urgente en la sanidad pública, que llevaban de media 122 días en la lista. Las diferencias entre comunidades son grandes. En Andalucía y Cataluña, uno de cada tres pacientes (32,2 % y 32,0 %) llevaba más de seis meses esperando; en Madrid, menos de uno de cada cien (0,8 %), y en el País Vasco, el 2,3 %. La espera para ver por primera vez al especialista sigue otro orden: la media es de 102 días, y va de 32 en La Rioja a 162 en Canarias, sin contar Ceuta y Melilla. Madrid, que tiene la espera quirúrgica más corta, es la comunidad con más pacientes por habitante pendientes de esa primera consulta (134,7 por cada 1.000).",
          "On 31 December 2025, 853,740 patients were waiting for non-urgent surgery in the public health system, and they had been on the list for 122 days on average. The differences between regions are large. In Andalusia and Catalonia, one in three patients (32.2% and 32.0%) had been waiting for more than six months; in Madrid, fewer than one in a hundred (0.8%), and in the Basque Country 2.3%. The wait for a first appointment with a specialist follows a different order: the average is 102 days, ranging from 32 in La Rioja to 162 in the Canary Islands, leaving aside Ceuta and Melilla. Madrid, which has the shortest surgical wait, is the region with the most patients per inhabitant waiting for that first appointment (134.7 per 1,000).",
        ),
        { fig: "sad1-espera-comunidades", code: "D1" },
        p(
          "Tampoco gastan lo mismo. En 2024, el País Vasco y Asturias gastaron en sanidad más de 2.300 euros por habitante; Andalucía, la que menos, y Madrid, la segunda que menos, por debajo de 1.800. Pero gastar más no se traduce en esperar menos: entre las 17 comunidades, la relación entre el gasto por habitante y el tiempo de espera quirúrgica es prácticamente nula (coeficiente de correlación de -0,09). Madrid gasta poco y tiene la espera más corta; Andalucía gasta lo mínimo y tiene la más larga; Cantabria y Extremadura gastan más de 2.200 euros y sus pacientes llevan más de 130 días esperando. La espera depende también de cuántos pacientes entran en la lista, de cómo se organizan los quirófanos y los especialistas, y de cómo cuenta cada comunidad su propia lista.",
          "Nor do they spend the same. In 2024, the Basque Country and Asturias spent more than 2,300 euros per inhabitant on health; Andalusia, the lowest, and Madrid, the second lowest, less than 1,800. But spending more does not translate into waiting less: across the 17 regions, the relationship between spending per inhabitant and the surgical waiting time is practically zero (correlation coefficient of -0.09). Madrid spends little and has the shortest wait; Andalusia spends the least and has the longest; Cantabria and Extremadura spend more than 2,200 euros and their patients have been waiting more than 130 days. Waits also depend on how many patients join the list, on how operating theatres and specialists are organised, and on how each region counts its own list.",
        ),
        { fig: "sad2-gasto-comunidades", code: "D2" },

        { h: { es: "La ficha: los tiempos máximos de espera garantizados", en: "Policy file: guaranteed maximum waiting times" }, id: "ficha-tiempos-maximos" },
        { steps: [
          {
            title: { es: "Qué es.", en: "What it is." },
            text: {
              es: "El Real Decreto 1039/2011 garantiza a todos los usuarios del Sistema Nacional de Salud un tiempo máximo de 180 días naturales, desde que el médico indica la operación, para cinco intervenciones: cirugía cardíaca valvular, cirugía cardíaca coronaria, cataratas, prótesis de cadera y prótesis de rodilla.",
              en: "Royal Decree 1039/2011 guarantees every National Health System user a maximum of 180 calendar days, from the moment the doctor prescribes the operation, for five procedures: heart valve surgery, coronary heart surgery, cataracts, hip replacement and knee replacement.",
            },
          },
          {
            title: { es: "Quién y cuándo.", en: "Who and when." },
            text: {
              es: "Lo aprobó el Gobierno en julio de 2011, en aplicación de la Ley 16/2003 de cohesión y calidad del Sistema Nacional de Salud, y está en vigor desde el 30 de agosto de 2011. Las comunidades concretan la garantía en su territorio y pueden fijar plazos más cortos.",
              en: "The Government approved it in July 2011, under Law 16/2003 on the cohesion and quality of the National Health System, and it has been in force since 30 August 2011. The regions set out the guarantee in their own territory and can establish shorter deadlines.",
            },
          },
          {
            title: { es: "Qué debería pasar.", en: "What should happen." },
            text: {
              es: "Que ningún paciente espere más de 180 días para esas operaciones. Si el plazo no se puede cumplir, el servicio de salud debe ofrecer alternativas, como operarse en otro centro. Quien rechaza la alternativa pierde la garantía.",
              en: "No patient should wait more than 180 days for those operations. If the deadline cannot be met, the health service must offer alternatives, such as surgery at another hospital. Patients who turn down the alternative lose the guarantee.",
            },
          },
          {
            title: { es: "Con qué lo comparamos.", en: "What we compare it with." },
            text: {
              es: "Con el porcentaje de pacientes de esas operaciones que llevaban más de seis meses en la lista a 31 de diciembre de 2025, según el informe del Ministerio de Sanidad.",
              en: "With the percentage of patients waiting for those operations who had been on the list for more than six months on 31 December 2025, according to the Ministry of Health report.",
            },
          },
        ] },
        p(
          "El resultado. Seis meses equivalen, aproximadamente, a los 180 días garantizados. A finales de 2025 llevaban más de seis meses esperando el 15,9 % de los pacientes pendientes de una prótesis de rodilla y el 13,7 % de los de una prótesis de cadera. En cirugía cardíaca valvular eran el 6,9 %; en cataratas, el 2,6 %, y en cirugía coronaria, el 1,6 %. Son datos de todo el sistema: el informe no los da por comunidad. Y miden la lista estructural, de la que salen los pacientes que rechazan operarse en otro centro, así que no dicen cuántos pacientes se quedaron sin la garantía.",
          "The result. Six months are roughly equivalent to the guaranteed 180 days. At the end of 2025, 15.9% of patients waiting for a knee replacement and 13.7% of those waiting for a hip replacement had been on the list for more than six months. For heart valve surgery the figure was 6.9%; for cataracts, 2.6%, and for coronary surgery, 1.6%. These are figures for the whole system: the report does not break them down by region. And they measure the structural list, which patients who turn down surgery at another hospital leave, so they do not say how many patients lost the guarantee.",
        ),
      ],
    },
    tiempo: {
      lede: {
        es: "Hay más pacientes esperando que antes de la pandemia, y el dinero se ha ido concentrando en los hospitales.",
        en: "More patients are waiting than before the pandemic, and money has become increasingly concentrated in hospitals.",
      },
      body: [
        p(
          "La pandemia disparó la espera: en junio de 2020, los pacientes llevaban de media 170 días en la lista, frente a 121 a finales de 2019. El tiempo medio ha vuelto a ese nivel (122 días a finales de 2025), pero la lista es más larga. El máximo fue a finales de 2023, con 18,1 pacientes por cada 1.000 habitantes. Entran más pacientes que antes, 2,81 millones en 2025 frente a 2,47 millones en 2019, pero por habitante casi los mismos (58,2 por cada 1.000 frente a 57,2). En cambio, la lista por habitante es un 14 % más larga que a finales de 2019.",
          "The pandemic sent waits soaring: in June 2020, patients had been on the list for 170 days on average, against 121 at the end of 2019. The average time has returned to that level (122 days at the end of 2025), but the list is longer. The peak was at the end of 2023, with 18.1 patients per 1,000 inhabitants. More patients join than before, 2.81 million in 2025 against 2.47 million in 2019, but per inhabitant almost the same number (58.2 per 1,000 against 57.2). The list per inhabitant, by contrast, is 14% longer than at the end of 2019.",
        ),
        { fig: "sat1-lista-espera", code: "T1" },
        p(
          "En 2024, el gasto sanitario público de todas las administraciones fue de 101.739 millones de euros, y cada vez se concentra más en los hospitales y los especialistas. La factura de las recetas ha crecido mucho menos y ha perdido peso. Parte del cambio es contable: los medicamentos que se dispensan en el hospital no cuentan como farmacia, sino como gasto hospitalario, y estos datos no permiten separarlos. La atención primaria, la puerta de entrada al sistema, mantiene una parte casi igual que en 2002, en torno a uno de cada siete euros.",
          "In 2024, public health spending by all levels of government came to 101,739 million euros, and it is increasingly concentrated in hospitals and specialists. The prescription bill has grown much less and lost weight. Part of the change is an accounting one: medicines dispensed in hospital do not count as pharmacy but as hospital spending, and this data does not allow them to be separated. Primary care, the entry point to the system, keeps almost the same share as in 2002, around one in every seven euros.",
        ),
        { fig: "sat2-gasto-funciones", code: "T2" },
        p(
          "Lo que no dicen estos datos. La lista de espera mide cuánto llevan esperando los que siguen en ella, no cuánto tardaron en operarse los demás, y deja fuera a quienes esperan por decisión propia o por motivos clínicos. Cada comunidad cuenta su lista y responde de sus datos, según el propio Ministerio, que los agrega; en el pasado ha habido cambios de cómputo que rompen la serie, como el de Andalucía en 2018. El gasto por habitante no tiene en cuenta la edad de la población ni lo que pagan las mutualidades de funcionarios en cada territorio. La comparación europea mezcla sistemas con carteras de servicios distintas: el pago de los hogares es mayor donde el sistema público cubre menos, como el dentista. Y ni la espera ni el gasto dicen nada de la calidad de la atención ni de sus resultados en salud, ni permiten atribuir las diferencias a la gestión de un gobierno concreto.",
          "What this data does not say. The waiting list measures how long those still on it have waited, not how long the others took to be operated on, and it leaves out those waiting by their own choice or for clinical reasons. Each region counts its own list and is responsible for its data, according to the Ministry itself, which compiles them; in the past there have been changes in counting methods that break the series, such as Andalusia's in 2018. Spending per inhabitant does not take into account the age of the population or what the civil servants' mutual funds pay in each territory. The European comparison mixes systems with different packages of services: household payments are higher where the public system covers less, such as dental care. And neither waits nor spending say anything about the quality of care or its health outcomes, nor do they allow the differences to be attributed to the management of a particular government.",
        ),
        { see: { es: "Financiación autonómica: quién recauda, quién recibe y a quién deben las comunidades", en: "Regional finance: who raises the money, who receives it and whom the regions owe" }, href: "/financiacion-autonomica/" },
        { see: { es: "Demografía y pensiones: un país que envejece", en: "Demographics and pensions: an ageing country" }, href: "/demografia/" },
      ],
    },
  },
  sources: [
    { name: "Real Decreto 1039/2011, de 15 de julio, por el que se establecen los criterios marco para garantizar un tiempo máximo de acceso a las prestaciones sanitarias del Sistema Nacional de Salud", url: "https://www.boe.es/buscar/act.php?id=BOE-A-2011-14190" },
    { name: "Real Decreto 605/2003, de 23 de mayo, por el que se establecen medidas para el tratamiento homogéneo de la información sobre las listas de espera en el Sistema Nacional de Salud", url: "https://www.boe.es/buscar/act.php?id=BOE-A-2003-11266" },
    { name: { es: "Ministerio de Sanidad, SISLE-SNS: indicadores resumen a 31 de diciembre de 2025 (versión rectificada), con los procesos garantizados y las consultas externas", en: "Ministry of Health, SISLE-SNS: summary indicators on 31 December 2025 (corrected version), including guaranteed procedures and outpatient appointments" }, url: "https://www.sanidad.gob.es/estadEstudios/estadisticas/inforRecopilaciones/docs/LISTAS_PUBLICACION_Dic_2025_rectificado.pdf" },
    { name: { es: "Eurostat, gasto sanitario por habitante en estándares de poder adquisitivo (hlth_sha11_hf)", en: "Eurostat, health spending per inhabitant in purchasing power standards (hlth_sha11_hf)" }, url: "https://ec.europa.eu/eurostat/databrowser/view/hlth_sha11_hf/default/table" },
  ],
};

export default theme;
