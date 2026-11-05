# Pendientes antes de publicar

Nada de lo que aparece en **A. Bloqueantes** es inventable: si falta, el sitio se ve
incompleto o se estaría afirmando algo falso. Los puntos de **B. Recomendados** mejoran
conversión, cumplimiento o rendimiento.

---

## A. Bloqueantes (los define el cliente / distribuidor)

| # | Pendiente | Dónde se configura | Consecuencia si falta |
| --- | --- | --- | --- |
| 1 | **Número de WhatsApp** del asesor | `SITE.whatsapp.numero` | El botón existe pero lleva al formulario; se muestra insignia de configuración |
| 2 | **Logotipo oficial de Chevrolet** (SVG o PNG) | `assets/marca/bowtie.svg` | Hoy se usa el respaldo tipográfico “CHEVROLET” |
| 3 | **Versión y equipamiento que se venderán** | `SITE.especificaciones` | Los datos quedan como “referencia oficial por confirmar” |
| 4 | **Vigencia exacta de la promoción** | `SITE.oferta.vigencia` | No se muestra fecha (correcto, pero la oferta pierde urgencia) |
| 5 | **Condiciones legales de la promoción** (bono, seguro, aseguradora, restricciones) | `SITE.oferta.notaLegal` | El texto actual es un descargo genérico |
| 6 | **Dominio canónico** | `SITE.meta.urlCanonica` | Open Graph y JSON‑LD apuntan a un dominio de ejemplo |
| 7 | **Distribuidor, teléfono, correo y horario** | `SITE.contacto` | El pie de página omite esos datos |
| 8 | **Revisión del aviso de privacidad** por el área legal | `SITE.formulario.privacidad` / `SITE.legales` | Riesgo de incumplimiento en captación de datos |
| 9 | **Destino de los prospectos** (CRM o webhook) | `SITE.leads` | Los leads quedan solo en `data/prospectos.jsonl` del servidor |
| 10 | **Meta Pixel ID** (y token de Conversion API si aplica) | `SITE.analitica` | No se mide la campaña |

## B. Recomendados

1. **Testimonios autorizados** (mínimo dos, con consentimiento por escrito y foto o logo del
   negocio). Hoy la sección se muestra como “contenido pendiente de autorización”, sin inventar
   personas ni experiencias.
2. **Reseñas verificadas del distribuidor** (Google Business Profile / Facebook). Integrar con
   enlace real; no se muestran reseñas de ejemplo.
3. **Fotografía con contexto de ferretería** (patio, bodega, carga real de material). Se tiene
   la fotografía del vehículo y la pieza de campaña, pero no una escena de uso real en CDMX.
   Habría que producirla o conseguirla con autorización. Evita el riesgo de imágenes de banco
   que no correspondan al producto real.
4. **Fotografía de los colores faltantes**, solo si se van a ofrecer más de los cinco actuales.
   Misma toma, mismo ángulo, mismo encuadre; de lo contrario el selector se rompe visualmente.
5. **Fuentes oficiales** `ChevySans-*.woff2` en `assets/fuentes/` para no depender del CDN ni
   de la fuente local. Mejora fidelidad de marca y evita un salto tipográfico.
6. **Archivo `robots.txt` / `sitemap.xml`** con el dominio real.
7. **Definir si se mostrará precio o mensualidad.** Hoy no se publica ninguno: no se inventan
   precios. Si el distribuidor los entrega, deben agregarse con su propio descargo y vigencia.
8. **Acordar el mensaje de seguimiento** posterior al envío del formulario (tiempo de respuesta
   y responsable), porque el sitio promete “un asesor se pondrá en contacto”.

## C. Decisiones técnicas tomadas (para tu revisión)

1. **Sin framework instalado.** El entorno de construcción no tuvo salida a internet ni acceso
   a npm, por lo que no fue posible instalar Next.js, React, Tailwind ni Framer Motion. Se
   construyó una implementación equivalente **sin dependencias** (HTML por parciales, CSS con
   variables de diseño y módulos ES nativos) que conserva componentes reutilizables, animaciones
   al hacer scroll y persistencia real de prospectos. La ruta de migración a Next.js está
   documentada en [`MIGRACION-NEXTJS.md`](MIGRACION-NEXTJS.md).
2. **2.5D en lugar de modelo 3D.** Solo se recibió una toma por color (mismo ángulo). Un
   vehículo 3D requeriría un modelo o una secuencia de ángulos que no existe; construir uno con
   el vehículo deformado habría violado la regla de no alterar la camioneta. Se implementó
   profundidad con capas, perspectiva, paralaje e inclinación sobre la fotografía original.
3. **El remolque no se incluye.** La imagen de campaña lo muestra con una aclaración explícita
   en la sección de carga y remolque.
4. **Sin precios.** Se prioriza la cotización como conversión, sin inventar cifras.

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
