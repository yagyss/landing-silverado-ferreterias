"""Añade la guía de actualización de una implementación existente."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ruta = RAIZ / "docs" / "GOOGLE-SHEETS.md"
texto = ruta.read_text(encoding="utf-8")

bloque = """
---

## Actualizar una implementación que ya existe (conservando la misma URL)

Si el endpoint responde algo distinto de `{"ok":true,…}` —por ejemplo
`{"result":"success"}` o “No se encontró la función doGet”— significa que la
implementación publicada está corriendo **otra versión del código**.

1. Abre el proyecto en <https://script.google.com> (el mismo que publicó la URL `/exec`).
2. Selecciona todo el contenido de `Código.gs` y **reemplázalo** por
   [`google-apps-script.gs`](google-apps-script.gs) completo.
3. Guarda (Ctrl/⌘ + S).
4. **Implementar → Administrar implementaciones**.
5. En la implementación activa, pulsa el **lápiz (Editar)**.
6. En *Versión*, elige **Nueva versión** y pulsa **Implementar**.

> Editar la implementación existente conserva la **misma URL `/exec`**, así que no
> hay que tocar `netlify.toml`.

Prueba rápida después de publicar: abre la URL `/exec` en el navegador. Debe mostrar

```json
{"ok":true,"servicio":"cotizaciones-silverado"}
```

Si sigue apareciendo el aviso de `doGet`, vuelve a revisar que guardaste el archivo
completo y que publicaste una **versión nueva** (no la anterior).
"""

if "Actualizar una implementación que ya existe" not in texto:
    ruta.write_text(texto.rstrip() + "\n" + bloque, encoding="utf-8", newline="\n")
    print("  guía de actualización añadida")
else:
    print("  ya existe la sección")
