"""Cambia el fondo de la sección 5 al recorte cinematográfico sin texto."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
css = RAIZ / "src/styles/arte-final.css"
texto = css.read_text(encoding="utf-8")

texto = texto.replace(
    'background-image: url("/assets/vehiculos/silverado/campana-remolque-1122.webp");',
    'background-image: url("/assets/vehiculos/silverado/cierre-cinematico-1122.webp");',
)
texto = texto.replace(
    "  background-position: 50% 50%;\n  background-size: cover;",
    "  background-position: 62% 52%;\n  background-size: cover;",
)
texto = texto.replace(
    "    background-position: 52% 42%;\n  }\n\n  .remolque--sangre .remolque__fondo::after {",
    "    background-position: 66% 55%;\n  }\n\n  .remolque--sangre .remolque__fondo::after {",
)
texto = texto.replace(
    "  .remolque--sangre .remolque__fondo {\n    width: min(62vw, 1000px);",
    "  .remolque--sangre .remolque__fondo {\n    width: min(64vw, 1040px);",
)

css.write_text(texto, encoding="utf-8", newline="\n")
print("  fondo actualizado al recorte sin texto")
