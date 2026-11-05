import { useEffect, useState } from "react";

import { crearSolicitud, obtenerSaldo } from "../api/vacaciones.js";

export default function ModalVacaciones({ empleado, onCerrar }) {
  const [fechaInicio, setFechaInicio] = useState("");
  const [fechaFin, setFechaFin] = useState("");
  const [diasDisponibles, setDiasDisponibles] = useState(null);
  const [mensaje, setMensaje] = useState("");

  async function cargarSaldo() {
    const saldo = await obtenerSaldo(empleado.id);
    setDiasDisponibles(saldo.dias_disponibles);
  }

  useEffect(() => {
    cargarSaldo();
  }, [empleado.id]);

  async function manejarEnviar() {
    try {
      const resultado = await crearSolicitud(empleado.id, {
        fecha_inicio: fechaInicio,
        fecha_fin: fechaFin,
      });
      const anio = fechaInicio.slice(0, 4);
      setMensaje(
        `Solicitud registrada: ${resultado.dias_habiles} días hábiles. ` +
          `Te quedan ${resultado.dias_restantes} días hábiles en ${anio}.`
      );
      await cargarSaldo();
    } catch (error) {
      setMensaje(error.message);
    }
  }

  return (
    <div role="dialog">
      <p>Solicitar vacaciones de {empleado.nombre}</p>

      <label htmlFor="vacaciones-fecha-inicio">Fecha de inicio</label>
      <input
        id="vacaciones-fecha-inicio"
        data-testid="vacaciones-fecha-inicio"
        type="date"
        value={fechaInicio}
        onChange={(evento) => setFechaInicio(evento.target.value)}
        required
      />

      <label htmlFor="vacaciones-fecha-fin">Fecha de fin</label>
      <input
        id="vacaciones-fecha-fin"
        data-testid="vacaciones-fecha-fin"
        type="date"
        value={fechaFin}
        onChange={(evento) => setFechaFin(evento.target.value)}
        required
      />

      <p data-testid="vacaciones-disponibles">Días disponibles: {diasDisponibles ?? "..."}</p>

      <button type="button" data-testid="vacaciones-enviar" onClick={manejarEnviar}>
        Enviar solicitud
      </button>
      <button type="button" onClick={onCerrar}>
        Cerrar
      </button>

      {mensaje && <p data-testid="vacaciones-mensaje">{mensaje}</p>}
    </div>
  );
}
