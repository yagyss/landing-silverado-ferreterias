"""Corrige la composición a sangre de la sección 5 y el arnés de captura."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# ------------------------------------------------ Arnés de QA: carga forzada
qa = RAIZ / "src/layout/_qa-view.html"
t = qa.read_text(encoding="utf-8")
if "loading" not in t or "cargarTodo" not in t:
    t = t.replace(
        "        const ir = () => {",
        "        // Para la captura: evita que las imágenes diferidas queden sin cargar\n"
        "        const cargarTodo = () => {\n"
        "          documento.querySelectorAll('img[loading=\"lazy\"]').forEach((img) => {\n"
        "            img.loading = 'eager';\n"
        "          });\n"
        "        };\n\n"
        "        const ir = () => {\n"
        "          cargarTodo();",
    )
    qa.write_text(t, encoding="utf-8", newline="\n")
    print("  arnés actualizado")

# -------------------------------------------------------- Sección 5: rejilla
css = RAIZ / "src/styles/arte-final.css"
texto = css.read_text(encoding="utf-8")

bloque = """
/* --- Remolque a sangre: composición en rejilla (corrige el traslape) --- */
@media (min-width: 1080px) {
  .remolque--sangre .remolque-layout.remolque-layout {
    display: grid;
    grid-template-columns: minmax(0, 47%) minmax(0, 53%);
    align-items: stretch;
    gap: clamp(1.5rem, 3vw, 3rem);
  }

  .remolque--sangre .remolque-poster.remolque-poster {
    position: relative;
    inset: auto;
    width: auto;
    height: 100%;
    margin: 0 calc(50% - 50vw) 0 0;
    padding: 0;
    background: transparent;
    border: 0;
    border-radius: 0;
    overflow: hidden;
  }

  .remolque--sangre .remolque-poster.remolque-poster img {
    width: 100%;
    height: 100%;
    min-height: 620px;
    object-fit: cover;
    object-position: 54% 42%;
    border-radius: 0;
  }

  .remolque--sangre .remolque-poster.remolque-poster::after {
    background: linear-gradient(
      90deg,
      #080c13 0%,
      rgba(8, 12, 19, 0.85) 12%,
      rgba(8, 12, 19, 0.25) 34%,
      rgba(8, 12, 19, 0) 58%
    );
  }

  .remolque--sangre .remolque-contenido.remolque-contenido {
    max-width: none;
    padding-block: 0.5rem;
  }

  .remolque--sangre .remolque-lista.remolque-lista {
    grid-template-columns: minmax(0, 1fr);
  }

  .remolque--sangre .remolque-fotos.remolque-fotos {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

/* Evita el bloque blanco bajo el póster en cualquier ancho */
.remolque--sangre .remolque-poster {
  background: transparent;
  border: 0;
  box-shadow: none;
}
"""

if "corrige el traslape" not in texto:
    css.write_text(texto.rstrip() + "\n" + bloque, encoding="utf-8", newline="\n")
    print("  composición de remolque corregida")
else:
    print("  ya aplicado")
