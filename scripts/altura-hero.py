"""Ajuste fino de altura del hero para que entre en la primera pantalla."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
css = RAIZ / "src/styles/apple.css"
texto = css.read_text(encoding="utf-8")

bloque = """
/* --- Altura del hero: todo entra en la primera pantalla --- */
.hero--apple {
  padding-top: calc(var(--header-h) + clamp(1.75rem, 3vw, 2.5rem));
}

.hero--apple .hero__intro {
  gap: 0.4rem;
}

.hero__modelo {
  font-size: clamp(2.9rem, 5.2vw, 4.7rem);
}

.hero__lema {
  font-size: clamp(1.02rem, 1.8vw, 1.4rem);
  max-width: 30ch;
}

.hero__nota {
  font-size: clamp(0.88rem, 1.05vw, 0.96rem);
}

.eng--apple .eng__stack {
  max-width: min(84vw, 1040px);
}

.hero__acciones {
  margin-top: 0.6rem;
}

.hero__pie {
  margin-top: clamp(0.75rem, 1.6vw, 1.25rem);
  padding-top: 0.75rem;
}
"""

if "Altura del hero" not in texto:
    css.write_text(texto.rstrip() + "\n" + bloque, encoding="utf-8", newline="\n")
    print("  altura ajustada")
else:
    print("  ya aplicado")
