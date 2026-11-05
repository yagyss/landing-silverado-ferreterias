"""Sección 05 a sangre, pie con emblema real y tipografía de titulares."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- 05 · HTML
ruta = RAIZ / "src/sections/05-remolque.html"
t = ruta.read_text(encoding="utf-8")
t = t.replace(
    '<section id="remolque" class="section section--paper remolque" aria-labelledby="remolque-title">',
    '<section id="remolque" class="section remolque remolque--sangre" aria-labelledby="remolque-title">',
)
ruta.write_text(t, encoding="utf-8", newline="\n")

# --------------------------------------------------------------- FOOTER HTML
ruta = RAIZ / "src/layout/footer.html"
t = ruta.read_text(encoding="utf-8")
if "site-footer__logo" not in t:
    t = t.replace(
        '<span class="site-footer__lockup">CHEVROLET</span>\n        <span class="site-footer__model">SILVERADO</span>',
        '<img\n          class="site-footer__logo"\n          src="/assets/marca/chevrolet-lockup.png"\n'
        '          alt="Chevrolet"\n          width="220"\n          height="24"\n          loading="lazy"\n          decoding="async"\n        />\n'
        '        <span class="site-footer__model">SILVERADO</span>',
    )
    ruta.write_text(t, encoding="utf-8", newline="\n")
    print("  footer con emblema")
else:
    print("  footer ya actualizado")

# ---------------------------------------------------------------- 05 · CSS
css = RAIZ / "src/styles/arte-final.css"
texto = css.read_text(encoding="utf-8")

bloque = """
/* ==========================================================================
   SECCIÓN 5 · Carga y remolque, póster a sangre
   La pieza de campaña sangra hasta el borde derecho y se funde con el texto
   mediante un degradado, en lugar de vivir dentro de una tarjeta.
   ==========================================================================*/

.remolque--sangre {
  position: relative;
  isolation: isolate;
  overflow: hidden;
  padding-block: clamp(3.5rem, 7vw, 6rem);
  background: #080c13;
  color: #eef1f5;
}

.remolque--sangre::before {
  content: "";
  position: absolute;
  inset: 0;
  z-index: 0;
  background: radial-gradient(ellipse 60% 60% at 8% 30%, rgba(199, 162, 76, 0.1), transparent 62%),
    radial-gradient(ellipse 70% 70% at 30% 100%, rgba(28, 70, 126, 0.22), transparent 66%);
  pointer-events: none;
}

.remolque--sangre .container {
  position: relative;
  z-index: 2;
}

.remolque--sangre .section-header {
  max-width: 560px;
  margin-bottom: clamp(1.75rem, 3vw, 2.5rem);
}

.remolque--sangre .eyebrow {
  color: var(--gold-bright);
}

.remolque--sangre h2 {
  color: #ffffff;
}

.remolque--sangre .lead {
  color: #b4becc;
}

/* El póster sale del flujo y sangra por la derecha */
.remolque--sangre .remolque-layout {
  display: block;
}

.remolque--sangre .remolque-poster {
  position: absolute;
  inset: 0 0 0 auto;
  width: 54%;
  margin: 0;
  z-index: 1;
}

.remolque--sangre .remolque-poster img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: 52% 42%;
}

.remolque--sangre .remolque-poster::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(
    90deg,
    #080c13 0%,
    rgba(8, 12, 19, 0.92) 18%,
    rgba(8, 12, 19, 0.45) 46%,
    rgba(8, 12, 19, 0) 74%
  );
}

.remolque--sangre .remolque-contenido {
  position: relative;
  max-width: 620px;
  color: #c8d0dc;
}

.remolque--sangre .remolque-contenido > .eyebrow {
  margin-bottom: 0.6rem;
}

.remolque--sangre .remolque-intro {
  color: #aab4c2;
  font-size: var(--fs-small);
  max-width: 46ch;
  margin-bottom: 1.2rem;
}

.remolque--sangre .remolque-lista {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 0;
}

.remolque--sangre .remolque-item {
  display: grid;
  grid-template-columns: 34px minmax(0, 1fr);
  gap: 0.85rem;
  padding: 0.8rem 0;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.remolque--sangre .remolque-item__icon {
  color: var(--gold);
  border-color: rgba(199, 162, 76, 0.32);
  background: rgba(199, 162, 76, 0.08);
}

.remolque--sangre .remolque-item h3 {
  color: #ffffff;
  font-size: 0.92rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.remolque--sangre .remolque-item p {
  color: #8e99a7;
  font-size: 0.82rem;
}

/* Fotos de detalle */
.remolque--sangre .remolque-fotos {
  margin-top: 1.4rem;
}

.remolque--sangre .remolque-foto img {
  border-radius: var(--r-sm);
  border: 1px solid rgba(255, 255, 255, 0.12);
}

.remolque--sangre .remolque-foto figcaption {
  color: #7f8a98;
}

/* Nota legal: sobre oscuro, con acento dorado */
.remolque--sangre .remolque-nota {
  position: relative;
  z-index: 2;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-left: 2px solid var(--gold);
  border-radius: 0 var(--r-md) var(--r-md) 0;
  backdrop-filter: blur(6px);
  max-width: 720px;
}

.remolque--sangre .remolque-nota__icon {
  color: var(--gold-bright);
}

.remolque--sangre .remolque-nota__title {
  color: #ffffff;
}

.remolque--sangre .remolque-nota .disclaimer {
  color: #9aa4b2;
}

.remolque--sangre .remolque-cta {
  position: relative;
  z-index: 2;
  margin-top: clamp(1.5rem, 3vw, 2.25rem);
}

@media (max-width: 1079px) {
  .remolque--sangre .remolque-poster {
    position: relative;
    inset: auto;
    width: 100%;
    max-height: 420px;
    margin-top: 1.75rem;
    border-radius: var(--r-md);
    overflow: hidden;
  }

  .remolque--sangre .remolque-poster img {
    max-height: 420px;
    object-position: 50% 30%;
  }

  .remolque--sangre .remolque-poster::after {
    background: linear-gradient(180deg, rgba(8, 12, 19, 0.15) 0%, rgba(8, 12, 19, 0.75) 100%);
  }
}

@media (min-width: 1080px) {
  .remolque--sangre .remolque-lista {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    column-gap: 1.75rem;
  }
}

/* --------------------------------------------------------------- Tipografía */
h1,
h2,
h3,
.hero__title,
.cotiza__titulo,
.oferta__titulo {
  font-stretch: 94%;
  font-variation-settings: "wdth" 94;
}

/* ----------------------------------------------------------- Pie de página */
.site-footer__logo {
  height: 26px;
  width: auto;
  margin-bottom: 0.5rem;
  opacity: 0.95;
}

.site-footer__model {
  margin-top: 0.15rem;
}
"""

if "SECCIÓN 5 · Carga y remolque" not in texto:
    css.write_text(texto.rstrip() + "\n" + bloque, encoding="utf-8", newline="\n")
    print("  CSS de sección 5 + tipografía + pie aplicado")
else:
    print("  ya aplicado")
