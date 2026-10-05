"""Territorios: comunidades y provincias con los códigos del INE.

Se usan siempre los códigos del INE. Infoelectoral numera las comunidades de otra forma,
así que la comunidad se deduce siempre de la provincia, nunca de su código de comunidad.
"""

# Comunidades y ciudades autónomas (código INE -> nombre corto)
CCAA = {
    "01": "Andalucía",
    "02": "Aragón",
    "03": "Asturias",
    "04": "Baleares",
    "05": "Canarias",
    "06": "Cantabria",
    "07": "Castilla y León",
    "08": "Castilla-La Mancha",
    "09": "Cataluña",
    "10": "Comunidad Valenciana",
    "11": "Extremadura",
    "12": "Galicia",
    "13": "Madrid",
    "14": "Murcia",
    "15": "Navarra",
    "16": "País Vasco",
    "17": "La Rioja",
    "18": "Ceuta",
    "19": "Melilla",
}

# Provincias (código INE -> nombre, comunidad)
PROVINCIAS = {
    "01": ("Álava", "16"), "02": ("Albacete", "08"), "03": ("Alicante", "10"), "04": ("Almería", "01"),
    "05": ("Ávila", "07"), "06": ("Badajoz", "11"), "07": ("Baleares", "04"), "08": ("Barcelona", "09"),
    "09": ("Burgos", "07"), "10": ("Cáceres", "11"), "11": ("Cádiz", "01"), "12": ("Castellón", "10"),
    "13": ("Ciudad Real", "08"), "14": ("Córdoba", "01"), "15": ("A Coruña", "12"), "16": ("Cuenca", "08"),
    "17": ("Girona", "09"), "18": ("Granada", "01"), "19": ("Guadalajara", "08"), "20": ("Gipuzkoa", "16"),
    "21": ("Huelva", "01"), "22": ("Huesca", "02"), "23": ("Jaén", "01"), "24": ("León", "07"),
    "25": ("Lleida", "09"), "26": ("La Rioja", "17"), "27": ("Lugo", "12"), "28": ("Madrid", "13"),
    "29": ("Málaga", "01"), "30": ("Murcia", "14"), "31": ("Navarra", "15"), "32": ("Ourense", "12"),
    "33": ("Asturias", "03"), "34": ("Palencia", "07"), "35": ("Las Palmas", "05"), "36": ("Pontevedra", "12"),
    "37": ("Salamanca", "07"), "38": ("Santa Cruz de Tenerife", "05"), "39": ("Cantabria", "06"), "40": ("Segovia", "07"),
    "41": ("Sevilla", "01"), "42": ("Soria", "07"), "43": ("Tarragona", "09"), "44": ("Teruel", "02"),
    "45": ("Toledo", "08"), "46": ("Valencia", "10"), "47": ("Valladolid", "07"), "48": ("Bizkaia", "16"),
    "49": ("Zamora", "07"), "50": ("Zaragoza", "02"), "51": ("Ceuta", "18"), "52": ("Melilla", "19"),
}

assert len(PROVINCIAS) == 52 and {c for _, c in PROVINCIAS.values()} == set(CCAA)


def ccaa_of_province(prov: str) -> str:
    return PROVINCIAS[prov][1]


# ---------- Países (para la mirada «España frente a Europa»), copiado de Europa en datos ----------

# ISO3: (código Eurostat, nombre ES, nombre EN, es miembro de la UE)
COUNTRIES = {
    "AUT": ("AT", "Austria", "Austria", True),
    "BEL": ("BE", "Bélgica", "Belgium", True),
    "BGR": ("BG", "Bulgaria", "Bulgaria", True),
    "HRV": ("HR", "Croacia", "Croatia", True),
    "CYP": ("CY", "Chipre", "Cyprus", True),
    "CZE": ("CZ", "Chequia", "Czechia", True),
    "DNK": ("DK", "Dinamarca", "Denmark", True),
    "EST": ("EE", "Estonia", "Estonia", True),
    "FIN": ("FI", "Finlandia", "Finland", True),
    "FRA": ("FR", "Francia", "France", True),
    "DEU": ("DE", "Alemania", "Germany", True),
    "GRC": ("EL", "Grecia", "Greece", True),
    "HUN": ("HU", "Hungría", "Hungary", True),
    "IRL": ("IE", "Irlanda", "Ireland", True),
    "ITA": ("IT", "Italia", "Italy", True),
    "LVA": ("LV", "Letonia", "Latvia", True),
    "LTU": ("LT", "Lituania", "Lithuania", True),
    "LUX": ("LU", "Luxemburgo", "Luxembourg", True),
    "MLT": ("MT", "Malta", "Malta", True),
    "NLD": ("NL", "Países Bajos", "Netherlands", True),
    "POL": ("PL", "Polonia", "Poland", True),
    "PRT": ("PT", "Portugal", "Portugal", True),
    "ROU": ("RO", "Rumanía", "Romania", True),
    "SVK": ("SK", "Eslovaquia", "Slovakia", True),
    "SVN": ("SI", "Eslovenia", "Slovenia", True),
    "ESP": ("ES", "España", "Spain", True),
    "SWE": ("SE", "Suecia", "Sweden", True),
    # Europa fuera de la UE
    "NOR": ("NO", "Noruega", "Norway", False),
    "ISL": ("IS", "Islandia", "Iceland", False),
    "CHE": ("CH", "Suiza", "Switzerland", False),
    "GBR": ("UK", "Reino Unido", "United Kingdom", False),
    "TUR": ("TR", "Turquía", "Türkiye", False),
    "SRB": ("RS", "Serbia", "Serbia", False),
    "MNE": ("ME", "Montenegro", "Montenegro", False),
    "BIH": ("BA", "Bosnia y Herzegovina", "Bosnia and Herzegovina", False),
    "ALB": ("AL", "Albania", "Albania", False),
    "MKD": ("MK", "Macedonia del Norte", "North Macedonia", False),
    "XKX": ("XK", "Kosovo", "Kosovo", False),
    "UKR": ("UA", "Ucrania", "Ukraine", False),
    "MDA": ("MD", "Moldavia", "Moldova", False),
    # Resto del mundo
    "USA": (None, "Estados Unidos", "United States", False),
    "CHN": (None, "China", "China", False),
    "JPN": (None, "Japón", "Japan", False),
    "KOR": (None, "Corea del Sur", "South Korea", False),
}

EU27 = [iso3 for iso3, c in COUNTRIES.items() if c[3]]
EU_NAMES = {"es": "Unión Europea", "en": "European Union"}

_FROM_EUROSTAT = {c[0]: iso3 for iso3, c in COUNTRIES.items() if c[0]}
_AGGREGATES = {"EU27_2020": "EU27", "EU27": "EU27", "EUU": "EU27"}
# Códigos de socios comerciales de Eurostat fuera de Europa (China sin Hong Kong)
_PARTNERS = {"US": "USA", "CN_X_HK": "CHN", "JP": "JPN", "KR": "KOR"}
# Agregado UE-27 en la OIT
_ILO = {"X92": "EU27"}



def from_eurostat(code: str) -> str | None:
    """Código Eurostat a ISO3 (o 'EU27'). None para agregados que no usamos."""
    return _AGGREGATES.get(code) or _PARTNERS.get(code) or _FROM_EUROSTAT.get(code)


def country_table(codes) -> dict:
    """Nombres de países para el JSON de salida."""
    out = {}
    for c in sorted(set(codes)):
        nm = "Unión Europea" if c == "EU27" else COUNTRIES[c][1]
        out[c] = {"es": nm, "eu": c == "EU27" or COUNTRIES[c][3], "aggregate": c == "EU27"}
    return out


def ccaa_table(codes) -> dict:
    """Nombres de comunidades (y España) para el JSON de salida."""
    out = {}
    for c in sorted(set(codes)):
        out[c] = {"es": "España" if c == "ES" else CCAA[c], "ccaa": c != "ES", "aggregate": c == "ES"}
    return out
