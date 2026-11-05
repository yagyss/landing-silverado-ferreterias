"""Conecta la URL real del Apps Script y reconstruye el sitio."""

import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
URL = "https://script.google.com/macros/s/AKfycbwj3hEDWUEcZa94a1ZThZHK4lWbJW7CsmGysRbXUayBrJcTV-MNWNHSd6BcZCZigBua/exec"

config = RAIZ / "netlify.toml"
t = config.read_text(encoding="utf-8")

# Reemplaza el destino del proxy por la implementación real
inicio = t.find('from = "/api/cotizacion"')
if inicio == -1:
    raise SystemExit("No se encontró la regla del proxy en netlify.toml")

fin = t.find("[[redirects]]", inicio)
if fin == -1:
    fin = len(t)
bloque = t[inicio:fin]

nuevo_bloque = (
    'from = "/api/cotizacion"\n'
    f'to = "{URL}"\n'
    "status = 200\n"
    "force = true\n\n"
)

config.write_text(t[:inicio] + nuevo_bloque + t[fin:], encoding="utf-8", newline="\n")
print("  netlify.toml: proxy apuntando a Apps Script")

# Guarda también la URL en un archivo de referencia para el cliente
(RAIZ / "docs" / "ENDPOINT.txt").write_text(
    "Endpoint de recepción de leads (Google Apps Script)\n\n"
    f"URL /exec: {URL}\n\n"
    "Proxy configurado en netlify.toml:\n"
    "  /api/cotizacion  →  esta URL (status 200)\n\n"
    "Si cambias de implementación, actualiza ambos archivos.\n",
    encoding="utf-8",
)

# Reconstrucción
for comando in (["node", "scripts/build-index-html.mjs"], ["node", "build.mjs"]):
    r = subprocess.run(comando, cwd=RAIZ, capture_output=True, text=True)
    print("  ", comando[-1], "->", "OK" if r.returncode == 0 else r.stderr[:200])

print("  netlify.toml en dist:", (RAIZ / "dist" / "netlify.toml").exists())
print("  destino correcto:", URL in (RAIZ / "dist" / "netlify.toml").read_text(encoding="utf-8"))
