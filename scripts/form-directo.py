"""Permite enviar el formulario directo al Apps Script (incluido file://)."""

from pathlib import Path
import re
import subprocess

RAIZ = Path(__file__).resolve().parent.parent
URL = "https://script.google.com/macros/s/AKfycbwj3hEDWUEcZa94a1ZThZHK4lWbJW7CsmGysRbXUayBrJcTV-MNWNHSd6BcZCZigBua/exec"

# ------------------------------------------------------------- site.js
site = RAIZ / "src/data/site.js"
t = site.read_text(encoding="utf-8")

if "endpointRemoto" not in t:
    t = t.replace(
        '    endpoint: "/api/cotizacion",',
        '    endpoint: "/api/cotizacion",\n'
        '    /** Destino directo cuando la página se abre como archivo (file://).\n'
        '     *  Publicado en Netlify se usa el proxy /api/cotizacion. */\n'
        f'    endpointRemoto: "{URL}",',
    )
    site.write_text(t, encoding="utf-8", newline="\n")
    print("  site.js: endpointRemoto agregado")

# -------------------------------------------------------- formulario.js
js = RAIZ / "src/js/formulario.js"
c = js.read_text(encoding="utf-8")

# 1) Sustituye el bloqueo de file:// por envío directo
bloqueo = """    if (window.location.protocol === "file:") {
      mostrarEstado(
        "Vista de revisión: para enviar la solicitud abre la página con el servidor local (node server.mjs) o publícala con el formulario conectado a Google Sheets.",
        "error",
      );
      return;
    }

"""

if bloqueo in c:
    c = c.replace(bloqueo, "")
    print("  formulario.js: sin bloqueo de file://")

# 2) Endpoint según protocolo
viejo_fetch = """      const respuesta = await fetch(SITE.formulario.endpoint, {
        method: "POST",
        headers: { "content-type": "application/json" },"""

nuevo_fetch = """      // Abierto como archivo se envía directo al Apps Script (sin proxy).
      const esArchivo = window.location.protocol === "file:";
      const destino =
        esArchivo && SITE.formulario.endpointRemoto
          ? SITE.formulario.endpointRemoto
          : SITE.formulario.endpoint;

      const respuesta = await fetch(destino, {
        method: "POST",
        // Con file:// el navegador no permite leer la respuesta (CORS),
        // así que se usa una petición simple y se informa con honestidad.
        mode: esArchivo ? "no-cors" : "cors",
        headers: {
          "content-type": esArchivo ? "text/plain;charset=utf-8" : "application/json",
        },"""

if viejo_fetch in c:
    c = c.replace(viejo_fetch, nuevo_fetch)
    print("  formulario.js: fetch por protocolo")

# 3) Sin cuerpo JSON cuando la respuesta es opaca
viejo_parse = """      let cuerpo = {};
      try {
        cuerpo = await respuesta.json();
      } catch {
        cuerpo = {};
      }"""

nuevo_parse = """      let cuerpo = {};
      if (respuesta.type !== "opaque") {
        try {
          cuerpo = await respuesta.json();
        } catch {
          cuerpo = {};
        }
      }

      // Envío desde archivo: la petición salió, pero el navegador no puede
      // leer la respuesta. Se confirma sólo lo que sí sabemos.
      if (respuesta.type === "opaque") {
        if (exito) {
          exito.hidden = false;
          exito.querySelector("[data-success-titulo]").textContent = "Solicitud enviada";
          exito.querySelector("[data-success-mensaje]").textContent =
            "Tu solicitud salió hacia la hoja de cotizaciones. Un asesor te contactará. " +
            "Si no recibes confirmación en unos minutos, escríbenos por WhatsApp.";
          exito.querySelector("[data-success-folio-wrap]").hidden = true;
          form.hidden = true;
          exito.scrollIntoView({ behavior: "smooth", block: "center" });
        }
        trackLead({ folio: "", modo: "archivo-local" });
        return;
      }"""

if viejo_parse in c:
    c = c.replace(viejo_parse, nuevo_parse)
    print("  formulario.js: manejo de respuesta opaca")

js.write_text(c, encoding="utf-8", newline="\n")

# ------------------------------------------------------------ reconstruir
for comando in (["node", "scripts/build-index-html.mjs"], ["node", "build.mjs"]):
    r = subprocess.run(comando, cwd=RAIZ, capture_output=True, text=True)
    print("  ", comando[-1], "->", "OK" if r.returncode == 0 else r.stderr[:200])

r = subprocess.run(["node", "--check", "src/js/formulario.js"], cwd=RAIZ, capture_output=True, text=True)
print("  formulario.js:", "OK" if r.returncode == 0 else r.stderr[:300])

html = (RAIZ / "index.html").read_text(encoding="utf-8")
print("  endpoint remoto en index:", "script.google.com/macros/s/AKfycbw" in html)
print("  bloqueo file:// eliminado:", "Vista de revisión: para enviar" not in html)
