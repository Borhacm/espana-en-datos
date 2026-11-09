import { p, type Theme } from "../../lib/content-types";

// Cifras comprobadas contra data/charts/pr*.json (Eurostat e INE, descargados el 9 de noviembre de 2026). Tabla de verificación en editorial/registro/a10.md.
// Objetivo de financiación pública de la I+D: Ley 17/2022, disposición adicional sexta (BOE-A-2022-14581).
const theme: Theme = {
  id: "productividad",
  code: "PR",
  slug: { es: "productividad", en: "productivity" },
  title: {
    es: "Productividad y empresa: por qué España crece pero no converge",
    en: "Productivity and business: why Spain grows but does not catch up",
  },
  status: "published",
  published: "2026-11-09",
  order: 11,
  dek: {
    es: "España produce por habitante un 8,6 % menos que la media de la UE, y la distancia no se ha reducido desde 2011. La mitad se explica porque trabaja menos gente y la otra mitad porque cada hora de trabajo produce menos: desde 2000, la productividad por hora ha crecido un 18,7 % en España y un 27,7 % en la UE. El tamaño de las empresas explica poco de esa diferencia; el gasto en I+D de las empresas, poco más de la mitad del europeo, es una de las piezas que faltan.",
    en: "Spain produces 8.6% less per person than the EU average, and the gap has not narrowed since 2011. Half of it is because fewer people work and the other half because each hour of work produces less: since 2000, productivity per hour has grown by 18.7% in Spain and 27.7% in the EU. Firm size explains little of that difference; business R&D spending, little more than half the European level, is one of the missing pieces.",
  },
  lenses: {
    europa: {
      lede: {
        es: "España está por debajo de la media europea en riqueza por habitante, y no solo porque trabaje menos gente: cada hora trabajada produce menos que en la UE.",
        en: "Spain is below the European average in output per person, and not only because fewer people work: each hour worked produces less than in the EU.",
      },
      body: [
        p(
          "La productividad, lo que se produce por cada hora de trabajo, es a largo plazo lo que permite subir los salarios sin perder empleo y pagar más gasto público sin subir impuestos: por eso pesa en casi todo lo que se discute ante el 29N, de las pensiones a la vivienda. En 2025, el PIB por habitante de España, una vez descontado que los precios son distintos en cada país, era el 91,4 % de la media de la UE. Francia (97,5), Italia (95,9) y Chequia (92,3) están algo por encima; Eslovenia (91,1), justo por debajo, y Portugal (81,4) y Polonia (81,1), más lejos. Irlanda y Luxemburgo encabezan la lista por razones que poco tienen que ver con el nivel de vida de sus habitantes: los beneficios de las multinacionales y los trabajadores que viven en otros países.",
          "Productivity, what is produced per hour of work, is in the long run what allows wages to rise without losing jobs and more public spending to be paid for without raising taxes: that is why it bears on almost everything being debated ahead of the 29 November election, from pensions to housing. In 2025, Spain's GDP per person, once differences in price levels between countries are taken into account, was 91.4% of the EU average. France (97.5), Italy (95.9) and Czechia (92.3) are slightly above; Slovenia (91.1) is just below, and Portugal (81.4) and Poland (81.1) further behind. Ireland and Luxembourg top the list for reasons that have little to do with their residents' living standards: multinational profits and workers who live in other countries.",
        ),
        { fig: "pre1-europa-pib", code: "E1" },
        p(
          "El PIB por habitante se puede descomponer en dos factores: cuánto se produce por hora trabajada y cuántas horas se trabajan por habitante. España está por debajo en los dos. En horas, no es porque cada ocupado trabaje menos: trabaja de media 1.633 horas al año, frente a 1.605 en la UE. Es porque hay menos ocupados por habitante: 94,3 por cada 100 en la UE. Lo que queda es la productividad: cada hora de trabajo en España genera un 4,7 % menos que la media europea.",
          "GDP per person can be broken down into two factors: how much is produced per hour worked and how many hours are worked per person. Spain is below on both. On hours, it is not because each worker works less: the average worker puts in 1,633 hours a year, against 1,605 in the EU. It is because there are fewer workers per person: 94.3 for every 100 in the EU. What remains is productivity: each hour of work in Spain generates 4.7% less than the European average.",
        ),
        { fig: "pre2-europa-brecha", code: "E2" },
        p(
          "Una explicación habitual es que en España hay demasiadas empresas pequeñas, que producen menos por trabajador. Las estadísticas de empresas de Eurostat matizan esa idea. En 2023, el 32,8 % de las personas que trabajaban en empresas de la industria, la construcción y los servicios de mercado lo hacía en microempresas de menos de diez personas, frente al 29,8 % en la UE, y el 34,8 % en empresas de 250 o más, frente al 36,5 %. Es una diferencia real, pero pequeña. Cada persona ocupada en esas empresas generó 54.700 euros de valor añadido en España y 64.500 en la UE. Si el empleo español se repartiera por tamaños como el europeo, con la productividad de cada tamaño en España, serían 55.600 euros: el tamaño explica menos de una décima parte de la distancia. La mayor diferencia está en las grandes empresas: 70.500 euros por persona en España, frente a 86.800 en la UE.",
          "A common explanation is that Spain has too many small firms, which produce less per worker. Eurostat's business statistics qualify that idea. In 2023, 32.8% of people working in firms in industry, construction and market services worked in micro-enterprises with fewer than ten people, against 29.8% in the EU, and 34.8% in firms with 250 or more, against 36.5%. It is a real difference, but a small one. Each person employed in those firms generated 54,700 euros of value added in Spain and 64,500 in the EU. If Spanish employment were spread across firm sizes like European employment, with each size's productivity in Spain, it would be 55,600 euros: firm size explains less than a tenth of the gap. The biggest difference is in large firms: 70,500 euros per person in Spain, against 86,800 in the EU.",
        ),
        { fig: "pre3-europa-tamano", code: "E3" },
      ],
    },
    dentro: {
      lede: {
        es: "Las diferencias de riqueza entre comunidades son grandes, pero se deben tanto a cuánta gente trabaja como a lo que produce cada hora.",
        en: "The differences in output between regions are large, but they are due as much to how many people work as to what each hour produces.",
      },
      body: [
        p(
          "Según la primera estimación del INE para 2025, el PIB por habitante fue de 34.237 euros en el conjunto de España. Madrid (47.220), el País Vasco (42.492), Navarra (40.421) y Cataluña (39.199) están a la cabeza; Andalucía (26.091), Extremadura (26.740), Canarias (27.190) y Castilla-La Mancha (27.307), a la cola. El dato de Madrid está inflado, y el de Castilla-La Mancha rebajado, porque el PIB se cuenta donde se trabaja y la población donde se vive, y muchos trabajadores de Madrid viven en las provincias vecinas.",
          "According to INE's first estimate for 2025, GDP per person was 34,237 euros for Spain as a whole. Madrid (47,220), the Basque Country (42,492), Navarre (40,421) and Catalonia (39,199) are at the top; Andalusia (26,091), Extremadura (26,740), the Canary Islands (27,190) and Castile-La Mancha (27,307) at the bottom. Madrid's figure is inflated, and Castile-La Mancha's depressed, because GDP is counted where people work and population where they live, and many of Madrid's workers live in neighbouring provinces.",
        ),
        { fig: "prd1-comunidades-pib", code: "D1" },
        p(
          "Por hora trabajada, el orden cambia y la distancia se reduce: la comunidad más productiva produce 1,41 veces lo que la menos productiva, frente a 1,81 veces en PIB por habitante. Con España igual a 100, Madrid tiene un PIB por habitante de 137,9, pero una productividad por hora de 111,2: su ventaja viene sobre todo de las horas trabajadas por habitante (124,0). En Andalucía pesan casi lo mismo los dos factores: produce por hora un 88,4 % de la media y trabaja un 86,2 % de las horas por habitante. Murcia, en cambio, trabaja casi tantas horas por habitante como la media (97,1) y tiene la productividad por hora más baja (84,4), sin contar Ceuta y Melilla. Las tres comunidades que más producen por hora son también las que más gastan en I+D: Navarra (2,34 % de su PIB en 2024), el País Vasco (2,30 %) y Madrid (2,18 %). Pero la relación no es general: Baleares, la cuarta en productividad por hora, es la comunidad autónoma que menos gasta (0,39 %).",
          "Per hour worked, the order changes and the gap narrows: the most productive region produces 1.41 times as much as the least productive, against 1.81 times in GDP per person. With Spain equal to 100, Madrid has a GDP per person of 137.9 but productivity per hour of 111.2: its advantage comes mainly from hours worked per person (124.0). In Andalusia both factors weigh almost equally: it produces 88.4% of the average per hour and works 86.2% of the hours per person. Murcia, on the other hand, works almost as many hours per person as the average (97.1) and has the lowest productivity per hour (84.4), leaving aside Ceuta and Melilla. The three regions that produce most per hour are also those that spend most on R&D: Navarre (2.34% of its GDP in 2024), the Basque Country (2.30%) and Madrid (2.18%). But the relationship is not general: the Balearic Islands, fourth in productivity per hour, spend the least of all the autonomous communities (0.39%).",
        ),
        { fig: "prd2-comunidades-hora", code: "D2" },
      ],
    },
    tiempo: {
      lede: {
        es: "España se acercó a Europa en los años del crecimiento con más empleo; desde la crisis financiera no ha recuperado el terreno perdido, porque la productividad por hora crece más despacio que en la UE.",
        en: "Spain caught up with Europe in the years of job-rich growth; since the financial crisis it has not regained the lost ground, because productivity per hour grows more slowly than in the EU.",
      },
      body: [
        p(
          "Entre 1995 y 2006, el PIB por habitante de España pasó del 91,4 % al 104,9 % de la media de la UE. No fue porque cada hora produjera más: la productividad por hora, que en 1995 estaba en el 109,3 % de la media europea, bajó al 96,8 % en 2004. España convergió porque trabajaba mucha más gente: los ocupados por habitante pasaron del 83,2 % de la media europea en 1995 al 103,6 % en 2006. La crisis de 2008 destruyó buena parte de ese empleo (87,1 % en 2013) y el PIB por habitante cayó al 89,7 %. Desde entonces el empleo se ha recuperado en parte (94,3 % en 2025), pero la distancia con Europa no se ha cerrado: el PIB por habitante está en el mismo 91,4 % de 1995. En volumen, sin el efecto de los precios, la productividad por hora ha crecido un 18,7 % desde 2000 en España y un 27,7 % en la UE; desde 2019, un 2,0 % y un 3,4 %.",
          "Between 1995 and 2006, Spain's GDP per person rose from 91.4% to 104.9% of the EU average. It was not because each hour produced more: productivity per hour, which in 1995 stood at 109.3% of the European average, fell to 96.8% in 2004. Spain caught up because many more people were working: workers per person rose from 83.2% of the European average in 1995 to 103.6% in 2006. The 2008 crisis destroyed much of that employment (87.1% in 2013) and GDP per person fell to 89.7%. Since then employment has partly recovered (94.3% in 2025), but the gap with Europe has not closed: GDP per person stands at the same 91.4% as in 1995. In volume terms, without the effect of prices, productivity per hour has grown by 18.7% since 2000 in Spain and 27.7% in the EU; since 2019, by 2.0% and 3.4%.",
        ),
        { fig: "prt1-convergencia", code: "T1" },
        p(
          "Una de las causas que más se citan es la inversión en conocimiento. En 2024, España dedicó a investigación y desarrollo el 1,50 % de su PIB, frente al 2,26 % de la UE; catorce de los otros 26 países gastan más. Casi toda la diferencia está en las empresas: las españolas ejecutaron I+D por el 0,84 % del PIB y las europeas, por el 1,50 %. El gasto subió hasta el 1,36 % en 2009, cayó con los recortes de la crisis hasta el 1,18 % en 2016 y desde entonces ha vuelto a crecer. El salto de 2020 coincide con la caída del PIB por la pandemia, que eleva el porcentaje aunque el gasto no cambie.",
          "One of the most frequently cited causes is investment in knowledge. In 2024, Spain devoted 1.50% of its GDP to research and development, against 2.26% in the EU; fourteen of the other 26 countries spend more. Almost all of the difference lies in businesses: Spanish firms carried out R&D worth 0.84% of GDP and European firms 1.50%. Spending rose to 1.36% in 2009, fell with the crisis cuts to 1.18% in 2016 and has grown again since. The jump in 2020 coincides with the fall in GDP during the pandemic, which raises the percentage even if spending does not change.",
        ),
        { fig: "prt2-id", code: "T2" },

        { h: { es: "La ficha: el objetivo de financiación pública de la ley de la ciencia", en: "Policy file: the public funding target in the science law" }, id: "ficha-ley-ciencia" },
        { steps: [
          {
            title: { es: "Qué es.", en: "What it is." },
            text: {
              es: "La Ley 17/2022, que reformó la Ley de la Ciencia, la Tecnología y la Innovación de 2011, establece en su disposición adicional sexta que los presupuestos de los organismos públicos del sistema de ciencia se encuadren en un marco a medio plazo, con el objetivo de que la financiación pública en I+D aumente regularmente hasta alcanzar el 1,25 % del PIB en 2030.",
              en: "Law 17/2022, which reformed the 2011 Science, Technology and Innovation Law, provides in its sixth additional provision that the budgets of the public bodies in the science system be set within a medium-term framework, with the aim of public R&D funding rising steadily to reach 1.25% of GDP in 2030.",
            },
          },
          {
            title: { es: "Quién y cuándo.", en: "Who and when." },
            text: {
              es: "La aprobaron las Cortes en septiembre de 2022, siguiendo una recomendación del Consejo de la UE de 2021 sobre un pacto europeo de investigación e innovación. El objetivo se cumple o no con los presupuestos de cada año, que dependen del Gobierno y de las Cortes que salgan del 29N, y también de las comunidades autónomas.",
              en: "Parliament passed it in September 2022, following a 2021 recommendation by the Council of the EU on a pact for research and innovation in Europe. Whether the target is met depends on each year's budgets, which depend on the government and parliament that emerge from the 29 November election, and also on the regions.",
            },
          },
          {
            title: { es: "Qué debería pasar.", en: "What should happen." },
            text: {
              es: "Que la parte del gasto en I+D que pagan las administraciones crezca cada año hasta llegar al 1,25 % del PIB en 2030.",
              en: "The share of R&D spending paid for by government should grow every year until it reaches 1.25% of GDP in 2030.",
            },
          },
          {
            title: { es: "Con qué lo comparamos.", en: "What we compare it with." },
            text: {
              es: "Con la financiación pública del gasto en I+D que publica Eurostat desde 2019, antes de la ley, y con el ritmo que haría falta para llegar al objetivo.",
              en: "With the public funding of R&D spending published by Eurostat since 2019, before the law, and with the pace needed to reach the target.",
            },
          },
        ] },
        p(
          "Las administraciones financiaron I+D por el 0,58 % del PIB en 2024, frente al 0,47 % en 2019 y el 0,64 % de 2009, el máximo de la serie. Ha subido unas dos centésimas al año; para llegar al 1,25 % en 2030 harían falta unas once al año, cinco veces más deprisa. En la UE, la financiación pública fue del 0,68 % del PIB en 2023. La ley no precisa con qué indicador se mide el objetivo: el de Eurostat no incluye las deducciones fiscales por I+D ni lo que se financia fuera de España, así que la comparación es orientativa.",
          "Government funded R&D worth 0.58% of GDP in 2024, against 0.47% in 2019 and 0.64% in 2009, the highest in the series. It has risen by about two hundredths of a point a year; reaching 1.25% by 2030 would take about eleven a year, five times faster. In the EU, public funding was 0.68% of GDP in 2023. The law does not specify which indicator the target is measured with: Eurostat's does not include R&D tax credits or funding for R&D carried out outside Spain, so the comparison is indicative.",
        ),
        p(
          "Lo que no dicen estos datos. La productividad que mide la contabilidad nacional es una media: no distingue entre una empresa que produce más porque innova y otra que lo hace porque sube precios, ni separa el efecto de la mezcla de sectores: una economía con más peso de actividades que producen poco por hora tiene una productividad media más baja aunque cada empresa sea tan eficiente como sus competidoras europeas. Las comparaciones en paridad de poder de compra sirven para comparar países en un año, no para medir con precisión cuánto ha cambiado la distancia. Los datos por comunidad son una primera estimación y se revisarán. Y que el gasto en I+D y la productividad vayan juntos no prueba que uno cause la otra, ni permite atribuir la evolución de la productividad a ningún gobierno: depende también de la inversión, de la formación de los trabajadores, del funcionamiento de los mercados y de la llegada de nuevos trabajadores, entre otras cosas.",
          "What this data does not say. Productivity as measured by the national accounts is an average: it does not distinguish between a firm that produces more because it innovates and one that does so because it raises prices, nor does it separate the effect of the sector mix: an economy where activities that produce little per hour weigh more has lower average productivity even if each firm is as efficient as its European competitors. Comparisons in purchasing power standards are meant to compare countries in a given year, not to measure precisely how much the gap has changed. The regional data are a first estimate and will be revised. And the fact that R&D spending and productivity go together does not prove that one causes the other, nor does it allow the evolution of productivity to be attributed to any government: it also depends on investment, workers' skills, how markets work and the arrival of new workers, among other things.",
        ),
        { see: { es: "La legislatura en datos: cómo ha cambiado España desde julio de 2023", en: "The parliament in data: how Spain has changed since July 2023" }, href: "/la-legislatura-en-datos/" },
        { see: { es: "Empleo: la reforma laboral, tres años después", en: "Jobs: the labour reform, three years on" }, href: "/empleo/" },
      ],
    },
  },
  sources: [
    { name: "Ley 17/2022, de 5 de septiembre, por la que se modifica la Ley 14/2011, de 1 de junio, de la Ciencia, la Tecnología y la Innovación (disposición adicional sexta)", url: "https://www.boe.es/buscar/doc.php?id=BOE-A-2022-14581" },
    { name: { es: "Eurostat, gasto en I+D por sector de ejecución y por regiones (rd_e_gerdtot y rd_e_gerdreg)", en: "Eurostat, R&D expenditure by sector of performance and by region (rd_e_gerdtot and rd_e_gerdreg)" }, url: "https://ec.europa.eu/eurostat/databrowser/view/rd_e_gerdtot/default/table" },
  ],
};

export default theme;
