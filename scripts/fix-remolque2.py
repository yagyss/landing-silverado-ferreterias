"""Anclaje definitivo del póster a sangre en la sección 5."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
css = RAIZ / "src/styles/arte-final.css"
texto = css.read_text(encoding="utf-8")

bloque = """
/* --- Remolque: póster anclado al borde de la ventana (definitivo) --- */
@media (min-width: 1080px) {
  .remolque--sangre {
    min-height: clamp(660px, 72vh, 860px);
  }

  .remolque--sangre .container {
    position: static;
  }

  .remolque--sangre .remolque-layout.remolque-layout {
    display: block;
  }

  .remolque--sangre .remolque-poster.remolque-poster {
    position: absolute;
    top: 0;
    bottom: 0;
    right: 0;
    left: auto;
    width: min(58vw, 940px);
    height: auto;
    margin: 0;
    z-index: 1;
  }

  .remolque--sangre .remolque-poster.remolque-poster img {
    width: 100%;
    height: 100%;
    min-height: 0;
    object-fit: cover;
    object-position: 52% 40%;
  }

  .remolque--sangre .remolque-contenido.remolque-contenido {
    position: relative;
    z-index: 3;
    max-width: 560px;
  }

  .remolque--sangre .remolque-lista.remolque-lista {
    grid-template-columns: minmax(0, 1fr);
  }

  .remolque--sangre .remolque-fotos.remolque-fotos {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .remolque--sangre .remolque-nota,
  .remolque--sangre .remolque-cta {
    position: relative;
    z-index: 3;
    max-width: 560px;
  }

  /* El encabezado no debe quedar debajo del degradado del póster */
  .remolque--sangre .section-header {
    position: relative;
    z-index: 3;
    max-width: 620px;
  }
}
"""

if "definitivo" not in texto:
    css.write_text(texto.rstrip() + "\n" + bloque, encoding="utf-8", newline="\n")
    print("  anclaje aplicado")
else:
    print("  ya aplicado")
