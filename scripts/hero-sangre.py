"""Hero cinematográfico a sangre (composición de la referencia)."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
css = RAIZ / "src/styles/apple.css"
texto = css.read_text(encoding="utf-8")

bloque = """
/* ==========================================================================
   HERO A SANGRE · fondo fotográfico + copy a la izquierda + vehículo a la derecha
   ==========================================================================*/

.hero--cine {
  position: relative;
  isolation: isolate;
  display: block;
  min-height: clamp(620px, 92svh, 900px);
  padding: 0;
  background: #070a11;
  overflow: hidden;
}

.hero__plate {
  position: absolute;
  inset: 0;
  z-index: 0;
  background-image: url("/assets/vehiculos/silverado/fondo-hero-2000.webp");
  background-size: cover;
  background-position: center 18%;
  background-repeat: no-repeat;
}

.hero__scrim {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
  background: linear-gradient(
      90deg,
      rgba(5, 7, 12, 0.94) 0%,
      rgba(5, 7, 12, 0.78) 34%,
      rgba(5, 7, 12, 0.32) 62%,
      rgba(5, 7, 12, 0.05) 100%
    ),
    linear-gradient(180deg, rgba(5, 7, 12, 0.55) 0%, rgba(5, 7, 12, 0) 26%, rgba(5, 7, 12, 0.9) 100%);
}

.hero--cine .hero__grid {
  position: relative;
  z-index: 2;
  display: grid;
  gap: clamp(1.25rem, 3vw, 2rem);
  align-items: end;
  min-height: clamp(620px, 92svh, 900px);
  padding-top: calc(var(--header-h) + var(--promo-h, 0px) + clamp(1.5rem, 3vw, 2.75rem));
  padding-bottom: clamp(1.25rem, 2.5vw, 2rem);
}

.hero--cine .hero__copy {
  display: grid;
  gap: 0.7rem;
  align-content: center;
  max-width: 640px;
}

.hero__titulo {
  font-size: clamp(2rem, 4vw, 3.5rem);
  line-height: 0.98;
  letter-spacing: -0.032em;
  text-transform: uppercase;
  color: #ffffff;
  max-width: 19ch;
  text-wrap: balance;
}

.hero__oro {
  background: linear-gradient(100deg, #f7e3b0 0%, #ddb96a 36%, #c7a24c 64%, #9c7c31 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  -webkit-text-fill-color: transparent;
}

.hero__bajada {
  max-width: 46ch;
  font-size: clamp(0.94rem, 1.1vw, 1.02rem);
  line-height: 1.6;
  color: #b3bdca;
}

.hero--cine .hero__acciones {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: flex-start;
  gap: 1rem;
  margin-top: 0.5rem;
}

.hero__oferta {
  justify-content: flex-start;
  justify-self: start;
  margin-top: 0.35rem;
  padding: 0.4rem 0.85rem;
  border-radius: var(--r-pill);
  border: 1px solid rgba(199, 162, 76, 0.3);
  background: rgba(10, 14, 20, 0.55);
  font-size: 0.78rem;
  color: #d9cdae;
}

.hero__oferta strong {
  color: #ffffff;
}

.hero__oferta span {
  color: #8b95a3;
  font-size: 0.7rem;
}

/* ---------------------------------------------------------- Vehículo */
.hero--cine .hero__vehiculo {
  position: relative;
  align-self: end;
  justify-self: end;
  width: 100%;
}

.hero__stack-wrap {
  position: relative;
  width: 100%;
}

.hero__stack {
  position: relative;
  aspect-ratio: 1314 / 630;
  width: min(62vw, 1080px);
  margin-left: auto;
  margin-right: clamp(-16vw, -8vw, -4vw);
  transform: translateY(clamp(0.5rem, 1.5vw, 1.25rem));
}

.hero__img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
  opacity: 0;
  transform: scale(0.99) translateY(6px);
  transition: opacity 520ms var(--ease-out), transform 900ms var(--ease-out);
  filter: drop-shadow(0 38px 52px rgba(0, 0, 0, 0.6));
}

.hero__img.is-active {
  opacity: 1;
  transform: none;
}

/* ------------------------------------------------------ Selector de color */
.hero__picker {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.9rem;
  margin-top: 0.35rem;
  margin-left: auto;
  margin-right: clamp(2rem, 12vw, 10rem);
  width: fit-content;
  padding: 0.5rem 0.95rem;
  border-radius: var(--r-pill);
  border: 1px solid rgba(255, 255, 255, 0.14);
  background: rgba(8, 12, 18, 0.62);
  backdrop-filter: blur(16px) saturate(140%);
  -webkit-backdrop-filter: blur(16px) saturate(140%);
}

.hero__color {
  display: flex;
  align-items: baseline;
  gap: 0.4rem;
  white-space: nowrap;
}

.hero__color-label {
  font-size: 0.62rem;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: #8590a0;
}

.hero__color strong {
  font-family: var(--font-display);
  font-size: 0.86rem;
  color: #ffffff;
}

.hero__swatches {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.hero--cine .swatch {
  width: 30px;
  height: 30px;
}

/* ------------------------------------------------------------------ Móvil */
@media (max-width: 900px) {
  .hero--cine .hero__grid {
    grid-template-columns: minmax(0, 1fr);
    align-items: start;
    min-height: auto;
  }

  .hero--cine .hero__copy {
    max-width: none;
  }

  .hero__titulo {
    max-width: 24ch;
  }

  .hero--cine .hero__vehiculo {
    justify-self: center;
  }

  .hero__stack {
    width: 100%;
    margin: 0;
    transform: none;
  }

  .hero__picker {
    margin-inline: auto;
  }

  .hero--cine .hero__acciones {
    justify-content: flex-start;
  }
}

@media (min-width: 901px) {
  .hero--cine .hero__grid {
    grid-template-columns: minmax(0, 0.92fr) minmax(0, 1.08fr);
  }
}

@media (prefers-reduced-motion: reduce) {
  .hero__img {
    transition: opacity 1ms linear;
    transform: none;
  }
}
"""

if "HERO A SANGRE" not in texto:
    css.write_text(texto.rstrip() + "\n" + bloque, encoding="utf-8", newline="\n")
    print("  hero a sangre aplicado")
else:
    print("  ya aplicado")
