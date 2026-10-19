import { p, type Theme } from "../../lib/content-types";

// Cifras comprobadas contra data/charts/de*.json (INE, Eurostat), el Real Decreto-ley 2/2023 (BOE), el Estudio 1/2026 de la
// AIReF y el Apunte 2025/18 de Fedea. Tabla de verificación y guion: editorial/registro/a03.md.
const theme: Theme = {
  id: "demografia",
  code: "DE",
  slug: { es: "demografia" },
  title: { es: "Demografía y pensiones: un país que envejece" },
  status: "published",
  published: "2026-10-14",
  updated: "2026-10-19",
  order: 4,
  dek: {
    es: "España gasta en pensiones el 13,2 % del PIB y su pensión mediana equivale al 81 % del salario mediano de quienes están a punto de jubilarse, la segunda proporción más alta de la UE. El gasto real ha subido un 53,5 % desde 2008, y por cada mayor de 64 hay menos personas trabajando que entonces. Cómo pagar las pensiones es una de las preguntas del 29N.",
  },
  lenses: {
    europa: {
      lede: { es: "España gasta en pensiones algo más que la media europea, sus pensiones sustituyen una parte mayor del salario y se cobran durante más años." },
      body: [
        p("Las pensiones son una de las preguntas que los partidos tendrán que responder antes del 29N. Para entender el debate hay tres datos de partida: cuánto se gasta, qué parte del sueldo sustituye la pensión y durante cuántos años se cobra."),
        p("España dedicó a pensiones el 13,2 % del PIB en 2024, frente al 12,6 % de la media de la UE: el séptimo porcentaje más alto de los 27. En 2008 era el 9,2 %, por debajo de la media europea (11,8 %). La subida, de 4,0 puntos, es la segunda mayor de la UE después de la de Finlandia (4,2). La definición europea incluye las pensiones de jubilación, viudedad, orfandad e incapacidad, también las de los funcionarios."),
        { fig: "dee2-europa-pensiones", code: "E1" },
        p("Una razón de ese gasto es la cuantía. La pensión mediana de las personas de 65 a 74 años equivale al 81 % de la renta del trabajo mediana de las de 50 a 59, en bruto. En la UE, al 60 %. Solo Luxemburgo tiene una proporción más alta (88 %); Italia está justo detrás de España (80 %). Es una foto de dos grupos distintos en el mismo año, no la pensión que cobrará cada trabajador sobre su último sueldo, pero indica que en España la jubilación reduce menos los ingresos que en casi toda Europa."),
        { fig: "dee3-europa-sustitucion", code: "E2" },
        p("La otra razón es la duración. A los 65 años, a una persona que vive en España le quedan de media 21,9 años de vida, igual que en Francia y más que en ningún otro país de la UE, cuya media es de 20,2. En 1975 eran 15,2 años: una persona que se jubila a esa edad cobra hoy su pensión, de media, 6,7 años más que entonces."),
        { fig: "dee4-europa-vida65", code: "E3" },
      ],
    },
    dentro: {
      lede: { es: "El envejecimiento es muy desigual entre comunidades, pero en todas hay hoy menos personas trabajando por cada mayor de 64 que en 2008." },
      body: [
        p("El 1 de enero de 2025 había en España 31,7 personas de 65 años o más por cada 100 de 16 a 64 años. La cifra va de 46,5 en Asturias, 44,7 en Castilla y León y 43,7 en Galicia a 24,5 en Baleares, 25,7 en Murcia y 26,1 en Canarias. En 1975, Asturias tenía 17,2, menos que Baleares (19,5): desde entonces ha sumado 29,3 puntos, la mayor subida de las 17 comunidades, y Baleares, 5,0, la menor. En esa diferencia influyen la fecundidad, la esperanza de vida y las migraciones, tanto la salida de jóvenes como la llegada de nuevos residentes."),
        { fig: "ded1-dependencia-comunidades", code: "D1" },
        p("Esa tasa es demográfica: compara edades, no quién trabaja. Si se cuenta a los ocupados de todas las edades por cada persona de 65 años o más, España tenía 2,19 en el último año, frente a 2,79 en 2008. La cifra ha bajado en las 17 comunidades. Desde 2008 los ocupados han crecido un 9,8 % y los mayores de 64, un 39,6 %."),
        p("Las diferencias territoriales se mantienen: en Baleares hay 2,98 ocupados por cada mayor de 64 y en Asturias, 1,50. Las pensiones las paga el sistema común de la Seguridad Social, así que estas diferencias no se traducen en pensiones distintas por comunidad, pero sí dibujan dónde pesa más el envejecimiento en los servicios que gestionan las comunidades, como la sanidad y los cuidados."),
        { fig: "ded3-ocupados-mayores", code: "D2" },
      ],
    },
    tiempo: {
      lede: { es: "Nacen menos niños que nunca, el gasto en pensiones crece por más pensionistas y por pensiones más altas, y lo que pase con la dependencia dependerá sobre todo de las migraciones." },
      body: [
        p("En 1975 nacían en España 2,77 hijos por mujer. En 1981 el indicador bajó por primera vez de 2,1 (2,04), el nivel con el que una población se mantiene sin migraciones, y siguió cayendo hasta 1,13 en 1998. Se recuperó hasta 1,44 en 2008 y desde entonces ha vuelto a bajar: 1,10 en 2024, el dato más bajo de la serie. En la UE solo Malta tiene menos hijos por mujer, y ningún país llega a 2,1."),
        { fig: "det1-fecundidad", code: "T1" },
        p("¿Por qué sube el gasto? Entre 2008 y 2024, el gasto en pensiones descontada la inflación creció un 53,5 %. Hay dos motivos que se suman: el número de pensionistas aumentó un 21,4 %, hasta 10,4 millones, y el gasto real por pensionista, un 26,4 %. Aproximadamente, el 45 % de la subida se debe a que hay más pensionistas y el 55 %, a que cobran más."),
        p("La pensión media no sube solo porque se revaloricen las pensiones existentes. Los nuevos jubilados tuvieron, de media, sueldos más altos y carreras de cotización más largas que las personas cuyas pensiones dejan de pagarse. Por eso la pensión media puede crecer más que la inflación aunque cada pensión solo se actualice con ella."),
        { fig: "det4-gasto-descomposicion", code: "T2" },
        p("¿Qué viene? Según las proyecciones del INE, la tasa de dependencia pasará de 31,7 en 2025 a 51,8 en 2050. Llegaría a 52,2 en 2054, bajaría un poco y volvería a subir hasta 53,1 en 2075."),
        p("El escenario central del INE supone que siguen llegando inmigrantes al ritmo de los últimos años. Si entraran tantas personas como salen, la tasa llegaría a 69,9 en 2050 y a 90,4 en 2075. La diferencia entre esos dos escenarios es mucho mayor que la que hay entre los de fecundidad alta y baja del propio INE: de los supuestos que prueba el INE, el saldo migratorio es el que más mueve la proyección."),
        { fig: "det5-dependencia-proyeccion", code: "T3" },
        { see: { es: "Inmigración en datos: quién llega, dónde trabaja y cuánto pesa en la población" }, href: "/inmigracion/" },

        { h: { es: "La ficha: la reforma de las pensiones de 2021 y 2023" }, id: "ficha-pensiones" },
        { steps: [
          { title: { es: "Qué es." }, text: { es: "Dos normas. La Ley 21/2021 vuelve a actualizar cada año las pensiones con la inflación media. El Real Decreto-ley 2/2023 sube los ingresos del sistema: una cotización finalista, el Mecanismo de Equidad Intergeneracional (MEI), que empieza en 0,6 puntos en 2023 y sube una décima al año hasta 1,2 en 2029; un aumento de la base máxima de cotización de 1,2 puntos al año por encima de la inflación entre 2024 y 2050; una cotización adicional de solidaridad sobre los salarios que superan esa base, desde 2025, y la posibilidad de calcular la pensión con los 29 últimos años descartando los 24 peores meses." } },
          { title: { es: "Quién y cuándo." }, text: { es: "La Ley 21/2021 la aprobaron las Cortes en diciembre de 2021. El Real Decreto-ley 2/2023 lo aprobó el Consejo de Ministros en marzo de 2023 y lo convalidó el Congreso." } },
          { title: { es: "Qué debería pasar." }, text: { es: "Que las pensiones mantengan su poder de compra y que los nuevos ingresos cubran una parte del aumento del gasto. La norma incluye una cláusula de cierre: cada tres años, la AIReF comprueba si el gasto medio en pensiones entre 2022 y 2050, descontados los nuevos ingresos, supera el 13,3 % del PIB. Si lo supera, el Gobierno debe proponer medidas o, en su defecto, subir el MEI." } },
          { title: { es: "Con qué lo comparamos." }, text: { es: "Con las proyecciones de gasto de la AIReF y de la Comisión Europea, y con el resto de las cuentas públicas." } },
        ] },
        p("Lo que dicen las evaluaciones independientes. La AIReF (Estudio 1/2026, de mayo de 2026) concluye que la regla se cumple: el gasto neto de las nuevas medidas de ingresos será del 13,0 % del PIB de media entre 2022 y 2050, por debajo del 13,3 %. Esas medidas aportarían un 1,6 % del PIB al año de media, un 0,4 % el MEI. Pero la misma AIReF advierte de que la regla no es un buen indicador de sostenibilidad: prevé que el gasto bruto en pensiones pase del 13 % al 16,4 % del PIB entre 2025 y 2050, que las transferencias del Estado y de otros fondos de la Seguridad Social para pagarlas tengan que subir 2,3 puntos del PIB, hasta el 3,0 %, y que, si no cambian las políticas, la deuda pública llegue al 123 % del PIB en 2050."),
        p("Ángel de la Fuente (Fedea, abril de 2025) comparte esas dudas y discute cómo se aplicó la regla en su primera evaluación: critica que cuenten como ingresos del sistema transferencias del Estado y que se corrigieran al alza las previsiones de PIB, y recuerda que una décima arriba o abajo habría cambiado el resultado. La evidencia, por tanto, no es concluyente: la regla se cumple, pero no hay acuerdo en que eso garantice que el sistema sea sostenible sin nuevas medidas."),
        p("Lo que no dicen estos datos. El gasto en pensiones se mide de formas distintas: el de Eurostat incluye a los funcionarios y es más amplio que el de la Seguridad Social, y el de la AIReF tampoco coincide con ninguno de los dos, así que las cifras no se pueden sumar ni restar entre sí. Los ocupados de la EPA no son lo mismo que los afiliados que cotizan, ni todos los mayores de 64 cobran una pensión. La tasa de sustitución compara a dos grupos de personas distintos y no dice si las pensiones son suficientes, ni recoge la pobreza entre los mayores. Las proyecciones muestran qué pasaría si se cumplen sus supuestos, no lo que va a pasar. Y ninguno de estos datos permite atribuir a un Gobierno concreto la evolución del gasto, que depende sobre todo de la demografía y de reglas aprobadas a lo largo de décadas."),
      ],
    },
  },
  sources: [
    { name: "BOE: Ley 21/2021, de garantía del poder adquisitivo de las pensiones", url: "https://www.boe.es/buscar/act.php?id=BOE-A-2021-21652" },
    { name: "BOE: Real Decreto-ley 2/2023, de ampliación de derechos de los pensionistas y nuevo marco de sostenibilidad del sistema público de pensiones", url: "https://www.boe.es/buscar/act.php?id=BOE-A-2023-6967" },
    { name: "AIReF: Estudio de evaluación de la regla de gasto de pensiones (Estudio 1/2026, 29 de mayo de 2026)", url: "https://www.airef.es/wp-content/uploads/2026/05/Pensiones/Estudio_Regla_Gasto_Pensiones-2026.pdf" },
    { name: "AIReF: la AIReF constata el cumplimiento de la regla de gasto de pensiones, pero alerta de que la sostenibilidad no ha mejorado (nota de prensa, 31 de marzo de 2025)", url: "https://www.airef.es/wp-content/uploads/2025/03/Informe_regla_de_gasto_de_pensiones/Nota-de-prensa.pdf" },
    { name: "Ángel de la Fuente, Sobre la aplicación de la cláusula de salvaguarda del MEI: algunas dudas metodológicas (Fedea, Apuntes 2025/18)", url: "https://documentos.fedea.net/pubs/ap/2025/ap2025-18.pdf" },
    { name: "INE: Proyecciones de Población 2026-2075", url: "https://www.ine.es/jaxiT3/Tabla.htm?t=36652" },
  ],
};

export default theme;
