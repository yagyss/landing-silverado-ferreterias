"""Conecta el módulo de CTA y agrega el resaltado del formulario."""

import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# -------------------------------------------------------------- main.js
main = RAIZ / "src/js/main.js"
m = main.read_text(encoding="utf-8")

if "initCtaFormulario" not in m:
    m = m.replace(
        'import { initFormulario } from "./formulario.js";',
        'import { initFormulario } from "./formulario.js";\nimport { initCtaFormulario } from "./cta-formulario.js";',
    )
    m = m.replace(
        '["formulario", initFormulario],',
        '["formulario", initFormulario],\n    ["cta-formulario", initCtaFormulario],',
    )
    main.write_text(m, encoding="utf-8", newline="\n")
    print("  main.js con initCtaFormulario")

# ------------------------------------------------------- bundle autónomo
bundle = RAIZ / "scripts/build-index-html.mjs"
b = bundle.read_text(encoding="utf-8")
if '"cta-formulario.js"' not in b:
    b = b.replace('  "formulario.js",', '  "formulario.js",\n  "cta-formulario.js",')
    bundle.write_text(b, encoding="utf-8", newline="\n")
    print("  build-index-html.mjs incluye cta-formulario.js")

# ------------------------------------------------------------------ CSS
css = RAIZ / "src/styles/apple.css"
c = css.read_text(encoding="utf-8")

bloque = """
/* Llamada a la acción: resaltado del formulario al llegar */
.cotiza__card.is-destacada {
  animation: cotiza-pulso 1300ms var(--ease-out) both;
}

@keyframes cotiza-pulso {
  0% {
    box-shadow: 0 0 0 0 rgba(199, 162, 76, 0.55);
  }
  60% {
    box-shadow: 0 0 0 16px rgba(199, 162, 76, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(199, 162, 76, 0);
  }
}

@media (prefers-reduced-motion: reduce) {
  .cotiza__card.is-destacada {
    animation: none;
  }
}
"""

if "cotiza-pulso" not in c:
    css.write_text(c.rstrip() + "\n" + bloque, encoding="utf-8", newline="\n")
    print("  CSS de resaltado agregado")

# ------------------------------------------------------------ reconstruir
for comando in (["node", "scripts/build-index-html.mjs"], ["node", "build.mjs"]):
    r = subprocess.run(comando, cwd=RAIZ, capture_output=True, text=True)
    print("  ", comando[-1], "->", "OK" if r.returncode == 0 else r.stderr[:300])

for archivo in ("src/js/cta-formulario.js", "src/js/main.js"):
    r = subprocess.run(["node", "--check", archivo], cwd=RAIZ, capture_output=True, text=True)
    print(f"  {archivo}: {'OK' if r.returncode == 0 else r.stderr[:200]}")

html = (RAIZ / "index.html").read_text(encoding="utf-8")
print("  módulo en el bundle autónomo:", "irAlFormulario" in html)
