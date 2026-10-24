"""Tema Sanidad (código SA): gasto frente a Europa, listas de espera y gasto por comunidad, y en qué se gasta."""

from lib import geo, sources
from lib.output import THEMES, chart

from .common import bi, dec, es_num, ordinal_en

THEMES["sanidad"] = {"code": "SA", "title": "Sanidad"}

EUROSTAT = {"name": "Eurostat", "license": "CC BY 4.0"}

SISLE = {
    "name": "Ministerio de Sanidad, Sistema de Información sobre Listas de Espera del SNS (SISLE-SNS)",
    "dataset": "Indicadores resumen, situación a 31 de diciembre de cada año",
    "url": "https://www.sanidad.gob.es/estadEstudios/estadisticas/inforRecopilaciones/listaEspera.htm",
    "license": "Reutilización libre citando la fuente",
}
EGSP = {
    "name": "Ministerio de Sanidad, Estadística de Gasto Sanitario Público",
    "dataset": "Serie 2002-2024, gasto real (devengo)",
    "url": "https://www.sanidad.gob.es/estadEstudios/estadisticas/inforRecopilaciones/gastoSanitario2005/home.htm",
    "license": "Reutilización libre citando la fuente",
}

# ---------- Transcripciones ----------
# Los informes del SISLE-SNS solo se publican en PDF. Lista de espera quirúrgica a 31 de diciembre, por comunidad:
# tiempo medio de espera de los pacientes pendientes (días) y porcentaje con más de seis meses de espera.
# Informe de diciembre de 2025, versión rectificada (corrige Castilla-La Mancha), página 8.
WAIT_YEAR = 2025
WAIT_CCAA = {
    "01": (173, 32.2), "02": (132, 21.7), "03": (91, 10.4), "04": (105, 22.4), "05": (106, 17.4), "06": (137, 26.2),
    "07": (87, 13.8), "08": (117, 16.5), "09": (142, 32.0), "10": (88, 16.1), "11": (135, 23.1), "12": (73, 5.7),
    "13": (50, 0.8), "14": (103, 19.3), "15": (96, 16.7), "16": (64, 2.3), "17": (78, 6.4), "18": (94, 15.1),
    "19": (82, 8.2), "ES": (122, 21.6),
}
# Pacientes en lista de espera quirúrgica por 1.000 habitantes con tarjeta sanitaria, a 31 de diciembre de cada año,
# tomados del informe de cada corte. La serie empieza en 2018: ese año cambió el sistema de cómputo de Andalucía.
WAIT_RATE = {2018: 14.78, 2019: 15.53, 2020: 14.20, 2021: 15.39, 2022: 17.10, 2023: 18.11, 2024: 17.80, 2025: 17.70}

# Estadística de Gasto Sanitario Público: el Ministerio la publica en una hoja .xls (formato antiguo de Excel).
# Anexo I.2: gasto sanitario público consolidado del sector comunidades autónomas, euros por habitante. 2024, provisional.
SPEND_YEAR = 2024
SPEND_CCAA = {
    "01": 1657.8, "02": 2190.2, "03": 2322.4, "04": 1955.9, "05": 2035.5, "06": 2241.7, "07": 2218.1, "08": 1957.1,
    "09": 2060.6, "10": 1866.5, "11": 2245.9, "12": 2070.6, "13": 1778.6, "14": 2154.8, "15": 2155.7, "16": 2332.1,
    "17": 1878.4, "ES": 1957.6,
}
# Tabla 1.2: gasto sanitario público total consolidado por clasificación funcional, miles de euros (2023 y 2024, provisionales)
YEARS = list(range(2002, 2025))
FUNCTIONS = {
    "hospital": [20272339, 22612609, 24613492, 27198381, 30133824, 32711352, 37116566, 39347798, 39097748, 39896325, 38834712,
                 37498783, 38098775, 41187780, 41655003, 42624249, 44023409, 46710243, 52035263, 54268385, 55875223, 59582104,
                 63136414],
    "primaria": [5811071, 6455766, 7028223, 7630041, 8312731, 9261291, 10288049, 10661619, 10498960, 10040133, 9340532, 9027539,
                 8945922, 9256362, 9401799, 9613886, 10267866, 10921453, 11870349, 12659790, 13093253, 13855610, 14627147],
    "farmacia": [8484537, 9611402, 10152795, 10757585, 11303047, 11883760, 12684523, 13434241, 13370109, 12269035, 10825083,
                 10456329, 10388543, 10483275, 10899061, 11277270, 11566127, 11855177, 12184498, 12855427, 13552779, 13984427,
                 14684284],
    "salud_publica": [574272, 496317, 578586, 646896, 752736, 849403, 789200, 1168659, 776075, 760270, 713440, 690462, 677996,
                      687868, 767323, 778385, 790724, 831412, 1798221, 2570404, 3034286, 1712314, 1357042],
    "colectivos": [1078101, 1221990, 1185191, 1346738, 1534896, 1723569, 1791623, 2053872, 1935213, 2000542, 1987151, 1990210,
                   1742248, 1885880, 1807927, 1841795, 1858027, 1976161, 2068756, 2200502, 2437864, 2632530, 2895124],
    "traslados": [634458, 696970, 771988, 851768, 1028940, 1141155, 1294953, 1355647, 1411811, 1396472, 1253160, 1138145,
                  1238410, 1216171, 1221877, 1243416, 1255785, 1320004, 1300939, 1415640, 1542307, 1700846, 1840725],
    "capital": [1655708, 1781201, 1887690, 2227469, 2672323, 2788950, 2968597, 2704496, 2410189, 1670810, 1159703, 924713,
                880752, 1046537, 963666, 1150662, 1355267, 1373414, 2376420, 1965316, 2422627, 4163688, 3198180],
}
FUNCTIONS_TOTAL = [38510485, 42876255, 46217965, 50658878, 55738498, 60359481, 66933512, 70726332, 69500103, 68033586, 64113780,
                   61726181, 61972647, 65763873, 66716656, 68529663, 71117205, 74987862, 83634447, 87935463, 91958339, 97631519,
                   101738916]


def _eu_rows(raw: list[dict]) -> tuple[list[dict], str]:
    """Último año con dato de la UE: una fila por país de la UE y otra para la media."""
    year = sorted({r["time"] for r in raw if geo.from_eurostat(r["geo"]) == "EU27"})[-1]
    out = []
    for r in raw:
        c = geo.from_eurostat(r["geo"])
        if r["time"] == year and c and (c == "EU27" or geo.COUNTRIES.get(c, (0, 0, 0, False))[3]):
            out.append({"geo": c, "time": year, "value": round(r["value"], 1)})
    return sorted(out, key=lambda r: r["geo"]), year


def _rank(rows: list[dict], code: str) -> int:
    ranked = sorted((r for r in rows if r["geo"] != "EU27"), key=lambda r: -r["value"])
    return [r["geo"] for r in ranked].index(code) + 1


# ---------- España frente a Europa ----------

def europa_gasto():
    raw = sources.eurostat("gov_10a_exp", unit="PC_GDP", sector="S13", cofog99="GF07", na_item="TE")
    rows, year = _eu_rows(raw)
    es = next(r["value"] for r in rows if r["geo"] == "ESP")
    eu = next(r["value"] for r in rows if r["geo"] == "EU27")
    n = len(rows) - 1
    rank = _rank(rows, "ESP")
    return chart(
        id="sae1-europa-gasto",
        lens="europa", theme="sanidad",
        title=bi(f"España dedica a la sanidad pública el {dec(es, 'es')} % de su PIB; la UE, el {dec(eu, 'es')} %",
                 f"Spain spends {dec(es, 'en')}% of its GDP on public health care; the EU, {dec(eu, 'en')}%"),
        subtitle=bi(f"Gasto público en sanidad, {year}, en % del PIB. España es el {rank}.º de {n} países",
                    f"Public spending on health, {year}, as % of GDP. Spain ranks {ordinal_en(rank)} of {n} countries"),
        unit=bi("% del PIB", "% of GDP"),
        source={**EUROSTAT, "dataset": "gov_10a_exp",
                "url": "https://ec.europa.eu/eurostat/databrowser/view/gov_10a_exp/default/table"},
        notes={"es": ["Gasto de todas las administraciones públicas en la función «Sanidad» de la clasificación COFOG: hospitales, "
                      "atención primaria, medicamentos y productos sanitarios, salud pública e investigación.",
                      "Los datos de España, Alemania, Francia, Bélgica, Portugal y Eslovaquia son provisionales."],
               "en": ["Spending by all levels of government on the «Health» function of the COFOG classification: hospitals, "
                      "outpatient care, medicines and medical products, public health and research.",
                      "Figures for Spain, Germany, France, Belgium, Portugal and Slovakia are provisional."]},
        rows=rows,
        geos=geo.country_table(r["geo"] for r in rows),
    )


def europa_bolsillo():
    raw = sources.eurostat("hlth_sha11_hf", unit="PC_CHE", icha11_hf=["HF1", "HF2", "HF3"])
    by = {k: [r for r in raw if r["icha11_hf"] == k] for k in ("HF1", "HF2", "HF3")}
    rows, year = _eu_rows(by["HF3"])
    shares = {k: {r["geo"]: r["value"] for r in _eu_rows(v)[0]} for k, v in by.items()}
    es, eu = shares["HF3"]["ESP"], shares["HF3"]["EU27"]
    es_pub, es_vol = shares["HF1"]["ESP"], shares["HF2"]["ESP"]
    eu_pub = shares["HF1"]["EU27"]
    n = len(rows) - 1
    rank = _rank(rows, "ESP")
    return chart(
        id="sae2-europa-bolsillo",
        lens="europa", theme="sanidad",
        title=bi(f"Los hogares pagan de su bolsillo el {dec(es, 'es')} % del gasto sanitario en España; en la UE, el {dec(eu, 'es')} %",
                 f"Households pay {dec(es, 'en')}% of health spending out of pocket in Spain; in the EU, {dec(eu, 'en')}%"),
        subtitle=bi(f"Pagos directos de los hogares, {year}, en % del gasto sanitario corriente. España es el {rank}.º de {n}",
                    f"Household out-of-pocket payments, {year}, as % of current health expenditure. Spain ranks {ordinal_en(rank)} of {n}"),
        unit=bi("% del gasto sanitario", "% of health spending"),
        source={**EUROSTAT, "dataset": "hlth_sha11_hf",
                "url": "https://ec.europa.eu/eurostat/databrowser/view/hlth_sha11_hf/default/table"},
        notes={"es": [f"El gasto sanitario corriente se reparte entre tres pagadores. En España, las administraciones y la Seguridad Social "
                      f"pagan el {dec(es_pub, 'es')} % (en la UE, el {dec(eu_pub, 'es')} %); los seguros voluntarios, el {dec(es_vol, 'es')} %, "
                      f"y los hogares, el resto.",
                      "Pagos directos: lo que los hogares pagan sin seguro que los cubra, como la parte del precio de los medicamentos con "
                      "receta, el dentista, las gafas o las consultas privadas.",
                      "Cuentas de salud (System of Health Accounts). No incluye el gasto de capital."],
               "en": [f"Current health expenditure is split between three payers. In Spain, government and social security pay "
                      f"{dec(es_pub, 'en')}% (in the EU, {dec(eu_pub, 'en')}%); voluntary insurance {dec(es_vol, 'en')}%, "
                      f"and households the rest.",
                      "Out-of-pocket payments: what households pay with no insurance to cover it, such as their share of the price of "
                      "prescription medicines, the dentist, glasses or private consultations.",
                      "Health accounts (System of Health Accounts). Capital spending is not included."]},
        rows=rows,
        geos=geo.country_table(r["geo"] for r in rows),
    )


# ---------- España por dentro ----------

def espera_comunidades():
    rows = [{"geo": c, "time": str(WAIT_YEAR), "value": d, "over6m": p} for c, (d, p) in sorted(WAIT_CCAA.items())]
    es = WAIT_CCAA["ES"][0]
    # Ceuta y Melilla (gestionadas por el INGESA) tienen listas muy pequeñas: no protagonizan el titular
    main = [r for r in rows if r["geo"] not in ("ES", "18", "19")]
    top = max(main, key=lambda r: r["value"])
    low = min(main, key=lambda r: r["value"])
    return chart(
        id="sad1-espera-comunidades",
        lens="dentro", theme="sanidad",
        title=bi(f"Para operarse, en {geo.ccaa_name(top['geo'], 'es')} se espera de media {top['value']} días; en "
                 f"{geo.ccaa_name(low['geo'], 'es')}, {low['value']}",
                 f"Patients waiting for surgery in {geo.ccaa_name(top['geo'], 'en')} have waited {top['value']} days on average; in "
                 f"{geo.ccaa_name(low['geo'], 'en')}, {low['value']}"),
        subtitle=bi(f"Tiempo medio de espera de los pacientes pendientes de una operación, 31 de diciembre de {WAIT_YEAR}, en días. "
                    f"España: {es} días",
                    f"Average time waited by patients pending surgery, 31 December {WAIT_YEAR}, in days. Spain: {es} days"),
        unit=bi("Días", "Days"),
        source=SISLE,
        notes={"es": ["Lista de espera estructural: pacientes con una operación no urgente prescrita cuya espera depende de la organización "
                      "y los recursos del servicio de salud. No incluye a quienes esperan por decisión propia (por ejemplo, por rechazar "
                      "operarse en otro centro) ni a quienes no se pueden operar todavía por motivos clínicos.",
                      "Tiempo que llevan esperando, en la fecha de corte, los pacientes que siguen en la lista, no el tiempo que tardaron "
                      "en operarse los que ya salieron de ella.",
                      "Cada comunidad aporta y computa sus datos; el Ministerio los agrega. Ceuta y Melilla las gestiona el INGESA.",
                      "Datos rectificados por el Ministerio para Castilla-La Mancha."],
               "en": ["Structural waiting list: patients with non-urgent surgery prescribed whose wait depends on the organisation and "
                      "resources of the health service. It excludes those waiting by their own choice (for example because they turned "
                      "down surgery at another hospital) and those who cannot yet be operated on for clinical reasons.",
                      "Time already waited, on the reference date, by patients still on the list, not the time it took those who have "
                      "already left it to be operated on.",
                      "Each region supplies and computes its own data; the Ministry of Health compiles them. Ceuta and Melilla are run "
                      "by INGESA, the national health management agency.",
                      "Figures for Castile-La Mancha as corrected by the Ministry."]},
        rows=rows,
        geos=geo.ccaa_table(r["geo"] for r in rows),
    )


def gasto_comunidades():
    rows = [{"geo": c, "time": str(SPEND_YEAR), "value": v} for c, v in sorted(SPEND_CCAA.items())]
    main = [r for r in rows if r["geo"] != "ES"]
    top = max(main, key=lambda r: r["value"])
    low = min(main, key=lambda r: r["value"])
    es = SPEND_CCAA["ES"]

    def eur(v, lang):
        n = f"{round(v):,}"
        return n.replace(",", ".") if lang == "es" else n

    return chart(
        id="sad2-gasto-comunidades",
        lens="dentro", theme="sanidad",
        title=bi(f"Cada comunidad gasta en sanidad entre {eur(low['value'], 'es')} euros por habitante ({geo.ccaa_name(low['geo'], 'es')}) "
                 f"y {eur(top['value'], 'es')} ({geo.ccaa_name(top['geo'], 'es')})",
                 f"Regions spend between {eur(low['value'], 'en')} euros per inhabitant on health ({geo.ccaa_name(low['geo'], 'en')}) "
                 f"and {eur(top['value'], 'en')} ({geo.ccaa_name(top['geo'], 'en')})"),
        subtitle=bi(f"Gasto sanitario público de cada comunidad, {SPEND_YEAR}, en euros por habitante. Conjunto de las comunidades: "
                    f"{eur(es, 'es')} euros",
                    f"Public health spending by each region, {SPEND_YEAR}, in euros per inhabitant. All regions: {eur(es, 'en')} euros"),
        unit=bi("Euros por habitante", "Euros per inhabitant"),
        source=EGSP,
        notes={"es": ["Gasto consolidado del sector comunidades autónomas. No incluye el de las mutualidades de funcionarios (MUFACE, "
                      "ISFAS y MUGEJU), el de la Administración central ni el de los ayuntamientos. Ceuta y Melilla no figuran: las "
                      "gestiona el INGESA.",
                      f"Datos de {SPEND_YEAR} provisionales. Población residente a 1 de julio (INE).",
                      "Euros por habitante sin ajustar por edad: una población más envejecida necesita más atención por persona.",
                      "La barra de España es el conjunto de las comunidades."],
               "en": ["Consolidated spending by the regional government sector. It excludes the civil servants' mutual funds (MUFACE, "
                      "ISFAS and MUGEJU), central government and municipalities. Ceuta and Melilla are not shown: they are run by INGESA.",
                      f"{SPEND_YEAR} figures are provisional. Resident population on 1 July (INE).",
                      "Euros per inhabitant not adjusted for age: an older population needs more care per person.",
                      "The bar for Spain is all regions combined."]},
        rows=rows,
        geos=geo.ccaa_table(r["geo"] for r in rows),
    )


# ---------- España en el tiempo ----------

def lista_espera():
    rows = [{"time": str(y), "series": "tasa", "value": v} for y, v in sorted(WAIT_RATE.items())]
    first, last = min(WAIT_RATE), max(WAIT_RATE)
    peak = max(WAIT_RATE, key=WAIT_RATE.get)
    return chart(
        id="sat1-lista-espera",
        lens="tiempo", theme="sanidad",
        title=bi(f"Por cada 1.000 habitantes, {dec(WAIT_RATE[last], 'es')} personas esperan una operación; a finales de {first}, "
                 f"{dec(WAIT_RATE[first], 'es')}",
                 f"For every 1,000 inhabitants, {dec(WAIT_RATE[last], 'en')} people are waiting for surgery; at the end of {first}, "
                 f"{dec(WAIT_RATE[first], 'en')}"),
        subtitle=bi(f"Pacientes en lista de espera quirúrgica por 1.000 habitantes, a 31 de diciembre de cada año, {first}-{last}",
                    f"Patients on the surgical waiting list per 1,000 inhabitants, on 31 December each year, {first}-{last}"),
        unit=bi("Pacientes por 1.000 habitantes", "Patients per 1,000 inhabitants"),
        source=SISLE,
        notes={"es": [f"Población con tarjeta sanitaria. El máximo de la serie es el de {peak} ({dec(WAIT_RATE[peak], 'es')}).",
                      "La serie empieza en 2018 porque ese año Andalucía cambió su forma de contar la lista de espera; hasta 2016, "
                      "además, los datos de Cataluña eran una estimación.",
                      "Cada valor sale del informe de su corte. Los informes de junio no se incluyen."],
               "en": [f"Population with a health card. The highest value in the series is {peak} ({dec(WAIT_RATE[peak], 'en')}).",
                      "The series starts in 2018 because that year Andalusia changed the way it counts its waiting list; until 2016, "
                      "Catalonia's figures were also an estimate.",
                      "Each value comes from the report for that date. The June reports are not included."]},
        rows=rows,
        extra={"dimensions": {"series": {"tasa": bi("Lista de espera quirúrgica", "Surgical waiting list")}},
               "short_labels": {"tasa": bi("Lista de espera", "Waiting list")}},
    )


FUNCTION_GROUPS = {
    "hospital": bi("Hospitales y especialistas", "Hospitals and specialists"),
    "primaria": bi("Atención primaria", "Primary care"),
    "farmacia": bi("Farmacia (recetas)", "Pharmacy (prescriptions)"),
}
FUNCTION_SHORT = {"hospital": bi("Hospitales", "Hospitals"), "primaria": bi("Primaria", "Primary care"), "farmacia": bi("Farmacia", "Pharmacy")}


def gasto_funciones():
    for i, total in enumerate(FUNCTIONS_TOTAL):
        assert abs(sum(v[i] for v in FUNCTIONS.values()) - total) <= 10, (YEARS[i], total)
    share = {k: [100 * v[i] / FUNCTIONS_TOTAL[i] for i in range(len(YEARS))] for k, v in FUNCTIONS.items()}
    rows = [{"time": str(y), "series": k, "value": round(share[k][i], 1)} for k in FUNCTION_GROUPS for i, y in enumerate(YEARS)]
    first, last = YEARS[0], YEARS[-1]
    h0, h1 = share["hospital"][0], share["hospital"][-1]
    p0, p1 = share["primaria"][0], share["primaria"][-1]
    f0, f1 = share["farmacia"][0], share["farmacia"][-1]
    return chart(
        id="sat2-gasto-funciones",
        lens="tiempo", theme="sanidad",
        title=bi(f"Los hospitales se llevan el {es_num(h1)} % del gasto sanitario público, frente al {es_num(h0)} % en {first}; "
                 f"la farmacia baja del {es_num(f0)} % al {es_num(f1)} %",
                 f"Hospitals take {es_num(h1)}% of public health spending, against {es_num(h0)}% in {first}; "
                 f"pharmacy falls from {es_num(f0)}% to {es_num(f1)}%"),
        subtitle=bi(f"Reparto del gasto sanitario público por función, {first}-{last}, en % del total",
                    f"Breakdown of public health spending by function, {first}-{last}, as % of the total"),
        unit=bi("% del gasto sanitario público", "% of public health spending"),
        source=EGSP,
        notes={"es": ["Hospitales y especialistas incluye las consultas de especialistas fuera del hospital y los medicamentos que se "
                      "dispensan en el hospital. Farmacia es el gasto en recetas que se dispensan en las oficinas de farmacia.",
                      f"La atención primaria pasa del {dec(p0, 'es')} % al {dec(p1, 'es')} %. El resto del gasto es salud pública, servicios "
                      "colectivos, traslados, prótesis e inversión.",
                      "Gasto consolidado de todas las administraciones. 2023 y 2024, provisionales."],
               "en": ["Hospitals and specialists includes specialist consultations outside hospital and medicines dispensed in hospital. "
                      "Pharmacy is spending on prescriptions dispensed by community pharmacies.",
                      f"Primary care goes from {dec(p0, 'en')}% to {dec(p1, 'en')}%. The rest is public health, collective services, "
                      "patient transport, prostheses and investment.",
                      "Consolidated spending by all levels of government. 2023 and 2024 are provisional."]},
        rows=rows,
        extra={"dimensions": {"series": FUNCTION_GROUPS}, "short_labels": FUNCTION_SHORT},
    )


BUILDERS = [europa_gasto, europa_bolsillo, espera_comunidades, gasto_comunidades, lista_espera, gasto_funciones]
