/**
 * Prueba la nueva implementación y deja constancia del resultado.
 * Uso: node scripts/probar-nueva-url.mjs
 */

const URL =
  "https://script.google.com/macros/s/AKfycbyo3rlLi4VGjD7-Kz-OsWSViRAPOasfpyCG6DornXqCwzOT_aXb1W-WtlM7znlLCAI-/exec";

const lead = {
  nombre: "Prueba de conexion",
  whatsapp: "5512340009",
  correo: "prueba@ejemplo.com",
  plan: "Quiero conocer las opciones",
  mensaje: "Lead de prueba enviado al conectar la landing. Puedes borrar esta fila.",
  privacidad: true,
  iniciadoEn: Date.now() - 60_000,
  origen: { utm_source: "prueba-tecnica", utm_campaign: "conexion" },
};

const limpio = (t) => String(t).replace(/\s+/g, " ").slice(0, 300);

const main = async () => {
  console.log("GET …");
  try {
    const r = await fetch(URL, { redirect: "follow" });
    const texto = await r.text();
    const pareceHtml = texto.trim().startsWith("<");
    console.log("  status:", r.status);
    console.log("  respuesta:", limpio(texto));
    console.log("  ¿HTML de error?:", pareceHtml ? "SÍ (versión vieja)" : "no");
  } catch (e) {
    console.log("  falló:", e.message);
  }

  console.log("\nPOST (lead de prueba) …");
  try {
    const r = await fetch(URL, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(lead),
      redirect: "follow",
    });
    const texto = await r.text();
    console.log("  status:", r.status);
    console.log("  respuesta:", limpio(texto));

    let cuerpo = null;
    try {
      cuerpo = JSON.parse(texto);
    } catch {}

    if (cuerpo && cuerpo.ok === true && cuerpo.folio) {
      console.log("\n  ✓ Registro confirmado. Folio:", cuerpo.folio);
      console.log("  Revisa la hoja: debe aparecer la fila con nombre, teléfono, email, plan y mensaje.");
      console.log("  Y deben haber llegado los dos correos.");
    } else if (cuerpo && cuerpo.duplicado) {
      console.log("\n  ✓ Ya existía (deduplicado). Folio:", cuerpo.folio);
    } else {
      console.log("\n  ✗ La respuesta no confirma el registro.");
    }
  } catch (e) {
    console.log("  falló:", e.message);
  }
};

main();
