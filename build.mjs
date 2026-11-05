/**
 * Genera el sitio estático listo para publicar en /dist.
 *
 *   node build.mjs
 *
 * No requiere dependencias. El resultado se puede subir a cualquier hosting
 * estático (Vercel, Netlify, S3, cPanel) apuntando el dominio raíz.
 * El endpoint /api/cotizacion debe publicarse por separado (ver README).
 */

import { cp, mkdir, rm, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

import { renderDocumento } from "./lib/render.mjs";

const RAIZ = resolve(import.meta.dirname);
const DIST = resolve(RAIZ, "dist");

async function principal() {
  await rm(DIST, { recursive: true, force: true });
  await mkdir(DIST, { recursive: true });

  const html = await renderDocumento({ modo: "build" });
  await writeFile(resolve(DIST, "index.html"), html, "utf8");

  for (const carpeta of ["assets", "src"]) {
    await cp(resolve(RAIZ, carpeta), resolve(DIST, carpeta), { recursive: true });
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
