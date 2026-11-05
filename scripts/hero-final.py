"""Cierre del hero: legibilidad garantizada y capas deterministas."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
css = RAIZ / "src/styles/apple.css"
texto = css.read_text(encoding="utf-8")

bloque = """
/* ==========================================================================
   HERO FINAL · velo detrás del contenido y contraste garantizado
   ==========================================================================*/

.hero--cine {
  position: relative !important;
  overflow: hidden !important;
}

.hero__plate {
  z-index: 0 !important;
  filter: brightness(1.08) saturate(1.05);
}

/* El velo va DEBAJO del contenido (z-index 1) y es más suave */
.hero__scrim {
  z-index: 1 !important;
  background: linear-gradient(
      90deg,
      rgba(5, 7, 12, 0.78) 0%,
      rgba(5, 7, 12, 0.5) 34%,
      rgba(5, 7, 12, 0.16) 62%,
      rgba(5, 7, 12, 0) 100%
    ),
    linear-gradient(180deg, rgba(5, 7, 12, 0.28) 0%, rgba(5, 7, 12, 0) 30%, rgba(5, 7, 12, 0.7) 100%) !important;
}

.hero--cine .hero__grid {
  position: relative !important;
  z-index: 3 !important;
  display: grid !important;
  grid-template-columns: minmax(0, 0.92fr) minmax(0, 1.08fr) !important;
  align-items: center !important;
  gap: clamp(1rem, 2vw, 2rem) !important;
  min-height: clamp(620px, 88svh, 860px) !important;
}

/* Respaldo oscuro localizado: solo detrás del bloque de texto */
.hero--cine .hero__copy {
  position: relative;
  z-index: 2;
  align-content: center !important;
  max-width: 620px !important;
}

.hero--cine .hero__copy::before {
  content: "";
  position: absolute;
  inset: -2rem -3rem -2rem -3.5rem;
  z-index: -1;
  background: radial-gradient(72% 80% at 34% 50%, rgba(4, 6, 10, 0.82) 0%, rgba(4, 6, 10, 0.45) 55%, transparent 78%);
  filter: blur(14px);
  pointer-events: none;
}

.hero--cine .hero__titulo,
.hero--cine .hero__bajada,
.hero--cine .eyebrow {
  text-shadow: 0 2px 18px rgba(0, 0, 0, 0.55);
}

.hero--cine .hero__bajada {
  color: #c8d1dd;
}

.hero--cine .hero__vehiculo {
  align-self: end !important;
  justify-self: stretch !important;
  width: 100% !important;
}

.hero__stack {
  width: 100% !important;
  margin: 0 !important;
  margin-right: calc(50% - 52vw) !important;
  transform: translateY(clamp(0.5rem, 1.5vw, 1.25rem)) !important;
}

.hero__picker {
  margin: 0.6rem 0 0 auto !important;
  margin-right: clamp(0rem, 8vw, 7rem) !important;
}

.hero--cine .swatch {
  border-color: rgba(255, 255, 255, 0.42);
  box-shadow: 0 6px 16px -6px rgba(0, 0, 0, 0.8);
}

@media (max-width: 979px) {
  .hero--cine .hero__grid {
    grid-template-columns: minmax(0, 1fr) !important;
    align-items: start !important;
    min-height: auto !important;
    padding-top: calc(var(--header-h) + var(--promo-h, 0px) + 1.5rem) !important;
    padding-bottom: 1.5rem !important;
  }

  .hero--cine .hero__copy::before {
    inset: -1rem -1rem -1rem -1rem;
  }

  .hero__stack {
    margin-right: -6vw !important;
    margin-left: 0 !important;
    width: 106% !important;
    transform: none !important;
  }

  .hero__picker {
    margin: 0.75rem auto 0 !important;
  }
}
"""

if "HERO FINAL" not in texto:
    css.write_text(texto.rstrip() + "\n" + bloque, encoding="utf-8", newline="\n")
    print("  hero final aplicado")
else:
    print("  ya aplicado")
