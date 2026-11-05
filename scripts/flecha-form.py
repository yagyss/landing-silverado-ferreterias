"""Quita la nota de autocompletado y añade una flecha que guía al formulario."""

import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sec = RAIZ / "src/sections/11-cotizacion.html"
h = sec.read_text(encoding="utf-8")

# 1) Quitar la nota del autocompletado
nota = (
    '          <p class="cotiza__card-sub" id="form-ayuda">'
    "Puedes llenarlo más rápido con el autocompletado de tu navegador.</p>\n"
)
if nota in h:
    h = h.replace(nota, "")
    print("  nota de autocompletado eliminada")

# 2) Quitar la referencia aria-describedby a esa nota
h = h.replace(' aria-describedby="form-ayuda"', "")
print("  aria-describedby retirado")

# 3) Flecha en el mensaje que invita a llenar el formulario
viejo = """          <p class="cotiza__alt-text">
            <strong>Completa el siguiente formulario</strong>: son cinco datos y un asesor te
            contacta con disponibilidad, versiones y opciones de compra.
          </p>"""

nuevo = """          <p class="cotiza__alt-text">
            <strong>Completa el siguiente formulario</strong>: son cinco datos y un asesor te
            contacta con disponibilidad, versiones y opciones de compra.
            <span class="cotiza__alt-flecha" aria-hidden="true">
              <svg viewBox="0 0 32 16" fill="none" focusable="false">
                <path d="M1 8h27m0 0-7-6m7 6-7 6" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
            </span>
          </p>"""

if viejo in h:
    h = h.replace(viejo, nuevo)
    print("  flecha agregada al mensaje")
else:
    print("  (no coincidió el bloque del mensaje)")

sec.write_text(h, encoding="utf-8", newline="\n")

# 4) CSS de la flecha
css = RAIZ / "src/styles/apple.css"
c = css.read_text(encoding="utf-8")

bloque = """
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

@keyframes flecha-guia {
  0%,
  100% {
    transform: translateX(0);
  }
  50% {
    transform: translateX(7px);
  }
}

/* En pantallas angostas el formulario queda debajo: la flecha apunta hacia abajo */
@media (max-width: 979px) {
  .cotiza__alt-flecha {
    display: flex;
    margin: 0.5rem 0 0;
    transform: rotate(90deg);
    transform-origin: left center;
    animation: none;
  }
}

@media (prefers-reduced-motion: reduce) {
  .cotiza__alt-flecha {
    animation: none;
  }
}
"""

if "cotiza__alt-flecha" not in c:
    css.write_text(c.rstrip() + "\n" + bloque, encoding="utf-8", newline="\n")
    print("  CSS de la flecha agregado")

# 5) Reconstruir
for comando in (["node", "scripts/build-index-html.mjs"], ["node", "build.mjs"]):
    r = subprocess.run(comando, cwd=RAIZ, capture_output=True, text=True)
    print("  ", comando[-1], "->", "OK" if r.returncode == 0 else r.stderr[:200])

html = (RAIZ / "index.html").read_text(encoding="utf-8")
print("  nota eliminada:", "autocompletado de tu navegador" not in html)
print("  flecha presente:", "cotiza__alt-flecha" in html)
