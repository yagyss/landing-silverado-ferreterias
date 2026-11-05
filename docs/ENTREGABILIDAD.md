# Que los correos no caigan en Spam

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
