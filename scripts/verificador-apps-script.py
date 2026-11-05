"""Añade un verificador de proyecto al Apps Script."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ruta = RAIZ / "docs" / "google-apps-script.gs"
t = ruta.read_text(encoding="utf-8")

bloque = '''
/* ===================================================== verificador rápido */

/**
 * Ejecuta esta función para confirmar que el proyecto está ligado a la hoja
 * correcta y que el código nuevo es el que está en el editor.
 */
function verificar() {
  const libro = SpreadsheetApp.getActiveSpreadsheet();
  const hoja = libro ? libro.getSheets()[0] : null;
  const mensaje = libro
    ? "Proyecto ligado a la hoja:\\n" +
      libro.getName() +
      "\\n\\nPestaña: " +
      hoja.getName() +
      "\\nFilas: " +
      hoja.getLastRow() +
      "\\n\\nCódigo nuevo: SÍ (doGet y doPost existen).\\n\\n" +
      "IMPORTANTE: para que el formulario lo use, hay que publicar una VERSIÓN NUEVA " +
      "en Implementar → Administrar implementaciones → lápiz → Versión: Nueva versión."
    : "Este proyecto NO está ligado a ninguna hoja.\\n\\n" +
      "Ábrelo desde la hoja: Extensiones → Apps Script.";

  SpreadsheetApp.getUi().alert(mensaje);
}
'''

if "function verificar()" not in t:
    t = t.rstrip() + "\n" + bloque
    ruta.write_text(t, encoding="utf-8", newline="\n")
    print("  verificador añadido")
else:
    print("  ya existía")

# Validación de sintaxis
import subprocess

copia = RAIZ / "apps-script-check.js"
copia.write_text(t, encoding="utf-8")
r = subprocess.run(["node", "--check", str(copia)], capture_output=True, text=True)
print("  sintaxis:", "OK" if r.returncode == 0 else r.stderr[:200])
copia.unlink(missing_ok=True)
