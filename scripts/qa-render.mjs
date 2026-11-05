/**
 * Verificación rápida del ensamblado: tamaño, secciones presentes y avisos de
 * parciales/hojas faltantes. Se usa durante el desarrollo y antes de entregar.
 *
 *   node scripts/qa-render.mjs
 */

import { renderDocumento } from "../lib/render.mjs";

const SECCIONES_ESPERADAS = [
  "inicio",
  "problema",
  "vehiculo",
  "beneficios",
  "remolque",
  "transformacion",
  "oferta",
  "comparativa",
  "testimonios",
  "preguntas",
  "cotizacion",
  "cierre",
];

const html = await renderDocumento({ modo: "build" });
const kb = (Buffer.byteLength(html, "utf8") / 1024).toFixed(1);

const faltantes = SECCIONES_ESPERADAS.filter((id) => !html.includes(`id="${id}"`));
const hojas = (html.match(/href="\/src\/styles\/[^"]+"/g) ?? []).map((h) => h.split("/").pop().replace('"', ""));

console.log("");
console.log(`  Documento: ${kb} kB · ${html.split("\n").length} líneas`);
console.log(`  Hojas de estilo enlazadas (${hojas.length}): ${hojas.join(", ")}`);
console.log(`  Script de cliente: ${html.includes("/src/js/main.js") ? "OK" : "FALTA"}`);
console.log(`  JSON-LD: ${(html.match(/application\/ld\+json/g) ?? []).length} bloques`);
console.log("");

if (faltantes.length) {
  console.log(`  ⚠ Faltan secciones: ${faltantes.join(", ")}`);
  process.exitCode = 1;
} else {
  console.log("  ✓ Las 12 secciones están presentes");
}

const sinId = SECCIONES_ESPERADAS.filter((id) => !html.includes(`id="${id}"`));
if (sinId.length) process.exitCode = 1;
