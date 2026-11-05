"""Actualiza proxy y cliente con la URL de Apps Script que ya funciona."""

import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
VIEJA = "AKfycbwj3hEDWUEcZa94a1ZThZHK4lWbJW7CsmGysRbXUayBrJcTV-MNWNHSd6BcZCZigBua"
NUEVA = "AKfycbyo3rlLi4VGjD7-Kz-OsWSViRAPOasfpyCG6DornXqCwzOT_aXb1W-WtlM7znlLCAI-"

archivos = ["netlify.toml", "src/data/site.js", "docs/ENDPOINT.txt", "docs/GOOGLE-SHEETS.md"]

for archivo in archivos:
    ruta = RAIZ / archivo
    if not ruta.exists():
        print(f"  (omito {archivo}: no existe)")
        continue
    texto = ruta.read_text(encoding="utf-8")
    original = texto
    texto = texto.replace(VIEJA, NUEVA)
    # También reemplaza cualquier URL genérica de ejemplo
    texto = texto.replace("REEMPLAZA_ESTO", NUEVA)
    if texto != original:
        ruta.write_text(texto, encoding="utf-8", newline="\n")
        print(f"  {archivo}: URL actualizada")
    else:
        print(f"  {archivo}: sin cambios")

# Asegura que el endpoint remoto exista con la URL nueva
site = RAIZ / "src/data/site.js"
s = site.read_text(encoding="utf-8")
if NUEVA not in s:
    s = s.replace(
        '    endpoint: "/api/cotizacion",',
        f'    endpoint: "/api/cotizacion",\n    endpointRemoto:\n      "https://script.google.com/macros/s/{NUEVA}/exec",',
    )
    site.write_text(s, encoding="utf-8", newline="\n")
    print("  site.js: endpointRemoto agregado")

# Reconstrucción
for comando in (["node", "scripts/build-index-html.mjs"], ["node", "build.mjs"]):
    r = subprocess.run(comando, cwd=RAIZ, capture_output=True, text=True)
    print("  ", comando[-1], "->", "OK" if r.returncode == 0 else r.stderr[:200])

# Comprobaciones
toml = (RAIZ / "netlify.toml").read_text(encoding="utf-8")
index = (RAIZ / "index.html").read_text(encoding="utf-8")
print("  proxy en netlify.toml:", NUEVA in toml)
print("  URL en index.html:", NUEVA in index)
print("  netlify.toml en dist:", NUEVA in (RAIZ / "dist" / "netlify.toml").read_text(encoding="utf-8"))

# Commit
subprocess.run(["git", "add", "-A"], cwd=RAIZ, check=False)
r = subprocess.run(
    ["git", "commit", "-m", "Conecta el formulario con la implementacion activa de Google Apps Script"],
    cwd=RAIZ,
    capture_output=True,
    text=True,
)
print("  commit:", "OK" if r.returncode == 0 else r.stdout[:200])
