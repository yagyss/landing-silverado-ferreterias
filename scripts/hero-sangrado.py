"""Ajuste de sangrado del vehículo en el hero."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
css = RAIZ / "src/styles/apple.css"
texto = css.read_text(encoding="utf-8")

bloque = """
/* --- Sangrado real del vehículo por el borde derecho --- */
.hero__stack {
  width: min(74vw, 1240px);
  margin-right: clamp(-22vw, -12vw, -6vw);
  margin-left: auto;
  transform: translateY(clamp(0.75rem, 2vw, 1.75rem));
}

.hero--cine .hero__vehiculo {
  justify-self: end;
  align-self: end;
}

@media (max-width: 900px) {
  .hero__stack {
    width: 108%;
    margin-right: -4%;
    margin-left: 0;
    transform: none;
  }
}
"""

if "Sangrado real del vehículo" not in texto:
    css.write_text(texto.rstrip() + "\n" + bloque, encoding="utf-8", newline="\n")
    print("  sangrado ajustado")
else:
    print("  ya aplicado")
