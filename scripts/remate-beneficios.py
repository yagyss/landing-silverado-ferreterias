"""Remate de la capa editorial: rejilla de beneficios sin alturas forzadas."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ruta = RAIZ / "src/styles/arte-final.css"
texto = ruta.read_text(encoding="utf-8")

bloque = """
/* Beneficios: altura natural y sin relleno dorado en la quinta tarjeta */
.beneficios-card,
.beneficios-card.beneficios-card {
  min-height: 0;
}

.beneficios-grid > :last-child {
  background: transparent;
  border-color: rgba(255, 255, 255, 0.14);
}

.beneficios-grid {
  row-gap: clamp(1.75rem, 3vw, 2.5rem);
}
"""

if "altura natural" not in texto:
    ruta.write_text(texto.rstrip() + "\n" + bloque, encoding="utf-8", newline="\n")
    print("  remate aplicado")
else:
    print("  ya aplicado")
