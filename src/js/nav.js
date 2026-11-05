/**
 * Navegación: menú móvil accesible, desplazamiento suave compensado por el
 * header fijo y cierre del menú al navegar.
 */

const MENU_SELECTOR = "[data-mobile-menu]";

export function initNavegacion() {
  const boton = document.querySelector("[data-menu-toggle]");
  const menu = document.querySelector(MENU_SELECTOR);
  const header = document.querySelector("[data-header]");

  const altoHeader = () => (header ? header.getBoundingClientRect().height : 68);

  const posicionar = () => {
    if (!menu || !header) return;
    menu.style.setProperty("--menu-top", `${Math.round(header.getBoundingClientRect().bottom)}px`);
  };

  const cerrar = () => {
    if (!menu || !boton) return;
    menu.hidden = true;
    boton.setAttribute("aria-expanded", "false");
    boton.setAttribute("aria-label", "Abrir menú");
    document.body.classList.remove("menu-open");
  };

  const abrir = () => {
    if (!menu || !boton) return;
    posicionar();
    menu.hidden = false;
    boton.setAttribute("aria-expanded", "true");
    boton.setAttribute("aria-label", "Cerrar menú");
    document.body.classList.add("menu-open");
    menu.querySelector("a, button")?.focus({ preventScroll: true });
  };

  boton?.addEventListener("click", () => {
    const abierto = boton.getAttribute("aria-expanded") === "true";
    if (abierto) cerrar();
    else abrir();
  });

  document.querySelectorAll("[data-menu-link]").forEach((enlace) => {
    enlace.addEventListener("click", () => cerrar());
  });

  document.addEventListener("keydown", (evento) => {
    if (evento.key === "Escape" && boton?.getAttribute("aria-expanded") === "true") {
      cerrar();
      boton.focus();
    }
  });

  window.addEventListener("resize", () => {
    posicionar();
    if (window.innerWidth >= 1080 && boton?.getAttribute("aria-expanded") === "true") cerrar();
  });

  /* Desplazamiento suave compensando el header fijo (incluye promo bar) */
  document.addEventListener("click", (evento) => {
    const enlace = evento.target instanceof Element ? evento.target.closest('a[href^="#"]') : null;
    if (!enlace) return;
    const destinoId = enlace.getAttribute("href")?.slice(1);
    if (!destinoId) return;
    const destino = document.getElementById(destinoId);
    if (!destino) return;

    evento.preventDefault();
    cerrar();

    const margen = altoHeader() + 14;
    const y = destino.getBoundingClientRect().top + window.scrollY - margen;
    const suave = !window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    window.scrollTo({ top: Math.max(0, y), behavior: suave ? "smooth" : "auto" });
    history.replaceState(null, "", `#${destinoId}`);

    // Mueve el foco para lectores de pantalla sin provocar salto visual
    if (!destino.hasAttribute("tabindex")) destino.setAttribute("tabindex", "-1");
    destino.focus({ preventScroll: true });
  });
}
