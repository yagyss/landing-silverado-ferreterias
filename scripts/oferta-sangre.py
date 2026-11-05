"""Promoción: escenario a sangre con la camioneta como acento y tarjetas planas."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------- HTML
ruta = RAIZ / "src/sections/07-oferta.html"
t = ruta.read_text(encoding="utf-8")
if "oferta__truck" not in t:
    t = t.replace(
        '<div class="oferta__fondo" aria-hidden="true"></div>',
        '<div class="oferta__fondo" aria-hidden="true"></div>\n'
        '  <img\n'
        '    class="oferta__truck"\n'
        '    src="/assets/vehiculos/silverado/cutout-blanco-1400.webp"\n'
        '    alt=""\n'
        '    aria-hidden="true"\n'
        '    width="1314"\n'
        '    height="630"\n'
        '    loading="lazy"\n'
        '    decoding="async"\n'
        '  />',
    )
    ruta.write_text(t, encoding="utf-8", newline="\n")
    print("  camioneta de acento insertada")

# -------------------------------------------------------------------- CSS
css = RAIZ / "src/styles/arte-final.css"
texto = css.read_text(encoding="utf-8")

bloque = """
/* ==========================================================================
   SECCIÓN 7 · Promoción a sangre
   La camioneta aparece recortada, muy tenue, detrás del bono; las tarjetas se
   convierten en bloques tipográficos separados por líneas finas.
   ==========================================================================*/

.oferta {
  overflow: hidden;
  isolation: isolate;
}

.oferta__inner {
  position: relative;
  z-index: 2;
}

.oferta__truck {
  position: absolute;
  right: -6%;
  bottom: -4%;
  width: min(70vw, 1040px);
  height: auto;
  z-index: 0;
  opacity: 0.42;
  filter: drop-shadow(0 40px 70px rgba(0, 0, 0, 0.65));
  mask-image: radial-gradient(ellipse 78% 82% at 62% 88%, #000 26%, transparent 76%);
  -webkit-mask-image: radial-gradient(ellipse 78% 82% at 62% 88%, #000 26%, transparent 76%);
  pointer-events: none;
  user-select: none;
}

/* Tarjetas: bloques tipográficos, sin caja */
.oferta .oferta__beneficios {
  gap: clamp(1.75rem, 4vw, 3.25rem);
  align-items: start;
  margin-top: clamp(1rem, 2.5vw, 1.75rem);
}

.oferta .oferta__card {
  position: relative;
  padding: clamp(1.25rem, 2.4vw, 1.9rem) 0 0;
  background: transparent;
  border: 0;
  border-top: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 0;
  box-shadow: none;
  backdrop-filter: none;
  overflow: visible;
}

.oferta .oferta__card::before {
  display: none;
}

.oferta .oferta__numero {
  color: rgba(255, 255, 255, 0.4);
  font-size: 0.68rem;
  letter-spacing: 0.2em;
}

.oferta .oferta__etiqueta {
  font-family: var(--font-display);
  font-size: clamp(2.7rem, 5.4vw, 4.5rem);
  line-height: 0.9;
  letter-spacing: -0.035em;
  background: linear-gradient(100deg, #f8e6bb 0%, #dcb96b 34%, #c7a24c 62%, #96762e 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  -webkit-text-fill-color: transparent;
  padding-block: 0.06em;
}

.oferta .oferta__titulo {
  margin-top: 0.35rem;
  font-family: var(--font-display);
  font-size: clamp(1.15rem, 2vw, 1.5rem);
  font-weight: 700;
  letter-spacing: -0.01em;
  color: #ffffff;
}

.oferta .oferta__detalle {
  margin-top: 0.6rem;
  max-width: 42ch;
  font-size: 0.88rem;
  line-height: 1.6;
  color: #a6b0be;
}

.oferta .oferta__acciones {
  margin-top: clamp(1.75rem, 3.5vw, 2.75rem);
}

.oferta .oferta__notas {
  position: relative;
  z-index: 2;
}

@media (min-width: 760px) {
  .oferta .oferta__beneficios {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 1079px) {
  .oferta__truck {
    width: 120vw;
    right: -30%;
    bottom: -2%;
    opacity: 0.26;
  }
}
"""

if "SECCIÓN 7 · Promoción a sangre" not in texto:
    css.write_text(texto.rstrip() + "\n" + bloque, encoding="utf-8", newline="\n")
    print("  CSS de promoción aplicado")
else:
    print("  ya aplicado")
