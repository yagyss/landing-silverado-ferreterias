from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
for nombre in ["src/sections/01-hero.html", "src/js/analytics.js", "api/cotizacion.mjs", "src/styles/hero.css"]:
    ruta = RAIZ / nombre
    texto = ruta.read_text(encoding="utf-8", errors="replace")
    raros = {}
    for i, ch in enumerate(texto):
        if ord(ch) > 127 or ord(ch) < 32 and ch not in "\n\r\t":
            raros.setdefault(ch, [0, i])[0] += 1
    print(f"\n== {nombre} ==")
    for ch, (cuenta, pos) in sorted(raros.items(), key=lambda kv: -kv[1][0]):
        print(f"   U+{ord(ch):04X} {ch!r} x{cuenta}  ctx: {texto[max(0,pos-30):pos+30]!r}")
