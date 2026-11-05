/**
 * Hidratación de los elementos globales del layout con datos de la config:
 * barra de promoción, logo de marca, pie de página, aviso de privacidad,
 * botón de WhatsApp y ficha técnica.
 */

import { SITE } from "../data/site.js";
import { escapar } from "./dom.js";

/* ---------------------------------------------- Barra de promoción superior */
export function initPromo() {
  const barra = document.querySelector("[data-promo-bar]");
  if (!barra) return;

  const { oferta } = SITE;
  if (!oferta?.activa || !oferta.beneficios?.length) return;

  const partes = oferta.beneficios
    .map((beneficio) => `<span class="promo-bar__accent">${escapar(beneficio.etiqueta)}</span> ${escapar(beneficio.titulo)}`)
    .join('<span class="promo-bar__dot" aria-hidden="true"></span>');

  barra.innerHTML = `<span class="promo-bar__dot" aria-hidden="true"></span>${partes}<span class="promo-bar__dot" aria-hidden="true"></span>`;
  barra.classList.add("is-visible");
  barra.removeAttribute("aria-label");
  document.documentElement.style.setProperty("--promo-h", "38px");
}

/* --------------------------------------------------------- Logo de la marca
   El logotipo oficial se intenta cargar en este orden:
   1) archivo local (assets/marca/bowtie.svg)
   2) archivo oficial en el CDN del fabricante
   3) respaldo tipográfico "CHEVROLET" (siempre visible, sin iconos roTOS) */
export function initMarca() {
  const contenedor = document.querySelector("[data-brand-mark]");
  if (!contenedor) return;

  const respaldo = contenedor.querySelector("[data-brand-wordmark]");
  const { logo } = SITE.marca;
  const candidatos = [logo?.local, logo?.remoto].filter(Boolean);
  if (!candidatos.length) return;

  const probar = (indice) => {
    if (indice >= candidatos.length) return;
    const imagen = new Image();
    imagen.decoding = "async";
    imagen.alt = logo.alt ?? "Chevrolet";
    imagen.className = "brand__logo";
    imagen.onload = () => {
      if (respaldo) respaldo.remove();
      contenedor.replaceChildren(imagen);
    };
    imagen.onerror = () => probar(indice + 1);
    imagen.src = candidatos[indice];
  };

  probar(0);
}

/* ------------------------------------------------------------ Pie de página */
export function initFooter() {
  const { contacto, legales } = SITE;

  const rellenar = (selector, valor, etiqueta) => {
    const nodo = document.querySelector(selector);
    if (!nodo || !valor) return;
    nodo.innerHTML = etiqueta ? `<span class="site-footer__label">${escapar(etiqueta)}</span> ${escapar(valor)}` : escapar(valor);
    nodo.hidden = false;
  };

  rellenar("[data-footer-distribuidor]", contacto.distribuidor, "Distribuidor:");
  rellenar("[data-footer-horario]", contacto.horario, "Horario:");
  rellenar("[data-footer-telefono]", contacto.telefono, "Teléfono:");
  rellenar("[data-footer-correo]", contacto.correo, "Correo:");

  const disclaimer = document.querySelector("[data-footer-disclaimer]");
  if (disclaimer) disclaimer.textContent = legales.disclaimerGeneral;

  const copyright = document.querySelector("[data-footer-copyright]");
  if (copyright) {
    copyright.textContent = `© ${new Date().getFullYear()} Página de campaña para ${SITE.marca.nombre} ${SITE.marca.modelo}. Uso informativo y comercial.`;
  }
}

/* --------------------------------------------------- Aviso de privacidad */
export function initAviso() {
  const dialogo = document.getElementById("aviso-privacidad");
  if (!dialogo) return;

  const abrir = () => {
    if (typeof dialogo.showModal === "function") dialogo.showModal();
    else dialogo.setAttribute("open", "");
  };

  document.querySelectorAll("[data-open-privacidad]").forEach((disparador) => {
    disparador.addEventListener("click", (evento) => {
      evento.preventDefault();
      abrir();
    });
  });

  document.querySelectorAll("[data-close-privacidad]").forEach((boton) => {
    boton.addEventListener("click", () => {
      if (typeof dialogo.close === "function") dialogo.close();
      else dialogo.removeAttribute("open");
    });
  });

  // Cierre al hacer clic en el fondo del diálogo
  dialogo.addEventListener("click", (evento) => {
    if (evento.target === dialogo) dialogo.close();
  });

  const titulo = document.querySelector("[data-aviso-titulo]");
  const texto = document.querySelector("[data-aviso-texto]");
  const nota = document.querySelector("[data-aviso-nota]");
  if (titulo) titulo.textContent = SITE.legales.avisoPrivacidadTitulo;
  if (texto) texto.textContent = SITE.formulario.privacidad.textoAviso;
  if (nota) nota.textContent = SITE.legales.notaPrivacidad;
}

/* ------------------------------------------------------- WhatsApp y contacto */
export function initWhatsApp() {
  const { whatsapp, desarrollo } = SITE;
  if (!whatsapp?.activo) {
    document.querySelectorAll("[data-wa-float]").forEach((nodo) => nodo.remove());
    return;
  }

  const numero = String(whatsapp.numero ?? "").replace(/\D/g, "");
  const configurado = numero.length >= 10;
  const url = configurado
    ? `https://wa.me/${numero}?text=${encodeURIComponent(whatsapp.mensaje)}`
    : "";

  document.querySelectorAll("[data-wa-float], [data-wa-form]").forEach((nodo) => {
    if (configurado) {
      nodo.setAttribute("href", url);
      nodo.setAttribute("target", "_blank");
      nodo.setAttribute("rel", "noopener");

      // Respaldo: si el marcado usara un <button>, igual abre WhatsApp.
      if (nodo.tagName === "BUTTON") {
        nodo.addEventListener("click", (evento) => {
          evento.preventDefault();
          window.open(url, "_blank", "noopener");
        });
      }
      return;
    }
    nodo.classList.add("is-sin-configurar");
    nodo.addEventListener("click", (evento) => {
      evento.preventDefault();
      document.getElementById("cotizacion")?.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });

  if (!configurado && desarrollo?.mostrarMarcadores) {
    const insignia = document.querySelector("[data-wa-badge]");
    if (insignia) insignia.hidden = false;
  }

  const etiqueta = document.querySelector(".wa-float__label");
  if (etiqueta && whatsapp.etiqueta) etiqueta.textContent = whatsapp.etiqueta;
}

/* ------------------------------------------------------------- Ficha técnica */
export function initEspecificaciones() {
  const contenedores = document.querySelectorAll("[data-specs-silverado]");
  if (!contenedores.length) return;

  const { especificaciones } = SITE;
  const etiquetaEstado = especificaciones.verificado
    ? ""
    : '<span class="spec__estado">Referencia oficial por confirmar</span>';

  const html = especificaciones.items
    .map(
      (item) => `<div class="spec">
        <dt class="spec__label">${escapar(item.etiqueta)}</dt>
        <dd class="spec__value">
          <strong>${escapar(item.valor)}</strong>
          ${etiquetaEstado}
          ${item.nota ? `<span class="spec__nota">${escapar(item.nota)}</span>` : ""}
        </dd>
      </div>`
    )
    .join("");

  contenedores.forEach((contenedor) => {
    contenedor.innerHTML = html;
    contenedor.classList.add("is-hidratado");
  });
}

/* ----------------------------------------------- Nota de privacidad del form */
export function initNotaPrivacidadForm() {
  const nota = document.querySelector("[data-form-privacidad-nota]");
  if (nota) nota.textContent = SITE.legales.notaPrivacidad;
}
