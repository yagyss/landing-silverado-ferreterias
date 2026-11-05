"""Ajusta el mensaje del formulario: invita a completarlo y quita el folio."""

import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sec = RAIZ / "src/sections/11-cotizacion.html"
h = sec.read_text(encoding="utf-8")

viejo = """        <div class="cotiza__alt">
          <p class="cotiza__alt-text">
            <strong>Llena tus datos</strong> y un asesor te contacta con disponibilidad,
            versiones y opciones de compra.
          </p>
          <p class="cotiza__alt-nota">
            Cotización sin costo y sin compromiso. Recibes tu folio al enviar.
          </p>
        </div>"""

nuevo = """        <div class="cotiza__alt">
          <p class="cotiza__alt-text">
            <strong>Completa el siguiente formulario</strong>: son cinco datos y un asesor te
            contacta con disponibilidad, versiones y opciones de compra.
          </p>
          <p class="cotiza__alt-nota">
            Cotización sin costo y sin compromiso.
          </p>
        </div>"""

if viejo in h:
    h = h.replace(viejo, nuevo)
    sec.write_text(h, encoding="utf-8", newline="\n")
    print("  mensaje actualizado y folio eliminado")
else:
    print("  (no se encontró el bloque exacto; revisar)")

for comando in (["node", "scripts/build-index-html.mjs"], ["node", "build.mjs"]):
    r = subprocess.run(comando, cwd=RAIZ, capture_output=True, text=True)
    print("  ", comando[-1], "->", "OK" if r.returncode == 0 else r.stderr[:200])

html = (RAIZ / "index.html").read_text(encoding="utf-8")
print("  texto nuevo:", "Completa el siguiente formulario" in html)
print("  mención de folio en el bloque:", "Recibes tu folio" in html)
