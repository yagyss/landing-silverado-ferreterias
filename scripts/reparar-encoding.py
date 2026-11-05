"""
Detecta y repara archivos de texto que quedaron con doble codificación
(mojibake: "Ã¡", "Ã©", "Â¿"...) por ediciones hechas desde PowerShell.

Estrategia: si el archivo contiene secuencias típicas de UTF-8 leído como
Latin-1, se revierte con texto.encode("latin-1").decode("utf-8").
Se reporta cada archivo reparado; si la reversión no es válida, NO se toca.
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
EXTENSIONES = {".html", ".css", ".js", ".mjs", ".json", ".md", ".txt", ".svg"}
CARPETAS = ["src", "lib", "api", "assets", "docs", "scripts", "data"]
# Señales inequívocas de UTF-8 interpretado como Latin-1/Windows-1252
SEÑALES = ("Ã¡", "Ã©", "Ã­", "Ã³", "Ãº", "Ã±", "Ã‘", "Â¿", "Â¡", "Ã", "Â")


def archivos() -> list[Path]:
    vistos: list[Path] = []
    for carpeta in CARPETAS:
        base = RAIZ / carpeta
        if not base.exists():
            continue
        for ruta in base.rglob("*"):
            if ruta.is_file() and ruta.suffix.lower() in EXTENSIONES:
                vistos.append(ruta)
    for nombre in ["index.html", "README.md", "package.json", "robots.txt"]:
        ruta = RAIZ / nombre
        if ruta.is_file():
            vistos.append(ruta)
    return vistos


def reparar(ruta: Path, aplicar: bool) -> bool:
    original = ruta.read_text(encoding="utf-8", errors="replace")
    if not any(señal in original for señal in SEÑALES):
        return False

    # PowerShell 5.1 añade BOM al guardar; hay que quitarlo antes de revertir.
    limpio = original.replace("\ufeff", "")
    recuperado = None
    for codec in ("latin-1", "cp1252"):
        try:
            candidato = limpio.encode(codec).decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            continue
        recuperado = candidato
        break

    if recuperado is None:
        print(f"  NO REPARABLE (revisar a mano): {ruta.relative_to(RAIZ)}")
        return False

    if aplicar:
        ruta.write_text(recuperado, encoding="utf-8", newline="\n")
    return True


def main() -> int:
    aplicar = "--aplicar" in sys.argv
    tocados = []
    for ruta in archivos():
        if reparar(ruta, aplicar):
            tocados.append(ruta.relative_to(RAIZ))

    print(f"  Archivos con mojibake: {len(tocados)}")
    for ruta in tocados:
        print(f"   - {ruta}")
    if tocados and not aplicar:
        print("\n  Ejecuta con --aplicar para repararlos.")
    if tocados and aplicar:
        print("\n  Reparados y guardados en UTF-8.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
