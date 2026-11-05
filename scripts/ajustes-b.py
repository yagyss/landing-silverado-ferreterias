from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ruta = RAIZ / "src/styles/seccion-b.css"
original = ruta.read_text(encoding="utf-8")

bloque = """
/* ==========================================================================
   Ajustes de integración (revisión final del Lead)
   ==========================================================================*/

/* La franja dorada lateral no debe desbordar el radio de la tarjeta */
.oferta__card {
  overflow: hidden;
}

/* Refuerzo el degradado del cierre para asegurar contraste del titular */
.cierre__scrim {
  background-image: linear-gradient(
      180deg,
      rgba(7, 9, 13, 0.3) 0%,
      rgba(7, 9, 13, 0.55) 38%,
      rgba(7, 9, 13, 0.9) 76%,
      rgba(7, 9, 13, 0.97) 100%
    ),
    linear-gradient(
      90deg,
      rgba(7, 9, 13, 0.82) 0%,
      rgba(7, 9, 13, 0.45) 44%,
      rgba(7, 9, 13, 0.12) 100%
    );
}

/* Carrusel de testimonios: 2 tarjetas en tablet y 3 en escritorio */
@media (min-width: 760px) {
  .testimonios__slide {
    flex-basis: calc((100% - var(--gap)) / 2);
  }
}

@media (min-width: 1080px) {
  .testimonios__slide {
    flex-basis: calc((100% - (2 * var(--gap))) / 3);
  }
}
"""

if "revisión final del Lead" in original:
    print("  ya aplicado")
else:
    ruta.write_text(original.rstrip() + "\n" + bloque, encoding="utf-8", newline="\n")
    print("  ajustes finales añadidos a seccion-b.css")
