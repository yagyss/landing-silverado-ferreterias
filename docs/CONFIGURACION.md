# Configuración de la landing

Todo el contenido editable vive en **`src/data/site.js`**. Este documento explica cada
bloque y qué ocurre cuando se deja un valor vacío.

---

## 1. `meta` — metadatos y SEO

```js
meta: {
  titulo: "Chevrolet Silverado para ferreterías | Movilidad para tu negocio",
  descripcion: "…",
  urlCanonica: "https://silverado-ferreterias.example.com/",
  imagenOg: "assets/og-silverado-ferreterias.jpg",
  …
}
```

- `urlCanonica` **debes cambiarla** por el dominio real antes de publicar: se usa para las
  etiquetas Open Graph, la imagen para Meta/WhatsApp y el JSON‑LD.
- `imagenOg` debe ser una ruta pública de 1200 × 630 px. Ya existe una pieza generada.

## 2. `marca` — identidad

- `logo.local`: ruta al archivo oficial (por ejemplo `assets/marca/bowtie.svg`).
- `logo.remoto`: URL oficial en el CDN del fabricante.
- Si ambos fallan, el sitio usa el respaldo tipográfico `CHEVROLET` sin romperse.

## 3. `oferta` — promoción

| Campo | Efecto |
| --- | --- |
| `activa` | Si es `false`, la barra superior de promoción no aparece |
| `beneficios[]` | Tarjetas principales: `etiqueta` (grande) + `titulo` + `detalle` |
| `vigencia` | Texto libre. **Vacío = no se muestra ninguna fecha** (no se inventa) |
| `notaCorta` / `notaLegal` | Notas al pie de la sección y condición legal completa |
| `cta` | Texto del botón |

La barra superior del sitio se construye automáticamente a partir de `beneficios[]`.

## 4. `colores[]` — selector de color

Cada elemento necesita `id`, `nombre`, `hex`, `hexSombra` y `descripcion`.
Los archivos de imagen se esperan en:

```
assets/vehiculos/silverado/color-{id}-1400.webp
assets/vehiculos/silverado/color-{id}-900.webp
```

> **Importante:** el selector solo debe ofrecer colores con fotografía real. Si se agrega un
> color sin imagen, aparecerá un hueco visual y no es honesto anunciarlo como disponible.

## 5. `especificaciones` — ficha técnica

```js
especificaciones: {
  verificado: false,
  versionReferencia: "Silverado Custom 4x4 (2026)",
  items: [{ etiqueta: "Potencia", valor: "355 hp" }, …],
  nota: "Cifras de referencia…",
}
```

- Mientras `verificado` sea `false`, cada dato muestra la leyenda
  «Referencia oficial por confirmar».
- Al confirmar la versión vendida: actualiza `items`, cambia `verificado: true` y ajusta la nota.
- **Nunca** agregues datos que no provengan de la ficha técnica oficial.

## 6. `transformacion`, `comparativa`, `faq`, `testimonios`

- `transformacion.antes` / `.despues`: listas de una línea por elemento.
- `comparativa.filas[].evaluacion`: `"alto" | "medio" | "bajo"` — solo cualitativo.
- `faq.items[]`: pares `{ p, r }`. Se recomienda respuestas de 2 a 4 líneas.
- `testimonios.estado`:
  - `"pendiente"` → carrusel de espacios marcados como *contenido pendiente de autorización*.
  - `"publicado"` → se muestran `items[]` con `autorizado: true`.
  - Solo publica testimonios con consentimiento por escrito.

## 7. `formulario`

- `endpoint`: ruta del API (por defecto `/api/cotizacion`).
- `opciones.ciudad` / `sucursales` / `usoVehiculo` / `interes`: catálogos de los controles.
  El servidor valida contra estas mismas listas, así que **son la única fuente de verdad**.
- `mensajes`: textos de éxito, error y duplicado. `{folio}` se sustituye por el folio real.
- `privacidad.urlAviso` y `.textoAviso`: aviso mostrado en el diálogo del pie.

## 8. `whatsapp`

```js
whatsapp: {
  activo: true,
  numero: "5215512345678", // formato internacional sin signos
  mensaje: "Hola, me interesa cotizar…",
}
```

- Con `numero` vacío: el botón permanece visible, lleva al formulario y (en revisión local)
  muestra una insignia de configuración. **No se inventa ningún número.**
- Con número: abre WhatsApp con el mensaje prellenado.

## 9. `analitica` — Meta Pixel y Conversion API

```js
analitica: {
  metaPixelId: "",        // vacío = no se carga ningún script de terceros
  conversionApi: { activo: false, endpoint: "", token: "" },
  dataLayer: true,
  eventos: { pageView: true, viewContent: true, ctaClick: true, lead: true },
}
```

- Con `metaPixelId` vacío el sitio no carga cookies ni scripts de Meta.
- Eventos enviados: `PageView`, `ViewContent`, `CtaClick` (personalizado) y `Lead`.
- El token de la Conversion API **no debe ir en el navegador**: se configura como variable de
  entorno del servidor y el envío se hace desde el backend.

## 10. `leads` — destino de los prospectos

```js
leads: {
  almacenamiento: "archivo-local",   // archivo-local | webhook | crm
  webhookUrl: "",
  crm: { proveedor: "", endpoint: "", tokenEnv: "" },
  archivo: "data/prospectos.jsonl",
  dedupeMinutos: 30,
}
```

- Cada prospecto se guarda como una línea JSON; el folio tiene el formato `SV-AAAAMMDD-XXXX`.
- Si defines `webhookUrl`, el servidor reenvía el prospecto y registra si el webhook confirmó.
- `data/` no se sirve por HTTP (el servidor solo publica `assets`, `styles`, `js`, `data` del
  cliente y layouts), por lo que los datos personales no quedan expuestos.

## 11. `desarrollo`

- `mostrarMarcadores: true` muestra insignias de configuración pendiente (por ejemplo, el
  WhatsApp sin número). Ponlo en `false` antes de publicar.
- `logEventos: true` imprime los eventos de seguimiento en la consola del navegador.

## 12. Cambios de diseño

- Colores, tipografía, sombras y movimiento: `src/styles/tokens.css`.
- El resto de hojas consume esas variables; evita valores hexadecimales sueltos.
- Tipografía: se intenta la fuente oficial (`ChevySans-*.woff2`) y, si no está disponible,
  el navegador usa **Bahnschrift** (DIN, incluida en Windows). Para uso 100 % offline coloca
  los archivos oficiales en `assets/fuentes/` (las reglas `@font-face` ya los buscan).
