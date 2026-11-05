"""Los avisos caen al correo dueño de la hoja si ADMIN_EMAIL no está configurado."""

import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ruta = RAIZ / "docs" / "google-apps-script.gs"
t = ruta.read_text(encoding="utf-8")

# 1) Helper de destinatario con respaldo real
if "function correoAdmin_()" not in t:
    t = t.replace(
        "function fechaLegible_(fecha) {",
        '''/**
 * Correo que recibe los avisos. Si CONFIG.ADMIN_EMAIL sigue con el valor de
 * ejemplo (o está vacío), usa el correo de la cuenta dueña de la hoja, para
 * que las notificaciones nunca se pierdan en un dominio inexistente.
 */
function correoAdmin_() {
  const configurado = String(CONFIG.ADMIN_EMAIL || "").trim();
  const invalido =
    !configurado ||
    configurado.indexOf("@") < 1 ||
    /tudominio\\.mx/i.test(configurado) ||
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

function fechaLegible_(fecha) {''',
    )
    print("  helper correoAdmin_() agregado")

# 2) El aviso al administrador usa el helper
t = t.replace("    to: CONFIG.ADMIN_EMAIL,", "    to: correoAdmin_(),")

# 3) La prueba muestra el destino real y el respaldo
t = t.replace(
    '  avisos.push("Destinatario administrador: " + CONFIG.ADMIN_EMAIL);',
    '  avisos.push("Destinatario administrador: " + correoAdmin_());',
)
t = t.replace(
    '    to: CONFIG.ADMIN_EMAIL,\n    subject: "Prueba de correo · landing Silverado",',
    '    to: correoAdmin_(),\n    subject: "Prueba de correo · landing Silverado",',
)
t = t.replace(
    '  if (String(CONFIG.ADMIN_EMAIL).indexOf("tudominio") >= 0) {',
    "  if (String(CONFIG.ADMIN_EMAIL).indexOf(\"tudominio\") >= 0 || !CONFIG.ADMIN_EMAIL) {",
)
t = t.replace(
    '    avisos.push("⚠ ADMIN_EMAIL sigue con el valor de ejemplo. Cámbialo antes de probar.");',
    '    avisos.push(\n      "⚠ ADMIN_EMAIL sigue con el valor de ejemplo: los avisos se enviarán a " +\n        correoAdmin_() +\n        "."\n    );',
)

# 4) El registro de configuración avisa del respaldo
t = t.replace(
    '        "Cambia CONFIG.ADMIN_EMAIL por un correo real; los avisos no llegarán."',
    '        "ADMIN_EMAIL sin configurar: los avisos se envían a " + correoAdmin_()',
)

ruta.write_text(t, encoding="utf-8", newline="\n")

copia = RAIZ / "apps-script-check.js"
copia.write_text(t, encoding="utf-8")
r = subprocess.run(["node", "--check", str(copia)], capture_output=True, text=True)
print("  sintaxis:", "OK" if r.returncode == 0 else r.stderr[:300])
copia.unlink(missing_ok=True)

# Mostrar los puntos clave
import re

for linea in t.splitlines():
    if "correoAdmin_()" in linea or "to: CONFIG.ADMIN_EMAIL" in linea:
        print("  →", linea.strip())

for comando in (["node", "scripts/build-index-html.mjs"], ["node", "build.mjs"]):
    rr = subprocess.run(comando, cwd=RAIZ, capture_output=True, text=True)
    print("  ", comando[-1], "->", "OK" if rr.returncode == 0 else rr.stderr[:200])
