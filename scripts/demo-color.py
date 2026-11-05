"""Crea una demo que hace clic en el swatch Negro para verificar el cambio."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
html = (RAIZ / "index.html").read_text(encoding="utf-8")

inyeccion = """
<script>
window.addEventListener('load', function () {
  setTimeout(function () {
    const boton = document.querySelector('[data-color="negro"]');
    if (boton) boton.click();
    setTimeout(function () {
      const activa = document.querySelector('[data-color-img].is-active');
      const nombre = document.querySelector('[data-color-name]');
      document.title = 'activo=' + (activa ? activa.dataset.colorImg : 'ninguno') +
        ' nombre=' + (nombre ? nombre.textContent : '-');
      const pre = document.createElement('pre');
      pre.id = 'resultado-color';
      pre.textContent = document.title + ' | inline-opacity=' +
        (activa ? activa.style.opacity : '-');
      document.body.appendChild(pre);
    }, 700);
  }, 900);
});
</script>
"""

html = html.replace("</body>", inyeccion + "\n</body>")
(RAIZ / "demo-color.html").write_text(html, encoding="utf-8")
print("  demo-color.html generado")
