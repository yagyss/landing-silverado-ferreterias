/**
 * Capa de seguimiento de conversiones.
 *
 * - Meta Pixel: sólo se carga si SITE.analitica.metaPixelId tiene valor.
 *   Con el ID vacío NO se inyecta ningún script de terceros (cero cookies).
 * - dataLayer: empuja todos los eventos por si se conecta GTM/GA4.
 * - Eventos del brief: PageView, ViewContent, CTA (personalizado) y Lead.
 * - Conversion API: se ejecuta del lado del servidor (ver api/cotizacion.mjs)
 *   porque el token no debe viajar al navegador.
 */

import { SITE } from "../data/site.js";

const CONFIG = SITE.analitica;
const LOG = Boolean(SITE.desarrollo?.logEventos);

let inicializado = false;
const enviados = new Set();

function registrarEnConsola(evento, parametros) {
  if (!LOG) return;
  // eslint-disable-next-line no-console
  console.info(`[seguimiento] ${evento}`, parametros ?? {});
}

function inyectarPixel() {
  if (!CONFIG.metaPixelId) return;
  if (window.fbq) return;

  /* Stub oficial de Meta */
  const fbq = function (...args) {
    if (fbq.callMethod) fbq.callMethod.apply(fbq, args);
    else fbq.queue.push(args);
  };
  fbq.push = fbq;
  fbq.loaded = true;
  fbq.version = "2.0";
  fbq.queue = [];
  window.fbq = fbq;

  const script = document.createElement("script");
  script.async = true;
  script.src = "https://connect.facebook.net/en_US/fbevents.js";
  document.head.appendChild(script);

  window.fbq("init", CONFIG.metaPixelId);
}

function empujarDataLayer(evento, parametros) {
  if (!CONFIG.dataLayer) return;
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({
    event: evento,
    campana: SITE.campana.id,
    ...parametros,
  });
}

/**
 * @param {string} evento
 * @param {Record<string, unknown>} [parametros]
 * @param {{ unaVez?: boolean }} [opciones]
 */
export function track(evento, parametros = {}, opciones = {}) {
  const { unaVez = false } = opciones;
  if (unaVez && enviados.has(evento)) return;
  enviados.add(evento);

  const mapa = {
    PageView: "PageView",
    ViewContent: "ViewContent",
    Lead: "Lead",
  };

  if (CONFIG.activo !== false) {
    const tipoPixel = mapa[evento];
    if (typeof window.fbq === "function") {
      if (tipoPixel) window.fbq("track", tipoPixel, parametros);
      else window.fbq("trackCustom", evento, parametros);
    }
  }

  empujarDataLayer(evento, parametros);
  registrarEnConsola(evento, parametros);
}

/** Inicializa pixel, PageView y delegación global de clics en CTAs. */
export function initAnalitica() {
  if (inicializado) return;
  inicializado = true;

  inyectarPixel();

  if (CONFIG.eventos.pageView) {
    track("PageView", { content_name: `${SITE.marca.nombre} ${SITE.marca.modelo}` });
  }

  // Delegación: cualquier [data-cta] dispara evento de conversión de CTA.
  document.addEventListener("click", (evento) => {
    const objetivo = evento.target instanceof Element ? evento.target.closest("[data-cta]") : null;
    if (!objetivo) return;
    if (!CONFIG.eventos.ctaClick) return;
    track("CtaClick", {
      ubicacion: objetivo.getAttribute("data-cta") ?? "desconocida",
      texto: (objetivo.textContent ?? "").trim().slice(0, 80),
    });
  });

  // ViewContent cuando el producto (hero) ya es visible.
  const producto = document.querySelector("[data-showcase]");
  if (producto && CONFIG.eventos.viewContent && "IntersectionObserver" in window) {
    const observador = new IntersectionObserver(
      (entradas) => {
        entradas.forEach((entrada) => {
          if (entrada.isIntersecting) {
            track(
              "ViewContent",
              {
                content_name: `${SITE.marca.nombre} ${SITE.marca.modelo}`,
                content_category: "camioneta de trabajo",
                content_ids: [SITE.campana.id],
              },
              { unaVez: true }
            );
            observador.disconnect();
          }
        });
      },
      { threshold: 0.25 }
    );
    observador.observe(producto);
  }
}

/** Evento de prospecto enviado (llamado únicamente tras confirmación del servidor). */
export function trackLead(datos = {}) {
  track("Lead", {
    content_name: `${SITE.marca.nombre} ${SITE.marca.modelo}`,
    content_category: "cotizacion-ferreteria",
    value: 1,
    currency: "MXN",
    ...datos,
  });
}

