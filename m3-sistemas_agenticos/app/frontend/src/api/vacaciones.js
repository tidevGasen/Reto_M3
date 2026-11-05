const BASE = "/api";

async function manejarRespuesta(respuesta) {
  const datos = await respuesta.json();
  if (!respuesta.ok) {
    const mensaje = typeof datos.detail === "string" ? datos.detail : "Ocurrió un error";
    throw new Error(mensaje);
  }
  return datos;
}

export async function obtenerSaldo(empleadoId, anio) {
  const query = anio ? `?anio=${anio}` : "";
  const respuesta = await fetch(`${BASE}/empleados/${empleadoId}/vacaciones${query}`);
  return manejarRespuesta(respuesta);
}

export async function crearSolicitud(empleadoId, datos) {
  const respuesta = await fetch(`${BASE}/empleados/${empleadoId}/vacaciones`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datos),
  });
  return manejarRespuesta(respuesta);
}
