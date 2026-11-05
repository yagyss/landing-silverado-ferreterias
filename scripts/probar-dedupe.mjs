/** Reproduce el caso: enviar dos veces el mismo celular. */

const URL =
  "https://script.google.com/macros/s/AKfycbyo3rlLi4VGjD7-Kz-OsWSViRAPOasfpyCG6DornXqCwzOT_aXb1W-WtlM7znlLCAI-/exec";

const enviar = async (telefono, nombre) => {
  const r = await fetch(URL, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      nombre,
      whatsapp: telefono,
      correo: "prueba@ejemplo.com",
      plan: "Contado",
      mensaje: "Prueba de deduplicación.",
      privacidad: true,
      origen: { utm_source: "diagnostico" },
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
  const telefono = "55" + String(Date.now()).slice(-8);

  console.log("1er envío (celular nuevo)…");
  const a = await enviar(telefono, "Prueba dedupe 1");
  console.log("  ", JSON.stringify(a.cuerpo ?? a.texto.slice(0, 200)));

  console.log("\n2do envío (mismo celular, enseguida)…");
  const b = await enviar(telefono, "Prueba dedupe 2");
  console.log("  ", JSON.stringify(b.cuerpo ?? b.texto.slice(0, 200)));

  if (b.cuerpo?.duplicado) {
    console.log("\n=> El segundo envío se marca como DUPLICADO:");
    console.log("   no escribe fila nueva y no envía correos.");
  }
};

main();
