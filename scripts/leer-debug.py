"""Imprime el bloque de diagnóstico del volcado DOM."""

import html
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
texto = (RAIZ / "debug-dom.html").read_text(encoding="utf-8", errors="replace")
coincidencia = re.search(r'<pre id="diagnostico">(.*?)</pre>', texto, re.S)
if not coincidencia:
    print("sin diagnóstico")
else:
    print(html.unescape(coincidencia.group(1)))
