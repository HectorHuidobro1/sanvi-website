#!/usr/bin/env python3
"""check_site.py - validador SEO on-page de las paginas de Sanvi.

Uso:
    python tools/check_site.py sitio-sanvi
    python tools/check_site.py sitio-sanvi --content
    python tools/check_site.py sitio-sanvi --content --strict
    python tools/check_site.py sitio-sanvi/index.html

Sin dependencias externas: solo la biblioteca estandar de Python 3.

DOMINIO: SITE/CANONICAL estan DUPLICADOS a proposito en tools/check_site.py y
tools/check_links.py para que cada script sea standalone. Si el negocio compra
el dominio real hay que actualizarlos en AMBOS archivos.
"""

import argparse
import json
import os
import re
import sys

SITE = "https://www.sanvicalama.cl"

PAGES = ["index.html", "servicios.html", "nosotros.html", "contacto.html"]

CANONICAL = {
    "index.html": SITE + "/",
    "servicios.html": SITE + "/servicios.html",
    "nosotros.html": SITE + "/nosotros.html",
    "contacto.html": SITE + "/contacto.html",
}

# Minimo de palabras visibles dentro de <main>, por pagina.
#   index.html     = 700 -> valor duro del plan: la home debe superar en
#                           volumen de contenido util al competidor (Draska
#                           tiene ~250 palabras). No cambiar.
#   servicios.html = 650 -> 4 servicios en profundidad, ~160 palabras c/u.
#   nosotros.html  = 650 -> historia + bioseguridad + credenciales.
#   contacto.html  = 350 -> pagina corta y transaccional a proposito.
MIN_WORDS = {
    "index.html": 700,
    "servicios.html": 650,
    "nosotros.html": 650,
    "contacto.html": 350,
}

# Rangos aceptables para title y meta description (en caracteres).
TITLE_MIN, TITLE_MAX = 15, 70
DESC_MIN, DESC_MAX = 70, 180

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
DESC_RE = re.compile(r'<meta\b[^>]*\bname=["\']description["\'][^>]*>', re.I)
CONTENT_RE = re.compile(r'\bcontent=["\'](.*?)["\']', re.I | re.S)
CANON_RE = re.compile(r'<link\b[^>]*\brel=["\']canonical["\'][^>]*>', re.I)
HREF_RE = re.compile(r'\bhref=["\'](.*?)["\']', re.I)
H1_RE = re.compile(r"<h1[\s>]", re.I)
LD_OPEN_RE = re.compile(r'<script\b[^>]*\btype=["\']application/ld\+json["\'][^>]*>', re.I)
LD_BLOCK_RE = re.compile(
    r'<script\b[^>]*\btype=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.I | re.S
)
MAIN_RE = re.compile(r"<main[^>]*>(.*?)</main>", re.I | re.S)
SCRIPT_STYLE_RE = re.compile(r"<(script|style)\b[^>]*>.*?</\1>", re.I | re.S)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
TAG_RE = re.compile(r"<[^>]+>")
ENTITY_RE = re.compile(r"&(?:[a-zA-Z]+|#\d+);")

LD_LITERAL_OPEN = '<script type="application/ld+json">'


def read_text(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def visible_words(fragment):
    """Cuenta palabras visibles: quita script/style/comentarios/tags y colapsa espacios."""
    text = SCRIPT_STYLE_RE.sub(" ", fragment)
    text = COMMENT_RE.sub(" ", text)
    text = TAG_RE.sub(" ", text)
    text = ENTITY_RE.sub(" ", text)
    return len([word for word in text.split(" ") if word.strip()])


def check_page(path, want_content):
    """Devuelve (errores, avisos) para una pagina. Los mensajes ya vienen formateados."""
    name = os.path.basename(path)
    html = read_text(path)
    errors = []
    warns = []

    # --- title ---
    match = TITLE_RE.search(html)
    if not match:
        errors.append("ERROR %s: falta <title>" % name)
    else:
        title = " ".join(match.group(1).split())
        if not title:
            errors.append("ERROR %s: <title> vacio" % name)
        elif not (TITLE_MIN <= len(title) <= TITLE_MAX):
            errors.append(
                "ERROR %s: <title> de %d caracteres, fuera del rango %d-%d"
                % (name, len(title), TITLE_MIN, TITLE_MAX)
            )

    # --- meta description ---
    match = DESC_RE.search(html)
    if not match:
        errors.append('ERROR %s: falta <meta name="description">' % name)
    else:
        content = CONTENT_RE.search(match.group(0))
        desc = " ".join(content.group(1).split()) if content else ""
        if not desc:
            errors.append("ERROR %s: meta description vacia" % name)
        elif not (DESC_MIN <= len(desc) <= DESC_MAX):
            errors.append(
                "ERROR %s: meta description de %d caracteres, fuera del rango %d-%d"
                % (name, len(desc), DESC_MIN, DESC_MAX)
            )

    # --- canonical ---
    match = CANON_RE.search(html)
    if not match:
        errors.append('ERROR %s: falta <link rel="canonical">' % name)
    else:
        href = HREF_RE.search(match.group(0))
        got = href.group(1).strip() if href else ""
        want = CANONICAL.get(name)
        if want is None:
            warns.append("WARN %s: sin canonical de referencia en CANONICAL" % name)
        elif got != want:
            errors.append(
                "ERROR %s: canonical %s, esperada %s" % (name, got or "(vacia)", want)
            )

    # --- exactamente un h1 ---
    count_h1 = len(H1_RE.findall(html))
    if count_h1 != 1:
        errors.append("ERROR %s: %d <h1>, se espera exactamente 1" % (name, count_h1))

    # --- JSON-LD ---
    opens = LD_OPEN_RE.findall(html)
    if not opens:
        warns.append("WARN %s: sin bloque JSON-LD" % name)
    elif len(opens) > 1:
        errors.append("ERROR %s: mas de un bloque JSON-LD" % name)
    else:
        if opens[0] != LD_LITERAL_OPEN:
            errors.append("ERROR %s: apertura de script JSON-LD no es literal" % name)
        blocks = LD_BLOCK_RE.findall(html)
        if not blocks:
            errors.append("ERROR %s: bloque JSON-LD sin cierre </script>" % name)
        else:
            try:
                json.loads(blocks[0])
            except ValueError as exc:
                errors.append("ERROR %s: JSON-LD invalido: %s" % (name, exc))

    # --- contenido dentro de <main> ---
    if want_content:
        main_match = MAIN_RE.search(html)
        if not main_match:
            errors.append("ERROR %s: falta <main>" % name)
        else:
            words = visible_words(main_match.group(1))
            minimum = MIN_WORDS.get(name)
            if minimum is not None and words < minimum:
                errors.append(
                    "ERROR %s: %d palabras visibles, minimo %d" % (name, words, minimum)
                )

    return errors, warns


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Valida SEO on-page de las paginas de Sanvi."
    )
    parser.add_argument("path", help="archivo .html o carpeta con las 4 paginas")
    parser.add_argument(
        "--content",
        action="store_true",
        help="ademas exige el minimo de palabras visibles dentro de <main>",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="trata los avisos (WARN) como fallo para el codigo de salida",
    )
    args = parser.parse_args(argv)

    if os.path.isdir(args.path):
        targets = [os.path.join(args.path, page) for page in PAGES]
        missing = [t for t in targets if not os.path.isfile(t)]
        if missing:
            for target in missing:
                print("ERROR %s: archivo no encontrado" % os.path.basename(target))
            return 1
        multi = True
    elif os.path.isfile(args.path):
        targets = [args.path]
        multi = False
    else:
        print("ERROR: ruta no encontrada: %s" % args.path)
        return 1

    total_errors = 0
    total_warns = 0
    for target in targets:
        errors, warns = check_page(target, args.content)
        for warn in warns:
            print(warn)
        for error in errors:
            print(error)
        total_errors += len(errors)
        total_warns += len(warns)

    failed = total_errors > 0 or (args.strict and total_warns > 0)

    if not failed:
        if multi:
            if total_warns:
                print(
                    "OK: 0 errores, %d aviso(s) en %d pagina(s)."
                    % (total_warns, len(targets))
                )
            else:
                print("OK: 0 errores en %d pagina(s)." % len(targets))
        else:
            print("OK: 0 errores")
        return 0

    if total_errors == 0 and args.strict:
        print("ERROR: %d aviso(s) tratados como error por --strict" % total_warns)
    return 1


if __name__ == "__main__":
    sys.exit(main())
