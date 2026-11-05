"""Prepara el build para publicar en una subcarpeta (GitHub Pages)."""

import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- build.mjs
build = RAIZ / "build.mjs"
t = build.read_text(encoding="utf-8")

if "RELATIVE_PATHS" not in t:
    t = t.replace(
        "  const html = await renderDocumento({ modo: \"build\" });\n  await writeFile(resolve(DIST, \"index.html\"), html, \"utf8\");",
        """  let html = await renderDocumento({ modo: "build" });

  // GitHub Pages sirve el sitio en /<repo>/: las rutas absolutas (/assets/…)
  // apuntarían a la raíz del dominio, así que se vuelven relativas.
  if (process.env.RELATIVE_PATHS === "1") {
    html = html
      .replaceAll('href="/', 'href="')
      .replaceAll('src="/', 'src="')
      .replaceAll('srcset="/', 'srcset="')
      .replaceAll(', /assets/', ', assets/')
      .replaceAll(' /assets/', ' assets/')
      .replaceAll('"/assets/', '"assets/')
      .replaceAll('"/src/', '"src/');
  }

  await writeFile(resolve(DIST, "index.html"), html, "utf8");""",
    )
    build.write_text(t, encoding="utf-8", newline="\n")
    print("  build.mjs con rutas relativas opcionales")

# ------------------------------------------------------------- workflow
wf = RAIZ / ".github" / "workflows" / "deploy.yml"
w = wf.read_text(encoding="utf-8")

if "RELATIVE_PATHS" not in w:
    w = w.replace(
        "      - name: Compilar sitio\n        run: node build.mjs",
        "      - name: Compilar sitio\n        run: node build.mjs\n        env:\n          RELATIVE_PATHS: \"1\"",
    )
    wf.write_text(w, encoding="utf-8", newline="\n")
    print("  workflow con RELATIVE_PATHS=1")

# ---------------------------------------------------- probar build relativo
r = subprocess.run(
    ["node", "build.mjs"],
    cwd=RAIZ,
    capture_output=True,
    text=True,
    env={**__import__("os").environ, "RELATIVE_PATHS": "1"},
)
print("  build relativo:", "OK" if r.returncode == 0 else r.stderr[:300])

html = (RAIZ / "dist" / "index.html").read_text(encoding="utf-8")
import re

absolutas = re.findall(r'(?:href|src)="(/[^"]+)"', html)
print("  rutas absolutas restantes:", len(absolutas), absolutas[:3])

# Reconstruye el build normal (para Netlify / archivo local)
subprocess.run(["node", "build.mjs"], cwd=RAIZ, check=False)
subprocess.run(["node", "scripts/build-index-html.mjs"], cwd=RAIZ, check=False)
print("  build normal restaurado")
