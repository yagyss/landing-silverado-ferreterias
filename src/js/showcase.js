/**
 * Selector de color del hero.
 *
 * Reglas de robustez:
 *  - Delegación de clic en el grupo de swatches (funciona aunque los botones
 *    se vuelvan a pintar o cambien de orden).
 *  - El cambio se aplica por clase Y por estilo en línea, de modo que ningún
 *    conflicto de CSS pueda dejar la camioneta sin actualizar.
 *  - Teclado (flechas, Home, End) y anuncio accesible del color activo.
 */

import { SITE } from "../data/site.js";
import { esTactil, sinMovimiento } from "./dom.js";
import { track } from "./analytics.js";

const CLASE_ACTIVA = "is-active";

export function initShowcase() {
  const grupo = document.querySelector("[data-colors]");
  const imagenes = Array.from(document.querySelectorAll("[data-color-img]"));
  if (!grupo || !imagenes.length) return;

  const botones = () => Array.from(grupo.querySelectorAll("[data-color]"));
  const nombre = document.querySelector("[data-color-name]");
  const descripcion = document.querySelector("[data-color-desc]");
  const porColor = new Map((SITE.colores ?? []).map((c) => [c.id, c]));

  let actual = botones().find((b) => b.getAttribute("aria-checked") === "true")?.dataset.color;

  /** Aplica el color indicado. Devuelve true si hubo cambio. */
  function aplicar(id, { notificar = true, forzar = false } = {}) {
    if (!id) return false;
    const lista = botones();
    if (!lista.some((b) => b.dataset.color === id)) return false;
    if (!forzar && id === actual) return false;

    // 1) Imágenes: clase + estilo en línea (doble seguro)
    imagenes.forEach((img) => {
      const activa = img.dataset.colorImg === id;
      img.classList.toggle(CLASE_ACTIVA, activa);
      img.style.opacity = activa ? "1" : "0";
      img.style.zIndex = activa ? "2" : "1";
      img.style.pointerEvents = "none";
      img.setAttribute("aria-hidden", String(!activa));
    });

    // 2) Estado accesible de los botones
    lista.forEach((boton) => {
      const activo = boton.dataset.color === id;
      boton.setAttribute("aria-checked", String(activo));
      boton.tabIndex = activo ? 0 : -1;
    });

    // 3) Nombre y descripción (config, con respaldo en el propio botón)
    const color = porColor.get(id);
    const etiqueta = color?.nombre || lista.find((b) => b.dataset.color === id)?.dataset.nombre;
    if (nombre && etiqueta) nombre.textContent = etiqueta;
    if (descripcion && color) descripcion.textContent = color.descripcion;

    grupo.dataset.colorActivo = id;
    actual = id;

    if (notificar && color) {
      track("ColorSeleccionado", { color: color.nombre, color_id: color.id });
    }
    return true;
  }

  // Estado inicial consistente (por si el HTML y la config no coinciden)
  const inicial = actual ?? imagenes[0]?.dataset.colorImg;
  if (inicial) aplicar(inicial, { notificar: false, forzar: true });

  // 4) Un solo listener por delegación: cubre clics en el círculo o en su relleno
  grupo.addEventListener("click", (evento) => {
    const objetivo = evento.target instanceof Element ? evento.target.closest("[data-color]") : null;
    if (!objetivo || !grupo.contains(objetivo)) return;
    evento.preventDefault();
    aplicar(objetivo.dataset.color);
  });

  // 5) Teclado
  grupo.addEventListener("keydown", (evento) => {
    const lista = botones();
    const indice = lista.indexOf(document.activeElement);
    if (indice < 0) return;

    const mover = (destino) => {
      evento.preventDefault();
      const siguiente = lista[(destino + lista.length) % lista.length];
      siguiente.focus();
      aplicar(siguiente.dataset.color);
    };

    if (evento.key === "ArrowRight" || evento.key === "ArrowDown") mover(indice + 1);
    if (evento.key === "ArrowLeft" || evento.key === "ArrowUp") mover(indice - 1);
    if (evento.key === "Home") mover(0);
    if (evento.key === "End") mover(lista.length - 1);
    if (evento.key === " " || evento.key === "Enter") {
      evento.preventDefault();
      aplicar(lista[indice].dataset.color);
    }
  });

  // Precarga del resto de colores en cuanto el navegador esté libre
  const precargar = () => {
    imagenes.forEach((img) => {
      img.loading = "eager";
      if (img.decode) img.decode().catch(() => {});
    });
  };
  if ("requestIdleCallback" in window) window.requestIdleCallback(precargar, { timeout: 2000 });
  else setTimeout(precargar, 1200);

  /* ---------------------------------------------- Inclinación 2.5D (opcional) */
  const escenario = document.querySelector("[data-showcase-stage]");
  const pila = document.querySelector("[data-showcase-stack]");
  if (!escenario || !pila || sinMovimiento() || esTactil()) return;

  const MAX = 3.5;
  let raf = 0;

  escenario.addEventListener("pointermove", (evento) => {
    if (raf) return;
    raf = window.requestAnimationFrame(() => {
      raf = 0;
      const caja = escenario.getBoundingClientRect();
      if (!caja.width || !caja.height) return;
      const x = (evento.clientX - caja.left) / caja.width - 0.5;
      const y = (evento.clientY - caja.top) / caja.height - 0.5;
      pila.style.setProperty("--rx", `${(-y * MAX).toFixed(2)}deg`);
      pila.style.setProperty("--ry", `${(x * MAX).toFixed(2)}deg`);
    });
  });

  escenario.addEventListener("pointerleave", () => {
    if (raf) cancelAnimationFrame(raf);
    raf = 0;
    pila.style.setProperty("--rx", "0deg");
    pila.style.setProperty("--ry", "0deg");
  });
}
