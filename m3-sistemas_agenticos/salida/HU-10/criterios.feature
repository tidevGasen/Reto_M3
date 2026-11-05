# language: es
# Historia: HU-10 · Solicitar vacaciones
# Fuente: historias/HU-10-solicitar-vacaciones.md, contexto/reglas_negocio.md
#          (reglas y convenciones de vacaciones anexadas)

Característica: Solicitar vacaciones
  Como empleado de la empresa
  Quiero solicitar días de vacaciones indicando una fecha de inicio y una de fin
  Para que mi solicitud quede registrada y sepa cuántos días me quedan en el año

  Escenario: Solicitud válida que se registra y descuenta del saldo del año
    Dado que el empleado 7 está activo, con fecha_ingreso "2024-03-10" y 0 días hábiles usados en 2026
    Cuando solicita vacaciones del "2026-07-06" al "2026-07-10"
    Entonces la API responde 201 con "dias_habiles" igual a 5 y "dias_restantes" igual a 7
    Y la pantalla muestra en "vacaciones-mensaje" el texto "Solicitud registrada: 5 días hábiles. Te quedan 7 días hábiles en 2026."

  Escenario: El cálculo de días hábiles excluye fines de semana y festivos oficiales
    Dado que el empleado 3 está activo, con fecha_ingreso "2020-01-15" y 0 días hábiles usados en 2026
    Cuando solicita vacaciones del "2026-12-21" al "2026-12-31"
    Entonces la API responde 201 con "dias_habiles" igual a 8 y "dias_restantes" igual a 4
    Y la pantalla muestra en "vacaciones-mensaje" el texto "Solicitud registrada: 8 días hábiles. Te quedan 4 días hábiles en 2026."

  Escenario: Rechazo cuando el empleado no existe
    Dado que no existe ningún empleado con id 9999
    Cuando solicita vacaciones del "2026-07-06" al "2026-07-10" para el empleado 9999
    Entonces la API responde 404 con "detail" igual a "Empleado no encontrado"

  Escenario: Rechazo cuando el empleado está dado de baja
    Dado que el empleado 5 está en estado "baja", con fecha_ingreso "2020-01-10"
    Cuando solicita vacaciones del "2026-07-06" al "2026-07-10"
    Entonces la API responde 409 con "detail" igual a "No se pueden solicitar vacaciones para un empleado dado de baja"

  Escenario: Rechazo cuando la fecha de fin es anterior a la fecha de inicio
    Dado que el empleado 7 está activo, con fecha_ingreso "2024-03-10"
    Cuando solicita vacaciones del "2026-07-10" al "2026-07-06"
    Entonces la API responde 400 con "detail" igual a "La fecha de fin no puede ser anterior a la fecha de inicio"

  Escenario: Rechazo cuando el periodo cruza de un año a otro
    Dado que el empleado 7 está activo, con fecha_ingreso "2024-03-10"
    Cuando solicita vacaciones del "2026-12-28" al "2027-01-08"
    Entonces la API responde 400 con "detail" igual a "Las vacaciones deben estar dentro de un mismo año calendario"

  Escenario: Rechazo cuando el año no está en la tabla de festivos
    Dado que el empleado 7 está activo, con fecha_ingreso "2024-03-10"
    Cuando solicita vacaciones del "2025-07-06" al "2025-07-10"
    Entonces la API responde 400 con "detail" igual a "Solo se pueden solicitar vacaciones en 2026 y 2027"

  Escenario: Rechazo por antigüedad insuficiente (Regla 1)
    Dado que el empleado 8 está activo, con fecha_ingreso "2025-12-21"
    Cuando solicita vacaciones del "2026-12-18" al "2026-12-19"
    Entonces la API responde 400 con "detail" igual a "Se requiere al menos un año de antigüedad a la fecha de inicio"

  Escenario: Rechazo cuando el periodo no incluye ningún día hábil (Regla 3)
    Dado que el empleado 7 está activo, con fecha_ingreso "2024-03-10"
    Cuando solicita vacaciones del "2026-07-11" al "2026-07-12"
    Entonces la API responde 400 con "detail" igual a "El periodo no incluye días hábiles"

  Escenario: Rechazo cuando la solicitud rebasa los días disponibles del año (Regla 2)
    Dado que el empleado 9 está activo, con fecha_ingreso "2020-01-01" y 4 días hábiles usados en 2026
    Cuando solicita vacaciones del "2026-11-02" al "2026-11-12"
    Entonces la API responde 400 con "detail" igual a "La solicitud excede los días disponibles: quedan 8 días hábiles"

# Preguntas abiertas
# Ninguna: la historia, las reglas y las convenciones (reglas_vacaciones.md y
# convenciones_vacaciones.md) cubren todos los casos listados en el resumen de
# criterios de aceptación de HU-10 con datos y mensajes exactos.
