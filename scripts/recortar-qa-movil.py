"""Recorta las capturas móviles al viewport real simulado (390x844)."""

from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
ANCHO, ALTO = 390, 844
recortadas = 0

for ruta in sorted(RAIZ.glob("qa-m-*.png")):
    if ruta.name == "qa-m-direct.png":
        continue
    with Image.open(ruta) as im:
        if im.width <= ANCHO and im.height <= ALTO:
            continue
        recorte = im.crop((0, 0, ANCHO, ALTO))
        recorte.save(ruta, optimize=True)
        recortadas += 1

print(f"  Recortadas {recortadas} capturas móviles a {ANCHO}x{ALTO}")
