/**
 * Google Apps Script · Landing Silverado → tu hoja + correos
 * ============================================================
 *  Se adapta a los encabezados que YA tiene tu hoja:
 *    nombre · telefono · email · plan · mensaje
 *  y agrega automáticamente las columnas que faltan:
 *    fecha · fuente · estado · asesor · notas · folio · campana
 *
 *  QUÉ HACE
 *   1. Recibe el formulario de la landing (POST JSON).
 *   2. Valida y deduplica por celular.
 *   3. Escribe el lead en TU hoja (usa la primera pestaña).
 *   4. Envía correo de confirmación al prospecto.
 *   5. Envía aviso al administrador con todos los datos.
 *
 *  INSTALACIÓN
 *   1. En tu hoja: Extensiones → Apps Script.
 *   2. Borra todo y pega este archivo.
 *   3. Ajusta CONFIG.ADMIN_EMAIL.
 *   4. Ejecuta la función `instalar` una vez (crea columnas y manda pruebas).
 *   5. Implementar → Administrar implementaciones → lápiz (Editar)
 *        · Versión: Nueva versión
 *        · Ejecutar como: Yo · Acceso: Cualquier persona
 *      (la URL /exec no cambia)
 */

const CONFIG = {
  ADMIN_EMAIL: "ventas@tudominio.mx",
  REMITENTE_NOMBRE: "Chevrolet Silverado · Ferreterías CDMX",
  /** Copia opcional: segundo correo que recibe los avisos (déjalo vacío si no). */
  COPIA_EMAIL: "",
  /** Si es true, el correo al prospecto llega también (CCO) al administrador.
   *  Sirve para verificar que el mensaje al lead realmente se envió. */
  COPIA_OCULTA_LEAD: true,
  /** El aviso interno se envía solo en texto plano: Gmail lo marca menos
   *  como spam que un correo HTML con botones y enlaces. */
  ADMIN_SIN_HTML: true,
  RESPONDER_A: "ventas@tudominio.mx",

  DISTRIBUIDOR: "Distribuidor autorizado Chevrolet",
  TELEFONO: "+52 55 0000 0000",
  WHATSAPP: "5215500000000",
  HORARIO: "Lunes a sábado, 9:00 a 19:00 h",

  ENVIAR_CORREO_LEAD: true,
  ENVIAR_CORREO_ADMIN: true,

  MINUTOS_DEDUPE: 30,
};

/** Columnas que el script garantiza, en este orden, al final de la fila. */
const COLUMNAS_PROPIAS = ["fecha", "fuente", "estado", "asesor", "notas", "folio", "campana"];

/** Equivalencias aceptadas para cada dato. */
const ALIAS = {
  nombre: ["nombre", "name", "nombre completo"],
  telefono: ["telefono", "teléfono", "celular", "whatsapp", "tel"],
  email: ["email", "correo", "correo electronico", "correo electrónico", "e-mail"],
  plan: ["plan", "plan de compra"],
  mensaje: ["mensaje", "message", "comentario", "comentarios"],
  fecha: ["fecha", "date", "timestamp"],
  fuente: ["fuente", "source", "origen", "landing"],
  estado: ["estado", "status"],
  asesor: ["asesor", "vendedor"],
  notas: ["notas", "nota", "observaciones"],
  folio: ["folio", "id"],
  campana: ["campana", "campaña", "campaign"],
};

/* ============================================================ utilidades */

function libro_() {
  return SpreadsheetApp.getActiveSpreadsheet();
}

function hoja_() {
  const libro = libro_();
  return libro.getSheets()[0];
}

function normalizar_(texto) {
  return String(texto == null ? "" : texto)
    .trim()
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
}

function leerMapa_(hoja) {
  const ancho = Math.max(hoja.getLastColumn(), 1);
  const fila = hoja.getRange(1, 1, 1, ancho).getValues()[0];
  const mapa = {};
  fila.forEach((valor, indice) => {
    const clave = normalizar_(valor);
    if (!clave) return;
    Object.keys(ALIAS).forEach((campo) => {
      if (ALIAS[campo].some((alias) => normalizar_(alias) === clave)) {
        mapa[campo] = indice + 1; // 1-based
      }
    });
  });
  return { mapa, ancho, fila };
}

function asegurarColumnas_(hoja) {
  let { mapa, ancho } = leerMapa_(hoja);

  // Si la hoja está vacía, crea los encabezados base
  if (hoja.getLastRow() === 0) {
    const base = ["nombre", "telefono", "email", "plan", "mensaje", ...COLUMNAS_PROPIAS];
    hoja.getRange(1, 1, 1, base.length).setValues([base]).setFontWeight("bold");
    hoja.setFrozenRows(1);
    ({ mapa, ancho } = leerMapa_(hoja));
  }

  // Agrega las columnas que falten
  const faltantes = COLUMNAS_PROPIAS.filter((columna) => !mapa[columna] && !mapa[columna === "campana" ? "campana" : columna]);
  faltantes.forEach((columna) => {
    ancho += 1;
    hoja.getRange(1, ancho).setValue(columna).setFontWeight("bold");
  });

  if (faltantes.length) {
    hoja.setFrozenRows(1);
    mapa = leerMapa_(hoja).mapa;
  }

  hoja.setColumnWidth(1, 170);
  hoja.setColumnWidth(2, 120);
  hoja.setColumnWidth(3, 200);
  hoja.setColumnWidth(4, 150);
  hoja.setColumnWidth(5, 320);

  return mapa;
}

function respuesta_(objeto) {
  return ContentService.createTextOutput(JSON.stringify(objeto)).setMimeType(
    ContentService.MimeType.JSON
  );
}

function limpiar_(valor, max) {
  return String(valor == null ? "" : valor).replace(/\s+/g, " ").trim().slice(0, max || 300);
}

function telefono_(valor) {
  let d = String(valor || "").replace(/\D/g, "");
  if (d.length === 12 && d.indexOf("52") === 0) d = d.slice(2);
  if (d.length === 13 && d.indexOf("521") === 0) d = d.slice(3);
  return d;
}

function folio_() {
  const fecha = Utilities.formatDate(new Date(), "America/Mexico_City", "yyyyMMdd");
  return "SV-" + fecha + "-" + Math.random().toString(36).slice(2, 6).toUpperCase();
}

/**
 * Correo que recibe los avisos. Si CONFIG.ADMIN_EMAIL sigue con el valor de
 * ejemplo (o está vacío), usa el correo de la cuenta dueña de la hoja, para
 * que las notificaciones nunca se pierdan en un dominio inexistente.
 */
function correoAdmin_() {
  const configurado = String(CONFIG.ADMIN_EMAIL || "").trim();
  const invalido =
    !configurado ||
    configurado.indexOf("@") < 1 ||
    /tudominio\.mx/i.test(configurado) ||
    /ejemplo|example/i.test(configurado);

  if (invalido) {
    try {
      return Session.getEffectiveUser().getEmail() || configurado;
    } catch (e) {
      return configurado;
    }
  }
  return configurado;
}

function fechaLegible_(fecha) {
  return Utilities.formatDate(fecha, "America/Mexico_City", "dd/MM/yyyy HH:mm");
}

function registrarError_(donde, error, detalle) {
  try {
    const libro = libro_();
    let hoja = libro.getSheetByName("Errores");
    if (!hoja) {
      hoja = libro.insertSheet("Errores");
      hoja.appendRow(["Fecha", "Dónde", "Mensaje", "Detalle"]).setFontWeight("bold");
    }
    hoja.appendRow([new Date(), donde, String(error), String(detalle || "").slice(0, 500)]);
  } catch (e) {
    console.error("No se pudo registrar el error: " + e);
  }
}

/* ============================================================== recepción */

function doPost(evento) {
  try {
    const crudo = (evento && evento.postData && evento.postData.contents) || "";
    let datos = {};
    try {
      datos = JSON.parse(crudo);
    } catch (e) {
      // Soporta también envíos de formulario tradicional
      datos = evento && evento.parameter ? evento.parameter : {};
    }

    // La landing envía "whatsapp"; la hoja usa "telefono"
    const nombre = limpiar_(datos.nombre || datos.name, 90);
    const celular = telefono_(datos.whatsapp || datos.telefono || datos.celular);
    const correo = limpiar_(datos.correo || datos.email, 120).toLowerCase();
    const plan = limpiar_(datos.plan, 60);
    const mensaje = limpiar_(datos.mensaje || datos.message, 600);

    const errores = {};
    if (nombre.length < 3) errores.nombre = "Escribe tu nombre completo.";
    if (celular.length !== 10) errores.whatsapp = "Escribe un celular a 10 dígitos.";
    if (!correo || correo.indexOf("@") < 1) errores.correo = "Escribe un correo válido.";
    if (!plan) errores.plan = "Selecciona un plan.";
    if (!datos.privacidad) errores.privacidad = "Debes aceptar el aviso de privacidad.";
    if (limpiar_(datos.honeypot, 50)) errores._spam = "rechazado";

    if (Object.keys(errores).length) {
      return respuesta_({
        ok: false,
        codigo: errores._spam ? "rechazado" : "validacion",
        errores: errores,
        mensaje: "Revisa los campos señalados.",
      });
    }

    const hoja = hoja_();
    const mapa = asegurarColumnas_(hoja);
    const filas = hoja.getLastRow();
    const ahora = new Date();

    // Deduplicación por celular (columna telefono)
    if (filas > 1 && mapa.telefono) {
      const desde = Math.max(2, filas - 199);
      const valores = hoja.getRange(desde, mapa.telefono, filas - desde + 1, 1).getValues();
      const fechas = mapa.fecha
        ? hoja.getRange(desde, mapa.fecha, filas - desde + 1, 1).getValues()
        : [];
      const limite = Date.now() - CONFIG.MINUTOS_DEDUPE * 60 * 1000;

      for (let i = valores.length - 1; i >= 0; i--) {
        const mismo = telefono_(valores[i][0]) === celular;
        const fechaFila = fechas.length ? fechas[i][0] : "";
        const reciente = fechaFila instanceof Date ? fechaFila.getTime() > limite : false;
        if (mismo && reciente) {
          const folioPrevio = mapa.folio
            ? hoja.getRange(2 + i, mapa.folio).getValue()
            : "";
          return respuesta_({
            ok: true,
            duplicado: true,
            folio: String(folioPrevio || ""),
            mensaje:
              "Ya tenemos una solicitud reciente con este número. Un asesor te contactará.",
          });
        }
      }
    }

    const folio = folio_();
    const origen = datos.origen || {};
    const fila = new Array(hoja.getLastColumn()).fill("");

    const poner = (campo, valor) => {
      if (mapa[campo]) fila[mapa[campo] - 1] = valor;
    };

    poner("nombre", nombre);
    poner("telefono", "'" + celular);
    poner("email", correo);
    poner("plan", plan);
    poner("mensaje", mensaje);
    poner("fecha", ahora);
    poner("fuente", limpiar_(origen.utm_source, 80) || "Landing Page");
    poner("estado", "Nuevo");
    poner("folio", folio);
    poner("campana", limpiar_(origen.utm_campaign, 120) || "silverado-ferreterias-cdmx-2026");

    hoja.appendRow(fila);

    const lead = {
      folio: folio,
      nombre: nombre,
      celular: celular,
      correo: correo,
      plan: plan,
      mensaje: mensaje,
      ciudad: limpiar_(datos.ciudad, 60),
      campana: limpiar_(origen.utm_campaign, 120) || "campaña directa",
      origen: limpiar_(origen.utm_source, 80) || "orgánico",
      fecha: fechaLegible_(ahora),
    };

    const estadoCorreos = {
      prospecto: "omitido",
      admin: "omitido",
      destinoProspecto: correo,
      destinoAdmin: destinatariosAdmin_(),
      error: "",
    };

    if (CONFIG.ENVIAR_CORREO_LEAD && correo) {
      try {
        enviarCorreoProspecto_(lead);
        estadoCorreos.prospecto = "enviado";
      } catch (falloProspecto) {
        estadoCorreos.prospecto = "error";
        estadoCorreos.error = String(falloProspecto);
        registrarError_("correo-prospecto", falloProspecto, correo);
      }
    }

    if (CONFIG.ENVIAR_CORREO_ADMIN) {
      try {
        enviarCorreoAdmin_(lead);
        estadoCorreos.admin = "enviado";
      } catch (falloAdmin) {
        estadoCorreos.admin = "error";
        estadoCorreos.error =
          (estadoCorreos.error ? estadoCorreos.error + " | " : "") + String(falloAdmin);
        registrarError_("correo-admin", falloAdmin, CONFIG.ADMIN_EMAIL);
      }
    }

    // Aviso explícito si el correo del administrador sigue sin configurar
    if (String(CONFIG.ADMIN_EMAIL).indexOf("tudominio") >= 0 || !CONFIG.ADMIN_EMAIL) {
      registrarError_(
        "configuracion",
        "ADMIN_EMAIL no configurado",
        "ADMIN_EMAIL sin configurar: los avisos se envían a " + correoAdmin_()
      );
    }

    return respuesta_({
      ok: true,
      duplicado: false,
      correo: estadoCorreos,
      registro: {
        archivo: libro_().getName(),
        pestana: hoja.getName(),
        fila: hoja.getLastRow(),
        hojaUrl: libro_().getUrl(),
      },
      folio: folio,
      mensaje:
        "Recibimos tus datos y quedaron registrados con folio " +
        folio +
        ". Un asesor se pondrá en contacto contigo.",
    });
  } catch (fallo) {
    console.error(fallo);
    registrarError_("doPost", fallo, "");
    return respuesta_({
      ok: false,
      codigo: "servidor",
      mensaje: "No pudimos registrar la solicitud. Intenta de nuevo.",
    });
  }
}

function doGet() {
  return respuesta_({ ok: true, servicio: "cotizaciones-silverado" });
}

/* ================================================================ correos */

function fila_(etiqueta, valor) {
  return (
    '<tr><td style="padding:7px 0;color:#6b7280;width:38%;vertical-align:top">' +
    etiqueta +
    '</td><td style="padding:7px 0;font-weight:bold">' +
    String(valor || "—") +
    "</td></tr>"
  );
}

/**
 * Envía el correo por MailApp y, si falla, reintenta con GmailApp.
 * Ambos envíos son inmediatos: no hay cola ni temporizador.
 */
function enviarConRespaldo_(parametros) {
  try {
    MailApp.sendEmail(parametros);
    return "MailApp";
  } catch (falloMail) {
    try {
      GmailApp.sendEmail(parametros.to, parametros.subject, parametros.body, {
        htmlBody: parametros.htmlBody,
        name: parametros.name,
        replyTo: parametros.replyTo,
      });
      return "GmailApp";
    } catch (falloGmail) {
      throw new Error("MailApp: " + falloMail + " | GmailApp: " + falloGmail);
    }
  }
}

/** Remitente de respuesta válido (evita un dominio inexistente). */
function responderA_() {
  const configurado = String(CONFIG.RESPONDER_A || "").trim();
  const invalido =
    !configurado ||
    configurado.indexOf("@") < 1 ||
    /tudominio\.mx/i.test(configurado) ||
    /ejemplo|example/i.test(configurado);
  return invalido ? correoAdmin_() : configurado;
}

function destinatariosAdmin_() {
  return [correoAdmin_(), String(CONFIG.COPIA_EMAIL || "").trim()]
    .filter((c) => c && c.indexOf("@") > 0)
    .join(",");
}

function enviarCorreoProspecto_(lead) {
  const wa = CONFIG.WHATSAPP
    ? '<p style="margin:18px 0"><a href="https://wa.me/' +
      CONFIG.WHATSAPP +
      '" style="background:#c7a24c;color:#171207;padding:12px 20px;border-radius:999px;text-decoration:none;font-weight:bold;display:inline-block">Escribir por WhatsApp</a></p>'
    : "";

  const html =
    '<div style="font-family:Arial,Helvetica,sans-serif;background:#f5f6f8;padding:28px">' +
    '<div style="max-width:560px;margin:0 auto;background:#ffffff;border-radius:14px;overflow:hidden">' +
    '<div style="background:#0b0e13;padding:22px 26px;color:#ffffff">' +
    '<div style="font-size:12px;letter-spacing:2px;color:#c7a24c;font-weight:bold">CHEVROLET SILVERADO</div>' +
    '<div style="font-size:22px;font-weight:bold;margin-top:6px">Recibimos tu solicitud</div></div>' +
    '<div style="padding:26px;color:#20242b;font-size:15px;line-height:1.6">' +
    "<p>Hola <strong>" +
    lead.nombre +
    "</strong>:</p>" +
    "<p>Gracias por tu interés. Tu solicitud quedó registrada con el folio <strong>" +
    lead.folio +
    "</strong>.</p>" +
    '<table style="width:100%;border-collapse:collapse;margin:18px 0;font-size:14px">' +
    fila_("Plan de compra", lead.plan) +
    fila_("Ciudad / Alcaldía", lead.ciudad) +
    fila_("Fecha", lead.fecha) +
    "</table>" +
    "<p>Un asesor de " +
    CONFIG.DISTRIBUIDOR +
    " te contactará en horario " +
    CONFIG.HORARIO +
    ".</p>" +
    wa +
    '<p style="font-size:12px;color:#6b7280;margin-top:22px">' +
    CONFIG.DISTRIBUIDOR +
    " · " +
    CONFIG.TELEFONO +
    "</p></div></div></div>";

  const texto =
    "Hola " + lead.nombre + ":\n\n" +
    "Recibimos tu solicitud de cotización de la Chevrolet Silverado.\n" +
    "Folio: " + lead.folio + "\n" +
    "Plan de compra: " + (lead.plan || "—") + "\n" +
    "Ciudad / Alcaldía: " + (lead.ciudad || "—") + "\n" +
    "Fecha: " + lead.fecha + "\n\n" +
    "Un asesor de " + CONFIG.DISTRIBUIDOR + " te contactará en horario " + CONFIG.HORARIO + ".\n" +
    (CONFIG.WHATSAPP ? "WhatsApp: https://wa.me/" + CONFIG.WHATSAPP + "\n" : "") +
    "\n" + CONFIG.DISTRIBUIDOR + " · " + CONFIG.TELEFONO + "\n";

  const opcionesProspecto = {
    to: lead.correo,
    subject: "Recibimos tu solicitud · Chevrolet Silverado (" + lead.folio + ")",
    body: texto,
    htmlBody: html,
    name: CONFIG.REMITENTE_NOMBRE,
    replyTo: responderA_(),
  };
  if (CONFIG.COPIA_OCULTA_LEAD) opcionesProspecto.bcc = correoAdmin_();
  enviarConRespaldo_(opcionesProspecto);
}

function enviarCorreoAdmin_(lead) {
  const url = libro_().getUrl();
  const html =
    '<div style="font-family:Arial,Helvetica,sans-serif;background:#f5f6f8;padding:24px">' +
    '<div style="max-width:600px;margin:0 auto;background:#ffffff;border-radius:14px;overflow:hidden">' +
    '<div style="background:#0b0e13;color:#ffffff;padding:20px 24px">' +
    '<div style="font-size:12px;letter-spacing:2px;color:#c7a24c;font-weight:bold">NUEVO LEAD</div>' +
    '<div style="font-size:20px;font-weight:bold;margin-top:4px">' +
    lead.nombre +
    "</div></div>" +
    '<div style="padding:22px 24px;color:#20242b;font-size:14px;line-height:1.6">' +
    '<table style="width:100%;border-collapse:collapse">' +
    fila_("Folio", lead.folio) +
    fila_("Celular", '<a href="https://wa.me/52' + lead.celular + '">' + lead.celular + "</a>") +
    fila_("Correo", '<a href="mailto:' + lead.correo + '">' + lead.correo + "</a>") +
    fila_("Plan", lead.plan) +
    fila_("Ciudad", lead.ciudad) +
    fila_("Campaña", lead.campana + " · " + lead.origen) +
    fila_("Fecha", lead.fecha) +
    (lead.mensaje ? fila_("Mensaje", lead.mensaje) : "") +
    "</table>" +
    '<p style="margin:20px 0"><a href="' +
    url +
    '" style="background:#c7a24c;color:#171207;padding:11px 18px;border-radius:999px;text-decoration:none;font-weight:bold">Abrir hoja de leads</a></p>' +
    '<p style="font-size:12px;color:#6b7280">Actualiza la columna «estado»: Nuevo → Contactado → Cotizado → Ganado / Perdido.</p>' +
    "</div></div></div>";

  const texto =
    "Nuevo lead de la landing.\n\n" +
    "Nombre: " + lead.nombre + "\n" +
    "Celular: " + lead.celular + "\n" +
    "Correo: " + lead.correo + "\n" +
    "Plan: " + (lead.plan || "—") + "\n" +
    "Ciudad: " + (lead.ciudad || "—") + "\n" +
    "Campaña: " + lead.campana + " · " + lead.origen + "\n" +
    "Folio: " + lead.folio + "\n" +
    "Fecha: " + lead.fecha + "\n" +
    (lead.mensaje ? "Mensaje: " + lead.mensaje + "\n" : "") +
    "\nHoja de leads: " + libro_().getUrl() + "\n";

  const opcionesAdmin = {
    to: destinatariosAdmin_(),
    subject: "Nuevo lead · " + lead.nombre + " · " + (lead.ciudad || "CDMX"),
    body: texto + "\n--\nVer en la hoja: " + url + "\n",
    name: CONFIG.REMITENTE_NOMBRE,
    replyTo: lead.correo || responderA_(),
  };
  if (!CONFIG.ADMIN_SIN_HTML) opcionesAdmin.htmlBody = html;
  enviarConRespaldo_(opcionesAdmin);
}

/* ============================================================= instalación */

/** Ejecuta `instalar` UNA vez después de pegar el código. */
function instalar() {
  const hoja = hoja_();
  asegurarColumnas_(hoja);

  const demo = {
    folio: "SV-DEMO-0001",
    nombre: "Prueba de instalación",
    celular: "5500000000",
    correo: CONFIG.ADMIN_EMAIL,
    plan: "Financiamiento",
    mensaje: "Correo de prueba.",
    ciudad: "Coyoacán",
    campana: "prueba",
    origen: "instalación",
    fecha: fechaLegible_(new Date()),
  };

  enviarCorreoAdmin_(demo);
  enviarCorreoProspecto_(demo);

  SpreadsheetApp.getUi().alert(
    "Listo.\n\nHoja preparada con las columnas necesarias.\nRevisa " +
      CONFIG.ADMIN_EMAIL +
      " y luego publica una NUEVA VERSIÓN de la implementación."
  );
}

/* ===================================================== verificador rápido */

/**
 * Ejecuta esta función para confirmar que el proyecto está ligado a la hoja
 * correcta y que el código nuevo es el que está en el editor.
 */
function verificar() {
  const libro = SpreadsheetApp.getActiveSpreadsheet();
  const hoja = libro ? libro.getSheets()[0] : null;
  const mensaje = libro
    ? "Proyecto ligado a la hoja:\n" +
      libro.getName() +
      "\n\nPestaña: " +
      hoja.getName() +
      "\nFilas: " +
      hoja.getLastRow() +
      "\n\nCódigo nuevo: SÍ (doGet y doPost existen).\n\n" +
      "IMPORTANTE: para que el formulario lo use, hay que publicar una VERSIÓN NUEVA " +
      "en Implementar → Administrar implementaciones → lápiz → Versión: Nueva versión."
    : "Este proyecto NO está ligado a ninguna hoja.\n\n" +
      "Ábrelo desde la hoja: Extensiones → Apps Script.";

  SpreadsheetApp.getUi().alert(mensaje);
}

/**
 * Prueba el envío de correos y muestra el resultado exacto.
 * Ejecútala desde el editor de Apps Script después de ajustar CONFIG.
 */
function probarCorreos() {
  const avisos = [];
  avisos.push("Destinatario administrador: " + destinatariosAdmin_());
  avisos.push("Cuota diaria restante: " + MailApp.getRemainingDailyQuota() + " correos");

  if (String(CONFIG.ADMIN_EMAIL).indexOf("tudominio") >= 0 || !CONFIG.ADMIN_EMAIL) {
    avisos.push(
      "⚠ ADMIN_EMAIL sigue con el valor de ejemplo: los avisos se enviarán a " +
        correoAdmin_() +
        "."
    );
  }

  try {
    MailApp.sendEmail({
      to: correoAdmin_(),
      subject: "Prueba de correo · landing Silverado",
      htmlBody:
        '<div style="font-family:Arial;padding:20px"><h2>Correo de prueba</h2>' +
        "<p>Si ves este mensaje, el envío desde Apps Script funciona.</p>" +
        "<p>Fecha: " + new Date() + "</p></div>",
      name: CONFIG.REMITENTE_NOMBRE,
    });
    avisos.push("✓ Administrador: enviado");
  } catch (fallo) {
    avisos.push("✗ Administrador: " + fallo);
    registrarError_("prueba-admin", fallo, CONFIG.ADMIN_EMAIL);
  }

  try {
    MailApp.sendEmail({
      to: CONFIG.RESPONDER_A || CONFIG.ADMIN_EMAIL,
      subject: "Prueba · confirmación al prospecto",
      htmlBody: '<div style="font-family:Arial;padding:20px"><p>Correo de prueba al prospecto.</p></div>',
      name: CONFIG.REMITENTE_NOMBRE,
    });
    avisos.push("✓ Prospecto: enviado");
  } catch (fallo) {
    avisos.push("✗ Prospecto: " + fallo);
    registrarError_("prueba-prospecto", fallo, CONFIG.RESPONDER_A);
  }

  avisos.push("");
  avisos.push("Si ambos dicen OK y no llegan: revisa Spam y Promociones.");
  avisos.push("Los correos salen de la cuenta que ejecuta el script.");
  SpreadsheetApp.getUi().alert(avisos.join("\n"));
}

/**
 * Muestra en un aviso: archivo, pestañas, encabezados y últimas filas escritas.
 * Úsala cuando un lead "no aparece": dirá dónde está escribiendo el script.
 */
function revisarHoja() {
  const libro = SpreadsheetApp.getActiveSpreadsheet();
  if (!libro) {
    SpreadsheetApp.getUi().alert("Este proyecto no está ligado a ninguna hoja.");
    return;
  }

  const pestanas = libro.getSheets().map((h) => h.getName());
  const hoja = hoja_();
  const filas = hoja.getLastRow();
  const columnas = Math.min(hoja.getLastColumn(), 12);
  const encabezados = filas > 0 ? hoja.getRange(1, 1, 1, columnas).getValues()[0].join(" | ") : "(vacía)";

  let ultimas = "(sin datos)";
  if (filas > 1) {
    const desde = Math.max(2, filas - 2);
    ultimas = hoja
      .getRange(desde, 1, filas - desde + 1, columnas)
      .getValues()
      .map((f) => f.join(" | "))
      .join("\n");
  }

  SpreadsheetApp.getUi().alert(
    "Archivo: " +
      libro.getName() +
      "\n" +
      libro.getUrl() +
      "\n\nPestañas: " +
      pestanas.join(", ") +
      "\n\nEl script escribe en la PESTAÑA: " +
      hoja.getName() +
      "\n(la primera del archivo)\n\nEncabezados:\n" +
      encabezados +
      "\n\nÚltimas filas:\n" +
      ultimas
  );
}
