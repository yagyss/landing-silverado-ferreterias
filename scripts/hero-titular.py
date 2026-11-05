"""Titular más grande y oferta visible en el hero."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
css = RAIZ / "src/styles/apple.css"
texto = css.read_text(encoding="utf-8")

bloque = """
/* --- Titular protagonista y copy persuasivo --- */
.hero__modelo {
  font-size: clamp(3.4rem, 8.6vw, 7.2rem);
  line-height: 0.9;
  letter-spacing: -0.05em;
  font-weight: 700;
}

.hero--apple .hero__modelo {
  font-size: clamp(3.4rem, 8.6vw, 7.2rem);
}

.hero__modelo span {
  font-size: 0.26em;
  letter-spacing: 0.08em;
  vertical-align: 0.52em;
}

.hero__lema {
  max-width: 30ch;
  font-size: clamp(1.12rem, 2.1vw, 1.6rem);
  line-height: 1.25;
  letter-spacing: -0.015em;
  color: #ffffff;
}

.hero__nota {
  max-width: 56ch;
  font-size: clamp(0.9rem, 1.1vw, 1rem);
  line-height: 1.6;
  color: #a2adbb;
}

.hero__oferta {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  justify-content: center;
  gap: 0.35rem 0.5rem;
  margin-top: 0.35rem;
  padding: 0.45rem 0.9rem;
  border-radius: var(--r-pill);
  border: 1px solid rgba(199, 162, 76, 0.32);
  background: rgba(199, 162, 76, 0.08);
  font-size: 0.8rem;
  color: #e9dcbc;
  text-align: center;
}

.hero__oferta strong {
  color: #ffffff;
  font-weight: 700;
}

.hero__oferta span {
  color: #8b95a3;
  font-size: 0.72rem;
}

@media (min-width: 760px) {
  .hero__modelo {
    font-size: clamp(4rem, 7.4vw, 7.2rem);
  }
}

@media (min-width: 1080px) {
  .hero--apple .hero__intro {
    gap: 0.35rem;
  }

  .eng--apple .eng__stack {
    max-width: min(62vw, 880px);
  }
}
"""

if "Titular protagonista" not in texto:
    css.write_text(texto.rstrip() + "\n" + bloque, encoding="utf-8", newline="\n")
    print("  hero actualizado")
else:
    print("  ya aplicado")
