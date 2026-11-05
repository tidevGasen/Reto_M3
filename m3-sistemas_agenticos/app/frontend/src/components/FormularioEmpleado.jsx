import { useState } from "react";

const DEPARTAMENTO_VACIO = "";

export default function FormularioEmpleado({
  modo,
  empleadoInicial,
  departamentos,
  onCrear,
  onEditar,
  onCancelar,
}) {
  const esEdicion = modo === "editar";

  const [nombre, setNombre] = useState(empleadoInicial?.nombre ?? "");
  const [correo, setCorreo] = useState(empleadoInicial?.correo ?? "");
  const [puesto, setPuesto] = useState(empleadoInicial?.puesto ?? "");
  const [departamento, setDepartamento] = useState(
    empleadoInicial?.departamento ?? DEPARTAMENTO_VACIO
  );
  const [fechaIngreso, setFechaIngreso] = useState(empleadoInicial?.fecha_ingreso ?? "");
  const [mensajeExito, setMensajeExito] = useState("");
  const [mensajeError, setMensajeError] = useState("");

  async function manejarGuardar(evento) {
    evento.preventDefault();
    setMensajeExito("");
    setMensajeError("");
    try {
      if (esEdicion) {
        await onEditar(empleadoInicial.numero_empleado, { puesto, departamento });
      } else {
        await onCrear({ nombre, correo, puesto, departamento, fecha_ingreso: fechaIngreso });
        setNombre("");
        setCorreo("");
        setPuesto("");
        setDepartamento(DEPARTAMENTO_VACIO);
        setFechaIngreso("");
        setMensajeExito("Empleado registrado");
      }
    } catch (error) {
      setMensajeError(error.message);
    }
  }

  return (
    <form onSubmit={manejarGuardar}>
      <div>
        <label htmlFor="empleado-nombre">Nombre</label>
        <input
          id="empleado-nombre"
          data-testid="empleado-nombre"
          value={nombre}
          onChange={(evento) => setNombre(evento.target.value)}
          disabled={esEdicion}
          required
        />
      </div>

      <div>
        <label htmlFor="empleado-correo">Correo</label>
        <input
          id="empleado-correo"
          data-testid="empleado-correo"
          type="email"
          value={correo}
          onChange={(evento) => setCorreo(evento.target.value)}
          disabled={esEdicion}
          required
        />
      </div>

      <div>
        <label htmlFor="empleado-puesto">Puesto</label>
        <input
          id="empleado-puesto"
          data-testid="empleado-puesto"
          value={puesto}
          onChange={(evento) => setPuesto(evento.target.value)}
          required
        />
      </div>

      <div>
        <label htmlFor="empleado-departamento">Departamento</label>
        <select
          id="empleado-departamento"
          data-testid="empleado-departamento"
          value={departamento}
          onChange={(evento) => setDepartamento(evento.target.value)}
          required
        >
          <option value={DEPARTAMENTO_VACIO} disabled>
            Selecciona un departamento
          </option>
          {departamentos.map((d) => (
            <option key={d} value={d}>
              {d}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label htmlFor="empleado-fecha-ingreso">Fecha de ingreso</label>
        <input
          id="empleado-fecha-ingreso"
          data-testid="empleado-fecha-ingreso"
          type="date"
          value={fechaIngreso}
          onChange={(evento) => setFechaIngreso(evento.target.value)}
          disabled={esEdicion}
          required
        />
      </div>

      <button type="submit" data-testid="empleado-guardar">
        Guardar
      </button>
      {esEdicion && (
        <button type="button" onClick={onCancelar}>
          Cancelar
        </button>
      )}

      {mensajeExito && <p data-testid="mensaje-exito">{mensajeExito}</p>}
      {mensajeError && <p data-testid="mensaje-error">{mensajeError}</p>}
    </form>
  );
}
