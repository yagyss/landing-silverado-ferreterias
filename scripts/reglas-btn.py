"""Muestra las reglas de .btn y sus variantes de mayúsculas."""

import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

for hoja in ["base.css", "layout.css", "hero.css", "apple.css", "arte-final.css", "seccion-b.css"]:
    ruta = RAIZ / "src" / "styles" / hoja
    if not ruta.exists():
        continue
    texto = ruta.read_text(encoding="utf-8")
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", texto):
        selector = " ".join(m.group(1).split())
        cuerpo = m.group(2)
        if "text-transform" in cuerpo and ("btn" in selector or "localnav" in selector):
            transform = re.search(r"text-transform:\s*([a-z-]+)", cuerpo)
            print(f"{hoja}: {selector[:70]}  →  {transform.group(1) if transform else '?'}")
