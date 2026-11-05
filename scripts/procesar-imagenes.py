"""
Procesa las fotografías originales de la Chevrolet Silverado para la landing page.

- Recorta el margen blanco de las tomas de catálogo (mismo ángulo, distinto color).
- Genera variantes WebP responsivas (evita servir PNG pesados).
- Crea un recorte cinematográfico del póster de campaña para el CTA final.
- Genera la imagen Open Graph (1200x630) para Meta Ads / WhatsApp.

Uso:  python scripts/procesar-imagenes.py
Requiere Pillow (incluido en el runtime del proyecto).
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "assets" / "vehiculos" / "silverado"
ORIGINALES = ENTRADA / "_originales"
CALIDAD = 82
BLANCO = 250  # umbral de "blanco de estudio"


def recortar_fondo_blanco(im: Image.Image, margen: int = 12) -> Image.Image:
    """Recorta el marco blanco de una toma de catálogo sobre fondo blanco."""
    rgb = im.convert("RGB")
    escala = 4
    mini = rgb.resize((max(1, rgb.width // escala), max(1, rgb.height // escala)))
    mascara = mini.convert("L").point(lambda v: 0 if v >= BLANCO else 255)
    caja = mascara.getbbox()
    if not caja:
        return rgb
    x0, y0, x1, y1 = [v * escala for v in caja]
    x0 = max(0, x0 - margen)
    y0 = max(0, y0 - margen)
    x1 = min(rgb.width, x1 + margen)
    y1 = min(rgb.height, y1 + margen)
    # Ajuste fino a resolución completa dentro de la caja detectada
    fino = rgb.crop((x0, y0, x1, y1))
    mascara_fina = fino.convert("L").point(lambda v: 0 if v >= 252 else 255)
    caja_fina = mascara_fina.getbbox()
    if caja_fina:
        fx0, fy0, fx1, fy1 = caja_fina
        fino = fino.crop(
            (
                max(0, fx0 - margen),
                max(0, fy0 - margen),
                min(fino.width, fx1 + margen),
                min(fino.height, fy1 + margen),
            )
        )
    return fino


def guardar_webp(im: Image.Image, destino: Path, ancho_objetivo: int) -> Path:
    if im.width > ancho_objetivo:
        alto = round(im.height * ancho_objetivo / im.width)
        im = im.resize((ancho_objetivo, alto), Image.LANCZOS)
    destino.parent.mkdir(parents=True, exist_ok=True)
    im.save(destino, "WEBP", quality=CALIDAD, method=6)
    kb = destino.stat().st_size / 1024
    print(f"  {destino.name:<44} {im.width}x{im.height}  {kb:6.1f} kB")
    return destino


def procesar_color(nombre: str) -> None:
    origen = ORIGINALES / nombre
    im = Image.open(origen)
    im = recortar_fondo_blanco(im)
    base = nombre.replace("color-", "").replace(".png", "")
    guardar_webp(im, ENTRADA / f"color-{base}-1400.webp", 1400)
    guardar_webp(im, ENTRADA / f"color-{base}-900.webp", 900)


def procesar_simple(nombre: str, salida: str, anchos: tuple[int, ...]) -> None:
    im = Image.open(ORIGINALES / nombre).convert("RGB")
    for ancho in anchos:
        sufijo = f"-{ancho}" if len(anchos) > 1 else ""
        guardar_webp(im, ENTRADA / f"{salida}{sufijo}.webp", ancho)


GRAFITO = (11, 13, 17)
ORO = (199, 162, 76)
GRIS = (168, 173, 182)


def _fuente(tam: int, bold: bool = True):
    candidatos = (
        [r"C:\Windows\Fonts\bahnschrift.ttf", r"C:\Windows\Fonts\segoeuib.ttf"]
        if bold
        else [r"C:\Windows\Fonts\bahnschrift.ttf", r"C:\Windows\Fonts\segoeui.ttf"]
    )
    for ruta in candidatos:
        try:
            return ImageFont.truetype(ruta, tam)
        except OSError:
            continue
    return ImageFont.load_default()


def _texto_espaciado(draw, xy, texto, fuente, relleno, espacio: int) -> None:
    x, y = xy
    for ch in texto:
        draw.text((x, y), ch, font=fuente, fill=relleno)
        x += draw.textlength(ch, font=fuente) + espacio


def _ajustar_lineas(draw, lineas, ancho_max, tam_inicial, bold=True):
    tam = tam_inicial
    while tam > 14:
        f = _fuente(tam, bold)
        if all(draw.textlength(l, font=f) <= ancho_max for l in lineas):
            return f, tam
        tam -= 2
    return _fuente(tam, bold), tam


def recorte_cinematografico() -> None:
    """Del póster vertical toma la franja camioneta + remolque + camino, sin textos."""
    im = Image.open(ORIGINALES / "campana-remolque.png").convert("RGB")
    w, h = im.size
    # Titular arriba y firma "SILVERADO" al pie: se recortan ambos.
    caja = (0, int(h * 0.40), w, int(h * 0.845))
    franja = im.crop(caja)
    guardar_webp(franja, ENTRADA / "cierre-cinematico-1122.webp", 1122)
    guardar_webp(franja, ENTRADA / "cierre-cinematico-800.webp", 800)

    # ---- Open Graph 1200x630 estilo pieza publicitaria ----
    W, H = 1200, 630
    og = Image.new("RGB", (W, H), GRAFITO)

    # Fotografía ocupando el 62% derecho, recortada en "cover".
    panel_x = 470
    panel_w = W - panel_x
    escala = max(panel_w / franja.width, H / franja.height)
    foto = franja.resize((round(franja.width * escala), round(franja.height * escala)), Image.LANCZOS)
    izq = round((foto.width - panel_w) * 0.62)
    arr = round((foto.height - H) * 0.42)
    foto = foto.crop((izq, arr, izq + panel_w, arr + H))
    og.paste(foto, (panel_x, 0))

    # Degradado de fundición entre el panel tipográfico y la fotografía.
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = capa.load()
    for x in range(panel_x, panel_x + 260):
        alfa = int(255 * (1 - (x - panel_x) / 260) ** 1.6)
        for y in range(H):
            px[x, y] = (*GRAFITO, alfa)
    og = Image.alpha_composite(og.convert("RGBA"), capa).convert("RGB")

    draw = ImageDraw.Draw(og)
    x0 = 64
    max_w = 372

    # Regla dorada + eyebrow de marca
    draw.rectangle([x0, 84, x0 + 44, 87], fill=ORO)
    f_eye = _fuente(17, True)
    _texto_espaciado(draw, (x0, 106), "CHEVROLET SILVERADO", f_eye, ORO, 3)

    # Titular
    lineas = ["TU NEGOCIO", "CRECIÓ. DALE LA", "MOVILIDAD QUE", "NECESITA."]
    f_tit, tam = _ajustar_lineas(draw, lineas, max_w, 58)
    y = 168
    for linea in lineas:
        draw.text((x0, y), linea, font=f_tit, fill=(255, 255, 255))
        y += round(tam * 1.06)

    # Bajada
    f_sub = _fuente(19, False)
    y += 18
    for linea in ["Camioneta de trabajo para", "ferreterías de la Ciudad de México."]:
        draw.text((x0, y), linea, font=f_sub, fill=GRIS)
        y += 27

    # Pie: CTA
    f_cta = _fuente(20, True)
    etiqueta = "SOLICITA TU COTIZACIÓN"
    ancho_cta = int(draw.textlength(etiqueta, font=f_cta)) + 52
    alto_cta = 54
    cy = H - 64 - alto_cta
    draw.rounded_rectangle([x0, cy, x0 + ancho_cta, cy + alto_cta], radius=6, fill=ORO)
    draw.text(
        (x0 + 26, cy + (alto_cta - 20) / 2 - 2), etiqueta, font=f_cta, fill=(12, 12, 14)
    )

    salida = RAIZ / "assets" / "og-silverado-ferreterias.jpg"
    og.save(salida, "JPEG", quality=88, optimize=True, progressive=True)
    print(f"  og-silverado-ferreterias.jpg                1200x630  {salida.stat().st_size/1024:6.1f} kB")


def main() -> int:
    if not ENTRADA.exists():
        print(f"No existe {ENTRADA}", file=sys.stderr)
        return 1

    ORIGINALES.mkdir(exist_ok=True)
    # Mover los PNG originales a una carpeta de referencia (no se sirven en producción)
    for png in sorted(ENTRADA.glob("*.png")):
        destino = ORIGINALES / png.name
        if not destino.exists():
            png.replace(destino)
            print(f"origen -> {destino.relative_to(RAIZ)}")

    print("\nTomas de catálogo por color (fondo blanco recortado):")
    for nombre in [
        "color-rojo-lava.png",
        "color-negro.png",
        "color-blanco.png",
        "color-gris-tiburon.png",
        "color-arena-lunar.png",
    ]:
        procesar_color(nombre)

    print("\nFotografía de ambiente y detalle:")
    procesar_simple("interior-tablero.png", "interior-tablero", (1700, 1000))
    procesar_simple("interior-asientos.png", "interior-asientos", (900,))
    procesar_simple("campana-remolque.png", "campana-remolque", (1122, 800))
    procesar_simple("exterior-trasera-roja.png", "exterior-trasera-roja", (900,))
    procesar_simple("caja-herramientas.png", "caja-herramientas", (900,))
    procesar_simple("hitch-receptor.png", "hitch-receptor", (900,))

    print("\nRecorte cinematográfico + Open Graph:")
    recorte_cinematografico()
    print("\nListo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
