/**
 * Prueba de conexión con el Apps Script publicado.
 * Envía un lead claramente marcado como PRUEBA y muestra el estado HTTP
 * y la respuesta. No se guarda nada en el proyecto local.
 */

const URL =
  "https://script.google.com/macros/s/AKfycbwj3hEDWUEcZa94a1ZThZHK4lWbJW7CsmGysRbXUayBrJcTV-MNWNHSd6BcZCZigBua/exec";

const payload = {
  nombre: "PRUEBA DE CONEXION",
  whatsapp: "5512340000",
  correo: "prueba@ejemplo.com",
  plan: "Quiero conocer las opciones",
  mensaje: "Registro de prueba generado al conectar la landing. Puedes borrarlo.",
  privacidad: true,
  iniciadoEn: Date.now() - 60_000,
  origen: { utm_source: "prueba-tecnica" },
};

async function main() {
  console.log("GET …");
  try {
    const get = await fetch(URL, { redirect: "follow" });
    const texto = await get.text();
    console.log("  status:", get.status);
    console.log("  respuesta:", texto.slice(0, 200).replace(/\s+/g, " "));
  } catch (error) {
    console.log("  GET falló:", error.message);
  }

  console.log("\nPOST …");
  try {
    const post = await fetch(URL, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(payload),
      redirect: "follow",
    });
    const texto = await post.text();
    console.log("  status:", post.status);
    console.log("  respuesta:", texto.slice(0, 400).replace(/\s+/g, " "));
  } catch (error) {
    console.log("  POST falló:", error.message);
  }
}

main();
