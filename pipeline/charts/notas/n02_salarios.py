"""N02. Salarios reales y salario mínimo.

Datos: salario medio por trabajador (INE, ETCL), IPC (INE) y salario mínimo interprofesional (Eurostat, earn_mw_cur, que
lo publica en 12 pagas: la cuantía del BOE por 14 / 12). Todo en medias anuales de años completos, desde 2008.
"""

from lib import sources
from lib.output import chart

from ..common import annual, pct
from ..legislatura import CPI_TABLE, INE_CPI, INE_WAGE, WAGE_TABLE, es1

BASE = 2008             # primer año de la ETCL con la serie actual
WAGE_NAME = ("Total Nacional. Industria, construcción y servicios (excepto actividades de los hogares como empleadores y de "
             "organizaciones y organismos extraterritoriales). Coste salarial total. Costes laborales. Euros")
EUROSTAT_MW = {"name": "Eurostat, salarios mínimos mensuales", "dataset": "earn_mw_cur",
               "url": "https://ec.europa.eu/eurostat/databrowser/view/earn_mw_cur/default/table", "license": "CC BY 4.0"}
BOE_2026 = {"name": "BOE, Real Decreto 126/2026 (salario mínimo de 2026: 1.221 euros al mes en 14 pagas)",
            "url": "https://www.boe.es/eli/es/rd/2026/02/18/126/con"}


def _data():
    wage = annual([r for r in sources.ine_table(WAGE_TABLE) if r["series"] == WAGE_NAME])
    cpi = annual([r for r in sources.ine_table(CPI_TABLE) if r["series"].startswith("Índice general. Índice")
                  or r["series"].startswith("Nacional. Índice general. Índice")])
    # Valor vigente el 1 de julio (segundo semestre): el del 1 de enero no recoge las subidas aprobadas con efecto
    # retroactivo después de esa fecha (por ejemplo, la de 2023, aprobada en febrero).
    mw = {int(r["time"][:4]): r["value"] for r in sources.eurostat("earn_mw_cur", geo="ES", currency="EUR")
          if r["time"].endswith("S2")}
    years = [y for y in sorted(set(wage) & set(cpi) & set(mw)) if y >= BASE]
    assert years[0] == BASE, years
    return wage, cpi, mw, years


def salario_real():
    wage, cpi, mw, years = _data()
    real = {"salario": {y: wage[y] / cpi[y] for y in years}, "smi": {y: mw[y] / cpi[y] for y in years}}
    rows = [{"time": str(y), "series": k, "value": round(100 * s[y] / s[BASE], 1)} for k, s in real.items() for y in years]
    last = years[-1]
    w, m = pct(real["salario"][BASE], real["salario"][last]), pct(real["smi"][BASE], real["smi"][last])
    title = (f"Descontada la inflación, el salario medio de {last} es un {es1(abs(w))} % {'menor' if w < 0 else 'mayor'} que el de {BASE}; "
             f"el salario mínimo, un {es1(m)} % mayor")
    return chart(
        id="n02-salario-real",
        lens="tiempo", theme="empleo",
        title=title,
        subtitle=f"Salario medio por trabajador y salario mínimo descontada la inflación. Índices, {BASE} = 100, medias anuales, {BASE}-{last}",
        unit=f"Índice ({BASE} = 100)",
        source={**INE_WAGE, "also": [INE_CPI, EUROSTAT_MW, BOE_2026]},
        notes=["Salario medio: coste salarial total por trabajador y mes de la ETCL (industria, construcción y servicios; "
               "sin agricultura ni empleo del hogar), con las pagas extra repartidas. Es una media: si se destruye sobre todo "
               "empleo de salario bajo, como en 2008-2013 o en 2020, la media sube aunque ningún salario lo haga.",
               "En 2020 el salario medio baja también porque los trabajadores en ERTE cobraban de la Seguridad Social, no de la empresa.",
               "Salario mínimo: cuantía mensual vigente el 1 de julio de cada año, en 12 pagas (Eurostat).",
               "Inflación: IPC general, media anual. Los dos índices se deflactan con el mismo IPC.",
               f"Solo años completos: el último año con salario e IPC de todo el año es {last}."],
        rows=rows,
        extra={"dimensions": {"series": {"salario": {"es": "Salario medio"}, "smi": {"es": "Salario mínimo"}}},
               "ref_line": {"value": 100, "label": {"es": str(BASE)}}},
    )


def smi_salario_medio():
    wage, cpi, mw, years = _data()
    rows = [{"time": str(y), "series": "ratio", "value": round(100 * mw[y] / wage[y], 1)} for y in years]
    v = {int(r["time"]): r["value"] for r in rows}
    last = years[-1]
    return chart(
        id="n02-smi-salario-medio",
        lens="tiempo", theme="empleo",
        title=f"El salario mínimo pasa del {es1(v[BASE])} % al {es1(v[last])} % del salario medio entre {BASE} y {last}",
        subtitle=f"Salario mínimo en % del salario medio por trabajador, {BASE}-{last}",
        unit="% del salario medio",
        source={**EUROSTAT_MW, "also": [INE_WAGE]},
        notes=["Las dos cifras son mensuales y en 12 pagas: el salario mínimo vigente el 1 de julio (Eurostat) y el coste "
               "salarial total por trabajador de la ETCL (media anual, industria, construcción y servicios).",
               "Es el salario medio, no la mediana ni el salario neto: no es la referencia de la Carta Social Europea "
               "(60 % del salario neto medio), que usa otra definición.",
               "El salario medio baja en 2020 por los ERTE, y eso sube el porcentaje de ese año."],
        rows=rows,
        extra={"dimensions": {"series": {"ratio": {"es": "Salario mínimo / salario medio"}}}},
    )


BUILDERS = [salario_real, smi_salario_medio]
