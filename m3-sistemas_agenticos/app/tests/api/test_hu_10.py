"""Pruebas de API para HU-10: solicitud y consulta de vacaciones."""

import uuid

import httpx


def _datos_empleado(**overrides: object) -> dict:
    datos = {
        "nombre": "Empleado de Vacaciones",
        "correo": f"hu10.{uuid.uuid4().hex[:8]}@empresa.com",
        "puesto": "Analista Junior",
        "departamento": "Ventas",
        "fecha_ingreso": "2022-03-01",
    }
    datos.update(overrides)
    return datos


def _crear_empleado(url_api: str, **overrides: object) -> dict:
    respuesta = httpx.post(f"{url_api}/api/empleados", json=_datos_empleado(**overrides))
    assert respuesta.status_code == 201
    return respuesta.json()


def _dar_de_baja(url_api: str, numero_empleado: str, fecha_baja: str) -> dict:
    respuesta = httpx.patch(
        f"{url_api}/api/empleados/{numero_empleado}/baja", json={"fecha_baja": fecha_baja}
    )
    assert respuesta.status_code == 200
    return respuesta.json()


def _solicitar_vacaciones(
    url_api: str, empleado_id: int, fecha_inicio: str, fecha_fin: str
) -> httpx.Response:
    return httpx.post(
        f"{url_api}/api/empleados/{empleado_id}/vacaciones",
        json={"fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin},
    )


def test_cp_01_solicitud_valida_descuenta_del_saldo(url_api: str) -> None:
    """CP-01: solicitud válida que se registra y descuenta del saldo del año."""
    empleado = _crear_empleado(url_api, fecha_ingreso="2024-03-10")

    respuesta = _solicitar_vacaciones(url_api, empleado["id"], "2026-07-06", "2026-07-10")

    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert cuerpo["empleado_id"] == empleado["id"]
    assert cuerpo["dias_habiles"] == 5
    assert cuerpo["dias_restantes"] == 7


def test_cp_03_calculo_excluye_fines_de_semana_y_festivos(url_api: str) -> None:
    """CP-03: el cálculo de días hábiles excluye fines de semana y festivos oficiales."""
    empleado = _crear_empleado(url_api, fecha_ingreso="2020-01-15")

    respuesta = _solicitar_vacaciones(url_api, empleado["id"], "2026-12-21", "2026-12-31")

    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert cuerpo["dias_habiles"] == 8
    assert cuerpo["dias_restantes"] == 4


def test_cp_05_rechazar_empleado_inexistente(url_api: str) -> None:
    """CP-05: rechazo cuando el empleado no existe."""
    respuesta = _solicitar_vacaciones(url_api, 2_000_000_000, "2026-07-06", "2026-07-10")

    assert respuesta.status_code == 404
    assert respuesta.json()["detail"] == "Empleado no encontrado"


def test_cp_06_rechazar_empleado_dado_de_baja(url_api: str) -> None:
    """CP-06: rechazo cuando el empleado está dado de baja."""
    empleado = _crear_empleado(url_api, fecha_ingreso="2020-01-10")
    _dar_de_baja(url_api, empleado["numero_empleado"], "2024-01-10")

    respuesta = _solicitar_vacaciones(url_api, empleado["id"], "2026-07-06", "2026-07-10")

    assert respuesta.status_code == 409
    assert (
        respuesta.json()["detail"]
        == "No se pueden solicitar vacaciones para un empleado dado de baja"
    )


def test_cp_07_rechazar_fecha_fin_anterior_a_inicio(url_api: str) -> None:
    """CP-07: rechazo cuando la fecha de fin es anterior a la fecha de inicio."""
    empleado = _crear_empleado(url_api, fecha_ingreso="2024-03-10")

    respuesta = _solicitar_vacaciones(url_api, empleado["id"], "2026-07-10", "2026-07-06")

    assert respuesta.status_code == 400
    assert (
        respuesta.json()["detail"] == "La fecha de fin no puede ser anterior a la fecha de inicio"
    )


def test_cp_08_rechazar_periodo_cruza_de_anio(url_api: str) -> None:
    """CP-08: rechazo cuando el periodo cruza de un año a otro."""
    empleado = _crear_empleado(url_api, fecha_ingreso="2024-03-10")

    respuesta = _solicitar_vacaciones(url_api, empleado["id"], "2026-12-28", "2027-01-08")

    assert respuesta.status_code == 400
    assert (
        respuesta.json()["detail"] == "Las vacaciones deben estar dentro de un mismo año calendario"
    )


def test_cp_09_rechazar_anio_sin_festivos(url_api: str) -> None:
    """CP-09: rechazo cuando el año no está en la tabla de festivos."""
    empleado = _crear_empleado(url_api, fecha_ingreso="2024-03-10")

    respuesta = _solicitar_vacaciones(url_api, empleado["id"], "2025-07-06", "2025-07-10")

    assert respuesta.status_code == 400
    assert respuesta.json()["detail"] == "Solo se pueden solicitar vacaciones en 2026 y 2027"


def test_cp_10_rechazar_antiguedad_insuficiente(url_api: str) -> None:
    """CP-10: rechazo por antigüedad insuficiente (Regla 1)."""
    empleado = _crear_empleado(url_api, fecha_ingreso="2025-12-21")

    respuesta = _solicitar_vacaciones(url_api, empleado["id"], "2026-12-18", "2026-12-19")

    assert respuesta.status_code == 400
    assert (
        respuesta.json()["detail"]
        == "Se requiere al menos un año de antigüedad a la fecha de inicio"
    )


def test_cp_11_rechazar_periodo_sin_dias_habiles(url_api: str) -> None:
    """CP-11: rechazo cuando el periodo no incluye ningún día hábil (Regla 3)."""
    empleado = _crear_empleado(url_api, fecha_ingreso="2024-03-10")

    respuesta = _solicitar_vacaciones(url_api, empleado["id"], "2026-07-11", "2026-07-12")

    assert respuesta.status_code == 400
    assert respuesta.json()["detail"] == "El periodo no incluye días hábiles"


def test_cp_12_rechazar_excede_dias_disponibles(url_api: str) -> None:
    """CP-12: rechazo cuando la solicitud rebasa los días disponibles del año (Regla 2)."""
    empleado = _crear_empleado(url_api, fecha_ingreso="2020-01-01")
    consumo = _solicitar_vacaciones(url_api, empleado["id"], "2026-07-13", "2026-07-16")
    assert consumo.status_code == 201
    assert consumo.json()["dias_habiles"] == 4

    respuesta = _solicitar_vacaciones(url_api, empleado["id"], "2026-11-02", "2026-11-12")

    assert respuesta.status_code == 400
    assert (
        respuesta.json()["detail"]
        == "La solicitud excede los días disponibles: quedan 8 días hábiles"
    )
