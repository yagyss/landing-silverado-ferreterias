"""Corrige la colisión de clases del hero y el sangrado del vehículo."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# --- HTML: el contenedor de contenido deja de llamarse hero__grid ---
ruta = RAIZ / "src/sections/01-hero.html"
t = ruta.read_text(encoding="utf-8")
t = t.replace('<div class="container hero__grid">', '<div class="container hero__layout">')
ruta.write_text(t, encoding="utf-8", newline="\n")
print("  hero__layout en HTML")

# --- CSS: los bloques nuevos apuntan al nuevo nombre ---
css = RAIZ / "src/styles/apple.css"
texto = css.read_text(encoding="utf-8")

# Solo en los bloques del hero a sangre (los que llevan .hero--cine)
texto = texto.replace(".hero--cine .hero__grid", ".hero--cine .hero__layout")

bloque = """
/* --- Corrección: contenedor del hero y sangrado del vehículo --- */
.hero--cine .hero__layout {
  position: relative !important;
  z-index: 3 !important;
  opacity: 1 !important;
  background: none !important;
}

.hero__stack {
  width: 124% !important;
  margin: 0 0 0 -6% !important;
  transform: translateY(clamp(0.5rem, 1.5vw, 1.25rem)) !important;
}

.hero__picker {
  margin: 0.4rem 0 0 2rem !important;
}

@media (max-width: 979px) {
  .hero__stack {
    width: 108% !important;
    margin: 0 -4% 0 0 !important;
    transform: none !important;
  }

  .hero__picker {
    margin: 0.75rem auto 0 !important;
  }
}
"""

if "Corrección: contenedor del hero" not in texto:
    css.write_text(texto.rstrip() + "\n" + bloque, encoding="utf-8", newline="\n")
    print("  bloque de corrección aplicado")

# --- index.html autónomo ---
import subprocess  # noqa: E402
subprocess.run(["node", "scripts/build-index-html.mjs"], cwd=RAIZ, check=False)
