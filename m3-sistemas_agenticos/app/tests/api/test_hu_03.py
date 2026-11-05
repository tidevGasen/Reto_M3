"""Pruebas de API para HU-03: edición y baja de empleados."""

import uuid

import httpx


def _datos_empleado(**overrides: object) -> dict:
    datos = {
        "nombre": "Empleada de Prueba",
        "correo": f"hu03.{uuid.uuid4().hex[:8]}@empresa.com",
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


def test_cp_01_editar_puesto_y_departamento_empleado_activo(url_api: str) -> None:
    """CP-01: editar el puesto y el departamento de un empleado activo."""
    empleado = _crear_empleado(url_api, puesto="Analista Junior", departamento="Ventas")

    respuesta = httpx.put(
        f"{url_api}/api/empleados/{empleado['numero_empleado']}",
        json={"puesto": "Analista Senior", "departamento": "Finanzas"},
    )

    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert cuerpo["puesto"] == "Analista Senior"
    assert cuerpo["departamento"] == "Finanzas"
    assert cuerpo["numero_empleado"] == empleado["numero_empleado"]
    assert cuerpo["correo"] == empleado["correo"]


def test_cp_03_dar_de_baja_empleado_activo(url_api: str) -> None:
    """CP-03: dar de baja a un empleado activo."""
    empleado = _crear_empleado(url_api, fecha_ingreso="2022-03-01")

    respuesta = httpx.patch(
        f"{url_api}/api/empleados/{empleado['numero_empleado']}/baja",
        json={"fecha_baja": "2024-06-15"},
    )

    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert cuerpo["estado"] == "baja"
    assert cuerpo["fecha_baja"] == "2024-06-15"

    lista = httpx.get(f"{url_api}/api/empleados")
    assert lista.status_code == 200
    numeros = [e["numero_empleado"] for e in lista.json()]
    assert empleado["numero_empleado"] in numeros


def test_cp_05_rechazar_puesto_invalido(url_api: str) -> None:
    """CP-05: rechazar la edición cuando el puesto no es válido."""
    empleado = _crear_empleado(url_api, puesto="Coordinador", departamento="Operaciones")

    respuesta = httpx.put(
        f"{url_api}/api/empleados/{empleado['numero_empleado']}",
        json={"puesto": "A", "departamento": "Operaciones"},
    )

    assert respuesta.status_code == 422
    assert "puesto" in respuesta.json()["detail"]


def test_cp_07_rechazar_departamento_invalido(url_api: str) -> None:
    """CP-07: rechazar la edición cuando el departamento no es válido."""
    empleado = _crear_empleado(url_api, puesto="Coordinador", departamento="Operaciones")

    respuesta = httpx.put(
        f"{url_api}/api/empleados/{empleado['numero_empleado']}",
        json={"puesto": "Coordinador", "departamento": "Marketing"},
    )

    assert respuesta.status_code == 422
    assert "departamento" in respuesta.json()["detail"]


def test_cp_09_rechazar_edicion_empleado_de_baja(url_api: str) -> None:
    """CP-09: rechazar la edición de un empleado dado de baja."""
    empleado = _crear_empleado(url_api, puesto="Supervisor Jr", departamento="Ventas")
    baja = httpx.patch(
        f"{url_api}/api/empleados/{empleado['numero_empleado']}/baja",
        json={"fecha_baja": "2024-01-10"},
    )
    assert baja.status_code == 200

    respuesta = httpx.put(
        f"{url_api}/api/empleados/{empleado['numero_empleado']}",
        json={"puesto": "Supervisor", "departamento": "Tecnología"},
    )

    assert respuesta.status_code == 409
    assert respuesta.json()["detail"] == "No se puede editar a un empleado dado de baja"

    lista = httpx.get(f"{url_api}/api/empleados")
    actual = next(
        e for e in lista.json() if e["numero_empleado"] == empleado["numero_empleado"]
    )
    assert actual["puesto"] == "Supervisor Jr"
    assert actual["departamento"] == "Ventas"


def test_cp_11_rechazar_fecha_baja_anterior_a_ingreso(url_api: str) -> None:
    """CP-11: rechazar una fecha de baja anterior a la fecha de ingreso."""
    empleado = _crear_empleado(url_api, fecha_ingreso="2023-05-01")

    respuesta = httpx.patch(
        f"{url_api}/api/empleados/{empleado['numero_empleado']}/baja",
        json={"fecha_baja": "2023-04-20"},
    )

    assert respuesta.status_code == 422
    assert "fecha_baja" in respuesta.json()["detail"]
