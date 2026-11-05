"""Genera una copia de index.html con diagnóstico de layout del hero."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
html = (RAIZ / "index.html").read_text(encoding="utf-8")

diagnostico = """
<script>
window.addEventListener('load', function () {
  setTimeout(function () {
    const t = (sel) => {
      const el = document.querySelector(sel);
      if (!el) return sel + ': NO EXISTE';
      const r = el.getBoundingClientRect();
      const cs = getComputedStyle(el);
      return sel + ' | x=' + Math.round(r.x) + ' w=' + Math.round(r.width) +
        ' y=' + Math.round(r.y) + ' h=' + Math.round(r.height) +
        ' opacity=' + cs.opacity + ' z=' + cs.zIndex + ' pos=' + cs.position +
        ' vis=' + cs.visibility;
    };
    const lineas = [
      'viewport=' + window.innerWidth + 'x' + window.innerHeight,
      'scrollW=' + document.documentElement.scrollWidth,
      t('.hero--cine'),
      t('.hero__grid'),
      t('.hero__copy'),
      t('.hero__titulo'),
      t('.hero__vehiculo'),
      t('.hero__stack'),
      t('.hero__img.is-active'),
      t('.hero__scrim'),
      t('.hero__plate'),
    ];
    const pre = document.createElement('pre');
    pre.id = 'diagnostico';
    pre.textContent = lineas.join('\\n');
    document.body.appendChild(pre);
  }, 600);
});
</script>
"""

html = html.replace("</body>", diagnostico + "\n</body>")
(RAIZ / "debug-hero.html").write_text(html, encoding="utf-8")
print("  debug-hero.html generado")
