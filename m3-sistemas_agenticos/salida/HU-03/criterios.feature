# language: es
Característica: Editar y dar de baja a un empleado
  Como persona del área de Recursos Humanos
  Quiero cambiar el puesto y el departamento de un empleado, y poder darlo de baja
  Para mantener el directorio al día sin perder el historial

  Escenario: Editar el puesto y el departamento de un empleado activo
    Dado que existe un empleado activo con número "EMP-0010", correo "ana.lopez@empresa.com", puesto "Analista Junior" y departamento "Ventas"
    Cuando edito al empleado "EMP-0010" con puesto "Analista Senior" y departamento "Finanzas"
    Entonces el sistema responde 200 con el empleado actualizado
    Y el empleado "EMP-0010" muestra puesto "Analista Senior" y departamento "Finanzas"
    Y el empleado "EMP-0010" conserva el número de empleado "EMP-0010" y el correo "ana.lopez@empresa.com"

  Escenario: Dar de baja a un empleado activo
    Dado que existe un empleado activo con número "EMP-0011", fecha_ingreso "2022-03-01" y estado "activo"
    Cuando doy de baja al empleado "EMP-0011" con fecha_baja "2024-06-15"
    Entonces el sistema responde 200 con el empleado actualizado
    Y el empleado "EMP-0011" tiene estado "baja" y fecha_baja "2024-06-15"
    Y el empleado "EMP-0011" sigue apareciendo en el directorio

  Esquema del escenario: Rechazar la edición cuando el puesto o el departamento no son válidos
    Dado que existe un empleado activo con número "EMP-0012", puesto "Coordinador" y departamento "Operaciones"
    Cuando edito al empleado "EMP-0012" con puesto "<puesto>" y departamento "<departamento>"
    Entonces el sistema responde 422
    Y la pantalla indica que el campo "<campo_invalido>" debe corregirse

    Ejemplos:
      | puesto         | departamento  | campo_invalido |
      | A              | Operaciones   | puesto         |
      | Coordinador    | Marketing     | departamento   |

  Escenario: Rechazar la edición de un empleado dado de baja
    Dado que existe un empleado con número "EMP-0013", estado "baja" y fecha_baja "2024-01-10"
    Cuando edito al empleado "EMP-0013" con puesto "Supervisor" y departamento "Tecnología"
    Entonces el sistema responde 409 con el mensaje "No se puede editar a un empleado dado de baja"
    Y el empleado "EMP-0013" conserva su puesto y departamento originales

  Escenario: Rechazar una fecha de baja anterior a la fecha de ingreso
    Dado que existe un empleado activo con número "EMP-0014" y fecha_ingreso "2023-05-01"
    Cuando doy de baja al empleado "EMP-0014" con fecha_baja "2023-04-20"
    Entonces el sistema responde 422
    Y la pantalla indica que el campo "fecha_baja" debe corregirse

# Preguntas abiertas
# - La HU indica que el número de empleado y el correo no se editan, pero no dice qué debe
#   responder la API si el cliente intenta enviarlos en la solicitud de edición (¿se ignoran
#   silenciosamente, responden 422 o 409?). Se asumió que se conservan sin generar error.
# - No hay una regla explícita sobre si se puede volver a dar de baja a un empleado que ya
#   está en estado "baja", ni qué respuesta debería dar el sistema en ese caso.
# - No se especifica el mensaje exacto de error para una fecha de baja anterior a la fecha de
#   ingreso (se usó el patrón general de la regla 3: 422 e indicar el campo a corregir).
