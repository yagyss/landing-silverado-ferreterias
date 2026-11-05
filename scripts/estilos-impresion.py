"""Estilos de impresión para exportar la landing completa y utilidades."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
css = RAIZ / "src/styles/arte-final.css"
texto = css.read_text(encoding="utf-8")

bloque = """
/* ==========================================================================
   IMPRESIÓN · Exportación de la landing completa (PDF / captura larga)
   ==========================================================================*/

@media print {
  html,
  body {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  .site-header,
  .promo-bar,
  .wa-float,
  .scroll-progress,
  .skip-link,
  .hero__scroll {
    display: none !important;
  }

  .hero,
  .remolque--sangre,
  .cierre {
    min-height: auto !important;
    padding-block: 2.5rem !important;
  }

  .section,
  .hero,
  .cierre {
    break-inside: avoid;
    page-break-inside: avoid;
  }

  .reveal,
  .stagger,
  .stagger > * {
    opacity: 1 !important;
    transform: none !important;
    filter: none !important;
  }
}
"""

if "IMPRESIÓN · Exportación" not in texto:
    css.write_text(texto.rstrip() + "\n" + bloque, encoding="utf-8", newline="\n")
    print("  estilos de impresión añadidos")
else:
    print("  ya aplicado")
