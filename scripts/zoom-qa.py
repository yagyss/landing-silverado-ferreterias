from PIL import Image

# Recorta zonas dudosas de las capturas para inspeccionarlas de cerca.
trabajos = [
    ("qa-d-vehiculo.png", (110, 590, 760, 900), "zoom-solucion.png"),
    ("qa-d-inicio.png", (700, 240, 1330, 760), "zoom-showcase.png"),
]

for origen, caja, destino in trabajos:
    try:
        im = Image.open(origen)
    except FileNotFoundError:
        print(f"falta {origen}")
        continue
    recorte = im.crop(caja)
    recorte = recorte.resize((recorte.width * 2, recorte.height * 2), Image.LANCZOS)
    recorte.save(destino)
    print(destino, recorte.size)
