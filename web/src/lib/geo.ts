// Comunidades y ciudades autónomas con el código del INE (el mismo que usa el pipeline, lib/geo.py).
export const CCAA: Record<string, string> = {
  "01": "Andalucía", "02": "Aragón", "03": "Asturias", "04": "Baleares", "05": "Canarias",
  "06": "Cantabria", "07": "Castilla y León", "08": "Castilla-La Mancha", "09": "Cataluña",
  "10": "Comunidad Valenciana", "11": "Extremadura", "12": "Galicia", "13": "Madrid", "14": "Murcia",
  "15": "Navarra", "16": "País Vasco", "17": "La Rioja", "18": "Ceuta", "19": "Melilla",
};

/** Nombres en inglés (los mismos que pone el pipeline en los JSON, lib/geo.py) */
export const CCAA_EN: Record<string, string> = {
  "01": "Andalusia", "02": "Aragon", "03": "Asturias", "04": "Balearic Islands", "05": "Canary Islands",
  "06": "Cantabria", "07": "Castile and León", "08": "Castile-La Mancha", "09": "Catalonia",
  "10": "Valencian Community", "11": "Extremadura", "12": "Galicia", "13": "Madrid", "14": "Murcia",
  "15": "Navarre", "16": "Basque Country", "17": "La Rioja", "18": "Ceuta", "19": "Melilla",
};
