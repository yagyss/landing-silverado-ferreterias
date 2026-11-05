"""Ajusta el mensaje de envío desde archivo y prueba el formulario de punta a punta."""

import re
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------ copy honesto
js = RAIZ / "src/js/formulario.js"
c = js.read_text(encoding="utf-8")

c = c.replace(
    "Tu solicitud salió hacia la hoja de cotizaciones. Un asesor te contactará. \" +\n"
    "            \"Si no recibes confirmación en unos minutos, escríbenos por WhatsApp.",
    "Enviamos tu solicitud. Un asesor te contactará. \" +\n"
    "            \"Si no recibes la confirmación por correo en unos minutos, escríbenos por WhatsApp.",
)
js.write_text(c, encoding="utf-8", newline="\n")

# ---------------------------------------------------- demo de envío (QA)
html = (RAIZ / "index.html").read_text(encoding="utf-8")

demo = """
<script>
window.addEventListener('load', function () {
  setTimeout(function () {
    const f = document.querySelector('[data-form-cotizacion]');
    if (!f) { document.title = 'sin formulario'; return; }

    f.elements.namedItem('nombre').value = 'PRUEBA DESDE ARCHIVO';
    f.elements.namedItem('whatsapp').value = '5512340001';
    f.elements.namedItem('correo').value = 'prueba@ejemplo.com';
    const plan = f.elements.namedItem('plan');
    if (plan) plan.value = plan.options[1] ? plan.options[1].value : '';
    f.elements.namedItem('mensaje').value = 'Registro de prueba del formulario.';
    f.elements.namedItem('privacidad').checked = true;

    f.querySelector('[data-form-submit]').click();

    setTimeout(function () {
      const exito = document.querySelector('[data-form-success]');
      const estado = document.querySelector('[data-form-status]');
      const pre = document.createElement('pre');
      pre.id = 'resultado-form';
      pre.textContent =
        'exitoVisible=' + (!exito || exito.hidden ? 'no' : 'si') +
        ' | titulo=' + (exito?.querySelector('[data-success-titulo]')?.textContent || '-') +
        ' | estado=' + (estado?.textContent || '(vacío)') +
        ' | formOculto=' + (f.hidden ? 'si' : 'no');
      document.body.appendChild(pre);
    }, 3500);
  }, 1200);
});
</script>
"""

(RAIZ / "demo-form.html").write_text(html.replace("</body>", demo + "\n</body>"), encoding="utf-8")
print("  demo-form.html generado")

for comando in (["node", "scripts/build-index-html.mjs"], ["node", "build.mjs"]):
    r = subprocess.run(comando, cwd=RAIZ, capture_output=True, text=True)
    print("  ", comando[-1], "->", "OK" if r.returncode == 0 else r.stderr[:200])

# Regenera la demo con el index ya actualizado
html = (RAIZ / "index.html").read_text(encoding="utf-8")
(RAIZ / "demo-form.html").write_text(html.replace("</body>", demo + "\n</body>"), encoding="utf-8")
print("  demo-form.html regenerado")
