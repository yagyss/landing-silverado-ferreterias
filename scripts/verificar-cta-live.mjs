/** Verifica en el sitio publicado que los CTA dicen «Solicitar cotización». */

const BASE = "https://yagyss.github.io/landing-silverado-ferreterias/";
const esperar = (ms) => new Promise((r) => setTimeout(r, ms));
const SELECTOR = 'a[href="#cotizacion"].btn';

const main = async () => {
  for (let intento = 1; intento <= 14; intento++) {
    const html = await (await fetch(`${BASE}?t=${Date.now()}`)).text();
    const version = (html.match(/main\.js\?v=(\d+)/) || [])[1] ?? "?";
    const css = await (await fetch(`${BASE}src/styles/apple.css?v=${version}`)).text();

    if (css.includes(SELECTOR)) {
      console.log("Publicado ✓  versión:", version);
      console.log("  «Solicitar cotización» en el HTML:", (html.match(/Solicitar cotización/g) || []).length);
      console.log("  etiqueta vieja «Quiero mi cotización»:", html.includes("QUIERO MI COTIZACIÓN"));
      console.log("  etiqueta vieja «Hablar con un asesor»:", html.includes("Hablar con un asesor"));
      console.log("  CSS sin mayúsculas en CTA:", css.includes(SELECTOR));

      const siteJs = await (await fetch(`${BASE}src/data/site.js?v=${version}`)).text();
      console.log("  oferta.cta en site.js:", (siteJs.match(/cta:\s*"([^"]+)"/) || [])[1] ?? "—");

      const cuenta = (html.match(/href="#cotizacion"/g) || []).length;
      console.log("  enlaces al formulario en el HTML:", cuenta);
      return;
    }

    console.log(`  intento ${intento}: aún no está el CSS nuevo (versión ${version})…`);
    await esperar(15000);
  }
  console.log("No se detectó el cambio en el tiempo de espera.");
};

main();
