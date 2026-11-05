"""Composición final de la sección 3 (escenario nocturno)."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ruta = RAIZ / "src/styles/arte-final.css"
texto = ruta.read_text(encoding="utf-8")

bloque = """
/* --- Composición de la sección 3: respiración y anclaje de la unidad --- */
.solucion--cine .solucion-layout {
  align-items: start;
  gap: clamp(2rem, 4vw, 3.5rem);
}

.solucion--cine .solucion-stage {
  padding-inline: clamp(0.5rem, 2.5vw, 2rem);
  padding-block: clamp(0.5rem, 1.5vw, 1rem) 0;
}

.solucion--cine .solucion-figura {
  position: relative;
}

/* Piso de luz bajo la camioneta */
.solucion--cine .solucion-figura::after {
  content: "";
  position: absolute;
  left: 50%;
  bottom: 12%;
  width: 60%;
  height: 40px;
  transform: translateX(-50%);
  background: radial-gradient(ellipse at center, rgba(0, 0, 0, 0.55), rgba(0, 0, 0, 0) 70%);
  filter: blur(10px);
  z-index: 0;
  pointer-events: none;
}

.solucion--cine .solucion-stage__tag {
  top: 0.25rem;
  left: auto;
  right: 0.5rem;
}

.solucion--cine .solucion-item:first-child {
  border-top: 0;
}

@media (min-width: 1080px) {
  .solucion--cine .solucion-layout {
    grid-template-columns: minmax(0, 1.15fr) minmax(0, 0.85fr);
  }

  .solucion--cine .solucion-stage {
    padding-inline: clamp(1rem, 3.5vw, 3rem);
  }
}
"""

if "Composición de la sección 3" not in texto:
    ruta.write_text(texto.rstrip() + "\n" + bloque, encoding="utf-8", newline="\n")
    print("  polish sección 3 aplicado")
else:
    print("  ya aplicado")
