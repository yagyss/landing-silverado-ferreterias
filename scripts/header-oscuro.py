"""Encabezado y menú móvil en grafito para acompañar el hero cinematográfico."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ruta = RAIZ / "src/styles/layout.css"
texto = ruta.read_text(encoding="utf-8")

marca = "HEADER OSCURO (arte final)"
if marca in texto:
    print("  ya aplicado")
    raise SystemExit(0)

bloque = """
/* ==========================================================================
   HEADER OSCURO (arte final)
   El hero es un escenario nocturno: el encabezado se integra en grafito y
   conserva la legibilidad sobre las secciones claras con blur + borde tenue.
   ==========================================================================*/

.site-header {
  background: rgba(7, 10, 17, 0.72);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.site-header.is-scrolled {
  background: rgba(7, 10, 17, 0.94);
  border-bottom-color: rgba(255, 255, 255, 0.12);
  box-shadow: 0 18px 40px -28px rgba(0, 0, 0, 0.9);
}

.brand {
  color: #ffffff;
}

.brand__mark {
  min-width: auto;
}

.brand__logo {
  height: 30px;
  filter: drop-shadow(0 1px 6px rgba(0, 0, 0, 0.45));
}

.brand__wordmark {
  color: var(--gold-bright);
}

.brand__divider {
  background: rgba(255, 255, 255, 0.16);
}

.brand__model {
  color: rgba(255, 255, 255, 0.92);
}

.nav__link {
  color: rgba(238, 241, 245, 0.66);
}

.nav__link:hover,
.nav__link.is-active {
  color: #ffffff;
}

.menu-toggle {
  color: #ffffff;
  border-color: rgba(255, 255, 255, 0.16);
  background: rgba(255, 255, 255, 0.06);
}

.mobile-menu {
  background: #080c13;
  border-bottom-color: rgba(255, 255, 255, 0.1);
  box-shadow: 0 30px 60px -30px rgba(0, 0, 0, 0.9);
}

.mobile-menu__link {
  color: #eef1f5;
  border-color: rgba(255, 255, 255, 0.09);
}

.mobile-menu__foot {
  color: #7d8794;
}

/* La barra de promoción se separa del hero con una línea dorada tenue */
.promo-bar.is-visible {
  border-bottom: 1px solid rgba(199, 162, 76, 0.22);
  background: linear-gradient(90deg, #05070b 0%, #0a0f18 50%, #05070b 100%);
}
"""

ruta.write_text(texto.rstrip() + "\n" + bloque, encoding="utf-8", newline="\n")
print("  header oscuro aplicado")
