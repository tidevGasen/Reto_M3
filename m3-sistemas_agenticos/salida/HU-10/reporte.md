# Reporte · HU-10

**Estado:** LISTA
**Costo de agentes:** 1.69 USD
**Ciclos de corrección:** 1

## Bitácora
- Filtro de historia: OK
- Criterios escritos en criterios.feature
- Preguntas abiertas: la persona respondió 'Si'
- Casos de prueba escritos en casos_prueba.json
- Plan aprobado por una persona
- Construcción 1
- Verificación: OK
- Pruebas automatizadas: OK (12 casos)
- Despliegue: OK
- Despliegue y pruebas listos
- Pruebas E2E: 1 failed, 23 passed, 1 warning in 27.12s
- Triage → automatizador: La prueba test_cp_08_rechazar_departamento_invalido intenta seleccionar una opción en el combo "empleado-departamento" que no existe en el DOM (select_option falla con 'did not find some options'). El select fue localizado y está visible/habilitado, pero el valor que la prueba intenta elegir para probar un departamento inválido no está presente entre las opciones reales del formulario, lo que indica un selector/valor incorrecto en el test, no un fallo de la aplicación ni de la infraestructura.
- Pruebas corregidas
- Pruebas E2E: 24 passed, 1 warning in 15.23s

## Última ejecución de pruebas
```
24 passed, 1 warning in 15.23s

```