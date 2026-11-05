"""Capa editorial: sustituye las tarjetas "de plantilla" por composiciones a línea."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ruta = RAIZ / "src/styles/arte-final.css"
texto = ruta.read_text(encoding="utf-8")

bloque = """
/* ==========================================================================
   SECCIÓN 2 · El problema, en clave editorial
   Sin cajas blancas: cuatro columnas separadas por líneas finas, como una
   revista de producto.
   ==========================================================================*/

.problema-grid {
  gap: clamp(1.5rem, 3vw, 2.5rem);
  align-items: start;
}

.problema-card.problema-card {
  position: relative;
  padding: clamp(1.1rem, 2vw, 1.6rem) 0 0;
  background: transparent;
  border: 0;
  border-top: 1px solid var(--line-strong);
  border-radius: 0;
  box-shadow: none;
  transition: border-color var(--dur) var(--ease-out);
}

.problema-card.problema-card::before {
  display: none;
}

.problema-card.problema-card:hover {
  transform: none;
  box-shadow: none;
  border-top-color: var(--gold);
}

.problema-card__top {
  margin-bottom: 0.9rem;
}

.problema-card__icon {
  background: transparent !important;
  border-color: var(--line-strong) !important;
  color: var(--gold-deep) !important;
}

.problema-card__num {
  font-size: 0.7rem;
  letter-spacing: 0.18em;
  color: var(--steel-light);
}

.problema-card h3 {
  font-size: clamp(1.05rem, 1.5vw, 1.2rem);
  margin-bottom: 0.4rem;
}

.problema-card p {
  font-size: 0.9rem;
  line-height: 1.6;
  color: var(--ink-soft);
}

/* El remate mantiene el bloque destacado pero sin caja dura */
.problema-cierre {
  border: 0;
  border-left: 2px solid var(--gold);
  border-radius: 0;
  background: linear-gradient(100deg, rgba(199, 162, 76, 0.09), rgba(199, 162, 76, 0.01));
  box-shadow: none;
}

/* ==========================================================================
   SECCIÓN 4 · Beneficios con separadores, no con tarjetas
   ==========================================================================*/

.beneficios-grid {
  gap: clamp(1.5rem, 3vw, 2.75rem) clamp(1.5rem, 3vw, 2.25rem);
  align-items: start;
}

.beneficios-card {
  padding: clamp(1rem, 2vw, 1.5rem) 0 0;
  background: transparent;
  border: 0;
  border-top: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: 0;
  box-shadow: none;
  transition: border-color var(--dur) var(--ease-out);
}

.beneficios-card:hover {
  transform: none;
  border-top-color: var(--gold);
  box-shadow: none;
  background: transparent;
}

.beneficios-card__num {
  font-size: 0.68rem;
  letter-spacing: 0.2em;
  color: var(--gold);
}

.beneficios-card__num::after {
  background: linear-gradient(90deg, var(--oro-medio), transparent);
}

.beneficios-card h3 {
  font-size: clamp(0.95rem, 1.35vw, 1.08rem);
  letter-spacing: 0.06em;
  color: #ffffff;
}

.beneficios-card p {
  font-size: 0.89rem;
  line-height: 1.6;
  color: #9aa4b2;
}

/* La pieza de imagen gana protagonismo y pierde el marco */
.beneficios-media {
  border-radius: var(--r-md);
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* ==========================================================================
   Secciones claras: menos cajas, más aire y jerarquía
   ==========================================================================*/

.section--mist .card:not(.problema-card) {
  border-color: rgba(11, 14, 19, 0.07);
  box-shadow: none;
}

.section--mist {
  background: linear-gradient(180deg, #f5f6f8 0%, #f2f4f7 100%);
}

.section--paper {
  background: linear-gradient(180deg, #ffffff 0%, #fdfdfe 100%);
}
"""

if "SECCIÓN 2 · El problema" not in texto:
    ruta.write_text(texto.rstrip() + "\n" + bloque, encoding="utf-8", newline="\n")
    print("  capa editorial aplicada")
else:
    print("  ya aplicado")
