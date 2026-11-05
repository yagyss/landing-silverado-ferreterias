"""Prepara las capturas de evidencia para la documentación y limpia el QA temporal."""

from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "docs" / "capturas"
SALIDA.mkdir(parents=True, exist_ok=True)

EVIDENCIA = [
    ("qa-d-inicio.png", "01-hero-escritorio.jpg"),
    ("qa-m-inicio.png", "02-hero-movil.jpg"),
    ("qa-d-oferta.png", "03-promocion.jpg"),
    ("qa-d-comparativa.png", "04-comparativa.jpg"),
    ("qa-d-cotizacion.png", "05-formulario.jpg"),
    ("qa-d-cierre.png", "06-cierre.jpg"),
]

for origen, destino in EVIDENCIA:
    ruta = RAIZ / origen
    if not ruta.exists():
        print(f"  falta {origen}")
        continue
    with Image.open(ruta) as im:
        im.convert("RGB").save(SALIDA / destino, "JPEG", quality=84, optimize=True, progressive=True)
    print(f"  {destino}")

# Limpieza de artefactos temporales de revisión
patrones = ["qa-*.png", "qa-*.html", "qa-*.html.err", "zoom-*.png"]
borrados = 0
for patron in patrones:
    for ruta in RAIZ.glob(patron):
        if ruta.is_file():
            ruta.unlink()
            borrados += 1

print(f"  archivos temporales eliminados: {borrados}")
