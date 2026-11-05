"""Flecha móvil independiente (apunta hacia abajo sin tapar el texto)."""

import re
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- HTML
sec = RAIZ / "src/sections/11-cotizacion.html"
h = sec.read_text(encoding="utf-8")

# Quita la flecha dentro del párrafo y deja solo la versión escritorio
patron = re.compile(r'\s*<span class="cotiza__alt-flecha" aria-hidden="true">.*?</span>', re.S)
h, cuantas = patron.subn("", h, count=1)
print("  flecha del párrafo reemplazada:", cuantas)

bloque = """          <span class="cotiza__alt-flecha" aria-hidden="true">
            <svg viewBox="0 0 32 16" fill="none" focusable="false">
              <path d="M1 8h27m0 0-7-6m7 6-7 6" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
          </span>
          <span class="cotiza__alt-flecha cotiza__alt-flecha--abajo" aria-hidden="true">
            <svg viewBox="0 0 16 32" fill="none" focusable="false">
              <path d="M8 1v27m0 0-6-7m6 7 6-7" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
          </span>"""

# Inserta ambas flechas justo después del párrafo de invitación
viejo_cierre = """            contacta con disponibilidad, versiones y opciones de compra.
          </p>"""
nuevo_cierre = """            contacta con disponibilidad, versiones y opciones de compra.
          </p>
""" + bloque
if viejo_cierre in h:
    h = h.replace(viejo_cierre, nuevo_cierre, 1)
    print("  flechas colocadas (escritorio y móvil)")

sec.write_text(h, encoding="utf-8", newline="\n")

# ----------------------------------------------------------------- CSS
css = RAIZ / "src/styles/apple.css"
c = css.read_text(encoding="utf-8")

# Reemplaza el bloque anterior de la flecha por uno limpio
c = re.sub(
    r"/\* Flecha que señala el formulario \*/.*?(?=\n/\*|\Z)",
    "",
    c,
    flags=re.S,
)

bloque_css = """
/* Flecha que señala el formulario */
.cotiza__alt-flecha {
  display: inline-flex;
  align-items: center;
  margin-left: 0.35rem;
  color: var(--gold, #c7a24c);
  vertical-align: -0.15em;
  animation: flecha-guia 1500ms var(--ease-out) infinite;
}

.cotiza__alt-flecha svg {
  width: 30px;
  height: 15px;
}

/* La versión vertical solo aparece en pantallas angostas */
.cotiza__alt-flecha--abajo {
  display: none;
}

@keyframes flecha-guia {
  0%,
  100% {
    transform: translateX(0);
  }
  50% {
    transform: translateX(7px);
  }
}

@keyframes flecha-guia-abajo {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(6px);
  }
}

/* En móvil el formulario queda debajo: flecha vertical centrada, fuera del texto */
@media (max-width: 979px) {
  .cotiza__alt-flecha {
    display: none;
  }

  .cotiza__alt-flecha--abajo {
    display: flex;
    justify-content: center;
    margin: 0.5rem 0 0.1rem;
    animation: flecha-guia-abajo 1500ms var(--ease-out) infinite;
  }

  .cotiza__alt-flecha--abajo svg {
    width: 17px;
    height: 34px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .cotiza__alt-flecha,
  .cotiza__alt-flecha--abajo {
    animation: none;
  }
}
"""

if "cotiza__alt-flecha--abajo" not in c:
    c = c.rstrip() + "\n" + bloque_css
    css.write_text(c, encoding="utf-8", newline="\n")
    print("  CSS de flechas actualizado")

# ------------------------------------------------------------ reconstruir
for comando in (["node", "scripts/build-index-html.mjs"], ["node", "build.mjs"]):
    r = subprocess.run(comando, cwd=RAIZ, capture_output=True, text=True)
    print("  ", comando[-1], "->", "OK" if r.returncode == 0 else r.stderr[:200])

html = (RAIZ / "index.html").read_text(encoding="utf-8")
print("  flecha escritorio:", 'cotiza__alt-flecha"' in html)
print("  flecha móvil:", "cotiza__alt-flecha--abajo" in html)
