"""Añade el nombre del color a cada swatch y reconstruye la página."""

import re
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

NOMBRES = {
    "rojo-lava": "Rojo Lava",
    "negro": "Negro",
    "blanco": "Blanco",
    "gris-tiburon": "Gris Tiburón",
    "arena-lunar": "Arena Lunar",
}

hero = RAIZ / "src/sections/01-hero.html"
t = hero.read_text(encoding="utf-8")

for slug, nombre in NOMBRES.items():
    # Añade data-nombre si el botón aún no lo tiene
    patron = r'(<button class="swatch"[^>]*data-color="' + re.escape(slug) + r'")'
    if f'data-color="{slug}"' in t and 'data-nombre=' not in t:
        t = re.sub(patron, r'\1 data-nombre="' + nombre + '"', t, count=1)

hero.write_text(t, encoding="utf-8", newline="\n")
print("  data-nombre agregado a los swatches")

# JS: usar el nombre del botón como respaldo
js = RAIZ / "src/js/showcase.js"
c = js.read_text(encoding="utf-8")

if "dataset.nombre" not in c:
    c = c.replace(
        "    // 3) Nombre y descripción\n    const color = porColor.get(id);\n    if (color) {\n      if (nombre) nombre.textContent = color.nombre;\n      if (descripcion) descripcion.textContent = color.descripcion;\n    }",
        "    // 3) Nombre y descripción (config, con respaldo en el propio botón)\n"
        "    const color = porColor.get(id);\n"
        "    const etiqueta = color?.nombre || lista.find((b) => b.dataset.color === id)?.dataset.nombre;\n"
        "    if (nombre && etiqueta) nombre.textContent = etiqueta;\n"
        "    if (descripcion && color) descripcion.textContent = color.descripcion;",
    )
    js.write_text(c, encoding="utf-8", newline="\n")
    print("  showcase.js con respaldo de nombre")

# Reconstrucción
for comando in (["node", "scripts/build-index-html.mjs"], ["node", "build.mjs"]):
    r = subprocess.run(comando, cwd=RAIZ, capture_output=True, text=True)
    print("  ", " ".join(comando), "->", "OK" if r.returncode == 0 else r.stderr[:200])

# Verificación básica del HTML resultante
html = (RAIZ / "index.html").read_text(encoding="utf-8")
print("  secciones en index:", html.count("<section"))
print("  declaración presente:", "01a-declaracion" in html or "declaracion__titulo" in html)
print("  swatches con nombre:", html.count("data-nombre="))
