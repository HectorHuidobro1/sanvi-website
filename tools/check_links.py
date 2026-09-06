#!/usr/bin/env python3
"""check_links.py - verifica enlaces internos, anclas y assets de sitio-sanvi.

Uso:
    python tools/check_links.py sitio-sanvi

Sin dependencias externas: solo la biblioteca estandar de Python 3.

DOMINIO: SITE/CANONICAL estan DUPLICADOS a proposito en tools/check_site.py y
tools/check_links.py para que cada script sea standalone. Si el negocio compra
el dominio real hay que actualizarlos en AMBOS archivos.
"""

import os
import re
import sys
import xml.etree.ElementTree as ET

SITE = "https://www.sanvicalama.cl"

PAGES = ["index.html", "servicios.html", "nosotros.html", "contacto.html"]

CANONICAL = {
    "index.html": SITE + "/",
    "servicios.html": SITE + "/servicios.html",
    "nosotros.html": SITE + "/nosotros.html",
    "contacto.html": SITE + "/contacto.html",
}

EXTERNAL_PREFIXES = ("http://", "https://", "//", "mailto:", "tel:", "javascript:", "data:")

A_TAG_RE = re.compile(r"<a\b[^>]*>", re.I)
LINK_TAG_RE = re.compile(r"<link\b[^>]*>", re.I)
SCRIPT_TAG_RE = re.compile(r"<script\b[^>]*>", re.I)
IMG_TAG_RE = re.compile(r"<img\b[^>]*>", re.I)
HREF_RE = re.compile(r'\bhref=["\']([^"\']*)["\']', re.I)
SRC_RE = re.compile(r'\bsrc=["\']([^"\']*)["\']', re.I)
ID_RE = re.compile(r'\bid=["\']([^"\']+)["\']', re.I)


def read_text(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def refs_of(html):
    """href de <a>/<link> y src de <script>/<img>, en orden de aparicion."""
    found = []
    for tag in A_TAG_RE.findall(html) + LINK_TAG_RE.findall(html):
        match = HREF_RE.search(tag)
        if match:
            found.append(match.group(1).strip())
    for tag in SCRIPT_TAG_RE.findall(html) + IMG_TAG_RE.findall(html):
        match = SRC_RE.search(tag)
        if match:
            found.append(match.group(1).strip())
    return found


def ids_of(html):
    return set(ID_RE.findall(html))


def main(argv):
    if len(argv) != 1:
        print("Uso: python tools/check_links.py <carpeta-del-sitio>")
        return 1

    root = argv[0]
    if not os.path.isdir(root):
        print("ERROR: carpeta no encontrada: %s" % root)
        return 1

    errors = []
    warns = []
    notes = []

    pages_html = {}
    for page in PAGES:
        full = os.path.join(root, page)
        if not os.path.isfile(full):
            errors.append("ERROR: falta la pagina %s" % page)
            continue
        pages_html[page] = read_text(full)

    pages_ids = {page: ids_of(html) for page, html in pages_html.items()}

    for page in PAGES:
        html = pages_html.get(page)
        if html is None:
            continue
        for ref in refs_of(html):
            if not ref or ref == "#" or ref.startswith(EXTERNAL_PREFIXES):
                continue
            target, _, fragment = ref.partition("#")

            if not target:
                # Ancla dentro de la misma pagina, p.ej. href="#main".
                if fragment and fragment not in pages_ids[page]:
                    errors.append(
                        "ERROR: ancla #%s no existe en %s" % (fragment, page)
                    )
                continue

            asset = os.path.normpath(os.path.join(root, target))
            if not os.path.isfile(asset):
                errors.append(
                    "ERROR: %s referencia %s y ese archivo no existe" % (page, target)
                )
                continue

            if fragment:
                target_name = os.path.basename(target)
                if target_name in pages_ids:
                    if fragment not in pages_ids[target_name]:
                        errors.append(
                            "ERROR: ancla #%s no existe en %s" % (fragment, target_name)
                        )
                else:
                    warns.append(
                        "WARN: no se verifico el ancla #%s en %s" % (fragment, target)
                    )

    # --- sitemap.xml ---
    sitemap_path = os.path.join(root, "sitemap.xml")
    if not os.path.isfile(sitemap_path):
        warns.append("WARN: falta sitemap.xml")
    else:
        try:
            tree = ET.parse(sitemap_path)
        except ET.ParseError as exc:
            errors.append("ERROR: sitemap.xml no es XML valido: %s" % exc)
        else:
            notes.append("sitemap.xml: XML valido")
            locs = []
            for element in tree.getroot().iter():
                tag = element.tag.split("}")[-1]
                if tag == "loc" and element.text:
                    locs.append(element.text.strip())
            if sorted(locs) != sorted(CANONICAL.values()):
                errors.append(
                    "ERROR: sitemap.xml no contiene exactamente las 4 URLs canonicas"
                )

    # --- robots.txt ---
    robots_path = os.path.join(root, "robots.txt")
    if not os.path.isfile(robots_path):
        warns.append("WARN: falta robots.txt")
    else:
        robots = read_text(robots_path)
        if not any(line.strip().startswith("Sitemap:") for line in robots.splitlines()):
            errors.append("ERROR: robots.txt sin linea Sitemap:")

    for note in notes:
        print(note)
    for warn in warns:
        print(warn)
    for error in errors:
        print(error)

    if errors:
        return 1

    print("OK: todos los enlaces internos, anclas y assets resuelven.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
