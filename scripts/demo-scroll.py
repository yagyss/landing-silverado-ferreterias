"""Diagnóstico: ¿el documento se puede desplazar en este navegador?"""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
html = (RAIZ / "index.html").read_text(encoding="utf-8")

demo = """
<script>
window.addEventListener('load', function () {
  setTimeout(function () {
    window.scrollTo(0, 5000);
    requestAnimationFrame(function () {
      const estHtml = getComputedStyle(document.documentElement);
      const estBody = getComputedStyle(document.body);
      const pre = document.createElement('pre');
      pre.id = 'diag-scroll';
      pre.textContent =
        'despues de scrollTo(5000) → scrollY=' + window.scrollY +
        ' | documentElement.scrollTop=' + document.documentElement.scrollTop +
        ' | body.scrollTop=' + document.body.scrollTop +
        ' | html.overflow=' + estHtml.overflowY +
        ' | body.overflow=' + estBody.overflowY +
        ' | altura=' + document.documentElement.scrollHeight +
        ' | claseBody=' + document.body.className;
      document.body.appendChild(pre);
    });
  }, 800);
});
</script>
"""

(RAIZ / "demo-scroll.html").write_text(html.replace("</body>", demo + "\n</body>"), encoding="utf-8")
print("  demo-scroll.html generado")
