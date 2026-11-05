"""Actualiza la documentación tras el rediseño y limpia evidencia antigua."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CAPTURAS = RAIZ / "docs" / "capturas"

# Evidencia anterior sustituida por la de esta ronda
for viejo in ("03-promocion.jpg", "04-comparativa.jpg", "05-formulario.jpg",
              "06-cierre.jpg", "06-promocion.jpg"):
    ruta = CAPTURAS / viejo
    if ruta.exists():
        ruta.unlink()
        print(f"  eliminado docs/capturas/{viejo}")

# ---------------------------------------------------------------- README
readme = RAIZ / "README.md"
texto = readme.read_text(encoding="utf-8")

bloque = """
---

## 9. Dirección de arte (segunda ronda)

La primera versión resolvía la estructura pero se veía como una ficha de catálogo:
la camioneta aparecía en una tarjeta blanca, el dorado se leía pardo y el encabezado
era texto plano. La segunda ronda cambió el lenguaje visual completo:

- **Hero cinematográfico.** Escenario nocturno en grafito con halos de luz, grano sutil
  y piso de luz. La Silverado se recortó del fondo de estudio (PNG con transparencia),
  de modo que flota sobre el fondo oscuro con sombra propia, en lugar de vivir dentro
  de una tarjeta. El selector de color sigue siendo funcional con las cinco carrocerías.
- **Logotipo oficial real.** El bowtie se extrajo del propio póster de campaña que
  proporcionó el cliente (`assets/marca/chevrolet-bowtie.png`) y ahora aparece en el
  encabezado, en lugar del respaldo tipográfico.
- **Encabezado en grafito** translúcido con el emblema y “SILVERADO”, integrado con el hero.
- **Sección de producto (03) convertida en escenario nocturno**: la unidad flota sobre un
  piso de luz con un “SILVERADO” fantasma detrás del titular.
- **Secciones claras en clave editorial**: el problema y los beneficios dejaron de ser
  tarjetas con borde y pasaron a columnas separadas por líneas finas, con numeración
  discreta y mucho más aire.
- **Oro metálico** recalibrado (de pardo a dorado luminoso) en títulos, botones y reglas.

Los archivos nuevos de esta ronda son `src/styles/arte-final.css` (capa de dirección de
arte que se carga al final), `assets/marca/chevrolet-bowtie.png`,
`assets/marca/chevrolet-lockup.png` y los `assets/vehiculos/silverado/cutout-*.webp`.
El script `scripts/extraer-recursos.py` documenta y reproduce la extracción.

Evidencia: [`docs/capturas/`](docs/capturas/).
"""

if "Dirección de arte (segunda ronda)" not in texto:
    readme.write_text(texto.rstrip() + "\n" + bloque, encoding="utf-8", newline="\n")
    print("  README actualizado")

# ---------------------------------------------------------- REGISTRO DE QA
qa = RAIZ / "docs" / "REGISTRO-QA.md"
texto = qa.read_text(encoding="utf-8")

bloque_qa = """
---

## 8. Revisión de arte (ronda 2)

Motivo: la primera entrega, aunque funcional, se percibía como una ficha de catálogo.

Cambios de dirección de arte:

1. Hero rediseñado como escenario nocturno con la camioneta recortada (fondo de estudio
   eliminado con alfa y halo limpio), halos de luz, grano y piso de luz.
2. Bowtie oficial extraído del póster de campaña del cliente e integrado en el encabezado.
3. Encabezado y menú móvil en grafito translúcido.
4. Sección 03 convertida en escenario cinematográfico; se eliminó la tarjeta blanca.
5. Sección 02 y 04 pasaron de tarjetas con borde a composición editorial con líneas finas.
6. Oro metálico recalibrado; botones y acentos con degradado luminoso.

Defectos detectados y corregidos en esta ronda:

| Defecto | Corrección |
| --- | --- |
| Restos de sombra de estudio (parches blancos bajo el chasis) | Recorte por silueta columna a columna + limpieza de halo |
| Titular del hero en seis líneas, empujaba el CTA fuera del pliegue | Escala reducida y espaciado compactado |
| Tarjeta blanca alrededor de la camioneta | Reemplazada por escenario con transparencia |
| Beneficios con alturas forzadas y hueco central | Altura natural y rejilla de 3 columnas |
| Dorado percibido como pardo | Degradado metálico con parada clara |
| Palabra fantasma “SILVERADO” cortada en el hero | Se retiró del hero y se reubicó en la sección 03 |

Verificación: capturas de escritorio (1440 px) y móvil (390 px reales) de hero, producto,
problema, beneficios, promoción, formulario y cierre; sin errores 404 y con el selector
de color operativo.
"""

if "Revisión de arte (ronda 2)" not in texto:
    qa.write_text(texto.rstrip() + "\n" + bloque_qa, encoding="utf-8", newline="\n")
    print("  REGISTRO-QA actualizado")

# -------------------------------------------------------------- PENDIENTES
pend = RAIZ / "docs" / "PENDIENTES.md"
texto = pend.read_text(encoding="utf-8")

bloque_pend = """
---

## D. Actualización tras el rediseño

- **Logotipo:** el encabezado ya muestra el bowtie oficial, extraído del material de campaña
  que compartiste. Aun así conviene sustituirlo por el archivo vectorial oficial
  (`bowtie.svg`) cuando lo tengas: la extracción es fiel pero es un mapa de bits.
- **Fotografía adicional:** con el recorte con transparencia, agregar tomas nuevas (patio,
  bodega, carga real) multiplicaría el impacto del hero y de la sección de producto. Solo se
  necesitan el mismo ángulo y encuadre para que el selector de color no salte.
- **Tipografía:** el sitio funciona con Bahnschrift como respaldo. Las fuentes oficiales
  `ChevySans-*.woff2` en `assets/fuentes/` darían el último punto de fidelidad de marca.
"""

if "Actualización tras el rediseño" not in texto:
    pend.write_text(texto.rstrip() + "\n" + bloque_pend, encoding="utf-8", newline="\n")
    print("  PENDIENTES actualizado")
