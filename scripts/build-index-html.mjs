/**
 * Genera un `index.html` autónomo que se abre con doble clic (file://).
 *
 * Por qué existe: los módulos ES (`<script type="module">`) están bloqueados
 * en file:// por CORS, y las rutas absolutas ("/assets/...") apuntarían a la
 * raíz del disco. Este script:
 *   1. Ensambla el mismo HTML que el servidor.
 *   2. Embebe todas las hojas de estilo en un <style>.
 *   3. Concatena los módulos JS en un solo <script> clásico.
 *   4. Convierte todas las rutas a relativas.
 *
 * Uso: node scripts/build-index-html.mjs
 */

import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

import { renderDocumento } from "../lib/render.mjs";

const RAIZ = resolve(import.meta.dirname, "..");

const CSS = [
  "tokens.css",
  "base.css",
  "layout.css",
  "hero.css",
  "showcase.css",
  "seccion-a.css",
  "seccion-b.css",
  "formulario.css",
  "arte-final.css",
  "apple.css",
];

/** Orden de dependencias para el bundle clásico. */
const JS = [
  "site.js",
  "dom.js",
  "validation.mjs",
  "analytics.js",
  "motion.js",
  "nav.js",
  "localnav.js",
  "showcase.js",
  "ui.js",
  "express.js",
  "formulario.js",
  "secciones-b.js",
  "main.js",
];

const leer = (ruta) => readFile(resolve(RAIZ, ruta), "utf8");

/* ------------------------------------------------------- Rutas relativas */
function relativizar(texto) {
  return texto
    .replaceAll('href="/', 'href="')
    .replaceAll('src="/', 'src="')
    .replaceAll('srcset="/', 'srcset="')
    .replaceAll('url("/', 'url("')
    .replaceAll('url("../assets/', 'url("assets/')
    .replaceAll('url("../', 'url("')
    .replaceAll('"/assets/', '"assets/')
    .replaceAll('"/src/', '"src/')
    // Candidatos siguientes dentro de un srcset: ", /assets/..." y " /assets/..."
    .replaceAll(', /assets/', ', assets/')
    .replaceAll(', /src/', ', src/')
    .replaceAll(' /assets/', ' assets/')
    .replaceAll(' /src/', ' src/');
}

/* --------------------------------------------------------------- CSS */
const hojas = [];
for (const hoja of CSS) {
  const contenido = await leer(`src/styles/${hoja}`);
  hojas.push(`/* ==== ${hoja} ==== */\n${relativizar(contenido)}`);
}
const cssFinal = hojas.join("\n");

/* ---------------------------------------------------------------- JS */
const declaraciones = new Map();
const bundle = [];

for (const archivo of JS) {
  const carpeta = archivo.endsWith(".mjs") ? "src/js" : archivo === "site.js" ? "src/data" : "src/js";
  let codigo = await leer(`${carpeta}/${archivo}`);

  // Quita imports (se resuelven por concatenación)
  codigo = codigo.replace(/^import\s[\s\S]*?from\s+["'][^"']+["'];?\s*$/gm, "");
  // Quita exports
  codigo = codigo.replace(/^export\s+(?=(const|let|var|function|class|async))/gm, "");
  codigo = codigo.replace(/^export\s*\{[^}]*\};?\s*$/gm, "");

  // Detecta declaraciones duplicadas que romperían el bundle
  for (const coincidencia of codigo.matchAll(/^(?:const|let|var|function|class|async function)\s+([A-Za-z_$][\w$]*)/gm)) {
    const nombre = coincidencia[1];
    if (declaraciones.has(nombre)) {
      throw new Error(
        `Declaración duplicada "${nombre}" en ${archivo} (ya existía en ${declaraciones.get(nombre)}).`,
      );
    }
    declaraciones.set(nombre, archivo);
  }

  bundle.push(`/* ==== ${archivo} ==== */\n${codigo.trim()}`);
}

const jsFinal = `(function () {\n"use strict";\n${bundle.join("\n\n")}\n})();`;

/* ------------------------------------------------------------- Documento */
let html = await renderDocumento({ modo: "build" });

html = html
  .replace(/^[ \t]*<link rel="stylesheet"[^>]*\/>\s*$/gm, "")
  .replace(/^[ \t]*<script type="module"[^>]*><\/script>\s*$/gm, "");

html = relativizar(html);

// Se usa una función de reemplazo: con un string, `$$` se interpreta como `$`
// y el código JavaScript quedaría alterado.
html = html.replace("</head>", () => `  <style>\n${cssFinal}\n  </style>\n  </head>`);
html = html.replace("</body>", () => `  <script>\n${jsFinal}\n  </script>\n  </body>`);

await writeFile(resolve(RAIZ, "index.html"), html, "utf8");

const kb = (Buffer.byteLength(html, "utf8") / 1024).toFixed(0);
console.log("");
console.log("  index.html autónomo generado");
console.log(`   tamaño      ${kb} kB`);
console.log(`   CSS embebido ${hojas.length} hojas`);
console.log(`   JS embebido  ${JS.length} módulos`);
console.log("");
