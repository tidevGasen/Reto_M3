"""Pruebas end-to-end para HU-10: solicitud de vacaciones."""

import uuid

import httpx
from playwright.sync_api import Page, expect


def _datos_empleado(**overrides: object) -> dict:
    datos = {
        "nombre": "Empleado de Vacaciones",
        "correo": f"hu10e2e.{uuid.uuid4().hex[:8]}@empresa.com",
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


def test_cp_02_solicitud_valida_descuenta_del_saldo(
    page: Page, url_api: str, url_web: str
) -> None:
    """CP-02: solicitud válida que se registra y descuenta del saldo del año."""
    empleado = _crear_empleado(url_api, fecha_ingreso="2024-03-10")
    fila_id = empleado["id"]

    page.goto(url_web)
    page.get_by_test_id(f"vacaciones-abrir-{fila_id}").click()
    page.get_by_test_id("vacaciones-fecha-inicio").fill("2026-07-06")
    page.get_by_test_id("vacaciones-fecha-fin").fill("2026-07-10")
    page.get_by_test_id("vacaciones-enviar").click()

    expect(page.get_by_test_id("vacaciones-mensaje")).to_have_text(
        "Solicitud registrada: 5 días hábiles. Te quedan 7 días hábiles en 2026."
    )


def test_cp_04_calculo_excluye_fines_de_semana_y_festivos(
    page: Page, url_api: str, url_web: str
) -> None:
    """CP-04: el cálculo de días hábiles excluye fines de semana y festivos oficiales."""
    empleado = _crear_empleado(url_api, fecha_ingreso="2020-01-15")
    fila_id = empleado["id"]

    page.goto(url_web)
    page.get_by_test_id(f"vacaciones-abrir-{fila_id}").click()
    page.get_by_test_id("vacaciones-fecha-inicio").fill("2026-12-21")
    page.get_by_test_id("vacaciones-fecha-fin").fill("2026-12-31")
    page.get_by_test_id("vacaciones-enviar").click()

    expect(page.get_by_test_id("vacaciones-mensaje")).to_have_text(
        "Solicitud registrada: 8 días hábiles. Te quedan 4 días hábiles en 2026."
    )
