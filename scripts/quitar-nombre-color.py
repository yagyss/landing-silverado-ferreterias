"""Quita la etiqueta 'COLOR / Rojo Lava' del selector del hero."""

import re
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
hero = RAIZ / "src/sections/01-hero.html"
t = hero.read_text(encoding="utf-8")

# Elimina el bloque <p class="hero__color">…</p> completo
patron = re.compile(r'\s*<p class="hero__color">.*?</p>', re.S)
t, n = patron.subn("", t)
print(f"  etiqueta de color eliminada: {n}")

hero.write_text(t, encoding="utf-8", newline="\n")

# Selector más compacto (solo los círculos)
css = RAIZ / "src/styles/apple.css"
c = css.read_text(encoding="utf-8")

bloque = """
/* Selector sin etiqueta: solo los círculos de color */
.hero__picker {
  gap: 0 !important;
  padding: 0.5rem 0.7rem !important;
  border-radius: var(--r-pill) !important;
}

.hero__color {
  display: none !important;
}

.hero__swatches {
  gap: 0.55rem !important;
}
"""

if "Selector sin etiqueta" not in c:
    css.write_text(c.rstrip() + "\n" + bloque, encoding="utf-8", newline="\n")
    print("  estilo compacto aplicado")

for comando in (["node", "scripts/build-index-html.mjs"], ["node", "build.mjs"]):
    r = subprocess.run(comando, cwd=RAIZ, capture_output=True, text=True)
    print("  ", comando[-1], "->", "OK" if r.returncode == 0 else r.stderr[:200])

html = (RAIZ / "index.html").read_text(encoding="utf-8")
print("  'Rojo Lava' en texto visible:", 'hero__color' in html.split("<body")[1].split("<script")[0])
print("  swatches:", html.count("data-color="))
