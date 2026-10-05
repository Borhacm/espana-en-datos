"""Resultados de las elecciones al Congreso por provincia y por municipio.

Fuente: Ministerio del Interior, Infoelectoral (área de descargas, ficheros MUNI). Ficheros de texto de
ancho fijo descritos en FICHEROS.doc dentro de cada zip. Las candidaturas se agrupan por su «cabecera de
acumulación nacional» (PSC cuenta como PSOE, Sumar con sus marcas regionales, etc.).

El voto exterior (CERA) solo está en los totales provinciales: los municipios no lo incluyen.
"""

import io
import zipfile
from collections import defaultdict

from lib import geo
from lib.http import fetch

URL = "https://infoelectoral.interior.gob.es/estaticos/docxl/apliextr/02{ym}_MUNI.zip"
SOURCE = {
    "name": "Ministerio del Interior, Infoelectoral",
    "url": "https://infoelectoral.interior.gob.es/opencms/es/elecciones-celebradas/area-de-descargas/",
    "license": "Reutilización libre citando la fuente (Ley 37/2007)",
}

# Siglas oficiales -> nombre corto para gráficos
LABELS = {
    "PP": "PP", "PSOE": "PSOE", "VOX": "Vox", "SUMAR": "Sumar", "ERC": "ERC", "JxCAT - JUNTS": "Junts",
    "EH Bildu": "EH Bildu", "EAJ-PNV": "PNV", "B.N.G.": "BNG", "CCa": "CC", "U.P.N.": "UPN", "PACMA": "PACMA",
    "CUP-PR": "CUP", "NC-bc": "NC", "U.P.L.": "UPL", "EXISTE": "Existe", "PDeCAT-E-CiU": "PDeCAT",
}


def _read(ym: str) -> dict[str, list[str]]:
    zf = zipfile.ZipFile(fetch(URL.format(ym=ym), ".zip"))
    files = {}
    for name in zf.namelist():
        if name.upper().endswith(".DAT"):
            files[name[:2]] = io.TextIOWrapper(zf.open(name), encoding="latin-1").read().splitlines()
    return files


def results(ym: str) -> dict:
    f = _read(ym)

    # 03: candidaturas. Cada una apunta a su cabecera nacional, que da la familia de partido.
    sigla, cabecera = {}, {}
    for line in f["03"]:
        code = line[8:14]
        sigla[code] = line[14:64].strip()
        cabecera[code] = line[226:232]
    family = {code: LABELS.get(sigla[cab], sigla[cab]) for code, cab in cabecera.items()}

    # 07 + 08: ámbitos superiores al municipio. Nos quedamos con los totales provinciales y el nacional.
    def key(line):
        ccaa, prov = line[9:11], line[11:13]
        if ccaa == "99":
            return "ES"
        return prov if prov != "99" else None

    areas = {}
    for line in f["07"]:
        k = key(line)
        if k is None or line[13] != "9":
            continue
        areas[k] = {
            "census": int(line[85:93]),
            "census_cera": int(line[93:101]),
            "blank": int(line[125:133]),
            "null": int(line[133:141]),
            "to_parties": int(line[141:149]),
            "seats": int(line[149:155]),
            "votes": defaultdict(int),
            "won": defaultdict(int),
        }
    for line in f["08"]:
        k = key(line)
        if k is None or line[13] != "9" or k not in areas:
            continue
        party = family[line[14:20]]
        areas[k]["votes"][party] += int(line[20:28])
        areas[k]["won"][party] += int(line[28:33])

    provinces = []
    for k, a in areas.items():
        voters = a["blank"] + a["null"] + a["to_parties"]
        provinces.append({
            "geo": k,
            "name": "España" if k == "ES" else geo.PROVINCIAS[k][0],
            "ccaa": None if k == "ES" else geo.ccaa_of_province(k),
            "census": a["census"],
            "voters": voters,
            "turnout": round(100 * voters / a["census"], 2),
            "blank": a["blank"],
            "null": a["null"],
            "seats": a["seats"],
            "votes": dict(sorted(a["votes"].items(), key=lambda x: -x[1])),
            "won": {p: s for p, s in a["won"].items() if s},
        })

    # 05 + 06: municipios (solo totales municipales, distrito 99)
    munis = {}
    for line in f["05"]:
        if line[16:18] != "99":
            continue
        code = line[11:16]
        munis[code] = {
            "geo": code,
            "name": line[18:118].strip(),
            "prov": line[11:13],
            "census": int(line[149:157]),
            "blank": int(line[189:197]),
            "null": int(line[197:205]),
            "to_parties": int(line[205:213]),
            "votes": defaultdict(int),
        }
    for line in f["06"]:
        if line[14:16] != "99":
            continue
        m = munis.get(line[9:14])
        if m:
            m["votes"][family[line[16:22]]] += int(line[22:30])

    municipalities = []
    for m in munis.values():
        voters = m.pop("blank") + m.pop("null") + m.pop("to_parties")
        votes = {p: v for p, v in sorted(m.pop("votes").items(), key=lambda x: -x[1]) if v}
        municipalities.append({**m, "voters": voters, "votes": votes})

    nat = next(p for p in provinces if p["geo"] == "ES")
    seats_sum = sum(p["seats"] for p in provinces if p["geo"] != "ES")
    assert seats_sum == 350 == sum(nat["won"].values()), f"escaños: {seats_sum}"
    return {
        "provinces": sorted(provinces, key=lambda p: p["geo"]),
        "municipalities": sorted(municipalities, key=lambda m: m["geo"]),
    }


def build(ym: str = "202307") -> dict:
    r = results(ym)
    return {
        "id": f"congreso-{ym}",
        "title": f"Elecciones al Congreso de {ym[4:]}/{ym[:4]}: resultados por provincia y municipio",
        "source": SOURCE,
        "notes": [
            "Votos agrupados por la candidatura cabecera nacional (por ejemplo, PSC cuenta como PSOE).",
            "Participación = (votos a candidaturas + blancos + nulos) / censo de escrutinio.",
            "Los municipios no incluyen el voto exterior (CERA); los totales provinciales y nacional, sí.",
        ],
        **r,
    }
