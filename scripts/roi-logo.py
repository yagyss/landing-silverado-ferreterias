from PIL import Image
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
poster = Image.open(RAIZ / "assets/vehiculos/silverado/_originales/campana-remolque.png").convert("RGB")
print("poster:", poster.size)

# Recortes candidatos de la zona del logotipo (parte superior del póster)
for i, caja in enumerate([(250, 40, 900, 150), (280, 50, 880, 140), (300, 60, 860, 130)]):
    rec = poster.crop(caja)
    rec = rec.resize((rec.width * 2, rec.height * 2), Image.LANCZOS)
    destino = RAIZ / f"logo-roi-{i}.png"
    rec.save(destino)
    print(destino.name, rec.size)
