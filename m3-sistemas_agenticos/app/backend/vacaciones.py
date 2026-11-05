"""Reglas de negocio de vacaciones: festivos, días hábiles, antigüedad y tope anual."""

from datetime import date, timedelta

DIAS_POR_ANIO = 12

FESTIVOS: dict[int, set[date]] = {
    2026: {
        date(2026, 1, 1),
        date(2026, 2, 2),
        date(2026, 3, 16),
        date(2026, 5, 1),
        date(2026, 9, 16),
        date(2026, 11, 16),
        date(2026, 12, 25),
    },
    2027: {
        date(2027, 1, 1),
        date(2027, 2, 1),
        date(2027, 3, 15),
        date(2027, 5, 1),
        date(2027, 9, 16),
        date(2027, 11, 15),
        date(2027, 12, 25),
    },
}


def anio_valido(anio: int) -> bool:
    return anio in FESTIVOS


def contar_dias_habiles(fecha_inicio: date, fecha_fin: date) -> int:
    """Cuenta los días hábiles entre dos fechas, incluyendo ambos extremos."""
    festivos = FESTIVOS.get(fecha_inicio.year, set())
    dias = 0
    dia_actual = fecha_inicio
    while dia_actual <= fecha_fin:
        if dia_actual.weekday() < 5 and dia_actual not in festivos:
            dias += 1
        dia_actual += timedelta(days=1)
    return dias


def cumple_antiguedad(fecha_ingreso: date, fecha_inicio: date) -> bool:
    """Verifica que haya pasado al menos un año de la fecha de ingreso a la fecha de inicio."""
    try:
        aniversario = fecha_ingreso.replace(year=fecha_ingreso.year + 1)
    except ValueError:
        # 29 de febrero en un año no bisiesto: el aniversario cae el 1 de marzo.
        aniversario = date(fecha_ingreso.year + 1, 3, 1)
    return fecha_inicio >= aniversario
