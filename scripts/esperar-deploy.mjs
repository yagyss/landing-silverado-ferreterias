/** Espera a que GitHub Pages publique el build nuevo y verifica los textos. */

const BASE = "https://yagyss.github.io/landing-silverado-ferreterias/";
const VERSION_ANTERIOR = "1793855015";

const esperar = (ms) => new Promise((r) => setTimeout(r, ms));

const main = async () => {
  for (let intento = 1; intento <= 20; intento++) {
    const html = await (await fetch(`${BASE}?t=${Date.now()}`)).text();
    const version = (html.match(/main\.js\?v=(\d+)/) || [])[1] ?? "?";

    if (version !== VERSION_ANTERIOR) {
      console.log(`Build nuevo detectado (intento ${intento}), versión: ${version}\n`);

      const siteJs = await (await fetch(`${BASE}src/data/site.js?v=${version}`)).text();
      const ofertaJs = await (await fetch(`${BASE}src/js/secciones-b.js?v=${version}`)).text();

      console.log("index.html:");
      console.log("  «Solicitar cotización»:", (html.match(/Solicitar cotización/g) || []).length);
      console.log("  «QUIERO MI COTIZACIÓN»:", html.includes("QUIERO MI COTIZACIÓN"));
      console.log("  «Hablar con un asesor»:", html.includes("Hablar con un asesor"));
      console.log("site.js → cta:", (siteJs.match(/cta:\s*"([^"]+)"/) || [])[1] ?? "—");
      console.log("secciones-b carga la etiqueta:", ofertaJs.includes("oferta-cta-label"));

      const css = await (await fetch(`${BASE}src/styles/apple.css?v=${version}`)).text();
      console.log("CSS sin mayúsculas en CTA:", css.includes('a[href="#cotizacion"].btn'));
      return;
    }

    console.log(`  intento ${intento}: aún versión ${version}…`);
    await esperar(15000);
  }
  console.log("No se detectó build nuevo en el tiempo de espera.");
};

main();
