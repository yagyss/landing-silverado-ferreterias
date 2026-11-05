"""Verifica que los CTA lleven al formulario (prueba con clic simulado)."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
html = (RAIZ / "index.html").read_text(encoding="utf-8")

demo = """
<script>
window.addEventListener('load', function () {
  setTimeout(function () {
    const cta = document.querySelector('[data-cta="hero"]') || document.querySelector('a[href="#cotizacion"]');
    if (!cta) { document.title = 'sin CTA'; return; }
    cta.click();

    setTimeout(function () {
      const seccion = document.querySelector('#cotizacion');
      const caja = seccion.getBoundingClientRect();
      const activo = document.activeElement;
      const visible = caja.top < window.innerHeight && caja.bottom > 0;
      const pre = document.createElement('pre');
      pre.id = 'resultado-cta';
      pre.textContent =
        'scrollY=' + Math.round(window.scrollY) +
        ' | seccionTop=' + Math.round(caja.top) +
        ' | visible=' + visible +
        ' | foco=' + (activo ? (activo.id || activo.tagName) : 'ninguno') +
        ' | url=' + location.hash +
        ' | resaltado=' + Boolean(document.querySelector('.cotiza__card.is-destacada'));
      document.body.appendChild(pre);
      document.title = 'resultado listo';
    }, 1800);
  }, 900);
});
</script>
"""

(RAIZ / "demo-cta.html").write_text(html.replace("</body>", demo + "\n</body>"), encoding="utf-8")
print("  demo-cta.html generado")
