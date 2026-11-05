"""
Extrae los recursos con transparencia a partir del material original del cliente:

1) `assets/marca/chevrolet-lockup.png`
   Logotipo oficial (bowtie + wordmark) recortado del póster de campaña que
   proporcionó el cliente. Se elimina el cielo azul con relleno desde los bordes,
   de modo que los reflejos metálicos interiores se conservan.

2) `assets/vehiculos/silverado/cutout-<color>-1400.webp`
   Tomas de catálogo con el fondo blanco de estudio recortado, para poder
   colocarlas sobre escenarios oscuros (hero cinematográfico). Se eliminan los
   píxeles de fondo conectados al borde y se recorta la sombra gris de estudio
   (la página dibuja su propia sombra/reflejo con CSS).

Los bordes se "descontaminan" contra el color de fondo original para evitar el
halo claro típico de un recorte sobre blanco.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

RAIZ = Path(__file__).resolve().parent.parent
SILVERADO = RAIZ / "assets" / "vehiculos" / "silverado"
ORIGINALES = SILVERADO / "_originales"
MARCA = RAIZ / "assets" / "marca"

COLORES = ["rojo-lava", "negro", "blanco", "gris-tiburon", "arena-lunar"]


def relleno_desde_bordes(mascara: np.ndarray) -> np.ndarray:
    """Devuelve la región de `mascara` conectada con el borde de la imagen."""
    alcanzado = np.zeros_like(mascara, dtype=bool)
    alcanzado[0, :] |= mascara[0, :]
    alcanzado[-1, :] |= mascara[-1, :]
    alcanzado[:, 0] |= mascara[:, 0]
    alcanzado[:, -1] |= mascara[:, -1]
    while True:
        nuevo = alcanzado.copy()
        nuevo[1:, :] |= alcanzado[:-1, :]
        nuevo[:-1, :] |= alcanzado[1:, :]
        nuevo[:, 1:] |= alcanzado[:, :-1]
        nuevo[:, :-1] |= alcanzado[:, 1:]
        nuevo &= mascara
        if np.array_equal(nuevo, alcanzado):
            break
        alcanzado = nuevo
    return alcanzado


def descontaminar(rgb: np.ndarray, alfa: np.ndarray, color_fondo: np.ndarray) -> np.ndarray:
    """Quita el color de fondo mezclado en los píxeles semitransparentes."""
    salida = rgb.astype(np.float32)
    a = (alfa.astype(np.float32) / 255.0)[..., None]
    seguro = a > 0.02
    # color = (observado - fondo*(1-a)) / a
    recuperado = (salida - color_fondo * (1.0 - a)) / np.maximum(a, 1e-3)
    recuperado = np.clip(recuperado, 0, 255)
    salida = np.where(seguro, recuperado, salida)
    return salida.astype(np.uint8)


def extraer_lockup() -> None:
    origen = Image.open(ORIGINALES / "campana-remolque.png").convert("RGB")
    # Zona del logotipo en el póster (1122 x 1402)
    caja = (292, 56, 872, 138)
    recorte = np.array(origen.crop(caja)).astype(np.int16)
    alto, ancho, _ = recorte.shape

    r, g, b = recorte[..., 0], recorte[..., 1], recorte[..., 2]

    # "Azul de cielo": el canal azul domina claramente
    azul = (b > r + 16) & (b >= g - 2)
    fondo = relleno_desde_bordes(azul)

    # Contracanales interiores (por ejemplo, el hueco de la "O") que quedaron
    # encerrados por el logotipo: también son cielo, pero no tocan el borde.
    luminancia = 0.2126 * r + 0.7152 * g + 0.0722 * b
    azul_interior = (b > r + 22) & (b >= g + 8) & (luminancia > 60)
    fondo = fondo | azul_interior

    # Dilata un píxel para comer el borde anti-aliasing del cielo
    fondo_dil = fondo.copy()
    fondo_dil[1:, :] |= fondo[:-1, :]
    fondo_dil[:-1, :] |= fondo[1:, :]
    fondo_dil[:, 1:] |= fondo[:, :-1]
    fondo_dil[:, :-1] |= fondo[:, 1:]

    alfa = np.where(fondo_dil, 0, 255).astype(np.uint8)
    imagen_alfa = Image.fromarray(alfa, "L").filter(ImageFilter.GaussianBlur(0.6))
    alfa = np.array(imagen_alfa)

    # Color de fondo estimado en las esquinas superiores
    muestra = np.concatenate([recorte[:4, :40].reshape(-1, 3), recorte[:4, -40:].reshape(-1, 3)])
    fondo_rgb = np.median(muestra, axis=0)

    limpio = descontaminar(np.array(recorte, dtype=np.uint8), alfa, fondo_rgb)
    resultado = np.dstack([limpio, alfa])
    imagen = Image.fromarray(resultado, "RGBA")

    # Recorta al contenido real
    caja_contenido = imagen.getbbox()
    imagen = imagen.crop(caja_contenido)
    MARCA.mkdir(parents=True, exist_ok=True)
    imagen.save(MARCA / "chevrolet-lockup.png")
    print(f"  chevrolet-lockup.png {imagen.size}")

    # Vista previa sobre fondo oscuro y claro
    for nombre, fondo in (("oscuro", (11, 14, 19)), ("claro", (244, 245, 247))):
        lienzo = Image.new("RGB", imagen.size, fondo)
        lienzo.paste(imagen, (0, 0), imagen)
        lienzo.save(RAIZ / f"preview-lockup-{nombre}.png")

    # Bowtie solo (para el encabezado): se separa por la columna vacía que hay
    # entre el emblema y el wordmark.
    alfa_lockup = np.array(imagen.split()[-1])
    columnas = (alfa_lockup > 12).sum(axis=0)
    limite = int(imagen.width * 0.45)
    corte = limite
    for x in range(int(imagen.width * 0.08), limite):
        if columnas[x] == 0 and columnas[x + 1] == 0 and columnas[x + 2] == 0:
            corte = x
            break
    bowtie = imagen.crop((0, 0, corte, imagen.height))
    caja_bowtie = bowtie.getbbox()
    if caja_bowtie:
        bowtie = bowtie.crop(caja_bowtie)
    bowtie.save(MARCA / "chevrolet-bowtie.png")
    print(f"  chevrolet-bowtie.png {bowtie.size}")


def extraer_vehiculo(color: str) -> None:
    origen = Image.open(ORIGINALES / f"color-{color}.png").convert("RGB")
    rgb = np.array(origen)
    alto, ancho, _ = rgb.shape

    minimo = rgb.min(axis=2).astype(np.int16)
    maximo = rgb.max(axis=2).astype(np.int16)
    # Blanco de estudio: muy luminoso y neutro
    blanco = (minimo >= 246) & ((maximo - minimo) <= 6)
    fondo = relleno_desde_bordes(blanco)

    alfa = np.where(fondo, 0, 255).astype(np.uint8)

    # Sombra de estudio: gris neutro entre el vehículo y el fondo blanco. Se
    # propaga desde el fondo (ya transparente) para no comerse la carrocería,
    # que en la unidad blanca es mucho más luminosa (>225).
    luminancia = 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]
    ys = np.arange(alto)[:, None]
    neutro = (maximo - minimo) <= 12
    gris = neutro & (luminancia >= 45) & (luminancia <= 224) & (ys >= int(alto * 0.70))
    sombra = relleno_desde_bordes(gris | fondo) & gris
    alfa[sombra] = 0

    # Halo blanco dejado por el borde anti-aliasing de la sombra: se dilata la
    # zona de sombra y se limpian los grises claros de alrededor (las llantas
    # son oscuras, así que no se ven afectadas).
    mascara_sombra = Image.fromarray((sombra * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(9))
    halo = (np.array(mascara_sombra) > 0) & neutro & (luminancia >= 105)
    alfa[halo] = 0

    # Restos sueltos de sombra en la franja inferior (las llantas son oscuras)
    resto = neutro & (luminancia >= 150) & (luminancia <= 250) & (ys >= int(alto * 0.93))
    alfa[resto] = 0

    # Hueco de fondo encerrado por la sombra (bajo el chasis, entre ruedas):
    # para cada columna se localiza el último píxel "de camioneta" y se limpia
    # todo lo claro que quede por debajo. Las llantas y el chasis no se tocan.
    saturacion = maximo - minimo
    es_vehiculo = (luminancia < 50) | (saturacion > 30)
    indices = np.where(es_vehiculo, ys, -1)
    ultimo = indices.max(axis=0)
    debajo = ys > ultimo[None, :]
    claro = luminancia >= 105
    alfa[debajo & claro] = 0

    alfa = np.array(Image.fromarray(alfa, "L").filter(ImageFilter.GaussianBlur(0.7)))

    limpio = descontaminar(rgb, alfa, np.array([255, 255, 255], dtype=np.float32))
    imagen = Image.fromarray(np.dstack([limpio, alfa]), "RGBA")

    caja = imagen.getbbox()
    imagen = imagen.crop(caja)
    # Un pequeño margen para que el recorte respire
    margen = 6
    lienzo = Image.new("RGBA", (imagen.width + margen * 2, imagen.height + margen * 2), (0, 0, 0, 0))
    lienzo.paste(imagen, (margen, margen))

    for ancho_objetivo, sufijo in ((1400, "1400"), (900, "900")):
        if lienzo.width > ancho_objetivo:
            proporcion = ancho_objetivo / lienzo.width
            redimension = lienzo.resize(
                (ancho_objetivo, round(lienzo.height * proporcion)), Image.LANCZOS
            )
        else:
            redimension = lienzo
        destino = SILVERADO / f"cutout-{color}-{sufijo}.webp"
        redimension.save(destino, "WEBP", quality=88, method=6, exact=True)
        print(f"  cutout-{color}-{sufijo}.webp {redimension.size} {(destino.stat().st_size/1024):.1f} kB")

    # Vista previa sobre fondo oscuro (el escenario real del hero)
    previa = Image.new("RGB", (lienzo.width, lienzo.height), (10, 13, 20))
    previa.paste(lienzo, (0, 0), lienzo)
    previa.thumbnail((900, 900), Image.LANCZOS)
    previa.save(RAIZ / f"preview-vehiculo-{color}.png")


if __name__ == "__main__":
    print("Logotipo oficial:")
    extraer_lockup()
    print("\nRecortes de vehículo:")
    for nombre in COLORES:
        extraer_vehiculo(nombre)
