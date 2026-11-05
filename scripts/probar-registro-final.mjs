/**
 * Prueba de registro completa:
 *  1. Envía un lead.
 *  2. Envía OTRO con el mismo celular (para confirmar que ya no hay bloqueo).
 *  3. Muestra la respuesta del servidor y a dónde fue cada correo.
 */

const URL =
  "https://script.google.com/macros/s/AKfycbyo3rlLi4VGjD7-Kz-OsWSViRAPOasfpyCG6DornXqCwzOT_aXb1W-WtlM7znlLCAI-/exec";

const telefono = "55" + String(Date.now()).slice(-8);

const enviar = async (nombre) => {
  const r = await fetch(URL, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      nombre,
      whatsapp: telefono,
      correo: "prueba@ejemplo.com",
      plan: "Financiamiento",
      mensaje: "Registro de prueba desde el diagnóstico.",
      privacidad: true,
      iniciadoEn: Date.now() - 60_000,
      origen: { utm_source: "prueba-registro", utm_campaign: "diagnostico" },
    }),
  });
  const texto = await r.text();
  let cuerpo = null;
  try {
    cuerpo = JSON.parse(texto);
  } catch {}
  return { status: r.status, cuerpo, texto };
};

const main = async () => {
  console.log("Celular usado:", telefono, "\n");

  console.log("ENVÍO 1");
  const a = await enviar("Prueba de registro A");
  console.log("  status:", a.status);
  console.log("  respuesta:", a.texto.slice(0, 400));

  console.log("\nENVÍO 2 (mismo celular)");
  const b = await enviar("Prueba de registro B");
  console.log("  status:", b.status);
  console.log("  respuesta:", b.texto.slice(0, 400));

  const resumen = (etiqueta, r) => {
    const c = r.cuerpo ?? {};
    console.log(
      `\n${etiqueta}: ok=${c.ok} | duplicado=${c.duplicado} | folio=${c.folio ?? "—"}` +
        (c.registro ? ` | fila=${c.registro.fila} (${c.registro.pestana})` : "") +
        (c.correo ? ` | correos: prospecto=${c.correo.prospecto} admin=${c.correo.admin}` : ""),
    );
  };

  resumen("RESUMEN 1", a);
  resumen("RESUMEN 2", b);

  const ambos = [a, b].every((r) => r.cuerpo?.ok === true && r.cuerpo?.duplicado !== true);
  console.log(
    "\n" +
      (ambos
        ? "✓ Los dos registros se aceptaron: no hay restricción para repetir."
        : "✗ Alguno se bloqueó como duplicado: el endpoint desplegado aún tiene la versión anterior."),
  );
};

main();
