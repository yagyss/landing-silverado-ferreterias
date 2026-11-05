"""Instala la etiqueta de Google exactamente como la entrega Google (una sola)."""

import re
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
render = RAIZ / "lib/render.mjs"
r = render.read_text(encoding="utf-8")

etiqueta = """    <!-- Google tag (gtag.js) · Google Tag Manager GTM-5CJH58QK -->
    <script async src="https://www.googletagmanager.com/gtm.js?id=GTM-5CJH58QK"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag() {
        dataLayer.push(arguments);
      }
      gtag("js", new Date());
    </script>
"""

# 1) Reemplaza cualquier bloque de GTM previo por la etiqueta oficial
r = re.sub(
    r"\n *<!-- Google Tag Manager -->.*?<!-- End Google Tag Manager -->\n",
    "\n",
    r,
    flags=re.S,
)

# 2) Quita el noscript del contenedor (Google pide una sola etiqueta)
r = re.sub(
    r"\n *<noscript><iframe src=\"https://www\.googletagmanager\.com/ns\.html[^>]*></iframe></noscript>",
    "",
    r,
)

# 3) Inserta justo después de <head>
r = r.replace("  <head>\n", "  <head>\n" + etiqueta, 1)

render.write_text(r, encoding="utf-8", newline="\n")

print("  etiquetas de Google en el documento:", r.count("googletagmanager.com/gtm.js?id="))
print("  noscript restante:", "googletagmanager.com/ns.html" in r)

# ------------------------------------------------------------ reconstruir
for comando in (["node", "scripts/build-index-html.mjs"], ["node", "build.mjs"]):
    res = subprocess.run(comando, cwd=RAIZ, capture_output=True, text=True)
    print("  ", comando[-1], "->", "OK" if res.returncode == 0 else res.stderr[:300])

html = (RAIZ / "index.html").read_text(encoding="utf-8")
print("  GTM en index.html:", html.count("googletagmanager.com/gtm.js?id=GTM-5CJH58QK"))
print("  gtag init:", "gtag(\"js\", new Date())" in html or "gtag('js', new Date())" in html)
