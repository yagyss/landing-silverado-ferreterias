/**
 * Servidor de revisión local · sin dependencias externas.
 *
 *   node server.mjs            -> http://localhost:4173
 *
 * - Ensambla index.html al vuelo a partir de los parciales de /src.
 * - Sirve assets, estilos y módulos JS.
 * - Expone POST /api/cotizacion (registro real de prospectos).
 * - Bloquea el acceso web a /data (prospectos), /scripts, /lib y la raíz.
 */

import { createServer } from "node:http";
import { readFile, stat } from "node:fs/promises";
import { extname, resolve, sep } from "node:path";

import { procesarProspecto } from "./api/cotizacion.mjs";
import { renderDocumento } from "./lib/render.mjs";

const RAIZ = resolve(import.meta.dirname);
const PUERTO = Number(process.env.PORT ?? 4173);
const HOST = process.env.HOST ?? "127.0.0.1";

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".webp": "image/webp",
  ".avif": "image/avif",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".svg": "image/svg+xml",
  ".ico": "image/x-icon",
  ".woff2": "font/woff2",
  ".txt": "text/plain; charset=utf-8",
  ".webmanifest": "application/manifest+json",
};

/** Sólo estas carpetas se publican en la vista local. */
const PREFIJOS_PUBLICOS = ["/assets/", "/src/styles/", "/src/js/", "/src/data/", "/src/layout/"];

function esPublico(pathname) {
  if (pathname === "/favicon.ico" || pathname === "/robots.txt") return true;
  return PREFIJOS_PUBLICOS.some((prefijo) => pathname.startsWith(prefijo));
}

function respuestaJson(res, status, cuerpo) {
  const texto = JSON.stringify(cuerpo);
  res.writeHead(status, {
    "content-type": "application/json; charset=utf-8",
    "content-length": Buffer.byteLength(texto),
    "cache-control": "no-store",
  });
  res.end(texto);
}

async function leerCuerpo(req, limite = 64 * 1024) {
  return new Promise((resolve, reject) => {
    let datos = "";
    req.on("data", (trozo) => {
      datos += trozo;
      if (datos.length > limite) {
        reject(new Error("cuerpo-demasiado-grande"));
        req.destroy();
      }
    });
    req.on("end", () => resolve(datos));
    req.on("error", reject);
  });
}

async function servirArchivo(res, rutaAbsoluta, { cache = "no-store" } = {}) {
  const info = await stat(rutaAbsoluta);
  if (!info.isFile()) throw new Error("no-es-archivo");
  const contenido = await readFile(rutaAbsoluta);
  res.writeHead(200, {
    "content-type": MIME[extname(rutaAbsoluta).toLowerCase()] ?? "application/octet-stream",
    "content-length": contenido.byteLength,
    "cache-control": cache,
  });
  res.end(contenido);
}

const servidor = createServer(async (req, res) => {
  const url = new URL(req.url ?? "/", `http://${req.headers.host ?? `${HOST}:${PUERTO}`}`);
  const pathname = decodeURIComponent(url.pathname);
  const inicio = Date.now();

  try {
    /* ------------------------------------------------------------- API */
    if (pathname === "/api/cotizacion") {
      if (req.method !== "POST") {
        res.setHeader("allow", "POST");
        return respuestaJson(res, 405, { ok: false, mensaje: "Método no permitido" });
      }
      let cuerpo = {};
      try {
        cuerpo = JSON.parse((await leerCuerpo(req)) || "{}");
      } catch {
        return respuestaJson(res, 400, { ok: false, mensaje: "Solicitud inválida." });
      }
      const ip = req.socket.remoteAddress ?? "local";
      const resultado = await procesarProspecto({
        body: cuerpo,
        ip,
        userAgent: req.headers["user-agent"],
        referrer: cuerpo.referrer ?? req.headers.referer,
        pagina: cuerpo.pagina,
        utm: cuerpo.origen,
      });
      return respuestaJson(res, resultado.status, resultado.body);
    }

    if (pathname === "/api/estado") {
      let total = 0;
      try {
        const contenido = await readFile(resolve(RAIZ, "data", "prospectos.jsonl"), "utf8");
        total = contenido.split("\n").filter(Boolean).length;
      } catch {
        total = 0;
      }
      return respuestaJson(res, 200, {
        ok: true,
        prospectosRegistrados: total,
        almacenamiento: "data/prospectos.jsonl",
      });
    }

    if (req.method !== "GET" && req.method !== "HEAD") {
      return respuestaJson(res, 405, { ok: false, mensaje: "Método no permitido" });
    }

    /* --------------------------------------------------------- Documento */
    if (pathname === "/" || pathname === "/index.html") {
      const html = await renderDocumento({ modo: "dev" });
      res.writeHead(200, {
        "content-type": MIME[".html"],
        "cache-control": "no-store",
      });
      res.end(html);
      console.log(`  GET  /                       200  ${Date.now() - inicio}ms`);
      return;
    }

    /* ------------------------------------------------------------ Estático */
    if (esPublico(pathname)) {
      const rutaAbsoluta = resolve(RAIZ, `.${pathname}`);
      if (!rutaAbsoluta.startsWith(RAIZ + sep)) {
        return respuestaJson(res, 403, { ok: false, mensaje: "Acceso denegado" });
      }
      const cache = pathname.startsWith("/assets/") ? "public, max-age=3600" : "no-store";
      await servirArchivo(res, rutaAbsoluta, { cache });
      return;
    }

    /* --------------------------------------------------------------- 404 */
    res.writeHead(404, { "content-type": MIME[".html"] });
    res.end(`<!DOCTYPE html><html lang="es-MX"><head><meta charset="utf-8" />
<title>No encontrado</title>
<style>body{font-family:system-ui;background:#0b0e13;color:#f7f8fa;display:grid;place-items:center;height:100vh;margin:0;text-align:center}
a{color:#e3c47c}</style></head><body><div><h1>404</h1><p>Esta página no existe.</p><p><a href="/">Volver a la landing</a></p></div></body></html>`);
  } catch (error) {
    console.error("[server]", error?.message ?? error);
    if (!res.headersSent) {
      respuestaJson(res, 500, { ok: false, mensaje: "Error interno del servidor de revisión." });
    } else {
      res.end();
    }
  }
});

servidor.listen(PUERTO, HOST, () => {
  console.log("");
  console.log("   Chevrolet Silverado - landing para ferreterias (revision)");
  console.log(`   URL         http://${HOST}:${PUERTO}`);
  console.log(`   Prospectos  data/prospectos.jsonl`);
  console.log(`   Estado      http://${HOST}:${PUERTO}/api/estado`);
  console.log("");
});
