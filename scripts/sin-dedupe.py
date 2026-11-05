"""Permite registros repetidos: desactiva la deduplicación."""

import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ruta = RAIZ / "docs" / "google-apps-script.gs"
t = ruta.read_text(encoding="utf-8")

# 1) Configuración: sin ventana de deduplicación
t = t.replace(
    "  MINUTOS_DEDUPE: 10,",
    "  /** 0 = sin restricciones: la misma persona puede registrarse varias veces.\n"
    "   *  Si algún día quieres bloquear repetidos, pon 10 (minutos). */\n"
    "  MINUTOS_DEDUPE: 0,",
)

# 2) Solo ejecutar la comprobación si hay ventana
t = t.replace(
    "    // Deduplicación por celular (columna telefono)\n    if (filas > 1 && mapa.telefono) {",
    "    // Deduplicación por celular (solo si CONFIG.MINUTOS_DEDUPE > 0)\n    if (CONFIG.MINUTOS_DEDUPE > 0 && filas > 1 && mapa.telefono) {",
)

ruta.write_text(t, encoding="utf-8", newline="\n")

copia = RAIZ / "apps-script-check.js"
copia.write_text(t, encoding="utf-8")
r = subprocess.run(["node", "--check", str(copia)], capture_output=True, text=True)
print("  sintaxis:", "OK" if r.returncode == 0 else r.stderr[:300])
copia.unlink(missing_ok=True)

for linea in t.splitlines():
    if "MINUTOS_DEDUPE" in linea:
        print("  >", linea.strip()[:78])
