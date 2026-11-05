"""Hace visible el estado de los correos y agrega una prueba directa."""

import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ruta = RAIZ / "docs" / "google-apps-script.gs"
t = ruta.read_text(encoding="utf-8")

# ------------------------------------------------- 1. Estado de correos en el doPost
viejo = """    try {
      if (CONFIG.ENVIAR_CORREO_LEAD && correo) enviarCorreoProspecto_(lead);
      if (CONFIG.ENVIAR_CORREO_ADMIN) enviarCorreoAdmin_(lead);
    } catch (falloCorreo) {
      console.error("Correo no enviado: " + falloCorreo);
    }

    return respuesta_({
      ok: true,
      duplicado: false,
      folio: folio,"""

nuevo = """    const estadoCorreos = { prospecto: "omitido", admin: "omitido", error: "" };

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
    if (String(CONFIG.ADMIN_EMAIL).indexOf("tudominio") >= 0) {
      registrarError_(
        "configuracion",
        "ADMIN_EMAIL no configurado",
        "Cambia CONFIG.ADMIN_EMAIL por un correo real; los avisos no llegarán."
      );
    }

    return respuesta_({
      ok: true,
      duplicado: false,
      correo: estadoCorreos,
      folio: folio,"""

if viejo in t:
    t = t.replace(viejo, nuevo)
    print("  estado de correos en la respuesta")
else:
    print("  (no se encontró el bloque de correos: revisar a mano)")

# ------------------------------------------------------- 2. Prueba de correos
bloque = '''
/**
 * Prueba el envío de correos y muestra el resultado exacto.
 * Ejecútala desde el editor de Apps Script después de ajustar CONFIG.
 */
function probarCorreos() {
  const avisos = [];
  avisos.push("Destinatario administrador: " + CONFIG.ADMIN_EMAIL);
  avisos.push("Cuota diaria restante: " + MailApp.getRemainingDailyQuota() + " correos");

  if (String(CONFIG.ADMIN_EMAIL).indexOf("tudominio") >= 0) {
    avisos.push("⚠ ADMIN_EMAIL sigue con el valor de ejemplo. Cámbialo antes de probar.");
  }

  try {
    MailApp.sendEmail({
      to: CONFIG.ADMIN_EMAIL,
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
  avisos.push("Si ambos dicen ✓ y no llegan: revisa Spam, Promociones y la cuota.");
  SpreadsheetApp.getUi().alert(avisos.join("\\n"));
}
'''

if "function probarCorreos()" not in t:
    t = t.rstrip() + "\n" + bloque
    print("  función probarCorreos() agregada")

ruta.write_text(t, encoding="utf-8", newline="\n")

copia = RAIZ / "apps-script-check.js"
copia.write_text(t, encoding="utf-8")
r = subprocess.run(["node", "--check", str(copia)], capture_output=True, text=True)
print("  sintaxis:", "OK" if r.returncode == 0 else r.stderr[:300])
copia.unlink(missing_ok=True)
