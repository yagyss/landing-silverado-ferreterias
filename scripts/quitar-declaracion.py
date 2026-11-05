"""Quita la sección de declaración (redundante) y revisa el estado del selector."""

import html as htmllib
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# ---------------------------------------------------- 1. Estado del selector
dom = RAIZ / "demo-dom.html"
if dom.exists():
    texto = dom.read_text(encoding="utf-8", errors="replace")
    m = re.search(r'<pre id="resultado-color">(.*?)</pre>', texto, re.S)
    print("estado del selector:", htmllib.unescape(m.group(1)) if m else "sin datos")
    activos = re.findall(r'data-color-img="([^"]+)"[^>]*class="([^"]*)"', texto)
    print("imágenes con clase:", activos[:3])
    marcados = re.findall(r'data-color="([^"]+)"[^>]*aria-checked="([^"]+)"', texto)
    print("botones aria-checked:", marcados[:5])

# --------------------------------------- 2. Quitar la sección de declaración
render = RAIZ / "lib/render.mjs"
t = render.read_text(encoding="utf-8")
if '"01a-declaracion",' in t:
    t = t.replace('  "01a-declaracion",\n', "")
    render.write_text(t, encoding="utf-8", newline="\n")
    print("  declaración fuera del ensamblado")

seccion = RAIZ / "src/sections/01a-declaracion.html"
if seccion.exists():
    seccion.unlink()
    print("  archivo 01a-declaracion.html eliminado")

# ----------------------------------- 3. Revisar si queda alguna referencia rota
referencias = []
for ruta in (RAIZ / "src").rglob("*"):
    if ruta.is_file() and ruta.suffix in {".html", ".js", ".mjs", ".css"}:
        contenido = ruta.read_text(encoding="utf-8", errors="replace")
        if "declaracion" in contenido:
            referencias.append(ruta.relative_to(RAIZ))
print("  archivos que aún mencionan 'declaracion':")
for ruta in referencias:
    print("   -", ruta)
