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
