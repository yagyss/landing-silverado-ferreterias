/**
 * Barra de producto (localnav) al estilo de la referencia: aparece al salir
 * del hero y da acceso permanente a la cotización.
 */

export function initLocalNav() {
  const barra = document.querySelector("[data-localnav]");
  if (!barra) return;

  let anterior = false;

  const actualizar = () => {
    const visible = window.scrollY > window.innerHeight * 0.55;
    if (visible === anterior) return;
    anterior = visible;
    barra.classList.toggle("is-visible", visible);
    barra.setAttribute("aria-hidden", String(!visible));
  };

  window.addEventListener("scroll", actualizar, { passive: true });
  window.addEventListener("resize", actualizar);
  actualizar();
}
