import { p, type Theme } from "../../lib/content-types";

// Cifras comprobadas contra data/charts/jo*.json (Eurostat e INE, descargados el 13 de noviembre de 2026). Tabla de verificación en editorial/registro/a11.md.
// Ayuda al alquiler para jóvenes: Real Decreto 326/2026, artículos 132 a 138 (BOE-A-2026-8872); Bono Alquiler Joven anterior: Real Decreto 42/2022 (BOE-A-2022-802).
// Estudios citados: Aparicio-Fenoll y Oppedisano (IZA DP 6651, 2012; B.E. Journal of Economic Analysis & Policy, 2015) y Fack (Labour Economics, 2006).
const theme: Theme = {
  id: "jovenes",
  code: "JO",
  slug: { es: "jovenes", en: "young-people" },
  title: {
    es: "Jóvenes: emancipación, paro y vivienda",
    en: "Young people: leaving home, unemployment and housing",
  },
  status: "published",
  published: "2026-11-13",
  order: 12,
  dek: {
    es: "Los jóvenes españoles se van de casa casi cuatro años más tarde que la media europea, y no solo por el paro: la mayoría de los que siguen con sus padres trabaja. Hoy vive con ellos la mitad de los españoles de 25 a 34 años, más que en ningún año desde 2004, y los que se independizan lo hacen sobre todo de alquiler. El próximo Gobierno heredará una ayuda al alquiler para menores de 35 años recién ampliada, con una evidencia mixta sobre lo que consiguen estas ayudas.",
    en: "Young Spaniards leave home almost four years later than the European average, and not only because of unemployment: most of those still living with their parents have a job. Today half of Spaniards aged 25 to 34 live with them, more than in any year since 2004, and those who do move out mostly rent. The next government will inherit a newly expanded rent subsidy for under-35s, with mixed evidence on what such subsidies achieve.",
  },
  lenses: {
    europa: {
      lede: {
        es: "En España se sale de casa de los padres más tarde que en casi toda Europa, y tener trabajo no basta para hacerlo.",
        en: "In Spain people leave their parents' home later than almost anywhere else in Europe, and having a job is not enough to do so.",
      },
      body: [
        p(
          "Cuándo se independizan los jóvenes es una de las preguntas que cruzan la campaña del 29N: depende del empleo, de los salarios y del precio de la vivienda, y de ello dependen a su vez la formación de parejas y la natalidad. Según la estimación de Eurostat, en 2025 los jóvenes españoles dejaban el hogar de sus padres a los 30,2 años de media, la misma edad que en Italia y 3,9 años más tarde que la media de la UE (26,3). Solo en Croacia (31,5), Grecia y Eslovaquia (30,9) se van más tarde. En Portugal la edad es de 28,8 años; en Alemania, de 24,1; en Francia, de 23,8, y en Finlandia, de 21,3. La distancia con Europa ha crecido: en 2002 era de 2,8 años (29,3 frente a 26,5).",
          "When young people become independent is one of the questions running through the 29 November election campaign: it depends on jobs, wages and house prices, and in turn shapes when couples form and how many children are born. According to Eurostat's estimate, in 2025 young Spaniards left their parents' home at 30.2 on average, the same age as in Italy and 3.9 years later than the EU average (26.3). Only in Croatia (31.5), Greece and Slovakia (30.9) do they leave later. In Portugal the age is 28.8; in Germany, 24.1; in France, 23.8, and in Finland, 21.3. The gap with Europe has widened: in 2002 it was 2.8 years (29.3 against 26.5).",
        ),
        { fig: "joe1-europa-edad", code: "E1" },
        p(
          "La explicación más habitual es el paro, y algo explica: entre los jóvenes de 25 a 34 años que viven con sus padres, el 17,6 % está en paro en España, frente al 11,4 % en la UE. Pero la mayoría trabaja: el 66,3 %, no muy lejos del 70,2 % europeo, aunque más a menudo a tiempo parcial (14,2 % frente a 9,2 %). Como en España vive con sus padres una proporción mucho mayor de jóvenes, la diferencia con Europa está sobre todo entre los que tienen empleo. De los 20,1 puntos que separan a España (50,2 % de los jóvenes de 25 a 34 años en casa de sus padres) de la UE (30,1 %), 12,2 corresponden a jóvenes que trabajan: seis de cada diez.",
          "The most common explanation is unemployment, and it explains something: among people aged 25 to 34 who live with their parents, 17.6% are unemployed in Spain, against 11.4% in the EU. But most of them work: 66.3%, not far from the European 70.2%, although more often part-time (14.2% against 9.2%). Because a much larger share of young people live with their parents in Spain, the gap with Europe lies mainly among those with a job. Of the 20.1 points separating Spain (50.2% of people aged 25 to 34 living with their parents) from the EU (30.1%), 12.2 correspond to young people who work: six in every ten.",
        ),
        { fig: "joe2-europa-trabajan", code: "E2" },
        p(
          "Tener un empleo, por tanto, no garantiza poder independizarse. Influyen el salario, la estabilidad del contrato y lo que cuesta la vivienda, y también factores culturales: en todo el sur de Europa los jóvenes se van más tarde, con economías y mercados de vivienda distintos. Estos datos no permiten separar cuánto pesa cada cosa.",
          "Having a job, therefore, does not guarantee being able to move out. Wages, job stability and the cost of housing all play a part, and so do cultural factors: young people leave later across southern Europe, with different economies and housing markets. This data cannot separate how much each factor weighs.",
        ),
        { see: { es: "Empleo: el paro de los menores de 25 años frente a la UE", en: "Jobs: unemployment among under-25s compared with the EU" }, href: "/empleo/" },
      ],
    },
    dentro: {
      lede: {
        es: "Las diferencias entre comunidades se ven mejor en quién se queda fuera del trabajo y de los estudios, y en lo que protege tener estudios.",
        en: "The differences between regions show most clearly in who is left out of both work and education, and in how much education protects.",
      },
      body: [
        p(
          "Entre 2023 y 2025, el 11,9 % de los jóvenes españoles de 15 a 29 años no trabajaba ni estudiaba ni se formaba, algo más que la media de la UE (11,2 %). Es un grupo variado: hay quien busca empleo, quien cuida de familiares y quien ha dejado de buscar. Por comunidades, va del 8,0 % de Cantabria y el 8,1 % del País Vasco al 14,4 % de Andalucía, el 14,1 % de Canarias y el 13,7 % de Murcia. Siete comunidades están por debajo de la media europea: Aragón, Cantabria, Castilla y León, Galicia, Madrid, Navarra y el País Vasco.",
          "Between 2023 and 2025, 11.9% of young Spaniards aged 15 to 29 were neither working nor in education or training, slightly more than the EU average (11.2%). It is a varied group: some are looking for work, some care for relatives and some have stopped looking. By region, it ranges from 8.0% in Cantabria and 8.1% in the Basque Country to 14.4% in Andalusia, 14.1% in the Canary Islands and 13.7% in Murcia. Seven regions are below the European average: Aragon, Cantabria, Castile and León, Galicia, Madrid, Navarre and the Basque Country.",
        ),
        { fig: "jod1-comunidades-ninis", code: "D1" },
        p(
          "Una parte de esas diferencias tiene que ver con los estudios. Entre los jóvenes de 25 a 34 años, que en su mayoría ya han terminado de estudiar, la tasa de paro de los que no pasaron de la ESO fue del 20,9 % entre 2023 y 2025, más del doble que la de los que tienen estudios superiores (8,8 %). Ocurre en todas las comunidades, pero con distinta intensidad: en el País Vasco el paro de los menos formados (21,6 %) triplica con creces el de los que tienen estudios superiores (6,4 %); en Extremadura la distancia es menor porque el paro de los titulados también es alto (25,0 % frente a 15,7 %). Un joven con estudios superiores en Extremadura tiene casi la misma tasa de paro que uno que no pasó de la ESO en Cantabria (15,8 %).",
          "Part of those differences has to do with education. Among people aged 25 to 34, most of whom have finished studying, the unemployment rate of those with no more than lower secondary education was 20.9% between 2023 and 2025, more than double that of those with tertiary education (8.8%). This is the case in every region, but to different degrees: in the Basque Country, unemployment among the least educated (21.6%) is more than three times that of those with tertiary education (6.4%); in Extremadura the gap is smaller because unemployment among graduates is also high (25.0% against 15.7%). A young person with tertiary education in Extremadura has almost the same unemployment rate as one with no more than lower secondary education in Cantabria (15.8%).",
        ),
        { fig: "jod2-comunidades-paro-estudios", code: "D2" },
        p(
          "Estos datos describen las diferencias, pero no dicen qué las causa: influyen la estructura de cada economía (turismo, agricultura, industria), la renta de las familias y la llegada de jóvenes de otros lugares. Tampoco permite atribuir las diferencias a la política de un gobierno autonómico concreto.",
          "This data describes the differences, but does not say what causes them: the structure of each economy (tourism, agriculture, industry), family income and the arrival of young people from elsewhere all play a part. Nor does it allow the differences to be attributed to the policy of a particular regional government.",
        ),
        { see: { es: "Educación: abandono escolar, resultados y gasto", en: "Education: early school leaving, results and spending" }, href: "/educacion/" },
      ],
    },
    tiempo: {
      lede: {
        es: "En los últimos quince años se han ido de casa cada vez menos jóvenes, y los que se van ya no compran: alquilan.",
        en: "Over the last fifteen years, fewer and fewer young people have moved out, and those who do no longer buy: they rent.",
      },
      body: [
        p(
          "En 2008, el 36,6 % de los españoles de 25 a 34 años vivía con sus padres. Tras bajar ligeramente hasta 2010 (35,1 %), ha subido casi sin pausa, también en los años de crecimiento y de bajada del paro posteriores a 2014: llegó al 46,4 % en 2019 y al 50,2 % en 2025, el más alto desde que empieza la serie, en 2004. En la media de la UE apenas ha cambiado: el 29,0 % en 2010 y el 30,1 % en 2025.",
          "In 2008, 36.6% of Spaniards aged 25 to 34 lived with their parents. After dipping slightly to 2010 (35.1%), it has risen almost without pause, including in the years of growth and falling unemployment after 2014: it reached 46.4% in 2019 and 50.2% in 2025, the highest since the series began in 2004. The EU average has barely changed: 29.0% in 2010 and 30.1% in 2025.",
        ),
        { fig: "jot1-con-padres", code: "T1" },
        p(
          "También ha cambiado cómo viven los que se independizan. Entre 2006 y 2008, el 56 % de los hogares encabezados por menores de 30 años era propietario de su vivienda y el 29 % pagaba un alquiler a precio de mercado. Entre 2023 y 2025, la proporción se ha dado la vuelta: el 29 % es propietario y el 50 % paga un alquiler de mercado. No es solo cosa de los más jóvenes: entre los hogares encabezados por personas de 30 a 44 años, los propietarios han bajado del 74 % al 54 % en el mismo periodo. Alquilar no es necesariamente peor, pero en España pesa más que en la media europea: como contamos en el artículo de vivienda, el 27 % de los inquilinos a precio de mercado dedica más del 40 % de su renta a la vivienda, frente al 19 % en la UE.",
          "How those who move out live has also changed. Between 2006 and 2008, 56% of households headed by under-30s owned their home and 29% paid market rent. Between 2023 and 2025, the proportions have reversed: 29% are owners and 50% pay market rent. It is not only the youngest: among households headed by people aged 30 to 44, owners have fallen from 74% to 54% over the same period. Renting is not necessarily worse, but in Spain it weighs more than the European average: as we showed in the housing piece, 27% of tenants paying market rent spend more than 40% of their income on housing, against 19% in the EU.",
        ),
        { fig: "jot2-tenencia", code: "T2" },

        { h: { es: "La ficha: la ayuda al alquiler para jóvenes", en: "Policy file: the rent subsidy for young people" }, id: "ficha-bono-joven" },
        { steps: [
          {
            title: { es: "Qué es.", en: "What it is." },
            text: {
              es: "Una ayuda mensual para pagar el alquiler a personas de hasta 35 años. El Bono Alquiler Joven de 2022 (Real Decreto 42/2022) daba 250 euros al mes durante dos años. El Plan Estatal de Vivienda 2026-2030 (Real Decreto 326/2026, en vigor desde el 24 de abril de 2026) la sustituye por una ayuda de hasta 300 euros al mes por una vivienda y 200 por una habitación, con el límite del 60 % del alquiler.",
              en: "A monthly payment towards the rent for people aged up to 35. The 2022 Youth Rent Bonus (Royal Decree 42/2022) paid 250 euros a month for two years. The 2026-2030 State Housing Plan (Royal Decree 326/2026, in force since 24 April 2026) replaces it with a subsidy of up to 300 euros a month for a home and 200 for a room, capped at 60% of the rent.",
            },
          },
          {
            title: { es: "Quién y cuándo.", en: "Who and when." },
            text: {
              es: "La financia el Estado y la convocan y pagan las comunidades autónomas. Pueden pedirla quienes ingresen hasta cinco veces el IPREM al año y no tengan una vivienda en propiedad, por un alquiler de hasta 1.000 euros al mes (600 si es una habitación; 500 y 250 en municipios de 10.000 habitantes o menos). Se concede por dos años, prorrogables otros dos.",
              en: "It is funded by the central government and called and paid by the regional governments. It is open to those earning up to five times the IPREM (the public income benchmark) a year who do not own a home, for a rent of up to 1,000 euros a month (600 for a room; 500 and 250 in municipalities of 10,000 inhabitants or fewer). It is granted for two years, extendable for two more.",
            },
          },
          {
            title: { es: "Qué debería pasar.", en: "What should happen." },
            text: {
              es: "Que más jóvenes puedan independizarse o mantenerse en su vivienda, porque el alquiler pesa menos en su renta. El riesgo que señalan sus críticos es que, si la oferta de pisos no aumenta, una parte de la ayuda acabe en alquileres más altos.",
              en: "More young people should be able to move out or stay in their home, because rent takes a smaller share of their income. The risk its critics point to is that, if the supply of homes does not increase, part of the subsidy ends up in higher rents.",
            },
          },
          {
            title: { es: "Con qué lo comparamos.", en: "What we compare it with." },
            text: {
              es: "No hay datos públicos de beneficiarios por edad y comunidad que permitan evaluar el bono de 2022 con un grupo de control, y no hemos encontrado evaluaciones independientes. Lo comparamos con lo que se sabe de ayudas parecidas: la Renta Básica de Emancipación de 2008 en España y las ayudas a la vivienda en Francia.",
              en: "There is no public data on recipients by age and region that would allow the 2022 bonus to be evaluated against a control group, and we have found no independent evaluations. We compare it with what is known about similar subsidies: Spain's 2008 Basic Emancipation Income and housing benefits in France.",
            },
          },
        ] },
        p(
          "La Renta Básica de Emancipación pagaba desde 2008 210 euros al mes a jóvenes de 22 a 29 años que vivían de alquiler. Aparicio-Fenoll y Oppedisano compararon a los jóvenes que acababan de cumplir 22 años con los que aún no los tenían y encontraron que la ayuda aumentó la emancipación entre 0,9 y 2,3 puntos, con más efecto entre los jóvenes con menos ingresos y en las zonas con alquileres más caros. En Francia, Fack estudió una reforma que extendió las ayudas a la vivienda y estimó que cada euro de ayuda subió en 78 céntimos el alquiler de los nuevos beneficiarios, porque la oferta de vivienda apenas respondió.",
          "From 2008, the Basic Emancipation Income paid 210 euros a month to young people aged 22 to 29 who rented. Aparicio-Fenoll and Oppedisano compared young people who had just turned 22 with those who had not yet done so and found that the subsidy raised emancipation by between 0.9 and 2.3 points, with a larger effect among young people with lower incomes and in areas with higher rents. In France, Fack studied a reform that extended housing benefits and estimated that each euro of benefit raised new recipients' rent by 78 cents, because housing supply barely responded.",
        ),
        p(
          "Las dos conclusiones no se contradicen: una ayuda así puede adelantar la emancipación de algunos jóvenes y, a la vez, encarecer el alquiler si hay pocos pisos disponibles. Cuánto pesa cada efecto con el bono actual no se sabe, porque nadie lo ha evaluado de forma independiente, y la evidencia de otros países y épocas no es concluyente para la España de hoy.",
          "The two conclusions do not contradict each other: a subsidy like this can bring forward some young people's move out of home and, at the same time, push rents up if few homes are available. How much each effect weighs with the current bonus is not known, because no one has evaluated it independently, and evidence from other countries and periods is not conclusive for Spain today.",
        ),
        p(
          "Lo que no dicen estos datos. Las cifras de emancipación salen de encuestas, con su margen de error, y la edad de salida del hogar es una estimación de Eurostat. «Vivir con los padres» incluye a quien aporta ingresos a la casa o cuida de ellos, y no distingue a quien vive así por elección. No hay datos comparables de emancipación por comunidad en las fuentes que usamos, así que las diferencias territoriales se miran a través del trabajo y los estudios. La tenencia de la vivienda solo describe a los jóvenes que ya han formado su hogar: si se independizan menos, y sobre todo los que tienen más recursos, la composición de ese grupo cambia. Y nada de esto permite atribuir los cambios a una ley o a un gobierno concretos: el retraso en la emancipación empezó tras la crisis de 2008 y ha seguido con gobiernos de distinto color.",
          "What this data does not say. The figures on leaving home come from surveys, with their margin of error, and the age at which young people leave is a Eurostat estimate. «Living with parents» includes those who contribute income to the household or care for their parents, and does not distinguish those who live this way by choice. The sources we use have no comparable data on leaving home by region, so regional differences are looked at through work and education. Housing tenure only describes young people who have already formed their own household: if fewer move out, and especially those with more resources, the make-up of that group changes. And none of this allows the changes to be attributed to a particular law or government: the delay in leaving home began after the 2008 crisis and has continued under governments of different parties.",
        ),
        { see: { es: "Vivienda: por qué es el tema de estas elecciones", en: "Housing: why it is the issue of this election" }, href: "/vivienda/" },
        { see: { es: "Demografía y pensiones: un país que envejece", en: "Demographics and pensions: an ageing country" }, href: "/demografia/" },
      ],
    },
  },
  sources: [
    { name: { es: "Real Decreto 326/2026, Plan Estatal de Vivienda 2026-2030 (ayuda al alquiler para jóvenes, artículos 132 a 138)", en: "Royal Decree 326/2026, State Housing Plan 2026-2030 (rent subsidy for young people, articles 132 to 138)" }, url: "https://www.boe.es/buscar/act.php?id=BOE-A-2026-8872" },
    { name: { es: "Real Decreto 42/2022, Bono Alquiler Joven y Plan Estatal para el acceso a la vivienda 2022-2025", en: "Royal Decree 42/2022, Youth Rent Bonus and State Plan for access to housing 2022-2025" }, url: "https://www.boe.es/buscar/act.php?id=BOE-A-2022-802" },
    { name: "Aparicio-Fenoll y Oppedisano, Fostering the Emancipation of Young People: Evidence from a Spanish Rental Subsidy (IZA DP 6651)", url: "https://docs.iza.org/dp6651.pdf" },
    { name: "Fack, Are housing benefit an effective way to redistribute income? Evidence from a natural experiment in France (Labour Economics, 2006)", url: "https://ideas.repec.org/p/hal/journl/hal-00813573.html" },
  ],
};

export default theme;
