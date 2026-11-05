import { useState } from "react";

export default function ModalBaja({ empleado, onConfirmar, onCancelar }) {
  const [fechaBaja, setFechaBaja] = useState("");
  const [mensajeError, setMensajeError] = useState("");

  async function manejarConfirmar() {
    setMensajeError("");
    try {
      await onConfirmar(empleado.numero_empleado, fechaBaja);
    } catch (error) {
      setMensajeError(error.message);
    }
  }

  return (
    <div role="dialog">
      <p>Dar de baja a {empleado.nombre}</p>
      <label htmlFor="empleado-fecha-baja">Fecha de baja</label>
      <input
        id="empleado-fecha-baja"
        data-testid="empleado-fecha-baja"
        type="date"
        value={fechaBaja}
        onChange={(evento) => setFechaBaja(evento.target.value)}
        required
      />
      <button type="button" data-testid="confirmar-baja" onClick={manejarConfirmar}>
        Confirmar baja
      </button>
      <button type="button" onClick={onCancelar}>
        Cancelar
      </button>

      {mensajeError && <p data-testid="mensaje-error">{mensajeError}</p>}
    </div>
  );
}
