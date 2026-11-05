# Migración a Next.js + React (si se decide escalar)

La entrega actual funciona **sin dependencias**. Si el proyecto crece (multi‑marca, CMS,
varias campañas, A/B testing), esta es la ruta de migración conservando el diseño y el copy.

---

## Por qué la entrega actual no usa Next.js

El entorno donde se construyó esta landing **no tenía salida a internet** y la caché de npm no
incluía Next.js: `npm install` no pudo completarse. En lugar de entregar una maqueta sin
funcionar, se implementó el sitio completo sin dependencias, con la misma separación por
componentes. Todo el HTML se genera en el servidor y la interactividad está en módulos ES.

## Mapa de equivalencias

| Actual (sin dependencias) | Next.js equivalente |
| --- | --- |
| `lib/render.mjs` (ensambla parciales) | `app/page.tsx` + Server Components |
| `src/sections/01-hero.html … 12-cta-final.html` | `components/sections/Hero.tsx`, etc. |
| `src/layout/header.html` / `footer.html` | `components/layout/Header.tsx` / `Footer.tsx` |
| `src/data/site.js` | `data/site.ts` (tipado) o CMS |
| `src/styles/tokens.css` | mismo archivo + Tailwind `theme.extend` si se desea |
| `src/js/motion.js` | `framer-motion` (`whileInView`, `useScroll`, `useTransform`) |
| `src/js/showcase.js` | componente cliente con estado de color + `useMotionValue` |
| `src/js/formulario.js` | `react-hook-form` + `zod` (misma validación en el servidor) |
| `src/js/analytics.js` | `next/script` + hook de eventos |
| `src/js/secciones-b.js` | componentes con estado (acordeón, carrusel, tabla) |
| `api/cotizacion.mjs` | `app/api/cotizacion/route.ts` |
| `server.mjs` | `next dev` / `next start` |
| `build.mjs` | `next build` (SSG/ISR) |

## Componentes ya pensados para React

La estructura de secciones y clases CSS está separada por bloque, así que el traslado es
casi mecánico:

```
components/
  layout/Header.tsx          ← src/layout/header.html + src/js/nav.js
  layout/Footer.tsx          ← src/layout/footer.html + initFooter()
  layout/WhatsAppFloat.tsx   ← botón flotante
  sections/Hero.tsx          ← 01-hero
  sections/ProblemSection.tsx        ← 02
  sections/VehicleShowcase.tsx       ← 03 + hero showcase
  sections/ColorSelector.tsx         ← selector real (estado)
  sections/BenefitsSection.tsx       ← 04
  sections/TrailerSection.tsx        ← 05
  sections/TransformationSection.tsx ← 06
  sections/OfferSection.tsx          ← 07
  sections/ComparisonTable.tsx       ← 08
  sections/Testimonials.tsx          ← 09
  sections/FAQ.tsx                   ← 10
  sections/QuoteForm.tsx             ← 11
  sections/FinalCTA.tsx              ← 12
```

## Pasos sugeridos

1. `npx create-next-app@latest --ts --app --tailwind` (cuando haya red).
2. Copiar `src/styles/tokens.css` y `base.css` tal cual; el resto de hojas se puede importar
   por componente o convertir a módulos CSS.
3. Copiar `src/data/site.js` a `data/site.ts` y tipar las estructuras (`Color`, `Benefit`,
   `FAQItem`, `Prospect`).
4. Migrar cada sección a un componente; los textos se reciben por props o se importan de
   `site.ts`. Mantener el HTML semántico actual.
5. En el formulario, reutilizar la validación: mover `src/js/validation.mjs` a
   `lib/validation.ts` y usarla tanto en el cliente como en la ruta de API (la lógica ya es
   isomorfa).
6. Sustituir la animación por IntersectionObserver por `motion.div` con `whileInView` y
   `viewport={{ once: true }}`, respetando `useReducedMotion()`.
7. `app/api/cotizacion/route.ts` puede reutilizar directamente `api/cotizacion.mjs`.
8. Configurar variables de entorno: `META_CAPI_TOKEN`, `CRM_WEBHOOK_URL`, `LEADS_FILE`.
9. Verificar que la migración conserve: deduplicación, antispam, folio, UTM y mensajes
   honestos de éxito/error.

## Lo que no debe cambiar en la migración

- El copy en es‑MX y el orden de las 12 secciones.
- La honestidad de los datos: nada de precios, testimonios, vigencia o cifras sin fuente.
- Las notas legales de promoción y de remolque.
- El respeto a `prefers-reduced-motion`.
- El peso de la página: la fotografía ya está optimizada en WebP con variantes responsivas.
