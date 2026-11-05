"""Mejora la entregabilidad de los correos (texto plano + diagnósticos)."""

import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ruta = RAIZ / "docs" / "google-apps-script.gs"
t = ruta.read_text(encoding="utf-8")

# 1) Correo al prospecto: agrega cuerpo en texto plano
t = t.replace(
    """  MailApp.sendEmail({
    to: lead.correo,
    subject: "Recibimos tu solicitud · Chevrolet Silverado (" + lead.folio + ")",
    htmlBody: html,""",
    """  const texto =
    "Hola " + lead.nombre + ":\\n\\n" +
    "Recibimos tu solicitud de cotización de la Chevrolet Silverado.\\n" +
    "Folio: " + lead.folio + "\\n" +
    "Plan de compra: " + (lead.plan || "—") + "\\n" +
    "Ciudad / Alcaldía: " + (lead.ciudad || "—") + "\\n" +
    "Fecha: " + lead.fecha + "\\n\\n" +
    "Un asesor de " + CONFIG.DISTRIBUIDOR + " te contactará en horario " + CONFIG.HORARIO + ".\\n" +
    (CONFIG.WHATSAPP ? "WhatsApp: https://wa.me/" + CONFIG.WHATSAPP + "\\n" : "") +
    "\\n" + CONFIG.DISTRIBUIDOR + " · " + CONFIG.TELEFONO + "\\n";

  MailApp.sendEmail({
    to: lead.correo,
    subject: "Recibimos tu solicitud · Chevrolet Silverado (" + lead.folio + ")",
    body: texto,
    htmlBody: html,""",
)

# 2) Correo al administrador: texto plano y asunto más neutro
t = t.replace(
    """  MailApp.sendEmail({
    to: correoAdmin_(),
    subject: "Nuevo lead · " + lead.nombre + " · " + (lead.ciudad || "CDMX"),
    htmlBody: html,""",
    """  const texto =
    "Nuevo lead de la landing.\\n\\n" +
    "Nombre: " + lead.nombre + "\\n" +
    "Celular: " + lead.celular + "\\n" +
    "Correo: " + lead.correo + "\\n" +
    "Plan: " + (lead.plan || "—") + "\\n" +
    "Ciudad: " + (lead.ciudad || "—") + "\\n" +
    "Campaña: " + lead.campana + " · " + lead.origen + "\\n" +
    "Folio: " + lead.folio + "\\n" +
    "Fecha: " + lead.fecha + "\\n" +
    (lead.mensaje ? "Mensaje: " + lead.mensaje + "\\n" : "") +
    "\\nHoja de leads: " + libro_().getUrl() + "\\n";

  MailApp.sendEmail({
    to: correoAdmin_(),
    subject: "Nuevo lead · " + lead.nombre + " · " + (lead.ciudad || "CDMX"),
    body: texto,
    htmlBody: html,""",
)

# 3) Prueba con más contexto
t = t.replace(
    '  avisos.push("");\n  avisos.push("Si ambos dicen ✓ y no llegan: revisa Spam, Promociones y la cuota.");',
    '  avisos.push("");\n'
    '  avisos.push("Si ambos dicen OK y no llegan: revisa Spam y Promociones.");\n'
    '  avisos.push("Los correos salen de la cuenta que ejecuta el script.");',
)

ruta.write_text(t, encoding="utf-8", newline="\n")

copia = RAIZ / "apps-script-check.js"
copia.write_text(t, encoding="utf-8")
r = subprocess.run(["node", "--check", str(copia)], capture_output=True, text=True)
print("  sintaxis:", "OK" if r.returncode == 0 else r.stderr[:300])
copia.unlink(missing_ok=True)

for linea in t.splitlines():
    if "body: texto" in linea:
        print("  texto plano añadido:", linea.strip()[:60])
