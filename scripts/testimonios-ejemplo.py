"""Testimonios de ejemplo (marcados como tal) + estilos de la tarjeta."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------- site.js
ruta = RAIZ / "src/data/site.js"
t = ruta.read_text(encoding="utf-8")

inicio = t.index("  testimonios: {")
fin = t.index("  /* ------------------------------------------------- SECCIÓN 10")
actual = t[inicio:fin]

nuevo = '''  testimonios: {
    titulo: "Empresarios que saben lo que significa mover un negocio",
    /** Estados:
     *   "pendiente" → espacio reservado, sin contenido
     *   "borrador"  → ejemplos visibles, marcados como editables (para revisión)
     *   "publicado" → solo items con autorizado: true (requiere consentimiento)
     */
    estado: "borrador",
    items: [
      {
        rol: "Propietario",
        zona: "Ferretería en Coyoacán",
        sucursales: "2 sucursales",
        comentario:
          "Antes dependíamos de la agenda de los fletes. Ahora programamos la salida a sucursal el mismo día que llega el pedido y resolvemos lo urgente sin esperar a un tercero.",
        ejemplo: true,
        autorizado: false,
      },
      {
        rol: "Encargada de operaciones",
        zona: "Ferretería en Iztapalapa",
        sucursales: "3 sucursales",
        comentario:
          "Lo que más nos ha servido es mover material voluminoso entre sucursales sin contratar un viaje extra cada semana.",
        ejemplo: true,
        autorizado: false,
      },
      {
        rol: "Dueño",
        zona: "Ferretería en Tlalpan",
        sucursales: "1 sucursal",
        comentario:
          "Recoger mercancía directo con el proveedor nos dio margen para aceptar pedidos que antes teníamos que rechazar.",
        ejemplo: true,
        autorizado: false,
      },
    ],
    notaEjemplos:
      "Textos de ejemplo para revisar el diseño, no testimonios reales. Sustitúyelos por declaraciones autorizadas por escrito antes de publicar: en la configuración, cambia estado a «publicado» y marca cada testimonio con autorizado: true.",
    notaPendiente:
      "Espacio reservado para testimonios de empresarios ferreteros. Se publicarán únicamente con autorización por escrito del cliente y verificación del distribuidor.",
    resenasVerificadas: {
      titulo: "Reseñas verificadas del distribuidor",
      fuente: "",
      estado: "pendiente",
      nota:
        "Aquí se integrarán las reseñas verificadas del distribuidor autorizado (Google, Facebook o portal oficial). No se muestran reseñas de ejemplo.",
    },
  },

'''

t = t[:inicio] + nuevo + t[fin:]
ruta.write_text(t, encoding="utf-8", newline="\n")
print("  site.js: testimonios de ejemplo")

# ------------------------------------------------------------------- CSS
css = RAIZ / "src/styles/arte-final.css"
texto = css.read_text(encoding="utf-8")

bloque = """
/* ==========================================================================
   SECCIÓN 9 · Testimonios de ejemplo
   Tarjeta limpia, cita en primer plano y etiqueta visible de "ejemplo".
   ==========================================================================*/

.testimonios__tarjeta--ejemplo {
  position: relative;
  background: linear-gradient(168deg, #ffffff 0%, #fafbfc 100%);
  border: 1px solid rgba(11, 14, 19, 0.09);
  border-style: solid;
  box-shadow: 0 26px 50px -40px rgba(11, 14, 19, 0.55);
  padding-top: clamp(2.4rem, 3vw, 2.9rem);
}

.testimonios__chip {
  position: absolute;
  top: 1rem;
  right: 1rem;
  padding: 0.3rem 0.55rem;
  border-radius: var(--r-pill);
  border: 1px solid rgba(199, 162, 76, 0.5);
  background: rgba(199, 162, 76, 0.12);
  font-family: var(--font-display);
  font-size: 0.58rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--gold-deep);
}

.testimonios__tarjeta--ejemplo .testimonios__cita p {
  font-size: clamp(0.98rem, 1.25vw, 1.08rem);
  line-height: 1.6;
  color: var(--ink);
}

.testimonios__tarjeta--ejemplo .testimonios__avatar {
  border: 1px solid var(--line-strong);
  background: var(--mist);
  color: var(--steel);
}

.testimonios__tarjeta--ejemplo .testimonios__nombre {
  color: var(--ink);
}

.testimonios__tarjeta--ejemplo .testimonios__meta {
  color: var(--steel);
}
"""

if "Testimonios de ejemplo" not in texto:
    css.write_text(texto.rstrip() + "\n" + bloque, encoding="utf-8", newline="\n")
    print("  CSS de testimonios aplicado")
else:
    print("  ya aplicado")
