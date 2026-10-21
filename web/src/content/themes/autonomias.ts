import { p, type Theme } from "../../lib/content-types";

// Cifras comprobadas contra data/charts/au*.json (Eurostat, Banco de España y Fedea, descargados el 21 de octubre de 2026).
// Ficha: Ley 22/2009 (BOE-A-2009-20375). Condonación: nota de Hacienda del 9 de diciembre de 2025 y Europa Press (29/09/2026).
// Caducidad: Reglamento del Congreso, art. 207, y Real Decreto 806/2026 de disolución. Flujos de nivelación: Fedea 2026/24, cuadro 10.
const theme: Theme = {
  id: "autonomias",
  code: "AU",
  slug: { es: "financiacion-autonomica", en: "regional-finance" },
  title: {
    es: "Financiación autonómica: quién recauda, quién recibe y a quién deben las comunidades",
    en: "Regional finance: who raises the money, who receives it and whom the regions owe",
  },
  status: "published",
  published: "2026-10-21",
  order: 6,
  dek: {
    es: "Las comunidades gestionan la sanidad y la educación, y con los ayuntamientos gastan la mitad del dinero público. Se financian con un sistema de 2009 que reparte de forma desigual y deben al Estado más de la mitad de su deuda. Las dos cuestiones llegan abiertas al 29N: la ley para condonar parte de esa deuda caducó al disolverse las Cortes.",
    en: "The regions run health and education, and together with municipalities they spend half of all public money. They are funded by a 2009 system that shares money out unevenly, and they owe more than half of their debt to central government. Both questions are open on 29 November: the bill to write off part of that debt lapsed when parliament was dissolved.",
  },
  lenses: {
    europa: {
      lede: {
        es: "España es uno de los países más descentralizados de la UE, y sus comunidades, de las más endeudadas.",
        en: "Spain is one of the most decentralised countries in the EU, and its regions are among the most indebted.",
      },
      body: [
        p(
          "En 2025, las comunidades autónomas gastaron el equivalente al 16,9 % del PIB y los ayuntamientos, el 6,1 %. Juntos hacen la mitad del gasto público, una proporción solo superada en la UE por Dinamarca y parecida a la de dos países federales, Bélgica (50 %) y Alemania (47 %). Francia (20 %) e Italia (29 %) están muy por debajo. La diferencia es quién gasta: en Dinamarca o Suecia, todo lo hacen los gobiernos locales; en España, las comunidades, que tienen la sanidad, la educación y buena parte de los servicios sociales.",
          "In 2025, the regions spent the equivalent of 16.9% of GDP and municipalities 6.1%. Together they account for half of public spending, a share exceeded in the EU only by Denmark and similar to that of two federal countries, Belgium (50%) and Germany (47%). France (20%) and Italy (29%) are well below. The difference is who spends: in Denmark or Sweden, all of it is local government; in Spain, the regions, which are responsible for health, education and much of social services.",
        ),
        { fig: "aue1-europa-gasto", code: "E1" },
        p(
          "Esa descentralización viene con deuda. A finales de 2025, las comunidades debían el 20,2 % del PIB y los ayuntamientos, el 1,2 %. Solo los gobiernos regionales de Bélgica deben una proporción parecida (20,4 %); los estados federados alemanes, el 14,6 %, y los austriacos, el 6,2 %. Parte de esa deuda es una deuda dentro del propio sector público: más de la mitad se la deben las comunidades al Estado, como se ve en «España en el tiempo».",
          "That decentralisation comes with debt. At the end of 2025, the regions owed 20.2% of GDP and municipalities 1.2%. Only Belgium's regional governments owe a similar share (20.4%); the German federal states owe 14.6%, and the Austrian ones 6.2%. Part of that debt is owed within the public sector itself: the regions owe more than half of it to central government, as shown in «Spain over time».",
        ),
        { fig: "aue2-europa-deuda", code: "E2" },
      ],
    },
    dentro: {
      lede: {
        es: "Las comunidades no deben lo mismo ni reciben lo mismo. Las que menos financiación reciben por habitante están entre las más endeudadas, pero eso no lo explica todo.",
        en: "The regions do not owe the same, nor do they receive the same. Those with the least funding per inhabitant are among the most indebted, but that does not explain everything.",
      },
      body: [
        p(
          "Cuatro comunidades deben más de una cuarta parte de su PIB: la Comunidad Valenciana, Murcia (30,8 %), Castilla-La Mancha y Cataluña (28,1 % cada una). Madrid (12,3 %) y Asturias (12,5 %) están entre las que menos deben. El País Vasco (11,7 %) y Navarra (8,4 %) tienen un régimen foral: recaudan casi todos sus impuestos y pagan al Estado una cantidad, el cupo vasco y la aportación navarra, por las competencias que este mantiene. Por eso no entran en el sistema común ni en las comparaciones de financiación que siguen.",
          "Four regions owe more than a quarter of their GDP: the Valencian Community, Murcia (30.8%), Castile-La Mancha and Catalonia (28.1% each). Madrid (12.3%) and Asturias (12.5%) are among those that owe least. The Basque Country (11.7%) and Navarre (8.4%) have a foral regime: they collect almost all their own taxes and pay central government an amount, the Basque «cupo» and the Navarrese contribution, for the services it still provides. That is why they are not part of the common system or of the funding comparisons that follow.",
        ),
        { fig: "aud1-deuda-comunidades", code: "D1" },
        p(
          "Las comunidades de régimen común se financian sobre todo con impuestos cedidos: la mitad del IRPF y del IVA, el 58 % de los impuestos especiales de fabricación y tributos como patrimonio, sucesiones o transmisiones. Como lo que se recauda depende de la renta de cada territorio, el sistema lo redistribuye. El 75 % entra en un Fondo de Garantía, junto con una aportación del Estado, que se reparte según la población ajustada; después se suman otros fondos. En 2024, según los cálculos de Fedea sobre la liquidación de Hacienda, el sistema dio a las comunidades de menor renta 24.647 millones de euros más de lo que recaudaban: 13.238 los puso el Estado y 11.409, Madrid, Cataluña y Baleares, las únicas que aportaron más de lo que recibieron. Madrid aportó 8.681 millones, el 26 % de lo que recauda.",
          "The common-regime regions are funded mainly by ceded taxes: half of income tax and VAT, 58% of manufacturing excise duties and taxes such as wealth, inheritance and property transfer tax. Since what is collected depends on each territory's income, the system redistributes it. 75% goes into a Guarantee Fund, together with a central government contribution, which is shared out according to adjusted population; other funds are then added. In 2024, according to Fedea's calculations on the Finance Ministry settlement, the system gave the lower-income regions 24,647 million euros more than they collected: central government put in 13,238 million and Madrid, Catalonia and the Balearic Islands 11,409 million, as the only regions that paid in more than they received. Madrid contributed 8,681 million, 26% of what it collects.",
        ),
        { fig: "aud2-financiacion", code: "D2" },
        p(
          "El reparto no deja a todas en la media. Tras él, la financiación por habitante ajustado va de 92,0 en Murcia a 118,6 en Cantabria. Murcia, la Comunidad Valenciana, Andalucía y Castilla-La Mancha quedan por debajo de 95; Cantabria, La Rioja (112,2) y Extremadura (110,6), en cabeza. Según Fedea, el Fondo de Garantía reduce mucho las diferencias (la desviación típica del índice baja de 22,2 a 6,1 puntos), pero los fondos que añade después el Estado la suben a 7,5 y cambian el orden de las comunidades.",
          "The redistribution does not leave every region at the average. Afterwards, funding per adjusted inhabitant ranges from 92.0 in Murcia to 118.6 in Cantabria. Murcia, the Valencian Community, Andalusia and Castile-La Mancha remain below 95; Cantabria, La Rioja (112.2) and Extremadura (110.6) are at the top. According to Fedea, the Guarantee Fund greatly reduces the differences (the standard deviation of the index falls from 22.2 to 6.1 points), but the funds central government adds afterwards raise it to 7.5 and change the order of the regions.",
        ),
        p(
          "¿Tiene que ver con la deuda? En parte. En las 15 comunidades de régimen común, la relación entre financiación y deuda es negativa (coeficiente de correlación de -0,57): las dos peor financiadas, Murcia y la Comunidad Valenciana, son las dos más endeudadas. Pero no lo explica todo. Cataluña, con una financiación algo por encima de la media (102,6), comparte el tercer puesto en deuda con Castilla-La Mancha, y Andalucía, con la misma financiación que esta (94,7), debe bastante menos (18,2 %). La deuda depende también de cuánto gastó cada comunidad, de los déficits acumulados en las crisis y de las decisiones de cada gobierno, que estos datos no separan.",
          "Is it related to debt? Partly. Across the 15 common-regime regions, the relationship between funding and debt is negative (correlation coefficient of -0.57): the two worst funded, Murcia and the Valencian Community, are the two most indebted. But that does not explain everything. Catalonia, with funding slightly above average (102.6), shares third place in debt with Castile-La Mancha, and Andalusia, with the same funding as the latter (94.7), owes considerably less (18.2%). Debt also depends on how much each region spent, on the deficits built up during the crises and on each government's decisions, which this data does not separate.",
        ),

        { h: { es: "La ficha: el sistema de financiación de 2009", en: "Policy file: the 2009 funding system" }, id: "ficha-financiacion" },
        { steps: [
          {
            title: { es: "Qué es.", en: "What it is." },
            text: {
              es: "La Ley 22/2009 regula cómo se financian las 15 comunidades de régimen común: qué parte de los impuestos estatales se les cede y cómo se reparte entre ellas a través del Fondo de Garantía de Servicios Públicos Fundamentales (el 75 % de sus ingresos tributarios más una aportación del Estado) y de los fondos de Suficiencia, Cooperación y Competitividad.",
              en: "Law 22/2009 sets out how the 15 common-regime regions are funded: what share of national taxes is ceded to them and how it is shared out through the Guarantee Fund for Essential Public Services (75% of their tax revenue plus a central government contribution) and the Sufficiency, Cooperation and Competitiveness funds.",
            },
          },
          {
            title: { es: "Quién y cuándo.", en: "Who and when." },
            text: {
              es: "La aprobaron las Cortes en diciembre de 2009. Prevé valorar cada cinco años sus elementos principales, pero no se ha sustituido: la liquidación de 2024, que se paga en 2026, todavía se calcula con ella.",
              en: "Parliament passed it in December 2009. It provides for its main elements to be reviewed every five years, but it has not been replaced: the 2024 settlement, paid in 2026, is still calculated under it.",
            },
          },
          {
            title: { es: "Qué debería pasar.", en: "What should happen." },
            text: {
              es: "Que todas las comunidades tengan recursos parecidos por unidad de necesidad para prestar los servicios básicos (sanidad, educación y servicios sociales), recauden lo que recauden.",
              en: "Every region should have similar resources per unit of need to provide basic services (health, education and social services), whatever it collects.",
            },
          },
          {
            title: { es: "Con qué lo comparamos.", en: "What we compare it with." },
            text: {
              es: "Con lo que cada comunidad reúne con sus propios impuestos antes del reparto (gráfico D2), usando los cálculos de Fedea sobre la liquidación oficial.",
              en: "With what each region raises from its own taxes before redistribution (chart D2), using Fedea's calculations on the official settlement.",
            },
          },
        ] },
        p(
          "Lo que queda pendiente. En diciembre de 2025, el Consejo de Ministros envió al Congreso un proyecto de ley orgánica para que el Estado asuma 83.252 millones de euros de deuda de las comunidades de régimen común, con un ahorro de intereses estimado de unos 6.700 millones, según Hacienda. Es algo más de dos de cada diez euros de lo que debían las comunidades en junio de 2026. En julio de 2026, el Pleno rechazó las enmiendas a la totalidad y el proyecto siguió su tramitación, pero no había terminado su tramitación cuando el Real Decreto 806/2026 disolvió las Cortes el 5 de octubre. Según el Reglamento del Congreso (artículo 207), la disolución deja caducados los asuntos pendientes: el próximo Congreso tendrá que decidir si lo retoma. Ni un sistema de financiación nuevo ni la condonación se han aprobado, así que sus efectos no se pueden evaluar con datos.",
          "What remains pending. In December 2025, the Council of Ministers sent Congress an organic bill for central government to take on 83,252 million euros of the common-regime regions' debt, with estimated interest savings of around 6,700 million, according to the Finance Ministry. That is a little more than two in every ten euros the regions owed in June 2026. In July 2026, the plenary rejected the amendments to the whole bill and it continued through parliament, but it had not completed its passage when Royal Decree 806/2026 dissolved parliament on 5 October. Under the Rules of Congress (article 207), dissolution means all pending business lapses: the next Congress will have to decide whether to take it up again. Neither a new funding system nor the debt write-off has been approved, so their effects cannot be assessed with data.",
        ),
      ],
    },
    tiempo: {
      lede: {
        es: "La deuda de las comunidades se disparó tras la crisis de 2008, y desde 2012 su principal prestamista es el Estado.",
        en: "Regional debt soared after the 2008 crisis, and since 2012 the regions' main lender has been central government.",
      },
      body: [
        p(
          "Hasta 2008, la deuda de las comunidades se movió entre el 5,5 % y el 6,7 % del PIB. Con la crisis se triplicó en cinco años, hasta el 18,3 % a finales de 2012, y desde 2014 no ha bajado del 20 %. En proporción al PIB ha bajado desde 2021, pero en euros sigue creciendo: de 303.992 millones a finales de 2020 a 355.241 millones en junio de 2026.",
          "Until 2008, regional debt moved between 5.5% and 6.7% of GDP. With the crisis it tripled in five years, to 18.3% at the end of 2012, and since 2014 it has not fallen below 20%. As a share of GDP it has fallen since 2021, but in euros it keeps growing: from 303,992 million at the end of 2020 to 355,241 million in June 2026.",
        ),
        { fig: "aut1-deuda", code: "T1" },
        p(
          "En julio de 2012, con muchas comunidades con dificultades para financiarse en los mercados, el Estado creó el Fondo de Liquidez Autonómico, un mecanismo voluntario para prestarles el dinero que necesitaban para pagar sus vencimientos. Junto a él ha habido otros mecanismos del Estado con el mismo fin. Desde entonces, buena parte de la deuda nueva de las comunidades se la presta el Estado: a finales de 2024 era el acreedor del 62,8 %. En el primer semestre de 2026, la deuda con bancos, mercados y otros acreedores creció en 16.500 millones de euros, mientras la que tienen con el Estado bajó.",
          "In July 2012, with many regions struggling to borrow on the markets, central government created the Regional Liquidity Fund, a voluntary mechanism to lend them the money they needed to meet their maturities. Other central government mechanisms with the same aim have operated alongside it. Since then, much of the regions' new debt has been lent by central government: at the end of 2024 it was the creditor for 62.8% of it. In the first half of 2026, debt owed to banks, markets and other creditors grew by 16,500 million euros, while debt owed to central government fell.",
        ),
        { fig: "aut2-acreedores", code: "T2" },
        p(
          "Para el conjunto de las administraciones, lo que una comunidad debe al Estado se compensa con lo que el Estado tiene prestado: por eso la deuda pública total, la que se compara con Europa, no lo cuenta dos veces. Si el Estado asume parte de esa deuda, baja la de las comunidades, pero la del conjunto de las administraciones no cambia: cambia quién la debe.",
          "For government as a whole, what a region owes central government is offset by what central government has lent: that is why total public debt, the figure compared across Europe, does not count it twice. If central government takes on part of that debt, regional debt falls, but debt for government as a whole does not change: what changes is who owes it.",
        ),
        p(
          "Lo que no dicen estos datos. La deuda mide lo que se debe, no si el dinero se gastó bien ni en qué. La financiación por habitante ajustado es un cálculo de Fedea a igual esfuerzo fiscal: no incluye lo que cada comunidad recauda de más o de menos al subir o bajar sus impuestos, y Fedea presenta los resultados de 2024 como provisionales. La población ajustada es la estimación de necesidades que fija la propia ley, y se discute. Las forales no se pueden comparar con la misma medida. Estos datos no permiten atribuir la deuda de una comunidad a su financiación, a su gestión o a un gobierno concreto. Y la comparación europea suma niveles de gobierno que no tienen las mismas competencias en cada país.",
          "What this data does not say. Debt measures what is owed, not whether the money was well spent or on what. Funding per adjusted inhabitant is a Fedea calculation at equal tax effort: it does not include what each region collects above or below that by raising or lowering its taxes, and Fedea presents the 2024 results as provisional. Adjusted population is the estimate of needs set by the law itself, and it is debated. The foral regions cannot be compared with the same measure. This data does not allow a region's debt to be attributed to its funding, its management or a particular government. And the European comparison adds up levels of government that do not have the same responsibilities in each country.",
        ),
        { see: { es: "La legislatura en datos: deuda y déficit del conjunto de las administraciones", en: "The parliament in data: debt and deficit for government as a whole" }, href: "/la-legislatura-en-datos/" },
      ],
    },
  },
  sources: [
    { name: "Ley 22/2009, de 18 de diciembre, por la que se regula el sistema de financiación de las Comunidades Autónomas de régimen común", url: "https://www.boe.es/buscar/act.php?id=BOE-A-2009-20375" },
    { name: "A. de la Fuente (Fedea), La liquidación de 2024 del sistema de financiación de las comunidades autónomas de régimen común", url: "https://documentos.fedea.net/pubs/eee/2026/eee2026-24.pdf" },
    { name: { es: "Ministerio de Hacienda: el Consejo de Ministros aprueba el proyecto de ley de condonación de deuda (9 de diciembre de 2025)", en: "Finance Ministry: the Council of Ministers approves the debt write-off bill (9 December 2025)" }, url: "https://www.hacienda.gob.es/es-ES/Prensa/Noticias/Paginas/2025/20251209-NP-CM-CONDONACION-DEUDA-CCAA.aspx" },
    { name: { es: "Europa Press (en LegalToday): el Congreso reactiva la ley para condonar deuda a las comunidades (29 de septiembre de 2026)", en: "Europa Press (via LegalToday): Congress revives the bill to write off regional debt (29 September 2026)" }, url: "https://www.legaltoday.com/actualidad-juridica/noticias-de-derecho/el-congreso-reactiva-la-ley-para-condonar-deuda-a-las-comunidades-autonomas-tras-casi-un-ano-guardada-en-un-cajon-2026-09-29/" },
    { name: { es: "BOE: Real Decreto 806/2026, de disolución del Congreso y del Senado y de convocatoria de elecciones", en: "BOE (official gazette): Royal Decree 806/2026 dissolving Congress and the Senate and calling the election" }, url: "https://www.boe.es/buscar/doc.php?id=BOE-A-2026-20742" },
    { name: { es: "Reglamento del Congreso de los Diputados (artículo 207: caducidad de los asuntos pendientes)", en: "Rules of the Congress of Deputies (article 207: pending business lapses)" }, url: "https://www.boe.es/buscar/act.php?id=BOE-A-1982-5196" },
    { name: { es: "BOE: Real Decreto-ley 21/2012, de medidas de liquidez de las Administraciones públicas (Fondo de Liquidez Autonómico)", en: "BOE: Royal Decree-law 21/2012 on liquidity measures for public administrations (Regional Liquidity Fund)" }, url: "https://www.boe.es/buscar/act.php?id=BOE-A-2012-9365" },
  ],
};

export default theme;
