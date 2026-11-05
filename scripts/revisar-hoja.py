"""Añade diagnóstico de ubicación de la hoja y devuelve dónde se escribió."""

import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ruta = RAIZ / "docs" / "google-apps-script.gs"
t = ruta.read_text(encoding="utf-8")

# 1) La respuesta del doPost indica archivo, pestaña y fila
t = t.replace(
    """    return respuesta_({
      ok: true,
      duplicado: false,
      correo: estadoCorreos,
      folio: folio,""",
    """    return respuesta_({
      ok: true,
      duplicado: false,
      correo: estadoCorreos,
      registro: {
        archivo: libro_().getName(),
        pestana: hoja.getName(),
        fila: hoja.getLastRow(),
        hojaUrl: libro_().getUrl(),
      },
      folio: folio,""",
)

# 2) Función de verificación de ubicación
bloque = '''
/**
 * Muestra en un aviso: archivo, pestañas, encabezados y últimas filas escritas.
 * Úsala cuando un lead "no aparece": dirá dónde está escribiendo el script.
 */
function revisarHoja() {
  const libro = SpreadsheetApp.getActiveSpreadsheet();
  if (!libro) {
    SpreadsheetApp.getUi().alert("Este proyecto no está ligado a ninguna hoja.");
    return;
  }

  const pestanas = libro.getSheets().map((h) => h.getName());
  const hoja = hoja_();
  const filas = hoja.getLastRow();
  const columnas = Math.min(hoja.getLastColumn(), 12);
  const encabezados = filas > 0 ? hoja.getRange(1, 1, 1, columnas).getValues()[0].join(" | ") : "(vacía)";

  let ultimas = "(sin datos)";
  if (filas > 1) {
    const desde = Math.max(2, filas - 2);
    ultimas = hoja
      .getRange(desde, 1, filas - desde + 1, columnas)
      .getValues()
      .map((f) => f.join(" | "))
      .join("\\n");
  }

  SpreadsheetApp.getUi().alert(
    "Archivo: " +
      libro.getName() +
      "\\n" +
      libro.getUrl() +
      "\\n\\nPestañas: " +
      pestanas.join(", ") +
      "\\n\\nEl script escribe en la PESTAÑA: " +
      hoja.getName() +
      "\\n(la primera del archivo)\\n\\nEncabezados:\\n" +
      encabezados +
      "\\n\\nÚltimas filas:\\n" +
      ultimas
  );
}
'''

if "function revisarHoja()" not in t:
    t = t.rstrip() + "\n" + bloque
    print("  revisarHoja() agregada")

ruta.write_text(t, encoding="utf-8", newline="\n")

copia = RAIZ / "apps-script-check.js"
copia.write_text(t, encoding="utf-8")
r = subprocess.run(["node", "--check", str(copia)], capture_output=True, text=True)
print("  sintaxis:", "OK" if r.returncode == 0 else r.stderr[:300])
copia.unlink(missing_ok=True)
