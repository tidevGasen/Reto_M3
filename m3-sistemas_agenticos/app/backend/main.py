"""API de gestión de empleados."""

from datetime import date

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import func, select
from sqlalchemy.orm import Session

import vacaciones as reglas_vacaciones
from database import Base, engine, obtener_sesion
from models import Empleado, Vacacion
from schemas import (
    Departamento,
    EmpleadoActualizar,
    EmpleadoBaja,
    EmpleadoCrear,
    EmpleadoRespuesta,
    VacacionCrear,
    VacacionRespuesta,
    VacacionSaldo,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gestión de empleados")


@app.exception_handler(RequestValidationError)
async def manejar_error_validacion(request: Request, excepcion: RequestValidationError):
    primer_error = excepcion.errors()[0]
    campo = primer_error["loc"][-1]
    mensaje = primer_error.get("msg", "valor inválido")
    prefijo = "Value error, "
    if mensaje.startswith(prefijo):
        # Los field_validator con mensajes propios ya están en español y completos.
        return JSONResponse(status_code=422, content={"detail": mensaje[len(prefijo) :]})
    return JSONResponse(
        status_code=422,
        content={"detail": f"El campo '{campo}' es inválido: {mensaje}"},
    )


@app.get("/api/salud")
def salud():
    return {"estado": "ok"}


@app.get("/api/departamentos")
def listar_departamentos():
    return [d.value for d in Departamento]


def _siguiente_numero_empleado(sesion: Session) -> str:
    total = sesion.scalar(select(func.count()).select_from(Empleado)) or 0
    return f"EMP-{total + 1:04d}"


def _obtener_empleado_o_404(sesion: Session, numero_empleado: str) -> Empleado:
    empleado = sesion.scalar(select(Empleado).where(Empleado.numero_empleado == numero_empleado))
    if empleado is None:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return empleado


@app.post("/api/empleados", response_model=EmpleadoRespuesta, status_code=201)
def crear_empleado(datos: EmpleadoCrear, sesion: Session = Depends(obtener_sesion)):
    existe = sesion.scalar(select(Empleado).where(func.lower(Empleado.correo) == datos.correo))
    if existe is not None:
        raise HTTPException(status_code=409, detail="El correo ya está registrado")

    empleado = Empleado(
        numero_empleado=_siguiente_numero_empleado(sesion),
        nombre=datos.nombre,
        correo=datos.correo,
        puesto=datos.puesto,
        departamento=datos.departamento.value,
        fecha_ingreso=datos.fecha_ingreso,
        estado="activo",
    )
    sesion.add(empleado)
    sesion.commit()
    sesion.refresh(empleado)
    return empleado


@app.get("/api/empleados", response_model=list[EmpleadoRespuesta])
def listar_empleados(sesion: Session = Depends(obtener_sesion)):
    return list(sesion.scalars(select(Empleado).order_by(Empleado.id)))


@app.put("/api/empleados/{numero_empleado}", response_model=EmpleadoRespuesta)
def editar_empleado(
    numero_empleado: str, datos: EmpleadoActualizar, sesion: Session = Depends(obtener_sesion)
):
    empleado = _obtener_empleado_o_404(sesion, numero_empleado)
    if empleado.estado == "baja":
        raise HTTPException(status_code=409, detail="No se puede editar a un empleado dado de baja")

    empleado.puesto = datos.puesto
    empleado.departamento = datos.departamento.value
    sesion.commit()
    sesion.refresh(empleado)
    return empleado


@app.patch("/api/empleados/{numero_empleado}/baja", response_model=EmpleadoRespuesta)
def dar_de_baja(numero_empleado: str, datos: EmpleadoBaja, sesion: Session = Depends(obtener_sesion)):
    empleado = _obtener_empleado_o_404(sesion, numero_empleado)
    if datos.fecha_baja < empleado.fecha_ingreso:
        raise HTTPException(
            status_code=422,
            detail="El campo 'fecha_baja' es inválido: no puede ser anterior a la fecha de ingreso",
        )

    empleado.estado = "baja"
    empleado.fecha_baja = datos.fecha_baja
    sesion.commit()
    sesion.refresh(empleado)
    return empleado


def _obtener_empleado_por_id_o_404(sesion: Session, empleado_id: int) -> Empleado:
    empleado = sesion.get(Empleado, empleado_id)
    if empleado is None:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return empleado


def _dias_usados_en_anio(sesion: Session, empleado_id: int, anio: int) -> int:
    solicitudes = sesion.scalars(
        select(Vacacion).where(
            Vacacion.empleado_id == empleado_id,
            func.strftime("%Y", Vacacion.fecha_inicio) == str(anio),
        )
    )
    return sum(solicitud.dias_habiles for solicitud in solicitudes)


@app.post(
    "/api/empleados/{empleado_id}/vacaciones", response_model=VacacionRespuesta, status_code=201
)
def solicitar_vacaciones(
    empleado_id: int, datos: VacacionCrear, sesion: Session = Depends(obtener_sesion)
):
    empleado = _obtener_empleado_por_id_o_404(sesion, empleado_id)
    if empleado.estado == "baja":
        raise HTTPException(
            status_code=409,
            detail="No se pueden solicitar vacaciones para un empleado dado de baja",
        )
    if datos.fecha_fin < datos.fecha_inicio:
        raise HTTPException(
            status_code=400, detail="La fecha de fin no puede ser anterior a la fecha de inicio"
        )
    if datos.fecha_inicio.year != datos.fecha_fin.year:
        raise HTTPException(
            status_code=400, detail="Las vacaciones deben estar dentro de un mismo año calendario"
        )
    anio = datos.fecha_inicio.year
    if not reglas_vacaciones.anio_valido(anio):
        raise HTTPException(
            status_code=400, detail="Solo se pueden solicitar vacaciones en 2026 y 2027"
        )
    if not reglas_vacaciones.cumple_antiguedad(empleado.fecha_ingreso, datos.fecha_inicio):
        raise HTTPException(
            status_code=400,
            detail="Se requiere al menos un año de antigüedad a la fecha de inicio",
        )
    dias_habiles = reglas_vacaciones.contar_dias_habiles(datos.fecha_inicio, datos.fecha_fin)
    if dias_habiles == 0:
        raise HTTPException(status_code=400, detail="El periodo no incluye días hábiles")

    dias_usados = _dias_usados_en_anio(sesion, empleado_id, anio)
    dias_disponibles = reglas_vacaciones.DIAS_POR_ANIO - dias_usados
    if dias_habiles > dias_disponibles:
        raise HTTPException(
            status_code=400,
            detail=f"La solicitud excede los días disponibles: quedan {dias_disponibles} días hábiles",
        )

    solicitud = Vacacion(
        empleado_id=empleado_id,
        fecha_inicio=datos.fecha_inicio,
        fecha_fin=datos.fecha_fin,
        dias_habiles=dias_habiles,
    )
    sesion.add(solicitud)
    sesion.commit()
    sesion.refresh(solicitud)

    return VacacionRespuesta(
        id=solicitud.id,
        empleado_id=solicitud.empleado_id,
        fecha_inicio=solicitud.fecha_inicio,
        fecha_fin=solicitud.fecha_fin,
        dias_habiles=solicitud.dias_habiles,
        dias_restantes=dias_disponibles - dias_habiles,
    )


@app.get("/api/empleados/{empleado_id}/vacaciones", response_model=VacacionSaldo)
def consultar_saldo_vacaciones(
    empleado_id: int, anio: int | None = None, sesion: Session = Depends(obtener_sesion)
):
    _obtener_empleado_por_id_o_404(sesion, empleado_id)
    anio_consulta = anio if anio is not None else date.today().year

    solicitudes = list(
        sesion.scalars(
            select(Vacacion)
            .where(
                Vacacion.empleado_id == empleado_id,
                func.strftime("%Y", Vacacion.fecha_inicio) == str(anio_consulta),
            )
            .order_by(Vacacion.fecha_inicio)
        )
    )
    dias_usados = sum(solicitud.dias_habiles for solicitud in solicitudes)

    return VacacionSaldo(
        empleado_id=empleado_id,
        anio=anio_consulta,
        dias_usados=dias_usados,
        dias_disponibles=reglas_vacaciones.DIAS_POR_ANIO - dias_usados,
        solicitudes=solicitudes,
    )
