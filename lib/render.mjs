/**
 * Ensamblado del documento HTML.
 *
 * La página se compone de parciales independientes (una sección por archivo),
 * lo que permite editar cada bloque sin tocar los demás y mantener el HTML
 * final renderizado en el servidor (mejor primera pintura y SEO).
 *
 * Uso interno: server.mjs (vista local) y build.mjs (sitio estático).
 */

import { readFile } from "node:fs/promises";
import { resolve } from "node:path";

import { SITE } from "../src/data/site.js";

const RAIZ = resolve(import.meta.dirname, "..");

/** Orden de las hojas de estilo. Los archivos ausentes se omiten. */
const HOJAS = [
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

/** Orden de las secciones de la landing (coincide con el brief). */
const SECCIONES = [
  "01-hero",
  "01b-destacados",
  "02-problema",
  "03-solucion",
  "04-beneficios",
  "05-remolque",
  "06-transformacion",
  "07-oferta",
  "08-comparativa",
  "09-testimonios",
  "10-faq",
  "11-cotizacion",
  "12-cta-final",
];

async function leerArchivo(rutaRelativa, { opcional = true } = {}) {
  try {
    return await readFile(resolve(RAIZ, rutaRelativa), "utf8");
  } catch (error) {
    if (opcional) return "";
    throw error;
  }
}

/**
 * Marca de versión para que el navegador no reutilice CSS/JS antiguos.
 * Cambia en cada build, así los visitantes reciben siempre el código actual.
 */
const VERSION_ASSETS = process.env.ASSET_VERSION || String(Date.now()).slice(0, 10);

async function leerHojasExistentes() {
  const enlaces = [];
  for (const hoja of HOJAS) {
    const contenido = await leerArchivo(`src/styles/${hoja}`);
    if (contenido.trim()) {
      enlaces.push(
        `<link rel="stylesheet" href="/src/styles/${hoja}?v=${VERSION_ASSETS}" />`,
      );
    }
  }
  return enlaces.join("\n    ");
}

function jsonLd() {
  const base = SITE.meta.urlCanonica.replace(/\/$/, "");
  const faq = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: SITE.faq.items.map((item) => ({
      "@type": "Question",
      name: item.p,
      acceptedAnswer: { "@type": "Answer", text: item.r },
    })),
  };
  const pagina = {
    "@context": "https://schema.org",
    "@type": "WebPage",
    name: SITE.meta.titulo,
    description: SITE.meta.descripcion,
    inLanguage: SITE.meta.idioma,
    url: SITE.meta.urlCanonica,
    about: {
      "@type": "Car",
      name: `${SITE.marca.nombre} ${SITE.marca.modelo}`,
      brand: { "@type": "Brand", name: SITE.marca.nombre },
      model: SITE.marca.modelo,
      vehicleModelDate: SITE.marca.anio,
    },
    publisher: { "@type": "Organization", name: SITE.contacto.distribuidor || "Distribuidor autorizado" },
    image: `${base}/${SITE.meta.imagenOg}`,
  };
  return [pagina, faq]
    .map((bloque) => `<script type="application/ld+json">${JSON.stringify(bloque)}</script>`)
    .join("\n    ");
}

async function construirHead() {
  const base = SITE.meta.urlCanonica.replace(/\/$/, "");
  const hojas = await leerHojasExistentes();
  return `<!DOCTYPE html>
<html lang="${SITE.meta.idioma}" class="no-js">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
    <title>${SITE.meta.titulo}</title>
    <meta name="description" content="${SITE.meta.descripcion}" />
    <meta name="keywords" content="${SITE.meta.palabrasClave.join(", ")}" />
    <meta name="robots" content="index, follow" />
    <meta name="theme-color" content="${SITE.meta.themeColor}" />
    <link rel="canonical" href="${SITE.meta.urlCanonica}" />

    <meta property="og:type" content="website" />
    <meta property="og:locale" content="es_MX" />
    <meta property="og:site_name" content="${SITE.marca.nombre} ${SITE.marca.modelo}" />
    <meta property="og:title" content="${SITE.meta.titulo}" />
    <meta property="og:description" content="${SITE.meta.descripcion}" />
    <meta property="og:url" content="${SITE.meta.urlCanonica}" />
    <meta property="og:image" content="${base}/${SITE.meta.imagenOg}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="${SITE.meta.titulo}" />
    <meta name="twitter:description" content="${SITE.meta.descripcion}" />
    <meta name="twitter:image" content="${base}/${SITE.meta.imagenOg}" />

    <link rel="icon" href="/assets/marca/favicon.svg" type="image/svg+xml" />
    <link rel="apple-touch-icon" href="/assets/marca/apple-touch-icon.png" />

    <link rel="preconnect" href="https://brands.gm-cdn.com" crossorigin />
    <link rel="preconnect" href="https://www.chevrolet.com.mx" crossorigin />
    <link
      rel="preload"
      as="image"
      href="/assets/vehiculos/silverado/color-rojo-lava-1400.webp"
      fetchpriority="high"
      media="(min-width: 760px)"
    />
    <link
      rel="preload"
      as="image"
      href="/assets/vehiculos/silverado/color-rojo-lava-900.webp"
      fetchpriority="high"
      media="(max-width: 759px)"
    />

    ${hojas}

    <!-- Marca la disponibilidad de JS antes de pintar para evitar saltos -->
    <script>
      document.documentElement.classList.remove("no-js");
      document.documentElement.classList.add("js");
    </script>
    ${jsonLd()}
  </head>`;
}

async function construirSecciones() {
  const partes = [];
  for (const nombre of SECCIONES) {
    const contenido = await leerArchivo(`src/sections/${nombre}.html`);
    if (contenido.trim()) {
      partes.push(`      <!-- ===== ${nombre} ===== -->\n${contenido.trimEnd()}`);
    }
  }
  return partes.join("\n\n");
}

/**
 * @param {{ modo?: "dev" | "build" }} [opciones]
 * @returns {Promise<string>}
 */
export async function renderDocumento(opciones = {}) {
  const { modo = "dev" } = opciones;
  const head = await construirHead();
  const header = await leerArchivo("src/layout/header.html");
  const localnav = await leerArchivo("src/layout/localnav.html");
  const footer = await leerArchivo("src/layout/footer.html");
  const secciones = await construirSecciones();
  const aviso = await leerArchivo("src/layout/aviso-privacidad.html");

  const atributoModo = modo === "dev" ? ' data-modo="dev"' : "";

  return `${head}
  <body${atributoModo}>
    <a class="skip-link" href="#contenido">Saltar al contenido</a>
    <div class="scroll-progress" id="scroll-progress" aria-hidden="true"></div>

${header}

${localnav}

    <main id="contenido" tabindex="-1">
${secciones}
    </main>

${footer}
${aviso}

    <script type="module" src="/src/js/main.js?v=${VERSION_ASSETS}"></script>
  </body>
</html>
`;
}

export { SECCIONES, HOJAS };
