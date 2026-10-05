import { p, type Theme } from "../../lib/content-types";

// Cifras comprobadas contra data/charts/vi*.json (INE, Eurostat y Generalitat, descargados el 6 de octubre de 2026).
// Estudios citados: Monràs y García-Montalvo (UPF, documento de trabajo 1836, versión de abril de 2022) y
// Jofre-Monseny, Martínez-Mazza y Segú (UB, 2022; publicado en Regional Science and Urban Economics, 2023).
const theme: Theme = {
  id: "vivienda",
  code: "VI",
  slug: { es: "vivienda" },
  title: { es: "Vivienda: por qué es el tema de estas elecciones" },
  status: "published",
  published: "2026-10-06",
  order: 1,
  dek: {
    es: "Las elecciones del 29N se convocaron después de que el Congreso rechazara dos decretos de alquiler. Los datos explican por qué la vivienda está en el centro: desde 2015 ha subido un 80 %, y los salarios, un 25 %.",
  },
  lenses: {
    europa: {
      lede: { es: "España no es donde más ha subido la vivienda, pero sí uno de los países donde el alquiler más pesa." },
      body: [
        p("Desde 2015, la vivienda ha subido un 81 % en España, por encima de la media de la UE (62 %), de Alemania (53 %), Francia (27 %) e Italia (16 %). Otros países han ido mucho más lejos: en Portugal ha subido un 164 % y en Hungría se ha multiplicado por más de tres y media."),
        { fig: "vie1-europa-precios", code: "E1" },
        p("Donde España destaca es en lo que cuesta vivir de alquiler. El 27 % de los inquilinos que pagan precio de mercado dedica más del 40 % de su renta a la vivienda, frente al 19 % de la media europea. Es el octavo porcentaje más alto de la UE."),
        { fig: "vie2-europa-sobrecarga", code: "E2" },
      ],
    },
    dentro: {
      lede: { es: "En Madrid la vivienda ha doblado su precio desde 2015; en Extremadura ha subido un 40 %. Y Cataluña lleva dos años probando los topes al alquiler." },
      body: [
        p("La subida no ha sido igual en todas partes. En Madrid el precio prácticamente se ha duplicado desde 2015 y en Baleares ha subido un 95 %. En el otro extremo están Castilla-La Mancha (43 %) y Extremadura (40 %)."),
        { fig: "vid1-comunidades", code: "D1" },

        { h: { es: "La ficha: topes al alquiler en Cataluña" }, id: "ficha-topes" },
        { steps: [
          { title: { es: "Qué es." }, text: { es: "Un límite a la renta de los nuevos contratos de alquiler de vivienda habitual en las zonas declaradas «de mercado residencial tensionado», según el índice de referencia del Ministerio de Vivienda. Lo permite la Ley 12/2023, por el derecho a la vivienda." } },
          { title: { es: "Quién y cuándo." }, text: { es: "La declaración la pide cada comunidad. Cataluña es la que más tiempo lleva aplicándolo y la que cubre más municipios: 140 desde el 16 de marzo de 2024 y 131 más desde el 10 de octubre de 2024. El País Vasco, Navarra, Galicia y Asturias lo han empezado a aplicar después en algunos municipios. Antes, una ley catalana de 2020 limitó las rentas hasta que el Tribunal Constitucional la anuló en marzo de 2022." } },
          { title: { es: "Qué debería pasar." }, text: { es: "Que las rentas de los nuevos contratos suban menos. El riesgo que señalan sus críticos es que haya menos pisos en alquiler habitual." } },
          { title: { es: "Con qué lo comparamos." }, text: { es: "Con los municipios catalanes sin tope, usando la misma fuente: las fianzas de alquiler que se depositan en la Generalitat." } },
        ] },
        p("Antes de 2024, las rentas de los nuevos contratos subían al mismo ritmo en los municipios que luego tendrían tope y en los demás. Desde que se aplica, se han separado: en el último año, la renta media en los municipios con tope desde marzo de 2024 estaba un 4 % por encima de 2023, y en los municipios sin tope, un 12 %."),
        { fig: "vid2-cataluna-rentas", code: "D2" },
        p("Al mismo tiempo, se firman menos contratos: un 20 % menos que en 2023 en los municipios con tope, frente a un 2 % menos en los que no lo tienen. Puede significar que hay menos pisos en alquiler habitual (porque pasan al alquiler de temporada o se venden), pero también que los inquilinos se mudan menos para no perder su renta. Estos datos no permiten distinguirlo."),
        { fig: "vid3-cataluna-contratos", code: "D3" },
        p("Lo que dice la investigación sobre la ley catalana de 2020, que funcionaba de forma parecida: dos estudios con datos de fianzas coinciden en que bajó las rentas, entre un 5 % y un 6 %. Discrepan en la oferta. Monràs y García-Montalvo (Universitat Pompeu Fabra) encuentran menos viviendas en alquiler y atribuyen la mitad de la bajada de precio a que cambió el tipo de piso que se alquilaba. Jofre-Monseny, Martínez-Mazza y Segú (Universitat de Barcelona) no encuentran menos contratos. Sobre los topes de 2024 todavía hay pocas evaluaciones independientes."),
        p("En resumen: los datos de estos dos años son coherentes con lo que encontraron los estudios de la ley de 2020. Los topes contienen las rentas de los nuevos contratos, y a la vez hay menos contratos nuevos. Por qué hay menos, y si compensa, es la pregunta que dividirá el debate de la campaña, y los datos públicos todavía no la responden del todo."),
      ],
    },
    tiempo: {
      lede: { es: "La vivienda se ha encarecido mucho más que los sueldos." },
      body: [
        p("Entre 2015 y 2025, el precio de la vivienda subió un 80 %, el salario medio por trabajador un 25 % y los precios de consumo un 27 %. Descontada la inflación, comprar una casa cuesta un 42 % más que hace diez años, mientras que el salario medio compra algo menos que entonces."),
        { fig: "vit1-precios-salarios", code: "T1" },
        p("Mirado desde 2008, el ciclo es completo: tras la burbuja, la vivienda cayó un 35 % hasta 2013 y desde entonces casi ha duplicado su precio. En 2025 estaba un 22 % por encima de su máximo anterior, en euros corrientes."),
        p("A finales de septiembre el Gobierno aprobó dos decretos sobre alquiler: limitaban al 2 % la actualización anual de las rentas, permitían prorrogar los contratos y fijaban indemnizaciones si el propietario no los renovaba. El 2 de octubre el Congreso no los convalidó y quedaron derogados. Tres días después se convocaron las elecciones."),
      ],
    },
  },
  sources: [
    { name: "BOE: derogación del Real Decreto-ley 26/2026 (2 de octubre de 2026)", url: "https://www.boe.es/buscar/doc.php?id=BOE-A-2026-20526" },
    { name: "OCU: qué contenían los decretos 26 y 27/2026", url: "https://www.ocu.org/fincas-y-casas/gestion/alquiler/analisis/2026/10/derogados-los-decretos-de-alquileres" },
    { name: "Ley 12/2023, por el derecho a la vivienda", url: "https://www.boe.es/buscar/act.php?id=BOE-A-2023-12203" },
    { name: "La Moncloa: zonas tensionadas en 140 municipios de Cataluña (marzo de 2024)", url: "https://www.lamoncloa.gob.es/serviciosdeprensa/notasprensa/vivienda-agenda-urbana/paginas/2024/150324-indice-precios-alquiler-areas-tensionadas.aspx" },
    { name: "BOE: 131 nuevos municipios tensionados en Cataluña (octubre de 2024)", url: "https://www.boe.es/diario_boe/txt.php?id=BOE-A-2024-20576" },
    { name: "Civio: nuevas zonas tensionadas en Galicia, País Vasco y Asturias (julio de 2026)", url: "https://civio.es/el-boe-nuestro-de-cada-dia/2026/07/29/nuevas-zonas-tensionadas-santiago-de-compostela-basauri-y-cinco-municipios-de-asturias/" },
    { name: "Monràs y García-Montalvo, The effect of second generation rent controls: New evidence from Catalonia (UPF)", url: "https://econ-papers.upf.edu/papers/1836.pdf" },
    { name: "Jofre-Monseny, Martínez-Mazza y Segú, Effectiveness and supply effects of high-coverage rent control policies (UB)", url: "https://diposit.ub.edu/items/5bd0c94a-ecb7-48d1-b0ce-d8406677b4f5" },
  ],
};

export default theme;
