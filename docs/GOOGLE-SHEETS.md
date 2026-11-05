# Conectar la landing con Google Sheets + notificaciones por correo

Resultado: cada persona que envía el formulario queda registrada en una hoja de Google,
**recibe un correo de confirmación** y **te llega un aviso a ti** con todos sus datos.
Todo sin servidor propio.

```
Visitante → index.html (Netlify)
          → POST /api/cotizacion
          → proxy de Netlify (netlify.toml)
          → Google Apps Script
                ├─ escribe el lead en la hoja
                ├─ correo al prospecto
                └─ correo al administrador
          ← { ok: true, folio: "SV-…" }
```

---

## Paso 1 · Crear la hoja

1. Entra a <https://sheets.google.com> y crea una hoja nueva.
2. Nómbrala como quieras (por ejemplo **Cotizaciones Silverado**).
3. No escribas nada: el script crea encabezados y formato.

## Paso 2 · Pegar el script

1. En la hoja: **Extensiones → Apps Script**.
2. Borra `Código.gs` y pega completo [`google-apps-script.gs`](google-apps-script.gs).
3. Arriba, en `CONFIG`, cambia como mínimo:

```js
ADMIN_EMAIL: "tu-correo@tudominio.mx",   // aquí llegan los avisos de leads
RESPONDER_A: "tu-correo@tudominio.mx",
DISTRIBUIDOR: "Nombre del distribuidor",
TELEFONO: "+52 55 ...",
WHATSAPP: "52155...",                    // internacional, sin signos
HORARIO: "Lunes a sábado, 9:00 a 19:00 h",
```

4. Guarda (Ctrl/⌘ + S).

## Paso 3 · Ejecutar la instalación

1. En el editor de Apps Script, selecciona la función **`instalar`** y pulsa **Ejecutar**.
2. Autoriza los permisos (hoja + envío de correo). Es tu propia cuenta.
3. Debe crearse la pestaña **Panel** y llegarte **dos correos de prueba**
   (uno como administrador y otro como prospecto).

> Si no llegan, revisa **Spam** y la carpeta de promociones.

## Paso 4 · Publicar como aplicación web

1. **Implementar → Nueva implementación**.
2. Tipo: **Aplicación web**.
3. **Ejecutar como:** Yo · **Quién tiene acceso:** Cualquier persona.
4. Copia la URL (termina en `/exec`) y ábrela en el navegador:
   debe responder `{"ok":true,"servicio":"cotizaciones-silverado"}`.

## Paso 5 · Conectar la landing

1. En `netlify.toml`, reemplaza:
   ```toml
   to = "https://script.google.com/macros/s/AKfycbyo3rlLi4VGjD7-Kz-OsWSViRAPOasfpyCG6DornXqCwzOT_aXb1W-WtlM7znlLCAI-/exec"
   ```
   por tu URL real.
2. `node build.mjs`
3. Publica `dist/` en Netlify (arrastrar en <https://app.netlify.com/drop> o por Git).

## Paso 6 · Probar

1. Abre el dominio de Netlify y envía una cotización con **tu propio correo**.
2. Debe aparecer un renglón en la hoja, llegar el correo al prospecto y el aviso al administrador.
3. Revisa la pestaña **Panel**: totales, leads de hoy/semana, por alcaldía y por plan.

---

## Qué guarda cada lead

| Columna | Ejemplo |
| --- | --- |
| Folio | `SV-20261105-8ON1` |
| Fecha | `05/11/2026 18:42` |
| Nombre · Celular · Correo | datos del formulario |
| Plan | Contado · Financiamiento · Conocer opciones |
| Mensaje | lo que escribió el prospecto |
| Ciudad / Alcaldía | Coyoacán |
| Campaña · utm_* · fbclid · Referrer | origen de Meta Ads |
| **Estado** | Nuevo → Contactado → Cotizado → Ganado / Perdido |
| Asesor · Notas | para la gestión comercial |

El **Panel** calcula solo: total, nuevos, contactados, cotizados, ganados, perdidos,
leads de hoy, de la semana, por alcaldía y por plan.

## Correos automáticos

**Al prospecto** (`ENVIAR_CORREO_LEAD`): confirmación con folio, plan, ciudad y fecha,
teléfono/horario del distribuidor y botón de WhatsApp. Asunto:
*“Recibimos tu solicitud · Chevrolet Silverado (folio)”*.

**Al administrador** (`ENVIAR_CORREO_ADMIN`): aviso inmediato con nombre, celular
(liga directa a WhatsApp), correo, plan, ciudad, campaña, fecha y mensaje, más un botón
para abrir la hoja. Responde al correo del prospecto con un clic.

Puedes apagar cualquiera de los dos con `false` en `CONFIG`.

## Límites y buenas prácticas

- `MailApp`: **100 correos/día** con Gmail gratuito, **1,500/día** con Google Workspace.
- Los correos salen de la cuenta dueña de la hoja. Con Workspace, ejecuta el script desde
  `ventas@tudominio.mx` para que el remitente sea ese.
- El script ya valida, deduplica por celular (30 min) y bloquea spam.
- Si un correo falla, **el lead ya quedó guardado**: el sitio recibe `ok: true` igual.

## Si algo no funciona

| Síntoma | Causa probable |
| --- | --- |
| “No pudimos registrar…” en el sitio | URL del proxy sin reemplazar, o el deploy no incluyó `netlify.toml` |
| La hoja no recibe nada | Implementación no está como **Cualquier persona** |
| No llegan los correos | Ejecuta `instalar` y revisa **Ejecuciones** en Apps Script; revisa Spam |
| Duplicados | Ajusta `MINUTOS_DEDUPE` |
| Cambié el script y no cambia nada | Hay que crear **Nueva versión** de la implementación |

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
