"""Envío directo al Apps Script también fuera de Netlify (GitHub Pages)."""

import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ruta = RAIZ / "src/js/formulario.js"
t = ruta.read_text(encoding="utf-8")

# 1) Decide el destino: proxy en Netlify, directo en archivo o GitHub Pages
viejo = """      // Abierto como archivo se envía directo al Apps Script (sin proxy).
      const esArchivo = window.location.protocol === "file:";
      const destino =
        esArchivo && SITE.formulario.endpointRemoto
          ? SITE.formulario.endpointRemoto
          : SITE.formulario.endpoint;"""

nuevo = """      // Netlify usa su proxy (/api/cotizacion). En archivo local o GitHub Pages
      // se envía directo al Apps Script.
      const host = window.location.hostname;
      const sinProxy =
        window.location.protocol === "file:" || host.endsWith("github.io") || host === "";
      const esArchivo = window.location.protocol === "file:";
      const destino =
        sinProxy && SITE.formulario.endpointRemoto
          ? SITE.formulario.endpointRemoto
          : SITE.formulario.endpoint;"""

if viejo in t:
    t = t.replace(viejo, nuevo)
    print("  destino por host configurado")

# 2) Petición tolerante: primero normal; si CORS falla, se reintenta simple
viejo_fetch = """      const respuesta = await fetch(destino, {
        method: "POST",
        // Con file:// el navegador no permite leer la respuesta (CORS),
        // así que se usa una petición simple y se informa con honestidad.
        mode: esArchivo ? "no-cors" : "cors",
        headers: {
          "content-type": esArchivo ? "text/plain;charset=utf-8" : "application/json",
        },"""

nuevo_fetch = """      const cuerpoEnvio = JSON.stringify({
        nombre: limpio.nombre,
        whatsapp: normalizarTelefono(limpio.whatsapp),
        correo: limpio.correo,
        plan: limpio.plan,
        mensaje: limpio.mensaje,
        privacidad: true,
        honeypot: limpio.honeypot,
        iniciadoEn: comenzado,
        pagina: window.location.href,
        referrer: document.referrer,
        origen: leerUtm(),
      });

      const enviar = (modo) =>
        fetch(destino, {
          method: "POST",
          mode: modo,
          headers: {
            "content-type": modo === "no-cors" ? "text/plain;charset=utf-8" : "application/json",
          },
          body: cuerpoEnvio,
        });

      // Apps Script no siempre expone CORS: se intenta leer la respuesta y, si
      // el navegador la bloquea, se reenvía igual y se informa con honestidad.
      let respuesta;
      try {
        respuesta = await enviar("cors");
      } catch (errorCors) {
        respuesta = await enviar("no-cors");
      }

      const respuestaVieja = {"""

if viejo_fetch in t:
    t = t.replace(viejo_fetch, nuevo_fetch)
    # Elimina el objeto viejo que quedó abierto (resto de la llamada anterior)
    t = t.replace(
        """      const respuestaVieja = {
        body: JSON.stringify({
          nombre: limpio.nombre,
          whatsapp: normalizarTelefono(limpio.whatsapp),
          correo: limpio.correo,
          plan: limpio.plan,
          mensaje: limpio.mensaje,
          privacidad: true,
          honeypot: limpio.honeypot,
          iniciadoEn: comenzado,
          pagina: window.location.href,
          referrer: document.referrer,
          origen: leerUtm(),
        }),
      });""",
        "",
    )
    print("  fetch con reintento sin CORS")

# 3) Trata como opaca cuando no se pudo leer
t = t.replace(
    'if (respuesta.type === "opaque") {',
    'if (respuesta.type === "opaque" || respuesta.status === 0) {',
)

ruta.write_text(t, encoding="utf-8", newline="\n")

r = subprocess.run(["node", "--check", "src/js/formulario.js"], cwd=RAIZ, capture_output=True, text=True)
print("  formulario.js:", "OK" if r.returncode == 0 else r.stderr[:400])

for comando in (["node", "scripts/build-index-html.mjs"], ["node", "build.mjs"]):
    rr = subprocess.run(comando, cwd=RAIZ, capture_output=True, text=True)
    print("  ", comando[-1], "->", "OK" if rr.returncode == 0 else rr.stderr[:200])
