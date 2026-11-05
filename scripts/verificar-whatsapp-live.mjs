/** Verifica en el sitio publicado el WhatsApp flotante y el mensaje del formulario. */

const BASE = "https://yagyss.github.io/landing-silverado-ferreterias/";
const esperar = (ms) => new Promise((r) => setTimeout(r, ms));

const main = async () => {
  for (let intento = 1; intento <= 12; intento++) {
    const html = await (await fetch(`${BASE}?t=${Date.now()}`)).text();
    const version = (html.match(/main\.js\?v=(\d+)/) || [])[1] ?? "?";

    if (html.includes("Llena tus datos")) {
      console.log("Publicado ✓ versión:", version);
      console.log("  mensaje nuevo del formulario:", html.includes("Llena tus datos"));
      console.log("  nota de la cotización:", html.includes("Cotización sin costo y sin compromiso"));
      console.log("  botón interno de WhatsApp eliminado:", !html.includes("Escríbenos por WhatsApp"));
      console.log("  número en el HTML:", html.includes("5215580516601"));

      const siteJs = await (await fetch(`${BASE}src/data/site.js?v=${version}`)).text();
      console.log("  whatsapp.numero:", (siteJs.match(/numero:\s*"([^"]*)"/) || [])[1] ?? "—");
      console.log("  telefono:", (siteJs.match(/telefono:\s*"([^"]*)"/) || [])[1] ?? "—");
      return;
    }

    console.log(`  intento ${intento}: aún no (versión ${version})…`);
    await esperar(15000);
  }
  console.log("No se detectó el cambio en el tiempo de espera.");
};

main();
