"""Modo 'página completa' en el arnés de QA para capturas largas."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ruta = RAIZ / "src/layout/_qa-view.html"
t = ruta.read_text(encoding="utf-8")

if "modo-pagina-completa" not in t:
    t = t.replace(
        "        // Para la captura: evita que las imágenes diferidas queden sin cargar",
        "        // Modo página completa: neutraliza las alturas basadas en el viewport\n"
        "        if (parametros.get('full')) {\n"
        "          const completo = documento.createElement('style');\n"
        "          completo.id = 'modo-pagina-completa';\n"
        "          completo.textContent = `\n"
        "            .hero, .cierre, .remolque--sangre { min-height: auto !important; }\n"
        "            .hero { padding-top: 90px !important; }\n"
        "          `;\n"
        "          documento.head.appendChild(completo);\n"
        "        }\n\n"
        "        // Para la captura: evita que las imágenes diferidas queden sin cargar",
    )
    ruta.write_text(t, encoding="utf-8", newline="\n")
    print("  arnés con modo página completa")
else:
    print("  ya aplicado")
