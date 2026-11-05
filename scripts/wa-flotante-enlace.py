"""El botón flotante de WhatsApp pasa a ser un enlace real."""

import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# 1) footer.html: <button> → <a>
pie = RAIZ / "src/layout/footer.html"
texto = pie.read_text(encoding="utf-8")

texto = texto.replace(
    '<button class="wa-float" type="button" data-wa-float aria-label="Cotizar por WhatsApp">',
    '<a class="wa-float" data-wa-float href="#cotizacion" aria-label="Solicitar cotización por WhatsApp" rel="noopener">',
)
texto = texto.replace(
    '  <span class="wa-float__badge" data-wa-badge hidden>Configura tu número en site.js</span>\n</button>',
    '  <span class="wa-float__badge" data-wa-badge hidden>Configura tu número en site.js</span>\n</a>',
)
# Etiqueta visible
texto = texto.replace(
    '<span class="wa-float__label">Cotiza por WhatsApp</span>',
    '<span class="wa-float__label">Solicitar cotización</span>',
)
pie.write_text(texto, encoding="utf-8", newline="\n")
print("  footer.html: enlace flotante listo")

# 2) ui.js: respaldo por si el elemento fuera un botón
ui = RAIZ / "src/js/ui.js"
js = ui.read_text(encoding="utf-8")

if "abrirWhatsApp" not in js:
    js = js.replace(
        """    if (configurado) {
      nodo.setAttribute("href", url);
      nodo.setAttribute("target", "_blank");
      nodo.setAttribute("rel", "noopener");
      return;
    }""",
        """    if (configurado) {
      nodo.setAttribute("href", url);
      nodo.setAttribute("target", "_blank");
      nodo.setAttribute("rel", "noopener");

      // Respaldo: si el marcado usara un <button>, igual abre WhatsApp.
      if (nodo.tagName === "BUTTON") {
        nodo.addEventListener("click", (evento) => {
          evento.preventDefault();
          window.open(url, "_blank", "noopener");
        });
      }
      return;
    }""",
    )
    ui.write_text(js, encoding="utf-8", newline="\n")
    print("  ui.js: respaldo para botón")

# 3) CSS: el elemento ahora es <a>
css = RAIZ / "src/styles/apple.css"
c = css.read_text(encoding="utf-8")
if "a.wa-float" not in c:
    c = c.rstrip() + """

/* El botón flotante es un enlace real (abre WhatsApp en otra pestaña) */
a.wa-float {
  text-decoration: none;
  color: inherit;
}
"""
    css.write_text(c, encoding="utf-8", newline="\n")
    print("  CSS del enlace flotante agregado")

# 4) Reconstruir
for comando in (["node", "scripts/build-index-html.mjs"], ["node", "build.mjs"]):
    r = subprocess.run(comando, cwd=RAIZ, capture_output=True, text=True)
    print("  ", comando[-1], "->", "OK" if r.returncode == 0 else r.stderr[:200])

html = (RAIZ / "index.html").read_text(encoding="utf-8")
print("  flotante es enlace:", 'class="wa-float"' in html and 'data-wa-float' in html)
print("  etiqueta visible:", "Solicitar cotización</span>" in html)
