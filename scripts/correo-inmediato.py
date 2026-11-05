"""Copia opcional al administrador y reintento por GmailApp."""

import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ruta = RAIZ / "docs" / "google-apps-script.gs"
t = ruta.read_text(encoding="utf-8")

# 1) Opción de copia
if "COPIA_EMAIL" not in t:
    t = t.replace(
        '  REMITENTE_NOMBRE: "Chevrolet Silverado · Ferreterías CDMX",',
        '  REMITENTE_NOMBRE: "Chevrolet Silverado · Ferreterías CDMX",\n'
        '  /** Copia opcional: segundo correo que recibe los avisos (déjalo vacío si no). */\n'
        '  COPIA_EMAIL: "",',
    )
    print("  COPIA_EMAIL agregada")

# 2) Función de envío con reintento
if "function enviarConRespaldo_" not in t:
    t = t.replace(
        "function enviarCorreoProspecto_(lead) {",
        '''/**
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

function destinatariosAdmin_() {
  return [correoAdmin_(), String(CONFIG.COPIA_EMAIL || "").trim()]
    .filter((c) => c && c.indexOf("@") > 0)
    .join(",");
}

function enviarCorreoProspecto_(lead) {''',
    )
    print("  envío con reintento agregado")

# 3) Usar la función de respaldo en el aviso al administrador
t = t.replace(
    """  MailApp.sendEmail({
    to: correoAdmin_(),
    subject: "Nuevo lead · " + lead.nombre + " · " + (lead.ciudad || "CDMX"),
    body: texto,
    htmlBody: html,
    name: CONFIG.REMITENTE_NOMBRE,
    replyTo: lead.correo || CONFIG.RESPONDER_A,
  });""",
    """  enviarConRespaldo_({
    to: destinatariosAdmin_(),
    subject: "Nuevo lead · " + lead.nombre + " · " + (lead.ciudad || "CDMX"),
    body: texto,
    htmlBody: html,
    name: CONFIG.REMITENTE_NOMBRE,
    replyTo: lead.correo || CONFIG.RESPONDER_A,
  });""",
)

# 4) La prueba también muestra la copia y el estado
t = t.replace(
    '  avisos.push("Destinatario administrador: " + correoAdmin_());',
    '  avisos.push("Destinatario administrador: " + destinatariosAdmin_());',
)
t = t.replace(
    """    to: correoAdmin_(),
    subject: "Prueba de correo · landing Silverado",""",
    """    to: destinatariosAdmin_(),
    subject: "Prueba de correo · landing Silverado",""",
)

ruta.write_text(t, encoding="utf-8", newline="\n")

copia = RAIZ / "apps-script-check.js"
copia.write_text(t, encoding="utf-8")
r = subprocess.run(["node", "--check", str(copia)], capture_output=True, text=True)
print("  sintaxis:", "OK" if r.returncode == 0 else r.stderr[:300])
copia.unlink(missing_ok=True)

for linea in t.splitlines():
    if "enviarConRespaldo_(" in linea or "COPIA_EMAIL" in linea or "destinatariosAdmin_" in linea:
        print("  >", linea.strip()[:80])
