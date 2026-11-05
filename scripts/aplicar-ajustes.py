"""Añade ajustes de integración (revisión del Lead) al final de las hojas CSS.

Se hace desde Python para garantizar UTF-8 sin BOM (PowerShell 5.1 corrompe
los acentos al releer/escribir archivos).
"""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

AJUSTES = {
    "src/styles/layout.css": """
/* ==========================================================================
   Ajustes de integración · barra de promoción y WhatsApp
   ==========================================================================*/

/* En móvil la barra de promoción debe caber en una sola línea */
@media (max-width: 759px) {
  .promo-bar {
    font-size: 0.58rem;
    letter-spacing: 0.035em;
    gap: 0.35rem;
    white-space: nowrap;
    overflow: hidden;
  }

  .promo-bar.is-visible {
    padding-block: 0.5rem;
  }

  .promo-bar__dot {
    width: 4px;
    height: 4px;
  }
}

/* Botón flotante discreto: círculo en todos los tamaños */
.wa-float {
  width: 56px;
  height: 56px;
  padding: 0;
  justify-content: center;
  border-radius: 50%;
}

.wa-float__label {
  display: none;
}

.wa-float__icon {
  width: 100%;
  height: 100%;
  background: transparent;
}

.wa-float__icon svg {
  width: 26px;
  height: 26px;
}

/* La insignia de configuración sólo aparece al interactuar con el botón */
.wa-float__badge {
  display: none;
  right: 0;
  left: auto;
}

.wa-float:hover .wa-float__badge,
.wa-float:focus-visible .wa-float__badge {
  display: block;
}
""",
    "src/styles/formulario.css": """
/* ------------------------------------------------- Ajustes de integración */
.cotiza__card-head {
  justify-items: start;
}

.cotiza__card-head .tag {
  justify-self: start;
  width: fit-content;
}
""",
    "src/styles/seccion-b.css": """
/* ==========================================================================
   Ajustes de integración (revisión final del Lead)
   ==========================================================================*/

/* La franja dorada lateral no debe desbordar el radio de la tarjeta */
.oferta__card {
  overflow: hidden;
}

/* Refuerzo el degradado del cierre para asegurar contraste del titular */
.cierre__scrim {
  background-image: linear-gradient(
      180deg,
      rgba(7, 9, 13, 0.3) 0%,
      rgba(7, 9, 13, 0.55) 38%,
      rgba(7, 9, 13, 0.9) 76%,
      rgba(7, 9, 13, 0.97) 100%
    ),
    linear-gradient(
      90deg,
      rgba(7, 9, 13, 0.82) 0%,
      rgba(7, 9, 13, 0.45) 44%,
      rgba(7, 9, 13, 0.12) 100%
    );
}

/* Carrusel de testimonios: 2 tarjetas en tablet y 3 en escritorio */
@media (min-width: 760px) {
  .testimonios__slide {
    flex-basis: calc((100% - var(--gap)) / 2);
  }
}

@media (min-width: 1080px) {
  .testimonios__slide {
    flex-basis: calc((100% - (2 * var(--gap))) / 3);
  }
}
""",
}

for relativa, bloque in AJUSTES.items():
    ruta = RAIZ / relativa
    original = ruta.read_text(encoding="utf-8")
    marca = "Ajustes de integración"
    if marca in original:
        print(f"  ya aplicado: {relativa}")
        continue
    ruta.write_text(original.rstrip() + "\n" + bloque, encoding="utf-8", newline="\n")
    print(f"  ajustes añadidos: {relativa}")
