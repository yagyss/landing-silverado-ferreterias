/**
 * Genera el sitio estático listo para publicar en /dist.
 *
 *   node build.mjs
 *
 * No requiere dependencias. El resultado se puede subir a cualquier hosting
 * estático (Vercel, Netlify, S3, cPanel) apuntando el dominio raíz.
 * El endpoint /api/cotizacion debe publicarse por separado (ver README).
 */

import { cp, mkdir, readFile, readdir, rm, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

import { renderDocumento } from "./lib/render.mjs";

const RAIZ = resolve(import.meta.dirname);
const DIST = resolve(RAIZ, "dist");

async function principal() {
  await rm(DIST, { recursive: true, force: true });
  await mkdir(DIST, { recursive: true });

  let html = await renderDocumento({ modo: "build" });

  // GitHub Pages sirve el sitio en /<repo>/: las rutas absolutas (/assets/…)
  // apuntarían a la raíz del dominio, así que se vuelven relativas.
  if (process.env.RELATIVE_PATHS === "1") {
    html = html
      .replaceAll('href="/', 'href="')
      .replaceAll('src="/', 'src="')
      .replaceAll('srcset="/', 'srcset="')
      .replaceAll(', /assets/', ', assets/')
      .replaceAll(' /assets/', ' assets/')
      .replaceAll('"/assets/', '"assets/')
      .replaceAll('"/src/', '"src/');
  }

  await writeFile(resolve(DIST, "index.html"), html, "utf8");

  for (const carpeta of ["assets", "src"]) {
    await cp(resolve(RAIZ, carpeta), resolve(DIST, carpeta), { recursive: true });
  }

  // En subcarpeta (GitHub Pages) el CSS también debe usar rutas relativas:
  // desde /src/styles/ hacia /assets/ son dos niveles arriba.
  if (process.env.RELATIVE_PATHS === "1") {
    const estilos = resolve(DIST, "src", "styles");
    for (const archivo of await readdir(estilos)) {
      if (!archivo.endsWith(".css")) continue;
      const rutaCss = resolve(estilos, archivo);
      let css = await readFile(rutaCss, "utf8");
      css = css
        .replaceAll('url("/assets/', 'url("../../assets/')
        .replaceAll("url('/assets/", "url('../../assets/")
        .replaceAll('url("/src/', 'url("../../../src/');
      await writeFile(rutaCss, css, "utf8");
    }
  }

  // No publicar material de origen pesado
  await rm(resolve(DIST, "assets", "vehiculos", "silverado", "_originales"), {
    recursive: true,
    force: true,
  });

  // Las herramientas de revisión local no se publican
  await rm(resolve(DIST, "src", "layout", "_qa-view.html"), { force: true });

  // Archivos de raíz relevantes para el hosting (Netlify usa netlify.toml)
  for (const archivo of ["robots.txt", "netlify.toml"]) {
    try {
      await cp(resolve(RAIZ, archivo), resolve(DIST, archivo));
    } catch {
      // opcional: si no existe, se ignora
    }
  }

  // Deploys manuales (arrastrar carpeta) no leen netlify.toml: se copia la
  // regla del proxy a _redirects para garantizar /api/cotizacion.
  const toml = await readFile(resolve(RAIZ, "netlify.toml"), "utf8");
  const destino = toml.match(/from = "\/api\/cotizacion"\s*\n\s*to = "([^"]+)"/);
  if (destino) {
    await writeFile(
      resolve(DIST, "_redirects"),
      `/api/cotizacion  ${destino[1]}  200\n`,
      "utf8",
    );
  }


  // Rompe la caché del navegador: los módulos JS y el CSS cambian con cada
  // despliegue, así nadie queda ejecutando una versión anterior del formulario.
  const VERSION_ASSETS = process.env.ASSET_VERSION || String(Date.now()).slice(0, 10);
  {
    const dirs = [resolve(DIST, "src", "js"), resolve(DIST, "src", "data")];
    for (const dir of dirs) {
      let archivos = [];
      try {
        archivos = await readdir(dir);
      } catch {
        continue;
      }
      for (const archivo of archivos) {
        if (!archivo.endsWith(".js") && !archivo.endsWith(".mjs")) continue;
        const rutaJs = resolve(dir, archivo);
        let js = await readFile(rutaJs, "utf8");
        js = js.replace(
          /(from\s*["'])(\.{1,2}\/[^"']+\.(?:js|mjs))(["'])/g,
          `$1$2?v=${VERSION_ASSETS}$3`,
        );
        js = js.replace(
          /(import\s*["'])(\.{1,2}\/[^"']+\.(?:js|mjs))(["'])/g,
          `$1$2?v=${VERSION_ASSETS}$3`,
        );
        await writeFile(rutaJs, js, "utf8");
      }
    }
    // Los CSS que importan a otros también se versionan
    const estilos = resolve(DIST, "src", "styles");
    try {
      for (const archivo of await readdir(estilos)) {
        if (!archivo.endsWith(".css")) continue;
        const rutaCss = resolve(estilos, archivo);
        let css = await readFile(rutaCss, "utf8");
        css = css.replace(/@import\s+url\((["'])([^"']+\.css)\1\)/g, `@import url($1$2?v=${VERSION_ASSETS}$1)`);
        await writeFile(rutaCss, css, "utf8");
      }
    } catch {
      /* sin hojas que importar */
    }
  }

  const kb = (Buffer.byteLength(html, "utf8") / 1024).toFixed(1);
  console.log("");
  console.log("  Build estático generado en /dist");
  console.log(`   index.html   ${kb} kB`);
  console.log("   Publica /dist en Netlify (arrastrar o Git) y conecta el formulario");
  console.log("   a Google Sheets siguiendo docs/GOOGLE-SHEETS.md");
  console.log("");
}

principal().catch((error) => {
  console.error("Error al generar el build:", error);
  process.exit(1);
});
