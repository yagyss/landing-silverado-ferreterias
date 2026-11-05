/** Verificación del sitio publicado en GitHub Pages. */

const SITIO = "https://yagyss.github.io/landing-silverado-ferreterias/";
const APPS =
  "https://script.google.com/macros/s/AKfycbyo3rlLi4VGjD7-Kz-OsWSViRAPOasfpyCG6DornXqCwzOT_aXb1W-WtlM7znlLCAI-/exec";

const rutas = [
  "",
  "assets/vehiculos/silverado/cutout-rojo-lava-1400.webp",
  "assets/vehiculos/silverado/fondo-hero-2000.webp",
  "assets/marca/chevrolet-bowtie.png",
  "src/styles/apple.css",
  "src/js/main.js",
  "src/data/site.js",
  "robots.txt",
];

async function main() {
  console.log("== Recursos publicados ==");
  for (const ruta of rutas) {
    try {
      const r = await fetch(SITIO + ruta, { redirect: "follow" });
      console.log(`  ${r.status}  ${(ruta || "/").slice(0, 60)}  ${r.headers.get("content-type") ?? ""}`);
    } catch (e) {
      console.log(`  ERR ${ruta}: ${e.message}`);
    }
  }

  console.log("\n== CORS del Apps Script (para el formulario) ==");
  try {
    const r = await fetch(APPS, {
      method: "POST",
      headers: { "content-type": "application/json", Origin: "https://yagyss.github.io" },
      body: JSON.stringify({ prueba: true }),
    });
    const acao = r.headers.get("access-control-allow-origin");
    console.log("  status:", r.status, "| access-control-allow-origin:", acao ?? "(ninguno)");
    console.log(
      acao
        ? "  El navegador puede leer la respuesta: se mostrará el folio."
        : "  Sin cabecera CORS: el navegador enviará con no-cors y se confirmará sin folio.",
    );
  } catch (e) {
    console.log("  error:", e.message);
  }

  console.log("\n== Formulario en el HTML publicado ==");
  const html = await (await fetch(SITIO)).text();
  console.log("  campos:", ["nombre", "whatsapp", "correo", "plan", "mensaje"].filter((c) => html.includes(`name="${c}"`)).join(", "));
  console.log("  endpoint remoto:", /script\.google\.com\/macros\/s\/[^"']+/.test(html));
  console.log("  selector de color:", html.includes("data-color="));
}

main();
