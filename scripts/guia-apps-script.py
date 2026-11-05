"""Añade registro de errores en una pestaña para poder diagnosticar."""

from pathlib import Path
import subprocess

RAIZ = Path(__file__).resolve().parent.parent
ruta = RAIZ / "docs" / "google-apps-script.gs"
t = ruta.read_text(encoding="utf-8")

# 1) Función de registro de errores
if "function registrarError_" not in t:
    t = t.replace(
        "/* ============================================================== recepción */",
        '''function registrarError_(donde, error, detalle) {
  try {
    const libro = libro_();
    let hoja = libro.getSheetByName("Errores");
    if (!hoja) {
      hoja = libro.insertSheet("Errores");
      hoja.appendRow(["Fecha", "Dónde", "Mensaje", "Detalle"]).setFontWeight("bold");
    }
    hoja.appendRow([new Date(), donde, String(error), String(detalle || "").slice(0, 500)]);
  } catch (e) {
    console.error("No se pudo registrar el error: " + e);
  }
}

/* ============================================================== recepción */''',
    )

# 2) Registrar el fallo en el catch del doPost
t = t.replace(
    """  } catch (fallo) {
    console.error(fallo);
    return respuesta_({
      ok: false,
      codigo: "servidor",
      mensaje: "No pudimos registrar la solicitud. Intenta de nuevo.",
    });""",
    """  } catch (fallo) {
    console.error(fallo);
    registrarError_("doPost", fallo, "");
    return respuesta_({
      ok: false,
      codigo: "servidor",
      mensaje: "No pudimos registrar la solicitud. Intenta de nuevo.",
    });""",
)

ruta.write_text(t, encoding="utf-8", newline="\n")
print("  registro de errores agregado")

copia = RAIZ / "apps-script-check.js"
copia.write_text(t, encoding="utf-8")
r = subprocess.run(["node", "--check", str(copia)], capture_output=True, text=True)
print("  sintaxis:", "OK" if r.returncode == 0 else r.stderr[:300])
copia.unlink(missing_ok=True)

# 3) Guía ultra corta
guia = RAIZ / "docs" / "PASO-A-PASO-APPS-SCRIPT.md"
guia.write_text(
    """# Apps Script en 10 pasos (para que el formulario registre)

Si el formulario no registra, el 99% de las veces es porque **la URL publicada
pertenece a otro proyecto** o a una **versión vieja** del código.

## Hacerlo desde cero, sin dudas

1. Abre tu hoja de cálculo.
2. Menú **Extensiones → Apps Script**. (Ábrelo desde la hoja, no desde script.google.com.)
3. Selecciona todo el código (Ctrl+A) y bórralo.
4. Abre el archivo `docs/google-apps-script.gs` de este proyecto, cópialo **completo** y pégalo.
5. Cambia en `CONFIG` solo esta línea:
   `ADMIN_EMAIL: "tu-correo@tudominio.mx"`
6. Guarda con **Ctrl+S**.
7. En la lista de funciones (arriba), elige **`verificar`** y pulsa **Ejecutar**.
   Debe abrir un aviso con el nombre de tu hoja. Si no lo abre, este proyecto no está
   ligado a la hoja: repite el paso 2.
8. Elige **`instalar`** y pulsa **Ejecutar** → autoriza los permisos.
   Deben llegarte **dos correos de prueba** y crearse las columnas que faltan.
9. **Implementar → Nueva implementación**
   - Engrane ⚙️ → **Aplicación web**
   - *Ejecutar como*: **Yo**
   - *Quién tiene acceso*: **Cualquier persona**
   - **Implementar**
10. Aparece un cuadro con la **URL de la aplicación web**. **Cópiala de ahí.**
    Esa URL es distinta a cualquier anterior.

## Verificar (obligatorio)

Abre esa URL en el navegador. Debe mostrar exactamente:

```json
{"ok":true,"servicio":"cotizaciones-silverado"}
```

- Si muestra eso → **funciona**. Pega esa URL en `netlify.toml` (o mándamela).
- Si dice “No se encontró la función doGet” → estás abriendo la URL vieja.
- Si dice `{"result":"success"}` → esa URL es de otro proyecto.

## Limpiar implementaciones viejas (recomendado)

**Implementar → Administrar implementaciones** → en cada implementación que no uses,
menú ⋮ → **Archivar**. Así solo queda una URL viva y no hay confusión.

## Si nada de eso funciona

Pega el siguiente código mínimo en un proyecto **nuevo** (Archivo → Nuevo proyecto),
implementa como aplicación web y prueba la URL:

```javascript
function doGet() {
  return ContentService.createTextOutput(JSON.stringify({ ok: true, prueba: "vivo" }))
    .setMimeType(ContentService.MimeType.JSON);
}
function doPost(e) {
  return ContentService.createTextOutput(JSON.stringify({ ok: true, recibido: e.postData ? e.postData.contents : "" }))
    .setMimeType(ContentService.MimeType.JSON);
}
```

Si con eso la URL responde `{"ok":true,"prueba":"vivo"}`, el mecanismo funciona y el
problema era solo el proyecto/versión.
""",
    encoding="utf-8",
    newline="\n",
)
print("  guía PASO-A-PASO-APPS-SCRIPT.md creada")
