"""Agrega data-nombre a los cinco swatches (idempotente) y reconstruye."""

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
    patron = re.compile(
        r'(<button class="swatch"(?:(?!>).)*?data-color="' + re.escape(slug) + r'")(?![^>]*data-nombre)',
        re.S,
    )
    t, n = patron.subn(r'\1 data-nombre="' + nombre + '"', t, count=1)
    print(f"  {slug}: {'agregado' if n else 'ya tenía'}")

hero.write_text(t, encoding="utf-8", newline="\n")

for comando in (["node", "scripts/build-index-html.mjs"], ["node", "build.mjs"]):
    r = subprocess.run(comando, cwd=RAIZ, capture_output=True, text=True)
    print("  ", comando[-1], "->", "OK" if r.returncode == 0 else r.stderr[:200])

html = (RAIZ / "index.html").read_text(encoding="utf-8")
print("  swatches con data-nombre:", html.count("data-nombre="))
print("  secciones:", html.count("<section"))
