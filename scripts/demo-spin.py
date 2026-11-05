"""Demo de arrastre para verificar el visor interactivo."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
html = (RAIZ / "index.html").read_text(encoding="utf-8")

inyeccion = """
<script>
window.addEventListener('load', function () {
  setTimeout(function () {
    const visor = document.querySelector('[data-spin]');
    const pila = document.querySelector('[data-spin-stack]');
    if (!visor || !pila) { document.title = 'sin visor'; return; }

    const caja = visor.getBoundingClientRect();
    const y = caja.top + caja.height / 2;
    const opciones = { bubbles: true, cancelable: true, pointerId: 1, pointerType: 'mouse', button: 0 };

    visor.dispatchEvent(new PointerEvent('pointerdown', { ...opciones, clientX: caja.left + caja.width / 2, clientY: y }));
    visor.dispatchEvent(new PointerEvent('pointermove', { ...opciones, clientX: caja.left + caja.width * 0.92, clientY: y - 40 }));

    setTimeout(function () {
      const estilo = getComputedStyle(pila);
      const pre = document.createElement('pre');
      pre.id = 'resultado-spin';
      pre.textContent = 'transform=' + estilo.transform +
        ' | giro=' + pila.style.getPropertyValue('--giro') +
        ' | inclina=' + pila.style.getPropertyValue('--inclina') +
        ' | hint=' + (document.querySelector('[data-spin-hint]')?.className || 'sin pista');
      document.body.appendChild(pre);
      document.title = 'giro=' + pila.style.getPropertyValue('--giro');
    }, 400);
  }, 800);
});
</script>
"""

html = html.replace("</body>", inyeccion + "\n</body>")
(RAIZ / "demo-spin.html").write_text(html, encoding="utf-8")
print("  demo-spin.html generado")
