"""Divide la captura completa en tramos legibles y actualiza documentación."""

from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
CAPTURAS = RAIZ / "docs" / "capturas"
completa = CAPTURAS / "landing-completa.jpg"

# --- Tramos de lectura (4 partes de la página completa) ---
if completa.exists():
    with Image.open(completa) as im:
        ancho, alto = im.size
        partes = 4
        salto = alto // partes
        for i in range(partes):
            desde = i * salto
            hasta = alto if i == partes - 1 else (i + 1) * salto
            tramo = im.crop((0, desde, ancho, hasta))
            destino = CAPTURAS / f"landing-parte-{i + 1}.jpg"
            tramo.save(destino, "JPEG", quality=82, optimize=True, progressive=True)
            print(f"  landing-parte-{i + 1}.jpg {tramo.size}")

# --- Documentación: testimonios de ejemplo ---
pend = RAIZ / "docs" / "PENDIENTES.md"
texto = pend.read_text(encoding="utf-8")

bloque = """
## E. Testimonios: cómo pasar de ejemplo a real

La sección 9 está hoy en **estado `borrador`**: muestra tres testimonios de ejemplo con la
etiqueta visible «Ejemplo editable», roles genéricos y zonas de la ciudad. No son clientes
reales ni deben publicarse así.

Para publicarlos:

1. Reunir dos o tres declaraciones con **autorización por escrito** (incluye el uso de nombre,
   negocio, foto si aplica, y el texto exacto).
2. En `src/data/site.js` → `testimonios.items`, reemplazar cada elemento por:

   ```js
   {
     nombre: "Nombre autorizado",
     negocio: "Ferretería ...",
     sucursales: "3 sucursales",
     comentario: "Texto literal autorizado",
     foto: "assets/testimonios/nombre.jpg", // opcional
     autorizado: true,
   }
   ```

3. Cambiar `estado: "borrador"` por `estado: "publicado"`.
4. El sitio sólo renderiza elementos con `autorizado: true`; la etiqueta de ejemplo y la nota
   desaparecen automáticamente.
5. Borrar `notaEjemplos` no es necesario: deja de mostrarse.

La sección de **reseñas verificadas** sigue pendiente de enlazar el perfil del distribuidor.
"""

if "cómo pasar de ejemplo a real" not in texto:
    pend.write_text(texto.rstrip() + "\n" + bloque, encoding="utf-8", newline="\n")
    print("  PENDIENTES actualizado con testimonios")

# --- README: nota sobre estados de testimonios ---
readme = RAIZ / "README.md"
t = readme.read_text(encoding="utf-8")
if "estado `borrador`" not in t:
    t = t.replace(
        "9. **Testimonios** — carrusel preparado; se muestra como contenido pendiente autorizado.",
        "9. **Testimonios** — carrusel con tres ejemplos marcados como «Ejemplo editable» "
        "(estado `borrador`); al cargar testimonios autorizados y pasar a `publicado`, la marca "
        "desaparece. Ver `docs/PENDIENTES.md` §E.",
    )
    readme.write_text(t, encoding="utf-8", newline="\n")
    print("  README actualizado")
