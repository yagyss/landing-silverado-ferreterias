/**
 * Formulario express ("Cotiza en un minuto").
 *
 * Sólo pide nombre, WhatsApp y alcaldía; el resto de datos los completa el
 * asesor. Envía al mismo endpoint que el formulario completo y sólo muestra
 * éxito cuando el servidor confirma el registro.
 */

import { SITE } from "../data/site.js";
import { trackLead } from "./analytics.js";
import { escapar, leerUtm } from "./dom.js";
import { formatearTelefono, normalizarTelefono, validarProspecto } from "./validation.mjs";

const MENSAJE_RED_EXPRESS =
  "No pudimos conectar con el servidor. Revisa tu conexión e intenta de nuevo o escríbenos por WhatsApp.";

export function initExpressForm() {
  const form = document.querySelector("[data-form-express]");
  if (!form) return;

  const estado = form.querySelector("[data-express-status]");
  const boton = form.querySelector("[data-express-submit]");
  const exito = document.querySelector("[data-express-exito]");
  const inicio = form.querySelector("[data-express-inicio]");
  const telefono = form.elements.namedItem("whatsapp");
  const comenzado = Date.now();

  if (inicio) inicio.value = String(comenzado);

  // Alcaldías desde la configuración central
  const selectCiudad = form.elements.namedItem("ciudad");
  const ciudades = SITE.formulario.opciones.ciudad ?? [];
  if (selectCiudad && ciudades.length) {
    selectCiudad.innerHTML = [
      '<option value="" selected disabled>Selecciona tu alcaldía</option>',
      ...ciudades.map((valor) => `<option value="${escapar(valor)}">${escapar(valor)}</option>`),
    ].join("");
  }

  telefono?.addEventListener("input", () => {
    const digitos = telefono.value.replace(/\D/g, "").slice(0, 10);
    telefono.value = formatearTelefono(digitos);
    if (digitos.length === 10) limpiar("whatsapp");
  });

  const error = (nombre) => form.querySelector(`[data-error-for="${nombre}"]`);

  function marcar(nombre, mensaje) {
    const nodo = error(nombre);
    if (nodo) {
      nodo.textContent = mensaje;
      nodo.classList.add("is-visible");
    }
    const campo = form.elements.namedItem(nombre);
    if (campo && campo.setAttribute) campo.setAttribute("aria-invalid", "true");
    campo?.closest?.(".express__campo")?.classList.add("has-error");
  }

  function limpiar(nombre) {
    const nodo = error(nombre);
    if (nodo) {
      nodo.textContent = "";
      nodo.classList.remove("is-visible");
    }
    const campo = form.elements.namedItem(nombre);
    if (campo && campo.removeAttribute) campo.removeAttribute("aria-invalid");
    campo?.closest?.(".express__campo")?.classList.remove("has-error");
  }

  function mostrarEstado(mensaje, tipo = "error") {
    if (!estado) return;
    estado.textContent = mensaje;
    estado.classList.toggle("is-visible", Boolean(mensaje));
    estado.dataset.tipo = tipo;
  }

  function recolectar() {
    return {
      nombre: form.elements.namedItem("nombre")?.value ?? "",
      whatsapp: telefono?.value ?? "",
      ciudad: form.elements.namedItem("ciudad")?.value ?? "",
      privacidad: Boolean(form.elements.namedItem("privacidad")?.checked),
      honeypot: form.elements.namedItem("honeypot")?.value ?? "",
      iniciadoEn: comenzado,
      express: true,
    };
  }

  form.addEventListener("submit", async (evento) => {
    evento.preventDefault();
    mostrarEstado("");

    ["nombre", "whatsapp", "ciudad", "privacidad"].forEach(limpiar);
    const { errores, limpio } = validarProspecto(recolectar(), { ahora: Date.now() });

    if (Object.keys(errores).some((clave) => !clave.startsWith("_"))) {
      Object.entries(errores)
        .filter(([clave]) => !clave.startsWith("_"))
        .forEach(([campo, mensaje]) => marcar(campo, mensaje));
      mostrarEstado("Revisa los campos marcados.");
      return;
    }

    const textoOriginal = boton?.innerHTML;
    if (boton) {
      boton.disabled = true;
      boton.setAttribute("aria-busy", "true");
      boton.innerHTML = "<span>Enviando…</span>";
    }

    if (window.location.protocol === "file:") {
      mostrarEstado(
        "Vista de revisión: para enviar la solicitud abre la página con el servidor local (node server.mjs) o conéctala a tu CRM.",
        "error",
      );
      return;
    }

    try {
      const respuesta = await fetch(SITE.formulario.endpoint, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          nombre: limpio.nombre,
          whatsapp: normalizarTelefono(limpio.whatsapp),
          ciudad: limpio.ciudad,
          privacidad: true,
          honeypot: limpio.honeypot,
          iniciadoEn: comenzado,
          express: true,
          pagina: window.location.href,
          referrer: document.referrer,
          origen: leerUtm(),
        }),
      });

      let cuerpo = {};
      try {
        cuerpo = await respuesta.json();
      } catch {
        cuerpo = {};
      }

      if (respuesta.status === 422) {
        Object.entries(cuerpo.errores ?? {}).forEach(([campo, mensaje]) => marcar(campo, mensaje));
        mostrarEstado(cuerpo.mensaje ?? "Revisa los campos marcados.");
        return;
      }

      if (!respuesta.ok || cuerpo.ok !== true) {
        mostrarEstado(cuerpo.mensaje ?? MENSAJE_RED_EXPRESS);
        return;
      }

      // Éxito confirmado por el servidor
      if (exito) {
        form.hidden = true;
        exito.hidden = false;
        const folio = cuerpo.folio ?? "";
        exito.querySelector("[data-express-mensaje]").textContent =
          cuerpo.duplicado === true
            ? SITE.formulario.mensajes.duplicado
            : SITE.formulario.mensajes.exitoCuerpo.replace("{folio}", folio);
        const folioWrap = exito.querySelector("[data-express-folio-wrap]");
        if (folioWrap) {
          folioWrap.hidden = !folio;
          exito.querySelector("[data-express-folio]").textContent = folio;
        }
        exito.scrollIntoView({ behavior: "smooth", block: "center" });
      }

      trackLead({ folio: cuerpo.folio ?? "", express: true, ciudad: limpio.ciudad });
    } catch (fallo) {
      console.error("[express]", fallo);
      mostrarEstado(MENSAJE_RED_EXPRESS);
    } finally {
      if (boton) {
        boton.disabled = false;
        boton.removeAttribute("aria-busy");
        if (textoOriginal) boton.innerHTML = textoOriginal;
      }
    }
  });
}
