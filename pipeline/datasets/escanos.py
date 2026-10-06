"""Reparto de los 350 escaños del Congreso por provincia (LOREG, art. 162), a partir del padrón oficial.

Cada provincia tiene 2 escaños fijos y Ceuta y Melilla, 1. Los 248 restantes se reparten por población:
cuota = población total / 248; cada provincia recibe la parte entera de su población / cuota, y los escaños
que sobran van a las provincias con mayor resto decimal.

Fuente: INE, cifras oficiales del padrón (operación 22, una tabla por provincia). El decreto de convocatoria
fija el reparto oficial: el resultado se contrasta con él (CHECK_2026).
"""

import json
import unicodedata

from lib import geo
from lib.http import fetch

INE_TABLES = "https://servicios.ine.es/wstempus/js/ES/TABLAS_OPERACION/22"
INE_DATA = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/{id}?nult=1&tip=A"
SOURCE = {
    "name": "INE, cifras oficiales de población (revisión del padrón)",
    "url": "https://www.ine.es/dyngs/INEbase/operacion.htm?c=Estadistica_C&cid=1254736177011&menu=resultados&idp=1254734710990",
    "license": "Reutilización libre citando la fuente",
}

# Nombres del INE que no coinciden con los nuestros
ALIASES = {"araba/alava": "01", "alicante/alacant": "03", "balears, illes": "07", "castellon/castello": "12",
           "coruna, a": "15", "rioja, la": "26", "palmas, las": "35", "valencia/valencia": "46"}

# Reparto oficial del Real Decreto 806/2026, de 5 de octubre (BOE-A-2026-20742, BOE núm. 248 de 6 de octubre de 2026),
# anexo de diputados por circunscripción. Contrasta el cálculo.
CHECK_2026: dict[str, int] = {
    "01": 4, "02": 4, "03": 12, "04": 6, "05": 3, "06": 5, "07": 8, "08": 32, "09": 4, "10": 4,
    "11": 8, "12": 5, "13": 5, "14": 6, "15": 8, "16": 3, "17": 6, "18": 7, "19": 3, "20": 6,
    "21": 5, "22": 3, "23": 5, "24": 4, "25": 4, "26": 4, "27": 4, "28": 38, "29": 11, "30": 10,
    "31": 5, "32": 4, "33": 7, "34": 3, "35": 8, "36": 7, "37": 4, "38": 7, "39": 5, "40": 3,
    "41": 12, "42": 2, "43": 6, "44": 3, "45": 6, "46": 16, "47": 5, "48": 8, "49": 3, "50": 7,
    "51": 1, "52": 1,
}


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower().strip()
    return s


def population() -> tuple[dict[str, int], int]:
    names = {_norm(n): code for code, (n, _) in geo.PROVINCIAS.items()}
    names.update(ALIASES)
    tables = json.loads(fetch(INE_TABLES, ".json").read_text())
    out, year = {}, None
    for t in tables:
        if "Población por municipios y sexo" not in t["Nombre"]:
            continue
        series = json.loads(fetch(INE_DATA.format(id=t["Id"]), ".json").read_text())
        # El total de la provincia es la serie «Total» (ambos sexos) con más población; no siempre va primera
        totals = [x for x in series if x["Data"] and x["Nombre"].split(".")[1].strip() == "Total"]
        first = max(totals, key=lambda x: x["Data"][0]["Valor"])
        prov = first["Nombre"].split(".")[0]
        code = names.get(_norm(prov))
        assert code, f"provincia sin código: {prov}"
        out[code] = int(first["Data"][0]["Valor"])
        year = first["Data"][0]["Anyo"]
    assert len(out) == 52, len(out)
    return out, year


def allocate(pop: dict[str, int], total: int = 350) -> dict[str, int]:
    fixed = {c: (1 if c in ("51", "52") else 2) for c in pop}
    rest = total - sum(fixed.values())  # 248
    pool = {c: p for c, p in pop.items() if c not in ("51", "52")}
    quota = sum(pool.values()) / rest
    seats = {c: fixed[c] + int(p // quota) for c, p in pool.items()}
    left = rest - sum(int(p // quota) for p in pool.values())
    by_rest = sorted(pool, key=lambda c: -(pool[c] / quota - int(pool[c] / quota)))
    for c in by_rest[:left]:
        seats[c] += 1
    seats.update({"51": 1, "52": 1})
    assert sum(seats.values()) == total
    return seats


def build() -> dict:
    pop, year = population()
    seats = allocate(pop)
    if CHECK_2026:
        diff = {c: (seats[c], CHECK_2026[c]) for c in seats if seats[c] != CHECK_2026.get(c)}
        assert not diff, f"el cálculo no coincide con el decreto: {diff}"
    return {
        "id": "escanos-2026",
        "title": f"Escaños por provincia para las generales de 2026 (padrón a 1 de enero de {year})",
        "source": SOURCE,
        "verified": bool(CHECK_2026),
        "population_year": year,
        "notes": ["Cálculo según el artículo 162 de la LOREG. El reparto oficial lo fija el decreto de convocatoria."],
        "rows": [{"geo": c, "name": geo.PROVINCIAS[c][0], "population": pop[c], "seats": seats[c]} for c in sorted(seats)],
    }
