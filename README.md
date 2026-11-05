# Chevrolet Silverado · Landing para ferreterías de la Ciudad de México

Landing page de campaña para Meta Ads dirigida a dueños de ferretería con una a cinco
sucursales. Presentación de producto premium (estilo Apple) con identidad Chevrolet,
copy en español (es‑MX) y captación real de prospectos.

> **Estado:** construida y verificada localmente. **No se publicó ni se desplegó** nada:
> la revisión y el lanzamiento quedan del lado del cliente.

---

## 1. Cómo verla en tu computadora

Requisitos: **Node.js 20 o superior**. No hay dependencias que instalar.

```bash
node server.mjs
```

Abre <http://127.0.0.1:4173>.

| Comando | Para qué sirve |
| --- | --- |
| `node server.mjs` | Vista local con ensamblado en vivo y API de cotizaciones |
| `node build.mjs` | Genera el sitio estático listo para publicar en `/dist` |
| `node scripts/qa-render.mjs` | Verifica que las 12 secciones y las hojas CSS estén completas |
| `node scripts/probar-api.mjs` | Pruebas del endpoint de prospectos (con el servidor corriendo) |
| `python scripts/procesar-imagenes.py` | Reprocesa la fotografía original a WebP responsivo |

Para revisar el formulario de punta a punta: envía una solicitud y luego visita
<http://127.0.0.1:4173/api/estado> para confirmar cuántos prospectos se registraron.

---

## 2. Qué incluye la página

Las 12 secciones solicitadas, en orden:

1. **Hero** — titular, subtítulo, atributos (potencia, robustez, capacidad de trabajo),
   CTA y selector de color real con las cinco carrocerías.
2. **Identificación del problema** — cuatro tarjetas sobre la logística que se queda atrás.
3. **Solución / presentación del vehículo** — composición con fotografía del vehículo y
   ficha técnica honesta (marcada como referencia hasta confirmar versión).
4. **Beneficios** — cinco beneficios operativos para la ferretería.
5. **Carga y remolque** — pieza de campaña, ejemplos de mercancía y descargo legal.
6. **Antes y después** — de depender de terceros a operar con vehículo propio.
7. **Promoción** — 1 año de seguro gratis y bono de hasta $198,000, con nota legal editable.
8. **Comparativa** — tabla en escritorio y tarjetas en móvil (sin cifras inventadas).
9. **Testimonios** — carrusel con tres ejemplos marcados como «Ejemplo editable» (estado `borrador`); al cargar testimonios autorizados y pasar a `publicado`, la marca desaparece. Ver `docs/PENDIENTES.md` §E.
10. **Preguntas frecuentes** — acordeón con las diez preguntas solicitadas.
11. **Formulario de cotización** — validación, registro real, deduplicación y antispam.
12. **Cierre** — composición cinematográfica con llamado final.

Además: navegación con desplazamiento suave, menú móvil, pie de página, aviso de privacidad
en diálogo y botón flotante de WhatsApp configurable.

---

## 3. Estructura del proyecto

```
.
├── server.mjs                 Servidor local sin dependencias (HTML + API)
├── build.mjs                  Genera /dist (sitio estático)
├── lib/render.mjs             Ensambla el documento a partir de parciales
├── api/cotizacion.mjs         Validación, deduplicación y registro de prospectos
├── src/
│   ├── data/site.js           ⚙️  CONFIGURACIÓN CENTRAL (textos, oferta, colores…)
│   ├── layout/                Header, footer, aviso de privacidad
│   ├── sections/              Una sección por archivo (01 → 12)
│   ├── styles/                tokens, base, layout, hero, showcase, secciones, formulario
│   └── js/                    Módulos ES del cliente (motion, showcase, formulario…)
├── assets/
│   ├── marca/                 Favicon, icono de app (logotipo oficial: ver pendientes)
│   ├── vehiculos/silverado/   Fotografía procesada en WebP (+ _originales)
│   └── og-silverado-ferreterias.jpg
├── data/prospectos.jsonl      Prospectos registrados (no se sirve por HTTP)
├── docs/                      Configuración, pendientes, migración y registro de QA
└── scripts/                   Utilidades de imagen, encoding y pruebas
```

La página se **renderiza en el servidor** a partir de parciales: cada sección es un archivo
independiente, lo que permite editar un bloque sin tocar los demás.

---

## 4. Dónde se edita cada cosa

Casi todo el contenido comercial vive en **`src/data/site.js`**:

- Datos de campaña, ciudad y público objetivo.
- **Promoción**: beneficios, vigencia (vacía = no se muestra), nota legal.
- **Colores** de carrocería y sus fotografías.
- **Ficha técnica** con interruptor `verificado` y nota de confirmación.
- **Preguntas frecuentes**, **comparativa**, **transformación antes/después**.
- **Testimonios**: hoy `estado: "pendiente"` (no se inventan personas).
- **Formulario**: opciones de alcaldía, sucursales, uso de vehículo y forma de compra.
- **WhatsApp**, datos de contacto del distribuidor, aviso de privacidad.
- **Seguimiento**: Meta Pixel, Conversion API, dataLayer.
- **Prospectos**: almacenamiento local, webhook y CRM.
- **Legales**: descargos de remolque, fotografía y promoción.

El detalle de cada campo está en [`docs/CONFIGURACION.md`](docs/CONFIGURACION.md).

---

## 5. Formulario y prospectos (funcionamiento real)

- Validación en el navegador **y** en el servidor con el mismo módulo
  (`src/js/validation.mjs`), evitando reglas divergentes.
- Cada solicitud se guarda en `data/prospectos.jsonl` con folio, fecha, campaña,
  UTM/fbclid, referrer y datos de contacto.
- **Deduplicación** por WhatsApp en una ventana configurable (30 min por defecto).
- **Antispam**: campo trampa invisible + tiempo mínimo de llenado + límite de peticiones.
- El mensaje de éxito **solo** aparece cuando el servidor confirma el registro. Si el
  registro falla, se muestra un error y una vía alterna por WhatsApp: nunca se simula un envío.
- Reenvío opcional a webhook o CRM (`SITE.leads`).

---

## 6. Publicación (cuando el cliente decida lanzar)

1. Genera el sitio: `node build.mjs` → carpeta `dist/`.
2. Sube `dist/` a cualquier hosting estático apuntando al dominio raíz.
3. Publica `api/cotizacion.mjs` como función serverless en el mismo dominio
   (ruta `/api/cotizacion`), con almacenamiento persistente o webhook a tu CRM.
4. Ajusta antes de lanzar: `SITE.meta.urlCanonica`, `SITE.leads.webhookUrl`,
   `SITE.whatsapp.numero`, `SITE.analitica.metaPixelId` y `SITE.desarrollo.mostrarMarcadores = false`.
5. Verifica el aviso de privacidad y las condiciones de la promoción con el área legal.

---

## 7. Notas de transparencia

- **Las fotografías son las que proporcionaste.** Se recortaron, se convirtieron a WebP y se
  generaron variantes de tamaño; no se alteró la camioneta (parrilla, faros, ruedas ni
  proporciones intactas). El remolque aparece únicamente en la pieza de campaña y se aclara
  que no está incluido.
- **No hay datos inventados**: ni precios, ni mensualidades, ni tasas, ni testimonios, ni
  clientes, ni fechas de vigencia. Las cifras técnicas provienen de material oficial del
  fabricante y se muestran marcadas como referencia hasta que el distribuidor confirme la
  versión vendida.
- **El logotipo oficial de Chevrolet no se pudo descargar** en el entorno de construcción
  (sin salida a internet). El sitio muestra el respaldo tipográfico “CHEVROLET” y queda listo
  para usar el archivo oficial en cuanto lo proporciones o haya conexión (ver pendientes).
- **Selector de color:** funciona de verdad, pero solo con las cinco fotografías recibidas
  (mismo ángulo). Si se agrega un color sin fotografía, no debe publicarse como disponible.
- La revisión visual se hizo con capturas automáticas de escritorio (1440 px) y móvil (390 px).
  Ver [`docs/REGISTRO-QA.md`](docs/REGISTRO-QA.md).

---

## 8. Documentación

| Documento | Contenido |
| --- | --- |
| [`docs/CONFIGURACION.md`](docs/CONFIGURACION.md) | Cada campo editable de `site.js` con ejemplos |
| [`docs/PENDIENTES.md`](docs/PENDIENTES.md) | Lo que falta del cliente y del distribuidor |
| [`docs/MIGRACION-NEXTJS.md`](docs/MIGRACION-NEXTJS.md) | Cómo llevar esto a React/Next.js si se decide escalar |
| [`docs/REGISTRO-QA.md`](docs/REGISTRO-QA.md) | Pruebas ejecutadas y resultados |

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
