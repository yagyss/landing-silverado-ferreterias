"""Revisa qué selectores fuerzan mayúsculas y si el CTA del localnav cabe."""

import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

for hoja in sorted((RAIZ / "src" / "styles").glob("*.css")):
    texto = hoja.read_text(encoding="utf-8")
    for coincidencia in re.finditer(r"([^{}]+)\{([^{}]*)\}", texto):
        selectores, cuerpo = coincidencia.group(1).strip(), coincidencia.group(2)
        if "text-transform" in cuerpo and "uppercase" in cuerpo:
            selector = " ".join(selectores.split())
            if any(x in selector for x in [".btn", "localnav__cta", "header-cta", "cierre"]):
                print(f"{hoja.name}: {selector}")

print("\n--- localnav__cta ---")
texto = (RAIZ / "src" / "styles" / "layout.css").read_text(encoding="utf-8")
m = re.search(r"\.localnav__cta\s*\{([^}]*)\}", texto)
print(m.group(1).strip() if m else "no encontrado en layout.css")

print("\n--- ancho del localnav / fuente ---")
for m in re.finditer(r"\.localnav(?:__[a-z-]+)?\s*\{([^}]*)\}", texto):
    print("·", " ".join(m.group(1).split())[:160])
