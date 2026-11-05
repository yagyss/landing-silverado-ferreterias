"""Fuerza la carga y decodificación de imágenes en el arnés de QA."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ruta = RAIZ / "src/layout/_qa-view.html"
t = ruta.read_text(encoding="utf-8")

viejo = """        const cargarTodo = () => {
          documento.querySelectorAll('img[loading="lazy"]').forEach((img) => {
            img.loading = 'eager';
          });
        };"""

nuevo = """        const cargarTodo = () => {
          documento.querySelectorAll('img').forEach((img) => {
            img.loading = 'eager';
            if (img.decode) img.decode().catch(() => {});
          });
        };"""

if viejo in t:
    t = t.replace(viejo, nuevo)
    ruta.write_text(t, encoding="utf-8", newline="\n")
    print("  carga forzada aplicada")
else:
    print("  sin cambios (patrón distinto)")
