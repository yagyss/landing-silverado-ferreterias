"""Agrega columnas 'repetido' y 'veces' sin bloquear registros."""

import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ruta = RAIZ / "docs" / "google-apps-script.gs"
t = ruta.read_text(encoding="utf-8")

# 1) Nuevas columnas
t = t.replace(
    'const COLUMNAS_PROPIAS = ["fecha", "fuente", "estado", "asesor", "notas", "folio", "campana"];',
    'const COLUMNAS_PROPIAS = [\n'
    '  "fecha",\n'
    '  "fuente",\n'
    '  "estado",\n'
    '  "asesor",\n'
    '  "notas",\n'
    '  "folio",\n'
    '  "campana",\n'
    '  "repetido",\n'
    '  "veces",\n'
    '];',
)

# 2) Reemplaza el bloque de deduplicación por historial + marcado
inicio = t.index("    // Deduplicación por celular (solo si CONFIG.MINUTOS_DEDUPE > 0)")
fin = t.index("    const folio = folio_();", inicio)

nuevo = '''    // Historial del celular: marca repetidos sin bloquear el registro.
    let enviosPrevios = 0;
    let folioPrevio = "";

    if (filas > 1 && mapa.telefono) {
      const desde = Math.max(2, filas - 999);
      const valores = hoja.getRange(desde, mapa.telefono, filas - desde + 1, 1).getValues();
      const fechas = mapa.fecha
        ? hoja.getRange(desde, mapa.fecha, filas - desde + 1, 1).getValues()
        : [];
      const limite = Date.now() - CONFIG.MINUTOS_DEDUPE * 60 * 1000;

      for (let i = 0; i < valores.length; i++) {
        if (telefono_(valores[i][0]) !== celular) continue;
        enviosPrevios += 1;

        if (!folioPrevio && mapa.folio) {
          const valor = hoja.getRange(desde + i, mapa.folio).getValue();
          folioPrevio = valor ? String(valor) : "";
        }

        // Solo bloquea si CONFIG.MINUTOS_DEDUPE > 0
        if (CONFIG.MINUTOS_DEDUPE > 0) {
          const fechaFila = fechas.length ? fechas[i][0] : "";
          const reciente = fechaFila instanceof Date && fechaFila.getTime() > limite;
          if (!reciente) continue;

          if (CONFIG.AVISAR_DUPLICADOS) {
            try {
              MailApp.sendEmail({
                to: destinatariosAdmin_(),
                subject: "Envío repetido · " + nombre + " · " + celular,
                body:
                  "Alguien volvió a enviar el formulario con un celular registrado hace " +
                  CONFIG.MINUTOS_DEDUPE +
                  " minutos.\\n\\nNombre: " +
                  nombre +
                  "\\nCelular: " +
                  celular +
                  "\\nCorreo: " +
                  correo +
                  "\\nPlan: " +
                  plan +
                  "\\nFolio original: " +
                  (folioPrevio || "—") +
                  "\\n",
                name: CONFIG.REMITENTE_NOMBRE,
                replyTo: responderA_(),
              });
            } catch (falloAviso) {
              registrarError_("aviso-duplicado", falloAviso, celular);
            }
          }

          return respuesta_({
            ok: true,
            duplicado: true,
            folio: folioPrevio,
            mensaje:
              "Ya tenemos una solicitud reciente con este número. Un asesor te contactará.",
          });
        }
      }
    }

'''

t = t[:inicio] + nuevo + t[fin:]

# 3) Marcar las columnas al escribir la fila
t = t.replace(
    '    poner("campana", limpiar_(origen.utm_campaign, 120) || "silverado-ferreterias-cdmx-2026");',
    '    poner("campana", limpiar_(origen.utm_campaign, 120) || "silverado-ferreterias-cdmx-2026");\n'
    '    poner("repetido", enviosPrevios > 0 ? "Sí" : "No");\n'
    '    poner("veces", String(enviosPrevios + 1));',
)

# 4) Datos del lead para el correo
t = t.replace(
    '      origen: limpiar_(origen.utm_source, 80) || "orgánico",',
    '      origen: limpiar_(origen.utm_source, 80) || "orgánico",\n'
    '      repetido: enviosPrevios > 0,\n'
    '      veces: enviosPrevios + 1,',
)

# 5) El aviso al administrador indica si es repetido
t = t.replace(
    '    fila_("Fecha", lead.fecha) +\n    (lead.mensaje ? fila_("Mensaje", lead.mensaje) : "") +',
    '    fila_("Fecha", lead.fecha) +\n'
    '    (lead.repetido ? fila_("Repetido", "Sí · envío " + lead.veces) : "") +\n'
    '    (lead.mensaje ? fila_("Mensaje", lead.mensaje) : "") +',
)
t = t.replace(
    '    "Fecha: " + lead.fecha + "\\n" +\n    (lead.mensaje ? "Mensaje: " + lead.mensaje + "\\n" : "") +',
    '    "Fecha: " + lead.fecha + "\\n" +\n'
    '    (lead.repetido ? "Repetido: sí (envío " + lead.veces + ")\\n" : "") +\n'
    '    (lead.mensaje ? "Mensaje: " + lead.mensaje + "\\n" : "") +',
)

# 6) La respuesta incluye repetido/veces
t = t.replace(
    "      folio: folio,\n      mensaje:\n        \"Recibimos tus datos",
    "      repetido: enviosPrevios > 0,\n      veces: enviosPrevios + 1,\n      folio: folio,\n      mensaje:\n        \"Recibimos tus datos",
)

ruta.write_text(t, encoding="utf-8", newline="\n")

copia = RAIZ / "apps-script-check.js"
copia.write_text(t, encoding="utf-8")
r = subprocess.run(["node", "--check", str(copia)], capture_output=True, text=True)
print("  sintaxis:", "OK" if r.returncode == 0 else r.stderr[:400])
copia.unlink(missing_ok=True)

for linea in t.splitlines():
    if any(x in linea for x in ['"repetido"', "enviosPrevios", '"veces"', "repetido:"]):
        print("  >", linea.strip()[:76])
