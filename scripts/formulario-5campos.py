"""Ajustes del esquema del formulario en la configuración y el backend."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- site.js
ruta = RAIZ / "src/data/site.js"
t = ruta.read_text(encoding="utf-8")

if "plan: [" not in t:
    t = t.replace(
        "    opciones: {\n      ciudad: [",
        '    opciones: {\n      plan: ["Contado", "Financiamiento", "Quiero conocer las opciones"],\n      ciudad: [',
        1,
    )

t = t.replace(
    '      correo: { etiqueta: "Correo electrónico (opcional)", requerido: false, placeholder: "nombre@correo.com" },',
    '      correo: { etiqueta: "Correo electrónico", requerido: true, placeholder: "nombre@correo.com" },\n'
    '      plan: { etiqueta: "Plan", requerido: true },\n'
    '      mensaje: { etiqueta: "Mensaje", requerido: false },',
)

t = t.replace(
    '      whatsapp: {\n        etiqueta: "Número de WhatsApp",',
    '      whatsapp: {\n        etiqueta: "Celular",',
)

ruta.write_text(t, encoding="utf-8", newline="\n")
print("  site.js: plan/mensaje agregados")

# ------------------------------------------------------------ api handler
ruta = RAIZ / "api/cotizacion.mjs"
t = ruta.read_text(encoding="utf-8")

if "plan: limpio.plan" not in t:
    t = t.replace(
        "      sucursales: limpio.sucursales,\n      usoVehiculo: limpio.usoVehiculo,\n      interes: limpio.interes,",
        "      plan: limpio.plan,\n      mensaje: limpio.mensaje,\n"
        "      // Campos heredados (pueden venir vacíos)\n"
        "      sucursales: limpio.sucursales,\n      usoVehiculo: limpio.usoVehiculo,\n      interes: limpio.interes,",
    )
    ruta.write_text(t, encoding="utf-8", newline="\n")
    print("  api: plan/mensaje guardados")
else:
    print("  api: ya tenía plan")

# ------------------------------------------------------------ Apps Script
ruta = RAIZ / "docs/google-apps-script.gs"
t = ruta.read_text(encoding="utf-8")

if '"Plan"' not in t:
    t = t.replace(
        '  "Uso de vehículo",',
        '  "Plan",\n  "Uso de vehículo",',
    )
    t = t.replace(
        '  "Estado",\n];',
        '  "Mensaje",\n  "Estado",\n];',
    )
    t = t.replace(
        '      limpiar_(datos.usoVehiculo, 60) || (express ? "Por definir (express)" : ""),',
        '      limpiar_(datos.plan, 40),\n'
        '      limpiar_(datos.usoVehiculo, 60) || (express ? "Por definir (express)" : ""),',
    )
    t = t.replace(
        '      limpiar_(datos.pagina, 300),\n      "Nuevo",',
        '      limpiar_(datos.pagina, 300),\n      limpiar_(datos.mensaje, 600),\n      "Nuevo",',
    )
    ruta.write_text(t, encoding="utf-8", newline="\n")
    print("  Apps Script: columnas Plan y Mensaje")

# --------------------------------------------------------------- textarea
css = RAIZ / "src/styles/apple.css"
texto = css.read_text(encoding="utf-8")

bloque = """
/* Campo de mensaje del formulario */
.form__textarea {
  min-height: 118px;
  resize: vertical;
  line-height: 1.55;
  padding-top: 0.7rem;
}
"""

if "Campo de mensaje" not in texto:
    css.write_text(texto.rstrip() + "\n" + bloque, encoding="utf-8", newline="\n")
    print("  estilo de textarea")

# ------------------------------------------------------------- verificaciones
import subprocess  # noqa: E402

for archivo in ("src/js/formulario.js", "src/js/validation.mjs", "src/data/site.js"):
    resultado = subprocess.run(["node", "--check", archivo], cwd=RAIZ, capture_output=True, text=True)
    estado = "OK" if resultado.returncode == 0 else "ERROR"
    print(f"  {archivo}: {estado}")
    if resultado.returncode != 0:
        print(resultado.stderr[:400])
