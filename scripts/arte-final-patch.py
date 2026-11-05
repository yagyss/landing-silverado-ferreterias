"""Ajustes de arte final: hero más compacto y sección 3 cinematográfica."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# 1) Etiqueta más corta en los atributos del hero
hero = RAIZ / "src/sections/01-hero.html"
t = hero.read_text(encoding="utf-8")
t = t.replace("<em>espacio para tu mercancía</em>", "<em>espacio de carga</em>")
hero.write_text(t, encoding="utf-8", newline="\n")

# 2) Sección 3 sobre escenario oscuro con la unidad recortada
sol = RAIZ / "src/sections/03-solucion.html"
t = sol.read_text(encoding="utf-8")
t = t.replace(
    '<section id="vehiculo" class="section section--paper solucion" aria-labelledby="solucion-title">',
    '<section id="vehiculo" class="section section--azul solucion solucion--cine" aria-labelledby="solucion-title">\n'
    '  <span class="solucion__ghost" aria-hidden="true">SILVERADO</span>',
)
t = t.replace(
    'src="/assets/vehiculos/silverado/color-arena-lunar-1400.webp"',
    'src="/assets/vehiculos/silverado/cutout-arena-lunar-1400.webp"',
)
t = t.replace(
    'alt="Chevrolet Silverado 2026 en color Arena Lunar, vista de tres cuartos delantera sobre fondo blanco."',
    'alt="Chevrolet Silverado 2026 en color Arena Lunar, vista de tres cuartos delantera."',
)
t = t.replace('width="1322"\n            height="639"', 'width="1311"\n            height="630"')
sol.write_text(t, encoding="utf-8", newline="\n")

print("  hero y sección 3 actualizados")
