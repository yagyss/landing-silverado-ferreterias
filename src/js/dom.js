/** Utilidades DOM mínimas y helpers compartidos. */

export const $ = (selector, raiz = document) => raiz.querySelector(selector);
export const $$ = (selector, raiz = document) => Array.from(raiz.querySelectorAll(selector));

export const on = (elemento, evento, handler, opciones) => {
  if (!elemento) return () => {};
  elemento.addEventListener(evento, handler, opciones);
  return () => elemento.removeEventListener(evento, handler, opciones);
};

export const sinMovimiento = () =>
  typeof window !== "undefined" &&
  window.matchMedia("(prefers-reduced-motion: reduce)").matches;

export const esTactil = () =>
  typeof window !== "undefined" && window.matchMedia("(hover: none)").matches;

/** Escapa texto para insertarlo como HTML de forma segura. */
export function escapar(texto) {
  return String(texto ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

/** Ejecuta callback sólo cuando el nodo entra en pantalla (una vez). */
export function alEntrar(elemento, callback, { margen = "0px 0px -12% 0px", repetir = false } = {}) {
  if (!elemento) return;
  if (!("IntersectionObserver" in window)) {
    callback();
    return;
  }
  const observador = new IntersectionObserver(
    (entradas) => {
      entradas.forEach((entrada) => {
        if (entrada.isIntersecting) {
          callback(entrada);
          if (!repetir) observador.disconnect();
        }
      });
    },
    { rootMargin: margen, threshold: 0.05 }
  );
  observador.observe(elemento);
}

/** Debounce para eventos de scroll/resize. */
export function debounce(fn, espera = 150) {
  let t;
  return (...args) => {
    clearTimeout(t);
    t = setTimeout(() => fn(...args), espera);
  };
}

/** Lee los parámetros de campaña de la URL actual. */
export function leerUtm() {
  const params = new URLSearchParams(window.location.search);
  const claves = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "fbclid"];
  return Object.fromEntries(claves.map((clave) => [clave, params.get(clave) ?? ""]));
}
