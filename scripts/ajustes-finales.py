"""Ajustes puntuales de texto y robustez (UTF-8 seguro).

Los mensajes de consola son ASCII a propósito: la consola de Windows usa
cp1252 y no puede imprimir ciertos símbolos.
"""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def aplicar(relativa: str, reemplazos: list[tuple[str, str]]) -> None:
    ruta = RAIZ / relativa
    original = ruta.read_text(encoding="utf-8")
    texto = original
    cambios = 0
    for viejo, nuevo in reemplazos:
        if viejo not in texto:
            print(f"  [omitido] {relativa}: patron no encontrado ({len(viejo)} chars)")
            continue
        texto = texto.replace(viejo, nuevo)
        cambios += 1
    if texto != original:
        ruta.write_text(texto, encoding="utf-8", newline="\n")
    print(f"  {relativa}: {cambios} cambio(s)")


# 1) Banner y logs ASCII en el servidor
ruta = RAIZ / "server.mjs"
texto = ruta.read_text(encoding="utf-8")
if "Chevrolet Silverado - landing" not in texto:
    lineas = texto.split("\n")
    salida = []
    for linea in lineas:
        despojada = linea.strip()
        if despojada.startswith('console.log("  ┌') or despojada.startswith('console.log("  └'):
            continue
        if despojada.startswith('console.log("  │'):
            salida.append('  console.log("   Chevrolet Silverado - landing para ferreterias (revision)");')
            continue
        salida.append(linea)
    texto = "\n".join(salida).replace(
        "console.log(`[lead] prospecto registrado ${registro.folio} · ${registro.datos.ciudad} · ${registro.datos.sucursales}`);",
        "console.log(`[lead] prospecto registrado ${registro.folio} - ${registro.datos.ciudad} - ${registro.datos.sucursales}`);",
    )
    ruta.write_text(texto, encoding="utf-8", newline="\n")
    print("  server.mjs: banner en ASCII")
else:
    print("  server.mjs: ya aplicado")

# 2) Copy redundante en la franja de confianza del hero
aplicar(
    "src/sections/01-hero.html",
    [("Asesoría personalizada de un asesor", "Asesoría personalizada")],
)

# 3) Aviso de cifras de referencia en la ficha técnica
aplicar(
    "src/js/ui.js",
    [
        (
            "  const html = especificaciones.items\n"
            "    .map(\n"
            "      (item) => `<div class=\"spec\">\n"
            "        <dt class=\"spec__label\">${escapar(item.etiqueta)}</dt>\n"
            "        <dd class=\"spec__value\">\n"
            "          <strong>${escapar(item.valor)}</strong>\n"
            "          ${item.nota ? `<span class=\"spec__nota\">${escapar(item.nota)}</span>` : \"\"}\n"
            "        </dd>\n"
            "      </div>`\n"
            "    )\n"
            "    .join(\"\");",
            "  const etiquetaEstado = especificaciones.verificado\n"
            "    ? \"\"\n"
            "    : '<span class=\"spec__estado\">Referencia oficial por confirmar</span>';\n"
            "\n"
            "  const html = especificaciones.items\n"
            "    .map(\n"
            "      (item) => `<div class=\"spec\">\n"
            "        <dt class=\"spec__label\">${escapar(item.etiqueta)}</dt>\n"
            "        <dd class=\"spec__value\">\n"
            "          <strong>${escapar(item.valor)}</strong>\n"
            "          ${etiquetaEstado}\n"
            "          ${item.nota ? `<span class=\"spec__nota\">${escapar(item.nota)}</span>` : \"\"}\n"
            "        </dd>\n"
            "      </div>`\n"
            "    )\n"
            "    .join(\"\");",
        )
    ],
)

# 4) Estilo del aviso de referencia
ruta = RAIZ / "src/styles/showcase.css"
texto = ruta.read_text(encoding="utf-8")
if "spec__estado" not in texto:
    texto += """
[data-specs-silverado] .spec__estado {
  font-family: var(--font-display);
  font-size: 0.58rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--gold-deep);
  opacity: 0.85;
}
"""
    ruta.write_text(texto, encoding="utf-8", newline="\n")
    print("  showcase.css: estilo de referencia")
else:
    print("  showcase.css: ya aplicado")
