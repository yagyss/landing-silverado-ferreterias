"""Mejora el autocompletado del formulario con los datos de cada persona."""

import re
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
seccion = RAIZ / "src/sections/11-cotizacion.html"
t = seccion.read_text(encoding="utf-8")

# --- Nombre: nombre completo, primera letra en mayúscula, sin corrección ---
t = t.replace(
    '''                name="nombre"
                type="text"
                autocomplete="name"
                placeholder="Ej. Juan Pérez"
                required''',
    '''                name="nombre"
                type="text"
                autocomplete="name"
                autocapitalize="words"
                spellcheck="false"
                enterkeyhint="next"
                placeholder="Ej. Juan Pérez"
                required''',
)

# --- Celular: token estándar "tel" para que el navegador lo autocomplete ---
t = t.replace(
    '''                name="whatsapp"
                type="tel"
                inputmode="numeric"
                autocomplete="tel-national"
                placeholder="55 1234 5678"
                required''',
    '''                name="whatsapp"
                type="tel"
                inputmode="tel"
                autocomplete="tel"
                enterkeyhint="next"
                placeholder="55 1234 5678"
                required''',
)

# --- Correo ---
t = t.replace(
    '''                name="correo"
                type="email"
                autocomplete="email"
                placeholder="nombre@correo.com"
                required''',
    '''                name="correo"
                type="email"
                autocomplete="email"
                autocapitalize="off"
                spellcheck="false"
                enterkeyhint="next"
                placeholder="nombre@correo.com"
                required''',
)

# --- Plan y mensaje no deben autocompletarse con basura ---
t = t.replace(
    '<select class="form__input form__select" id="campo-plan" name="plan" required>',
    '<select class="form__input form__select" id="campo-plan" name="plan" autocomplete="off" required>',
)
t = t.replace(
    '''              name="mensaje"
              rows="4"''',
    '''              name="mensaje"
              autocomplete="off"
              rows="4"''',
)

# --- El formulario declara autocompletado y la sección relacionada ---
t = t.replace(
    '<form class="form" data-form-cotizacion novalidate autocomplete="on">',
    '<form class="form" data-form-cotizacion novalidate autocomplete="on" aria-describedby="form-ayuda">',
)

# --- Nota visible: se puede usar el autocompletado del navegador ---
if "form-ayuda" not in t.split("<form")[0] or True:
    if 'id="form-ayuda"' not in t:
        t = t.replace(
            '<p class="cotiza__card-sub">Campos marcados con <span aria-hidden="true">*</span> son obligatorios.</p>',
            '<p class="cotiza__card-sub">Campos marcados con <span aria-hidden="true">*</span> son obligatorios.</p>\n'
            '          <p class="cotiza__card-sub" id="form-ayuda">Puedes llenarlo más rápido con el autocompletado de tu navegador.</p>',
        )

seccion.write_text(t, encoding="utf-8", newline="\n")
print("  atributos de autocompletado aplicados")

# --- Verificación de tokens ---
tokens = {
    "name": t.count('autocomplete="name"'),
    "tel": t.count('autocomplete="tel"'),
    "email": t.count('autocomplete="email"'),
    "form on": t.count('autocomplete="on"'),
}
print("  tokens:", tokens)

for comando in (["node", "scripts/build-index-html.mjs"], ["node", "build.mjs"]):
    r = subprocess.run(comando, cwd=RAIZ, capture_output=True, text=True)
    print("  ", comando[-1], "->", "OK" if r.returncode == 0 else r.stderr[:200])

html = (RAIZ / "index.html").read_text(encoding="utf-8")
print("  autocomplete=tel en index:", 'autocomplete="tel"' in html)
print("  tel-national restante:", 'tel-national' in html)
