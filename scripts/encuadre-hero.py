"""Ajustes del hero para la versión de archivo (encuadre tipo Apple)."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
css = RAIZ / "src/styles/apple.css"
texto = css.read_text(encoding="utf-8")

bloque = """
/* --- Encuadre del hero: la camioneta respira y no se corta --- */
.hero--apple {
  padding-top: calc(var(--header-h) + clamp(1.25rem, 2.6vw, 2rem));
}

.eng--apple .eng__stack {
  margin-inline: auto !important;
  max-width: min(90vw, 1160px);
}

.eng--apple .eng__img {
  object-fit: contain;
}

.hero__lema {
  max-width: 34ch;
}

.hero__producto {
  margin-top: clamp(0.25rem, 1.5vw, 0.75rem);
}

@media (min-width: 1080px) {
  .hero--apple .hero__intro {
    gap: 0.5rem;
  }

  .hero__modelo {
    font-size: clamp(3.4rem, 6.2vw, 5.4rem);
  }
}

/* En pantallas bajas, la camioneta no debe empujar el contenido */
@media (max-height: 780px) and (min-width: 1080px) {
  .eng--apple .eng__stack {
    max-width: min(78vw, 980px);
  }
}
"""

if "Encuadre del hero" not in texto:
    css.write_text(texto.rstrip() + "\n" + bloque, encoding="utf-8", newline="\n")
    print("  encuadre aplicado")
else:
    print("  ya aplicado")
