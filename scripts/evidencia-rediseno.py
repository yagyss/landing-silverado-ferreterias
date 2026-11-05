"""Evidencia del rediseño + limpieza de archivos temporales de revisión."""

from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "docs" / "capturas"
SALIDA.mkdir(parents=True, exist_ok=True)

# (origen, destino, recorte)
EVIDENCIA = [
    ("fin-hero.png", "01-hero-escritorio.jpg", None),
    ("fin-movil.png", "02-hero-movil.jpg", (0, 0, 390, 844)),
    ("fin-vehiculo.png", "03-producto-escenario.jpg", None),
    ("fin-problema.png", "04-problema-editorial.jpg", None),
    ("fin-beneficios.png", "05-beneficios.jpg", None),
    ("fin-oferta.png", "06-promocion.jpg", None),
    ("fin-cotizacion.png", "07-formulario.jpg", None),
    ("fin-cierre.png", "08-cierre.jpg", None),
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

# Limpieza de artefactos temporales
for patron in ("fin-*.png", "r-*.png", "e-*.png", "v2-*.png", "v3-*.png", "v4-*.png",
               "v5-*.png", "v6-*.png", "v7-*.png", "v8-*.png", "debug-*.png",
               "preview-*.png", "logo-roi-*.png", "qa-*.png"):
    for ruta in RAIZ.glob(patron):
        if ruta.is_file():
            ruta.unlink()
print("  temporales eliminados")
