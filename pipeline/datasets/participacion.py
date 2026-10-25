"""Participación en las elecciones al Congreso desde 1977, por provincia y en el total de España.

Fuente: Ministerio del Interior, Infoelectoral (ficheros MUNI de cada elección, fichero 07: totales por
ámbito superior al municipio). Se guarda en data/base porque Infoelectoral no responde desde algunos
entornos en la nube: así los gráficos se pueden rehacer sin volver a descargarlo.

Votantes = blancos + nulos + votos a candidaturas. La participación se calcula sobre el censo de escrutinio,
que incluye a los residentes en el extranjero (CERA): es la cifra oficial. Estos ficheros no separan el censo
ni el voto exterior.
"""

from lib import geo

from . import elecciones

# Elecciones generales: año y mes del fichero MUNI (02AAAAMM)
ELECTIONS = ["197706", "197903", "198210", "198606", "198910", "199306", "199603", "200003", "200403",
             "200803", "201111", "201512", "201606", "201904", "201911", "202307"]


def _totals(ym: str) -> list[dict]:
    f = elecciones._read(ym)
    out = []
    for line in f["07"]:
        ccaa, prov = line[9:11], line[11:13]
        if line[13] != "9":
            continue
        if ccaa == "99":
            code = "ES"
        elif prov != "99":
            code = prov
        else:
            continue
        census = int(line[85:93])  # columnas 86-93: censo de escrutinio
        blank, null, parties = int(line[125:133]), int(line[133:141]), int(line[141:149])
        voters = blank + null + parties
        out.append({
            "geo": code,
            "census": census,
            "voters": voters,
            "blank": blank,
            "null": null,
            "turnout": round(100 * voters / census, 2),
        })
    return out


def build() -> dict:
    rows = []
    warnings = []
    for ym in ELECTIONS:
        t = _totals(ym)
        nat = next((r for r in t if r["geo"] == "ES"), None)
        assert nat, f"{ym}: sin total nacional"
        provs = [r for r in t if r["geo"] != "ES"]
        if len(provs) != 52:
            warnings.append(f"{ym}: {len(provs)} provincias")
        diff = abs(sum(r["voters"] for r in provs) - nat["voters"])
        assert diff <= 0.001 * nat["voters"], f"{ym}: la suma provincial no cuadra con el total ({diff})"
        for r in t:
            rows.append({"election": f"{ym[:4]}-{ym[4:]}", "year": int(ym[:4]), **r})
    return {
        "id": "participacion",
        "title": "Participación en las elecciones al Congreso, 1977-2023",
        "source": {**elecciones.SOURCE, "dataset": "Ficheros MUNI de cada elección general (fichero 07)"},
        "notes": [
            "Votantes: votos en blanco, nulos y a candidaturas.",
            "census: censo de escrutinio, que incluye a los residentes en el extranjero (CERA). turnout: votantes entre ese censo, "
            "la participación oficial.",
            "Estos ficheros no separan el voto exterior: su caída con el voto rogado (2011-2022) baja la participación total "
            "de esos años y no se puede descontar con estos datos.",
            "geo: código INE de provincia o «ES» para el total. Los votos de los residentes en el extranjero se cuentan en su provincia.",
        ],
        "provinces": {k: v[0] for k, v in geo.PROVINCIAS.items()},
        "warnings": warnings,
        "rows": rows,
    }
