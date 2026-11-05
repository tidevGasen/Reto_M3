const BASE = "/api";

async function manejarRespuesta(respuesta) {
  const datos = await respuesta.json();
  if (!respuesta.ok) {
    const mensaje = typeof datos.detail === "string" ? datos.detail : "Ocurrió un error";
    throw new Error(mensaje);
  }
  return datos;
}

export async function listarEmpleados() {
  const respuesta = await fetch(`${BASE}/empleados`);
  return manejarRespuesta(respuesta);
}

export async function listarDepartamentos() {
  const respuesta = await fetch(`${BASE}/departamentos`);
  return manejarRespuesta(respuesta);
}

export async function crearEmpleado(datos) {
  const respuesta = await fetch(`${BASE}/empleados`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datos),
  });
  return manejarRespuesta(respuesta);
}

export async function actualizarEmpleado(numeroEmpleado, datos) {
  const respuesta = await fetch(`${BASE}/empleados/${numeroEmpleado}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datos),
  });
  return manejarRespuesta(respuesta);
}

export async function darDeBaja(numeroEmpleado, fechaBaja) {
  const respuesta = await fetch(`${BASE}/empleados/${numeroEmpleado}/baja`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ fecha_baja: fechaBaja }),
  });
  return manejarRespuesta(respuesta);
}
