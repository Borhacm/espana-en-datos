import { p, type Theme } from "../../lib/content-types";

// Cifras comprobadas contra data/charts/vi*.json (INE, Eurostat y Generalitat, descargados el 6 de octubre de 2026).
// Estudios citados: Monràs y García-Montalvo (UPF, documento de trabajo 1836, versión de abril de 2022) y
// Jofre-Monseny, Martínez-Mazza y Segú (UB, 2022; publicado en Regional Science and Urban Economics, 2023).
const theme: Theme = {
  id: "vivienda",
  code: "VI",
  slug: { es: "vivienda", en: "housing" },
  title: { es: "Vivienda: por qué es el tema de estas elecciones", en: "Housing: why it is the issue of this election" },
  status: "published",
  published: "2026-10-06",
  updated: "2026-10-19",
  order: 1,
  dek: {
    es: "Las elecciones del 29N se convocaron después de que el Congreso rechazara dos decretos de alquiler. Los datos explican por qué la vivienda está en el centro: desde 2015 ha subido un 80 %, y los salarios, un 25 %.",
    en: "The 29 November election was called after Congress rejected two rental decrees. The data explains why housing is at the centre: since 2015 house prices have risen 80%, and wages 25%.",
  },
  lenses: {
    europa: {
      lede: {
        es: "España no es donde más ha subido la vivienda, pero sí uno de los países donde el alquiler más pesa.",
        en: "Spain is not where house prices have risen most, but it is one of the countries where rent weighs most.",
      },
      body: [
        p(
          "Desde 2015, la vivienda ha subido un 81 % en España, por encima de la media de la UE (62 %), de Alemania (53 %), Francia (27 %) e Italia (16 %). Otros países han ido mucho más lejos: en Portugal ha subido un 164 % y en Hungría se ha multiplicado por más de tres y media.",
          "Since 2015, house prices have risen 81% in Spain, above the EU average (62%), Germany (53%), France (27%) and Italy (16%). Other countries have gone much further: in Portugal prices have risen 164% and in Hungary they have multiplied by more than three and a half.",
        ),
        { fig: "vie1-europa-precios", code: "E1" },
        p(
          "Donde España destaca es en lo que cuesta vivir de alquiler. El 27 % de los inquilinos que pagan precio de mercado dedica más del 40 % de su renta a la vivienda, frente al 19 % de la media europea. Es el octavo porcentaje más alto de la UE.",
          "Where Spain stands out is in what it costs to rent. 27% of tenants paying market rent spend more than 40% of their income on housing, against 19% on average in Europe. It is the eighth highest share in the EU.",
        ),
        { fig: "vie2-europa-sobrecarga", code: "E2" },
      ],
    },
    dentro: {
      lede: {
        es: "En Madrid la vivienda ha doblado su precio desde 2015; en Extremadura ha subido un 40 %. Y Cataluña lleva dos años probando los topes al alquiler.",
        en: "In Madrid house prices have doubled since 2015; in Extremadura they have risen 40%. And Catalonia has spent two years trying out rent caps.",
      },
      body: [
        p(
          "La subida no ha sido igual en todas partes. En Madrid el precio prácticamente se ha duplicado desde 2015 y en Baleares ha subido un 95 %. En el otro extremo están Castilla-La Mancha (43 %) y Extremadura (40 %).",
          "The rise has not been the same everywhere. In Madrid prices have practically doubled since 2015 and in the Balearic Islands they have risen 95%. At the other end are Castile-La Mancha (43%) and Extremadura (40%).",
        ),
        { fig: "vid1-comunidades", code: "D1" },

        { h: { es: "La ficha: topes al alquiler en Cataluña", en: "Policy file: rent caps in Catalonia" }, id: "ficha-topes" },
        { steps: [
          {
            title: { es: "Qué es.", en: "What it is." },
            text: {
              es: "Un límite a la renta de los nuevos contratos de alquiler de vivienda habitual en las zonas declaradas «de mercado residencial tensionado», según el índice de referencia del Ministerio de Vivienda. Lo permite la Ley 12/2023, por el derecho a la vivienda.",
              en: "A cap on the rent of new long-term residential leases in areas declared «stressed residential markets», based on the Housing Ministry's reference index. It is allowed by Law 12/2023 on the right to housing.",
            },
          },
          {
            title: { es: "Quién y cuándo.", en: "Who and when." },
            text: {
              es: "La declaración la pide cada comunidad. Cataluña es la que más tiempo lleva aplicándolo y la que cubre más municipios: 140 desde el 16 de marzo de 2024 y 131 más desde el 10 de octubre de 2024. El País Vasco, Navarra, Galicia y Asturias lo han empezado a aplicar después en algunos municipios. Antes, una ley catalana de 2020 limitó las rentas hasta que el Tribunal Constitucional la anuló en marzo de 2022.",
              en: "Each region applies for the declaration. Catalonia has been applying it the longest and covers the most municipalities: 140 since 16 March 2024 and 131 more since 10 October 2024. The Basque Country, Navarre, Galicia and Asturias have since started applying it in some municipalities. Before that, a 2020 Catalan law capped rents until the Constitutional Court struck it down in March 2022.",
            },
          },
          {
            title: { es: "Qué debería pasar.", en: "What should happen." },
            text: {
              es: "Que las rentas de los nuevos contratos suban menos. El riesgo que señalan sus críticos es que haya menos pisos en alquiler habitual.",
              en: "Rents on new leases should rise less. The risk its critics point to is that fewer homes are offered for long-term rent.",
            },
          },
          {
            title: { es: "Con qué lo comparamos.", en: "What we compare it with." },
            text: {
              es: "Con los municipios catalanes sin tope, usando la misma fuente: las fianzas de alquiler que se depositan en la Generalitat.",
              en: "With Catalan municipalities without a cap, using the same source: the rental deposits lodged with the Catalan government.",
            },
          },
        ] },
        p(
          "Antes de 2024, las rentas de los nuevos contratos subían al mismo ritmo en los municipios que luego tendrían tope y en los demás. Desde que se aplica, se han separado: en el último año, la renta media en los municipios con tope desde marzo de 2024 estaba un 4 % por encima de 2023, y en los municipios sin tope, un 12 %.",
          "Before 2024, rents on new leases rose at the same pace in the municipalities that would later have a cap and in the rest. Since it has applied, they have diverged: in the last year, the average rent in municipalities capped since March 2024 was 4% above 2023, and in municipalities without a cap, 12%.",
        ),
        { fig: "vid2-cataluna-rentas", code: "D2" },
        p(
          "Al mismo tiempo, se firman menos contratos: un 20 % menos que en 2023 en los municipios con tope, frente a un 2 % menos en los que no lo tienen. Puede significar que hay menos pisos en alquiler habitual (porque pasan al alquiler de temporada o se venden), pero también que los inquilinos se mudan menos para no perder su renta. Estos datos no permiten distinguirlo.",
          "At the same time, fewer contracts are being signed: 20% fewer than in 2023 in capped municipalities, against 2% fewer in those without a cap. It may mean there are fewer homes for long-term rent (because they move to seasonal lets or are sold), but also that tenants move less so as not to lose their rent. This data cannot tell the two apart.",
        ),
        { fig: "vid3-cataluna-contratos", code: "D3" },
        p(
          "Lo que dice la investigación sobre la ley catalana de 2020, que funcionaba de forma parecida: dos estudios con datos de fianzas coinciden en que bajó las rentas, entre un 5 % y un 6 %. Discrepan en la oferta. Monràs y García-Montalvo (Universitat Pompeu Fabra) encuentran menos viviendas en alquiler y atribuyen la mitad de la bajada de precio a que cambió el tipo de piso que se alquilaba. Jofre-Monseny, Martínez-Mazza y Segú (Universitat de Barcelona) no encuentran menos contratos. Sobre los topes de 2024 todavía hay pocas evaluaciones independientes.",
          "What research says about the 2020 Catalan law, which worked in a similar way: two studies using deposit data agree that it lowered rents, by between 5% and 6%. They disagree on supply. Monràs and García-Montalvo (Universitat Pompeu Fabra) find fewer homes for rent and attribute half of the price fall to a change in the type of flat being rented. Jofre-Monseny, Martínez-Mazza and Segú (Universitat de Barcelona) find no fall in contracts. There are still few independent evaluations of the 2024 caps.",
        ),
        p(
          "En resumen: los datos de estos dos años son coherentes con lo que encontraron los estudios de la ley de 2020. Los topes contienen las rentas de los nuevos contratos, y a la vez hay menos contratos nuevos. Por qué hay menos, y si compensa, es la pregunta que dividirá el debate de la campaña, y los datos públicos todavía no la responden del todo.",
          "In short: the data for these two years is consistent with what the studies of the 2020 law found. The caps hold down rents on new leases, and at the same time there are fewer new leases. Why there are fewer, and whether it is worth it, is the question that will divide the campaign debate, and public data does not yet fully answer it.",
        ),
      ],
    },
    tiempo: {
      lede: {
        es: "La vivienda se ha encarecido mucho más que los sueldos.",
        en: "Housing has become far more expensive than wages have risen.",
      },
      body: [
        p(
          "Entre 2015 y 2025, el precio de la vivienda subió un 80 %, el salario medio por trabajador un 25 % y los precios de consumo un 27 %. Descontada la inflación, comprar una casa cuesta un 42 % más que hace diez años, mientras que el salario medio compra un 1,5 % menos que entonces.",
          "Between 2015 and 2025, house prices rose 80%, the average wage per worker 25% and consumer prices 27%. Adjusted for inflation, buying a home costs 42% more than ten years ago, while the average wage buys 1.5% less than it did then.",
        ),
        { fig: "vit1-precios-salarios", code: "T1" },
        { see: { es: "Nota: salarios reales y salario mínimo desde 2008", en: "Note: real wages and the minimum wage since 2008" }, href: "/notas/salarios-reales-salario-minimo/" },
        p(
          "Mirado desde 2008, el ciclo es completo: tras la burbuja, la vivienda cayó un 35 % hasta 2013 y desde entonces casi ha duplicado su precio. En 2025 estaba un 22 % por encima de su máximo anterior, en euros corrientes.",
          "Seen from 2008, the cycle is complete: after the bubble, house prices fell 35% until 2013 and have almost doubled since. In 2025 they were 22% above their previous peak, in current euros.",
        ),
        p(
          "A finales de septiembre el Gobierno aprobó dos decretos sobre alquiler: limitaban al 2 % la actualización anual de las rentas, permitían prorrogar los contratos y fijaban indemnizaciones si el propietario no los renovaba. El 2 de octubre el Congreso no los convalidó y quedaron derogados. Tres días después se convocaron las elecciones.",
          "At the end of September the government approved two rental decrees: they capped the annual rent update at 2%, allowed leases to be extended and set compensation if the landlord did not renew them. On 2 October Congress did not validate them and they were struck down. Three days later the election was called.",
        ),
        p(
          "Lo que no dicen estos datos. Los precios de los gráficos de España y de las comunidades son de compraventa. Para el alquiler solo usamos las fianzas que se depositan en la Generalitat, así que no se pueden comparar los alquileres de Cataluña con los de otras comunidades con la misma fuente. Las fianzas recogen los contratos de vivienda habitual con fianza depositada: no incluyen los alquileres de temporada ni los contratos sin fianza. La comparación entre municipios catalanes con y sin tope no es un experimento: los municipios con tope son más urbanos y más caros, así que la diferencia no se puede atribuir solo a la norma. Y la sobrecarga de los inquilinos sale de una encuesta europea, con su margen de error.",
          "What this data does not say. The prices in the charts for Spain and the regions are sale prices. For rents we only use the deposits lodged with the Catalan government, so rents in Catalonia cannot be compared with other regions using the same source. The deposits cover long-term residential leases with a lodged deposit: they do not include seasonal lets or contracts without a deposit. The comparison between Catalan municipalities with and without a cap is not an experiment: capped municipalities are more urban and more expensive, so the difference cannot be attributed to the rule alone. And the tenants' cost overburden comes from a European survey, with its margin of error.",
        ),
        { see: { es: "La legislatura en datos: salarios, empleo y cuentas públicas desde 2023", en: "The parliament in data: wages, jobs and public finances since 2023" }, href: "/la-legislatura-en-datos/" },
      ],
    },
  },
  sources: [
    { name: { es: "BOE: derogación del Real Decreto-ley 26/2026 (2 de octubre de 2026)", en: "BOE (official gazette): repeal of Royal Decree-law 26/2026 (2 October 2026)" }, url: "https://www.boe.es/buscar/doc.php?id=BOE-A-2026-20526" },
    { name: { es: "OCU: qué contenían los decretos 26 y 27/2026", en: "OCU (consumer association): what decrees 26 and 27/2026 contained" }, url: "https://www.ocu.org/fincas-y-casas/gestion/alquiler/analisis/2026/10/derogados-los-decretos-de-alquileres" },
    { name: { es: "Ley 12/2023, por el derecho a la vivienda", en: "Law 12/2023 on the right to housing" }, url: "https://www.boe.es/buscar/act.php?id=BOE-A-2023-12203" },
    { name: { es: "La Moncloa: zonas tensionadas en 140 municipios de Cataluña (marzo de 2024)", en: "La Moncloa: stressed areas in 140 Catalan municipalities (March 2024)" }, url: "https://www.lamoncloa.gob.es/serviciosdeprensa/notasprensa/vivienda-agenda-urbana/paginas/2024/150324-indice-precios-alquiler-areas-tensionadas.aspx" },
    { name: { es: "BOE: 131 nuevos municipios tensionados en Cataluña (octubre de 2024)", en: "BOE: 131 new stressed municipalities in Catalonia (October 2024)" }, url: "https://www.boe.es/diario_boe/txt.php?id=BOE-A-2024-20576" },
    { name: { es: "Civio: nuevas zonas tensionadas en Galicia, País Vasco y Asturias (julio de 2026)", en: "Civio: new stressed areas in Galicia, the Basque Country and Asturias (July 2026)" }, url: "https://civio.es/el-boe-nuestro-de-cada-dia/2026/07/29/nuevas-zonas-tensionadas-santiago-de-compostela-basauri-y-cinco-municipios-de-asturias/" },
    { name: "Monràs y García-Montalvo, The effect of second generation rent controls: New evidence from Catalonia (UPF)", url: "https://econ-papers.upf.edu/papers/1836.pdf" },
    { name: "Jofre-Monseny, Martínez-Mazza y Segú, Effectiveness and supply effects of high-coverage rent control policies (UB)", url: "https://diposit.ub.edu/items/5bd0c94a-ecb7-48d1-b0ce-d8406677b4f5" },
  ],
};

export default theme;
