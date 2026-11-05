"""Configuración de la base de datos SQLite con SQLAlchemy."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATOS_DIR = os.path.join(os.path.dirname(__file__), "datos")
os.makedirs(DATOS_DIR, exist_ok=True)

RUTA_BASE_DATOS = os.path.join(DATOS_DIR, "empleados.db")
URL_BASE_DATOS = f"sqlite:///{RUTA_BASE_DATOS}"

engine = create_engine(URL_BASE_DATOS, connect_args={"check_same_thread": False})
SesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def obtener_sesion():
    sesion = SesionLocal()
    try:
        yield sesion
    finally:
        sesion.close()
