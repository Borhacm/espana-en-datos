"""Utilidades compartidas por los gráficos de todos los temas."""

import unicodedata
from collections import defaultdict


def _norm(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


# Nombres del INE ("Madrid, Comunidad de", "Castilla - La Mancha"...) -> código de comunidad
def ine_ccaa(name: str) -> str | None:
    n = _norm(name)
    if n.startswith("nacional") or n.startswith("total nacional"):
        return "ES"
    keys = {"andalucia": "01", "aragon": "02", "asturias": "03", "balears": "04", "canarias": "05", "cantabria": "06",
            "castilla y leon": "07", "castilla - la mancha": "08", "castilla-la mancha": "08", "cataluna": "09",
            "comunitat valenciana": "10", "extremadura": "11", "galicia": "12", "madrid": "13", "murcia": "14",
            "navarra": "15", "pais vasco": "16", "rioja": "17", "ceuta": "18", "melilla": "19"}
    for k, code in keys.items():
        if n.startswith(k):
            return code
    return None


def annual(rows: list[dict]) -> dict[int, float]:
    """Media anual de una serie trimestral o mensual, solo con años completos."""
    by_year = defaultdict(list)
    for r in rows:
        by_year[r["year"]].append(r["value"])
    full = 4 if "Q" in rows[0]["period"] else 12
    return {y: sum(v) / len(v) for y, v in by_year.items() if len(v) == full}


def pct(a: float, b: float) -> float:
    return round(100 * (b / a - 1), 1)


def es_num(v: float) -> str:
    """Entero redondeando los empates hacia arriba (62,5 -> 63), igual que el navegador (Intl.NumberFormat).
    El redondeo por defecto de Python lleva los empates al par (62,5 -> 62) y el texto no cuadraría con el gráfico."""
    from decimal import ROUND_HALF_UP, Decimal

    return str(Decimal(str(v)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def en_num(v: float) -> str:
    """Igual que es_num, para el texto en inglés (los enteros se escriben igual en los dos idiomas)."""
    return es_num(v)


def dec(v: float, lang: str, digits: int = 1) -> str:
    """Número con decimales en el idioma pedido: 3,7 en español, 3.7 en inglés."""
    s = f"{v:.{digits}f}"
    return s.replace(".", ",") if lang == "es" else s


def ordinal_en(n: int) -> str:
    """1 -> 1st, 2 -> 2nd, 11 -> 11th..."""
    suffix = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def bi(es: str, en: str) -> dict:
    """Texto en los dos idiomas de la web."""
    return {"es": es, "en": en}
