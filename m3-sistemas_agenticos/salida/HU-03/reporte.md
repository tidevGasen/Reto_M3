# Reporte · HU-03

**Estado:** ESCALAR A UNA PERSONA
**Costo de agentes:** 1.84 USD
**Ciclos de corrección:** 2

## Bitácora
- Filtro de historia: OK
- Criterios escritos en criterios.feature
- Preguntas abiertas: la persona respondió 'si'
- Casos de prueba escritos en casos_prueba.json
- Plan aprobado por una persona
- Construcción 1
- Verificación: OK
- Pruebas automatizadas: OK (12 casos)
- Despliegue: OK
- Despliegue y pruebas listos
- Pruebas E2E: 6 passed, 6 errors in 6.78s
- Triage → automatizador: El error ocurre en la fase de setup de Playwright, antes de ejecutar cualquier interacción con la aplicación: "BrowserType.launch: Executable doesn't exist at ...chrome-headless-shell.exe". Esto indica que los navegadores/binarios de Playwright no están instalados o no se completó su instalación en el entorno donde corren las pruebas, no un fallo de la aplicación ni del servidor.
- Pruebas corregidas
- Pruebas E2E: 3 failed, 9 passed, 1 warning in 46.79s
- Triage → desarrollador: La UI no muestra el formulario de edición/baja de empleado ni el elemento 'mensaje-exito' tras las acciones de editar y dar de baja; el 'main' permanece mostrando solo 'Registrar empleado', indicando que la aplicación no implementa o no renderiza correctamente el flujo de edición y baja descrito en los escenarios 'Editar el puesto y el departamento...' y 'Dar de baja a un empleado activo'.
- Código corregido; redespliegue OK
- Pruebas E2E: 1 failed, 11 passed, 1 warning in 14.51s

## Última ejecución de pruebas
```
1 failed, 11 passed, 1 warning in 14.51s
- tests.e2e.test_hu_03_e2e::test_cp_08_rechazar_departamento_invalido[chromium]
  playwright._impl._errors.TimeoutError: Locator.select_option: Timeout 5000ms exceeded.
Call log:
  - waiting for get_by_test_id("empleado-departamento")
    - locator resolved to <select required="" id="empleado-departamento" data-testid="empleado-departamento">…</select>
  - attempting select option action
    2 × waiting for element to be visible and enabled
      - did not find some options
   
```