"""Sección 5: el póster pasa a fondo de sección y a miniatura de contenido."""

import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ruta = RAIZ / "src/sections/05-remolque.html"
t = ruta.read_text(encoding="utf-8")

# 1) Fondo de sección (decorativo, no depende de carga diferida de <img>)
if "remolque__fondo" not in t:
    t = t.replace(
        '<section id="remolque" class="section remolque remolque--sangre" aria-labelledby="remolque-title">',
        '<section id="remolque" class="section remolque remolque--sangre" aria-labelledby="remolque-title">\n'
        '  <span class="remolque__fondo" aria-hidden="true"></span>',
    )

# 2) Se retira la figura grande del póster del flujo del layout
patron = re.compile(r"\n\s*<figure class=\"remolque-poster reveal\">.*?</figure>", re.S)
t, eliminados = patron.subn("", t)

# 3) Miniatura accesible del póster dentro de la franja de fotos
if "remolque-fotos" in t and "Pieza de campaña" not in t:
    miniatura = """<figure class="remolque-foto remolque-foto--poster">
              <img
                src="/assets/vehiculos/silverado/campana-remolque-800.webp"
                alt="Pieza de campaña del fabricante: una Silverado blanca remolca una plataforma cargada con materiales de construcción; la imagen incluye los textos «MÁS CAPACIDAD DE CARGA» y «SILVERADO»."
                width="800"
                height="1000"
                loading="lazy"
                decoding="async"
              />
              <figcaption>Pieza de campaña del fabricante.</figcaption>
            </figure>
            """
    t = t.replace('<div class="remolque-fotos">', '<div class="remolque-fotos">\n            ' + miniatura, 1)

ruta.write_text(t, encoding="utf-8", newline="\n")
print(f"  sección 5 reestructurada (figuras retiradas: {eliminados})")

# 4) CSS del fondo
css = RAIZ / "src/styles/arte-final.css"
texto = css.read_text(encoding="utf-8")

bloque = """
/* --- Remolque: póster como fondo de sección (versión determinista) --- */
.remolque__fondo {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  z-index: 0;
  background-image: url("/assets/vehiculos/silverado/campana-remolque-1122.webp");
  background-repeat: no-repeat;
  background-position: 50% 50%;
  background-size: cover;
  pointer-events: none;
}

.remolque__fondo::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(
      180deg,
      rgba(8, 12, 19, 0.55) 0%,
      rgba(8, 12, 19, 0.25) 45%,
      rgba(8, 12, 19, 0.75) 100%
    ),
    linear-gradient(
      90deg,
      #080c13 0%,
      rgba(8, 12, 19, 0.94) 30%,
      rgba(8, 12, 19, 0.55) 58%,
      rgba(8, 12, 19, 0.2) 100%
    );
}

@media (min-width: 1080px) {
  .remolque--sangre .remolque__fondo {
    width: min(62vw, 1000px);
    background-position: 52% 42%;
  }

  .remolque--sangre .remolque__fondo::after {
    background: linear-gradient(
      90deg,
      #080c13 0%,
      rgba(8, 12, 19, 0.92) 26%,
      rgba(8, 12, 19, 0.35) 62%,
      rgba(8, 12, 19, 0) 100%
    );
  }

  .remolque--sangre .remolque-contenido.remolque-contenido {
    max-width: 560px;
  }

  .remolque--sangre .remolque-fotos.remolque-fotos {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

/* Miniatura del póster dentro de la franja de fotos */
.remolque--sangre .remolque-foto--poster img {
  aspect-ratio: 4 / 5;
  object-fit: cover;
  object-position: 50% 24%;
}
"""

if "versión determinista" not in texto:
    css.write_text(texto.rstrip() + "\n" + bloque, encoding="utf-8", newline="\n")
    print("  CSS de fondo aplicado")
else:
    print("  ya aplicado")
