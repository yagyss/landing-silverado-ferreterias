"""Revierte la integración del visor 360 y deja la página en su versión estable."""

import re
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- CSS
css = RAIZ / "src/styles/apple.css"
texto = css.read_text(encoding="utf-8")
marca = "VISOR INTERACTIVO"
if marca in texto:
    corte = texto.index(marca)
    # Retrocede hasta el inicio del comentario de bloque que abre la sección
    inicio = texto.rfind("/*", 0, corte)
    texto = texto[:inicio].rstrip() + "\n"
    css.write_text(texto, encoding="utf-8", newline="\n")
    print("  CSS del visor retirado")

# ---------------------------------------------------------------- HTML
hero = RAIZ / "src/sections/01-hero.html"
t = hero.read_text(encoding="utf-8")

t = t.replace(" data-spin data-spin-stage", "")
t = t.replace(" data-spin-stack", "")

# Quita la pista de arrastre
t = re.sub(r'\s*<span class="hero__hint"[^>]*>.*?</span>', "", t, flags=re.S)

hero.write_text(t, encoding="utf-8", newline="\n")
print("  hero sin visor:", "data-spin" not in t)

# ----------------------------------------------------------------- JS
main = RAIZ / "src/js/main.js"
m = main.read_text(encoding="utf-8")
m = m.replace('import { initSpin } from "./spin.js";\n', "")
m = m.replace('    ["spin", initSpin],\n', "")
main.write_text(m, encoding="utf-8", newline="\n")
print("  main.js sin initSpin")

spin = RAIZ / "src/js/spin.js"
if spin.exists():
    spin.unlink()
    print("  spin.js eliminado")

# ------------------------------------------------------- Configuración
site = RAIZ / "src/data/site.js"
s = site.read_text(encoding="utf-8")
if "angulos: []" in s:
    s = re.sub(
        r"    /\*\* Secuencia de fotogramas.*?\*/\n    angulos: \[\],\n",
        "",
        s,
        flags=re.S,
    )
    site.write_text(s, encoding="utf-8", newline="\n")
    print("  site.js limpio (angulos)")

# --------------------------------------------------------- Reconstruir
for comando in (["node", "scripts/build-index-html.mjs"], ["node", "build.mjs"]):
    r = subprocess.run(comando, cwd=RAIZ, capture_output=True, text=True)
    print("  ", comando[-1], "->", "OK" if r.returncode == 0 else r.stderr[:200])

for archivo in ("src/js/main.js",):
    r = subprocess.run(["node", "--check", archivo], cwd=RAIZ, capture_output=True, text=True)
    print(f"  {archivo}: {'OK' if r.returncode == 0 else 'ERROR'}")

html = (RAIZ / "index.html").read_text(encoding="utf-8")
print("  data-spin restante:", html.count("data-spin"))
print("  hero__hint restante:", html.count("hero__hint"))
print("  swatches:", html.count("data-color="))
