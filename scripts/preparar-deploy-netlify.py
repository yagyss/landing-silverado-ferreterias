"""Genera _redirects para que el proxy funcione también en deploys manuales."""

import re
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

build = RAIZ / "build.mjs"
t = build.read_text(encoding="utf-8")

if "_redirects" not in t:
    t = t.replace(
        '  const kb = (Buffer.byteLength(html, "utf8") / 1024).toFixed(1);',
        '''  // Deploys manuales (arrastrar carpeta) no leen netlify.toml: se copia la
  // regla del proxy a _redirects para garantizar /api/cotizacion.
  const toml = await readFile(resolve(RAIZ, "netlify.toml"), "utf8");
  const destino = toml.match(/from = "\\/api\\/cotizacion"\\s*\\n\\s*to = "([^"]+)"/);
  if (destino) {
    await writeFile(
      resolve(DIST, "_redirects"),
      `/api/cotizacion  ${destino[1]}  200\\n`,
      "utf8",
    );
  }

  const kb = (Buffer.byteLength(html, "utf8") / 1024).toFixed(1);''',
    )
    # importa readFile
    if "readFile" not in t.split("const RAIZ")[0]:
        t = t.replace(
            'import { cp, mkdir, rm, writeFile } from "node:fs/promises";',
            'import { cp, mkdir, readFile, rm, writeFile } from "node:fs/promises";',
        )
    build.write_text(t, encoding="utf-8", newline="\n")
    print("  build.mjs genera _redirects")
else:
    print("  build.mjs ya lo genera")

r = subprocess.run(["node", "build.mjs"], cwd=RAIZ, capture_output=True, text=True)
print("  build:", "OK" if r.returncode == 0 else r.stderr[:300])

redir = RAIZ / "dist" / "_redirects"
print("  _redirects:", redir.read_text(encoding="utf-8").strip() if redir.exists() else "FALTA")

# Reempaquetar
import zipfile

zip_path = RAIZ / "landing-dist.zip"
if zip_path.exists():
    zip_path.unlink()

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for archivo in (RAIZ / "dist").rglob("*"):
        if archivo.is_file():
            z.write(archivo, archivo.relative_to(RAIZ / "dist"))
print(f"  paquete: {zip_path.stat().st_size/1024/1024:.2f} MB")
