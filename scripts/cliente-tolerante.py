"""Hace que el formulario acepte respuestas de Apps Script de otros formatos."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ruta = RAIZ / "src/js/formulario.js"
t = ruta.read_text(encoding="utf-8")

viejo = """      if (!respuesta.ok || cuerpo.ok !== true) {
        mostrarEstado(cuerpo.mensaje ?? MENSAJE_RED);
        return;
      }

      const folio = cuerpo.folio ?? "";"""

nuevo = """      // Algunos despliegues de Apps Script responden {result:"success"} en
      // lugar de {ok:true, folio}. Se aceptan ambos formatos para no bloquear
      // el registro en la hoja.
      const exitoConfirmado =
        respuesta.ok &&
        (cuerpo.ok === true || cuerpo.success === true || cuerpo.result === "success");

      if (!exitoConfirmado) {
        mostrarEstado(cuerpo.mensaje ?? MENSAJE_RED);
        return;
      }

      const folio = cuerpo.folio ?? "";"""

if "exitoConfirmado" not in t:
    t = t.replace(viejo, nuevo)
    ruta.write_text(t, encoding="utf-8", newline="\n")
    print("  formulario.js tolerante a {result:success}")
else:
    print("  ya aplicado")

import subprocess  # noqa: E402

for comando in (["node", "scripts/build-index-html.mjs"], ["node", "build.mjs"]):
    r = subprocess.run(comando, cwd=RAIZ, capture_output=True, text=True)
    print("  ", comando[-1], "->", "OK" if r.returncode == 0 else r.stderr[:200])

r = subprocess.run(["node", "--check", "src/js/formulario.js"], cwd=RAIZ, capture_output=True, text=True)
print("  formulario.js:", "OK" if r.returncode == 0 else r.stderr[:200])
