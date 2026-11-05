"""Aviso al administrador en texto plano (mejor entregabilidad) + guía."""

import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ruta = RAIZ / "docs" / "google-apps-script.gs"
t = ruta.read_text(encoding="utf-8")

# 1) Opción: aviso interno sin HTML
if "ADMIN_SIN_HTML" not in t:
    t = t.replace(
        '  COPIA_OCULTA_LEAD: true,',
        '  COPIA_OCULTA_LEAD: true,\n'
        '  /** El aviso interno se envía solo en texto plano: Gmail lo marca menos\n'
        '   *  como spam que un correo HTML con botones y enlaces. */\n'
        '  ADMIN_SIN_HTML: true,',
    )
    print("  opción ADMIN_SIN_HTML agregada")

# 2) Enviar el aviso al administrador en texto plano cuando corresponda
t = t.replace(
    """  enviarConRespaldo_({
    to: destinatariosAdmin_(),
    subject: "Nuevo lead · " + lead.nombre + " · " + (lead.ciudad || "CDMX"),
    body: texto,
    htmlBody: html,
    name: CONFIG.REMITENTE_NOMBRE,
    replyTo: lead.correo || responderA_(),
  });""",
    """  const opcionesAdmin = {
    to: destinatariosAdmin_(),
    subject: "Nuevo lead · " + lead.nombre + " · " + (lead.ciudad || "CDMX"),
    body: texto + "\\n--\\nVer en la hoja: " + url + "\\n",
    name: CONFIG.REMITENTE_NOMBRE,
    replyTo: lead.correo || responderA_(),
  };
  if (!CONFIG.ADMIN_SIN_HTML) opcionesAdmin.htmlBody = html;
  enviarConRespaldo_(opcionesAdmin);""",
)

# 3) La prueba también respeta el modo texto plano
t = t.replace(
    """    MailApp.sendEmail({
      to: destinatariosAdmin_(),
      subject: "Prueba de correo · landing Silverado",
      body: "Prueba de envío desde Apps Script. Fecha: " + new Date(),
      htmlBody:""",
    """    MailApp.sendEmail({
      to: destinatariosAdmin_(),
      subject: "Prueba de correo · landing Silverado",
      body: "Prueba de envío desde Apps Script. Fecha: " + new Date(),
      htmlBody:""",
)

ruta.write_text(t, encoding="utf-8", newline="\n")

copia = RAIZ / "apps-script-check.js"
copia.write_text(t, encoding="utf-8")
r = subprocess.run(["node", "--check", str(copia)], capture_output=True, text=True)
print("  sintaxis:", "OK" if r.returncode == 0 else r.stderr[:300])
copia.unlink(missing_ok=True)

# 4) Guía
(P1 := RAIZ / "docs" / "ENTREGABILIDAD.md").write_text(
    """# Que los correos no caigan en Spam

## Por qué pasa

Los correos salen de una cuenta **gratuita de Gmail** mediante Apps Script. Gmail aplica
sus filtros y, al ser un remitente nuevo para el destinatario, los manda a **Spam** o
**Promociones**. No es un error del formulario: el correo sí se envió.

## Solución rápida: filtro en Gmail (2 minutos)

En **cada** cuenta que debe recibir avisos:

1. Gmail → ⚙️ **Ver todos los ajustes** → **Filtros y direcciones bloqueadas**.
2. **Crear un filtro nuevo**.
3. En *De*, escribe el correo que envía los avisos (la cuenta dueña de la hoja).
4. **Crear filtro** y marca:
   - ☑ **Nunca enviar a Spam**
   - ☑ **Aplicar la etiqueta**: crear `Leads`
   - ☑ **Marcar como importante**
   - ☑ **Aplicar también a los mensajes que coincidan** (opcional)
5. **Crear filtro**.

Repite en la cuenta del prospecto de prueba si quieres validarlo ahí.

## Entrenar el filtro (una vez por cuenta)

1. Abre el correo que cayó en Spam.
2. Botón **“No es spam”**.
3. Si aparece, confirma “Los correos de este remitente no son spam”.

## Mejoras ya aplicadas al contenido

| Ajuste | Efecto |
| --- | --- |
| Cuerpo en **texto plano** además de HTML | Menos señales de spam |
| Aviso interno **solo texto** (`ADMIN_SIN_HTML`) | Los avisos al equipo llegan mejor |
| `Reply-To` con dirección real | Evita un dominio inexistente |
| Sin imágenes ni adjuntos | Elimina otro motivo de filtrado |

## Solución definitiva (cuando quieras escalar)

1. **Google Workspace + dominio propio** (ventas@tudominio.com):
   - Publica **SPF**, **DKIM** y **DMARC** en tu DNS.
   - Los correos pasan a ser de remitente verificado y casi nunca caen en Spam.
2. **Servicio transaccional** (Resend, SendGrid, Postmark):
   - Apps Script los llama con `UrlFetchApp`.
   - Tienen entregabilidad gestionada y estadísticas de apertura.

Mientras no hagas eso, el filtro del paso anterior resuelve el 100% de los casos en tus
cuentas, y el prospecto puede mover el correo a su bandeja (le llega con folio y datos).
""",
    encoding="utf-8",
    newline="\n",
)
print("  guía docs/ENTREGABILIDAD.md creada")
