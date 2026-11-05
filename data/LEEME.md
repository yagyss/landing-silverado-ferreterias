# Datos de prospectos

En esta carpeta se guarda `prospectos.jsonl`: **una línea JSON por solicitud de cotización**
registrada por el endpoint `POST /api/cotizacion`.

## Formato de cada registro

```json
{
  "folio": "SV-20261104-8ON1",
  "fecha": "2026-11-04T22:31:07.812Z",
  "campana": "silverado-ferreterias-cdmx-2026",
  "canal": "Meta Ads",
  "pagina": "https://dominio.mx/",
  "origen": {
    "utm_source": "facebook",
    "utm_medium": "paid_social",
    "utm_campaign": "silverado-ferreterias",
    "utm_content": "",
    "utm_term": "",
    "fbclid": "",
    "referrer": "https://facebook.com/"
  },
  "datos": {
    "nombre": "María Fernanda López",
    "whatsapp": "5512345678",
    "correo": "maria@ferreteria.mx",
    "ciudad": "Coyoacán",
    "ferreteria": "Ferretería El Tornillo",
    "sucursales": "2 sucursales",
    "usoVehiculo": "No, todavía no",
    "interes": "Financiamiento",
    "aceptoPrivacidad": true
  },
  "seguimiento": { "estado": "nuevo", "eventoMeta": "Lead" }
}
```

## Consideraciones

- **No se sirve por HTTP.** El servidor local solo publica `assets/`, `src/styles`, `src/js`,
  `src/data` y `src/layout`; esta carpeta queda fuera. Aun así, protégela en el hosting real.
- Contiene datos personales: aplica el aviso de privacidad y el principio de minimización.
  No se almacena la IP ni la dirección exacta.
- Para producción se recomienda enviar los prospectos a un CRM o webhook (`SITE.leads.webhookUrl`)
  y definir una política de retención y borrado.
- El archivo se crea automáticamente con el primer registro. Puedes vaciarlo sin riesgo: el
  servidor vuelve a crearlo cuando llegue la siguiente solicitud.
