"""WhatsApp real (+52 55 8051 6601) y mensaje del formulario enfocado a llenarlo."""

import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- site.js
site = RAIZ / "src/data/site.js"
s = site.read_text(encoding="utf-8")

s = s.replace('    telefono: "", // ej. "+52 55 1234 5678"', '    telefono: "+52 55 8051 6601",')
s = s.replace('    numero: "",', '    numero: "5215580516601",')
s = s.replace('    etiqueta: "Cotiza por WhatsApp",', '    etiqueta: "Solicitar cotización",')

# Textos que invitaban a resolver por mensaje dentro del formulario
s = s.replace(
    '"No pudimos registrar tu solicitud en este momento. Intenta de nuevo o escríbenos por WhatsApp; tus datos no se perdieron."',
    '"No pudimos registrar tu solicitud en este momento. Intenta de nuevo en unos segundos; tus datos no se perdieron."',
)
site.write_text(s, encoding="utf-8", newline="\n")
print("  site.js: teléfono y WhatsApp configurados")

# ------------------------------------------------------- sección 11 (HTML)
sec = RAIZ / "src/sections/11-cotizacion.html"
h = sec.read_text(encoding="utf-8")

bloque_viejo = """        <div class="cotiza__alt">
          <p class="cotiza__alt-text">¿Prefieres resolverlo por mensaje?</p>
          <a class="btn btn--ghost" href="#cotizacion" data-wa-form data-cta="form-whatsapp">
            <span>Escríbenos por WhatsApp</span>
          </a>
        </div>"""

bloque_nuevo = """        <div class="cotiza__alt">
          <p class="cotiza__alt-text">
            <strong>Llena tus datos</strong> y un asesor te contacta con disponibilidad,
            versiones y opciones de compra.
          </p>
          <p class="cotiza__alt-nota">
            Cotización sin costo y sin compromiso. Recibes tu folio al enviar.
          </p>
        </div>"""

if bloque_viejo in h:
    h = h.replace(bloque_viejo, bloque_nuevo)
    print("  formulario: mensaje enfocado a llenar el formulario")
else:
    print("  (no se encontró el bloque alternativo de WhatsApp)")

# Estado de éxito: quitar el botón de WhatsApp (ahora solo el flotante)
h = h.replace(
    """            <a class="btn btn--primary" href="#cotizacion" data-wa-form data-cta="success-whatsapp">Continuar por WhatsApp</a>
            <button class="btn btn--ghost" type="button" data-success-reset>Enviar otra solicitud</button>""",
    """            <button class="btn btn--primary" type="button" data-success-reset>Enviar otra solicitud</button>""",
)
sec.write_text(h, encoding="utf-8", newline="\n")
print("  formulario: sin botón de WhatsApp interno")

# -------------------------------------------------------- Apps Script
gs = RAIZ / "docs" / "google-apps-script.gs"
g = gs.read_text(encoding="utf-8")
g = g.replace('WHATSAPP: "5215500000000",', 'WHATSAPP: "5215580516601",')
g = g.replace('TELEFONO: "+52 55 0000 0000",', 'TELEFONO: "+52 55 8051 6601",')
gs.write_text(g, encoding="utf-8", newline="\n")
print("  Apps Script: WhatsApp y teléfono reales")

# ------------------------------------------------------------------- CSS
css = RAIZ / "src/styles/apple.css"
c = css.read_text(encoding="utf-8")
if ".cotiza__alt-nota" not in c:
    c = c.rstrip() + """

/* Nota bajo el mensaje del formulario */
.cotiza__alt {
  display: grid;
  gap: 0.35rem;
}

.cotiza__alt-nota {
  margin: 0;
  font-size: 0.86rem;
  color: var(--text-soft, #7c8798);
}
"""
    css.write_text(c, encoding="utf-8", newline="\n")
    print("  CSS de la nota agregado")

# ------------------------------------------------------------ reconstruir
for comando in (["node", "scripts/build-index-html.mjs"], ["node", "build.mjs"]):
    r = subprocess.run(comando, cwd=RAIZ, capture_output=True, text=True)
    print("  ", comando[-1], "->", "OK" if r.returncode == 0 else r.stderr[:200])

html = (RAIZ / "index.html").read_text(encoding="utf-8")
print("  número en index.html:", "5215580516601" in html)
print("  texto nuevo:", "Llena tus datos" in html)
print("  botón interno de WhatsApp eliminado:", "Escríbenos por WhatsApp" not in html)
