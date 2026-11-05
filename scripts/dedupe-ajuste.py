"""Deduplicación más razonable: ventana corta y aviso de repetidos."""

import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ruta = RAIZ / "docs" / "google-apps-script.gs"
t = ruta.read_text(encoding="utf-8")

# 1) Ventana más corta
t = t.replace("  MINUTOS_DEDUPE: 30,", "  MINUTOS_DEDUPE: 10,")

# 2) Opción de avisar repetidos
if "AVISAR_DUPLICADOS" not in t:
    t = t.replace(
        "  MINUTOS_DEDUPE: 10,",
        "  MINUTOS_DEDUPE: 10,\n"
        "  /** Si alguien repite el envío con el mismo celular, avisa al administrador\n"
        "   *  (no se envía correo al prospecto ni se duplica la fila). */\n"
        "  AVISAR_DUPLICADOS: true,",
    )
    print("  AVISAR_DUPLICADOS agregada")

# 3) Aviso al detectar duplicado
t = t.replace(
    """        if (mismo && reciente) {
          const folioPrevio = mapa.folio ? hoja.getRange(2 + i, mapa.folio).getValue() : "";
          return respuesta_({""",
    """        if (mismo && reciente) {
          const folioPrevio = mapa.folio ? hoja.getRange(2 + i, mapa.folio).getValue() : "";

          if (CONFIG.AVISAR_DUPLICADOS) {
            try {
              MailApp.sendEmail({
                to: destinatariosAdmin_(),
                subject: "Envío repetido · " + nombre + " · " + celular,
                body:
                  "Alguien volvió a enviar el formulario con un celular registrado hace " +
                  CONFIG.MINUTOS_DEDUPE +
                  " minutos.\\n\\n" +
                  "Nombre: " + nombre + "\\n" +
                  "Celular: " + celular + "\\n" +
                  "Correo: " + correo + "\\n" +
                  "Plan: " + plan + "\\n" +
                  "Folio original: " + (folioPrevio || "—") + "\\n\\n" +
                  "No se creó una fila nueva. Si fue una persona distinta, pídele que " +
                  "use otro número o espera " + CONFIG.MINUTOS_DEDUPE + " minutos.\\n",
                name: CONFIG.REMITENTE_NOMBRE,
                replyTo: responderA_(),
              });
            } catch (falloAviso) {
              registrarError_("aviso-duplicado", falloAviso, celular);
            }
          }

          return respuesta_({""",
)

ruta.write_text(t, encoding="utf-8", newline="\n")

copia = RAIZ / "apps-script-check.js"
copia.write_text(t, encoding="utf-8")
r = subprocess.run(["node", "--check", str(copia)], capture_output=True, text=True)
print("  sintaxis:", "OK" if r.returncode == 0 else r.stderr[:300])
copia.unlink(missing_ok=True)

for linea in t.splitlines():
    if any(x in linea for x in ["MINUTOS_DEDUPE:", "AVISAR_DUPLICADOS", "aviso-duplicado"]):
        print("  >", linea.strip()[:70])
