#!/usr/bin/env python3
"""shoot.py - captura una URL o un HTML local a PNG con Chrome/Edge headless.

Uso:
    python tools/shoot.py <url-o-archivo.html> --out <ruta.png> --width W --height H

Sin dependencias externas: solo la biblioteca estandar de Python 3 mas un
navegador Chromium ya instalado en la maquina (Chrome o Edge). Se usa para dos
cosas: (a) generar los rasters de marca desde tools/og/*.html y (b) revisar
visualmente el sitio a distintos anchos durante la implementacion.

Si el navegador no esta en una ruta tipica, exportar CHROME_PATH con la ruta
completa al ejecutable.
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Rutas relativas de los ejecutables dentro de los directorios raiz de Windows.
# Orden intencionado: Chrome antes que Edge.
WINDOWS_RELATIVE = (
    r"Google\Chrome\Application\chrome.exe",
    r"Microsoft\Edge\Application\msedge.exe",
)

PATH_NAMES = ("google-chrome", "chromium", "chromium-browser", "msedge", "chrome")


def find_browser():
    """Devuelve la ruta del navegador o None si no hay ninguno."""
    env = os.environ.get("CHROME_PATH")
    if env and Path(env).is_file():
        return env

    roots = [
        os.environ.get("ProgramFiles", r"C:\Program Files"),
        os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
        os.environ.get("LOCALAPPDATA", ""),
    ]
    for relative in WINDOWS_RELATIVE:
        for root in roots:
            if not root:
                continue
            candidate = Path(root) / relative
            if candidate.is_file():
                return str(candidate)

    for name in PATH_NAMES:
        found = shutil.which(name)
        if found:
            return found

    return None


def to_url(target):
    """http(s)/file se pasan tal cual; cualquier otra cosa es una ruta local."""
    if target.startswith(("http://", "https://", "file://")):
        return target
    return Path(target).resolve().as_uri()


def main():
    parser = argparse.ArgumentParser(
        description="Captura una pagina a PNG con Chrome o Edge en modo headless."
    )
    parser.add_argument("target", help="URL http(s) o ruta a un archivo .html local")
    parser.add_argument("--out", required=True, help="ruta del PNG de salida")
    parser.add_argument("--width", type=int, default=1280, help="ancho del viewport")
    parser.add_argument("--height", type=int, default=900, help="alto del viewport")
    parser.add_argument(
        "--wait",
        type=int,
        default=3000,
        help="ms de tiempo virtual antes de disparar la captura (fuentes web)",
    )
    args = parser.parse_args()

    browser = find_browser()
    if browser is None:
        print("ERROR: no se encontro Chrome ni Edge instalado (define CHROME_PATH)")
        return 1

    out = Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    # Si quedo un PNG de una corrida anterior, borrarlo: de lo contrario una
    # captura fallida se reportaria como exitosa.
    if out.exists():
        out.unlink()

    # Perfil temporal: sin esto, si el usuario tiene Chrome abierto, la
    # instancia headless choca con el perfil por defecto y no captura nada.
    profile = tempfile.mkdtemp(prefix="sanvi-shoot-")

    cmd = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--force-device-scale-factor=1",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-extensions",
        "--user-data-dir=" + profile,
        "--virtual-time-budget=%d" % args.wait,
        "--window-size=%d,%d" % (args.width, args.height),
        "--screenshot=" + str(out),
        to_url(args.target),
    ]

    result = None
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        print("ERROR: el navegador no respondio en 120 s")
        return 1
    finally:
        shutil.rmtree(profile, ignore_errors=True)

    if not out.is_file():
        print("ERROR: no se genero %s" % out)
        detail = ((result.stderr or "") + (result.stdout or "")).strip().splitlines()
        for line in detail[-5:]:
            print("       " + line)
        return 1

    print("OK: capturado %s (%dx%d)" % (out, args.width, args.height))
    return 0


if __name__ == "__main__":
    sys.exit(main())
