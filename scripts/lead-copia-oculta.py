"""Copia oculta al administrador del correo al lead y remitente válido."""

import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ruta = RAIZ / "docs" / "google-apps-script.gs"
t = ruta.read_text(encoding="utf-8")

# 1) Nueva opción: copia oculta del correo al prospecto
if "COPIA_OCULTA_LEAD" not in t:
    t = t.replace(
        '  COPIA_EMAIL: "",',
        '  COPIA_EMAIL: "",\n'
        '  /** Si es true, el correo al prospecto llega también (CCO) al administrador.\n'
        '   *  Sirve para verificar que el mensaje al lead realmente se envió. */\n'
        '  COPIA_OCULTA_LEAD: true,',
    )
    print("  opción COPIA_OCULTA_LEAD agregada")

# 2) Remitente de respuesta con respaldo real
if "function responderA_()" not in t:
    t = t.replace(
        "function destinatariosAdmin_() {",
        '''/** Remitente de respuesta válido (evita un dominio inexistente). */
function responderA_() {
  const configurado = String(CONFIG.RESPONDER_A || "").trim();
  const invalido =
    !configurado ||
    configurado.indexOf("@") < 1 ||
    /tudominio\\.mx/i.test(configurado) ||
    /ejemplo|example/i.test(configurado);
  return invalido ? correoAdmin_() : configurado;
}

function destinatariosAdmin_() {''',
    )
    print("  responderA_() agregada")

# 3) Envío al prospecto con copia oculta y reply-to válido
t = t.replace(
    """  MailApp.sendEmail({
    to: lead.correo,
    subject: "Recibimos tu solicitud · Chevrolet Silverado (" + lead.folio + ")",
    body: texto,
    htmlBody: html,
    name: CONFIG.REMITENTE_NOMBRE,
    replyTo: CONFIG.RESPONDER_A,
  });""",
    """  const opcionesProspecto = {
    to: lead.correo,
    subject: "Recibimos tu solicitud · Chevrolet Silverado (" + lead.folio + ")",
    body: texto,
    htmlBody: html,
    name: CONFIG.REMITENTE_NOMBRE,
    replyTo: responderA_(),
  };
  if (CONFIG.COPIA_OCULTA_LEAD) opcionesProspecto.bcc = correoAdmin_();
  enviarConRespaldo_(opcionesProspecto);""",
)

# 4) El comando de prueba también usa reply-to válido
t = t.replace("    replyTo: lead.correo || CONFIG.RESPONDER_A,", "    replyTo: lead.correo || responderA_(),")

# 5) La respuesta informa los destinos reales
t = t.replace(
    "    const estadoCorreos = { prospecto: \"omitido\", admin: \"omitido\", error: \"\" };",
    "    const estadoCorreos = {\n"
    "      prospecto: \"omitido\",\n"
    "      admin: \"omitido\",\n"
    "      destinoProspecto: correo,\n"
    "      destinoAdmin: destinatariosAdmin_(),\n"
    "      error: \"\",\n"
    "    };",
)

ruta.write_text(t, encoding="utf-8", newline="\n")

copia = RAIZ / "apps-script-check.js"
copia.write_text(t, encoding="utf-8")
r = subprocess.run(["node", "--check", str(copia)], capture_output=True, text=True)
print("  sintaxis:", "OK" if r.returncode == 0 else r.stderr[:400])
copia.unlink(missing_ok=True)

for linea in t.splitlines():
    if any(x in linea for x in ["COPIA_OCULTA_LEAD", "function responderA_", "opcionesProspecto.bcc", "destinoProspecto"]):
        print("  >", linea.strip()[:78])
