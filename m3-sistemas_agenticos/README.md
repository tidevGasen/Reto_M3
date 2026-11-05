# Fábrica de software con agentes · Módulo 3

Una cadena de seis agentes que convierte una historia de usuario en una aplicación de gestión de empleados desplegada y probada:

| # | Agente | Entrada | Salida | Sesión |
| --- | --- | --- | --- | --- |
| 1 | Analista | Historia de usuario | `salida/HU-xx/criterios.feature` | 1 |
| 2 | Diseñador de pruebas | Criterios | `salida/HU-xx/casos_prueba.json` | 1 |
| 3 | Desarrollador (Claude Code) | Criterios y casos | `app/backend`, `app/frontend` | 2 |
| 4 | Despliegue (Claude Code) | Código | Contenedores con Docker Compose | 3 |
| 5 | Automatizador (Claude Code) | Casos de prueba | `app/tests` (pytest + Playwright) | 3 |
| 6 | Flujo E2E con triage | Pruebas y app desplegada | `salida/HU-xx/reporte.md` | 4 |

El orquestador (LangGraph) encadena los agentes en el flujo
**spec → plan → código → tests → revisión**, con aprobación humana del plan (HITL),
un máximo de ciclos de corrección y una capa de seguridad que trata la historia como
contenido no confiable. Ver [`salida/seguridad.md`](salida/seguridad.md).

## Requisitos

Python 3.12, Node 20 o superior, Docker Desktop, Claude Code y una clave de API de Anthropic con créditos.

## Setup

### Mac / Linux

```bash
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
playwright install chromium
cp .env.example .env        # escribe ANTHROPIC_API_KEY y MODEL
```

### Windows (PowerShell)

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
Copy-Item .env.example .env   # escribe ANTHROPIC_API_KEY y MODEL
setx PYTHONUTF8 1             # una sola vez; cierra y reabre la terminal
```

> Si PowerShell no deja activar el entorno:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` (una vez).
> `uv` también funciona en Windows si lo tienes instalado (`uv venv`); el bloque de arriba usa
> solo Python estándar para no depender de él.

## Uso

Todo se ejecuta **desde la raíz del repositorio**, con el entorno activado y Docker Desktop abierto.

### Mac / Linux

```bash
# Agentes por separado (sesión 1)
python -m agentes.analista historias/HU-01-registrar-empleado.md
python -m agentes.disenador_pruebas salida/HU-01/criterios.feature

# La fábrica completa (sesiones 2 a 4)
python -m flujos.flujo_s2 historias/HU-01-registrar-empleado.md
python -m flujos.flujo_s3 historias/HU-01-registrar-empleado.md
python -m flujos.flujo_s4 historias/HU-10-solicitar-vacaciones.md
```

### Windows (PowerShell)

```powershell
python -m agentes.analista historias\HU-01-registrar-empleado.md
python -m agentes.disenador_pruebas salida\HU-01\criterios.feature

python -m flujos.flujo_s4 historias\HU-10-solicitar-vacaciones.md
```

Durante el flujo `flujo_s4` hay dos pausas humanas: responder las preguntas abiertas y
aprobar el plan (escribe `si`, o comentarios para que el desarrollador lo ajuste).

La aplicación queda en http://localhost:8080 y la documentación de la API en http://localhost:8000/docs.

## Pruebas

Las pruebas las genera el automatizador en `app/tests/` (API con `httpx`, E2E con Playwright) y
las ejecuta el flujo contra la app desplegada. Para correrlas a mano:

### Mac / Linux

```bash
cd app
URL_API=http://localhost:8000 URL_WEB=http://localhost:8080 python -m pytest tests -q
```

### Windows (PowerShell)

```powershell
cd app
$env:URL_API="http://localhost:8000"; $env:URL_WEB="http://localhost:8080"
python -m pytest tests -q
```

> Las pruebas E2E necesitan la app desplegada (`docker compose up -d --build` desde `app/`).
> Solo colectar sin ejecutar: `python -m pytest tests --collect-only -q`.

## Ejemplos

Los patrones de cada sesión tienen un ejemplo corto y ejecutable en
[`ejemplos/`](ejemplos/README.md), por ejemplo `python -m ejemplos.s2_flujos.enrutamiento`.

## Estructura

- `historias/` — historias de usuario de entrada (HU-01 a HU-03, HU-10; HU-99 es la historia de ataque)
- `contexto/` — reglas de negocio y convenciones de la app que los agentes leen como contexto
- `agentes/` — los seis agentes y el bucle base
- `flujos/` — el orquestador LangGraph (una versión por sesión) y las verificaciones deterministas
- `seguridad/hooks.py` — hooks de rol y de seguridad para Claude Code
- `app/` — la aplicación que generan los agentes; `salida/` — artefactos por historia
- Más detalles de convenciones y seguridad en [`CLAUDE.md`](CLAUDE.md) y [`CHANGELOG.md`](CHANGELOG.md).
