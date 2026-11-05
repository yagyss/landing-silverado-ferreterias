/**
 * Movimiento e interacción ligada al scroll.
 * Todo se desactiva cuando el usuario pide movimiento reducido.
 */

import { $$, sinMovimiento } from "./dom.js";

let observadorReveal = null;

/** Aparición progresiva de bloques (.reveal) y rejillas (.stagger). */
export function initReveals() {
  const elementos = $$(".reveal, .stagger");
  if (!elementos.length) return;

  if (sinMovimiento() || !("IntersectionObserver" in window)) {
    elementos.forEach((elemento) => elemento.classList.add("is-in"));
    return;
  }

  observadorReveal = new IntersectionObserver(
    (entradas) => {
      entradas.forEach((entrada) => {
        if (!entrada.isIntersecting) return;
        entrada.target.classList.add("is-in");
        observadorReveal.unobserve(entrada.target);
      });
    },
    { rootMargin: "0px 0px -10% 0px", threshold: 0.08 }
  );

  elementos.forEach((elemento) => observadorReveal.observe(elemento));
}

/** Barra de progreso de lectura + estado del header al hacer scroll. */
export function initScrollUI() {
  const header = document.querySelector("[data-header]");
  const barra = document.getElementById("scroll-progress");
  let pendiente = false;

  const actualizar = () => {
    pendiente = false;
    const scrollY = window.scrollY || document.documentElement.scrollTop;

    if (header) header.classList.toggle("is-scrolled", scrollY > 12);

    if (barra) {
      const alto = document.documentElement.scrollHeight - window.innerHeight;
      const avance = alto > 0 ? Math.min(1, Math.max(0, scrollY / alto)) : 0;
      barra.style.transform = `scaleX(${avance.toFixed(4)})`;
    }

    actualizarParallax(scrollY);
  };

  const alScroll = () => {
    if (pendiente) return;
    pendiente = true;
    window.requestAnimationFrame(actualizar);
  };

  window.addEventListener("scroll", alScroll, { passive: true });
  window.addEventListener("resize", alScroll);
  actualizar();
}

/* -------------------------------------------------------------- Parallax 2.5D */
const capas = [];

function recolectarCapas() {
  capas.length = 0;
  $$("[data-parallax]").forEach((elemento) => {
    capas.push({
      elemento,
      factor: Number(elemento.getAttribute("data-parallax")) || 0.12,
      tope: Number(elemento.getAttribute("data-parallax-tope")) || 120,
    });
  });
}

function actualizarParallax(scrollY) {
  if (sinMovimiento() || !capas.length) return;
  capas.forEach(({ elemento, factor, tope }) => {
    const caja = elemento.getBoundingClientRect();
    const centro = caja.top + caja.height / 2 - window.innerHeight / 2;
    const desplazamiento = Math.max(-tope, Math.min(tope, centro * -factor));
    elemento.style.setProperty("--py", `${desplazamiento.toFixed(1)}px`);
  });
}

export function initParallax() {
  if (sinMovimiento()) return;
  recolectarCapas();
  window.addEventListener("resize", () => {
    recolectarCapas();
  });
}

/** Resalta el enlace de navegación de la sección visible. */
export function initActiveNav() {
  const enlaces = $$(".nav__link");
  if (!enlaces.length || !("IntersectionObserver" in window)) return;

  const porSeccion = new Map();
  enlaces.forEach((enlace) => {
    const id = (enlace.getAttribute("href") ?? "").replace("#", "");
    if (id) porSeccion.set(id, enlace);
  });

  const secciones = $$("main section[id]").filter((seccion) => porSeccion.has(seccion.id));
  if (!secciones.length) return;

  const observador = new IntersectionObserver(
    (entradas) => {
      entradas.forEach((entrada) => {
        if (!entrada.isIntersecting) return;
        enlaces.forEach((enlace) => enlace.classList.remove("is-active"));
        porSeccion.get(entrada.target.id)?.classList.add("is-active");
      });
    },
    { rootMargin: "-45% 0px -45% 0px", threshold: 0 }
  );

  secciones.forEach((seccion) => observador.observe(seccion));
}
