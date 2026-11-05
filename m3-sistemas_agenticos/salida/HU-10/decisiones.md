# Decisiones · HU-10 (Solicitar vacaciones)

**Resultado:** Estado **LISTA** · 24 pruebas E2E pasando · 1 ciclo de corrección · 1.69 USD.

## Qué pasos son *workflow* (código decide) y cuáles *agente* (LLM decide)

| Paso | Tipo | Quién / qué |
|---|---|---|
| Enrutamiento del grafo (`construir_grafo`, `despues_de_*`) | **Workflow** | Supervisor determinista de LangGraph: decide el siguiente nodo |
| Filtro de seguridad de la historia | **Workflow** | `filtrar_historia` (clasifica y bloquea contenido no confiable) |
| Criterios de aceptación (Gherkin) | **Agente** | Analista |
| Casos de prueba (JSON) | **Agente** | Diseñador de pruebas |
| Plan de implementación | **Agente** | Desarrollador (modo planificar, solo lectura) |
| Código backend/frontend | **Agente** | Desarrollador (modo construir, Claude Code) |
| Despliegue en Docker | **Agente** | Agente de despliegue |
| Pruebas pytest + Playwright | **Agente** | Automatizador |
| Verificación (API, build, despliegue, pruebas) | **Workflow** | `flujos/verificacion.py` (determinista) |
| Diagnóstico de fallos | **Agente** | Triage (decide responsable; no corrige) |
| Elegir nodo de corrección y contar ciclos | **Workflow** | `despues_de_triage`, `MAX_CICLOS=2` |
| Aprobar el plan / escalar | **Human-in-the-loop** | `interrupt` + decisión de la persona |

Principio: **el agente propone, el validador (código) decide.** Toda salida de un agente pasa por
una verificación determinista antes de avanzar.

## Cómo se validó cada salida

| Salida | Validador (determinista) | Qué comprueba |
|---|---|---|
| `criterios.feature` | `validar_gherkin` + `preguntas_abiertas` | `# language: es`, `Característica:`, ≥2 escenarios, cada escenario con Dado/Cuando/Entonces |
| `casos_prueba.json` | Pydantic `PlanPruebas` + `validar_plan` | Esquema válido, cada escenario cubierto por ≥1 caso, ids únicos |
| Código (`app/backend`, `app/frontend`) | `verificar_app` | El backend arranca y responde `/api/salud`; `npm run build` sin errores |
| Despliegue | `verificar_despliegue` | Los contenedores responden en los puertos 8000/8080 |
| Comportamiento completo | `ejecutar_pruebas` (pytest + Playwright) | **Árbitro final**: 24/24 E2E en verde |

Verificación específica de HU-10: confirmé que los **8 mensajes de error exactos** y su **orden
de validación** (404 → 409 → 400 rango → cruce de año → año fuera de tabla → antigüedad → sin días
hábiles → tope anual) están en el backend, tal como los exige la calificación automática.

## Qué corregí (en los agentes / contexto / decisiones humanas)

1. **Preparación de contexto (lo más importante).** Los agentes leen archivos de nombre fijo y no
   siguen referencias solas. Fusioné `reglas_vacaciones.md` → `reglas_negocio.md` y
   `convenciones_vacaciones.md` → `convenciones_app.md` (que se copia como `app/CLAUDE.md`), para que
   el desarrollador, el diseñador y el automatizador recibieran de forma determinista los mensajes
   exactos y los `data-testid`. Sin esto, el desarrollador habría inventado los mensajes y fallado.
2. **Fix de portabilidad (reviewer/verificación).** `flujos/verificacion.py` → `_correr` usa
   `shell=True` en Windows: `npm` es `npm.cmd` y `CreateProcess` no lo resolvía (`WinError 2`), lo
   que rompía la verificación del frontend.
3. **Decisiones humanas durante el flujo (HITL).**
   - Preguntas abiertas: el analista reportó "Ninguna" → continué (`Si`).
   - Plan: lo revisé contra una checklist (no romper HU-01–03, dos endpoints, mensajes y orden
     exactos, `data-testid`) y lo aprobé.
   - Triage: validé que el único fallo (`test_cp_08_rechazar_departamento_invalido`) era un **test
     mal diseñado** (intentaba elegir una opción inexistente en el `<select>`), no un fallo de la app.
     El triage lo mandó al **automatizador**, que corrigió la prueba → 24/24 en verde.

## Reflexión

- **Qué funcionó:** preparar el contexto por adelantado volvió determinista lo que de otro modo
  dependía de que el modelo siguiera referencias; el resultado fue LISTA en un solo ciclo.
- **Qué mejoraría:** mover la fusión de contexto a código (que cada agente lea todo `contexto/`)
  para no depender de anexar manualmente; y usar `SqliteSaver` en vez de `InMemorySaver` para que
  una ejecución en pausa se retome entre procesos.
