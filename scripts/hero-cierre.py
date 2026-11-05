"""Ajuste de altura para que la camioneta cierre bien en pantallas comunes."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
css = RAIZ / "src/styles/apple.css"
texto = css.read_text(encoding="utf-8")

bloque = """
/* --- Cierre del hero: sin ruedas cortadas en 900 px de alto --- */
.hero--apple {
  padding-top: calc(var(--header-h) + clamp(1.25rem, 2.2vw, 1.9rem));
}

.hero__lema {
  font-size: clamp(1.06rem, 1.9vw, 1.45rem);
  max-width: 34ch;
}

.hero__nota {
  font-size: clamp(0.88rem, 1.02vw, 0.96rem);
  max-width: 54ch;
}

.hero__acciones {
  margin-top: 0.45rem;
}

@media (min-width: 1080px) {
  .eng--apple .eng__stack {
    max-width: min(56vw, 780px);
  }
}

/* Pantallas bajas: se prioriza que el vehículo quede completo */
@media (max-height: 860px) and (min-width: 1080px) {
  .hero__modelo {
    font-size: clamp(3.2rem, 6.4vw, 5.4rem);
  }

  .hero__nota {
    font-size: 0.9rem;
    line-height: 1.55;
  }

  .eng--apple .eng__stack {
    max-width: min(50vw, 700px);
  }
}
"""

if "sin ruedas cortadas" not in texto:
    css.write_text(texto.rstrip() + "\n" + bloque, encoding="utf-8", newline="\n")
    print("  cierre del hero ajustado")
else:
    print("  ya aplicado")
