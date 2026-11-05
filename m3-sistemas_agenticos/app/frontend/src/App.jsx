import { useEffect, useState } from "react";

import {
  actualizarEmpleado,
  crearEmpleado,
  darDeBaja,
  listarDepartamentos,
  listarEmpleados,
} from "./api/empleados.js";
import FormularioEmpleado from "./components/FormularioEmpleado.jsx";
import ModalBaja from "./components/ModalBaja.jsx";
import ModalVacaciones from "./components/ModalVacaciones.jsx";
import TablaEmpleados from "./components/TablaEmpleados.jsx";

export default function App() {
  const [empleados, setEmpleados] = useState([]);
  const [departamentos, setDepartamentos] = useState([]);
  const [empleadoEnEdicion, setEmpleadoEnEdicion] = useState(null);
  const [empleadoEnBaja, setEmpleadoEnBaja] = useState(null);
  const [empleadoEnVacaciones, setEmpleadoEnVacaciones] = useState(null);
  const [avisoExito, setAvisoExito] = useState("");

  async function cargarEmpleados() {
    setEmpleados(await listarEmpleados());
  }

  useEffect(() => {
    cargarEmpleados();
    listarDepartamentos().then(setDepartamentos);
  }, []);

  async function manejarCrear(datos) {
    await crearEmpleado(datos);
    await cargarEmpleados();
  }

  async function manejarEditar(numeroEmpleado, datos) {
    await actualizarEmpleado(numeroEmpleado, datos);
    await cargarEmpleados();
    setEmpleadoEnEdicion(null);
    setAvisoExito("Empleado actualizado");
  }

  async function manejarBaja(numeroEmpleado, fechaBaja) {
    await darDeBaja(numeroEmpleado, fechaBaja);
    await cargarEmpleados();
    setEmpleadoEnBaja(null);
    setAvisoExito("Empleado dado de baja");
  }

  function manejarIniciarEdicion(empleado) {
    setAvisoExito("");
    setEmpleadoEnEdicion(empleado);
  }

  function manejarIniciarBaja(empleado) {
    setAvisoExito("");
    setEmpleadoEnBaja(empleado);
  }

  function manejarIniciarVacaciones(empleado) {
    setAvisoExito("");
    setEmpleadoEnVacaciones(empleado);
  }

  return (
    <main>
      <h1>Gestión de empleados</h1>

      {!empleadoEnEdicion && !empleadoEnBaja && !empleadoEnVacaciones && (
        <section>
          <h2>Registrar empleado</h2>
          <FormularioEmpleado modo="alta" departamentos={departamentos} onCrear={manejarCrear} />
        </section>
      )}

      {empleadoEnEdicion ? (
        <FormularioEmpleado
          modo="editar"
          empleadoInicial={empleadoEnEdicion}
          departamentos={departamentos}
          onEditar={manejarEditar}
          onCancelar={() => setEmpleadoEnEdicion(null)}
        />
      ) : empleadoEnBaja ? (
        <ModalBaja
          empleado={empleadoEnBaja}
          onConfirmar={manejarBaja}
          onCancelar={() => setEmpleadoEnBaja(null)}
        />
      ) : empleadoEnVacaciones ? (
        <ModalVacaciones
          empleado={empleadoEnVacaciones}
          onCerrar={() => setEmpleadoEnVacaciones(null)}
        />
      ) : (
        <>
          {avisoExito && <p data-testid="mensaje-exito">{avisoExito}</p>}
          <TablaEmpleados
            empleados={empleados}
            onEditar={manejarIniciarEdicion}
            onDarDeBaja={manejarIniciarBaja}
            onSolicitarVacaciones={manejarIniciarVacaciones}
          />
        </>
      )}
    </main>
  );
}
