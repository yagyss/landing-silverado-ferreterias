# Registro de QA

Fecha de revisión: noviembre 2026 · Entorno: Windows, Node.js 24, servidor local `node server.mjs`.

---

## 1. Ensamblado y contenido

| Prueba | Resultado |
| --- | --- |
| `node scripts/qa-render.mjs` | 12/12 secciones presentes · 66.6 kB de HTML · 8 hojas de estilo · script de cliente enlazado · 2 bloques JSON‑LD |
| IDs duplicados en el documento ensamblado | Ninguno |
| Anclas internas (`href="#…"`) sin destino | Ninguna |
| Rutas de imagen referenciadas | Todas existen y responden 200 (`image/webp`) |
| Acentos y caracteres españoles | Verificados tras reparar un problema de doble codificación (ver §6) |

## 2. Formulario y API (pruebas automatizadas)

`node scripts/probar-api.mjs` → **16 de 16 comprobaciones correctas**:

- Alta válida → `201` con folio (`SV-AAAAMMDD-XXXX`).
- Mismo WhatsApp en la ventana de deduplicación → `200` con `duplicado: true`.
- Nombre inválido, WhatsApp incompleto y alcaldía fuera del catálogo → `422` con errores por campo.
- Campo trampa (honeypot) → `422` (rechazado).
- Envío instantáneo (menos del tiempo mínimo de llenado) → `422` (rechazado).
- `GET /api/cotizacion` → `405`.
- Persistencia en `data/prospectos.jsonl`: nombre con acentos intacto, UTM de campaña guardada,
  campaña asociada y preparación del evento `Lead`.
- `GET /api/estado` → conteo de prospectos.

## 3. Hidratación del cliente (DOM real en navegador)

Volcado del DOM después de ejecutar el JavaScript (`--dump-dom`), comprobando que los datos de
configuración se renderizaron en el navegador:

| Elemento | Resultado |
| --- | --- |
| Barra de promoción con montos | OK |
| Ficha técnica hidratada con aviso “Referencia oficial por confirmar” | OK |
| Tabla comparativa (6 criterios × 3 vehículos) | OK |
| Acordeón de 10 preguntas con `aria-expanded` | OK |
| Carrusel de testimonios en estado pendiente | OK |
| Beneficios de la promoción desde config | OK |
| Cierre cinematográfico | OK |
| Selects del formulario con las 16 alcaldías | OK |
| Pie de página con descargo legal | OK |
| WhatsApp en estado “sin configurar” | OK |
| Marcador de error de inicialización (`app-error`) | Ausente (ningún módulo falló) |

## 4. Revisión visual

Capturas automáticas de **escritorio (1440 px)** y **móvil (390 px reales)** de las 12 secciones.
Las capturas móviles requirieron fijar el viewport a 390 px dentro de un iframe porque Chrome
headless en Windows impone un ancho mínimo de ventana (~504 px). Evidencia en
[`capturas/`](capturas/):

| Archivo | Sección |
| --- | --- |
| `01-hero-escritorio.jpg` | Hero con selector de color |
| `02-hero-movil.jpg` | Hero en 390 px |
| `03-promocion.jpg` | Beneficios de lanzamiento |
| `04-comparativa.jpg` | Tabla comparativa |
| `05-formulario.jpg` | Formulario de cotización |
| `06-cierre.jpg` | Cierre cinematográfico |

Defectos encontrados y corregidos durante la revisión:

1. Barra de promoción partida en tres líneas en móvil → ajustada a una línea.
2. Botón flotante de WhatsApp demasiado ancho y tapando contenido → convertido en círculo;
   la insignia de configuración ahora aparece solo al interactuar.
3. Logotipo roto en el header → se sustituyó por respaldo tipográfico con carga en cascada.
4. Titular del hero sobredimensionado → escala reducida y atributos en tres columnas.
5. Etiquetas móviles duplicadas dentro de la tabla comparativa en escritorio → ocultas; columnas
   equilibradas con `table-layout: fixed`.
6. Píldora fantasma de vigencia vacía en la promoción → oculta cuando no hay fecha.
7. Avatar de testimonios ambiguo → reemplazado por un marcador genérico de persona.
8. Tarjetas de testimonios cortadas en escritorio → 3 por fila.
9. Contraste del titular del cierre sobre zonas claras de la fotografía → degradado reforzado.
10. Avatares/datos de ficha técnica sin señal de estado → leyenda “Referencia oficial por confirmar”.

## 5. Comportamiento sin JavaScript

- Las secciones narrativas (hero, problema, solución, beneficios, remolque) se ven completas: el
  contenido crítico no depende de JS.
- Las secciones dinámicas incluyen `<noscript>` explicando que requieren JavaScript o invitando a
  cotizar por el formulario/WhatsApp.
- El formulario no envía sin JavaScript: es intencional, para no perder solicitudes en silencio.

## 6. Incidencias técnicas resueltas durante el desarrollo

1. **Bloqueo de Chrome/Edge headless por el sandbox** (canales IPC). Se resolvió ejecutando la
   captura con permisos elevados y rutas absolutas de salida.
2. **Doble codificación (mojibake) en archivos editados desde PowerShell 5.1**: su `Get-Content`
   y se detectó comparando el texto renderizado: los acentos aparecían como dos caracteres extraños.
   Se reparó con scripts/reparar-encoding.py (reversión Latin-1 -> UTF-8). Los archivos se
   verificaron uno por uno; hoy el proyecto queda 100 % en UTF‑8 y las utilidades de parcheo
   escriben con Python para no repetir el problema.
3. **Sin salida a internet ni npm**: no fue posible instalar el stack solicitado; se documentó la
   decisión y la ruta de migración (ver `MIGRACION-NEXTJS.md`).
4. **Logotipo y fuentes oficiales inaccesibles sin red**: se dejaron ranuras de configuración y
   respaldos locales (tipografía Bahnschrift / wordmark).

## 7. Qué no se pudo verificar en este entorno

- Prueba de manejo real del teclado y lectores de pantalla: el código usa roles, `aria-expanded`,
  `aria-checked`, foco visible y navegación por flechas, pero conviene una pasada con VoiceOver o
  NVDA antes de publicar.
- Prueba de envío desde un dispositivo móvil físico y de apertura real de WhatsApp (requiere
  número configurado).
- Métricas de campo (Lighthouse/CrUX): la página no se desplegó. Aun así, la fotografía está en
  WebP con variantes de 390 px a 1700 px y la única librería externa posible es el pixel de Meta,
  que solo se activa al configurarlo.

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
