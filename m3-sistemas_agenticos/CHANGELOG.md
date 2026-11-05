# Changelog

Formato: `fecha · versión · resumen`. Registra los cambios relevantes a los agentes,
validadores, hooks y flujo de la fábrica.

## 2026-11-04 · v1.1.0 · Reto HU-10 (Solicitar vacaciones)

- **Contexto (HU-10).** Se agregó la historia `historias/HU-10-solicitar-vacaciones.md` y sus
  archivos de contexto `contexto/reglas_vacaciones.md` y `contexto/convenciones_vacaciones.md`.
- **Preparación de contexto.** Para que los seis agentes reciban de forma determinista los
  **mensajes de error exactos**, el **orden de validación** y los `data-testid`, el contenido de
  vacaciones se fusionó en los archivos canónicos que los agentes ya leen:
  - `reglas_vacaciones.md` → anexado a `contexto/reglas_negocio.md` (lo lee el analista y el desarrollador).
  - `convenciones_vacaciones.md` → anexado a `contexto/convenciones_app.md` (se copia como `app/CLAUDE.md`,
    lo leen el desarrollador y el automatizador).
  - Motivo: los agentes leen nombres de archivo fijos y no siguen referencias automáticamente; sin
    esta fusión, el desarrollador no vería los mensajes exactos y fallaría la calificación automática.

## 2026-10-31 · v1.0.1 · Portabilidad a Windows

- **Fix (`flujos/verificacion.py`).** `_correr()` ahora usa `shell=True` en Windows
  (`shell=(os.name == "nt")`). En Windows `npm` es `npm.cmd` (un script batch) y `CreateProcess`
  no lo resuelve sin shell, lo que provocaba `FileNotFoundError: [WinError 2]` al verificar el
  frontend (`npm install` / `npm run build`). En Mac/Linux el comportamiento no cambia.

## Base (Labs 1–4) · v1.0.0

- Fábrica de seis agentes (analista, diseñador de pruebas, desarrollador, despliegue,
  automatizador, triage) orquestada con LangGraph; flujos `flujo_s2`, `flujo_s3`, `flujo_s4`.
- Validadores deterministas: Gherkin (`validar_gherkin`), casos de prueba (Pydantic `PlanPruebas`),
  verificación de app y pruebas (`flujos/verificacion.py`).
- Capa de seguridad: `filtrar_historia`, prompt hardening, hooks de rol y de seguridad
  (`seguridad/hooks.py`), auditoría en `auditoria.jsonl`.
- Historias HU-01 a HU-03 procesadas; HU-99 como historia de ataque para la demo de seguridad.
