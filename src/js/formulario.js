/**
 * Formulario de cotización · esquema simplificado
 * nombre · celular · correo · plan · mensaje
 */

import { SITE } from "../data/site.js";
import { trackLead } from "./analytics.js";
import { escapar, leerUtm } from "./dom.js";
import { formatearTelefono, normalizarTelefono, validarProspecto } from "./validation.mjs";

const MENSAJE_RED =
  "No pudimos conectar con el servidor. Revisa tu conexión e intenta de nuevo o escríbenos por WhatsApp.";

const CAMPOS = ["nombre", "whatsapp", "correo", "plan", "privacidad"];

export function initFormulario() {
  const form = document.querySelector("[data-form-cotizacion]");
  if (!form) return;

  const estado = form.querySelector("[data-form-status]");
  const boton = form.querySelector("[data-form-submit]");
  const exito = document.querySelector("[data-form-success]");
  const inicio = form.querySelector("[data-form-inicio]");
  const telefono = form.elements.namedItem("whatsapp");
  const comenzado = Date.now();

  if (inicio) inicio.value = String(comenzado);

  // Planes desde la configuración central
  const selectPlan = form.elements.namedItem("plan");
  const planes = SITE.formulario.opciones.plan ?? [];
  if (selectPlan && planes.length) {
    selectPlan.innerHTML = [
      '<option value="" selected disabled>Selecciona una opción</option>',
      ...planes.map((valor) => `<option value="${escapar(valor)}">${escapar(valor)}</option>`),
    ].join("");
  }

  telefono?.addEventListener("input", () => {
    const digitos = telefono.value.replace(/\D/g, "").slice(0, 10);
    telefono.value = formatearTelefono(digitos);
    if (digitos.length === 10) limpiar("whatsapp");
  });

  const nodoError = (nombre) => form.querySelector(`[data-error-for="${nombre}"]`);

  function marcar(nombre, mensaje) {
    const nodo = nodoError(nombre);
    if (nodo) {
      nodo.textContent = mensaje;
      nodo.classList.add("is-visible");
    }
    const campo = form.elements.namedItem(nombre);
    if (campo && campo.setAttribute) campo.setAttribute("aria-invalid", "true");
    campo?.closest?.(".form__field")?.classList.add("has-error");
  }

  function limpiar(nombre) {
    const nodo = nodoError(nombre);
    if (nodo) {
      nodo.textContent = "";
      nodo.classList.remove("is-visible");
    }
    const campo = form.elements.namedItem(nombre);
    if (campo && campo.removeAttribute) campo.removeAttribute("aria-invalid");
    campo?.closest?.(".form__field")?.classList.remove("has-error");
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
      correo: form.elements.namedItem("correo")?.value ?? "",
      plan: form.elements.namedItem("plan")?.value ?? "",
      mensaje: form.elements.namedItem("mensaje")?.value ?? "",
      privacidad: Boolean(form.elements.namedItem("privacidad")?.checked),
      honeypot: form.elements.namedItem("honeypot")?.value ?? "",
      iniciadoEn: comenzado,
    };
  }

  form.addEventListener("submit", async (evento) => {
    evento.preventDefault();
    mostrarEstado("");
    CAMPOS.forEach(limpiar);

    const { errores, limpio } = validarProspecto(recolectar(), { ahora: Date.now() });
    const campos = Object.keys(errores).filter((clave) => !clave.startsWith("_"));

    if (campos.length) {
      campos.forEach((campo) => marcar(campo, errores[campo]));
      const primero = form.elements.namedItem(campos[0]);
      primero?.focus?.({ preventScroll: true });
      primero?.scrollIntoView?.({ behavior: "smooth", block: "center" });
      mostrarEstado("Revisa los campos marcados.");
      return;
    }

    const textoOriginal = boton?.innerHTML;
    if (boton) {
      boton.disabled = true;
      boton.setAttribute("aria-busy", "true");
      boton.innerHTML = "<span>Enviando…</span>";
    }

    try {
      // Abierto como archivo se envía directo al Apps Script (sin proxy).
      const esArchivo = window.location.protocol === "file:";
      const destino =
        esArchivo && SITE.formulario.endpointRemoto
          ? SITE.formulario.endpointRemoto
          : SITE.formulario.endpoint;

      const respuesta = await fetch(destino, {
        method: "POST",
        // Con file:// el navegador no permite leer la respuesta (CORS),
        // así que se usa una petición simple y se informa con honestidad.
        mode: esArchivo ? "no-cors" : "cors",
        headers: {
          "content-type": esArchivo ? "text/plain;charset=utf-8" : "application/json",
        },
        body: JSON.stringify({
          nombre: limpio.nombre,
          whatsapp: normalizarTelefono(limpio.whatsapp),
          correo: limpio.correo,
          plan: limpio.plan,
          mensaje: limpio.mensaje,
          privacidad: true,
          honeypot: limpio.honeypot,
          iniciadoEn: comenzado,
          pagina: window.location.href,
          referrer: document.referrer,
          origen: leerUtm(),
        }),
      });

      let cuerpo = {};
      if (respuesta.type !== "opaque") {
        try {
          cuerpo = await respuesta.json();
        } catch {
          cuerpo = {};
        }
      }

      // Envío desde archivo: la petición salió, pero el navegador no puede
      // leer la respuesta. Se confirma sólo lo que sí sabemos.
      if (respuesta.type === "opaque") {
        if (exito) {
          exito.hidden = false;
          exito.querySelector("[data-success-titulo]").textContent = "Solicitud enviada";
          exito.querySelector("[data-success-mensaje]").textContent =
            "Enviamos tu solicitud. Un asesor te contactará. " +
            "Si no recibes la confirmación por correo en unos minutos, escríbenos por WhatsApp.";
          exito.querySelector("[data-success-folio-wrap]").hidden = true;
          form.hidden = true;
          exito.scrollIntoView({ behavior: "smooth", block: "center" });
        }
        trackLead({ folio: "", modo: "archivo-local" });
        return;
      }

      if (respuesta.status === 422) {
        Object.entries(cuerpo.errores ?? {}).forEach(([campo, mensaje]) => marcar(campo, mensaje));
        mostrarEstado(cuerpo.mensaje ?? "Revisa los campos marcados.");
        return;
      }

      if (respuesta.status === 429) {
        mostrarEstado(cuerpo.mensaje ?? "Demasiadas solicitudes. Espera unos minutos.");
        return;
      }

      // Algunos despliegues de Apps Script responden {result:"success"} en
      // lugar de {ok:true, folio}. Se aceptan ambos formatos para no bloquear
      // el registro en la hoja.
      const exitoConfirmado =
        respuesta.ok &&
        (cuerpo.ok === true || cuerpo.success === true || cuerpo.result === "success");

      if (!exitoConfirmado) {
        mostrarEstado(cuerpo.mensaje ?? MENSAJE_RED);
        return;
      }

      const folio = cuerpo.folio ?? "";
      if (exito) {
        exito.hidden = false;
        exito.querySelector("[data-success-titulo]").textContent = SITE.formulario.mensajes.exitoTitulo;
        exito.querySelector("[data-success-mensaje]").textContent =
          cuerpo.duplicado === true
            ? SITE.formulario.mensajes.duplicado
            : SITE.formulario.mensajes.exitoCuerpo.replace("{folio}", folio);
        exito.querySelector("[data-success-folio]").textContent = folio;
        exito.querySelector("[data-success-folio-wrap]").hidden = !folio;
        form.hidden = true;
        exito.scrollIntoView({ behavior: "smooth", block: "center" });
        exito.querySelector("[data-success-reset]")?.focus({ preventScroll: true });
      }

      trackLead({ folio, plan: limpio.plan, duplicado: cuerpo.duplicado === true });
    } catch (fallo) {
      console.error("[formulario]", fallo);
      mostrarEstado(MENSAJE_RED);
    } finally {
      if (boton) {
        boton.disabled = false;
        boton.removeAttribute("aria-busy");
        if (textoOriginal) boton.innerHTML = textoOriginal;
      }
    }
  });

  document.querySelector("[data-success-reset]")?.addEventListener("click", () => {
    form.reset();
    CAMPOS.forEach(limpiar);
    mostrarEstado("");
    if (exito) exito.hidden = true;
    form.hidden = false;
    form.elements.namedItem("nombre")?.focus();
    form.scrollIntoView({ behavior: "smooth", block: "center" });
  });
}
