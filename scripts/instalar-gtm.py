"""Instala Google Tag Manager (GTM-5CJH58QK) y eventos de conversión."""

import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
GTM_ID = "GTM-5CJH58QK"

# ------------------------------------------------------------- 1. render.mjs
render = RAIZ / "lib/render.mjs"
r = render.read_text(encoding="utf-8")

if "googletagmanager" not in r:
    gtm_head = """
    <!-- Google Tag Manager -->
    <script>
      (function (w, d, s, l, i) {
        w[l] = w[l] || [];
        w[l].push({ "gtm.start": new Date().getTime(), event: "gtm.js" });
        var f = d.getElementsByTagName(s)[0],
          j = d.createElement(s),
          dl = l != "dataLayer" ? "&l=" + l : "";
        j.async = true;
        j.src = "https://www.googletagmanager.com/gtm.js?id=" + i + dl;
        f.parentNode.insertBefore(j, f);
      })(window, document, "script", "dataLayer", "${GTM_ID}");
      window.dataLayer = window.dataLayer || [];
      function gtag() {
        dataLayer.push(arguments);
      }
      gtag("js", new Date());
    </script>
    <!-- End Google Tag Manager -->
"""

    r = r.replace('  <head>\n    <meta charset="utf-8" />', "  <head>\n" + gtm_head + '    <meta charset="utf-8" />')
    print("  GTM en <head>")

if "googletagmanager.com/ns.html" not in r:
    noscript = (
        '\n    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id='
        + GTM_ID
        + '" height="0" width="0" style="display:none;visibility:hidden" title="Google Tag Manager"></iframe></noscript>'
    )
    r = r.replace("<body${atributoModo}>", "<body${atributoModo}>" + noscript)
    print("  GTM noscript en <body>")

render.write_text(r, encoding="utf-8", newline="\n")

# ------------------------------------------------------------ 2. analytics.js
ana = RAIZ / "src/js/analytics.js"
a = ana.read_text(encoding="utf-8")

if "export function eventoGTM" not in a:
    a = a.replace(
        "/**\n * @param {string} evento",
        """/**
 * Envía un evento a Google Tag Manager (dataLayer) sin pasar por Meta Pixel.
 * Se usa para conversiones específicas del embudo.
 */
export function eventoGTM(nombre, parametros = {}) {
  empujarDataLayer(nombre, parametros);
  registrarEnConsola(`[gtm] ${nombre}`, parametros);
}

/**
 * @param {string} evento""",
    )
    ana.write_text(a, encoding="utf-8", newline="\n")
    print("  analytics.js: eventoGTM exportado")

# ---------------------------------------------------------- 3. formulario.js
form = RAIZ / "src/js/formulario.js"
f = form.read_text(encoding="utf-8")

if "eventoGTM" not in f:
    f = f.replace(
        'import { trackLead } from "./analytics.js";',
        'import { eventoGTM, trackLead } from "./analytics.js";',
    )

    # Clic en el botón de envío (después de validar)
    f = f.replace(
        "    const textoOriginal = boton?.innerHTML;",
        """    // Conversión GTM: clic en «Solicitar mi cotización»
    eventoGTM("cotizacion_click", {
      plan: limpio.plan,
      ubicacion: "formulario",
      pagina: window.location.pathname,
    });

    const textoOriginal = boton?.innerHTML;""",
    )

    # Registro confirmado por el servidor
    f = f.replace(
        "        trackLead({ folio, plan: limpio.plan });",
        """        trackLead({ folio, plan: limpio.plan });
        eventoGTM("generate_lead", {
          folio: folio,
          plan: limpio.plan,
          value: 1,
          currency: "MXN",
        });""",
    )
    form.write_text(f, encoding="utf-8", newline="\n")
    print("  formulario.js: eventos cotizacion_click y generate_lead")

# ------------------------------------------------------------ 4. reconstruir
for comando in (["node", "scripts/build-index-html.mjs"], ["node", "build.mjs"]):
    res = subprocess.run(comando, cwd=RAIZ, capture_output=True, text=True)
    print("  ", comando[-1], "->", "OK" if res.returncode == 0 else res.stderr[:300])

for archivo in ("src/js/formulario.js", "src/js/analytics.js"):
    res = subprocess.run(["node", "--check", archivo], cwd=RAIZ, capture_output=True, text=True)
    print(f"  {archivo}: {'OK' if res.returncode == 0 else res.stderr[:200]}")

html = (RAIZ / "index.html").read_text(encoding="utf-8")
print("  GTM en index.html:", GTM_ID in html)
print("  noscript GTM:", "ns.html?id=" + GTM_ID in html)
print("  evento generate_lead:", "generate_lead" in html)
