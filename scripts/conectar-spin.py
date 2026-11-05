"""Conecta el visor interactivo (arrastre) en el hero."""

import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------ HTML
hero = RAIZ / "src/sections/01-hero.html"
t = hero.read_text(encoding="utf-8")

t = t.replace(
    '<div class="hero__stack-wrap" data-showcase data-showcase-stage>',
    '<div class="hero__stack-wrap" data-showcase data-showcase-stage data-spin data-spin-stage>',
)
t = t.replace('<div class="hero__stack" data-showcase-stack>', '<div class="hero__stack" data-showcase-stack data-spin-stack>')

if "data-spin-hint" not in t:
    t = t.replace(
        "</div>\n      </div>\n    </div>\n  </div>\n</section>",
        '  <span class="hero__hint" data-spin-hint>'
        '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M8 12H3m0 0 2.5-2.5M3 12l2.5 2.5M16 12h5m0 0-2.5-2.5M21 12l-2.5 2.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
        "Arrastra para explorar</span>\n"
        "</div>\n      </div>\n    </div>\n  </div>\n</section>",
    )

hero.write_text(t, encoding="utf-8", newline="\n")
print("  hero con data-spin")

# ------------------------------------------------------------------- CSS
css = RAIZ / "src/styles/apple.css"
c = css.read_text(encoding="utf-8")

bloque = """
/* ==========================================================================
   VISOR INTERACTIVO · arrastre para explorar la camioneta
   ==========================================================================*/

.hero__stack-wrap {
  position: relative;
  perspective: 1700px;
  cursor: grab;
  touch-action: pan-y;
  user-select: none;
}

.hero__stack-wrap.is-arrastrando {
  cursor: grabbing;
}

.hero__stack {
  transform: translateY(clamp(0.5rem, 1.5vw, 1.25rem)) rotateY(var(--giro, 0deg))
    rotateX(var(--inclina, 0deg)) !important;
  transform-style: preserve-3d;
  transition: transform 260ms var(--ease-out);
  will-change: transform;
}

.hero__stack.is-retorno {
  transition: transform 640ms var(--ease-spring);
}

.hero__stack-wrap.is-arrastrando .hero__stack {
  transition: none;
}

/* Un brillo tenue acompaña el giro para reforzar la sensación de volumen */
.hero__stack-wrap::after {
  content: "";
  position: absolute;
  inset: 6% 12% 18% 8%;
  border-radius: 50%;
  pointer-events: none;
  background: radial-gradient(60% 50% at 50% 40%, rgba(255, 255, 255, 0.1), transparent 70%);
  opacity: 0.6;
  transform: translateX(calc(var(--desfase, 0px) * 1.4));
  filter: blur(18px);
  z-index: 0;
}

/* Pista de interacción */
.hero__hint {
  position: absolute;
  left: 50%;
  bottom: -0.25rem;
  transform: translateX(-50%);
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.4rem 0.8rem;
  border-radius: var(--r-pill);
  border: 1px solid rgba(255, 255, 255, 0.16);
  background: rgba(8, 12, 18, 0.66);
  backdrop-filter: blur(14px);
  font-size: 0.7rem;
  letter-spacing: 0.04em;
  color: #c3ccd8;
  white-space: nowrap;
  pointer-events: none;
  transition: opacity 420ms var(--ease-out), transform 420ms var(--ease-out);
  z-index: 4;
}

.hero__hint svg {
  width: 14px;
  height: 14px;
  color: var(--gold-bright);
}

.hero__hint.is-oculta {
  opacity: 0;
  transform: translate(-50%, 6px);
}

@media (max-width: 979px) {
  .hero__hint {
    bottom: -0.5rem;
  }
}

@media (prefers-reduced-motion: reduce) {
  .hero__stack {
    transform: translateY(0) !important;
  }

  .hero__hint {
    display: none;
  }
}
"""

if "VISOR INTERACTIVO" not in c:
    css.write_text(c.rstrip() + "\n" + bloque, encoding="utf-8", newline="\n")
    print("  CSS del visor aplicado")

# -------------------------------------------------------------------- JS
main = RAIZ / "src/js/main.js"
m = main.read_text(encoding="utf-8")

if "initSpin" not in m:
    m = m.replace(
        'import { initShowcase } from "./showcase.js";',
        'import { initShowcase } from "./showcase.js";\nimport { initSpin } from "./spin.js";',
    )
    m = m.replace('["showcase", initShowcase],', '["showcase", initShowcase],\n    ["spin", initSpin],')
    main.write_text(m, encoding="utf-8", newline="\n")
    print("  main.js con initSpin")

# --------------------------------------------------------- Configuración
site = RAIZ / "src/data/site.js"
s = site.read_text(encoding="utf-8")

if "angulos:" not in s:
    s = s.replace(
        "  galeria: {\n    colores:",
        "  galeria: {\n    /** Secuencia de fotogramas para el giro 360 (opcional).\n"
        "     *  Con 8 o más rutas, el visor del hero las recorre al arrastrar.\n"
        "     *  Formato: \"assets/vehiculos/silverado/giro-001.webp\", …\n"
        "     *  Si queda vacío, el visor inclina la fotografía en 3D. */\n"
        "    angulos: [],\n    colores:",
    )
    site.write_text(s, encoding="utf-8", newline="\n")
    print("  site.js con galeria.angulos")

# ------------------------------------------------------------- Reconstruir
for comando in (["node", "scripts/build-index-html.mjs"], ["node", "build.mjs"]):
    r = subprocess.run(comando, cwd=RAIZ, capture_output=True, text=True)
    print("  ", comando[-1], "->", "OK" if r.returncode == 0 else r.stderr[:200])

for archivo in ("src/js/spin.js", "src/js/main.js", "src/data/site.js"):
    r = subprocess.run(["node", "--check", archivo], cwd=RAIZ, capture_output=True, text=True)
    print(f"  {archivo}: {'OK' if r.returncode == 0 else 'ERROR'}")
    if r.returncode != 0:
        print(r.stderr[:300])

html = (RAIZ / "index.html").read_text(encoding="utf-8")
print("  data-spin en index:", html.count("data-spin"), "| pista:", html.count("data-spin-hint"))
