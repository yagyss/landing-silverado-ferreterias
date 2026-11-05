/** Inspecciona el JavaScript realmente publicado en GitHub Pages. */

const base = "https://yagyss.github.io/landing-silverado-ferreterias/";

const main = async () => {
  const objetivo = ["src/data/site.js", "src/js/formulario.js", "src/js/main.js"];

  for (const ruta of objetivo) {
    const r = await fetch(base + ruta);
    const t = await r.text();
    console.log(`— ${ruta}  ${r.status}  ${t.length} bytes`);

    if (ruta.includes("site.js")) {
      const url = t.match(/AKfycb[\w-]+/);
      console.log("   endpointRemoto:", t.includes("endpointRemoto"));
      console.log("   URL usada:", url ? url[0].slice(0, 22) + "…" : "—");
    }

    if (ruta.includes("formulario")) {
      console.log("   rama github.io:", t.includes("github.io"));
      console.log("   no-cors:", t.includes("no-cors"));
      console.log("   usa /api/cotizacion:", t.includes("/api/cotizacion"));
      console.log("   reintento:", t.includes('enviar("no-cors")') || t.includes("enviar('no-cors')"));
    }
  }

  // Comparar con el archivo local
  const { readFile } = await import("node:fs/promises");
  const local = await readFile(new URL("../src/js/formulario.js", import.meta.url), "utf8");
  console.log("\nlocal formulario.js:", local.length, "bytes | rama github.io:", local.includes("github.io"));
};

main();
