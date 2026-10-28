import { p, type Theme } from "../../lib/content-types";

// Cifras comprobadas contra data/charts/ed*.json (Eurostat, descargados el 28 de octubre de 2026). Tabla de verificación en editorial/registro/a07.md.
// Gasto público en educación: Eurostat gov_10a_exp (COFOG GF09, 2024). Evolución de PISA: Eurostat sdg_04_40.
// Abandono de nativos y nacidos fuera en la UE: Eurostat edat_lfse_02 (2025).
// Ficha: Ley Orgánica 3/2022 (BOE-A-2022-5139), arts. 55.1, 66.1 y 67.2, disposiciones transitoria sexta y final novena; calendario en el Real Decreto 278/2023 (BOE-A-2023-9045), arts. 11 y 13.
const theme: Theme = {
  id: "educacion",
  code: "ED",
  slug: { es: "educacion", en: "education" },
  title: {
    es: "Educación: abandono escolar, resultados y gasto",
    en: "Education: early school leaving, results and spending",
  },
  status: "published",
  published: "2026-10-28",
  order: 8,
  dek: {
    es: "España ha reducido el abandono escolar a menos de la mitad en veinte años, pero sigue entre los países de la UE donde más jóvenes dejan los estudios sin pasar de la ESO. Le falta el escalón intermedio: tiene más titulados superiores que la media europea y muchos menos jóvenes con bachillerato o FP de grado medio. La nueva ley de FP quiere que todos los alumnos se formen también en la empresa, y los primeros datos todavía no lo reflejan.",
    en: "Spain has more than halved early school leaving in twenty years, but it is still among the EU countries where most young people leave education with no more than lower secondary. It is missing the middle rung: it has more graduates than the European average and far fewer young people whose highest qualification is upper secondary or intermediate vocational training. The new vocational training law wants every student to train in a company too, and the first data do not yet show it.",
  },
  lenses: {
    europa: {
      lede: {
        es: "España gasta menos en educación que la media de la UE, y es de los países donde más jóvenes dejan los estudios pronto.",
        en: "Spain spends less on education than the EU average, and it is one of the countries where most young people leave education early.",
      },
      body: [
        p(
          "Los colegios y los institutos los gestionan las comunidades, pero las reglas básicas del sistema son estatales: la ordenación de las etapas, los títulos, las enseñanzas mínimas, la formación profesional y las becas. Todas dependen de leyes que el Gobierno y las Cortes que salgan del 29N podrán cambiar. En 2024, el gasto público en educación equivalió al 4,1 % del PIB (dato provisional), frente al 4,7 % de la media de la UE; solo Irlanda, Grecia, Italia y Rumanía dedicaron menos. El indicador con el que la UE mide cuántos jóvenes se quedan atrás es el abandono temprano: en 2025, solo Rumanía y Alemania tenían una tasa más alta que España. Más de la mitad de los jóvenes españoles que abandonan pronto los estudios tiene trabajo, una parte mayor que en la UE.",
          "Schools are run by the regions, but the basic rules of the system are set nationally: how the stages are organised, qualifications, the core curriculum, vocational training and student grants. All of them depend on laws that the Government and parliament that emerge from the 29 November election will be able to change. In 2024, public spending on education was equivalent to 4.1% of GDP (provisional figure), against 4.7% for the EU average; only Ireland, Greece, Italy and Romania spent less. The indicator the EU uses to measure how many young people fall behind is early school leaving: in 2025, only Romania and Germany had a higher rate than Spain. More than half of the young Spaniards who leave education early have a job, a larger share than in the EU.",
        ),
        { fig: "ede1-europa-abandono", code: "E1" },
        p(
          "En lo que aprenden los alumnos que siguen en las aulas, España está en la media europea. El problema es que la media ha empeorado. Según PISA, la evaluación de la OCDE, el porcentaje de alumnos de 15 años que no llega al nivel básico de matemáticas subió en España del 27,3 % en 2022 al 33,4 % en 2025, el más alto desde que hay datos comparables (2003); entre 2003 y 2018 se había movido entre el 22,2 % y el 24,8 %. En la UE pasó del 29,5 % al 33,9 %.",
          "In what pupils who stay in the classroom learn, Spain is at the European average. The problem is that the average has worsened. According to PISA, the OECD assessment, the share of 15-year-olds who fall short of the basic level in mathematics rose in Spain from 27.3% in 2022 to 33.4% in 2025, the highest since comparable data began (2003); between 2003 and 2018 it had ranged between 22.2% and 24.8%. In the EU it went from 29.5% to 33.9%.",
        ),
        { fig: "ede2-europa-pisa", code: "E2" },
        p(
          "El nivel de estudios de los adultos jóvenes ayuda a entender el abandono. España no tiene menos titulados que Europa: tiene más jóvenes con estudios superiores, pero también muchos más que no pasaron de la ESO, y le falta el escalón intermedio. La diferencia está sobre todo en la formación profesional: solo el 10,0 % de los españoles de 25 a 34 años tiene una FP de nivel medio como estudios más altos, frente al 30,6 % en la UE.",
          "The qualifications of young adults help explain early leaving. Spain does not have fewer graduates than Europe: it has more young people with tertiary education, but also many more who did not go beyond lower secondary, and it is missing the middle rung. The gap lies mainly in vocational training: only 10.0% of Spaniards aged 25 to 34 have intermediate vocational training as their highest qualification, against 30.6% in the EU.",
        ),
        { fig: "ede3-europa-nivel", code: "E3" },
      ],
    },
    dentro: {
      lede: {
        es: "El abandono temprano casi cuadruplica en Murcia el del País Vasco, y donde más se abandona hay menos titulados superiores.",
        en: "Early school leaving in Murcia is almost four times that of the Basque Country, and where more young people drop out there are fewer graduates.",
      },
      body: [
        p(
          "Las diferencias entre comunidades son mayores que entre España y Europa. Entre 2023 y 2025, en Cantabria y Navarra abandonó pronto los estudios menos del 9 % de los jóvenes, y en el País Vasco, el 5,1 %, menos que en la mayoría de los países de la UE. En Murcia (19,3 %), Baleares (17,8 %), Andalucía y Castilla-La Mancha (15,6 % las dos) superó el 15 %. Ceuta y Melilla también están por encima del 17 %, pero con muy pocas observaciones en la encuesta.",
          "The differences between regions are larger than those between Spain and Europe. Between 2023 and 2025, fewer than 9% of young people left education early in Cantabria and Navarre, and 5.1% in the Basque Country, less than in most EU countries. In Murcia (19.3%), the Balearic Islands (17.8%), Andalusia and Castile-La Mancha (15.6% both) it was above 15%. Ceuta and Melilla are also above 17%, but with very few observations in the survey.",
        ),
        { fig: "edd1-comunidades-abandono", code: "D1" },
        p(
          "Las comunidades con más abandono son, en general, las que tienen menos adultos jóvenes con estudios superiores. Entre las 17 comunidades, la relación entre las dos tasas es muy estrecha: el coeficiente de correlación es de -0,88. Pero una correlación no dice qué causa qué. Las dos tasas pueden depender de lo mismo: la renta y los estudios de los padres, el tipo de empleo que ofrece cada economía a los jóvenes sin título o la llegada de inmigrantes y de titulados de otras comunidades. Estos datos no permiten separar esas causas, ni atribuir las diferencias a la política educativa de un gobierno autonómico concreto.",
          "The regions with the most early leaving are, in general, those with the fewest young adults with tertiary education. Across the 17 regions, the relationship between the two rates is very close: the correlation coefficient is -0.88. But a correlation does not say what causes what. Both rates may depend on the same things: parents' income and education, the kind of jobs each economy offers young people without qualifications, or the arrival of immigrants and of graduates from other regions. This data cannot separate those causes, nor attribute the differences to the education policy of a particular regional government.",
        ),
        { fig: "edd2-comunidades-superiores", code: "D2" },
      ],
    },
    tiempo: {
      lede: {
        es: "El abandono ha bajado entre los nacidos en España y entre los nacidos fuera. La FP en la empresa apenas ha empezado a crecer.",
        en: "Early leaving has fallen among those born in Spain and those born abroad. Vocational training in companies has barely begun to grow.",
      },
      body: [
        p(
          "La mayor parte de la caída del abandono se produjo entre 2008 y 2015, los años de la crisis: la tasa pasó del 31,7 % al 20,0 %. Desde entonces ha seguido bajando, más despacio, hasta el 12,8 % de 2025. La de la UE también ha bajado, pero menos, y por eso la distancia se ha estrechado.",
          "Most of the fall in early leaving happened between 2008 and 2015, the years of the crisis: the rate went from 31.7% to 20.0%. It has kept falling since then, more slowly, to 12.8% in 2025. The EU rate has also fallen, but by less, which is why the gap has narrowed.",
        ),
        { fig: "edt1-abandono", code: "T1" },
        p(
          "La bajada ha sido general. En 2025, el abandono de los jóvenes nacidos fuera de España casi triplicaba el de los nacidos en España, y su peso entre los jóvenes de 18 a 24 años ha pasado de cerca del 10 % en 2004 a cerca del 18 %. Ese cambio de composición sube la tasa total: con el peso de 2004 y las tasas de cada grupo en 2025, el abandono sería del 11,4 % en lugar del 12,8 %. Pero no lo explica todo. En la UE, el abandono de los nacidos fuera (20,5 %) también es muy superior al de los nativos (7,7 %), y los jóvenes nacidos en España siguen abandonando más (9,6 %) que los nativos del conjunto de la UE.",
          "The fall has been general. In 2025, early leaving among young people born outside Spain was almost three times that of those born in Spain, and their share of people aged 18 to 24 has gone from around 10% in 2004 to around 18%. That change in composition pushes the total rate up: with the 2004 share and each group's 2025 rate, early leaving would be 11.4% instead of 12.8%. But it does not explain everything. In the EU, early leaving among those born abroad (20.5%) is also far higher than among natives (7.7%), and young people born in Spain still leave early more often (9.6%) than natives across the EU.",
        ),
        { fig: "edt2-abandono-origen", code: "T2" },

        { h: { es: "La ficha: la ley de FP y la formación en la empresa", en: "Policy file: the vocational training law and training in companies" }, id: "ficha-ley-fp" },
        { steps: [
          {
            title: { es: "Qué es.", en: "What it is." },
            text: {
              es: "La Ley Orgánica 3/2022, de ordenación e integración de la Formación Profesional, da carácter dual a toda la FP: los ciclos formativos incluyen una fase de formación en la empresa. En el régimen general, la empresa asume entre el 25 % y el 35 % de la duración de la formación; en el intensivo, más del 35 %, con un contrato de formación.",
              en: "Organic Law 3/2022 on the organisation and integration of vocational training makes all vocational training dual: training cycles include a period of training in a company. Under the general scheme, the company takes on between 25% and 35% of the length of the training; under the intensive scheme, more than 35%, with a training contract.",
            },
          },
          {
            title: { es: "Quién y cuándo.", en: "Who and when." },
            text: {
              es: "La aprobaron las Cortes en marzo de 2022 y está en vigor desde el 21 de abril de 2022. El Real Decreto 278/2023 fijó su calendario: los nuevos ciclos empezaron a implantarse en el curso 2023-2024, el primer curso de todos se completó en el 2024-2025 y el segundo, en el 2025-2026. Las comunidades organizan la oferta.",
              en: "Parliament passed it in March 2022 and it has been in force since 21 April 2022. Royal Decree 278/2023 set its timetable: the new cycles began to be introduced in the 2023-2024 school year, the first year of all of them was completed in 2024-2025 and the second year in 2025-2026. The regions organise what is on offer.",
            },
          },
          {
            title: { es: "Qué debería pasar.", en: "What should happen." },
            text: {
              es: "Que todos los alumnos de los ciclos formativos pasen una parte de su formación en una empresa, como ya ocurre en los sistemas de FP dual de otros países europeos.",
              en: "Every student in a training cycle should spend part of their training in a company, as already happens in the dual vocational training systems of other European countries.",
            },
          },
          {
            title: { es: "Con qué lo comparamos.", en: "What we compare it with." },
            text: {
              es: "Con el porcentaje de alumnos de FP de grado básico y medio que estudian en programas que combinan centro y empresa, según la estadística de Eurostat, en España y en la UE.",
              en: "With the share of basic and intermediate vocational students in programmes that combine school and workplace, according to Eurostat statistics, in Spain and in the EU.",
            },
          },
        ] },
        { fig: "edt3-fp-dual", code: "T3" },
        p(
          "El resultado, por ahora. En el curso 2024-2025, el primero en que todos los primeros cursos seguían la nueva ley, ese porcentaje subió del 2,6 % al 4,1 %, todavía muy lejos de la UE. Es pronto para juzgar la ley: el segundo curso de todos los ciclos no se implantó hasta el 2025-2026, la ley dio de plazo hasta el 31 de diciembre de 2024 para adaptar la duración de la formación en empresa y hasta finales de 2028 para pasar de becas a contratos en el régimen intensivo. Además, cada país decide qué programas notifica como combinados, así que este dato no dice cuántos alumnos españoles pasan de hecho por una empresa.",
          "The result so far. In the 2024-2025 school year, the first in which all first-year courses followed the new law, that share rose from 2.6% to 4.1%, still very far from the EU. It is too early to judge the law: the second year of all cycles was not introduced until 2025-2026, and the law allowed until 31 December 2024 to adapt the length of company training and until the end of 2028 to move from grants to contracts under the intensive scheme. Moreover, each country decides which programmes it reports as combined, so this figure does not say how many Spanish students actually spend time in a company.",
        ),
        p(
          "Lo que no dicen estos datos. El abandono temprano sale de una encuesta, con margen de error, sobre todo en las comunidades pequeñas; cuenta a los jóvenes donde viven y no dice dónde estudiaron ni por qué dejaron los estudios. PISA mide competencias de alumnos de 15 años en tres materias, no todo lo que enseña la escuela, y sus diferencias pequeñas entre países no son significativas. El gasto en porcentaje del PIB depende también del tamaño de la economía y del número de alumnos, y esta pieza no compara el gasto por alumno de cada comunidad. Y ninguno de estos datos permite atribuir los cambios a una ley educativa concreta: el abandono ya bajaba antes de las últimas reformas, y los resultados de PISA han empeorado también en el conjunto de la UE.",
          "What this data does not say. Early leaving comes from a survey, with a margin of error, above all in small regions; it counts young people where they live and does not say where they studied or why they left. PISA measures the skills of 15-year-olds in three subjects, not everything schools teach, and small differences between countries are not significant. Spending as a percentage of GDP also depends on the size of the economy and the number of pupils, and this piece does not compare spending per pupil in each region. And none of this data allows changes to be attributed to a particular education law: early leaving was already falling before the latest reforms, and PISA results have also worsened across the EU as a whole.",
        ),
        { see: { es: "Empleo: la reforma laboral, tres años después", en: "Jobs: the labour reform, three years on" }, href: "/empleo/" },
        { see: { es: "Inmigración en datos", en: "Immigration in data" }, href: "/inmigracion/" },
      ],
    },
  },
  sources: [
    { name: "Ley Orgánica 3/2022, de 31 de marzo, de ordenación e integración de la Formación Profesional", url: "https://www.boe.es/buscar/act.php?id=BOE-A-2022-5139" },
    { name: "Real Decreto 278/2023, de 11 de abril, por el que se establece el calendario de implantación del Sistema de Formación Profesional establecido por la Ley Orgánica 3/2022, de 31 de marzo, de ordenación e integración de la Formación Profesional", url: "https://www.boe.es/buscar/act.php?id=BOE-A-2023-9045" },
    { name: { es: "Eurostat, gasto de las administraciones públicas en educación en % del PIB (gov_10a_exp, COFOG 09)", en: "Eurostat, general government spending on education as % of GDP (gov_10a_exp, COFOG 09)" }, url: "https://ec.europa.eu/eurostat/databrowser/view/gov_10a_exp/default/table" },
    { name: { es: "Eurostat, alumnos de 15 años por debajo del nivel básico en PISA, serie desde 2003 (sdg_04_40)", en: "Eurostat, 15-year-olds below the PISA baseline, series since 2003 (sdg_04_40)" }, url: "https://ec.europa.eu/eurostat/databrowser/view/sdg_04_40/default/table" },
    { name: { es: "Eurostat, abandono temprano por país de nacimiento (edat_lfse_02)", en: "Eurostat, early leavers by country of birth (edat_lfse_02)" }, url: "https://ec.europa.eu/eurostat/databrowser/view/edat_lfse_02/default/table" },
  ],
};

export default theme;
