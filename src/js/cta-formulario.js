/**
 * Botones de llamada a la acción → formulario.
 *
 * El desplazamiento lo hace el propio navegador con el ancla #cotizacion
 * (el CSS ya define scroll-behavior: smooth y scroll-padding para la barra
 * fija), así funciona igual en móvil, escritorio y con el teclado.
 *
 * Aquí solo se completa la experiencia:
 *   - si el formulario ya se envió, se restablece para mostrar los campos,
 *   - se enfoca el primer campo para que el cliente escriba de inmediato,
 *   - se resalta la tarjeta del formulario.
 */

const SELECTOR_CTA = 'a[href="#cotizacion"]:not([data-wa-form])';
const SELECTOR_SECCION = "#cotizacion";
const SELECTOR_EXITO = "[data-form-success]";
const SELECTOR_REINICIO = "[data-success-reset]";
const SELECTOR_PRIMER_CAMPO = "#campo-nombre";

function prepararFormulario() {
  const seccion = document.querySelector(SELECTOR_SECCION);
  if (!seccion) return;

  // Si se está mostrando el mensaje de éxito, se vuelve al formulario
  const exito = document.querySelector(SELECTOR_EXITO);
  if (exito && !exito.hidden) {
    document.querySelector(SELECTOR_REINICIO)?.click();
  }

  // Resalta la tarjeta
  const tarjeta = seccion.querySelector(".cotiza__card") ?? seccion;
  tarjeta.classList.remove("is-destacada");
  void tarjeta.offsetWidth;
  tarjeta.classList.add("is-destacada");
  window.setTimeout(() => tarjeta.classList.remove("is-destacada"), 1600);

  // Enfoca el primer campo (sin mover otra vez la página)
  const campo = document.querySelector(SELECTOR_PRIMER_CAMPO);
  if (campo && !campo.closest("[hidden]")) {
    campo.focus({ preventScroll: true });
  }
}

export function initCtaFormulario() {
  if (!document.querySelector(SELECTOR_SECCION)) return;

  document.addEventListener("click", (evento) => {
    const enlace = evento.target instanceof Element ? evento.target.closest(SELECTOR_CTA) : null;
    if (!enlace) return;

    // No se cancela el clic: el navegador salta al ancla por sí mismo.
    window.setTimeout(prepararFormulario, 450);
  });

  // Si se llega directo con #cotizacion en la URL
  if (window.location.hash === "#cotizacion") {
    window.setTimeout(prepararFormulario, 500);
  }
}
