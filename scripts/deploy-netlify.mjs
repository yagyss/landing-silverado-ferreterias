/**
 * Publica la landing en Netlify con el token de la cuenta.
 *
 * 1. Verifica el token.
 * 2. Crea el sitio (o reutiliza uno existente con el mismo nombre).
 * 3. Sube el paquete `landing-dist.zip` (deploy inmediato).
 * 4. Informa la URL y el estado.
 *
 * El token se lee de NETLIFY_TOKEN y nunca se imprime.
 */

import { readFile } from "node:fs/promises";
import { resolve } from "node:path";

const TOKEN = process.env.NETLIFY_TOKEN;
if (!TOKEN) {
  console.error("Falta NETLIFY_TOKEN en el entorno.");
  process.exit(1);
}

const RAIZ = resolve(import.meta.dirname, "..");
const NOMBRE_BASE = "silverado-ferreterias";

const cabeceras = {
  Authorization: `Bearer ${TOKEN}`,
  "User-Agent": "dsh-landing",
};

const api = async (ruta, opciones = {}) => {
  const respuesta = await fetch(`https://api.netlify.com/api/v1${ruta}`, {
    headers: { ...cabeceras, ...(opciones.headers ?? {}) },
    ...opciones,
  });
  const texto = await respuesta.text();
  let datos = null;
  try {
    datos = texto ? JSON.parse(texto) : null;
  } catch {
    datos = null;
  }
  return { status: respuesta.status, datos, texto };
};

async function main() {
  const yo = await api("/user");
  if (yo.status !== 200) {
    console.error("Token inválido:", yo.status, (yo.datos?.message ?? yo.texto).slice(0, 200));
    process.exit(1);
  }
  console.log("  cuenta:", yo.datos.email ?? yo.datos.full_name ?? yo.datos.id);

  // Buscar sitio existente
  const sitios = await api("/sites?per_page=100");
  const lista = Array.isArray(sitios.datos) ? sitios.datos : [];
  let sitio = lista.find((s) => String(s.name).startsWith(NOMBRE_BASE));

  if (!sitio) {
    const creado = await api("/sites", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ name: NOMBRE_BASE }),
    });
    if (creado.status >= 400) {
      console.error("No se pudo crear el sitio:", creado.status, (creado.datos?.message ?? "").slice(0, 200));
      process.exit(1);
    }
    sitio = creado.datos;
    console.log("  sitio creado:", sitio.ssl_url ?? sitio.url);
  } else {
    console.log("  sitio existente:", sitio.ssl_url ?? sitio.url);
  }

  // Subir el paquete
  const zip = await readFile(resolve(RAIZ, "landing-dist.zip"));
  console.log(`  subiendo ${(zip.length / 1024 / 1024).toFixed(2)} MB…`);

  const subida = await fetch(`https://api.netlify.com/api/v1/sites/${sitio.id}/deploys`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${TOKEN}`,
      "Content-Type": "application/zip",
      "User-Agent": "dsh-landing",
    },
    body: zip,
  });

  const texto = await subida.text();
  let deploy = null;
  try {
    deploy = JSON.parse(texto);
  } catch {
    deploy = null;
  }

  if (!subida.ok) {
    console.error("  deploy falló:", subida.status, texto.slice(0, 300));
    process.exit(1);
  }

  console.log("  deploy creado:", deploy.id ?? "—");
  console.log("  estado inicial:", deploy.state ?? "—");

  // Esperar a que termine
  for (let intento = 1; intento <= 30; intento++) {
    await new Promise((r) => setTimeout(r, 5000));
    const estado = await api(`/sites/${sitio.id}/deploys/${deploy.id}`);
    const actual = estado.datos?.state ?? "desconocido";
    console.log(`   ${intento * 5}s: ${actual}`);
    if (actual === "ready" || actual === "error") {
      console.log("\n  URL:", sitio.ssl_url ?? sitio.url);
      console.log("  resultado:", actual);
      if (actual === "error") console.log("  log:", estado.datos?.error_message ?? "—");
      return;
    }
  }

  console.log("\n  URL (aún procesando):", sitio.ssl_url ?? sitio.url);
}

main();
