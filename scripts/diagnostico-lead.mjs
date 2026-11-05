/** Prueba enfocada: registrar un lead y leer el estado de correos. */

const URL =
  "https://script.google.com/macros/s/AKfycbyo3rlLi4VGjD7-Kz-OsWSViRAPOasfpyCG6DornXqCwzOT_aXb1W-WtlM7znlLCAI-/exec";

const lead = {
  nombre: "Revisión de registro",
  whatsapp: "55" + String(Date.now()).slice(-8),
  correo: "prueba@ejemplo.com",
  plan: "Contado",
  mensaje: "Lead de diagnóstico: si no aparece en la hoja, el problema es la escritura.",
  privacidad: true,
  iniciadoEn: Date.now() - 120_000,
  origen: { utm_source: "diagnostico", utm_campaign: "revision" },
};

const main = async () => {
  const r = await fetch(URL, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(lead),
  });
  const texto = await r.text();
  console.log("status:", r.status);
  console.log("respuesta:", texto.slice(0, 500));

  let cuerpo = null;
  try {
    cuerpo = JSON.parse(texto);
  } catch {}

  if (cuerpo) {
    console.log("\nclaves devueltas:", Object.keys(cuerpo).join(", "));
    if (cuerpo.ok && cuerpo.folio) {
      console.log("=> El script confirmó escritura con folio:", cuerpo.folio);
      console.log("   Teléfono usado:", lead.whatsapp);
      if (cuerpo.correo) {
        console.log("   Correo prospecto:", cuerpo.correo.prospecto);
        console.log("   Correo admin:", cuerpo.correo.admin);
        if (cuerpo.correo.error) console.log("   Error:", cuerpo.correo.error);
      } else {
        console.log("   (versión desplegada sin estado de correos)");
      }
    }
    if (cuerpo.duplicado) console.log("=> Duplicado: NO se escribió fila nueva.");
  }

  // ¿Existe la hoja? Se puede comprobar con GET
  const g = await fetch(URL);
  console.log("\nGET:", (await g.text()).slice(0, 200));
};

main();
