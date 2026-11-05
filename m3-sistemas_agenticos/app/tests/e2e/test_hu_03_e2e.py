"""Pruebas end-to-end para HU-03: edición y baja de empleados."""

import uuid

import httpx
from playwright.sync_api import Page, expect


def _datos_empleado(**overrides: object) -> dict:
    datos = {
        "nombre": "Empleada de Prueba",
        "correo": f"hu03e2e.{uuid.uuid4().hex[:8]}@empresa.com",
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


def test_cp_02_editar_puesto_y_departamento_empleado_activo(
    page: Page, url_api: str, url_web: str
) -> None:
    """CP-02: editar el puesto y el departamento de un empleado activo."""
    empleado = _crear_empleado(url_api, puesto="Analista Junior", departamento="Ventas")
    fila_id = empleado["id"]

    page.goto(url_web)
    page.get_by_test_id(f"editar-empleado-{fila_id}").click()
    page.get_by_test_id("empleado-puesto").fill("Analista Senior")
    page.get_by_test_id("empleado-departamento").select_option("Finanzas")
    page.get_by_test_id("empleado-guardar").click()

    expect(page.get_by_test_id("mensaje-exito")).to_be_visible()
    fila = page.get_by_test_id(f"fila-empleado-{fila_id}")
    expect(fila).to_contain_text("Analista Senior")
    expect(fila).to_contain_text("Finanzas")
    expect(page.get_by_test_id(f"numero-empleado-{fila_id}")).to_have_text(
        empleado["numero_empleado"]
    )


def test_cp_04_dar_de_baja_empleado_activo(page: Page, url_api: str, url_web: str) -> None:
    """CP-04: dar de baja a un empleado activo."""
    empleado = _crear_empleado(url_api)
    fila_id = empleado["id"]

    page.goto(url_web)
    page.get_by_test_id(f"baja-empleado-{fila_id}").click()
    page.get_by_test_id("empleado-fecha-baja").fill("2024-06-15")
    page.get_by_test_id("confirmar-baja").click()

    expect(page.get_by_test_id("mensaje-exito")).to_be_visible()
    expect(page.get_by_test_id(f"estado-empleado-{fila_id}")).to_have_text("Baja")
    expect(page.get_by_test_id(f"fila-empleado-{fila_id}")).to_be_visible()


def test_cp_06_rechazar_puesto_invalido(page: Page, url_api: str, url_web: str) -> None:
    """CP-06: rechazar la edición cuando el puesto no es válido."""
    empleado = _crear_empleado(url_api, puesto="Coordinador", departamento="Operaciones")
    fila_id = empleado["id"]

    page.goto(url_web)
    page.get_by_test_id(f"editar-empleado-{fila_id}").click()
    page.get_by_test_id("empleado-puesto").fill("A")
    page.get_by_test_id("empleado-departamento").select_option("Operaciones")
    page.get_by_test_id("empleado-guardar").click()

    mensaje_error = page.get_by_test_id("mensaje-error")
    expect(mensaje_error).to_be_visible()
    expect(mensaje_error).to_contain_text("puesto")


def test_cp_08_rechazar_departamento_invalido(page: Page, url_api: str, url_web: str) -> None:
    """CP-08: el formulario de edición no ofrece un departamento inválido para elegir."""
    empleado = _crear_empleado(url_api, puesto="Coordinador", departamento="Operaciones")
    fila_id = empleado["id"]

    page.goto(url_web)
    page.get_by_test_id(f"editar-empleado-{fila_id}").click()

    opciones = page.get_by_test_id("empleado-departamento").locator("option").all_inner_texts()
    assert "Marketing" not in opciones


def test_cp_10_rechazar_edicion_empleado_de_baja(page: Page, url_api: str, url_web: str) -> None:
    """CP-10: rechazar la edición de un empleado dado de baja."""
    empleado = _crear_empleado(url_api, puesto="Supervisor Jr", departamento="Ventas")
    _dar_de_baja(url_api, empleado["numero_empleado"], "2024-01-10")
    fila_id = empleado["id"]

    page.goto(url_web)
    page.get_by_test_id(f"editar-empleado-{fila_id}").click()
    page.get_by_test_id("empleado-puesto").fill("Supervisor")
    page.get_by_test_id("empleado-departamento").select_option("Tecnología")
    page.get_by_test_id("empleado-guardar").click()

    mensaje_error = page.get_by_test_id("mensaje-error")
    expect(mensaje_error).to_be_visible()
    expect(mensaje_error).to_contain_text("No se puede editar a un empleado dado de baja")

    page.get_by_role("button", name="Cancelar").click()
    fila = page.get_by_test_id(f"fila-empleado-{fila_id}")
    expect(page.get_by_test_id(f"estado-empleado-{fila_id}")).to_have_text("Baja")
    expect(fila).to_contain_text("Supervisor Jr")
    expect(fila).to_contain_text("Ventas")


def test_cp_12_rechazar_fecha_baja_anterior_a_ingreso(
    page: Page, url_api: str, url_web: str
) -> None:
    """CP-12: rechazar una fecha de baja anterior a la fecha de ingreso."""
    empleado = _crear_empleado(url_api, fecha_ingreso="2023-05-01")
    fila_id = empleado["id"]

    page.goto(url_web)
    page.get_by_test_id(f"baja-empleado-{fila_id}").click()
    page.get_by_test_id("empleado-fecha-baja").fill("2023-04-20")
    page.get_by_test_id("confirmar-baja").click()

    mensaje_error = page.get_by_test_id("mensaje-error")
    expect(mensaje_error).to_be_visible()
    expect(mensaje_error).to_contain_text("fecha_baja")
