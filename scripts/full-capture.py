"""Recorta y comprime la captura de página completa de la landing."""

from pathlib import Path

import numpy as np
from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
origen = RAIZ / "full-raw.png"
destino = RAIZ / "docs" / "capturas" / "landing-completa.jpg"

with Image.open(origen) as im:
    im = im.convert("RGB")
    datos = np.array(im)
    alto, ancho, _ = datos.shape

    # Recorta las filas finales que sean de un solo color (relleno del viewport)
    fin = alto
    while fin > 10:
        fila = datos[fin - 1]
        if (fila == fila[0]).all():
            fin -= 1
        else:
            break

    recorte = im.crop((0, 0, ancho, fin))
    proporcion = 1200 / recorte.width
    recorte = recorte.resize((1200, round(recorte.height * proporcion)), Image.LANCZOS)
    recorte.save(destino, "JPEG", quality=80, optimize=True, progressive=True)
    print(f"  landing-completa.jpg {recorte.size} {(destino.stat().st_size/1024):.0f} kB")

origen.unlink(missing_ok=True)
