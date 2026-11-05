"""Quita los avisos de campaña del formulario (columna y tarjeta)."""

import re
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sec = RAIZ / "src/sections/11-cotizacion.html"
h = sec.read_text(encoding="utf-8")

# 1) Nota de la columna izquierda
h = h.replace('        <p class="disclaimer cotiza__nota" data-form-privacidad-nota></p>\n', "")
h = h.replace('  <p class="disclaimer cotiza__nota" data-form-privacidad-nota></p>\n', "")
h = h.replace('<p class="disclaimer cotiza__nota" data-form-privacidad-nota></p>', "")

# 2) Aviso dentro de la tarjeta del formulario
patron = re.compile(r'\s*<p class="form__legal">.*?</p>', re.S)
h, cuantos = patron.subn("", h)
print("  avisos de la tarjeta eliminados:", cuantos)

sec.write_text(h, encoding="utf-8", newline="\n")

for comando in (["node", "scripts/build-index-html.mjs"], ["node", "build.mjs"]):
    r = subprocess.run(comando, cwd=RAIZ, capture_output=True, text=True)
    print("  ", comando[-1], "->", "OK" if r.returncode == 0 else r.stderr[:200])

html = (RAIZ / "index.html").read_text(encoding="utf-8")
print("  «página de campaña» en el formulario:", "página de campaña" in html)
print("  «dar seguimiento a tu solicitud»:", "dar seguimiento a tu solicitud" in html)
