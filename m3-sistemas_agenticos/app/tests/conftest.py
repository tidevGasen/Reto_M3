"""Fixtures compartidas para las pruebas de la aplicación de empleados."""

import os

import pytest


@pytest.fixture
def url_api() -> str:
    """URL base de la API."""
    return os.environ.get("URL_API", "http://localhost:8000")


@pytest.fixture
def url_web() -> str:
    """URL base del front-end."""
    return os.environ.get("URL_WEB", "http://localhost:8080")
