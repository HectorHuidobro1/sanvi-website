#!/usr/bin/env python3
"""
check_perf.py - Heuristicas offline de Core Web Vitals para el sitio Sanvi.

No mide CWV reales (eso requiere URL publica). Verifica las causas conocidas de
LCP/CLS/INP malos que si se pueden comprobar en los archivos.

Uso:
    python tools/check_perf.py sitio-sanvi
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

PAGES = ("index.html", "servicios.html", "nosotros.html", "contacto.html")

MAX_PAGE_KB = 400        # HTML + CSS + JS + imagenes referenciadas
MAX_HTML_KB = 90
MAX_BLOCKING_CSS = 3     # tokens/base, components, pages


def local_assets(src: str) -> set[str]:
    out: set[str] = set()
    for attr in ("href", "src"):
        for ref in re.findall(r'(?is)<[a-z]+\b[^>]*\b' + attr + r'\s*=\s*["\']([^"\']+)["\']', src):
            if ref.startswith(("http", "mailto:", "tel:", "data:", "#")):
                continue
            path = ref.split("#", 1)[0].split("?", 1)[0]
            if path and not path.endswith(".html"):
                out.add(path)
    return out


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "sitio-sanvi").resolve()
    errors: list[str] = []

    for name in PAGES:
        page = root / name
        if not page.is_file():
            errors.append(f"ERROR  falta {name}")
            continue
        src = page.read_text(encoding="utf-8")

        html_kb = page.stat().st_size / 1024
        if html_kb > MAX_HTML_KB:
            errors.append(f"ERROR  {name}: HTML de {html_kb:.0f} KB, maximo {MAX_HTML_KB} KB")

        total = page.stat().st_size
        missing: list[str] = []
        for rel in sorted(local_assets(src)):
            asset = (root / rel).resolve()
            if asset.is_file():
                total += asset.stat().st_size
            else:
                missing.append(rel)
        for rel in missing:
            errors.append(f"ERROR  {name}: asset referenciado inexistente {rel}")
        total_kb = total / 1024
        if total_kb > MAX_PAGE_KB:
            errors.append(f"ERROR  {name}: peso total {total_kb:.0f} KB, maximo {MAX_PAGE_KB} KB")

        head = src.split("</head>", 1)[0]
        blocking = len(re.findall(r'(?is)<link\b[^>]*rel\s*=\s*["\']stylesheet["\'][^>]*>', head))
        local_blocking = len(re.findall(
            r'(?is)<link\b[^>]*rel\s*=\s*["\']stylesheet["\'][^>]*href\s*=\s*["\'](?!http)', head))
        if local_blocking > MAX_BLOCKING_CSS:
            errors.append(f"ERROR  {name}: {local_blocking} hojas locales bloqueantes, maximo {MAX_BLOCKING_CSS}")

        if "fonts.googleapis.com" in head:
            if 'rel="preconnect" href="https://fonts.gstatic.com"' not in head:
                errors.append(f"ERROR  {name}: usa Google Fonts sin preconnect a fonts.gstatic.com")
            if "display=swap" not in head:
                errors.append(f"ERROR  {name}: la peticion de Google Fonts no lleva display=swap")

        for tag in re.findall(r"(?is)<script\b[^>]*\bsrc\s*=[^>]*>", src):
            if not re.search(r"(?i)\b(defer|async)\b", tag):
                errors.append(f"ERROR  {name}: script sin defer/async: {tag[:80]}")

        body = src.split("</head>", 1)[-1]
        imgs = re.findall(r"(?is)<img\b[^>]*>", body)
        for i, tag in enumerate(imgs):
            has_dims = all(re.search(r'(?i)\b' + a + r'\s*=\s*["\']?\d', tag) for a in ("width", "height"))
            if not has_dims:
                errors.append(f"ERROR  {name}: <img> sin width/height (riesgo de CLS): {tag[:80]}")
            lazy = 'loading="lazy"' in tag
            if i == 0 and lazy:
                errors.append(f"ERROR  {name}: la primera imagen no debe ser lazy (dana el LCP)")
            if i > 0 and not lazy:
                errors.append(f"ERROR  {name}: imagen bajo el fold sin loading=lazy: {tag[:80]}")

        print(f"INFO   {name}: HTML {html_kb:.0f} KB · pagina {total_kb:.0f} KB · "
              f"{blocking} hojas de estilo · {len(imgs)} imagenes en body")

    for line in errors:
        print(line)
    if errors:
        print(f"\nFALLO: {len(errors)} problema(s) de rendimiento.")
        return 1
    print("\nOK: heuristicas de rendimiento superadas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
