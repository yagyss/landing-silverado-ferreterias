/**
 * Registro de prospectos (lead) · Chevrolet Silverado para ferreterías.
 *
 * Este handler es intencionalmente agnóstico del hosting: lo usa el servidor
 * local (server.mjs) y puede publicarse tal cual como función serverless.
 *
 * Además de validar y deduplicar, DEJA RASTRO REAL del prospecto:
 *   · almacenamiento local  -> data/prospectos.jsonl (una línea JSON por lead)
 *   · webhook / CRM         -> reenvío opcional configurado en site.js
 *
 * Nunca responde "éxito" si no se pudo registrar la solicitud.
 */

import { appendFile, mkdir, readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";

import { SITE } from "../src/data/site.js";
import { validarProspecto } from "../src/js/validation.mjs";

const RAIZ = resolve(import.meta.dirname, "..");
const RUTA_ARCHIVO = resolve(RAIZ, SITE.leads.archivo);
const LIMITE_PETICIONES = { max: 6, ventanaMs: 10 * 60 * 1000 };

/** Ventana de rate-limit en memoria (suficiente para un servidor único). */
const peticiones = new Map();

function limitarPorIp(ip) {
  const ahora = Date.now();
  const registro = peticiones.get(ip) ?? { inicio: ahora, cuenta: 0 };
  if (ahora - registro.inicio > LIMITE_PETICIONES.ventanaMs) {
    registro.inicio = ahora;
    registro.cuenta = 0;
  }
  registro.cuenta += 1;
  peticiones.set(ip, registro);
  if (peticiones.size > 5000) peticiones.clear();
  return registro.cuenta <= LIMITE_PETICIONES.max;
}

function generarFolio() {
  const fecha = new Date().toISOString().slice(0, 10).replaceAll("-", "");
  const azar = Math.random().toString(36).slice(2, 6).toUpperCase();
  return `SV-${fecha}-${azar}`;
}

async function leerRegistros() {
  try {
    const contenido = await readFile(RUTA_ARCHIVO, "utf8");
    return contenido
      .split("\n")
      .filter(Boolean)
      .slice(-400)
      .map((linea) => {
        try {
          return JSON.parse(linea);
        } catch {
          return null;
        }
      })
      .filter(Boolean);
  } catch {
    return [];
  }
}

function buscarDuplicado(registros, telefono) {
  const ventana = SITE.leads.dedupeMinutos * 60 * 1000;
  const ahora = Date.now();
  return registros.find(
    (r) =>
      r?.datos?.whatsapp === telefono &&
      ahora - new Date(r.fecha).getTime() < ventana
  );
}

function recortar(valor, max = 300) {
  return String(valor ?? "").slice(0, max);
}

function construirRegistro(limpio, contexto) {
  const { utm = {}, referrer = "", userAgent = "", pagina = "" } = contexto;
  return {
    folio: generarFolio(),
    fecha: new Date().toISOString(),
    campana: SITE.campana.id,
    canal: SITE.campana.canal,
    pagina,
    origen: {
      utm_source: recortar(utm.utm_source, 80),
      utm_medium: recortar(utm.utm_medium, 80),
      utm_campaign: recortar(utm.utm_campaign, 120),
      utm_content: recortar(utm.utm_content, 120),
      utm_term: recortar(utm.utm_term, 120),
      fbclid: recortar(utm.fbclid, 200),
      referrer: recortar(referrer, 300),
    },
    datos: {
      nombre: limpio.nombre,
      whatsapp: limpio.whatsapp,
      correo: limpio.correo,
      ciudad: limpio.ciudad,
      ferreteria: limpio.ferreteria,
      plan: limpio.plan,
      mensaje: limpio.mensaje,
      // Campos heredados (pueden venir vacíos)
      sucursales: limpio.sucursales,
      usoVehiculo: limpio.usoVehiculo,
      interes: limpio.interes,
      aceptoPrivacidad: limpio.privacidad,
    },
    tecnico: {
      userAgent: recortar(userAgent, 220),
      idioma: "es-MX",
    },
    seguimiento: { estado: "nuevo", eventoMeta: "Lead" },
  };
}

async function guardarLocal(registro) {
  await mkdir(dirname(RUTA_ARCHIVO), { recursive: true });
  await appendFile(RUTA_ARCHIVO, `${JSON.stringify(registro)}\n`, "utf8");
}

async function enviarWebhook(registro) {
  const url = SITE.leads.webhookUrl;
  if (!url) return { enviado: false, motivo: "sin-webhook" };
  try {
    const controlador = new AbortController();
    const t = setTimeout(() => controlador.abort(), 6000);
    const respuesta = await fetch(url, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(registro),
      signal: controlador.signal,
    });
    clearTimeout(t);
    return { enviado: respuesta.ok, motivo: respuesta.ok ? "ok" : `http-${respuesta.status}` };
  } catch (error) {
    return { enviado: false, motivo: `error:${error?.name ?? "desconocido"}` };
  }
}

/**
 * @param {{ body: unknown, ip?: string, userAgent?: string, referrer?: string, pagina?: string }} peticion
 */
export async function procesarProspecto(peticion) {
  const cuerpo = peticion.body ?? {};
  const ahora = Date.now();

  if (!limitarPorIp(peticion.ip ?? "local")) {
    return {
      status: 429,
      body: {
        ok: false,
        codigo: "demasiadas_peticiones",
        mensaje: "Recibimos varias solicitudes seguidas. Espera unos minutos o escríbenos por WhatsApp.",
      },
    };
  }

  if (!SITE.oferta.activa) {
    // La captación sigue habilitada, sólo se informa que la promoción no está vigente.
  }

  const { valido, errores, limpio } = validarProspecto(cuerpo, { ahora });
  if (!valido) {
    return {
      status: 422,
      body: {
        ok: false,
        codigo: errores._spam ? "rechazado" : "validacion",
        errores: Object.fromEntries(Object.entries(errores).filter(([k]) => !k.startsWith("_"))),
        mensaje: errores._spam
          ? "No pudimos procesar la solicitud. Intenta de nuevo."
          : "Revisa los campos señalados.",
      },
    };
  }

  const registros = await leerRegistros();
  const duplicado = buscarDuplicado(registros, limpio.whatsapp);
  if (duplicado) {
    return {
      status: 200,
      body: {
        ok: true,
        duplicado: true,
        folio: duplicado.folio,
        mensaje: SITE.formulario.mensajes.duplicado,
      },
    };
  }

  const registro = construirRegistro(limpio, {
    utm: peticion.utm,
    referrer: peticion.referrer,
    userAgent: peticion.userAgent,
    pagina: peticion.pagina,
  });

  try {
    await guardarLocal(registro);
  } catch (error) {
    console.error("[lead] no se pudo guardar el prospecto:", error);
    return {
      status: 500,
      body: {
        ok: false,
        codigo: "almacenamiento",
        mensaje:
          "No pudimos registrar tu solicitud. Intenta de nuevo o escríbenos por WhatsApp; tus datos no se perdieron.",
      },
    };
  }

  const webhook = await enviarWebhook(registro);
  if (SITE.leads.webhookUrl && !webhook.enviado) {
    console.warn(`[lead] webhook no confirmado (${webhook.motivo}) para folio ${registro.folio}`);
  }

  console.log(`[lead] prospecto registrado ${registro.folio} · ${registro.datos.ciudad} · ${registro.datos.sucursales}`);

  return {
    status: 201,
    body: {
      ok: true,
      duplicado: false,
      folio: registro.folio,
      integracion: webhook.enviado ? "webhook-confirmado" : SITE.leads.webhookUrl ? "webhook-pendiente" : "solo-local",
      mensaje: SITE.formulario.mensajes.exitoCuerpo.replace("{folio}", registro.folio),
    },
  };
}

/** Adaptador estilo serverless (Vercel / Netlify Functions). */
export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.statusCode = 405;
    res.setHeader("allow", "POST");
    res.end(JSON.stringify({ ok: false, mensaje: "Método no permitido" }));
    return;
  }
  const resultado = await procesarProspecto({
    body: req.body,
    ip: req.headers["x-forwarded-for"] ?? "remoto",
    userAgent: req.headers["user-agent"],
    referrer: req.headers.referer,
  });
  res.statusCode = resultado.status;
  res.setHeader("content-type", "application/json; charset=utf-8");
  res.end(JSON.stringify(resultado.body));
}

