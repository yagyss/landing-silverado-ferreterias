"""Corrige el bloque CSS de los CTA (selectores con comillas y texto sin mojibake)."""

import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ruta = RAIZ / "src" / "styles" / "apple.css"
texto = ruta.read_text(encoding="utf-8", errors="replace")

# Quita el bloque mal escrito (comentario + regla)
patron = re.compile(
    r"\n*/\* Los CTA de formulario.*?\}\s*$",
    re.S,
)
texto_sin = patron.sub("\n", texto)
if texto_sin == texto:
    # Variante: buscar solo la regla mal formada
    texto_sin = re.sub(r"\n*a\[href=#cotizacion\]\.btn,[^{]*\{[^}]*\}\s*", "\n", texto)

bloque = """
/* Llamadas a la acción del formulario: misma caja tipográfica que el botón del
   hero, siempre con el texto «Solicitar cotización». */
a[href="#cotizacion"].btn,
a[href="#cotizacion"].localnav__cta {
  text-transform: none;
  letter-spacing: 0.01em;
  font-weight: 700;
}
"""

ruta.write_text(texto_sin.rstrip() + "\n" + bloque, encoding="utf-8", newline="\n")

actual = ruta.read_text(encoding="utf-8")
print("  selector correcto:", 'a[href="#cotizacion"].btn' in actual)
print("  mojibake restante:", "Ã" in actual or "Â" in actual)
print("  longitud:", len(actual), "caracteres")

# Reconstruir
import subprocess

for comando in (["node", "build.mjs"], ["node", "scripts/build-index-html.mjs"]):
    r = subprocess.run(comando, cwd=RAIZ, capture_output=True, text=True)
    print("  ", comando[-1], "->", "OK" if r.returncode == 0 else r.stderr[:200])

dist = (RAIZ / "dist" / "src" / "styles" / "apple.css").read_text(encoding="utf-8")
print("  en dist:", 'a[href="#cotizacion"].btn' in dist)
