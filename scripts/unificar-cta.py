"""Unifica el texto de todos los CTA a «Solicitar cotización»."""

import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CAMBIOS = [
    ("src/layout/localnav.html", "Cotizar", "Solicitar cotización"),
    ("src/layout/footer.html", "Hablar con un asesor", "Solicitar cotización"),
    ("src/sections/07-oferta.html", "QUIERO MI COTIZACIÓN", "Solicitar cotización"),
    ("src/sections/10-faq.html", "Hablar con un asesor", "Solicitar cotización"),
    ("src/sections/12-cta-final.html", "SOLICITAR COTIZACIÓN", "Solicitar cotización"),
    ("src/data/site.js", 'cta: "QUIERO MI COTIZACIÓN"', 'cta: "Solicitar cotización"'),
]

for archivo, viejo, nuevo in CAMBIOS:
    ruta = RAIZ / archivo
    texto = ruta.read_text(encoding="utf-8")
    if viejo in texto:
        ruta.write_text(texto.replace(viejo, nuevo), encoding="utf-8", newline="\n")
        print(f"  {archivo}: «{viejo}» → «{nuevo}»")
    else:
        print(f"  {archivo}: no contenía «{viejo}»")

# Revisar si el CSS fuerza mayúsculas en los botones
css = "\n".join(
    (RAIZ / "src" / "styles" / nombre).read_text(encoding="utf-8")
    for nombre in ["base.css", "layout.css", "hero.css", "apple.css"]
    if (RAIZ / "src" / "styles" / nombre).exists()
)
mayusculas = [linea.strip() for linea in css.splitlines() if "text-transform" in linea and "upper" in linea]
print("  reglas de mayúsculas en CSS:", len(mayusculas))
for linea in mayusculas[:6]:
    print("   ·", linea[:80])

for comando in (["node", "scripts/build-index-html.mjs"], ["node", "build.mjs"]):
    r = subprocess.run(comando, cwd=RAIZ, capture_output=True, text=True)
    print("  ", comando[-1], "->", "OK" if r.returncode == 0 else r.stderr[:200])

# Verificación de textos visibles en el HTML final
html = (RAIZ / "index.html").read_text(encoding="utf-8")
for etiqueta in ["QUIERO MI COTIZACIÓN", "Hablar con un asesor", "SOLICITAR COTIZACIÓN", ">Cotizar<"]:
    print(f"  ¿sigue «{etiqueta}»?:", etiqueta in html)
print("  apariciones de «Solicitar cotización»:", html.count("Solicitar cotización"))
