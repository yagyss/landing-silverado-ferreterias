/** Confirma en el sitio publicado que la flecha móvil ya está desplegada. */

const BASE = "https://yagyss.github.io/landing-silverado-ferreterias/";
const esperar = (ms) => new Promise((r) => setTimeout(r, ms));

const main = async () => {
  for (let intento = 1; intento <= 12; intento++) {
    const html = await (await fetch(`${BASE}?t=${Date.now()}`)).text();

    if (html.includes("cotiza__alt-flecha--abajo")) {
      const oficial = (html.match(/main\.js\?v=(\d+)/) || [])[1] ?? "?";
      console.log("Publicado ✓  versión:", oficial);
      console.log("  flecha vertical (móvil):", html.includes("cotiza__alt-flecha--abajo"));
      console.log("  flecha horizontal (escritorio):", /class="cotiza__alt-flecha"/.test(html));
      console.log("  avisos de campaña fuera:", !html.includes("data-form-privacidad-nota"));
      return;
    }

    console.log(`  intento ${intento}: aún no…`);
    await esperar(15000);
  }
  console.log("No se detectó el despliegue en el tiempo de espera.");
};

main();
