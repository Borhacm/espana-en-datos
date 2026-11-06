import { p, type Theme } from "../../lib/content-types";

// Cifras comprobadas contra data/charts/en*.json (Eurostat e INE, descargados el 6 de noviembre de 2026). Tabla de verificación en editorial/registro/a09.md.
// Objetivos para 2030: Ley 7/2021, de cambio climático y transición energética, artículo 3 (texto consolidado del BOE, última actualización publicada el 30 de junio de 2026).
const theme: Theme = {
  id: "energia",
  code: "EN",
  slug: { es: "energia", en: "energy" },
  title: {
    es: "Energía: precio de la luz, renovables y dependencia",
    en: "Energy: electricity prices, renewables and dependency",
  },
  status: "published",
  published: "2026-11-06",
  order: 10,
  dek: {
    es: "Desde 2023, los hogares españoles pagan la luz más barata que la media de la UE, sobre todo porque la energía cuesta menos: en cinco años, la solar ha pasado de generar el 5,5 % de la electricidad al 20,2 %. Pero el 15,9 % de los españoles vive en hogares que no pueden mantener la casa caliente, frente al 8,8 % en la UE, y España sigue importando más de dos tercios de la energía que utiliza.",
    en: "Since 2023, Spanish households have paid less for electricity than the EU average, mainly because energy costs less: in five years, solar has gone from generating 5.5% of electricity to 20.2%. But 15.9% of Spaniards live in households that cannot keep their home warm, against 8.8% in the EU, and Spain still imports more than two thirds of the energy it uses.",
  },
  lenses: {
    europa: {
      lede: {
        es: "La luz es más barata que en la media europea, pero en España hay más hogares que no pueden calentar su casa que en casi toda la UE.",
        en: "Electricity is cheaper than the European average, but more households in Spain cannot heat their home than in almost any other EU country.",
      },
      body: [
        p(
          "Lo que pagan los hogares por la luz y el gas depende en buena parte de decisiones de las Cortes y del Gobierno que salgan del 29N: el IVA y el impuesto sobre la electricidad, los cargos regulados de la factura, el bono social para los hogares vulnerables y el ritmo de la transición energética, cuyos objetivos para 2030 fija la Ley 7/2021, de cambio climático. Entre el segundo semestre de 2025 y el primero de 2026, los hogares españoles pagaron de media 25,9 céntimos por kWh, impuestos incluidos, frente a 28,6 en la UE. Once países la pagan más cara, con Irlanda (39,6) y Alemania (37,4) a la cabeza; Francia (25,2), Países Bajos (25,0) y Portugal (24,0) están muy cerca de España. Si se tiene en cuenta el nivel de precios de cada país, la diferencia desaparece: en paridad de poder de compra, España (28,9) queda prácticamente en la media de la UE (28,7).",
          "What households pay for electricity and gas depends to a large extent on decisions by the parliament and the government that emerge from the 29 November election: VAT and the electricity tax, the regulated charges on the bill, the bono social (discounted tariff) for vulnerable households and the pace of the energy transition, whose 2030 targets are set by Law 7/2021 on climate change. Between the second half of 2025 and the first half of 2026, Spanish households paid an average of 25.9 cents per kWh, including taxes, against 28.6 in the EU. Eleven countries pay more, led by Ireland (39.6) and Germany (37.4); France (25.2), the Netherlands (25.0) and Portugal (24.0) are very close to Spain. Taking each country's price level into account, the difference disappears: in purchasing power standards, Spain (28.9) is practically at the EU average (28.7).",
        ),
        { fig: "ene1-europa-precio", code: "E1" },
        p(
          "La diferencia no está en los impuestos. En 2025, el IVA supuso 4,4 céntimos por kWh en España y en la UE, y el resto de impuestos y cargos, 3,8 frente a 3,9. De los 2,5 céntimos que separaban el precio español (26,4) del europeo (28,9), 1,4 salían del coste de la energía y su comercialización y 1,0 de las redes de transporte y distribución.",
          "The difference does not lie in taxes. In 2025, VAT accounted for 4.4 cents per kWh in both Spain and the EU, and other taxes and levies for 3.8 against 3.9. Of the 2.5 cents separating the Spanish price (26.4) from the European one (28.9), 1.4 came from the cost of energy and its retail supply and 1.0 from the transmission and distribution networks.",
        ),
        { fig: "ene2-europa-componentes", code: "E2" },
        p(
          "Una luz más barata no ha significado menos hogares con dificultades para calentar su casa. En 2025, el 15,9 % de la población española vivía en hogares que declaraban no poder permitirse mantener la vivienda a una temperatura adecuada, frente al 8,8 % de la UE. Solo Grecia (18,1 %), Lituania (16,7 %) y Bulgaria (16,1 %) tenían un porcentaje más alto, y Portugal (15,6 %) está justo por debajo. En 2019, la diferencia con la UE era pequeña (7,5 % frente a 6,9 %); en España el porcentaje se disparó hasta el 20,8 % en 2023 y desde entonces ha bajado, pero sigue en más del doble que en 2019.",
          "Cheaper electricity has not meant fewer households struggling to heat their home. In 2025, 15.9% of the Spanish population lived in households that said they could not afford to keep their home adequately warm, against 8.8% in the EU. Only Greece (18.1%), Lithuania (16.7%) and Bulgaria (16.1%) had a higher share, and Portugal (15.6%) is just below. In 2019, the gap with the EU was small (7.5% against 6.9%); in Spain the share shot up to 20.8% in 2023 and has fallen since, but it is still more than double the 2019 figure.",
        ),
        { fig: "ene3-europa-frio", code: "E3" },
      ],
    },
    dentro: {
      lede: {
        es: "Donde más hogares dicen no poder calentar su casa no es en las comunidades más frías, sino en el sur.",
        en: "The regions where most households say they cannot heat their home are not the coldest ones, but those in the south.",
      },
      body: [
        p(
          "Entre 2023 y 2025, el 18,2 % de los hogares españoles declaró de media que no podía mantener su vivienda a una temperatura adecuada. Los porcentajes más altos están en Murcia (23,4 %), Extremadura (22,9 %), Andalucía (20,9 %) y Castilla-La Mancha (20,7 %); los más bajos, en Navarra (11,0 %), el País Vasco (11,9 %), Aragón (12,7 %) y Castilla y León (14,0 %), comunidades con inviernos más fríos. La encuesta no permite saber cuánto pesan en estas diferencias la renta de los hogares, el aislamiento de las viviendas o el tipo de calefacción.",
          "Between 2023 and 2025, an average of 18.2% of Spanish households said they could not keep their home adequately warm. The highest shares are in Murcia (23.4%), Extremadura (22.9%), Andalusia (20.9%) and Castile-La Mancha (20.7%); the lowest in Navarre (11.0%), the Basque Country (11.9%), Aragon (12.7%) and Castile and León (14.0%), regions with colder winters. The survey cannot tell how much of these differences is due to household income, home insulation or the type of heating.",
        ),
        { fig: "end1-comunidades-frio", code: "D1" },
        p(
          "Lo que sí muestra la Encuesta de Presupuestos Familiares es que se gasta de forma distinta. En 2025, un hogar medio gastó 1.255 euros en electricidad, gas y otros combustibles para su vivienda, el 3,6 % de todo su gasto. En Castilla-La Mancha la factura energética pesa más que en ninguna otra comunidad (5,0 % del gasto), seguida de Castilla y León (4,6 %); en el otro extremo, sin contar Ceuta y Melilla, está Canarias (2,4 %). En el sur y el Mediterráneo casi todo es electricidad: el 92,6 % del gasto en Canarias, el 85,8 % en Murcia y el 85,5 % en Andalucía. En Castilla y León (48,8 %), La Rioja (49,8 %) y Navarra (53,4 %), cerca de la mitad se va en gas, gasóleo y otros combustibles, que se usan sobre todo para la calefacción, el agua caliente y la cocina.",
          "What the Household Budget Survey does show is that spending patterns differ. In 2025, the average household spent 1,255 euros on electricity, gas and other fuels for its home, 3.6% of all its spending. In Castile-La Mancha the energy bill weighs more than in any other region (5.0% of spending), followed by Castile and León (4.6%); at the other end, leaving aside Ceuta and Melilla, are the Canary Islands (2.4%). In the south and along the Mediterranean almost all of it is electricity: 92.6% of spending in the Canary Islands, 85.8% in Murcia and 85.5% in Andalusia. In Castile and León (48.8%), La Rioja (49.8%) and Navarre (53.4%), around half goes on gas, heating oil and other fuels, used mainly for heating, hot water and cooking.",
        ),
        { fig: "end2-comunidades-gasto", code: "D2" },
      ],
    },
    tiempo: {
      lede: {
        es: "En cinco años, la solar ha pasado de ser una fuente menor a generar una de cada cinco unidades de electricidad, y la luz ha dejado de ser más cara que en Europa.",
        en: "In five years, solar has gone from a minor source to generating one in five units of electricity, and electricity is no longer more expensive than in Europe.",
      },
      body: [
        p(
          "En 2000, el carbón y la nuclear producían más del 60 % de la electricidad española (35,2 % y 27,7 %). En 2024, la eólica (21,6 %) fue la primera fuente, seguida de la solar (20,2 %), la nuclear (18,9 %) y el gas (18,2 %), que ha bajado desde el 30,6 % de 2019. La hidráulica depende de la lluvia: fue el 6,0 % en 2022 y el 12,0 % en 2024. En conjunto, las renovables generaron el 55,9 % de la electricidad en 2024, frente al 37,0 % en 2019. Con el método de cálculo de los objetivos europeos, el peso de las renovables en el consumo de electricidad fue en 2025 del 60,7 % en España y del 49,9 % en la UE.",
          "In 2000, coal and nuclear produced more than 60% of Spain's electricity (35.2% and 27.7%). In 2024, wind (21.6%) was the leading source, followed by solar (20.2%), nuclear (18.9%) and gas (18.2%), which has fallen from 30.6% in 2019. Hydro depends on rainfall: it was 6.0% in 2022 and 12.0% in 2024. Taken together, renewables generated 55.9% of electricity in 2024, against 37.0% in 2019. Using the calculation method for the European targets, renewables accounted for 60.7% of electricity consumption in 2025 in Spain and 49.9% in the EU.",
        ),
        { fig: "ent1-generacion", code: "T1" },

        { h: { es: "La ficha: los objetivos de la ley de cambio climático", en: "Policy file: the targets of the climate change law" }, id: "ficha-ley-clima" },
        { steps: [
          {
            title: { es: "Qué es.", en: "What it is." },
            text: {
              es: "La Ley 7/2021, de cambio climático y transición energética, fija en su artículo 3 objetivos mínimos para 2030. Entre ellos, que las renovables cubran al menos el 42 % del consumo de energía final y que al menos el 74 % de la electricidad se genere con renovables. Antes de 2050, el sistema eléctrico deberá ser solo renovable.",
              en: "Law 7/2021 on climate change and the energy transition sets minimum targets for 2030 in its article 3. Among them, renewables must cover at least 42% of final energy consumption and at least 74% of electricity must be generated from renewable sources. Before 2050, the electricity system must be exclusively renewable.",
            },
          },
          {
            title: { es: "Quién y cuándo.", en: "Who and when." },
            text: {
              es: "La aprobaron las Cortes en mayo de 2021. El Plan Nacional Integrado de Energía y Clima es el instrumento que la desarrolla, y la ley permite al Consejo de Ministros revisar los objetivos, pero solo al alza.",
              en: "Parliament passed it in May 2021. The National Integrated Energy and Climate Plan is the instrument that implements it, and the law allows the Council of Ministers to revise the targets, but only upwards.",
            },
          },
          {
            title: { es: "Qué debería pasar.", en: "What should happen." },
            text: {
              es: "Que el peso de las renovables siga subiendo hasta alcanzar esos niveles en 2030, en la electricidad y también en el resto de usos de la energía: el transporte, la calefacción y la industria.",
              en: "The share of renewables should keep rising to reach those levels by 2030, in electricity and also in other uses of energy: transport, heating and industry.",
            },
          },
          {
            title: { es: "Con qué lo comparamos.", en: "What we compare it with." },
            text: {
              es: "Con el ritmo al que ha crecido el peso de las renovables según Eurostat desde 2019, antes de la pandemia y de la ley, y con el que haría falta para llegar a los objetivos.",
              en: "With the pace at which the share of renewables has grown according to Eurostat since 2019, before the pandemic and the law, and with the pace needed to reach the targets.",
            },
          },
        ] },
        p(
          "En la electricidad, el objetivo está al alcance si se mantiene el ritmo: las renovables pasaron del 37,0 % al 55,9 % de la producción entre 2019 y 2024, unos 3,8 puntos al año, y para llegar al 74 % en 2030 bastarían algo más de 3 puntos al año. En el conjunto de la energía, no: las renovables cubrían en 2025 el 26,0 % del consumo final (la media de la UE es el 26,2 %), frente al 17,9 % en 2019. Han subido unos 1,4 puntos al año y harían falta 3,2 para llegar al 42 % en 2030. Donde menos han avanzado es en el transporte y en la calefacción: en 2024, las renovables cubrían el 11,3 % de la energía del transporte y el 21,6 % de la de calefacción y refrigeración. Las cifras son de Eurostat; la ley no detalla en ese artículo con qué indicador se mide cada objetivo, así que la comparación es orientativa.",
          "In electricity, the target is within reach if the pace is maintained: renewables went from 37.0% to 55.9% of production between 2019 and 2024, around 3.8 points a year, and reaching 74% by 2030 would require just over 3 points a year. For energy as a whole, it is not: in 2025 renewables covered 26.0% of final consumption (the EU average is 26.2%), against 17.9% in 2019. They have risen by around 1.4 points a year and 3.2 would be needed to reach 42% by 2030. Progress has been slowest in transport and heating: in 2024, renewables covered 11.3% of the energy used in transport and 21.6% of that used for heating and cooling. The figures are from Eurostat; that article of the law does not specify which indicator is used to measure each target, so the comparison is indicative.",
        ),
        p(
          "El precio de la luz no siempre ha sido más bajo que en Europa. Desde la segunda mitad de 2009 hasta 2022, los hogares españoles la pagaron más cara que la media de la UE. En la crisis energética de 2022, la distancia llegó a su máximo: 33,5 céntimos por kWh en España en el segundo semestre, frente a 27,7 en la UE. Desde 2023, la relación se ha invertido: en el primer semestre de 2026, 25,1 céntimos frente a 28,3.",
          "Electricity has not always been cheaper than in Europe. From the second half of 2009 until 2022, Spanish households paid more than the EU average. In the 2022 energy crisis, the gap reached its widest: 33.5 cents per kWh in Spain in the second half of the year, against 27.7 in the EU. Since 2023, the relationship has been reversed: in the first half of 2026, 25.1 cents against 28.3.",
        ),
        { fig: "ent2-precio", code: "T2" },
        p(
          "España sigue dependiendo del exterior más que la media europea. En 2024 importó en neto el 68,9 % de la energía que utiliza, frente al 57,3 % del conjunto de la UE. Es mucho menos que en 2008 (81,6 %), pero casi todo el gas (97,4 %) y todo el petróleo se compran fuera, porque España apenas los produce. La energía nuclear cuenta como producción propia por convenio estadístico, aunque el uranio se importe.",
          "Spain still depends on imports more than the European average. In 2024 its net imports covered 68.9% of the energy it uses, against 57.3% for the EU as a whole. That is much less than in 2008 (81.6%), but almost all the gas (97.4%) and all the oil are bought abroad, because Spain produces hardly any. Nuclear energy counts as domestic production by statistical convention, even though the uranium is imported.",
        ),
        { fig: "ent3-dependencia", code: "T3" },
        p(
          "Lo que no dicen estos datos. El precio medio de Eurostat es el de un hogar tipo y no refleja cuánto paga cada familia, que depende de su tarifa, de su consumo y de si recibe el bono social. Las partidas del precio no coinciden exactamente con las de la factura española. Decir que no se puede mantener la casa caliente es una respuesta a una encuesta: no mide la temperatura de las viviendas ni separa el efecto de la renta, del aislamiento o del clima, y en cada comunidad la muestra es pequeña. Que las renovables hayan crecido coincide con que la luz se haya abaratado respecto a la UE, pero estos datos no permiten atribuir cuánto se debe a ellas y cuánto al precio del gas, a los impuestos o a otras causas, ni a ningún gobierno.",
          "What this data does not say. Eurostat's average price is that of a typical household and does not reflect what each family pays, which depends on its tariff, its consumption and whether it receives the bono social. The price components do not exactly match those of the Spanish bill. Saying that one cannot keep the home warm is a survey answer: it does not measure the temperature of homes or separate the effect of income, insulation or climate, and each region's sample is small. The growth of renewables coincides with electricity becoming cheaper than in the EU, but this data does not allow us to attribute how much of that is due to them and how much to the price of gas, taxes or other causes, nor to any government.",
        ),
        { see: { es: "Vivienda: por qué es el tema de estas elecciones", en: "Housing: why it is the issue of this election" }, href: "/vivienda/" },
        { see: { es: "Impuestos y gasto público: España frente a Europa", en: "Taxes and public spending: Spain and Europe" }, href: "/impuestos/" },
      ],
    },
  },
  sources: [
    { name: "Ley 7/2021, de 20 de mayo, de cambio climático y transición energética (artículo 3)", url: "https://www.boe.es/buscar/act.php?id=BOE-A-2021-8447" },
    { name: { es: "Eurostat, cuota de energías renovables (nrg_ind_ren): consumo final de energía y electricidad", en: "Eurostat, share of energy from renewable sources (nrg_ind_ren): final energy consumption and electricity" }, url: "https://ec.europa.eu/eurostat/databrowser/view/nrg_ind_ren/default/table" },
  ],
};

export default theme;
