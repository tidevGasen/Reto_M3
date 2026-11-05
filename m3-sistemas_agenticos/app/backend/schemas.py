"""Esquemas Pydantic para validar entradas y salidas de la API."""

from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Departamento(str, Enum):
    TECNOLOGIA = "Tecnología"
    VENTAS = "Ventas"
    FINANZAS = "Finanzas"
    RECURSOS_HUMANOS = "Recursos Humanos"
    OPERACIONES = "Operaciones"


class EmpleadoCrear(BaseModel):
    nombre: str = Field(min_length=2, max_length=80)
    correo: str
    puesto: str = Field(min_length=2, max_length=60)
    departamento: Departamento
    fecha_ingreso: date

    @field_validator("fecha_ingreso")
    @classmethod
    def validar_fecha_ingreso(cls, valor: date) -> date:
        if valor > date.today():
            raise ValueError("La fecha de ingreso no puede ser futura")
        return valor

    @field_validator("correo")
    @classmethod
    def validar_correo_corporativo(cls, valor: str) -> str:
        if not valor.lower().endswith("@empresa.com"):
            raise ValueError("Usa el correo corporativo @empresa.com")
        return valor.lower()


class EmpleadoActualizar(BaseModel):
    """Solo puesto y departamento son editables; otros campos enviados se ignoran."""

    model_config = ConfigDict(extra="ignore")

    puesto: str = Field(min_length=2, max_length=60)
    departamento: Departamento


class EmpleadoBaja(BaseModel):
    fecha_baja: date


class EmpleadoRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    numero_empleado: str
    nombre: str
    correo: str
    puesto: str
    departamento: str
    fecha_ingreso: date
    estado: str
    fecha_baja: date | None
    creado_en: datetime


class VacacionCrear(BaseModel):
    fecha_inicio: date
    fecha_fin: date


class VacacionRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    empleado_id: int
    fecha_inicio: date
    fecha_fin: date
    dias_habiles: int
    dias_restantes: int


class VacacionResumen(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha_inicio: date
    fecha_fin: date
    dias_habiles: int


class VacacionSaldo(BaseModel):
    empleado_id: int
    anio: int
    dias_usados: int
    dias_disponibles: int
    solicitudes: list[VacacionResumen]
