export default function TablaEmpleados({ empleados, onEditar, onDarDeBaja, onSolicitarVacaciones }) {
  return (
    <table data-testid="tabla-empleados">
      <thead>
        <tr>
          <th>Número</th>
          <th>Nombre</th>
          <th>Correo</th>
          <th>Puesto</th>
          <th>Departamento</th>
          <th>Estado</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        {empleados.map((empleado) => (
          <tr key={empleado.id} data-testid={`fila-empleado-${empleado.id}`}>
            <td data-testid={`numero-empleado-${empleado.id}`}>{empleado.numero_empleado}</td>
            <td>{empleado.nombre}</td>
            <td>{empleado.correo}</td>
            <td>{empleado.puesto}</td>
            <td>{empleado.departamento}</td>
            <td data-testid={`estado-empleado-${empleado.id}`}>
              {empleado.estado === "activo" ? "Activo" : "Baja"}
            </td>
            <td>
              <button
                type="button"
                data-testid={`editar-empleado-${empleado.id}`}
                onClick={() => onEditar(empleado)}
              >
                Editar
              </button>
              <button
                type="button"
                data-testid={`baja-empleado-${empleado.id}`}
                onClick={() => onDarDeBaja(empleado)}
                disabled={empleado.estado === "baja"}
              >
                Dar de baja
              </button>
              {empleado.estado === "activo" && (
                <button
                  type="button"
                  data-testid={`vacaciones-abrir-${empleado.id}`}
                  onClick={() => onSolicitarVacaciones(empleado)}
                >
                  Solicitar vacaciones
                </button>
              )}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
