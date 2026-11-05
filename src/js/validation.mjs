/**
 * Validación compartida entre el navegador y el servidor.
 *
 * Esquema vigente de la landing:
 *   nombre    · obligatorio
 *   whatsapp  · celular a 10 dígitos (obligatorio)
 *   correo    · obligatorio y con formato
 *   plan      · obligatorio, de la lista de la configuración
 *   mensaje   · opcional (máx. 600 caracteres)
 *   privacidad· obligatorio
 *
 * Se conservan los campos anteriores como opcionales para no romper
 * integraciones existentes (CRM, hojas ya creadas).
 */

import { SITE } from "../data/site.js";

const RE_CORREO = /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i;

export function normalizarTelefono(valor) {
  const digitos = String(valor ?? "").replace(/\D/g, "");
  if (digitos.length === 12 && digitos.startsWith("52")) return digitos.slice(2);
  if (digitos.length === 13 && digitos.startsWith("521")) return digitos.slice(3);
  return digitos;
}

export function formatearTelefono(valor) {
  const d = normalizarTelefono(valor);
  if (d.length !== 10) return d;
  return `${d.slice(0, 2)} ${d.slice(2, 6)} ${d.slice(6)}`;
}

function limpiarTexto(valor, max = 180) {
  return String(valor ?? "")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, max);
}

const enLista = (valor, lista) => (lista ?? []).includes(valor);

/**
 * @param {object} datos
 * @param {{ ahora?: number, trampaTiempoMs?: number }} [opciones]
 * @returns {{ valido: boolean, errores: Record<string,string>, limpio: object }}
 */
export function validarProspecto(datos = {}, opciones = {}) {
  const { ahora = Date.now(), trampaTiempoMs = 2500 } = opciones;
  const express = Boolean(datos.express);
  const op = SITE.formulario.opciones;
  const errores = {};

  const limpio = {
    nombre: limpiarTexto(datos.nombre, 90),
    whatsapp: normalizarTelefono(datos.whatsapp),
    correo: limpiarTexto(datos.correo, 120).toLowerCase(),
    plan: limpiarTexto(datos.plan, 40),
    mensaje: limpiarTexto(datos.mensaje, 600),
    // Campos heredados (opcionales)
    ciudad: limpiarTexto(datos.ciudad, 60),
    ferreteria: limpiarTexto(datos.ferreteria, 90),
    sucursales: limpiarTexto(datos.sucursales, 40),
    usoVehiculo: limpiarTexto(datos.usoVehiculo, 60),
    interes: limpiarTexto(datos.interes, 60),
    privacidad: Boolean(datos.privacidad),
    honeypot: limpiarTexto(datos.honeypot, 80),
    iniciadoEn: Number(datos.iniciadoEn) || 0,
  };

  if (limpio.nombre.length < 3) {
    errores.nombre = "Escribe tu nombre completo.";
  } else if (!/^[\p{L}\s.'´-]+$/u.test(limpio.nombre)) {
    errores.nombre = "El nombre solo puede contener letras y espacios.";
  }

  if (limpio.whatsapp.length !== 10) {
    errores.whatsapp = "Escribe un celular a 10 dígitos.";
  } else if (!/^[1-9]/.test(limpio.whatsapp)) {
    errores.whatsapp = "Revisa el número: no puede iniciar con 0.";
  }

  if (!limpio.correo) {
    errores.correo = "Escribe tu correo electrónico.";
  } else if (!RE_CORREO.test(limpio.correo)) {
    errores.correo = "Revisa el formato del correo.";
  }

  if (!express) {
    if (!limpio.plan) {
      errores.plan = "Selecciona un plan de compra.";
    } else if (!enLista(limpio.plan, op.plan)) {
      errores.plan = "Selecciona una opción de la lista.";
    }

    if (!limpio.privacidad) {
      errores.privacidad = "Para continuar debes aceptar el aviso de privacidad.";
    }
  } else if (!limpio.privacidad) {
    errores.privacidad = "Para continuar debes aceptar el aviso de privacidad.";
  }

  // Anti-spam
  if (limpio.honeypot) errores._spam = "spam";
  if (limpio.iniciadoEn && ahora - limpio.iniciadoEn < trampaTiempoMs) {
    errores._spam = "spam";
  }

  return { valido: Object.keys(errores).length === 0, errores, limpio };
}

export const CAMPOS_REQUERIDOS = ["nombre", "whatsapp", "correo", "plan", "privacidad"];
