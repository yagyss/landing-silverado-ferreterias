"""Extrae el bundle embebido de index.html para validarlo y diagnosticar."""

import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
html = (RAIZ / "index.html").read_text(encoding="utf-8")

coincidencia = None
for coincidencia in re.finditer(r"<script>(.*?)</script>", html, re.S):
    pass
if not coincidencia:
    raise SystemExit("No se encontró el script embebido")

codigo = coincidencia.group(1)
(RAIZ / "bundle-check.js").write_text(codigo, encoding="utf-8")

restos = [linea for linea in codigo.splitlines() if re.match(r"^\s*(import|export)\s", linea)]
print(f"  bundle: {len(codigo)} caracteres")
print(f"  líneas import/export restantes: {len(restos)}")
for linea in restos[:10]:
    print("   ", linea[:110])

imgs = re.findall(r'(?:src|srcset)="([^"]+)"', html)
print("  primeras rutas de imagen:")
for ruta in imgs[:5]:
    print("   ", ruta[:110])

# Comprueba que las rutas relativas existan realmente en disco
faltantes = []
for ruta in imgs:
    primera = ruta.split()[0].split(",")[0]
    if primera.startswith(("http", "data:")):
        continue
    if not (RAIZ / primera).exists():
        faltantes.append(primera)
print(f"  rutas de imagen inexistentes: {len(faltantes)}")
for ruta in faltantes[:8]:
    print("   falta:", ruta[:110])
