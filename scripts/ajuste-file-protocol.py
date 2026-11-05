"""Ajustes para que la página funcione (y sea honesta) abierta como archivo."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# 1) Evita colisión de nombres al concatenar los módulos
ruta = RAIZ / "src/js/express.js"
t = ruta.read_text(encoding="utf-8")
t = t.replace('const MENSAJE_RED =', 'const MENSAJE_RED_EXPRESS =')
t = t.replace('mostrarEstado(cuerpo.mensaje ?? MENSAJE_RED);', 'mostrarEstado(cuerpo.mensaje ?? MENSAJE_RED_EXPRESS);')
t = t.replace('mostrarEstado(MENSAJE_RED);', 'mostrarEstado(MENSAJE_RED_EXPRESS);')

# 2) Aviso honesto cuando se abre con file:// (no hay servidor para registrar)
guardia = """    if (window.location.protocol === "file:") {
      mostrarEstado(
        "Vista de revisión: para enviar la solicitud abre la página con el servidor local (node server.mjs) o conéctala a tu CRM.",
        "error",
      );
      return;
    }

"""
if "Vista de revisión: para enviar" not in t:
    t = t.replace("    try {\n      const respuesta = await fetch(", guardia + "    try {\n      const respuesta = await fetch(")

ruta.write_text(t, encoding="utf-8", newline="\n")
print("  express.js ajustado")

# 3) Misma guardia en el formulario completo
ruta = RAIZ / "src/js/formulario.js"
t = ruta.read_text(encoding="utf-8")
if "Vista de revisión: para enviar" not in t:
    t = t.replace(
        "    try {\n      const respuesta = await fetch(SITE.formulario.endpoint, {",
        guardia + "    try {\n      const respuesta = await fetch(SITE.formulario.endpoint, {",
    )
    ruta.write_text(t, encoding="utf-8", newline="\n")
    print("  formulario.js ajustado")
else:
    print("  formulario.js ya ajustado")
