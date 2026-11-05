"""Evidencia final de la segunda ronda de arte."""

from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "docs" / "capturas"
SALIDA.mkdir(parents=True, exist_ok=True)

EVIDENCIA = [
    ("fin2-hero.png", "01-hero-escritorio.jpg", None),
    ("fin2-movil.png", "02-hero-movil.jpg", (0, 0, 390, 844)),
    ("fin2-vehiculo.png", "03-producto-escenario.jpg", None),
    ("fin2-problema.png", "04-problema-editorial.jpg", None),
    ("fin2-beneficios.png", "05-beneficios.jpg", None),
    ("fin2-remolque.png", "06-carga-remolque.jpg", None),
    ("fin2-oferta.png", "07-promocion.jpg", None),
    ("fin2-cotizacion.png", "08-formulario.jpg", None),
    ("fin2-cierre.png", "09-cierre.jpg", None),
]

for origen, destino, caja in EVIDENCIA:
    ruta = RAIZ / origen
    if not ruta.exists():
        print(f"  falta {origen}")
        continue
    with Image.open(ruta) as im:
        if caja:
            im = im.crop(caja)
        im.convert("RGB").save(SALIDA / destino, "JPEG", quality=84, optimize=True, progressive=True)
    print(f"  {destino}")

# Elimina duplicados de la ronda anterior que ya no corresponden
for viejo in ("06-promocion.jpg", "07-formulario.jpg", "08-cierre.jpg"):
    ruta = SALIDA / viejo
    if ruta.exists():
        ruta.unlink()
        print(f"  eliminado {viejo}")

for patron in ("fin2-*.png", "s5-*.png", "s6-*.png", "s7-*.png", "s8-*.png", "s9-*.png",
               "sA-*.png", "cc-*.png"):
    for ruta in RAIZ.glob(patron):
        if ruta.is_file():
            ruta.unlink()
print("  temporales eliminados")
