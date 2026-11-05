"""Actualiza la evidencia de la promoción y limpia temporales."""

from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "docs" / "capturas" / "07-promocion.jpg"

origen = RAIZ / "o2-oferta.png"
if origen.exists():
    with Image.open(origen) as im:
        im.convert("RGB").save(DESTINO, "JPEG", quality=84, optimize=True, progressive=True)
    print("  07-promocion.jpg actualizado")

for patron in ("o-*.png", "o2-*.png"):
    for ruta in RAIZ.glob(patron):
        if ruta.is_file():
            ruta.unlink()
print("  temporales eliminados")
