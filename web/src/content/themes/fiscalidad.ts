import { p, type Theme } from "../../lib/content-types";

// Cifras comprobadas contra data/charts/fi*.json (Eurostat, descargados el 30 de octubre de 2026). Tabla de verificación en editorial/registro/a08.md.
// Gasto en protección social por subfunción: Eurostat gov_10a_exp (COFOG GF1001-GF1007, 2024), en el campo «social» de fie3.
// Progresividad en frío: Banco de España, Documento Ocasional 2422 (2024) y Documento de Trabajo 2545 (2025).
const theme: Theme = {
  id: "fiscalidad",
  code: "FI",
  slug: { es: "impuestos", en: "taxes" },
  title: {
    es: "Impuestos y gasto público: España frente a Europa",
    en: "Taxes and public spending: Spain and Europe",
  },
  status: "published",
  published: "2026-10-30",
  order: 9,
  dek: {
    es: "España recauda menos que la media de la UE, pero la distancia es la menor desde 1995. Ya no está en el IRPF ni en sociedades, que han subido con fuerza desde 2019 y recaudan como la media europea, sino en los impuestos sobre el consumo y en las cotizaciones. En gasto, España se queda por debajo sobre todo en protección social y sanidad, y dentro de la protección social, en las ayudas a las familias.",
    en: "Spain collects less than the EU average, but the gap is the smallest since 1995. It no longer lies in personal income tax or corporate tax, which have risen sharply since 2019 and now collect as much as the European average, but in taxes on consumption and in social contributions. On spending, Spain falls short mainly in social protection and health, and within social protection, in support for families.",
  },
  lenses: {
    europa: {
      lede: {
        es: "La diferencia con Europa ya no está en lo que se paga por la renta, sino en lo que se paga al consumir y en las cotizaciones.",
        en: "The gap with Europe no longer lies in what is paid on income, but in what is paid on consumption and in social contributions.",
      },
      body: [
        p(
          "Cuánto se recauda, con qué impuestos y en qué se gasta son decisiones de las Cortes que salgan del 29N: aprueban los presupuestos y las leyes del IRPF, el IVA, el impuesto de sociedades y las cotizaciones. Las comunidades pueden fijar su parte del IRPF y los impuestos de patrimonio, sucesiones y transmisiones, dentro del marco estatal; el País Vasco y Navarra, con su régimen foral, tienen su propio IRPF e impuesto de sociedades. En 2025, los impuestos y las cotizaciones sociales equivalieron al 38,1 % del PIB en España, frente al 40,7 % en la media de la UE. España está en mitad de la tabla, entre Croacia (38,9 %) y Polonia (37,6 %). Francia es el país que más recauda (46,0 %) e Irlanda, el que menos (22,7 %), en parte porque su PIB está muy influido por las grandes multinacionales.",
          "How much is collected, with which taxes and on what it is spent are decisions for the parliament that emerges from the 29 November election: it passes the budget and the laws on personal income tax (IRPF), VAT, corporate tax and social contributions. The regions can set their share of personal income tax and the wealth, inheritance and property transfer taxes, within the national framework; the Basque Country and Navarre, with their foral regime, have their own personal income tax and corporate tax. In 2025, taxes and social contributions were equivalent to 38.1% of GDP in Spain, against 40.7% for the EU average. Spain is mid-table, between Croatia (38.9%) and Poland (37.6%). France collects the most (46.0%) and Ireland the least (22.7%), partly because its GDP is heavily influenced by large multinationals.",
        ),
        { fig: "fie1-europa-presion", code: "E1" },
        p(
          "Los 2,6 puntos de diferencia con la UE salen casi enteros de dos partidas. Los impuestos sobre el consumo y la producción recaudan 1,4 puntos menos: el IVA, el 6,8 % del PIB frente al 7,2 %, y el resto (impuestos especiales, transmisiones, IBI y otros), el 4,7 % frente al 5,7 %. Las cotizaciones sociales, 1,1 puntos menos: el 13,2 % frente al 14,3 %. En cambio, el IRPF (9,6 %) y el impuesto de sociedades (3,2 %) recaudan en España lo mismo que en la media europea, en proporción del PIB.",
          "The 2.6-point gap with the EU comes almost entirely from two items. Taxes on consumption and production collect 1.4 points less: VAT, 6.8% of GDP against 7.2%, and the rest (excise duties, property transfer tax, property tax and others), 4.7% against 5.7%. Social contributions, 1.1 points less: 13.2% against 14.3%. By contrast, personal income tax (9.6%) and corporate tax (3.2%) collect the same in Spain as in the European average, as a share of GDP.",
        ),
        { fig: "fie2-europa-impuestos", code: "E2" },
        p(
          "En el gasto, la distancia es algo mayor: en 2024, el último año con datos por funciones, 3,3 puntos del PIB. Dentro de la protección social, España gasta casi lo mismo que la UE en pensiones de jubilación (10,4 % del PIB frente a 10,6 %) y más en pensiones de viudedad y orfandad (2,2 % frente a 1,4 %) y en desempleo (1,5 % frente a 1,2 %). La diferencia está en las familias y los hijos, donde gasta la mitad (1,0 % frente a 2,0 %), en vivienda, donde el gasto en prestaciones es prácticamente nulo (0,0 % frente a 0,3 %), y en exclusión social (0,7 % frente a 0,9 %). Fuera de la protección social, la mayor distancia, además de la sanidad, está en defensa (0,9 % frente a 1,5 %) y en educación (4,1 % frente a 4,7 %).",
          "On spending, the gap is somewhat larger: in 2024, the latest year with data by function, 3.3 points of GDP. Within social protection, Spain spends almost the same as the EU on retirement pensions (10.4% of GDP against 10.6%) and more on survivors' pensions (2.2% against 1.4%) and unemployment (1.5% against 1.2%). The difference lies in families and children, where it spends half as much (1.0% against 2.0%), in housing, where spending on benefits is practically nil (0.0% against 0.3%), and in social exclusion (0.7% against 0.9%). Outside social protection, the largest gaps, besides health, are in defence (0.9% against 1.5%) and education (4.1% against 4.7%).",
        ),
        { fig: "fie3-europa-gasto", code: "E3" },
      ],
    },
    dentro: {
      lede: {
        es: "Los impuestos sobre la renta, las cotizaciones y las pensiones trasladan renta de las comunidades donde más se gana a las demás y estrechan las diferencias entre ellas.",
        en: "Income taxes, contributions and pensions shift income from the regions where people earn the most to the rest and narrow the differences between them.",
      },
      body: [
        p(
          "Las cuentas de los hogares de cada comunidad permiten ver qué pagan sus habitantes en impuestos sobre la renta y cotizaciones y qué reciben en pensiones y otras prestaciones en dinero. En 2023, los hogares del conjunto de España pagaron 1.795 euros por habitante más de lo que recibieron. Los de Madrid, Baleares (3.392) y Cataluña (3.123) son los que más aportaron en neto; los de Extremadura (391 euros) y Asturias, los únicos que recibieron más de lo que pagaron. No es un saldo entre gobiernos autonómicos: las cotizaciones y las pensiones son de la Seguridad Social, común a toda España, y lo que se paga de IRPF depende ante todo de la renta de cada contribuyente. La diferencia sale de cuánto se gana en cada territorio y de lo que se recibe en pensiones y otras prestaciones: Asturias es la comunidad que más recibe en prestaciones por habitante (7.988 euros), por delante del País Vasco (7.667).",
          "The household accounts of each region show what their inhabitants pay in income taxes and social contributions and what they receive in pensions and other cash benefits. In 2023, households across Spain paid 1,795 euros per inhabitant more than they received. Those in Madrid, the Balearic Islands (3,392) and Catalonia (3,123) contributed the most in net terms; those in Extremadura (391 euros) and Asturias were the only ones to receive more than they paid. This is not a balance between regional governments: contributions and pensions belong to Social Security, which covers all of Spain, and what is paid in personal income tax depends above all on each taxpayer's income. The difference comes from how much people earn in each territory and from what they receive in pensions and other benefits: Asturias is the region that receives the most in benefits per inhabitant (7,988 euros), ahead of the Basque Country (7,667).",
        ),
        { fig: "fid1-comunidades-saldo", code: "D1" },
        p(
          "El resultado es que las diferencias de renta entre comunidades se estrechan. Los hogares de Madrid conservan el 80,8 % de lo que ganan antes de impuestos y prestaciones; los de Asturias acaban con un 105,4 % y los de Extremadura, con un 101,7 %. Después del reparto, el País Vasco (132,4) supera a Madrid (123,7) en renta disponible por habitante, y Asturias pasa de estar por debajo de la media (91,0) a estar por encima (106,6). Andalucía es la comunidad con menos renta disponible por habitante (80,4). Estos datos no incluyen el IVA ni el gasto público en sanidad o educación, que también reparten renta, ni dicen nada sobre la gestión de los gobiernos autonómicos.",
          "The result is that income differences between regions narrow. Households in Madrid keep 80.8% of what they earn before taxes and benefits; those in Asturias end up with 105.4% and those in Extremadura with 101.7%. After redistribution, the Basque Country (132.4) overtakes Madrid (123.7) in disposable income per inhabitant, and Asturias goes from below the average (91.0) to above it (106.6). Andalusia is the region with the lowest disposable income per inhabitant (80.4). This data does not include VAT or public spending on health or education, which also redistribute income, and it says nothing about how regional governments are run.",
        ),
        { fig: "fid2-comunidades-renta", code: "D2" },
      ],
    },
    tiempo: {
      lede: {
        es: "La recaudación se hundió con el fin de la burbuja inmobiliaria y desde 2019 ha subido sobre todo por el IRPF y el impuesto de sociedades.",
        en: "Revenue collapsed when the housing bubble burst, and since 2019 it has risen mainly through personal income tax and corporate tax.",
      },
      body: [
        p(
          "En 2007, en lo más alto de la burbuja inmobiliaria, la presión fiscal llegó al 37,2 % del PIB, a 2,9 puntos de la UE. En solo dos años cayó al 30,5 %: el impuesto de sociedades pasó del 4,6 % al 2,2 % del PIB y el IVA, del 5,8 % al 3,4 %. La recuperación fue lenta, y hasta 2020 la distancia con la UE no volvió a bajar de los cinco puntos. En 2025, la presión fiscal (38,1 %) igualó el máximo de la serie, alcanzado en 2021.",
          "In 2007, at the height of the housing bubble, the tax burden reached 37.2% of GDP, 2.9 points below the EU. In just two years it fell to 30.5%: corporate tax went from 4.6% to 2.2% of GDP and VAT from 5.8% to 3.4%. The recovery was slow, and it was not until 2020 that the gap with the EU fell below five points again. In 2025, the tax burden (38.1%) matched the highest level on record, reached in 2021.",
        ),
        { fig: "fit1-presion", code: "T1" },
        p(
          "Desde 2019, la recaudación ha subido 2,9 puntos del PIB, y el IRPF y sociedades suman 2,8. En el IRPF influyen el aumento del empleo y de los salarios, los cambios en el impuesto y la llamada progresividad en frío: cuando los precios suben y los tramos y las deducciones no se actualizan, una misma renta real paga un tipo medio más alto. Un estudio del Banco de España con datos de los declarantes (Balladares y García-Miralles, 2024) estima que este efecto explica en torno a la mitad del aumento del IRPF en proporción del PIB entre 2019 y 2023. Otro estudio del Banco de España con otros bancos centrales europeos (García-Miralles y otros, 2025) estima que, en muchos de los 21 países analizados, un 1 % más de base imponible eleva la recaudación del impuesto sobre la renta entre un 1,7 % y un 2 %, y calcula qué parte de ese efecto compensaron los gobiernos con la indexación o con otras reformas. Ninguno de los dos mide con datos observados lo ocurrido en 2024 y 2025, ni explica la subida del impuesto de sociedades, que depende sobre todo de los beneficios de las empresas.",
          "Since 2019, revenue has risen by 2.9 points of GDP, and personal income tax and corporate tax together account for 2.8. Personal income tax is affected by rising employment and wages, by changes to the tax and by what is known as fiscal drag: when prices rise and tax brackets and deductions are not updated, the same real income pays a higher average rate. A Bank of Spain study using taxpayer data (Balladares and García-Miralles, 2024) estimates that this effect explains around half of the increase in personal income tax as a share of GDP between 2019 and 2023. Another Bank of Spain study with other European central banks (García-Miralles and others, 2025) estimates that, in many of the 21 countries analysed, a 1% rise in the tax base increases income tax revenue by between 1.7% and 2%, and calculates how much of that effect governments offset through indexation or other reforms. Neither of them measures what happened in 2024 and 2025 with observed data, nor explains the rise in corporate tax, which depends mainly on company profits.",
        ),
        { fig: "fit2-impuestos", code: "T2" },
        p(
          "Lo que no dicen estos datos. Recaudar un porcentaje del PIB más bajo no significa que cada contribuyente pague menos: depende de los tipos, pero también de las exenciones, del fraude y de cuánta renta y consumo hay. Los datos de 2025 son provisionales. La comparación del gasto en % del PIB no tiene en cuenta que unos países tienen más jubilados o más niños que otros, y no dice si el dinero se gasta bien. Las cuentas regionales de los hogares no incluyen el IVA ni los servicios públicos que se reciben en especie, como la sanidad o la educación. Y ninguna de estas cifras permite atribuir la subida de la recaudación a un gobierno: influyen la inflación, el empleo, los beneficios de las empresas y las decisiones de varias legislaturas.",
          "What this data does not say. Collecting a lower share of GDP does not mean that each taxpayer pays less: it depends on tax rates, but also on exemptions, tax evasion and how much income and consumption there is. The 2025 figures are provisional. Comparing spending as a share of GDP does not take into account that some countries have more retired people or more children than others, and it does not say whether the money is well spent. The regional household accounts do not include VAT or public services received in kind, such as health or education. And none of these figures allows the rise in revenue to be attributed to one government: inflation, employment, company profits and decisions taken over several parliaments all play a part.",
        ),
        { see: { es: "La legislatura en datos: cómo ha cambiado España desde julio de 2023", en: "The parliament in data: how Spain has changed since July 2023" }, href: "/la-legislatura-en-datos/" },
        { see: { es: "Financiación autonómica y deuda de las comunidades", en: "Regional funding and regional debt" }, href: "/financiacion-autonomica/" },
      ],
    },
  },
  sources: [
    { name: { es: "Balladares, S. y García-Miralles, E. (2024): Progresividad en frío: el impacto heterogéneo de la inflación sobre la recaudación por IRPF. Banco de España, Documentos Ocasionales 2422", en: "Balladares, S. and García-Miralles, E. (2024): Progresividad en frío: el impacto heterogéneo de la inflación sobre la recaudación por IRPF (fiscal drag: the uneven impact of inflation on personal income tax revenue). Bank of Spain, Occasional Papers 2422" }, url: "https://doi.org/10.53479/36733" },
    { name: { es: "García-Miralles, E. y otros (2025): Fiscal drag in theory and in practice: A European perspective. Banco de España, Documentos de Trabajo 2545", en: "García-Miralles, E. and others (2025): Fiscal drag in theory and in practice: A European perspective. Bank of Spain, Working Papers 2545" }, url: "https://repositorio.bde.es/handle/123456789/41507" },
    { name: { es: "Eurostat, gasto de las administraciones públicas en protección social por subfunción (gov_10a_exp, COFOG 10)", en: "Eurostat, general government spending on social protection by sub-function (gov_10a_exp, COFOG 10)" }, url: "https://ec.europa.eu/eurostat/databrowser/view/gov_10a_exp/default/table" },
  ],
};

export default theme;
