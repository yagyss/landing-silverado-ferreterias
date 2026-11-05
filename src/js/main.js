/**
 * Punto de entrada del cliente.
 *
 * Cada subsistema se inicializa de forma aislada: si uno falla, el resto de la
 * página sigue funcionando. El orden importa:
 *   1. datos/config y chrome global
 *   2. secciones dinámicas (antes de los reveals, para que sus nodos nuevos
 *      queden observados por el IntersectionObserver)
 *   3. navegación, movimiento y formulario
 */

import { initAnalitica } from "./analytics.js";
import { initExpressForm } from "./express.js";
import { initFormulario } from "./formulario.js";
import { initLocalNav } from "./localnav.js";
import { initActiveNav, initParallax, initReveals, initScrollUI } from "./motion.js";
import { initNavegacion } from "./nav.js";
import { initSeccionesB } from "./secciones-b.js";
import { initShowcase } from "./showcase.js";
import {
  initAviso,
  initEspecificaciones,
  initFooter,
  initMarca,
  initNotaPrivacidadForm,
  initPromo,
  initWhatsApp,
} from "./ui.js";

/** Ejecuta un inicializador capturando errores para no tumbar la página. */
function seguro(nombre, fn) {
  try {
    fn();
  } catch (error) {
    console.error(`[app] ${nombre} no pudo inicializarse:`, error);
  }
}

function iniciar() {
  const pasos = [
    ["analitica", initAnalitica],
    ["promo", initPromo],
    ["marca", initMarca],
    ["footer", initFooter],
    ["aviso", initAviso],
    ["whatsapp", initWhatsApp],
    ["nota-privacidad", initNotaPrivacidadForm],
    ["especificaciones", initEspecificaciones],
    ["secciones-b", initSeccionesB],
    ["navegacion", initNavegacion],
    ["localnav", initLocalNav],
    ["parallax", initParallax],
    ["reveals", initReveals],
    ["scroll-ui", initScrollUI],
    ["nav-activo", initActiveNav],
    ["showcase", initShowcase],
    ["formulario", initFormulario],
    ["formulario-express", initExpressForm],
  ];

  pasos.forEach(([nombre, fn]) => seguro(nombre, fn));

  document.documentElement.classList.add("app-lista");
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", iniciar, { once: true });
} else {
  iniciar();
}
