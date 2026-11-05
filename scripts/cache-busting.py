"""Marca módulos JS y CSS con versión para romper la caché del navegador."""

import re
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
build = RAIZ / "build.mjs"
t = build.read_text(encoding="utf-8")

marca = "VERSION_ASSETS"

if marca not in t:
    bloque = '''
  // Rompe la caché del navegador: los módulos JS y el CSS cambian con cada
  // despliegue, así nadie queda ejecutando una versión anterior del formulario.
  const VERSION_ASSETS = process.env.ASSET_VERSION || String(Date.now()).slice(0, 10);
  {
    const dirs = [resolve(DIST, "src", "js"), resolve(DIST, "src", "data")];
    for (const dir of dirs) {
      let archivos = [];
      try {
        archivos = await readdir(dir);
      } catch {
        continue;
      }
      for (const archivo of archivos) {
        if (!archivo.endsWith(".js") && !archivo.endsWith(".mjs")) continue;
        const rutaJs = resolve(dir, archivo);
        let js = await readFile(rutaJs, "utf8");
        js = js.replace(
          /(from\\s*["'])(\\.{1,2}\\/[^"']+\\.(?:js|mjs))(["'])/g,
          `$1$2?v=${VERSION_ASSETS}$3`,
        );
        js = js.replace(
          /(import\\s*["'])(\\.{1,2}\\/[^"']+\\.(?:js|mjs))(["'])/g,
          `$1$2?v=${VERSION_ASSETS}$3`,
        );
        await writeFile(rutaJs, js, "utf8");
      }
    }
    // Los CSS que importan a otros también se versionan
    const estilos = resolve(DIST, "src", "styles");
    try {
      for (const archivo of await readdir(estilos)) {
        if (!archivo.endsWith(".css")) continue;
        const rutaCss = resolve(estilos, archivo);
        let css = await readFile(rutaCss, "utf8");
        css = css.replace(/@import\\s+url\\((["'])([^"']+\\.css)\\1\\)/g, `@import url($1$2?v=${VERSION_ASSETS}$1)`);
        await writeFile(rutaCss, css, "utf8");
      }
    } catch {
      /* sin hojas que importar */
    }
  }
'''

    # Insertar antes del mensaje final de compilación
    ancla = "  const kb = (Buffer.byteLength(html, \"utf8\") / 1024).toFixed(1);"
    if ancla in t:
        t = t.replace(ancla, bloque + "\n" + ancla)
        build.write_text(t, encoding="utf-8", newline="\n")
        print("  build.mjs versiona módulos JS y CSS")
    else:
        print("  (no se encontró el ancla de compilación)")
else:
    print("  ya estaba versionado")

r = subprocess.run(["node", "build.mjs"], cwd=RAIZ, capture_output=True, text=True)
print("  build:", "OK" if r.returncode == 0 else r.stderr[:400])

# Verificación
dist = RAIZ / "dist"
html = (dist / "index.html").read_text(encoding="utf-8")
main_js = (dist / "src" / "js" / "main.js").read_text(encoding="utf-8")

print("  index referencia main.js con versión:", bool(re.search(r"main\.js\?v=", html)))
print("  main.js versiona sus imports:", "?v=" in main_js)
