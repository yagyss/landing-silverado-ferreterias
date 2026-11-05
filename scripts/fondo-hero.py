"""
Fondo del hero: horizonte de desierto (sin vehículo) a partir del póster.

Se toma una franja limpia de cielo y cerros del material del cliente, se
espeja para formar un panorama, se difumina y se funde con un piso oscuro.
La camioneta recortada (que cambia de color) se coloca encima.
"""

from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

RAIZ = Path(__file__).resolve().parent.parent
POSTER = RAIZ / "assets/vehiculos/silverado/_originales/campana-remolque.png"
DESTINO = RAIZ / "assets/vehiculos/silverado"

W, H = 2400, 1350

poster = Image.open(POSTER).convert("RGB")
print("póster:", poster.size)

# Franja limpia: cielo arriba, cerros al centro, sin texto ni camioneta
franja = poster.crop((0, 520, 286, 686))  # franja limpia del extremo izquierdo

# Panorama por espejo (evita repetir el mismo lado)
espejo = franja.transpose(Image.FLIP_LEFT_RIGHT)
panorama = Image.new("RGB", (franja.width * 2, franja.height))
panorama.paste(franja, (0, 0))
panorama.paste(espejo, (franja.width, 0))

alto_horizonte = int(H * 0.62)
horizonte = panorama.resize((W, alto_horizonte), Image.LANCZOS).filter(
    ImageFilter.GaussianBlur(16)
)

lienzo = Image.new("RGB", (W, H), (6, 8, 13))
lienzo.paste(horizonte, (0, 0))

datos = np.array(lienzo).astype(np.float32)
ys = np.arange(H)[:, None].astype(np.float32)
xs = np.arange(W)[None, :].astype(np.float32)

# --- Piso oscuro con reflejo cálido ---
inicio_piso = int(H * 0.30)
progreso = np.clip((ys - inicio_piso) / (H - inicio_piso), 0, 1)
arriba = np.array([38, 31, 24], dtype=np.float32)
abajo = np.array([4, 6, 10], dtype=np.float32)
color_piso = arriba * (1 - progreso[..., None]) + abajo * progreso[..., None]
mezcla = np.clip(progreso / 0.42, 0, 1)[..., None]
datos = datos * (1 - mezcla) + color_piso * mezcla

# --- Viñeta ---
cx, cy = W * 0.64, H * 0.30
dist = np.sqrt(((xs - cx) / (W * 0.75)) ** 2 + ((ys - cy) / (H * 0.80)) ** 2)
vineta = np.clip(dist - 0.30, 0, 1)[..., None] * 0.8
datos = datos * (1 - vineta)

# --- Halo de atardecer a la derecha ---
halo = (
    np.exp(-(((xs - W * 0.84) / (W * 0.24)) ** 2))
    * np.exp(-(((ys - H * 0.16) / (H * 0.28)) ** 2))
)[..., None]
datos = datos + halo * np.array([52, 33, 12], dtype=np.float32)

# --- Oscurecer la zona del texto (izquierda) ---
oscuro = np.clip(1 - (xs / (W * 0.50)), 0, 1)[..., None] * 0.60
datos = datos * (1 - oscuro)

# --- Grano sutil ---
ruido = np.random.default_rng(11).normal(0, 3.0, (H, W, 1)).astype(np.float32)
datos = datos + ruido

final = Image.fromarray(np.clip(datos, 0, 255).astype(np.uint8))

for ancho, sufijo in ((2000, "2000"), (1200, "1200")):
    alto = round(final.height * ancho / final.width)
    redim = final.resize((ancho, alto), Image.LANCZOS)
    salida = DESTINO / f"fondo-hero-{sufijo}.webp"
    redim.save(salida, "WEBP", quality=86, method=6)
    print(f"  {salida.name} {redim.size} {(salida.stat().st_size/1024):.0f} kB")

previa = final.copy()
previa.thumbnail((1200, 1200), Image.LANCZOS)
previa.save(RAIZ / "preview-fondo-hero.jpg", quality=88)
