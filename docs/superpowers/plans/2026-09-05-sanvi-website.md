# Sanvi — Sitio Web Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construir y publicar un sitio estatico de 4 paginas para Sanvi (enfermeria e inyecciones a domicilio en Calama) que supere en contenido, precios visibles, datos estructurados y Core Web Vitals al competidor Draska, listo para desplegar en Netlify/Vercel/Cloudflare Pages.

**Architecture:** HTML plano por pagina (sin build step, sin framework, sin bundler) + tres hojas de estilo en cascada por responsabilidad (`base.css` = tokens/reset/utilidades, `components.css` = header/footer/botones/cards reutilizables, `pages.css` = secciones especificas de cada pagina) + un unico `site.js` diferido para menu movil, FAQ acordeon y validacion del formulario. La verificacion es un par de scripts Python 3 de stdlib (`tools/check_site.py`, `tools/check_links.py`) que actuan como suite de tests del sitio: se corren despues de cada tarea y su salida exacta es el criterio de aceptacion de cada paso.

**Tech Stack:** HTML5 semantico, CSS3 (custom properties, `clamp()`, grid/flex, `:focus-visible`), JavaScript vanilla ES2020 (sin dependencias), Google Fonts (Sora + Inter con `font-display: swap`), JSON-LD schema.org (`MedicalBusiness`), Python 3 stdlib para los validadores, git para control de versiones.

## Global Constraints

- Sitio estatico HTML/CSS/JS puro, **sin framework, sin build step, sin gestor de paquetes**: los archivos que se escriben son los que se publican.
- Carpeta raiz del sitio: `sitio-sanvi/` dentro de `C:\Users\PC\Desktop\claude\Paginas web con SEO\`. Los scripts de verificacion viven en `tools/` en la raiz del proyecto (fuera de `sitio-sanvi/`, no se publican).
- Dominio placeholder: `https://www.sanvicalama.cl` — se usa en canonicals, `og:url`, `sitemap.xml`, `robots.txt` y JSON-LD hasta que el negocio compre el dominio real. Esta centralizado en la constante `SITE` de ambos scripts de `tools/` para poder cambiarlo de una sola pasada.
- Paleta turquesa `#0F9B8E` / `#14B8A6` / `#2DD4BF` + coral `#FF6B57` como acento de accion; fondo `#F4FBFA`; texto `#0B2A3A`.
- Tipografias: `Sora` para titulares, `Inter` para cuerpo, via Google Fonts con `display=swap`.
- Telefono/WhatsApp: `+56 9 7883 3741`. Numero E.164 sin `+` para enlaces `wa.me`: `56978833741`.
- Horario: `8:00–21:00`, todos los dias, **con agendamiento previo** (no walk-in). Nunca prometer atencion inmediata.
- Cobertura: **solo Calama**. No mencionar otras comunas ni "todo el norte".
- 4 paginas exactas: `index.html`, `servicios.html`, `nosotros.html`, `contacto.html`. No se agregan paginas ni blog.
- Precios visibles y consistentes en todo el sitio (CLP): inyeccion intramuscular **$10.000**, inyeccion intravenosa **$17.000**, curacion simple **$15.000**, curacion compleja **$33.000**.
- Idioma: `lang="es-CL"`, copy en espanol de Chile, sin emojis en el HTML publicado.
- Errores del competidor que NO se replican: `AggregateRating` sin resenas reales, `sameAs` con Place ID crudo, codigo postal invalido, CSS inline masivo, paginas de prueba en el sitemap.

---

### Task 1: Estructura base, tokens de diseno y esqueleto de las 4 paginas

**Files:**
- Create: `sitio-sanvi/assets/css/base.css`
- Create: `sitio-sanvi/assets/css/components.css` (stub vacio — la Tarea 2 escribe su contenido real)
- Create: `sitio-sanvi/assets/css/pages.css` (stub vacio — la Tarea 3 escribe su contenido real)
- Create: `sitio-sanvi/assets/js/site.js` (stub vacio — la Tarea 2 escribe su contenido real)
- Create: `sitio-sanvi/assets/img/favicon.svg`
- Create: `sitio-sanvi/index.html`
- Create: `sitio-sanvi/servicios.html`
- Create: `sitio-sanvi/nosotros.html`
- Create: `sitio-sanvi/contacto.html`
- Create: `tools/check_site.py`
- Create: `tools/check_links.py`
- Create: `.gitignore`

> **Nota sobre los stubs:** `components.css`, `pages.css` y `site.js` se crean en esta tarea como archivos con un solo comentario. Motivo: `tools/check_links.py` valida que **todo** asset referenciado exista en disco, y las 4 paginas ya los referencian desde su `<head>`/`<body>`. Sin los stubs, la verificacion de esta tarea daria 3 errores por pagina. Las Tareas 2 y 3 **sobrescriben** estos archivos con su contenido real; no hay conflicto.

**Interfaces:**

*Produces — variables CSS en `:root` de `sitio-sanvi/assets/css/base.css` (nombres congelados, las Tareas 2–9 las consumen literalmente):*

- Espaciado: `--sp-2` `--sp-3` `--sp-4` `--sp-5` `--sp-6` `--sp-7` `--sp-8` `--sp-9`
- Tipografia (tamanos): `--fs-100` `--fs-200` `--fs-300` `--fs-400` `--fs-500` `--fs-600` `--fs-700` `--fs-800` `--fs-900`
- Tipografia (familias): `--font-display` (Sora), `--font-body` (Inter)
- Color: `--c-teal-050` `--c-teal-100` `--c-teal-300` `--c-teal-400` `--c-teal-500` `--c-teal-900` `--c-coral-500` `--c-coral-600` `--c-surface` `--c-line` `--c-ink` `--c-muted`
- Radios: `--r-md` `--r-lg` `--r-pill`
- Sombra: `--shadow-sm`
- Gradientes: `--grad-soft` `--grad-teal`
- Layout: `--section-y` `--container-max`

*Produces — clases utilitarias en `base.css` (el header/footer de la Tarea 2 las usa verbatim):*

- `.container` — ancho maximo `--container-max` centrado, con padding horizontal responsive.
- `.skip-link` — enlace de salto, oculto fuera de pantalla hasta `:focus`. Marcado obligatorio y literal, como **primer hijo de `<body>`** en las 4 paginas: `<a class="skip-link" href="#main">Saltar al contenido</a>`
- `.sr-only` — visualmente oculto, accesible para lectores de pantalla.

*Produces — contratos de marcado consumidos por tareas posteriores:*

- Cada pagina contiene exactamente los comentarios `<!-- HEADER_PLACEHOLDER -->` y `<!-- FOOTER_PLACEHOLDER -->` (la Tarea 2 busca esas cadenas exactas y las reemplaza por el `<header>` y `<footer>` reales).
- Cada pagina contiene `<main id="main">` (destino del skip-link; `check_site.py --content` cuenta palabras dentro de ese elemento).
- El `<head>` de cada pagina queda **definitivo** en esta tarea y no se vuelve a tocar. Los bloques JSON-LD de tareas posteriores se insertan en el `<body>`; `check_site.py` los busca en todo el documento.

*Produces — contratos de `tools/check_site.py`:*

- `SITE = "https://www.sanvicalama.cl"`
- `PAGES = ["index.html", "servicios.html", "nosotros.html", "contacto.html"]`
- `CANONICAL` — dict `pagina -> URL canonica completa`
- `MIN_WORDS` — dict `pagina -> minimo de palabras visibles en <main>`; `MIN_WORDS["index.html"] == 700` (valor duro).
- Mensajes de salida literales: `WARN <archivo>: sin bloque JSON-LD`, `ERROR <archivo>: JSON-LD invalido: <detalle>`, `ERROR <archivo>: mas de un bloque JSON-LD`, `ERROR <archivo>: apertura de script JSON-LD no es literal`, `ERROR <archivo>: N palabras visibles, minimo M`, `OK: 0 errores`, `OK: 0 errores, N aviso(s) en 4 pagina(s).`, `OK: 0 errores en 4 pagina(s).`
- Codigo de salida: `0` sin errores, `1` con errores.

*Produces — contratos de `tools/check_links.py`:*

- `SITE` y `CANONICAL` duplicados (mismo contenido que en `check_site.py`).
- Mensajes literales: `ERROR: ancla #<id> no existe en <pagina>`, `WARN: falta sitemap.xml`, `WARN: falta robots.txt`, `sitemap.xml: XML valido`, `ERROR: sitemap.xml no contiene exactamente las 4 URLs canonicas`, `ERROR: robots.txt sin linea Sitemap:`, `OK: todos los enlaces internos, anclas y assets resuelven.`
- Codigo de salida: `0` sin errores, `1` con errores.

---

- [ ] **Step 1: Crear la estructura de carpetas y los stubs de assets**

Desde `C:\Users\PC\Desktop\claude\Paginas web con SEO`:

```powershell
New-Item -ItemType Directory -Force "sitio-sanvi\assets\css"
New-Item -ItemType Directory -Force "sitio-sanvi\assets\js"
New-Item -ItemType Directory -Force "sitio-sanvi\assets\img"
New-Item -ItemType Directory -Force "tools"
```

Crear `sitio-sanvi/assets/css/components.css` con exactamente:

```css
/* components.css — header, footer, botones y cards. Se escribe en la Tarea 2. */
```

Crear `sitio-sanvi/assets/css/pages.css` con exactamente:

```css
/* pages.css — secciones especificas de cada pagina. Se escribe en la Tarea 3. */
```

Crear `sitio-sanvi/assets/js/site.js` con exactamente:

```js
/* site.js — menu movil, FAQ acordeon y formulario. Se escribe en la Tarea 2. */
```

Crear `sitio-sanvi/assets/img/favicon.svg` con exactamente (usa los mismos tres stops que `--grad-teal`):

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="Sanvi">
  <defs>
    <linearGradient id="sanviTeal" x1="0" y1="0" x2="64" y2="64" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#0F9B8E"/>
      <stop offset="0.5" stop-color="#14B8A6"/>
      <stop offset="1" stop-color="#2DD4BF"/>
    </linearGradient>
  </defs>
  <rect width="64" height="64" rx="16" fill="url(#sanviTeal)"/>
  <path d="M27 15h10v12h12v10H37v12H27V37H15V27h12z" fill="#FFFFFF"/>
</svg>
```

---

- [ ] **Step 2: Escribir `sitio-sanvi/assets/css/base.css` completo**

```css
/* ==========================================================================
   base.css — Sanvi
   Tokens de diseno, reset, tipografia base, foco visible y utilidades.
   Se carga PRIMERO en las 4 paginas. No contiene componentes ni layout de
   secciones (eso vive en components.css y pages.css).
   ========================================================================== */

/* --------------------------------------------------------------------------
   1. Tokens
   -------------------------------------------------------------------------- */
:root {
  /* Espaciado — escala base 4px */
  --sp-2: 0.25rem;   /*  4px */
  --sp-3: 0.5rem;    /*  8px */
  --sp-4: 0.75rem;   /* 12px */
  --sp-5: 1rem;      /* 16px */
  --sp-6: 1.5rem;    /* 24px */
  --sp-7: 2rem;      /* 32px */
  --sp-8: 3rem;      /* 48px */
  --sp-9: 4.5rem;    /* 72px */

  /* Tipografia — tamanos (fluidos desde --fs-600 hacia arriba) */
  --fs-100: 0.75rem;
  --fs-200: 0.8125rem;
  --fs-300: 0.9375rem;
  --fs-400: 1rem;
  --fs-500: 1.125rem;
  --fs-600: clamp(1.25rem, 1.10rem + 0.60vw, 1.50rem);
  --fs-700: clamp(1.50rem, 1.25rem + 1.10vw, 2.00rem);
  --fs-800: clamp(2.00rem, 1.60rem + 1.80vw, 2.75rem);
  --fs-900: clamp(2.25rem, 1.70rem + 2.60vw, 3.50rem);

  /* Tipografia — familias */
  --font-display: "Sora", "Segoe UI", system-ui, -apple-system, sans-serif;
  --font-body: "Inter", "Segoe UI", system-ui, -apple-system, sans-serif;

  /* Color — turquesa (base de marca) */
  --c-teal-050: #F4FBFA;
  --c-teal-100: #DDF5F1;
  --c-teal-300: #2DD4BF;
  --c-teal-400: #14B8A6;
  --c-teal-500: #0F9B8E;
  --c-teal-900: #0B3B37;

  /* Color — coral (acento de accion, solo CTA) */
  --c-coral-500: #FF6B57;
  --c-coral-600: #E5533F;

  /* Color — superficies y texto */
  --c-surface: #FFFFFF;
  --c-line: #DCE7E6;
  --c-ink: #0B2A3A;
  --c-muted: #4A6B78;

  /* Radios */
  --r-md: 10px;
  --r-lg: 18px;
  --r-pill: 999px;

  /* Sombra */
  --shadow-sm: 0 1px 2px rgba(11, 42, 58, 0.06), 0 6px 18px rgba(11, 42, 58, 0.06);

  /* Gradientes */
  --grad-soft: linear-gradient(180deg, #F4FBFA 0%, #FFFFFF 55%, #EAF7F5 100%);
  --grad-teal: linear-gradient(135deg, #0F9B8E 0%, #14B8A6 50%, #2DD4BF 100%);

  /* Layout */
  --container-max: 1120px;
  --section-y: clamp(3rem, 2rem + 4vw, 5.5rem);
}

/* --------------------------------------------------------------------------
   2. Reset / normalize
   -------------------------------------------------------------------------- */
*,
*::before,
*::after { box-sizing: border-box; }

html {
  -webkit-text-size-adjust: 100%;
  scroll-behavior: smooth;
  scroll-padding-top: 5rem;
}

body,
h1, h2, h3, h4, h5, h6,
p, figure, blockquote, dl, dd,
ul, ol { margin: 0; }

ul[class],
ol[class] {
  list-style: none;
  padding: 0;
}

img,
picture,
svg,
video {
  display: block;
  max-width: 100%;
  height: auto;
}

input,
button,
textarea,
select {
  font: inherit;
  color: inherit;
}

button { cursor: pointer; }

table {
  border-collapse: collapse;
  width: 100%;
}

@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}

/* --------------------------------------------------------------------------
   3. Tipografia base
   -------------------------------------------------------------------------- */
body {
  font-family: var(--font-body);
  font-size: var(--fs-400);
  line-height: 1.65;
  color: var(--c-ink);
  background-color: var(--c-teal-050);
  background-image: var(--grad-soft);
  background-attachment: fixed;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}

h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-display);
  font-weight: 700;
  line-height: 1.15;
  letter-spacing: -0.015em;
  color: var(--c-ink);
  text-wrap: balance;
}

h1 { font-size: var(--fs-900); }
h2 { font-size: var(--fs-800); }
h3 { font-size: var(--fs-700); }
h4 { font-size: var(--fs-600); }
h5 { font-size: var(--fs-500); }
h6 { font-size: var(--fs-400); }

p { text-wrap: pretty; }

p + p { margin-top: var(--sp-5); }

small { font-size: var(--fs-200); }

strong { font-weight: 600; }

/* --------------------------------------------------------------------------
   4. Enlaces
   -------------------------------------------------------------------------- */
a {
  color: var(--c-teal-500);
  text-decoration-thickness: 1px;
  text-underline-offset: 0.18em;
  transition: color 0.15s ease;
}

a:hover { color: var(--c-teal-900); }

/* --------------------------------------------------------------------------
   5. Foco visible — anillo turquesa
   -------------------------------------------------------------------------- */
:focus-visible {
  outline: 3px solid var(--c-teal-500);
  outline-offset: 2px;
  border-radius: var(--r-md);
}

/* --------------------------------------------------------------------------
   6. Utilidades
   -------------------------------------------------------------------------- */
.container {
  width: 100%;
  max-width: var(--container-max);
  margin-inline: auto;
  padding-inline: var(--sp-5);
}

@media (min-width: 40em) {
  .container { padding-inline: var(--sp-6); }
}

@media (min-width: 64em) {
  .container { padding-inline: var(--sp-7); }
}

.skip-link {
  position: absolute;
  left: var(--sp-5);
  top: var(--sp-5);
  z-index: 999;
  transform: translateY(-200%);
  padding: var(--sp-4) var(--sp-6);
  background: var(--c-surface);
  color: var(--c-ink);
  font-family: var(--font-display);
  font-weight: 600;
  font-size: var(--fs-300);
  text-decoration: none;
  border: 2px solid var(--c-teal-500);
  border-radius: var(--r-pill);
  box-shadow: var(--shadow-sm);
  transition: transform 0.15s ease;
}

.skip-link:focus {
  transform: translateY(0);
}

.sr-only {
  position: absolute !important;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

---

- [ ] **Step 3: Escribir `sitio-sanvi/index.html` completo**

```html
<!DOCTYPE html>
<html lang="es-CL">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Sanvi | Enfermeria e inyecciones a domicilio en Calama</title>
  <meta name="description" content="Enfermeria e inyecciones a domicilio en Calama. Intramuscular $10.000, intravenosa $17.000 y curaciones. Atencion de 8:00 a 21:00 con hora agendada.">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta name="theme-color" content="#0F9B8E">
  <link rel="canonical" href="https://www.sanvicalama.cl/">

  <meta property="og:type" content="website">
  <meta property="og:locale" content="es_CL">
  <meta property="og:site_name" content="Sanvi">
  <meta property="og:url" content="https://www.sanvicalama.cl/">
  <meta property="og:title" content="Sanvi | Enfermeria e inyecciones a domicilio en Calama">
  <meta property="og:description" content="Enfermeria e inyecciones a domicilio en Calama. Intramuscular $10.000, intravenosa $17.000 y curaciones. Atencion de 8:00 a 21:00 con hora agendada.">
  <meta property="og:image" content="https://www.sanvicalama.cl/assets/img/og-sanvi.png">
  <meta name="twitter:card" content="summary_large_image">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Sora:wght@600;700&display=swap">

  <link rel="stylesheet" href="assets/css/base.css">
  <link rel="stylesheet" href="assets/css/components.css">
  <link rel="stylesheet" href="assets/css/pages.css">
  <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
</head>
<body>
<a class="skip-link" href="#main">Saltar al contenido</a>
<!-- HEADER_PLACEHOLDER -->
<main id="main">
  <h1>Enfermeria e inyecciones a domicilio en Calama</h1>
  <p>Contenido pendiente.</p>
</main>
<!-- FOOTER_PLACEHOLDER -->
<script src="assets/js/site.js" defer></script>
</body>
</html>
```

---

- [ ] **Step 4: Escribir `sitio-sanvi/servicios.html` completo**

```html
<!DOCTYPE html>
<html lang="es-CL">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Servicios y precios de enfermeria a domicilio en Calama | Sanvi</title>
  <meta name="description" content="Precios y detalles de nuestros servicios: inyeccion intramuscular $10.000, intravenosa $17.000, curacion simple $15.000 y compleja $33.000 en Calama.">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta name="theme-color" content="#0F9B8E">
  <link rel="canonical" href="https://www.sanvicalama.cl/servicios.html">

  <meta property="og:type" content="website">
  <meta property="og:locale" content="es_CL">
  <meta property="og:site_name" content="Sanvi">
  <meta property="og:url" content="https://www.sanvicalama.cl/servicios.html">
  <meta property="og:title" content="Servicios y precios de enfermeria a domicilio en Calama | Sanvi">
  <meta property="og:description" content="Precios y detalles de nuestros servicios: inyeccion intramuscular $10.000, intravenosa $17.000, curacion simple $15.000 y compleja $33.000 en Calama.">
  <meta property="og:image" content="https://www.sanvicalama.cl/assets/img/og-sanvi.png">
  <meta name="twitter:card" content="summary_large_image">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Sora:wght@600;700&display=swap">

  <link rel="stylesheet" href="assets/css/base.css">
  <link rel="stylesheet" href="assets/css/components.css">
  <link rel="stylesheet" href="assets/css/pages.css">
  <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
</head>
<body>
<a class="skip-link" href="#main">Saltar al contenido</a>
<!-- HEADER_PLACEHOLDER -->
<main id="main">
  <h1>Servicios y precios de enfermeria a domicilio</h1>
  <p>Contenido pendiente.</p>
</main>
<!-- FOOTER_PLACEHOLDER -->
<script src="assets/js/site.js" defer></script>
</body>
</html>
```

---

- [ ] **Step 5: Escribir `sitio-sanvi/nosotros.html` completo**

```html
<!DOCTYPE html>
<html lang="es-CL">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Sobre Sanvi | Equipo de enfermeria a domicilio en Calama</title>
  <meta name="description" content="Conoce al equipo de Sanvi: tecnicos en enfermeria de nivel superior, protocolo de bioseguridad y atencion a domicilio en Calama con hora agendada.">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta name="theme-color" content="#0F9B8E">
  <link rel="canonical" href="https://www.sanvicalama.cl/nosotros.html">

  <meta property="og:type" content="website">
  <meta property="og:locale" content="es_CL">
  <meta property="og:site_name" content="Sanvi">
  <meta property="og:url" content="https://www.sanvicalama.cl/nosotros.html">
  <meta property="og:title" content="Sobre Sanvi | Equipo de enfermeria a domicilio en Calama">
  <meta property="og:description" content="Conoce al equipo de Sanvi: tecnicos en enfermeria de nivel superior, protocolo de bioseguridad y atencion a domicilio en Calama con hora agendada.">
  <meta property="og:image" content="https://www.sanvicalama.cl/assets/img/og-sanvi.png">
  <meta name="twitter:card" content="summary_large_image">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Sora:wght@600;700&display=swap">

  <link rel="stylesheet" href="assets/css/base.css">
  <link rel="stylesheet" href="assets/css/components.css">
  <link rel="stylesheet" href="assets/css/pages.css">
  <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
</head>
<body>
<a class="skip-link" href="#main">Saltar al contenido</a>
<!-- HEADER_PLACEHOLDER -->
<main id="main">
  <h1>Quienes somos</h1>
  <p>Contenido pendiente.</p>
</main>
<!-- FOOTER_PLACEHOLDER -->
<script src="assets/js/site.js" defer></script>
</body>
</html>
```

---

- [ ] **Step 6: Escribir `sitio-sanvi/contacto.html` completo**

```html
<!DOCTYPE html>
<html lang="es-CL">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Contacto y agendamiento | Sanvi enfermeria a domicilio Calama</title>
  <meta name="description" content="Agenda tu visita de enfermeria a domicilio en Calama por WhatsApp al +56 9 7883 3741. Atendemos todos los dias de 8:00 a 21:00 con hora previa.">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta name="theme-color" content="#0F9B8E">
  <link rel="canonical" href="https://www.sanvicalama.cl/contacto.html">

  <meta property="og:type" content="website">
  <meta property="og:locale" content="es_CL">
  <meta property="og:site_name" content="Sanvi">
  <meta property="og:url" content="https://www.sanvicalama.cl/contacto.html">
  <meta property="og:title" content="Contacto y agendamiento | Sanvi enfermeria a domicilio Calama">
  <meta property="og:description" content="Agenda tu visita de enfermeria a domicilio en Calama por WhatsApp al +56 9 7883 3741. Atendemos todos los dias de 8:00 a 21:00 con hora previa.">
  <meta property="og:image" content="https://www.sanvicalama.cl/assets/img/og-sanvi.png">
  <meta name="twitter:card" content="summary_large_image">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Sora:wght@600;700&display=swap">

  <link rel="stylesheet" href="assets/css/base.css">
  <link rel="stylesheet" href="assets/css/components.css">
  <link rel="stylesheet" href="assets/css/pages.css">
  <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
</head>
<body>
<a class="skip-link" href="#main">Saltar al contenido</a>
<!-- HEADER_PLACEHOLDER -->
<main id="main">
  <h1>Contacto y agendamiento</h1>
  <p>Contenido pendiente.</p>
</main>
<!-- FOOTER_PLACEHOLDER -->
<script src="assets/js/site.js" defer></script>
</body>
</html>
```

---

- [ ] **Step 7: Escribir `tools/check_site.py` completo**

```python
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
```

---

- [ ] **Step 8: Escribir `tools/check_links.py` completo**

```python
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
```

---

- [ ] **Step 9: Ejecutar `check_site.py` y verificar la salida EXACTA**

Desde `C:\Users\PC\Desktop\claude\Paginas web con SEO`:

```powershell
python tools/check_site.py sitio-sanvi
```

Salida esperada, literal y completa (codigo de salida `0`):

```
WARN index.html: sin bloque JSON-LD
WARN servicios.html: sin bloque JSON-LD
WARN nosotros.html: sin bloque JSON-LD
WARN contacto.html: sin bloque JSON-LD
OK: 0 errores, 4 aviso(s) en 4 pagina(s).
```

Luego verificar el modo archivo unico:

```powershell
python tools/check_site.py sitio-sanvi/index.html
```

Salida esperada (codigo de salida `0`):

```
WARN index.html: sin bloque JSON-LD
OK: 0 errores
```

Si aparece cualquier linea `ERROR`, **no continuar**: corregir el HTML o el CSS hasta que la salida coincida caracter por caracter. Los 4 `WARN` son correctos y esperados en esta etapa (el JSON-LD se agrega en una tarea posterior); las tareas siguientes vuelven a correr este mismo comando y esperan exactamente esta salida.

---

- [ ] **Step 10: Ejecutar `check_links.py` y verificar la salida EXACTA**

```powershell
python tools/check_links.py sitio-sanvi
```

Salida esperada, literal y completa (codigo de salida `0`):

```
WARN: falta sitemap.xml
WARN: falta robots.txt
OK: todos los enlaces internos, anclas y assets resuelven.
```

En esta tarea todavia no hay enlaces cruzados entre paginas (el header/footer con la navegacion llega en la Tarea 2), asi que las unicas referencias relativas son `assets/css/base.css`, `assets/css/components.css`, `assets/css/pages.css`, `assets/img/favicon.svg`, `assets/js/site.js` y el ancla `#main` del skip-link — todas resuelven gracias a los stubs del Step 1 y al `<main id="main">`. Si aparece un `ERROR: ... y ese archivo no existe`, falta crear el stub correspondiente.

Comprobar ademas los codigos de salida:

```powershell
python tools/check_site.py sitio-sanvi; Write-Output "check_site exit=$LASTEXITCODE"
python tools/check_links.py sitio-sanvi; Write-Output "check_links exit=$LASTEXITCODE"
```

Esperado: `check_site exit=0` y `check_links exit=0`.

---

- [ ] **Step 11: Inicializar git y crear `.gitignore`**

El directorio del proyecto todavia no es un repo git. Desde `C:\Users\PC\Desktop\claude\Paginas web con SEO`:

```powershell
git init
git branch -M main
```

Crear `.gitignore` en la raiz del proyecto con exactamente:

```gitignore
# Estado interno de las skills (no forma parte del entregable)
.superpowers/

# Python
__pycache__/
*.pyc

# Sistema operativo
.DS_Store
Thumbs.db

# Dependencias que este proyecto NO usa, pero que herramientas externas
# podrian generar si alguien corre un tooling de node en la carpeta
node_modules/
```

Verificar que `.superpowers/` quede efectivamente ignorado:

```powershell
git status --short
```

Esperado: la lista de archivos sin seguimiento incluye `.gitignore`, `docs/`, `draska-audit/`, `sitio-sanvi/` y `tools/`, y **no** incluye `.superpowers/`.

---

- [ ] **Step 12: Commit inicial**

```powershell
git add .gitignore docs draska-audit sitio-sanvi tools
git commit -m @'
feat: estructura base del sitio Sanvi y validadores estaticos

- sitio-sanvi/ con las 4 paginas (index, servicios, nosotros, contacto):
  head SEO definitivo (title/description unicos, canonical, OG, fonts,
  favicon) y body con skip-link, placeholders de header/footer y main#main.
- assets/css/base.css: tokens de diseno (espaciado, escala tipografica,
  paleta turquesa/coral, radios, sombra, gradientes), reset, tipografia
  Sora/Inter, foco visible y utilidades .container/.skip-link/.sr-only.
- Stubs de components.css, pages.css, site.js y favicon.svg.
- tools/check_site.py: valida title, description, canonical, un unico h1,
  bloques JSON-LD y (con --content) el minimo de palabras en <main>.
- tools/check_links.py: valida enlaces internos, anclas, assets, sitemap.xml
  y robots.txt.

Verificado: check_site.py -> "OK: 0 errores, 4 aviso(s) en 4 pagina(s)."
Verificado: check_links.py -> "OK: todos los enlaces internos, anclas y
assets resuelven."

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
'@
```

---

### Task 2: Identidad visual, rasters de marca y componentes compartidos

**Files:**
- Create: `tools/shoot.py`
- Create: `tools/og/og.html`
- Create: `tools/og/logo.html`
- Create: `tools/og/touch-icon.html`
- Create: `sitio-sanvi/assets/img/hero-cuidado.svg`
- Create: `sitio-sanvi/assets/img/cobertura-calama.svg`
- Create (generado por `tools/shoot.py`, no se escribe a mano): `sitio-sanvi/assets/img/og-sanvi.png`
- Create (generado): `sitio-sanvi/assets/img/logo-sanvi.png`
- Create (generado): `sitio-sanvi/assets/img/apple-touch-icon.png`
- Modify: `sitio-sanvi/assets/css/components.css` (sobrescribe el stub de la Tarea 1)
- Modify: `sitio-sanvi/assets/js/site.js` (sobrescribe el stub de la Tarea 1)
- Modify: `sitio-sanvi/index.html`, `sitio-sanvi/servicios.html`, `sitio-sanvi/nosotros.html`, `sitio-sanvi/contacto.html` (añadir `<link rel="apple-touch-icon">` en el `<head>`; sustituir `<!-- HEADER_PLACEHOLDER -->` y `<!-- FOOTER_PLACEHOLDER -->` por el header, el footer y el FAB reales)

**Interfaces:**

*Consumes — tokens y utilidades de `base.css` (Tarea 1), usados literalmente:* `--sp-2…--sp-9`, `--fs-100…--fs-900`, `--font-display`, `--font-body`, `--c-teal-050/100/300/400/500/900`, `--c-coral-500/600`, `--c-surface`, `--c-line`, `--c-ink`, `--c-muted`, `--r-md`, `--r-lg`, `--r-pill`, `--shadow-sm`, `--grad-soft`, `--grad-teal`, `--container-max`, `--section-y`, y las clases `.container`, `.sr-only`, `.skip-link`. También los contratos de marcado: `<!-- HEADER_PLACEHOLDER -->`, `<!-- FOOTER_PLACEHOLDER -->`, `<main id="main">`.

*Produces — 4 tokens de color nuevos, declarados en un `:root` propio de `components.css` porque `base.css` no tiene equivalente:* `--c-ink-950` (fondo oscuro del footer), `--c-amber-050` y `--c-amber-500` (callout de advertencia), `--c-coral-050` (fondo del icono de la checklist negativa).

*Produces — clases de `components.css` (contrato congelado; las Tareas 3–6 las consumen sin redefinirlas):*

- Layout de sección: `.section`, `.section--surface`, `.section--tint`, `.section__head`, `.eyebrow`, `.lede`, `.stack`
- Header y navegación: `.site-header`, `.site-header.is-stuck`, `.site-header__inner`, `.brand`, `.brand__mark`, `.brand__name`, `.nav-toggle`, `.nav-toggle__bars`, `.site-nav`, `.site-nav.nav-open`, `.site-nav__list`, `.site-nav__cta`
- Botones: `.btn`, `.btn--primary`, `.btn--ghost`, `.btn--sm`, `.btn--block`
- Badges: `.badge-row`, `.badge`
- Tarjetas: `.card`, `.card__icon`, `.card__title`, `.card__price`
- Tabla de precios: `.price-table`, `.price-table__name`, `.price-table__desc`, `.price-table__price`
- Pasos: `.steps`, `.step`, `.step__num`
- Listas: `.checklist`, `.checklist--no`
- Avisos: `.callout`, `.callout--warn`
- FAQ: `.faq`, `.faq__item` (sobre `<details>`/`<summary>` nativos)
- Formulario: `.field`, `.field__label`, `.field__control`, `.field__hint`, `.form-actions`
- Footer: `.site-footer`, `.footer__grid`, `.footer__col`, `.footer__nap`, `.footer__note`
- Flotante: `.wa-fab`, `.wa-fab__text`

*Produces — contrato de `site.js`:* constante `WA_NUMBER = '56978833741'`; el botón `.nav-toggle` alterna la clase **`nav-open` sobre `#site-nav`** (no sobre el header) y mantiene su propio `aria-expanded`; `#site-header` recibe/pierde `is-stuck` según `scrollY > 8`; el `<form data-wa-form>` se intercepta y abre `wa.me` con los campos `nombre`, `servicio`, `sector`, `horario`, `mensaje`.

*Produces — contrato de `tools/shoot.py`:* CLI `python tools/shoot.py <url-o-archivo.html> --out <ruta.png> --width W --height H`; salidas literales `OK: capturado {out} ({W}x{H})` (código 0), `ERROR: no se encontro Chrome ni Edge instalado (define CHROME_PATH)` (código 1), `ERROR: no se genero {out}` (código 1). Lo usan las Tareas 3–6 y 9 para las capturas de verificación visual.

> **Nota sobre `.section`, `.eyebrow`, `.lede` y `.stack`:** el marcado de las Tareas 3–6 las usa 20, 15, 16 y 17 veces respectivamente, y no están definidas ni en `base.css` (Tarea 1) ni en `pages.css` (Tarea 3). Viven aquí porque son componentes compartidos por las 4 páginas, no secciones concretas. Sin ellas el sitio se renderiza sin ritmo vertical ni jerarquía. Lo mismo aplica a `.btn--block` (3 usos en `contacto.html`) y al bloque de formulario, que la Tarea 6 declara como "ya definidas".

---

- [ ] **Step 1: Escribir `tools/shoot.py`**

Este script es la única herramienta de verificación visual del proyecto: todas las tareas posteriores lo invocan para abrir capturas con Read. Se escribe antes que nada porque el Step 3 depende de él.

Crear `tools/shoot.py`:

```python
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
```

Comprobar que encuentra un navegador antes de seguir:

```bash
cd "/c/Users/PC/Desktop/claude/Paginas web con SEO"
python -c "import sys; sys.path.insert(0,'tools'); import shoot; print(shoot.find_browser())"
```

Debe imprimir una ruta a `chrome.exe` o `msedge.exe`. Si imprime `None`, exportar `CHROME_PATH` antes de continuar; sin navegador los Steps 3, 10 y las verificaciones visuales de las Tareas 3–6 y 9 no se pueden ejecutar.

---

- [ ] **Step 2: Escribir los tres documentos de captura en `tools/og/`**

Son HTML aislados, con todo el CSS inline y los colores en hexadecimal literal (no dependen de `base.css`: se abren como `file://`, fuera del sitio). Nunca se publican: viven en `tools/`, que no se despliega.

```bash
mkdir -p "/c/Users/PC/Desktop/claude/Paginas web con SEO/tools/og"
```

Crear `tools/og/og.html` (se captura a 1200×630):

```html
<!DOCTYPE html>
<html lang="es-CL">
<head>
<meta charset="utf-8">
<title>og-sanvi</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=Sora:wght@600;700&display=swap">
<style>
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; }
  body {
    width: 1200px; height: 630px; overflow: hidden; position: relative;
    display: flex; flex-direction: column; justify-content: center;
    padding: 0 92px;
    background: linear-gradient(135deg, #0F9B8E 0%, #14B8A6 52%, #2DD4BF 100%);
    color: #FFFFFF;
    font-family: "Inter", "Segoe UI", system-ui, sans-serif;
  }
  .blob { position: absolute; border-radius: 50%; background: rgba(255,255,255,.10); }
  .blob--a { width: 520px; height: 520px; right: -150px; top: -190px; }
  .blob--b { width: 300px; height: 300px; right: 90px; bottom: -140px; background: rgba(255,255,255,.08); }
  .blob--c { width: 120px; height: 120px; left: -50px; bottom: 60px; background: rgba(255,255,255,.09); }
  .row { position: relative; display: flex; align-items: center; gap: 26px; }
  .mark { flex: none; }
  .word {
    font-family: "Sora", "Segoe UI", system-ui, sans-serif;
    font-weight: 700; font-size: 108px; line-height: 1; letter-spacing: -.03em;
  }
  .tagline {
    position: relative; margin-top: 34px;
    font-size: 42px; font-weight: 500; line-height: 1.25; letter-spacing: -.01em;
    color: rgba(255,255,255,.96); max-width: 900px;
  }
  .meta {
    position: relative; margin-top: 44px;
    display: flex; align-items: center; gap: 18px; flex-wrap: wrap;
  }
  .pill {
    padding: 14px 28px; border-radius: 999px;
    background: rgba(255,255,255,.16); border: 2px solid rgba(255,255,255,.34);
    font-size: 27px; font-weight: 500; letter-spacing: .01em;
  }
  .pill--solid { background: #FF6B57; border-color: #FF6B57; font-weight: 600; }
</style>
</head>
<body>
  <div class="blob blob--a"></div>
  <div class="blob blob--b"></div>
  <div class="blob blob--c"></div>

  <div class="row">
    <svg class="mark" viewBox="0 0 64 64" width="118" height="118" aria-hidden="true">
      <rect width="64" height="64" rx="16" fill="#FFFFFF" fill-opacity="0.18"/>
      <path d="M27 15h10v12h12v10H37v12H27V37H15V27h12z" fill="#FFFFFF"/>
      <circle cx="48" cy="16" r="6" fill="#FF6B57"/>
    </svg>
    <span class="word">Sanvi</span>
  </div>

  <p class="tagline">Enfermeria e inyecciones a domicilio &middot; Calama</p>

  <div class="meta">
    <span class="pill pill--solid">Desde $10.000</span>
    <span class="pill">Todos los dias, 8:00 a 21:00</span>
    <span class="pill">+56 9 7883 3741</span>
  </div>
</body>
</html>
```

Crear `tools/og/logo.html` (se captura a 512×512):

```html
<!DOCTYPE html>
<html lang="es-CL">
<head>
<meta charset="utf-8">
<title>logo-sanvi</title>
<style>
  html, body { margin: 0; padding: 0; }
  body {
    width: 512px; height: 512px; overflow: hidden;
    display: flex; align-items: center; justify-content: center;
    background: linear-gradient(135deg, #0F9B8E 0%, #14B8A6 50%, #2DD4BF 100%);
  }
</style>
</head>
<body>
  <svg viewBox="0 0 64 64" width="512" height="512" aria-hidden="true">
    <path d="M27 15h10v12h12v10H37v12H27V37H15V27h12z" fill="#FFFFFF"/>
    <circle cx="48" cy="16" r="6.5" fill="#FF6B57"/>
  </svg>
</body>
</html>
```

Crear `tools/og/touch-icon.html` (se captura a 180×180). iOS recorta el icono a un cuadrado redondeado y algunos launchers a un circulo: el glifo se centra y se reduce al 56% del lienzo para que nada quede fuera del area segura, y el punto coral se mueve dentro de esa area en vez de ir a la esquina:

```html
<!DOCTYPE html>
<html lang="es-CL">
<head>
<meta charset="utf-8">
<title>apple-touch-icon</title>
<style>
  html, body { margin: 0; padding: 0; }
  body {
    width: 180px; height: 180px; overflow: hidden;
    display: flex; align-items: center; justify-content: center;
    background: linear-gradient(135deg, #0F9B8E 0%, #14B8A6 50%, #2DD4BF 100%);
  }
</style>
</head>
<body>
  <svg viewBox="0 0 64 64" width="102" height="102" aria-hidden="true">
    <path d="M26 12h12v14h14v12H38v14H26V38H12V26h14z" fill="#FFFFFF"/>
    <circle cx="45.5" cy="45.5" r="5.5" fill="#FF6B57"/>
  </svg>
</body>
</html>
```

---

- [ ] **Step 3: Generar los tres PNG de marca y verificarlos**

```bash
cd "/c/Users/PC/Desktop/claude/Paginas web con SEO"
python tools/shoot.py tools/og/og.html         --out sitio-sanvi/assets/img/og-sanvi.png         --width 1200 --height 630
python tools/shoot.py tools/og/logo.html       --out sitio-sanvi/assets/img/logo-sanvi.png       --width 512  --height 512
python tools/shoot.py tools/og/touch-icon.html --out sitio-sanvi/assets/img/apple-touch-icon.png --width 180  --height 180
```

Los tres deben terminar en `OK: capturado … (WxH)`. Comprobar dimensiones y peso reales leyendo la cabecera IHDR de cada PNG (solo stdlib, sin Pillow):

```bash
python -c "
import struct, pathlib
for n in ('og-sanvi.png', 'logo-sanvi.png', 'apple-touch-icon.png'):
    b = pathlib.Path('sitio-sanvi/assets/img/' + n).read_bytes()
    w, h = struct.unpack('>II', b[16:24])
    print('%-22s %4dx%-4d %5.1f KB' % (n, w, h, len(b) / 1024))
"
```

Esperado exactamente `og-sanvi.png 1200x630`, `logo-sanvi.png 512x512`, `apple-touch-icon.png 180x180`. El `apple-touch-icon.png` debe pesar menos de 30 KB: es el unico de los tres que se referencia desde el `<head>` y por tanto cuenta en el presupuesto de 400 KB por pagina que verifica `tools/check_perf.py` en la Tarea 9 (los otros dos solo aparecen como URL absoluta en `og:image` y en el JSON-LD, y no cuentan).

Abrir los tres PNG con la herramienta Read y comprobar: (a) en `og-sanvi.png` la palabra **Sanvi** se ve en Sora (geometrica, con la `a` de un solo piso); si se ve en Segoe UI, la captura corrio sin red y hay que repetirla con conexion; (b) el texto no se corta por ningun borde y las tres pildoras caben en una sola linea; (c) en `logo-sanvi.png` la cruz blanca esta centrada y el punto coral no toca el borde; (d) en `apple-touch-icon.png` la cruz ocupa poco mas de la mitad del lienzo y se mantiene entera al imaginar un recorte circular.

---

- [ ] **Step 4: Escribir `sitio-sanvi/assets/img/hero-cuidado.svg`**

Ilustracion propia, plana y geometrica: una casa con una figura de enfermeria y su maletin. Sin fotos ni clipart. Los colores van en hexadecimal literal porque un `.svg` referenciado desde `<img>` no hereda las variables CSS del documento.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 460" width="520" height="460" role="img" aria-label="Visita de enfermeria a domicilio">
  <defs>
    <linearGradient id="hcTeal" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0F9B8E"/>
      <stop offset="0.5" stop-color="#14B8A6"/>
      <stop offset="1" stop-color="#2DD4BF"/>
    </linearGradient>
    <linearGradient id="hcTunic" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#2DD4BF"/>
      <stop offset="1" stop-color="#0F9B8E"/>
    </linearGradient>
  </defs>

  <!-- Fondo y acentos -->
  <rect x="10" y="30" width="500" height="400" rx="110" fill="#F4FBFA"/>
  <circle cx="352" cy="168" r="132" fill="#DDF5F1"/>
  <circle cx="96" cy="86" r="15" fill="#FF6B57"/>
  <circle cx="470" cy="332" r="10" fill="#2DD4BF"/>
  <rect x="432" y="94" width="16" height="52" rx="8" fill="#14B8A6" opacity="0.45"/>
  <rect x="414" y="112" width="52" height="16" rx="8" fill="#14B8A6" opacity="0.45"/>
  <rect x="46" y="374" width="428" height="12" rx="6" fill="#DDF5F1"/>

  <!-- Casa -->
  <rect x="266" y="128" width="26" height="64" rx="6" fill="#0F9B8E"/>
  <path d="M62 224 190 118 318 224Z" fill="#0F9B8E"/>
  <rect x="96" y="218" width="188" height="158" rx="16" fill="#FFFFFF" stroke="#DCE7E6" stroke-width="3"/>
  <rect x="120" y="248" width="46" height="46" rx="8" fill="#DDF5F1"/>
  <rect x="214" y="248" width="46" height="46" rx="8" fill="#DDF5F1"/>
  <rect x="162" y="304" width="56" height="72" rx="10" fill="url(#hcTeal)"/>
  <circle cx="205" cy="342" r="4" fill="#FFFFFF"/>

  <!-- Figura de enfermeria -->
  <rect x="340" y="268" width="24" height="24" fill="#FFD8C9"/>
  <path d="M310 376V314a42 42 0 0 1 84 0v62Z" fill="url(#hcTunic)"/>
  <path d="M320 328c-12 8-22 16-26 28" stroke="url(#hcTunic)" stroke-width="20" stroke-linecap="round" fill="none"/>
  <path d="M352 214a34 34 0 0 0-34 34v8h68v-8a34 34 0 0 0-34-34z" fill="#0B3B37"/>
  <circle cx="352" cy="250" r="32" fill="#FFD8C9"/>
  <rect x="330" y="215" width="44" height="17" rx="5" fill="#FFFFFF"/>
  <rect x="349" y="217" width="6" height="13" rx="2" fill="#FF6B57"/>
  <rect x="345.5" y="220.5" width="13" height="6" rx="2" fill="#FF6B57"/>
  <path d="M266 322v-9a14 14 0 0 1 28 0v9" stroke="#E5533F" stroke-width="7" fill="none" stroke-linecap="round"/>
  <rect x="242" y="322" width="76" height="58" rx="12" fill="#FF6B57"/>
  <rect x="274" y="336" width="12" height="30" rx="4" fill="#FFFFFF"/>
  <rect x="265" y="345" width="30" height="12" rx="4" fill="#FFFFFF"/>
</svg>
```

---

- [ ] **Step 5: Escribir `sitio-sanvi/assets/img/cobertura-calama.svg`**

Mapa **estilizado**, deliberadamente no geografico: manzanas esquematicas, una avenida diagonal, tres anillos de radio de servicio y un pin coral en el centro. Sin texto (evita depender de fuentes al rasterizar y no promete una precision que el dibujo no tiene).

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 300" width="420" height="300" role="img" aria-label="Radio de cobertura dentro del area urbana">
  <defs>
    <clipPath id="ccFrame"><rect x="0" y="0" width="420" height="300" rx="22"/></clipPath>
  </defs>

  <rect x="0" y="0" width="420" height="300" rx="22" fill="#F4FBFA"/>

  <g clip-path="url(#ccFrame)">
    <!-- Manzanas -->
    <g fill="#E2F3F0">
      <rect x="16"  y="18"  width="82" height="52" rx="8"/>
      <rect x="118" y="18"  width="82" height="52" rx="8"/>
      <rect x="220" y="18"  width="82" height="52" rx="8"/>
      <rect x="322" y="18"  width="82" height="52" rx="8"/>
      <rect x="16"  y="88"  width="82" height="52" rx="8"/>
      <rect x="118" y="88"  width="82" height="52" rx="8"/>
      <rect x="220" y="88"  width="82" height="52" rx="8"/>
      <rect x="322" y="88"  width="82" height="52" rx="8"/>
      <rect x="16"  y="158" width="82" height="52" rx="8"/>
      <rect x="118" y="158" width="82" height="52" rx="8"/>
      <rect x="220" y="158" width="82" height="52" rx="8"/>
      <rect x="322" y="158" width="82" height="52" rx="8"/>
      <rect x="16"  y="228" width="82" height="52" rx="8"/>
      <rect x="118" y="228" width="82" height="52" rx="8"/>
      <rect x="220" y="228" width="82" height="52" rx="8"/>
      <rect x="322" y="228" width="82" height="52" rx="8"/>
    </g>
    <!-- Avenida diagonal -->
    <path d="M-24 258 L196 26 L448 128" fill="none" stroke="#FFFFFF" stroke-width="15" stroke-linejoin="round"/>
    <path d="M-24 258 L196 26 L448 128" fill="none" stroke="#DCE7E6" stroke-width="1.5" stroke-linejoin="round"/>
  </g>

  <!-- Anillos de cobertura -->
  <circle cx="210" cy="150" r="120" fill="#14B8A6" opacity="0.08"/>
  <circle cx="210" cy="150" r="120" fill="none" stroke="#14B8A6" stroke-opacity="0.38" stroke-width="2" stroke-dasharray="7 9"/>
  <circle cx="210" cy="150" r="84"  fill="none" stroke="#14B8A6" stroke-opacity="0.48" stroke-width="2" stroke-dasharray="7 9"/>
  <circle cx="210" cy="150" r="48"  fill="#14B8A6" opacity="0.14"/>

  <!-- Pin -->
  <ellipse cx="210" cy="190" rx="26" ry="8" fill="#0B2A3A" opacity="0.10"/>
  <path d="M210 92c-17.7 0-32 14.3-32 32 0 23 32 60 32 60s32-37 32-60c0-17.7-14.3-32-32-32z" fill="#FF6B57"/>
  <circle cx="210" cy="124" r="11.5" fill="#FFFFFF"/>
</svg>
```

---

- [ ] **Step 6: Escribir `sitio-sanvi/assets/css/components.css` completo**

Sobrescribe integramente el stub de la Tarea 1. Todo el espaciado, color y tipografia sale de los tokens de `base.css`; los unicos valores nuevos son los 4 colores del `:root` inicial, justificados en su comentario.

```css
/* ==========================================================================
   components.css — Sanvi
   Componentes compartidos por las 4 paginas: layout de seccion, botones,
   badges, header/nav, tarjetas, tabla de precios, pasos, checklists,
   avisos, FAQ, formulario, footer y boton flotante de WhatsApp.
   Se carga DESPUES de base.css y ANTES de pages.css.
   Regla de oro: aqui no se define ninguna seccion concreta de una pagina
   (eso vive en pages.css) ni se redefine ningun token de base.css.
   ========================================================================== */

/* --------------------------------------------------------------------------
   0. Los cuatro colores que base.css no tiene
   base.css cubre la paleta de marca (turquesa, coral, superficie, tinta),
   pero no un fondo oscuro para el footer, ni un tono de advertencia, ni un
   fondo suave de coral. Se declaran aqui, junto a los componentes que son
   los unicos que los usan, en lugar de contaminar los tokens de base.
   -------------------------------------------------------------------------- */
:root {
  --c-ink-950: #08202B;    /* fondo del footer */
  --c-amber-050: #FFF6E6;  /* fondo de .callout--warn */
  --c-amber-500: #B26B00;  /* borde y titulo de .callout--warn (AA sobre --c-amber-050) */
  --c-coral-050: #FFEDE8;  /* fondo del icono de .checklist--no */
}

/* --------------------------------------------------------------------------
   1. Layout de seccion
   Consumido por las 4 paginas (Tareas 3–6). No esta en base.css porque no es
   un token ni una utilidad generica, sino el ritmo vertical del sitio.
   -------------------------------------------------------------------------- */
.section { padding-block: var(--section-y); }
.section--surface { background: var(--c-surface); }
.section--tint { background: var(--c-teal-050); }

.section__head {
  max-width: 62ch;
  margin-bottom: var(--sp-7);
}

.section__head h2 { margin-bottom: var(--sp-4); }

.eyebrow {
  margin-bottom: var(--sp-3);
  font-family: var(--font-display);
  font-size: var(--fs-200);
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--c-teal-500);
}

.lede {
  font-size: var(--fs-500);
  color: var(--c-muted);
}

/* Apila hijos con un ritmo unico. Se usa tambien en el <form> de contacto. */
.stack > * + * { margin-top: var(--sp-5); }

/* --------------------------------------------------------------------------
   2. Botones
   -------------------------------------------------------------------------- */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--sp-3);
  min-height: 48px;
  padding: var(--sp-4) var(--sp-6);
  font-family: var(--font-display);
  font-size: var(--fs-300);
  font-weight: 600;
  line-height: 1.2;
  text-align: center;
  text-decoration: none;
  border: 2px solid transparent;
  border-radius: var(--r-pill);
  transition: background-color 0.15s ease, border-color 0.15s ease,
              color 0.15s ease, transform 0.15s ease;
}

.btn:hover { transform: translateY(-1px); }
.btn:active { transform: translateY(0); }

.btn--primary {
  background: var(--c-coral-500);
  border-color: var(--c-coral-500);
  color: #FFFFFF;
  box-shadow: var(--shadow-sm);
}

.btn--primary:hover {
  background: var(--c-coral-600);
  border-color: var(--c-coral-600);
  color: #FFFFFF;
}

.btn--ghost {
  background: transparent;
  border-color: var(--c-teal-500);
  color: var(--c-teal-500);
}

.btn--ghost:hover {
  background: var(--c-teal-050);
  border-color: var(--c-teal-900);
  color: var(--c-teal-900);
}

.btn--sm {
  min-height: 40px;
  padding: var(--sp-3) var(--sp-5);
  font-size: var(--fs-200);
}

.btn--block {
  display: flex;
  width: 100%;
}

/* Unica regla que cruza a una clase de pages.css, y a proposito: dentro de
   .cta-band el fondo es --grad-teal, asi que un boton fantasma turquesa sobre
   turquesa quedaria ilegible. Con .cta-band .btn--ghost (0,2,0) gana sin
   depender del orden de carga de las hojas. */
.cta-band .btn--ghost {
  border-color: rgba(255, 255, 255, 0.8);
  color: #FFFFFF;
}

.cta-band .btn--ghost:hover {
  background: rgba(255, 255, 255, 0.16);
  border-color: #FFFFFF;
  color: #FFFFFF;
}

/* --------------------------------------------------------------------------
   3. Badges
   -------------------------------------------------------------------------- */
.badge-row {
  display: flex;
  flex-wrap: wrap;
  gap: var(--sp-3);
  list-style: none;
  padding: 0;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: var(--sp-3);
  padding: var(--sp-2) var(--sp-4);
  background: var(--c-surface);
  border: 1px solid var(--c-line);
  border-radius: var(--r-pill);
  font-size: var(--fs-300);
  color: var(--c-muted);
}

.badge::before {
  content: "";
  flex: none;
  width: 0.45rem;
  height: 0.45rem;
  border-radius: 50%;
  background: var(--c-teal-400);
}

/* --------------------------------------------------------------------------
   4. Header y navegacion
   Contrato con site.js: el boton .nav-toggle alterna la clase `nav-open`
   sobre #site-nav (NO sobre el header) y mantiene su propio aria-expanded,
   del que cuelga la animacion hamburguesa -> X. El header recibe `is-stuck`
   al hacer scroll.
   Sin JavaScript el menu movil no se abre; la navegacion completa sigue
   disponible en el footer de las 4 paginas, que no depende de JS.
   -------------------------------------------------------------------------- */
.site-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid transparent;
  transition: box-shadow 0.2s ease, border-color 0.2s ease;
}

.site-header.is-stuck {
  border-bottom-color: var(--c-line);
  box-shadow: var(--shadow-sm);
}

.site-header__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--sp-5);
  min-height: 72px;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: var(--sp-3);
  font-family: var(--font-display);
  font-weight: 700;
  color: var(--c-ink);
  text-decoration: none;
}

.brand:hover { color: var(--c-teal-500); }

.brand__mark {
  flex: none;
  border-radius: var(--r-md);
}

.brand__name {
  font-size: var(--fs-600);
  letter-spacing: -0.02em;
}

.nav-toggle {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: none;
  width: 46px;
  height: 46px;
  background: var(--c-surface);
  border: 1px solid var(--c-line);
  border-radius: var(--r-md);
  color: var(--c-ink);
}

.nav-toggle:hover { border-color: var(--c-teal-400); }

/* Hamburguesa de tres lineas hecha con la barra central y sus dos
   pseudo-elementos. Sin SVG y sin markup extra. */
.nav-toggle__bars {
  position: relative;
  display: block;
  width: 22px;
  height: 2px;
  border-radius: 2px;
  background: currentColor;
  transition: background-color 0.15s ease;
}

.nav-toggle__bars::before,
.nav-toggle__bars::after {
  content: "";
  position: absolute;
  left: 0;
  display: block;
  width: 22px;
  height: 2px;
  border-radius: 2px;
  background: currentColor;
  transition: transform 0.18s ease, top 0.18s ease;
}

.nav-toggle__bars::before { top: -7px; }
.nav-toggle__bars::after { top: 7px; }

.nav-toggle[aria-expanded="true"] .nav-toggle__bars { background: transparent; }
.nav-toggle[aria-expanded="true"] .nav-toggle__bars::before { top: 0; transform: rotate(45deg); }
.nav-toggle[aria-expanded="true"] .nav-toggle__bars::after { top: 0; transform: rotate(-135deg); }

/* Menu movil: panel desplegable bajo el header. Cerrado usa
   visibility:hidden, asi que sus enlaces salen del orden de tabulacion. */
.site-nav {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  display: grid;
  gap: var(--sp-4);
  padding: var(--sp-5) var(--sp-5) var(--sp-6);
  background: var(--c-surface);
  border-bottom: 1px solid var(--c-line);
  box-shadow: var(--shadow-sm);
  visibility: hidden;
  opacity: 0;
  transform: translateY(-8px);
  transition: opacity 0.18s ease, transform 0.18s ease, visibility 0.18s;
}

.site-nav.nav-open {
  visibility: visible;
  opacity: 1;
  transform: translateY(0);
}

.site-nav__list {
  display: grid;
  gap: var(--sp-2);
  list-style: none;
  padding: 0;
  margin: 0;
}

.site-nav__list a {
  position: relative;
  display: block;
  padding: var(--sp-3) var(--sp-4);
  font-family: var(--font-display);
  font-size: var(--fs-300);
  font-weight: 600;
  color: var(--c-ink);
  text-decoration: none;
  border-radius: var(--r-md);
}

.site-nav__list a:hover {
  background: var(--c-teal-050);
  color: var(--c-teal-900);
}

.site-nav__list a[aria-current="page"] {
  background: var(--c-teal-050);
  color: var(--c-teal-500);
}

.site-nav__cta { width: 100%; }

@media (min-width: 900px) {
  .nav-toggle { display: none; }

  .site-nav {
    position: static;
    display: flex;
    align-items: center;
    gap: var(--sp-6);
    padding: 0;
    background: none;
    border: 0;
    box-shadow: none;
    visibility: visible;
    opacity: 1;
    transform: none;
  }

  .site-nav__list {
    display: flex;
    align-items: center;
    gap: var(--sp-5);
  }

  .site-nav__list a { padding: var(--sp-2) var(--sp-3); }

  .site-nav__list a[aria-current="page"] {
    background: none;
    color: var(--c-teal-500);
  }

  .site-nav__list a[aria-current="page"]::after {
    content: "";
    position: absolute;
    left: var(--sp-3);
    right: var(--sp-3);
    bottom: -6px;
    height: 3px;
    border-radius: 3px;
    background: var(--c-teal-400);
  }

  .site-nav__cta { width: auto; }
}

/* --------------------------------------------------------------------------
   5. Tarjetas
   -------------------------------------------------------------------------- */
.card {
  display: flex;
  flex-direction: column;
  gap: var(--sp-3);
  padding: var(--sp-6);
  background: var(--c-surface);
  border: 1px solid var(--c-line);
  border-radius: var(--r-lg);
  box-shadow: var(--shadow-sm);
  transition: transform 0.18s ease, box-shadow 0.18s ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(11, 42, 58, 0.06), 0 14px 30px rgba(11, 42, 58, 0.10);
}

.card__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: var(--r-md);
  background: var(--grad-teal);
  color: #FFFFFF;
  font-family: var(--font-display);
  font-size: var(--fs-300);
  font-weight: 700;
  letter-spacing: 0.02em;
}

.card__title { font-size: var(--fs-600); }

.card__title a {
  color: inherit;
  text-decoration: none;
}

.card__title a:hover {
  color: var(--c-teal-500);
  text-decoration: underline;
}

/* El gap del flex ya aporta la separacion: se neutraliza el `p + p` de
   base.css. La regla del precio se escribe con el elemento incluido para
   ganar en especificidad a `.card > p`. */
.card > p {
  margin: 0;
  font-size: var(--fs-300);
  color: var(--c-muted);
}

.card > p.card__price {
  margin-top: auto;
  padding-top: var(--sp-2);
  font-family: var(--font-display);
  font-size: var(--fs-600);
  font-weight: 700;
  color: var(--c-teal-900);
}

/* --------------------------------------------------------------------------
   6. Tabla de precios
   Tabla real a partir de 48em; tarjetas apiladas por debajo, usando el
   data-label de cada <td> como etiqueta via ::before.
   -------------------------------------------------------------------------- */
.price-table {
  width: 100%;
  background: var(--c-surface);
  border: 1px solid var(--c-line);
  border-radius: var(--r-lg);
  border-collapse: separate;
  border-spacing: 0;
  box-shadow: var(--shadow-sm);
}

.price-table caption {
  caption-side: bottom;
  padding-top: var(--sp-4);
  font-size: var(--fs-300);
  color: var(--c-muted);
  text-align: left;
}

.price-table th,
.price-table td {
  padding: var(--sp-4) var(--sp-5);
  text-align: left;
  vertical-align: top;
  border-bottom: 1px solid var(--c-line);
}

.price-table thead th {
  background: var(--c-teal-050);
  font-family: var(--font-display);
  font-size: var(--fs-200);
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--c-teal-900);
}

.price-table tbody tr:last-child td { border-bottom: 0; }

.price-table__name { font-weight: 600; }

.price-table__name a {
  color: var(--c-ink);
  text-decoration: none;
}

.price-table__name a:hover {
  color: var(--c-teal-500);
  text-decoration: underline;
}

.price-table__desc {
  font-size: var(--fs-300);
  color: var(--c-muted);
}

.price-table__price {
  font-family: var(--font-display);
  font-size: var(--fs-500);
  font-weight: 700;
  color: var(--c-teal-900);
  white-space: nowrap;
}

@media (max-width: 47.99em) {
  .price-table {
    background: none;
    border: 0;
    box-shadow: none;
  }

  .price-table thead {
    position: absolute;
    width: 1px;
    height: 1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
  }

  .price-table tr {
    display: grid;
    gap: var(--sp-3);
    padding: var(--sp-5);
    margin-bottom: var(--sp-4);
    background: var(--c-surface);
    border: 1px solid var(--c-line);
    border-radius: var(--r-lg);
    box-shadow: var(--shadow-sm);
  }

  .price-table td {
    display: block;
    padding: 0;
    border: 0;
  }

  .price-table td[data-label]::before {
    content: attr(data-label);
    display: block;
    margin-bottom: var(--sp-2);
    font-size: var(--fs-100);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--c-muted);
  }

  .price-table__name { font-family: var(--font-display); font-size: var(--fs-600); font-weight: 700; }
  .price-table__price { font-size: var(--fs-700); }
}

/* --------------------------------------------------------------------------
   7. Pasos numerados
   -------------------------------------------------------------------------- */
.steps {
  display: grid;
  gap: var(--sp-5);
  list-style: none;
  padding: 0;
  margin: 0;
}

.step {
  display: flex;
  align-items: flex-start;
  gap: var(--sp-5);
  padding: var(--sp-6);
  background: var(--c-surface);
  border: 1px solid var(--c-line);
  border-radius: var(--r-lg);
  box-shadow: var(--shadow-sm);
}

.step__num {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: none;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: var(--grad-teal);
  color: #FFFFFF;
  font-family: var(--font-display);
  font-size: var(--fs-500);
  font-weight: 700;
}

.step h3 {
  margin-bottom: var(--sp-2);
  font-size: var(--fs-600);
}

.step p {
  font-size: var(--fs-300);
  color: var(--c-muted);
}

@media (min-width: 900px) {
  .steps { grid-template-columns: repeat(3, 1fr); }
  .step { flex-direction: column; }
}

/* --------------------------------------------------------------------------
   8. Checklists
   El icono va en el ::before como SVG en data-uri: sin peticiones extra y
   sin markup adicional en el HTML.
   -------------------------------------------------------------------------- */
.checklist {
  display: grid;
  gap: var(--sp-4);
  list-style: none;
  padding: 0;
  margin: 0;
}

.checklist li {
  position: relative;
  padding-left: calc(var(--sp-7) + var(--sp-3));
}

.checklist li::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0.12em;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background-color: var(--c-teal-100);
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%230F9B8E' stroke-width='3.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M4 12.5 9.5 18 20 6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: center;
  background-size: 14px 14px;
}

.checklist--no li::before {
  background-color: var(--c-coral-050);
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23E5533F' stroke-width='3.2' stroke-linecap='round'%3E%3Cpath d='M6 6l12 12M18 6L6 18'/%3E%3C/svg%3E");
  background-size: 13px 13px;
}

/* --------------------------------------------------------------------------
   9. Avisos
   -------------------------------------------------------------------------- */
.callout {
  padding: var(--sp-6);
  background: var(--c-teal-050);
  border: 1px solid var(--c-line);
  border-left: 5px solid var(--c-teal-500);
  border-radius: var(--r-md);
}

.callout h3 {
  margin-bottom: var(--sp-3);
  font-size: var(--fs-600);
}

.callout--warn {
  background: var(--c-amber-050);
  border-color: #F0DCB4;
  border-left-color: var(--c-amber-500);
}

.callout--warn h3 { color: var(--c-amber-500); }

/* --------------------------------------------------------------------------
   10. FAQ
   Acordeon nativo con <details>/<summary>. No lleva JavaScript a proposito:
   abre y cierra sin scripts, funciona con teclado y es indexable.
   -------------------------------------------------------------------------- */
.faq {
  display: grid;
  gap: var(--sp-3);
}

.faq__item {
  background: var(--c-surface);
  border: 1px solid var(--c-line);
  border-radius: var(--r-md);
  box-shadow: var(--shadow-sm);
}

.faq__item summary {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--sp-5);
  padding: var(--sp-5) var(--sp-6);
  list-style: none;
  cursor: pointer;
  font-family: var(--font-display);
  font-size: var(--fs-500);
  font-weight: 600;
  text-align: left;
  color: var(--c-ink);
}

.faq__item summary::-webkit-details-marker { display: none; }

.faq__item summary:hover { color: var(--c-teal-500); }

.faq__item summary::after {
  content: "";
  flex: none;
  width: 11px;
  height: 11px;
  margin-top: -4px;
  border-right: 2px solid var(--c-teal-500);
  border-bottom: 2px solid var(--c-teal-500);
  transform: rotate(45deg);
  transition: transform 0.2s ease;
}

.faq__item[open] summary { color: var(--c-teal-900); }

.faq__item[open] summary::after {
  margin-top: 4px;
  transform: rotate(-135deg);
}

.faq__item > div {
  padding: 0 var(--sp-6) var(--sp-6);
  color: var(--c-muted);
}

/* --------------------------------------------------------------------------
   11. Formulario
   -------------------------------------------------------------------------- */
.field {
  display: grid;
  gap: var(--sp-2);
}

.field__label {
  font-family: var(--font-display);
  font-size: var(--fs-300);
  font-weight: 600;
  color: var(--c-ink);
}

.field__control {
  width: 100%;
  min-height: 48px;
  padding: var(--sp-4) var(--sp-5);
  background: var(--c-surface);
  color: var(--c-ink);
  border: 1px solid var(--c-line);
  border-radius: var(--r-md);
  font-size: var(--fs-400);
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.field__control:hover { border-color: var(--c-teal-300); }

/* No se anula el outline: el anillo de foco de base.css sigue vigente y el
   box-shadow solo lo refuerza. */
.field__control:focus {
  border-color: var(--c-teal-500);
  box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.22);
}

.field__control::placeholder { color: var(--c-muted); opacity: 0.75; }

textarea.field__control {
  min-height: 120px;
  resize: vertical;
}

select.field__control {
  appearance: none;
  padding-right: var(--sp-8);
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%230F9B8E' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M5 9l7 7 7-7'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right var(--sp-5) center;
  background-size: 14px 14px;
}

.field__hint {
  font-size: var(--fs-200);
  color: var(--c-muted);
}

.form-actions {
  display: grid;
  gap: var(--sp-3);
  margin-top: var(--sp-5);
}

/* --------------------------------------------------------------------------
   12. Footer
   -------------------------------------------------------------------------- */
.site-footer {
  padding-block: var(--sp-8);
  background: var(--c-ink-950);
  color: #BFD6DE;
  font-size: var(--fs-300);
}

.site-footer a {
  color: #FFFFFF;
  text-decoration: none;
}

.site-footer a:hover {
  color: var(--c-teal-300);
  text-decoration: underline;
}

.footer__grid {
  display: grid;
  gap: var(--sp-7);
}

.footer__col h2 {
  margin-bottom: var(--sp-4);
  font-family: var(--font-display);
  font-size: var(--fs-500);
  color: #FFFFFF;
}

.footer__col ul {
  display: grid;
  gap: var(--sp-3);
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer__nap {
  display: grid;
  gap: var(--sp-2);
  font-style: normal;
}

.footer__note {
  display: grid;
  gap: var(--sp-3);
  margin-top: var(--sp-7);
  padding-top: var(--sp-6);
  border-top: 1px solid rgba(255, 255, 255, 0.14);
  font-size: var(--fs-200);
  color: #9FBCC6;
}

/* El gap ya separa los parrafos: se neutraliza el `p + p` de base.css. */
.footer__note p + p { margin-top: 0; }

@media (min-width: 720px) {
  .footer__grid {
    grid-template-columns: 1.4fr 1fr 1.2fr;
    gap: var(--sp-8);
  }
}

/* --------------------------------------------------------------------------
   13. Boton flotante de WhatsApp
   Bajo 900px es un circulo de 56px solo con el icono: el nombre accesible lo
   aporta el aria-label del enlace, y .wa-fab__text se oculta con display:none.
   Desde 900px se convierte en pildora con el texto visible.
   El footer gana relleno inferior extra en movil para que el FAB no tape la
   ultima linea del aviso legal.
   -------------------------------------------------------------------------- */
.wa-fab {
  position: fixed;
  right: var(--sp-5);
  bottom: var(--sp-5);
  z-index: 90;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--sp-3);
  width: 56px;
  height: 56px;
  background: var(--c-coral-500);
  color: #FFFFFF;
  border-radius: var(--r-pill);
  box-shadow: 0 6px 20px rgba(11, 42, 58, 0.22);
  text-decoration: none;
  transition: background-color 0.15s ease, transform 0.15s ease;
}

.wa-fab:hover {
  background: var(--c-coral-600);
  color: #FFFFFF;
  transform: translateY(-2px);
}

.wa-fab__text { display: none; }

@media (max-width: 47.99em) {
  .site-footer { padding-bottom: calc(var(--sp-8) + 4rem); }
}

@media (min-width: 900px) {
  .wa-fab {
    right: var(--sp-6);
    bottom: var(--sp-6);
    width: auto;
    height: auto;
    padding: var(--sp-4) var(--sp-6);
    font-family: var(--font-display);
    font-size: var(--fs-300);
    font-weight: 600;
  }

  .wa-fab__text { display: inline; }
}
```

---

- [ ] **Step 7: Escribir `sitio-sanvi/assets/js/site.js` completo**

Sobrescribe integramente el stub de la Tarea 1. Es el unico JavaScript del sitio: sin dependencias, sin build, cargado con `defer`.

```js
/* ==========================================================================
   site.js — Sanvi
   Mejora progresiva. Sin este archivo el sitio sigue siendo utilizable: los
   enlaces de WhatsApp del header, del FAB y de cada CTA son <a> reales, el
   acordeon del FAQ es <details> nativo y la navegacion completa esta ademas
   en el footer, que no depende de JavaScript.
   Se carga con `defer` como ultimo elemento del <body> de las 4 paginas.
   ========================================================================== */
(function () {
  'use strict';

  /* Numero E.164 sin '+' para los enlaces wa.me. Unica fuente de verdad del JS.
     Si cambia el telefono hay que actualizarlo tambien en el HTML de las 4
     paginas (header, FAB, CTA y footer) y en el JSON-LD. */
  var WA_NUMBER = '56978833741';

  /* --- 1. Menu movil ---
     Alterna la clase `nav-open` sobre #site-nav (components.css espera la
     clase EN EL NAV, no en el header) y mantiene sincronizado el
     aria-expanded del boton, del que components.css cuelga la animacion del
     icono hamburguesa -> X.
     El acordeon del FAQ no aparece aqui a proposito: <details>/<summary>
     abren y cierran solos, con teclado incluido. Anadir JS solo empeoraria
     el INP sin aportar nada. */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');

  if (toggle && nav) {
    var closeNav = function () {
      toggle.setAttribute('aria-expanded', 'false');
      nav.classList.remove('nav-open');
    };

    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      nav.classList
    .toggle('nav-open', !open);
    });

    nav.addEventListener('click', function (event) {
      if (event.target.closest('a')) closeNav();
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        closeNav();
        toggle.focus();
      }
    });

    window.addEventListener('resize', function () {
      if (window.innerWidth >= 900) closeNav();
    });
  }

  /* --- 2. Sombra del header al hacer scroll --- */
  var header = document.getElementById('site-header');
  if (header) {
    var syncHeader = function () {
      header.classList.toggle('is-stuck', window.scrollY > 8);
    };
    syncHeader();
    window.addEventListener('scroll', syncHeader, { passive: true });
  }

  /* --- 3. Formulario de contacto -> WhatsApp --- */
  var form = document.querySelector('[data-wa-form]');
  if (form) {
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      var data = new FormData(form);
      var value = function (key) { return String(data.get(key) || '').trim(); };

      var lines = [
        'Hola Sanvi, quiero agendar una atencion de enfermeria a domicilio en Calama.',
        'Nombre: ' + value('nombre'),
        'Servicio: ' + value('servicio'),
        'Sector de Calama: ' + value('sector'),
        'Dia y hora preferidos: ' + value('horario')
      ];
      if (value('mensaje')) lines.push('Comentario: ' + value('mensaje'));

      window.location.href =
        'https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent(lines.join('\n'));
    });
  }
})();
```

Comprobar que el archivo es sintacticamente valido antes de seguir (Node no es una dependencia del proyecto; si no esta instalado, saltar esta comprobacion y confiar en la revision visual del Step 10):

```bash
cd "/c/Users/PC/Desktop/claude/Paginas web con SEO"
node --check sitio-sanvi/assets/js/site.js && echo "site.js: sintaxis OK"
```

---

- [ ] **Step 8: Añadir `apple-touch-icon` al `<head>` de las 4 páginas**

Edicion puntual: **no** se reescribe el resto del `<head>`, que quedo definitivo en la Tarea 1. En `index.html`, `servicios.html`, `nosotros.html` y `contacto.html`, sustituir la linea:

```html
  <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
```

por estas dos:

```html
  <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
```

Es el ultimo consumidor del PNG generado en el Step 3 y la razon por la que ese archivo debe existir en disco: `tools/check_links.py` valida el `href` de todo `<link>`, asi que si falta el PNG la verificacion del Step 10 fallara con `ERROR: index.html referencia assets/img/apple-touch-icon.png y ese archivo no existe`.

Comprobar que quedaron las cuatro:

```bash
cd "/c/Users/PC/Desktop/claude/Paginas web con SEO"
grep -c "apple-touch-icon" sitio-sanvi/index.html sitio-sanvi/servicios.html sitio-sanvi/nosotros.html sitio-sanvi/contacto.html
```

Esperado: `1` en cada una de las cuatro.

---

- [ ] **Step 9: Instalar header, footer y botón flotante en las 4 páginas**

En cada uno de `index.html`, `servicios.html`, `nosotros.html` y `contacto.html`, insertar el siguiente `<header>` **inmediatamente después** de `<a class="skip-link" …>` y el `<footer>` + `<a class="wa-fab">` **inmediatamente antes** de `<script src="assets/js/site.js" defer></script>`.

Header (bloque canónico; el único cambio por página es en qué `<a>` va `aria-current="page"`):

```html
<header class="site-header" id="site-header">
  <div class="container site-header__inner">
    <a class="brand" href="index.html">
      <svg class="brand__mark" viewBox="0 0 64 64" width="38" height="38" aria-hidden="true" focusable="false">
        <defs><linearGradient id="brandHead" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stop-color="#0F9B8E"/><stop offset="1" stop-color="#2DD4BF"/>
        </linearGradient></defs>
        <rect width="64" height="64" rx="16" fill="url(#brandHead)"/>
        <path d="M26 16h12v10h10v12H38v10H26V38H16V26h10z" fill="#fff"/>
        <circle cx="47" cy="17" r="6" fill="#FF6B57"/>
      </svg>
      <span class="brand__name">Sanvi</span>
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">
      <span class="nav-toggle__bars" aria-hidden="true"></span>
      <span class="sr-only">Abrir menú de navegación</span>
    </button>
    <nav class="site-nav" id="site-nav" aria-label="Navegación principal">
      <ul class="site-nav__list">
        <li><a href="index.html" aria-current="page">Inicio</a></li>
        <li><a href="servicios.html">Servicios y precios</a></li>
        <li><a href="nosotros.html">Nosotros</a></li>
        <li><a href="contacto.html">Contacto</a></li>
      </ul>
      <a class="btn btn--primary btn--sm site-nav__cta" href="https://wa.me/56978833741?text=Hola%20Sanvi%2C%20quiero%20agendar%20una%20atenci%C3%B3n%20de%20enfermer%C3%ADa%20a%20domicilio%20en%20Calama.">Agendar por WhatsApp</a>
    </nav>
  </div>
</header>
```

Reglas de `aria-current` por página: `index.html` → en el `<a href="index.html">`; `servicios.html` → mover el atributo al `<a href="servicios.html">` y quitarlo del de Inicio; `nosotros.html` → al `<a href="nosotros.html">`; `contacto.html` → al `<a href="contacto.html">`. Exactamente un `aria-current="page"` por página.

Footer (idéntico en las cuatro páginas, sin variaciones):

```html
<footer class="site-footer">
  <div class="container">
    <div class="footer__grid">
      <div class="footer__col">
        <a class="brand" href="index.html" style="color:#fff">
          <svg class="brand__mark" viewBox="0 0 64 64" width="38" height="38" aria-hidden="true" focusable="false">
            <defs><linearGradient id="brandFoot" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0" stop-color="#0F9B8E"/><stop offset="1" stop-color="#2DD4BF"/>
            </linearGradient></defs>
            <rect width="64" height="64" rx="16" fill="url(#brandFoot)"/>
            <path d="M26 16h12v10h10v12H38v10H26V38H16V26h10z" fill="#fff"/>
            <circle cx="47" cy="17" r="6" fill="#FF6B57"/>
          </svg>
          <span class="brand__name">Sanvi</span>
        </a>
        <address class="footer__nap" style="margin-top:1rem">
          <span>Enfermería e inyecciones a domicilio</span>
          <span>Calama, Región de Antofagasta, Chile</span>
          <span>WhatsApp y teléfono: <a href="tel:+56978833741">+56 9 7883 3741</a></span>
          <span>Horario: todos los días, de 8:00 a 21:00, con hora agendada</span>
        </address>
      </div>
      <div class="footer__col">
        <h2>Páginas</h2>
        <ul>
          <li><a href="index.html">Inicio</a></li>
          <li><a href="servicios.html">Servicios y precios</a></li>
          <li><a href="nosotros.html">Nosotros</a></li>
          <li><a href="contacto.html">Contacto</a></li>
        </ul>
      </div>
      <div class="footer__col">
        <h2>Servicios en Calama</h2>
        <ul>
          <li><a href="servicios.html#inyeccion-intramuscular">Inyección intramuscular · $10.000</a></li>
          <li><a href="servicios.html#inyeccion-intravenosa">Inyección intravenosa · $17.000</a></li>
          <li><a href="servicios.html#curacion-simple">Curación simple · $15.000</a></li>
          <li><a href="servicios.html#curacion-compleja">Curación compleja · $33.000</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__note">
      <p>Sanvi no vende medicamentos ni reemplaza la indicación de tu médico tratante. Necesitas receta médica vigente para cualquier administración de fármacos inyectables.</p>
      <p>Ante una emergencia vital, llama al 131 (SAMU). Este sitio no atiende urgencias.</p>
      <p>© 2026 Sanvi · Calama, Chile.</p>
    </div>
  </div>
</footer>

<a class="wa-fab" href="https://wa.me/56978833741?text=Hola%20Sanvi%2C%20quiero%20agendar%20una%20atenci%C3%B3n%20de%20enfermer%C3%ADa%20a%20domicilio%20en%20Calama." aria-label="Agendar por WhatsApp al +56 9 7883 3741">
  <svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" focusable="false">
    <path fill="currentColor" d="M12.04 2C6.6 2 2.2 6.4 2.2 11.84c0 1.94.53 3.75 1.44 5.3L2 22l4.99-1.6a9.8 9.8 0 0 0 5.05 1.38h.01c5.43 0 9.84-4.4 9.84-9.84C21.89 6.4 17.48 2 12.04 2zm5.72 13.9c-.24.68-1.4 1.3-1.94 1.34-.5.05-.98.23-3.3-.7-2.79-1.1-4.56-3.94-4.7-4.13-.13-.19-1.12-1.5-1.12-2.85 0-1.36.71-2.02.96-2.3.25-.27.55-.34.73-.34h.53c.17 0 .4-.06.62.48.24.57.8 1.98.87 2.12.07.14.12.31.02.5-.1.19-.15.31-.29.48-.15.16-.31.37-.44.5-.15.14-.3.3-.13.58.17.29.76 1.25 1.63 2.03 1.12 1 2.06 1.3 2.35 1.45.29.14.46.12.63-.07.17-.2.72-.85.92-1.14.19-.29.38-.24.64-.14.26.09 1.66.78 1.95.93.29.14.48.21.55.33.07.12.07.69-.17 1.36z"/>
  </svg>
  <span class="wa-fab__text">Agendar por WhatsApp</span>
</a>
```

- [ ] **Step 10: Verificar estructura, enlaces y aspecto**

```bash
cd "/c/Users/PC/Desktop/claude/Paginas web con SEO"
python tools/check_site.py sitio-sanvi
python tools/check_links.py sitio-sanvi
```

Esperado en `check_site.py`: `OK: 0 errores, 4 aviso(s) en 4 pagina(s).` Esperado en `check_links.py`: **no** va a imprimir `OK` todavia. El footer que acabas de instalar enlaza `servicios.html#inyeccion-intramuscular`, `#inyeccion-intravenosa`, `#curacion-simple` y `#curacion-compleja` en las 4 paginas, pero esas anclas no existen hasta la Tarea 4 — vas a ver 16 lineas `ERROR: ancla #... no existe en servicios.html` mas los 2 `WARN` de sitemap/robots, y codigo de salida `1`. Es el mismo "rojo esperado que cierra la Tarea 4" que reconoce el Step de verificacion de la Tarea 3: no es un fallo, no lo corrijas aqui.

Levantar el servidor y capturar el header/footer en dos anchos:

```bash
python -m http.server 8080 --directory sitio-sanvi &
python tools/shoot.py http://localhost:8080/index.html --out "$TMPDIR/sanvi-390.png" --width 390 --height 1200
python tools/shoot.py http://localhost:8080/index.html --out "$TMPDIR/sanvi-1280.png" --width 1280 --height 1200
```

Abrir ambos PNG con la herramienta Read. A 390 px debe verse el logo a la izquierda, el botón hamburguesa a la derecha y **ningún** enlace de menú visible; a 1280 px los cuatro enlaces horizontales más el botón coral "Agendar por WhatsApp", sin hamburguesa. En ambos, el footer oscuro con el teléfono `+56 9 7883 3741` y el FAB coral fijo abajo a la derecha. Detener el servidor al terminar.

- [ ] **Step 11: Commit**

```bash
git add sitio-sanvi/assets tools/shoot.py tools/og sitio-sanvi/index.html sitio-sanvi/servicios.html sitio-sanvi/nosotros.html sitio-sanvi/contacto.html
git commit -m "$(cat <<'EOF'
feat: identidad visual y componentes compartidos de Sanvi

Favicon e ilustraciones SVG propias, generacion de og:image/logo/apple-touch-icon
con Chrome headless, components.css con header, nav, botones, tarjetas, tabla de
precios, acordeon FAQ, formulario, footer y FAB de WhatsApp, mas site.js diferido.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---


### Task 3: Página Home

**Files:**
- Modify: `sitio-sanvi/index.html` (reemplazar el `<main>` provisional por el definitivo)
- Create: `sitio-sanvi/assets/css/pages.css`

**Interfaces:**
- Consumes: tokens y utilidades de `base.css`; clases `.section .section--surface .section--tint .section__head .eyebrow .lede .stack .btn .btn--primary .btn--ghost .btn--block .badge-row .badge .card .card__icon .card__title .card__price .price-table .price-table__name .price-table__desc .price-table__price .steps .step .step__num .checklist .checklist--no .callout .callout--warn .faq .faq__item` de `components.css` (Tarea 2); `assets/img/hero-cuidado.svg` y `assets/img/cobertura-calama.svg` (Tarea 2).
- Produces: los `id` de sección `#precios #que-incluye #servicios #como-funciona #cobertura #equipo #opiniones #faq #agendar` (destinos de anclas internas) y las clases de página `.page-hero .hero .hero__media .hero__price .cards-grid .split .coverage__media .coverage__list .commitments .cta-band`, reutilizadas por las Tareas 4–6.

---

- [ ] **Step 1: Crear `assets/css/pages.css`**

Crear `Paginas web con SEO/sitio-sanvi/assets/css/pages.css`:

```css
/* ==========================================================================
   Sanvi - pages.css
   Secciones concretas de pagina. No redefine tokens ni componentes.
   ========================================================================== */

/* ---------- Hero de la home ---------- */
.hero { padding-block: var(--sp-8) var(--section-y); background: var(--grad-soft); }
.hero__grid { display: grid; gap: var(--sp-8); align-items: center; }
.hero h1 { margin-bottom: var(--sp-4); }
.hero .lede { margin-bottom: var(--sp-5); }
.hero__badges { margin-bottom: var(--sp-5); }
.hero__price {
  display: flex; flex-wrap: wrap; align-items: baseline; gap: var(--sp-2) var(--sp-3);
  padding: var(--sp-4) var(--sp-5); margin-bottom: var(--sp-5);
  background: var(--c-surface); border: 1px solid var(--c-line);
  border-radius: var(--r-md); box-shadow: var(--shadow-sm);
}
.hero__price b { font-family: var(--font-display); font-size: var(--fs-700); color: var(--c-teal-900); }
.hero__price span { color: var(--c-muted); font-size: var(--fs-400); }
.hero__actions { display: grid; gap: var(--sp-3); }
.hero__media { order: -1; }
.hero__media img { width: 100%; max-width: 520px; margin-inline: auto; }
@media (min-width: 640px) { .hero__actions { grid-auto-flow: column; justify-content: start; } }
@media (min-width: 900px) {
  .hero__grid { grid-template-columns: 1.05fr .95fr; gap: var(--sp-9); }
  .hero__media { order: 0; }
}

/* ---------- Hero de paginas internas ---------- */
.page-hero { padding-block: var(--sp-8) var(--sp-7); background: var(--grad-soft); }
.page-hero h1 { margin-bottom: var(--sp-4); }

/* ---------- Rejilla de tarjetas ---------- */
.cards-grid { display: grid; gap: var(--sp-5); }
@media (min-width: 640px) { .cards-grid { grid-template-columns: repeat(2, 1fr); } }
@media (min-width: 1200px) { .cards-grid--4 { grid-template-columns: repeat(4, 1fr); } }

/* ---------- Bloque partido ---------- */
.split { display: grid; gap: var(--sp-7); align-items: start; }
@media (min-width: 900px) { .split { grid-template-columns: repeat(2, 1fr); gap: var(--sp-8); } }

/* ---------- Cobertura ---------- */
.coverage__media img { width: 100%; border-radius: var(--r-lg); box-shadow: var(--shadow-sm); }
.coverage__list { display: flex; flex-wrap: wrap; gap: var(--sp-2); list-style: none; padding: 0; margin-top: var(--sp-4); }
.coverage__list li {
  padding: .4rem .85rem; background: var(--c-surface);
  border: 1px solid var(--c-line); border-radius: var(--r-pill); font-size: var(--fs-300);
}

/* ---------- Compromisos ---------- */
.commitments { display: grid; gap: var(--sp-5); list-style: none; padding: 0; }
.commitments li {
  padding: var(--sp-5); background: var(--c-surface);
  border: 1px solid var(--c-line); border-left: 5px solid var(--c-teal-500);
  border-radius: var(--r-md);
}
.commitments h3 { font-size: var(--fs-600); margin-bottom: var(--sp-2); }
.commitments p { color: var(--c-muted); font-size: var(--fs-400); }
@media (min-width: 900px) { .commitments { grid-template-columns: repeat(2, 1fr); } }

/* ---------- Banda de CTA final ---------- */
.cta-band { background: var(--grad-teal); color: #fff; }
.cta-band h2, .cta-band p { color: #fff; }
.cta-band .lede { color: rgba(255, 255, 255, .92); }
.cta-band__inner { display: grid; gap: var(--sp-5); align-items: center; }
.cta-band__actions { display: grid; gap: var(--sp-3); }
@media (min-width: 640px) { .cta-band__actions { grid-auto-flow: column; justify-content: start; } }
@media (min-width: 900px) { .cta-band__inner { grid-template-columns: 1.4fr 1fr; } }

/* ---------- Secciones de servicio (servicios.html) ---------- */
.anchor-nav { display: flex; flex-wrap: wrap; gap: var(--sp-2); list-style: none; padding: 0; margin-top: var(--sp-5); }
.anchor-nav a {
  display: inline-block; padding: .5rem 1rem;
  background: var(--c-surface); border: 1px solid var(--c-line); border-radius: var(--r-pill);
  font-size: var(--fs-300); font-weight: 500; text-decoration: none; color: var(--c-ink);
}
.anchor-nav a:hover { background: var(--c-teal-050); color: var(--c-teal-900); }

.service { padding-block: var(--sp-8); border-top: 1px solid var(--c-line); }
.service:first-of-type { border-top: 0; }
.service__head { display: grid; gap: var(--sp-3); margin-bottom: var(--sp-6); }
.service__price {
  display: inline-flex; align-items: baseline; gap: var(--sp-2);
  padding: .5rem 1.1rem; background: var(--c-teal-050);
  border-radius: var(--r-pill); width: max-content;
}
.service__price b { font-family: var(--font-display); font-size: var(--fs-700); color: var(--c-teal-900); }
.service__price span { font-size: var(--fs-300); color: var(--c-muted); }
.service__meta { display: flex; flex-wrap: wrap; gap: var(--sp-4); color: var(--c-muted); font-size: var(--fs-400); }
.service__body { display: grid; gap: var(--sp-6); }
.service__cta { margin-top: var(--sp-6); }
@media (min-width: 900px) { .service__body { grid-template-columns: repeat(2, 1fr); gap: var(--sp-8); } }

/* ---------- Contacto ---------- */
.contact-grid { display: grid; gap: var(--sp-7); align-items: start; }
@media (min-width: 900px) { .contact-grid { grid-template-columns: 1fr 1fr; gap: var(--sp-8); } }
.contact-card {
  padding: var(--sp-6); background: var(--c-surface);
  border: 1px solid var(--c-line); border-radius: var(--r-lg); box-shadow: var(--shadow-sm);
}
.contact-card h2 { font-size: var(--fs-700); margin-bottom: var(--sp-3); }
.hours-table th, .hours-table td { padding: var(--sp-3) 0; border-bottom: 1px solid var(--c-line); text-align: left; }
.hours-table th { font-weight: 600; }
.hours-table td { text-align: right; color: var(--c-muted); }
.hours-table tr:last-child th, .hours-table tr:last-child td { border-bottom: 0; }
```

- [ ] **Step 2: Escribir el `<main>` definitivo de `index.html`**

Reemplazar íntegramente el bloque `<main id="main"> … </main>` de `sitio-sanvi/index.html` por:

```html
<main id="main">

  <section class="hero">
    <div class="container hero__grid">
      <div>
        <h1>Inyecciones y curaciones a domicilio en Calama</h1>
        <p class="lede">Vamos a tu casa y te aplicamos la inyección o te hacemos la curación que indicó tu médico, con insumos estériles de un solo uso y retiro del material cortopunzante.</p>
        <ul class="badge-row hero__badges">
          <li class="badge">Técnicos en enfermería de nivel superior</li>
          <li class="badge">Insumos estériles de un solo uso</li>
          <li class="badge">Todos los días, de 8:00 a 21:00</li>
          <li class="badge">Solo Calama</li>
        </ul>
        <p class="hero__price"><b>Desde $10.000</b> <span>Precios publicados en esta página. Te confirmamos el valor final por WhatsApp antes de salir.</span></p>
        <div class="hero__actions">
          <a class="btn btn--primary" href="https://wa.me/56978833741?text=Hola%20Sanvi%2C%20quiero%20agendar%20una%20atenci%C3%B3n%20de%20enfermer%C3%ADa%20a%20domicilio%20en%20Calama.">Agendar por WhatsApp</a>
          <a class="btn btn--ghost" href="#precios">Ver precios</a>
        </div>
      </div>
      <div class="hero__media">
        <img src="assets/img/hero-cuidado.svg" width="520" height="460" alt="Ilustración de una visita de enfermería a domicilio en Calama" fetchpriority="high" decoding="async">
      </div>
    </div>
  </section>

  <section class="section section--surface" id="precios">
    <div class="container">
      <div class="section__head">
        <p class="eyebrow">Precios</p>
        <h2>Cuánto cuesta cada servicio en Calama</h2>
        <p class="lede">Publicamos los precios porque creemos que preguntar cuánto cuesta una inyección no debería costar una conversación de diez minutos.</p>
      </div>
      <table class="price-table">
        <caption>Valores en pesos chilenos, vigentes para atención dentro de Calama.</caption>
        <thead>
          <tr><th scope="col">Servicio</th><th scope="col">En qué consiste</th><th scope="col">Precio</th></tr>
        </thead>
        <tbody>
          <tr>
            <td class="price-table__name"><a href="servicios.html#inyeccion-intramuscular">Inyección intramuscular</a></td>
            <td class="price-table__desc" data-label="En qué consiste">Incluye multivitamínicos del complejo B (como Neurobionta) y el anticonceptivo inyectable mensual.</td>
            <td class="price-table__price" data-label="Precio">$10.000</td>
          </tr>
          <tr>
            <td class="price-table__name"><a href="servicios.html#inyeccion-intravenosa">Inyección intravenosa</a></td>
            <td class="price-table__desc" data-label="En qué consiste">Administración por vía endovenosa del medicamento indicado por tu médico tratante.</td>
            <td class="price-table__price" data-label="Precio">$17.000</td>
          </tr>
          <tr>
            <td class="price-table__name"><a href="servicios.html#curacion-simple">Curación simple</a></td>
            <td class="price-table__desc" data-label="En qué consiste">Heridas limpias y de poca extensión: aseo, cobertura estéril y control del cierre.</td>
            <td class="price-table__price" data-label="Precio">$15.000</td>
          </tr>
          <tr>
            <td class="price-table__name"><a href="servicios.html#curacion-compleja">Curación compleja</a></td>
            <td class="price-table__desc" data-label="En qué consiste">Heridas extensas, con tejido desvitalizado o de cicatrización lenta, con manejo avanzado.</td>
            <td class="price-table__price" data-label="Precio">$33.000</td>
          </tr>
        </tbody>
      </table>
      <p style="margin-top:1.5rem;color:var(--c-muted)">El precio incluye el traslado dentro de Calama, los insumos estériles del procedimiento y el retiro del material cortopunzante. El medicamento no está incluido y debe aportarlo el paciente.</p>
    </div>
  </section>

  <section class="section" id="que-incluye">
    <div class="container">
      <div class="section__head">
        <p class="eyebrow">Transparencia</p>
        <h2>Qué incluye y qué no incluye la visita</h2>
      </div>
      <div class="split">
        <div class="stack">
          <h3>Sí está incluido</h3>
          <ul class="checklist">
            <li>El traslado hasta tu domicilio, dentro de Calama.</li>
            <li>La revisión de tu receta médica y de que el medicamento corresponda a la indicación.</li>
            <li>Jeringa, aguja, antiséptico y apósitos estériles de un solo uso, abiertos delante de ti.</li>
            <li>El procedimiento realizado con técnica aséptica por un técnico en enfermería de nivel superior.</li>
            <li>El retiro de todo el material cortopunzante en un contenedor normado.</li>
          </ul>
        </div>
        <div class="stack">
          <h3>No está incluido</h3>
          <ul class="checklist checklist--no">
            <li>El medicamento. En Chile su venta corresponde exclusivamente a farmacias autorizadas.</li>
            <li>El diagnóstico médico o el cambio de tu indicación: trabajamos con la receta de tu médico tratante.</li>
            <li>La atención fuera de Calama.</li>
            <li>Las urgencias vitales. Ante una emergencia, llama al 131 (SAMU).</li>
          </ul>
        </div>
      </div>
      <div class="callout callout--warn" style="margin-top:2rem">
        <h3>Necesitas receta médica vigente</h3>
        <p>Antes de agendar, ten a mano la receta y el medicamento. Si la receta no está vigente o el fármaco no corresponde a la indicación, te lo decimos por WhatsApp antes de salir, no realizamos el procedimiento y no cobramos la visita.</p>
      </div>
    </div>
  </section>

  <section class="section section--surface" id="servicios">
    <div class="container">
      <div class="section__head">
        <p class="eyebrow">Servicios</p>
        <h2>Qué hacemos a domicilio en Calama</h2>
        <p class="lede">Cuatro servicios, cada uno con su precio, su duración estimada y sus requisitos explicados en detalle.</p>
      </div>
      <div class="cards-grid cards-grid--4">
        <article class="card">
          <span class="card__icon" aria-hidden="true">IM</span>
          <h3 class="card__title"><a href="servicios.html#inyeccion-intramuscular">Inyección intramuscular</a></h3>
          <p>Multivitamínicos del complejo B, anticonceptivo inyectable mensual y cualquier fármaco intramuscular con receta.</p>
          <p class="card__price">$10.000</p>
        </article>
        <article class="card">
          <span class="card__icon" aria-hidden="true">IV</span>
          <h3 class="card__title"><a href="servicios.html#inyeccion-intravenosa">Inyección intravenosa</a></h3>
          <p>Administración endovenosa con vigilancia durante y después del procedimiento.</p>
          <p class="card__price">$17.000</p>
        </article>
        <article class="card">
          <span class="card__icon" aria-hidden="true">CS</span>
          <h3 class="card__title"><a href="servicios.html#curacion-simple">Curación simple</a></h3>
          <p>Heridas limpias y de poca extensión: aseo, cobertura estéril y seguimiento del cierre.</p>
          <p class="card__price">$15.000</p>
        </article>
        <article class="card">
          <span class="card__icon" aria-hidden="true">CC</span>
          <h3 class="card__title"><a href="servicios.html#curacion-compleja">Curación compleja</a></h3>
          <p>Heridas extensas o de cicatrización lenta, con manejo avanzado y control programado.</p>
          <p class="card__price">$33.000</p>
        </article>
      </div>
    </div>
  </section>

  <section class="section" id="como-funciona">
    <div class="container">
      <div class="section__head">
        <p class="eyebrow">Cómo funciona</p>
        <h2>Agendar toma menos de un minuto</h2>
      </div>
      <ol class="steps">
        <li class="step">
          <span class="step__num" aria-hidden="true">1</span>
          <div>
            <h3>Escríbenos por WhatsApp</h3>
            <p>Cuéntanos qué necesitas y envíanos una foto de la receta. Revisamos que esté vigente y te confirmamos el precio final antes de salir.</p>
          </div>
        </li>
        <li class="step">
          <span class="step__num" aria-hidden="true">2</span>
          <div>
            <h3>Elegimos la hora</h3>
            <p>Acordamos un bloque entre las 8:00 y las 21:00, cualquier día de la semana. Trabajamos siempre con hora agendada: no atendemos sin cita previa.</p>
          </div>
        </li>
        <li class="step">
          <span class="step__num" aria-hidden="true">3</span>
          <div>
            <h3>Llegamos a tu casa</h3>
            <p>Llegamos con los insumos, te explicamos el procedimiento, lo realizamos con técnica aséptica y nos llevamos todo el material cortopunzante.</p>
          </div>
        </li>
      </ol>
    </div>
  </section>

  <section class="section section--tint" id="cobertura">
    <div class="container split">
      <div class="stack">
        <p class="eyebrow">Cobertura</p>
        <h2>Atendemos en Calama</h2>
        <p>Trabajamos dentro del radio urbano de Calama, en la Región de Antofagasta. Llegamos a todos los sectores de la ciudad, incluidos el centro, Villa Ayquina y Kamac Mayu.</p>
        <p>Por ahora no atendemos fuera de Calama: no cubrimos Chuquicamata, Chiu Chiu, San Pedro de Atacama ni otras localidades de la provincia de El Loa. Preferimos decírtelo antes que hacerte esperar una visita que no vamos a poder hacer.</p>
        <ul class="coverage__list">
          <li>Centro de Calama</li>
          <li>Villa Ayquina</li>
          <li>Kamac Mayu</li>
          <li>Resto del radio urbano</li>
        </ul>
      </div>
      <div class="coverage__media">
        <img src="assets/img/cobertura-calama.svg" width="420" height="300" alt="Mapa estilizado del área de cobertura de Sanvi dentro del radio urbano de Calama" loading="lazy" decoding="async">
      </div>
    </div>
  </section>

  <section class="section" id="equipo">
    <div class="container split">
      <div class="stack">
        <p class="eyebrow">Quién te atiende</p>
        <h2>Personal técnico en enfermería, no improvisado</h2>
        <p>La atención de Sanvi la realizan técnicos en enfermería de nivel superior, titulados y registrados ante la autoridad sanitaria. Llegamos identificados, te explicamos el procedimiento antes de empezar y respondemos tus dudas sin apuro.</p>
        <p>Cuando lleguemos a tu casa puedes pedirnos la credencial y el número de registro del profesional que te atiende, y verificarlo tú mismo en el buscador de la Superintendencia de Salud. Si alguien ofrece inyecciones a domicilio y no puede darte el suyo, no lo dejes entrar.</p>
        <p><a href="nosotros.html">Conoce cómo trabajamos y nuestro protocolo de bioseguridad</a></p>
      </div>
      <div class="callout">
        <h3>Cómo verificar a quien te atiende</h3>
        <p>La Superintendencia de Salud de Chile mantiene un buscador público y gratuito del Registro Nacional de Prestadores Individuales de Salud. Pídenos el número, búscalo y comprueba que la persona que está en tu casa es quien dice ser.</p>
        <p><a href="https://www.superdesalud.gob.cl/" target="_blank" rel="noopener">Superintendencia de Salud de Chile</a></p>
      </div>
    </div>
  </section>

  <section class="section section--surface" id="opiniones">
    <div class="container">
      <div class="section__head">
        <p class="eyebrow">Nuestros compromisos</p>
        <h2>Lo que te garantizamos en cada visita</h2>
        <p class="lede">Todavía no publicamos opiniones porque preferimos no mostrar ninguna antes que mostrar una inventada. Mientras tanto, esto es lo que sí puedes exigirnos.</p>
      </div>
      <ul class="commitments">
        <li>
          <h3>El precio que ves es el que pagas</h3>
          <p>No cobramos recargo por horario, por sector de Calama ni por fin de semana. Si algo cambiara, te lo decimos por WhatsApp antes de salir.</p>
        </li>
        <li>
          <h3>Primero la receta, después la visita</h3>
          <p>Revisamos tu receta antes de movernos. Si no está vigente o el medicamento no corresponde, no realizamos el procedimiento y no cobramos nada.</p>
        </li>
        <li>
          <h3>Material estéril abierto delante de ti</h3>
          <p>Jeringa, aguja y apósitos son de un solo uso y se abren en tu presencia. Nunca reutilizamos insumos.</p>
        </li>
        <li>
          <h3>Cero agujas en tu basura</h3>
          <p>Retiramos todo el material cortopunzante en un contenedor normado y lo eliminamos según la reglamentación sanitaria vigente.</p>
        </li>
      </ul>
    </div>
  </section>

  <section class="section" id="faq">
    <div class="container">
      <div class="section__head">
        <p class="eyebrow">Preguntas frecuentes</p>
        <h2>Lo que más nos preguntan por WhatsApp</h2>
      </div>
      <div class="faq">
        <details class="faq__item" name="faq-home">
          <summary>¿Necesito receta médica para una inyección a domicilio en Calama?</summary>
          <div><p>Sí. En Chile se exige receta médica vigente para administrar cualquier medicamento inyectable, incluidos el anticonceptivo mensual y el complejo vitamínico B. Revisamos la receta antes de aplicar y, si no la tienes, no realizamos el procedimiento y no cobramos la visita.</p></div>
        </details>
        <details class="faq__item" name="faq-home">
          <summary>¿Cuánto cuesta una inyección a domicilio en Calama?</summary>
          <div><p>Una inyección intramuscular a domicilio en Calama cuesta $10.000 y una intravenosa, $17.000. El valor incluye el traslado dentro de Calama, los insumos estériles y el retiro del material cortopunzante.</p></div>
        </details>
        <details class="faq__item" name="faq-home">
          <summary>¿El precio incluye el medicamento?</summary>
          <div><p>No. El medicamento debe aportarlo el paciente, porque en Chile la venta de fármacos corresponde exclusivamente a farmacias autorizadas. Nosotros llevamos la jeringa, la aguja, el antiséptico y el contenedor de residuos.</p></div>
        </details>
        <details class="faq__item" name="faq-home">
          <summary>¿En qué horario atienden?</summary>
          <div><p>Atendemos todos los días de 8:00 a 21:00, siempre con hora agendada previamente por WhatsApp.</p></div>
        </details>
        <details class="faq__item" name="faq-home">
          <summary>¿Atienden sin cita previa?</summary>
          <div><p>No. Trabajamos exclusivamente con agendamiento previo para poder confirmarte una hora de llegada realista y llevar los insumos correctos para tu procedimiento.</p></div>
        </details>
        <details class="faq__item" name="faq-home">
          <summary>¿Qué sectores de Calama cubren?</summary>
          <div><p>Cubrimos todo el radio urbano de Calama, incluidos el centro, Villa Ayquina y Kamac Mayu. No atendemos fuera de Calama.</p></div>
        </details>
        <details class="faq__item" name="faq-home">
          <summary>¿Qué hacen con la jeringa después de aplicarla?</summary>
          <div><p>Retiramos todo el material cortopunzante en un contenedor normado y lo eliminamos según la reglamentación sanitaria chilena de residuos de establecimientos de atención de salud. Nunca dejamos agujas en tu basura domiciliaria.</p></div>
        </details>
        <details class="faq__item" name="faq-home">
          <summary>¿Cómo sé que quien me atiende es realmente personal de enfermería?</summary>
          <div><p>Puedes pedirnos la credencial y el número de registro del profesional que llega a tu domicilio y verificarlo gratis en el buscador de la Superintendencia de Salud de Chile. Llegamos identificados y te explicamos el procedimiento antes de comenzar.</p></div>
        </details>
      </div>
    </div>
  </section>

  <section class="section cta-band" id="agendar">
    <div class="container cta-band__inner">
      <div>
        <h2>Agenda tu visita en Calama</h2>
        <p class="lede">Escríbenos por WhatsApp con una foto de tu receta y te confirmamos hora y precio final antes de salir. Todos los días, de 8:00 a 21:00.</p>
      </div>
      <div class="cta-band__actions">
        <a class="btn btn--primary" href="https://wa.me/56978833741?text=Hola%20Sanvi%2C%20quiero%20agendar%20una%20atenci%C3%B3n%20de%20enfermer%C3%ADa%20a%20domicilio%20en%20Calama.">Agendar por WhatsApp</a>
        <a class="btn btn--ghost" href="tel:+56978833741">Llamar al +56 9 7883 3741</a>
      </div>
    </div>
  </section>

</main>
```

- [ ] **Step 3: Verificar estructura y contenido**

```bash
cd "/c/Users/PC/Desktop/claude/Paginas web con SEO"
python tools/check_site.py sitio-sanvi/index.html --content
python tools/check_links.py sitio-sanvi
```

Esperado en el primero: un único `WARN … sin bloque JSON-LD` y `OK: 0 errores`. Si aparece `ERROR index.html: N palabras visibles, minimo 700`, faltó copy: no rellenar, revisar que se pegaron todas las secciones. El segundo debe seguir en `OK` salvo los avisos de sitemap/robots (las anclas `servicios.html#…` sólo resolverán tras la Tarea 4; hasta entonces `check_links.py` reportará `ancla #inyeccion-intramuscular no existe en servicios.html` — es el rojo esperado que cierra la Tarea 4).

- [ ] **Step 4: Verificar visualmente en los tres breakpoints**

```bash
python -m http.server 8080 --directory sitio-sanvi &
python tools/shoot.py http://localhost:8080/index.html --out "$TMPDIR/home-390.png"  --width 390  --height 5200
python tools/shoot.py http://localhost:8080/index.html --out "$TMPDIR/home-900.png"  --width 900  --height 4600
python tools/shoot.py http://localhost:8080/index.html --out "$TMPDIR/home-1280.png" --width 1280 --height 4400
```

Abrir las tres capturas con Read y comprobar: (a) a 390 px el hero muestra la ilustración arriba, luego titular, badges, línea de precio y los dos botones apilados a ancho completo; (b) la tabla de precios se ve como tarjetas apiladas a 390 px y como tabla de tres columnas a 900 y 1280; (c) las cuatro tarjetas de servicio están en 1 columna a 390, 2 a 900 y 4 a 1280; (d) ningún texto se desborda ni se solapa con el FAB; (e) la banda final turquesa tiene el botón coral legible. Detener el servidor.

- [ ] **Step 5: Commit**

```bash
git add sitio-sanvi/index.html sitio-sanvi/assets/css/pages.css
git commit -m "$(cat <<'EOF'
feat: pagina Home completa de Sanvi

Hero estructura B (titular, badges, linea de precio, CTA WhatsApp), tabla de
precios de los 4 servicios, que incluye/no incluye con aviso de receta, resumen
de servicios con anclas, 3 pasos, cobertura, credenciales, compromisos, FAQ de
8 preguntas y CTA final. Anade pages.css con las secciones de pagina.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 4: Página Servicios

**Files:**
- Modify: `sitio-sanvi/servicios.html` (reemplazar el `<main>` provisional)

**Interfaces:**
- Consumes: `.page-hero .anchor-nav .service .service__head .service__price .service__meta .service__body .service__cta .faq .faq__item .checklist .checklist--no .callout .cta-band` de `pages.css`/`components.css`.
- Produces: los `id` `#inyeccion-intramuscular #inyeccion-intravenosa #curacion-simple #curacion-compleja #preguntas #agendar`, destino de las anclas que ya emiten `index.html` (Tarea 3) y el footer (Tarea 2), y de los `url` de los nodos `Service` del JSON-LD (Tarea 7).

---

- [ ] **Step 1: Escribir el `<main>` definitivo de `servicios.html`**

Reemplazar el bloque `<main id="main"> … </main>` de `sitio-sanvi/servicios.html` por:

```html
<main id="main">

  <section class="page-hero">
    <div class="container">
      <p class="eyebrow">Servicios y precios</p>
      <h1>Servicios y precios de enfermería a domicilio en Calama</h1>
      <p class="lede">Cuatro servicios, cada uno con su precio publicado, su duración estimada y sus requisitos. Todos se realizan en tu domicilio, dentro de Calama, de 8:00 a 21:00 y con hora agendada.</p>
      <ul class="anchor-nav">
        <li><a href="#inyeccion-intramuscular">Inyección intramuscular · $10.000</a></li>
        <li><a href="#inyeccion-intravenosa">Inyección intravenosa · $17.000</a></li>
        <li><a href="#curacion-simple">Curación simple · $15.000</a></li>
        <li><a href="#curacion-compleja">Curación compleja · $33.000</a></li>
      </ul>
    </div>
  </section>

  <div class="container">

    <section class="service" id="inyeccion-intramuscular">
      <div class="service__head">
        <h2>Inyección intramuscular a domicilio</h2>
        <p class="service__price"><b>$10.000</b> <span>por aplicación, en Calama</span></p>
        <p class="service__meta"><span>Duración estimada: 15 a 20 minutos</span> <span>Requiere receta médica vigente</span></p>
      </div>
      <p class="lede">Aplicamos en tu casa cualquier medicamento de administración intramuscular indicado por tu médico, incluidos los multivitamínicos del complejo B (como Neurobionta) y el anticonceptivo inyectable mensual.</p>
      <div class="service__body">
        <div class="stack">
          <h3>Qué incluye</h3>
          <ul class="checklist">
            <li>Revisión de tu receta y verificación de que el medicamento corresponde a la indicación.</li>
            <li>Jeringa, aguja, antiséptico y apósito estériles de un solo uso.</li>
            <li>Aplicación con técnica aséptica por un técnico en enfermería de nivel superior.</li>
            <li>Indicaciones posteriores y señales de alerta que debes vigilar.</li>
            <li>Retiro del material cortopunzante en contenedor normado.</li>
          </ul>
        </div>
        <div class="stack">
          <h3>Qué necesitas tener listo</h3>
          <ul class="checklist">
            <li>La receta médica vigente, en papel o en foto legible.</li>
            <li>El medicamento en su envase original, sin abrir y dentro de su fecha de vencimiento.</li>
            <li>Un espacio con buena luz donde puedas sentarte o recostarte.</li>
          </ul>
          <h3>Qué no hacemos</h3>
          <ul class="checklist checklist--no">
            <li>No vendemos ni suministramos el medicamento.</li>
            <li>No cambiamos la dosis ni la vía indicada por tu médico.</li>
          </ul>
        </div>
      </div>
      <p class="service__cta"><a class="btn btn--primary" href="https://wa.me/56978833741?text=Hola%20Sanvi%2C%20quiero%20agendar%20una%20inyecci%C3%B3n%20intramuscular%20a%20domicilio%20en%20Calama%20(%2410.000).">Agendar inyección intramuscular</a></p>
    </section>

    <section class="service" id="inyeccion-intravenosa">
      <div class="service__head">
        <h2>Inyección intravenosa a domicilio</h2>
        <p class="service__price"><b>$17.000</b> <span>por administración, en Calama</span></p>
        <p class="service__meta"><span>Duración estimada: 30 a 45 minutos</span> <span>Requiere receta médica vigente</span></p>
      </div>
      <p class="lede">Administramos por vía endovenosa el medicamento que indicó tu médico tratante, con vigilancia durante el procedimiento y en los minutos posteriores. Es un procedimiento de mayor complejidad que el intramuscular, por eso toma más tiempo y tiene un valor distinto.</p>
      <div class="service__body">
        <div class="stack">
          <h3>Qué incluye</h3>
          <ul class="checklist">
            <li>Revisión de la receta y de la compatibilidad del medicamento con la vía endovenosa.</li>
            <li>Bránula o mariposa, jeringa, antiséptico y apósito estériles de un solo uso.</li>
            <li>Punción venosa y administración a la velocidad indicada.</li>
            <li>Vigilancia de reacciones durante y después de la administración.</li>
            <li>Retiro del acceso venoso y de todo el material cortopunzante.</li>
          </ul>
        </div>
        <div class="stack">
          <h3>Qué necesitas tener listo</h3>
          <ul class="checklist">
            <li>La receta médica vigente que especifique la vía intravenosa.</li>
            <li>El medicamento y el diluyente, si la indicación lo requiere.</li>
            <li>Un acompañante en el domicilio durante el procedimiento.</li>
          </ul>
          <h3>Cuándo no lo realizamos</h3>
          <ul class="checklist checklist--no">
            <li>Si la receta no especifica la vía intravenosa.</li>
            <li>Si presentas signos de una emergencia que requiera atención hospitalaria. En ese caso te indicamos llamar al 131.</li>
          </ul>
        </div>
      </div>
      <p class="service__cta"><a class="btn btn--primary" href="https://wa.me/56978833741?text=Hola%20Sanvi%2C%20quiero%20agendar%20una%20inyecci%C3%B3n%20intravenosa%20a%20domicilio%20en%20Calama%20(%2417.000).">Agendar inyección intravenosa</a></p>
    </section>

    <section class="service" id="curacion-simple">
      <div class="service__head">
        <h2>Curación simple a domicilio</h2>
        <p class="service__price"><b>$15.000</b> <span>por curación, en Calama</span></p>
        <p class="service__meta"><span>Duración estimada: 20 a 30 minutos</span> <span>Para heridas limpias y de poca extensión</span></p>
      </div>
      <p class="lede">Es la curación de heridas limpias, de bordes definidos y poca extensión: cortes suturados, heridas quirúrgicas en buena evolución, escoriaciones o quemaduras superficiales pequeñas. Incluye el aseo de la herida, la cobertura estéril y el control de cómo va cerrando.</p>
      <div class="service__body">
        <div class="stack">
          <h3>Qué incluye</h3>
          <ul class="checklist">
            <li>Valoración del aspecto de la herida y de los signos de infección.</li>
            <li>Aseo con suero fisiológico y antiséptico según corresponda.</li>
            <li>Cobertura con apósito estéril adecuado al tipo de herida.</li>
            <li>Indicaciones de cuidado y señales por las que debes consultar a tu médico.</li>
            <li>Retiro del material contaminado en contenedor normado.</li>
          </ul>
        </div>
        <div class="stack">
          <h3>Qué necesitas tener listo</h3>
          <ul class="checklist">
            <li>La indicación médica de curación, si la tienes, y los apósitos especiales que te hayan recetado.</li>
            <li>Una superficie limpia y despejada donde apoyar el material.</li>
          </ul>
          <h3>Cuándo pasa a ser curación compleja</h3>
          <ul class="checklist checklist--no">
            <li>Si la herida tiene tejido desvitalizado, mucho exudado, mal olor o profundidad importante, corresponde una curación compleja y te lo decimos antes de empezar, sin cobrarte la diferencia sin avisar.</li>
          </ul>
        </div>
      </div>
      <p class="service__cta"><a class="btn btn--primary" href="https://wa.me/56978833741?text=Hola%20Sanvi%2C%20quiero%20agendar%20una%20curaci%C3%B3n%20simple%20a%20domicilio%20en%20Calama%20(%2415.000).">Agendar curación simple</a></p>
    </section>

    <section class="service" id="curacion-compleja">
      <div class="service__head">
        <h2>Curación compleja a domicilio</h2>
        <p class="service__price"><b>$33.000</b> <span>por curación, en Calama</span></p>
        <p class="service__meta"><span>Duración estimada: 45 a 60 minutos</span> <span>Requiere indicación médica</span></p>
      </div>
      <p class="lede">Es la curación de heridas extensas, profundas o de cicatrización lenta: úlceras por presión, pie diabético, heridas con tejido desvitalizado o con abundante exudado. Requiere más tiempo, más material y una valoración en cada visita, por eso su valor es mayor.</p>
      <div class="service__body">
        <div class="stack">
          <h3>Qué incluye</h3>
          <ul class="checklist">
            <li>Valoración de la herida: extensión, profundidad, tipo de tejido y exudado.</li>
            <li>Aseo, arrastre mecánico y manejo del tejido no viable cuando está indicado.</li>
            <li>Cobertura avanzada acorde al tipo de herida.</li>
            <li>Registro de la evolución para que puedas mostrárselo a tu médico tratante.</li>
            <li>Programación de la siguiente curación y retiro del material contaminado.</li>
          </ul>
        </div>
        <div class="stack">
          <h3>Qué necesitas tener listo</h3>
          <ul class="checklist">
            <li>La indicación médica y los antecedentes de la herida, si es una curación de seguimiento.</li>
            <li>Los apósitos avanzados recetados, si tu médico indicó alguno en particular.</li>
          </ul>
          <h3>Qué no hacemos</h3>
          <ul class="checklist checklist--no">
            <li>No realizamos desbridamiento quirúrgico ni procedimientos que requieran pabellón.</li>
            <li>No reemplazamos el control médico de la herida: la curación acompaña ese control, no lo sustituye.</li>
          </ul>
        </div>
      </div>
      <p class="service__cta"><a class="btn btn--primary" href="https://wa.me/56978833741?text=Hola%20Sanvi%2C%20quiero%20agendar%20una%20curaci%C3%B3n%20compleja%20a%20domicilio%20en%20Calama%20(%2433.000).">Agendar curación compleja</a></p>
    </section>

  </div>

  <section class="section section--surface" id="preguntas">
    <div class="container">
      <div class="section__head">
        <p class="eyebrow">Precios y requisitos</p>
        <h2>Preguntas sobre nuestros servicios</h2>
      </div>
      <div class="faq">
        <details class="faq__item" name="faq-servicios">
          <summary>¿Los precios cambian según el sector de Calama o el horario?</summary>
          <div><p>No. El precio publicado es el mismo en todo el radio urbano de Calama y a cualquier hora dentro de nuestro horario de 8:00 a 21:00, todos los días de la semana.</p></div>
        </details>
        <details class="faq__item" name="faq-servicios">
          <summary>¿Puedo agendar varias aplicaciones seguidas, como un tratamiento de complejo B?</summary>
          <div><p>Sí. Puedes agendar todas las visitas del tratamiento en una sola conversación de WhatsApp y te dejamos la agenda cerrada. Cada aplicación se cobra por separado según el precio publicado.</p></div>
        </details>
        <details class="faq__item" name="faq-servicios">
          <summary>¿Qué pasa si la herida resulta más compleja de lo que pensábamos?</summary>
          <div><p>Te lo decimos antes de comenzar el procedimiento y decides tú. Nunca cambiamos el valor acordado sin avisarte primero y explicarte por qué la curación cambia de categoría.</p></div>
        </details>
        <details class="faq__item" name="faq-servicios">
          <summary>¿Atienden niños o adultos mayores?</summary>
          <div><p>Sí, siempre con la receta médica correspondiente y con un adulto responsable presente en el domicilio durante toda la atención.</p></div>
        </details>
      </div>
    </div>
  </section>

  <section class="section cta-band" id="agendar">
    <div class="container cta-band__inner">
      <div>
        <h2>¿No sabes qué servicio necesitas?</h2>
        <p class="lede">Escríbenos con una foto de tu receta o de la indicación médica y te decimos exactamente cuál corresponde y cuánto cuesta, antes de agendar. Todos los días, de 8:00 a 21:00, en Calama.</p>
      </div>
      <div class="cta-band__actions">
        <a class="btn btn--primary" href="https://wa.me/56978833741?text=Hola%20Sanvi%2C%20tengo%20una%20duda%20sobre%20qu%C3%A9%20servicio%20necesito%20a%20domicilio%20en%20Calama.">Preguntar por WhatsApp</a>
        <a class="btn btn--ghost" href="contacto.html">Ver contacto y cobertura</a>
      </div>
    </div>
  </section>

</main>
```

- [ ] **Step 2: Verificar**

```bash
cd "/c/Users/PC/Desktop/claude/Paginas web con SEO"
python tools/check_site.py sitio-sanvi/servicios.html --content
python tools/check_links.py sitio-sanvi
```

Esperado: en el primero un único `WARN` de JSON-LD y `OK: 0 errores`. En el segundo, desaparecen los errores `ancla #inyeccion-intramuscular no existe en servicios.html` (y sus tres hermanos): debe quedar `OK: todos los enlaces internos, anclas y assets resuelven` más los dos `WARN` de sitemap/robots.

- [ ] **Step 3: Verificar visualmente**

```bash
python -m http.server 8080 --directory sitio-sanvi &
python tools/shoot.py http://localhost:8080/servicios.html --out "$TMPDIR/serv-390.png"  --width 390  --height 6000
python tools/shoot.py http://localhost:8080/servicios.html --out "$TMPDIR/serv-1280.png" --width 1280 --height 4800
```

Leer ambas capturas y comprobar: los cuatro precios `$10.000`, `$17.000`, `$15.000`, `$33.000` aparecen en píldoras turquesa; las listas "Qué incluye" / "Qué necesitas" se apilan a 390 px y van en dos columnas a 1280 px; los chips de navegación por anclas envuelven sin cortarse. Detener el servidor.

- [ ] **Step 4: Commit**

```bash
git add sitio-sanvi/servicios.html
git commit -m "$(cat <<'EOF'
feat: pagina Servicios con los 4 servicios en profundidad

Cada servicio con id-ancla propio, precio, duracion estimada, que incluye, que
necesitas tener listo, limites del servicio y CTA de WhatsApp con mensaje
precargado especifico. Anade FAQ de precios y requisitos.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 5: Página Nosotros

**Files:**
- Modify: `sitio-sanvi/nosotros.html` (reemplazar el `<main>` provisional)

**Interfaces:**
- Consumes: `.page-hero .split .stack .checklist .checklist--no .callout .cards-grid .card .cta-band` ya definidas.
- Produces: los `id` `#historia #bioseguridad #domicilio-o-clinica #equipo #limites`, enlazables desde la Home (Tarea 3 ya enlaza `nosotros.html` sin fragmento) y desde el JSON-LD `AboutPage` (Tarea 7).

---

- [ ] **Step 1: Escribir el `<main>` definitivo de `nosotros.html`**

Reemplazar el bloque `<main id="main"> … </main>` de `sitio-sanvi/nosotros.html` por:

```html
<main id="main">

  <section class="page-hero">
    <div class="container">
      <p class="eyebrow">Nosotros</p>
      <h1>Quiénes somos: enfermería a domicilio en Calama</h1>
      <p class="lede">Somos Sanvi. Llevamos la atención de enfermería a las casas de Calama para que recibir una inyección o una curación no signifique perder media mañana en una fila.</p>
    </div>
  </section>

  <section class="section" id="historia">
    <div class="container split">
      <div class="stack">
        <h2>Cómo partimos</h2>
        <p>Sanvi nació en Calama con una idea simple: hay procedimientos de enfermería que no necesitan un box clínico. Una inyección intramuscular, un anticonceptivo mensual, la curación de una herida en buena evolución. Son atenciones breves, seguras y perfectamente realizables en el domicilio del paciente, hechas por personal técnico titulado.</p>
        <p>Lo que sí necesitan es orden: revisar la receta antes de aplicar, usar material estéril de un solo uso, explicar el procedimiento y llevarse los residuos. Eso es lo que hacemos, y lo hacemos siempre igual, tanto si la visita es un martes a las nueve de la mañana como un domingo a las ocho de la tarde.</p>
        <p>Atendemos únicamente en Calama. Preferimos cubrir bien una ciudad antes que prometer una cobertura que no podemos sostener.</p>
      </div>
      <div class="callout">
        <h3>Nuestra forma de trabajar, en una frase</h3>
        <p>Precio publicado antes de agendar, receta revisada antes de salir, material abierto delante tuyo y ninguna aguja abandonada en tu basura.</p>
      </div>
    </div>
  </section>

  <section class="section section--surface" id="bioseguridad">
    <div class="container">
      <div class="section__head">
        <p class="eyebrow">Bioseguridad</p>
        <h2>Nuestro protocolo de higiene y bioseguridad</h2>
        <p class="lede">Trabajar fuera de un recinto de salud no autoriza a trabajar con menos rigor. Este es el procedimiento que seguimos en cada visita, sin excepciones.</p>
      </div>
      <ul class="checklist">
        <li><strong>Higiene de manos antes y después.</strong> Lavado o desinfección con solución de base alcohólica al llegar, antes del procedimiento y al terminar.</li>
        <li><strong>Material estéril de un solo uso.</strong> Jeringas, agujas, apósitos y guantes se abren delante del paciente y nunca se reutilizan.</li>
        <li><strong>Antisepsia de la zona.</strong> Preparación de la piel con antiséptico antes de cualquier punción o curación.</li>
        <li><strong>Verificación de los cinco correctos.</strong> Paciente correcto, medicamento correcto, dosis correcta, vía correcta y horario correcto, contrastados con la receta antes de administrar.</li>
        <li><strong>Manejo del cortopunzante.</strong> La aguja no se re-encapucha: va directo al contenedor rígido normado que llevamos y que se retira del domicilio.</li>
        <li><strong>Eliminación de residuos según norma.</strong> Todo el material contaminado sale de tu casa con nosotros y se elimina según la reglamentación sanitaria chilena de residuos de establecimientos de atención de salud.</li>
        <li><strong>Registro de la atención.</strong> Dejamos constancia de qué se aplicó, cuándo y qué indicaciones se dieron, para que puedas mostrárselo a tu médico tratante.</li>
      </ul>
    </div>
  </section>

  <section class="section" id="domicilio-o-clinica">
    <div class="container">
      <div class="section__head">
        <p class="eyebrow">Cuándo conviene cada opción</p>
        <h2>Atención a domicilio o atención en un box clínico</h2>
        <p class="lede">No siempre la mejor opción es que vayamos a tu casa. Esto es lo que consideramos honesto decirte.</p>
      </div>
      <div class="cards-grid">
        <article class="card">
          <span class="card__icon" aria-hidden="true">✚</span>
          <h3 class="card__title">Conviene el domicilio</h3>
          <p>Cuando el traslado es el problema: adultos mayores, personas con movilidad reducida, pacientes en reposo indicado, tratamientos repetidos como el complejo B o el anticonceptivo mensual, o simplemente cuando no puedes salir del trabajo en horario de consultorio.</p>
        </article>
        <article class="card">
          <span class="card__icon" aria-hidden="true">!</span>
          <h3 class="card__title">Conviene un centro de salud</h3>
          <p>Cuando hay fiebre alta sin causa clara, dolor torácico, dificultad respiratoria, sangrado activo, sospecha de infección extendida o cualquier cuadro que requiera exámenes, imágenes o evaluación médica presencial. En esos casos te lo decimos y no agendamos la visita.</p>
        </article>
      </div>
      <div class="callout callout--warn" style="margin-top:2rem">
        <h3>Ante una emergencia, no nos escribas: llama al 131</h3>
        <p>Sanvi no atiende urgencias. Si hay compromiso de conciencia, dificultad para respirar, dolor de pecho o sangrado que no se detiene, llama de inmediato al SAMU al 131 o acude al servicio de urgencia más cercano.</p>
      </div>
    </div>
  </section>

  <section class="section section--tint" id="equipo">
    <div class="container split">
      <div class="stack">
        <h2>Quién te atiende</h2>
        <p>La atención la realizan técnicos en enfermería de nivel superior, titulados y registrados ante la autoridad sanitaria. Llegamos identificados, nos presentamos, te explicamos qué vamos a hacer y esperamos a que estés de acuerdo antes de comenzar.</p>
        <p>Estamos preparando la ficha pública de cada profesional del equipo, con nombre, título y número del Registro Nacional de Prestadores Individuales de Salud. Mientras tanto, puedes pedirnos ese número en el momento de la visita y verificarlo tú mismo, gratis, en el buscador de la Superintendencia de Salud.</p>
        <p>Y un consejo que damos aunque nos deje fuera: si alguien ofrece inyecciones a domicilio en Calama y no puede darte su número de registro, no lo dejes entrar a tu casa.</p>
      </div>
      <div class="callout">
        <h3>Verificar a quien te atiende, paso a paso</h3>
        <ol class="stack" style="padding-left:1.2rem">
          <li>Pídenos el nombre completo y el número de registro del profesional.</li>
          <li>Entra al sitio de la Superintendencia de Salud de Chile.</li>
          <li>Busca el número en el Registro Nacional de Prestadores Individuales de Salud.</li>
        </ol>
        <p><a href="https://www.superdesalud.gob.cl/" target="_blank" rel="noopener">Ir a la Superintendencia de Salud de Chile</a></p>
      </div>
    </div>
  </section>

  <section class="section" id="limites">
    <div class="container">
      <div class="section__head">
        <p class="eyebrow">Límites</p>
        <h2>Lo que no hacemos</h2>
      </div>
      <ul class="checklist checklist--no">
        <li>No vendemos medicamentos. En Chile su venta corresponde exclusivamente a farmacias autorizadas.</li>
        <li>No diagnosticamos, no recetamos y no modificamos la indicación de tu médico tratante.</li>
        <li>No aplicamos nada sin receta médica vigente cuando la normativa la exige.</li>
        <li>No atendemos urgencias ni emergencias vitales.</li>
        <li>No atendemos fuera de Calama.</li>
        <li>No atendemos sin hora agendada previamente.</li>
      </ul>
    </div>
  </section>

  <section class="section cta-band">
    <div class="container cta-band__inner">
      <div>
        <h2>Agenda con nosotros en Calama</h2>
        <p class="lede">Escríbenos por WhatsApp y te confirmamos hora, servicio y precio final antes de salir. Todos los días, de 8:00 a 21:00.</p>
      </div>
      <div class="cta-band__actions">
        <a class="btn btn--primary" href="https://wa.me/56978833741?text=Hola%20Sanvi%2C%20quiero%20agendar%20una%20atenci%C3%B3n%20de%20enfermer%C3%ADa%20a%20domicilio%20en%20Calama.">Agendar por WhatsApp</a>
        <a class="btn btn--ghost" href="servicios.html">Ver servicios y precios</a>
      </div>
    </div>
  </section>

</main>
```

- [ ] **Step 2: Verificar**

```bash
cd "/c/Users/PC/Desktop/claude/Paginas web con SEO"
python tools/check_site.py sitio-sanvi/nosotros.html --content
python tools/check_links.py sitio-sanvi
```

Esperado: un `WARN` de JSON-LD, `OK: 0 errores`, y el verificador de enlaces sin errores nuevos.

- [ ] **Step 3: Verificar visualmente**

```bash
python -m http.server 8080 --directory sitio-sanvi &
python tools/shoot.py http://localhost:8080/nosotros.html --out "$TMPDIR/nos-390.png"  --width 390  --height 4600
python tools/shoot.py http://localhost:8080/nosotros.html --out "$TMPDIR/nos-1280.png" --width 1280 --height 3800
```

Leer las capturas y confirmar que la lista de bioseguridad muestra los siete ítems con su check turquesa, que las dos tarjetas de "domicilio o box clínico" quedan lado a lado a 1280 px y apiladas a 390 px, y que el callout coral del 131 destaca sobre el resto. Detener el servidor.

- [ ] **Step 4: Commit**

```bash
git add sitio-sanvi/nosotros.html
git commit -m "$(cat <<'EOF'
feat: pagina Nosotros con protocolo de bioseguridad y credenciales

Historia, protocolo de higiene de 7 puntos, comparacion domicilio vs box
clinico con derivacion al 131, seccion de credenciales en version liviana
(sin numero de registro, con instrucciones de verificacion) y limites del
servicio.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 6: Página Contacto

**Files:**
- Modify: `sitio-sanvi/contacto.html` (reemplazar el `<main>` provisional)

**Interfaces:**
- Consumes: `.page-hero .contact-grid .contact-card .hours-table .field .field__label .field__control .field__hint .form-actions .btn .coverage__list .callout .faq` ya definidas; el manejador `[data-wa-form]` de `site.js` (Tarea 2).
- Produces: los `id` `#agendar #horario #cobertura #formulario`. El `<form data-wa-form>` debe llevar exactamente los `name` que espera `site.js`: `nombre`, `servicio`, `sector`, `horario`, `mensaje`.

---

- [ ] **Step 1: Escribir el `<main>` definitivo de `contacto.html`**

Reemplazar el bloque `<main id="main"> … </main>` de `sitio-sanvi/contacto.html` por:

```html
<main id="main">

  <section class="page-hero">
    <div class="container">
      <p class="eyebrow">Contacto</p>
      <h1>Contacto y cobertura en Calama</h1>
      <p class="lede">La forma más rápida de agendar es WhatsApp. Atendemos todos los días de 8:00 a 21:00, siempre con hora acordada previamente.</p>
    </div>
  </section>

  <section class="section" id="agendar">
    <div class="container contact-grid">

      <div class="contact-card">
        <h2>Escríbenos por WhatsApp</h2>
        <p>Cuéntanos qué necesitas y envíanos una foto de tu receta. Revisamos que esté vigente, te confirmamos el precio final y acordamos la hora de llegada.</p>
        <p class="form-actions">
          <a class="btn btn--primary btn--block" href="https://wa.me/56978833741?text=Hola%20Sanvi%2C%20quiero%20agendar%20una%20atenci%C3%B3n%20de%20enfermer%C3%ADa%20a%20domicilio%20en%20Calama.">Abrir WhatsApp</a>
          <a class="btn btn--ghost btn--block" href="tel:+56978833741">Llamar al +56 9 7883 3741</a>
        </p>

        <h2 id="horario" style="margin-top:2.5rem">Horario de atención</h2>
        <table class="hours-table">
          <caption class="sr-only">Horario de atención de Sanvi en Calama</caption>
          <tbody>
            <tr><th scope="row">Lunes</th><td>8:00 a 21:00</td></tr>
            <tr><th scope="row">Martes</th><td>8:00 a 21:00</td></tr>
            <tr><th scope="row">Miércoles</th><td>8:00 a 21:00</td></tr>
            <tr><th scope="row">Jueves</th><td>8:00 a 21:00</td></tr>
            <tr><th scope="row">Viernes</th><td>8:00 a 21:00</td></tr>
            <tr><th scope="row">Sábado</th><td>8:00 a 21:00</td></tr>
            <tr><th scope="row">Domingo</th><td>8:00 a 21:00</td></tr>
          </tbody>
        </table>
        <p class="field__hint" style="margin-top:1rem">Atendemos exclusivamente con hora agendada. No realizamos visitas sin cita previa.</p>
      </div>

      <div class="contact-card" id="formulario">
        <h2>O déjanos los datos aquí</h2>
        <p>Completa el formulario y se abrirá WhatsApp con tu mensaje ya escrito. No guardamos ningún dato en este sitio: la conversación ocurre directamente en tu WhatsApp.</p>
        <form data-wa-form class="stack" style="margin-top:1.5rem" novalidate="false">
          <div class="field">
            <label class="field__label" for="f-nombre">Tu nombre</label>
            <input class="field__control" type="text" id="f-nombre" name="nombre" autocomplete="name" required>
          </div>
          <div class="field">
            <label class="field__label" for="f-servicio">Servicio que necesitas</label>
            <select class="field__control" id="f-servicio" name="servicio" required>
              <option value="Inyección intramuscular ($10.000)">Inyección intramuscular · $10.000</option>
              <option value="Inyección intravenosa ($17.000)">Inyección intravenosa · $17.000</option>
              <option value="Curación simple ($15.000)">Curación simple · $15.000</option>
              <option value="Curación compleja ($33.000)">Curación compleja · $33.000</option>
              <option value="No estoy seguro, necesito orientación">No estoy seguro, necesito orientación</option>
            </select>
          </div>
          <div class="field">
            <label class="field__label" for="f-sector">Sector de Calama</label>
            <input class="field__control" type="text" id="f-sector" name="sector" placeholder="Centro, Villa Ayquina, Kamac Mayu…" required>
          </div>
          <div class="field">
            <label class="field__label" for="f-horario">Día y hora que prefieres</label>
            <input class="field__control" type="text" id="f-horario" name="horario" placeholder="Mañana a las 10:00, por ejemplo" required>
            <span class="field__hint">Atendemos entre las 8:00 y las 21:00, todos los días.</span>
          </div>
          <div class="field">
            <label class="field__label" for="f-mensaje">Algo más que debamos saber (opcional)</label>
            <textarea class="field__control" id="f-mensaje" name="mensaje" rows="4"></textarea>
          </div>
          <div class="form-actions">
            <button class="btn btn--primary btn--block" type="submit">Enviar por WhatsApp</button>
          </div>
        </form>
        <noscript>
          <p class="callout" style="margin-top:1.5rem">Este formulario necesita JavaScript para abrir WhatsApp con tu mensaje. Escríbenos directamente al <a href="https://wa.me/56978833741">+56 9 7883 3741</a> o llámanos al <a href="tel:+56978833741">+56 9 7883 3741</a>.</p>
        </noscript>
      </div>

    </div>
  </section>

  <section class="section section--tint" id="cobertura">
    <div class="container split">
      <div class="stack">
        <h2>Dónde atendemos</h2>
        <p>Atendemos dentro del radio urbano de Calama, Región de Antofagasta, Chile. Llegamos a todos los sectores de la ciudad, incluidos el centro, Villa Ayquina y Kamac Mayu.</p>
        <p>No atendemos fuera de Calama: quedan fuera Chuquicamata, Chiu Chiu, San Pedro de Atacama y las demás localidades de la provincia de El Loa.</p>
        <ul class="coverage__list">
          <li>Centro de Calama</li>
          <li>Villa Ayquina</li>
          <li>Kamac Mayu</li>
          <li>Resto del radio urbano</li>
        </ul>
        <p><a href="https://www.google.com/maps/place/Calama,+Antofagasta,+Chile" target="_blank" rel="noopener">Ver Calama en Google Maps</a></p>
      </div>
      <div class="coverage__media">
        <img src="assets/img/cobertura-calama.svg" width="420" height="300" alt="Mapa estilizado del radio urbano de Calama, área de cobertura de Sanvi" decoding="async">
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section__head">
        <h2>Antes de escribirnos</h2>
      </div>
      <div class="faq">
        <details class="faq__item" name="faq-contacto">
          <summary>¿Cuánto se demoran en responder por WhatsApp?</summary>
          <div><p>Respondemos dentro de nuestro horario de atención, entre las 8:00 y las 21:00. Los mensajes que llegan fuera de ese horario se responden a partir de las 8:00 del día siguiente.</p></div>
        </details>
        <details class="faq__item" name="faq-contacto">
          <summary>¿Qué información necesitan para agendar?</summary>
          <div><p>Necesitamos tres cosas: qué servicio requieres, una foto de tu receta médica vigente y tu dirección dentro de Calama. Con eso confirmamos el precio final y la hora de llegada.</p></div>
        </details>
        <details class="faq__item" name="faq-contacto">
          <summary>¿Guardan mis datos en este sitio?</summary>
          <div><p>No. Este sitio no tiene base de datos ni formulario que envíe información a un servidor: el formulario sólo arma un mensaje que se abre en tu propio WhatsApp. Los datos clínicos que compartas se quedan en esa conversación.</p></div>
        </details>
      </div>
    </div>
  </section>

</main>
```

- [ ] **Step 2: Verificar estructura y enlaces**

```bash
cd "/c/Users/PC/Desktop/claude/Paginas web con SEO"
python tools/check_site.py sitio-sanvi --content
python tools/check_links.py sitio-sanvi
```

Esperado: `check_site.py` sobre las cuatro páginas → cuatro `WARN` de JSON-LD y `OK: 0 errores, 4 aviso(s) en 4 pagina(s).` `check_links.py` → sólo los dos `WARN` de sitemap/robots y `OK`.

- [ ] **Step 3: Probar el formulario → WhatsApp manualmente**

```bash
python -m http.server 8080 --directory sitio-sanvi &
```

Abrir `http://localhost:8080/contacto.html` en Chrome, rellenar el formulario con `nombre = Prueba QA`, servicio `Inyección intramuscular`, sector `Centro`, horario `Mañana a las 10:00`, y pulsar "Enviar por WhatsApp". Verificar en la barra de direcciones que la URL destino empieza por `https://wa.me/56978833741?text=Hola%20Sanvi` y contiene `Nombre%3A%20Prueba%20QA` y `Servicio%3A%20Inyecci%C3%B3n%20intramuscular`. Comprobar además que dejando `Tu nombre` vacío el navegador bloquea el envío con el mensaje nativo de campo requerido. Detener el servidor.

- [ ] **Step 4: Commit**

```bash
git add sitio-sanvi/contacto.html
git commit -m "$(cat <<'EOF'
feat: pagina Contacto con formulario que compone mensaje de WhatsApp

WhatsApp y telefono directos, tabla de horario de los 7 dias, formulario sin
backend que abre wa.me con el mensaje prellenado (con fallback noscript),
cobertura de Calama con ilustracion y enlace a Maps, y FAQ de contacto.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 7: Datos estructurados JSON-LD y validación

**Files:**
- Modify: `sitio-sanvi/index.html` (insertar `<script type="application/ld+json">` antes de `</head>`)
- Modify: `sitio-sanvi/servicios.html`, `sitio-sanvi/nosotros.html`, `sitio-sanvi/contacto.html` (ídem)

**Interfaces:**
- Consumes: `check_site.py` (verifica que hay exactamente un bloque, que parsea y que la apertura es literal); las URLs canónicas de la Tarea 1; los precios y anclas de la Tarea 4; `assets/img/og-sanvi.png` y `logo-sanvi.png` de la Tarea 2.
- Produces: los `@id` estables `…/#business`, `…/#logo`, `…/#catalogo`, `…/#website`, `…/#webpage`, `…/#breadcrumb` y `…/servicios.html#<slug>-service`, referenciables si en el futuro se añaden páginas.

**Reglas que rigen esta tarea** (derivadas de `draska-audit/findings/schema.md`):
- Un solo bloque por página, dentro del `<head>`, con `@graph`.
- El nodo `#business` es **idéntico en las cuatro páginas salvo por `hasOfferCatalog`**, que sólo se incluye en `index.html` y `servicios.html`, donde los precios están visibles.
- Nada de `sameAs`, `hasMap`, `email`, `paymentAccepted`, `aggregateRating`, `review` ni `hasCredential` con número: no hay dato real que respalde ninguno.
- La apertura debe ser exactamente `<script type="application/ld+json">`.

---

- [ ] **Step 1: Insertar el `@graph` completo en `index.html`**

Añadir justo antes de `</head>` en `sitio-sanvi/index.html`:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "MedicalBusiness",
      "@id": "https://www.sanvicalama.cl/#business",
      "additionalType": ["https://schema.org/Nursing", "https://www.wikidata.org/wiki/Q1145306"],
      "name": "Sanvi",
      "alternateName": "Sanvi Enfermería a Domicilio Calama",
      "description": "Servicio móvil de enfermería a domicilio en Calama: inyecciones intramusculares e intravenosas y curaciones simples y complejas, realizadas por técnicos en enfermería de nivel superior. Atención todos los días de 8:00 a 21:00, con hora agendada.",
      "url": "https://www.sanvicalama.cl/",
      "logo": {
        "@type": "ImageObject",
        "@id": "https://www.sanvicalama.cl/#logo",
        "url": "https://www.sanvicalama.cl/assets/img/logo-sanvi.png",
        "width": 512,
        "height": 512,
        "caption": "Sanvi, enfermería a domicilio en Calama"
      },
      "image": "https://www.sanvicalama.cl/assets/img/og-sanvi.png",
      "telephone": "+56978833741",
      "priceRange": "$$",
      "currenciesAccepted": "CLP",
      "medicalSpecialty": "Nursing",
      "isAcceptingNewPatients": true,
      "address": {
        "@type": "PostalAddress",
        "addressLocality": "Calama",
        "addressRegion": "Antofagasta",
        "postalCode": "1390000",
        "addressCountry": "CL"
      },
      "geo": {"@type": "GeoCoordinates", "latitude": -22.4667, "longitude": -68.9333},
      "areaServed": {
        "@type": "City",
        "name": "Calama",
        "sameAs": "https://www.wikidata.org/wiki/Q233264"
      },
      "serviceArea": {
        "@type": "GeoCircle",
        "geoMidpoint": {"@type": "GeoCoordinates", "latitude": -22.4667, "longitude": -68.9333},
        "geoRadius": "12000"
      },
      "openingHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
          "opens": "08:00",
          "closes": "21:00"
        }
      ],
      "availableLanguage": [{"@type": "Language", "name": "Spanish", "alternateName": "es"}],
      "knowsAbout": [
        "Inyección intramuscular a domicilio",
        "Inyección intravenosa a domicilio",
        "Curación de heridas simples",
        "Curación de heridas complejas",
        "Complejo vitamínico B",
        "Anticonceptivo inyectable mensual",
        "Enfermería a domicilio en Calama"
      ],
      "contactPoint": [
        {
          "@type": "ContactPoint",
          "contactType": "customer service",
          "telephone": "+56978833741",
          "availableLanguage": "es",
          "areaServed": "CL"
        }
      ],
      "hasOfferCatalog": {"@id": "https://www.sanvicalama.cl/#catalogo"}
    },
    {
      "@type": "OfferCatalog",
      "@id": "https://www.sanvicalama.cl/#catalogo",
      "name": "Servicios de enfermería a domicilio en Calama",
      "itemListElement": [
        {"@type": "Offer", "position": 1, "priceCurrency": "CLP", "price": "10000", "availability": "https://schema.org/InStock", "url": "https://www.sanvicalama.cl/servicios.html#inyeccion-intramuscular", "itemOffered": {"@id": "https://www.sanvicalama.cl/servicios.html#inyeccion-intramuscular-service"}},
        {"@type": "Offer", "position": 2, "priceCurrency": "CLP", "price": "17000", "availability": "https://schema.org/InStock", "url": "https://www.sanvicalama.cl/servicios.html#inyeccion-intravenosa", "itemOffered": {"@id": "https://www.sanvicalama.cl/servicios.html#inyeccion-intravenosa-service"}},
        {"@type": "Offer", "position": 3, "priceCurrency": "CLP", "price": "15000", "availability": "https://schema.org/InStock", "url": "https://www.sanvicalama.cl/servicios.html#curacion-simple", "itemOffered": {"@id": "https://www.sanvicalama.cl/servicios.html#curacion-simple-service"}},
        {"@type": "Offer", "position": 4, "priceCurrency": "CLP", "price": "33000", "availability": "https://schema.org/InStock", "url": "https://www.sanvicalama.cl/servicios.html#curacion-compleja", "itemOffered": {"@id": "https://www.sanvicalama.cl/servicios.html#curacion-compleja-service"}}
      ]
    },
    {
      "@type": "Service",
      "@id": "https://www.sanvicalama.cl/servicios.html#inyeccion-intramuscular-service",
      "name": "Inyección intramuscular a domicilio en Calama",
      "serviceType": "Administración de inyección intramuscular",
      "description": "Aplicación a domicilio de medicamentos por vía intramuscular en Calama, incluidos multivitamínicos del complejo B y el anticonceptivo inyectable mensual. Requiere receta médica vigente. No incluye la venta del medicamento.",
      "url": "https://www.sanvicalama.cl/servicios.html#inyeccion-intramuscular",
      "provider": {"@id": "https://www.sanvicalama.cl/#business"},
      "areaServed": {"@type": "City", "name": "Calama", "sameAs": "https://www.wikidata.org/wiki/Q233264"},
      "offers": {"@type": "Offer", "priceCurrency": "CLP", "price": "10000", "availability": "https://schema.org/InStock", "url": "https://www.sanvicalama.cl/servicios.html#inyeccion-intramuscular", "eligibleRegion": {"@type": "City", "name": "Calama"}}
    },
    {
      "@type": "Service",
      "@id": "https://www.sanvicalama.cl/servicios.html#inyeccion-intravenosa-service",
      "name": "Inyección intravenosa a domicilio en Calama",
      "serviceType": "Administración de medicamento por vía intravenosa",
      "description": "Administración a domicilio de medicamentos por vía endovenosa en Calama, con vigilancia durante y después del procedimiento. Requiere receta médica vigente que especifique la vía intravenosa. No incluye la venta del medicamento.",
      "url": "https://www.sanvicalama.cl/servicios.html#inyeccion-intravenosa",
      "provider": {"@id": "https://www.sanvicalama.cl/#business"},
      "areaServed": {"@type": "City", "name": "Calama", "sameAs": "https://www.wikidata.org/wiki/Q233264"},
      "offers": {"@type": "Offer", "priceCurrency": "CLP", "price": "17000", "availability": "https://schema.org/InStock", "url": "https://www.sanvicalama.cl/servicios.html#inyeccion-intravenosa", "eligibleRegion": {"@type": "City", "name": "Calama"}}
    },
    {
      "@type": "Service",
      "@id": "https://www.sanvicalama.cl/servicios.html#curacion-simple-service",
      "name": "Curación simple de heridas a domicilio en Calama",
      "serviceType": "Curación de herida simple",
      "description": "Curación a domicilio de heridas limpias y de poca extensión en Calama: valoración, aseo con suero fisiológico, cobertura estéril, indicaciones de cuidado y retiro del material contaminado.",
      "url": "https://www.sanvicalama.cl/servicios.html#curacion-simple",
      "provider": {"@id": "https://www.sanvicalama.cl/#business"},
      "areaServed": {"@type": "City", "name": "Calama", "sameAs": "https://www.wikidata.org/wiki/Q233264"},
      "offers": {"@type": "Offer", "priceCurrency": "CLP", "price": "15000", "availability": "https://schema.org/InStock", "url": "https://www.sanvicalama.cl/servicios.html#curacion-simple", "eligibleRegion": {"@type": "City", "name": "Calama"}}
    },
    {
      "@type": "Service",
      "@id": "https://www.sanvicalama.cl/servicios.html#curacion-compleja-service",
      "name": "Curación compleja de heridas a domicilio en Calama",
      "serviceType": "Curación avanzada de herida compleja",
      "description": "Curación a domicilio en Calama de heridas extensas, profundas o de cicatrización lenta, como úlceras por presión y pie diabético: valoración, aseo, manejo del tejido no viable cuando está indicado, cobertura avanzada y registro de la evolución. Requiere indicación médica.",
      "url": "https://www.sanvicalama.cl/servicios.html#curacion-compleja",
      "provider": {"@id": "https://www.sanvicalama.cl/#business"},
      "areaServed": {"@type": "City", "name": "Calama", "sameAs": "https://www.wikidata.org/wiki/Q233264"},
      "offers": {"@type": "Offer", "priceCurrency": "CLP", "price": "33000", "availability": "https://schema.org/InStock", "url": "https://www.sanvicalama.cl/servicios.html#curacion-compleja", "eligibleRegion": {"@type": "City", "name": "Calama"}}
    },
    {
      "@type": "WebSite",
      "@id": "https://www.sanvicalama.cl/#website",
      "url": "https://www.sanvicalama.cl/",
      "name": "Sanvi",
      "inLanguage": "es-CL",
      "publisher": {"@id": "https://www.sanvicalama.cl/#business"}
    },
    {
      "@type": "WebPage",
      "@id": "https://www.sanvicalama.cl/#webpage",
      "url": "https://www.sanvicalama.cl/",
      "name": "Inyecciones a domicilio en Calama | Sanvi Enfermería",
      "description": "Inyecciones y curaciones a domicilio en Calama, aplicadas por técnicos en enfermería de nivel superior. Desde $10.000. Agenda por WhatsApp, de 8:00 a 21:00.",
      "inLanguage": "es-CL",
      "isPartOf": {"@id": "https://www.sanvicalama.cl/#website"},
      "about": {"@id": "https://www.sanvicalama.cl/#business"},
      "primaryImageOfPage": {"@id": "https://www.sanvicalama.cl/#logo"},
      "datePublished": "2026-09-05",
      "dateModified": "2026-09-05",
      "breadcrumb": {"@id": "https://www.sanvicalama.cl/#breadcrumb"}
    },
    {
      "@type": "BreadcrumbList",
      "@id": "https://www.sanvicalama.cl/#breadcrumb",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://www.sanvicalama.cl/"}
      ]
    }
  ]
}
</script>
```

- [ ] **Step 2: Insertar el `@graph` de `servicios.html`**

Añadir antes de `</head>` en `sitio-sanvi/servicios.html` un bloque con **exactamente los mismos nodos** `#business`, `#catalogo` y los cuatro `Service` del paso 1 (copiar literalmente desde `"@type": "MedicalBusiness"` hasta el cierre del cuarto `Service`), seguido de estos tres nodos finales en lugar de los del paso 1:

```json
    {
      "@type": "WebSite",
      "@id": "https://www.sanvicalama.cl/#website",
      "url": "https://www.sanvicalama.cl/",
      "name": "Sanvi",
      "inLanguage": "es-CL",
      "publisher": {"@id": "https://www.sanvicalama.cl/#business"}
    },
    {
      "@type": "WebPage",
      "@id": "https://www.sanvicalama.cl/servicios.html#webpage",
      "url": "https://www.sanvicalama.cl/servicios.html",
      "name": "Servicios y precios de enfermería a domicilio en Calama | Sanvi",
      "description": "Inyección intramuscular $10.000, intravenosa $17.000, curación simple $15.000 y curación compleja $33.000, a domicilio en Calama. Requisitos y agendamiento.",
      "inLanguage": "es-CL",
      "isPartOf": {"@id": "https://www.sanvicalama.cl/#website"},
      "about": {"@id": "https://www.sanvicalama.cl/#business"},
      "datePublished": "2026-09-05",
      "dateModified": "2026-09-05",
      "breadcrumb": {"@id": "https://www.sanvicalama.cl/servicios.html#breadcrumb"}
    },
    {
      "@type": "BreadcrumbList",
      "@id": "https://www.sanvicalama.cl/servicios.html#breadcrumb",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://www.sanvicalama.cl/"},
        {"@type": "ListItem", "position": 2, "name": "Servicios y precios", "item": "https://www.sanvicalama.cl/servicios.html"}
      ]
    }
```

- [ ] **Step 3: Insertar el `@graph` de `nosotros.html`**

Añadir antes de `</head>` en `sitio-sanvi/nosotros.html`:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "MedicalBusiness",
      "@id": "https://www.sanvicalama.cl/#business",
      "additionalType": ["https://schema.org/Nursing", "https://www.wikidata.org/wiki/Q1145306"],
      "name": "Sanvi",
      "alternateName": "Sanvi Enfermería a Domicilio Calama",
      "description": "Servicio móvil de enfermería a domicilio en Calama: inyecciones intramusculares e intravenosas y curaciones simples y complejas, realizadas por técnicos en enfermería de nivel superior. Atención todos los días de 8:00 a 21:00, con hora agendada.",
      "url": "https://www.sanvicalama.cl/",
      "logo": {
        "@type": "ImageObject",
        "@id": "https://www.sanvicalama.cl/#logo",
        "url": "https://www.sanvicalama.cl/assets/img/logo-sanvi.png",
        "width": 512,
        "height": 512,
        "caption": "Sanvi, enfermería a domicilio en Calama"
      },
      "image": "https://www.sanvicalama.cl/assets/img/og-sanvi.png",
      "telephone": "+56978833741",
      "priceRange": "$$",
      "currenciesAccepted": "CLP",
      "medicalSpecialty": "Nursing",
      "isAcceptingNewPatients": true,
      "address": {
        "@type": "PostalAddress",
        "addressLocality": "Calama",
        "addressRegion": "Antofagasta",
        "postalCode": "1390000",
        "addressCountry": "CL"
      },
      "geo": {"@type": "GeoCoordinates", "latitude": -22.4667, "longitude": -68.9333},
      "areaServed": {"@type": "City", "name": "Calama", "sameAs": "https://www.wikidata.org/wiki/Q233264"},
      "serviceArea": {
        "@type": "GeoCircle",
        "geoMidpoint": {"@type": "GeoCoordinates", "latitude": -22.4667, "longitude": -68.9333},
        "geoRadius": "12000"
      },
      "openingHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
          "opens": "08:00",
          "closes": "21:00"
        }
      ],
      "availableLanguage": [{"@type": "Language", "name": "Spanish", "alternateName": "es"}],
      "knowsAbout": [
        "Inyección intramuscular a domicilio",
        "Inyección intravenosa a domicilio",
        "Curación de heridas simples",
        "Curación de heridas complejas",
        "Complejo vitamínico B",
        "Anticonceptivo inyectable mensual",
        "Enfermería a domicilio en Calama"
      ],
      "contactPoint": [
        {"@type": "ContactPoint", "contactType": "customer service", "telephone": "+56978833741", "availableLanguage": "es", "areaServed": "CL"}
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://www.sanvicalama.cl/#website",
      "url": "https://www.sanvicalama.cl/",
      "name": "Sanvi",
      "inLanguage": "es-CL",
      "publisher": {"@id": "https://www.sanvicalama.cl/#business"}
    },
    {
      "@type": "AboutPage",
      "@id": "https://www.sanvicalama.cl/nosotros.html#webpage",
      "url": "https://www.sanvicalama.cl/nosotros.html",
      "name": "Quiénes somos | Sanvi, enfermería a domicilio en Calama",
      "description": "Conoce a Sanvi: técnicos en enfermería de nivel superior, protocolo de bioseguridad e insumos estériles de un solo uso para atenderte en tu casa, en Calama.",
      "inLanguage": "es-CL",
      "isPartOf": {"@id": "https://www.sanvicalama.cl/#website"},
      "about": {"@id": "https://www.sanvicalama.cl/#business"},
      "datePublished": "2026-09-05",
      "dateModified": "2026-09-05",
      "breadcrumb": {"@id": "https://www.sanvicalama.cl/nosotros.html#breadcrumb"}
    },
    {
      "@type": "BreadcrumbList",
      "@id": "https://www.sanvicalama.cl/nosotros.html#breadcrumb",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://www.sanvicalama.cl/"},
        {"@type": "ListItem", "position": 2, "name": "Nosotros", "item": "https://www.sanvicalama.cl/nosotros.html"}
      ]
    }
  ]
}
</script>
```

- [ ] **Step 4: Insertar el `@graph` de `contacto.html`**

Añadir antes de `</head>` en `sitio-sanvi/contacto.html` un bloque idéntico al del paso 3 salvo los tres últimos nodos, que se reemplazan por:

```json
    {
      "@type": "ContactPage",
      "@id": "https://www.sanvicalama.cl/contacto.html#webpage",
      "url": "https://www.sanvicalama.cl/contacto.html",
      "name": "Contacto y cobertura en Calama | Sanvi Enfermería",
      "description": "Agenda tu atención de enfermería a domicilio en Calama por WhatsApp al +56 9 7883 3741. Atendemos de 8:00 a 21:00 con hora previa. Cobertura: todo Calama.",
      "inLanguage": "es-CL",
      "isPartOf": {"@id": "https://www.sanvicalama.cl/#website"},
      "about": {"@id": "https://www.sanvicalama.cl/#business"},
      "datePublished": "2026-09-05",
      "dateModified": "2026-09-05",
      "breadcrumb": {"@id": "https://www.sanvicalama.cl/contacto.html#breadcrumb"}
    },
    {
      "@type": "BreadcrumbList",
      "@id": "https://www.sanvicalama.cl/contacto.html#breadcrumb",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://www.sanvicalama.cl/"},
        {"@type": "ListItem", "position": 2, "name": "Contacto", "item": "https://www.sanvicalama.cl/contacto.html"}
      ]
    }
```

(El nodo `WebSite` se mantiene tal cual entre `#business` y `ContactPage`.)

- [ ] **Step 5: Validar el JSON-LD con el validador de `claude-seo`**

El agente de schema de la auditoría usó los scripts Python de `claude-seo`. El validador que funciona sobre archivos HTML locales, sin red y sin dependencias, es el hook `validate-schema.py`. Ejecutar sobre las cuatro páginas:

```bash
cd "/c/Users/PC/Desktop/claude/Paginas web con SEO"
HOOK="/c/Users/PC/.claude/plugins/cache/agricidaniel-claude-seo/claude-seo/2.2.5/hooks/validate-schema.py"
for f in index servicios nosotros contacto; do
  echo "== $f.html =="
  python "$HOOK" "sitio-sanvi/$f.html" < /dev/null
  echo "exit=$?"
done
```

Esperado: cuatro bloques con `exit=0` y **sin ninguna línea impresa**. Cualquier salida significa error: `exit=2` indica placeholder o tipo deprecado (bloqueante); `exit=1` indica avisos (`Missing @context`, `Missing @type`, `@graph member N must be an object`). Los tres errores del competidor que este schema corrige (`addressCountry` ISO, `postalCode` de 7 dígitos, `sameAs` con URL) deben quedar verificados a ojo: `"addressCountry": "CL"`, `"postalCode": "1390000"` y ausencia total de `sameAs` con Place ID crudo.

- [ ] **Step 6: Validar coherencia entre JSON-LD y texto visible**

```bash
python tools/check_site.py sitio-sanvi --content
```

Esperado: `OK: 0 errores, 0 aviso(s) en 4 pagina(s).` — los cuatro `WARN` de "sin bloque JSON-LD" desaparecen.

Además, comprobar manualmente la paridad exigida por `schema.md` §6 nota 6 (todo lo marcado debe ser visible):

```bash
grep -c '"price": "10000"' sitio-sanvi/index.html && grep -c '\$10\.000' sitio-sanvi/index.html
grep -c '"opens": "08:00"' sitio-sanvi/contacto.html && grep -c '8:00 a 21:00' sitio-sanvi/contacto.html
```

Los cuatro conteos deben ser ≥ 1.

- [ ] **Step 7: Commit**

```bash
git add sitio-sanvi/index.html sitio-sanvi/servicios.html sitio-sanvi/nosotros.html sitio-sanvi/contacto.html
git commit -m "$(cat <<'EOF'
feat: JSON-LD MedicalBusiness con OfferCatalog y 4 Service

Un @graph por pagina con MedicalBusiness + Nursing, NAP corregido (postalCode
1390000, addressCountry CL), areaServed City + GeoCircle, openingHours 8-21 los
7 dias, hasOfferCatalog con los 4 Service y sus Offer, WebSite, WebPage y
BreadcrumbList. Sin aggregateRating, review, sameAs ni FAQPage: no hay dato
real que los respalde. Valida con 0 errores.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 8: SEO técnico, configuración de despliegue y README

**Files:**
- Create: `sitio-sanvi/sitemap.xml`
- Create: `sitio-sanvi/robots.txt`
- Create: `sitio-sanvi/netlify.toml`
- Create: `sitio-sanvi/_headers`
- Create: `sitio-sanvi/README.md`

**Interfaces:**
- Consumes: `check_links.py`, que valida que `sitemap.xml` contenga exactamente las cuatro URLs canónicas y que `robots.txt` declare la línea `Sitemap:`.
- Produces: la configuración de cabeceras de seguridad y el procedimiento documentado de cambio de dominio, consumidos por la Tarea 9 y por el despliegue.

---

- [ ] **Step 1: Crear `sitemap.xml`**

Crear `Paginas web con SEO/sitio-sanvi/sitemap.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://www.sanvicalama.cl/</loc>
    <lastmod>2026-09-05</lastmod>
  </url>
  <url>
    <loc>https://www.sanvicalama.cl/servicios.html</loc>
    <lastmod>2026-09-05</lastmod>
  </url>
  <url>
    <loc>https://www.sanvicalama.cl/nosotros.html</loc>
    <lastmod>2026-09-05</lastmod>
  </url>
  <url>
    <loc>https://www.sanvicalama.cl/contacto.html</loc>
    <lastmod>2026-09-05</lastmod>
  </url>
</urlset>
```

Cuatro URLs y ninguna más: la lección directa del `/test` indexable de Draska (`technical.md`).

- [ ] **Step 2: Crear `robots.txt`**

Crear `Paginas web con SEO/sitio-sanvi/robots.txt`:

```
User-agent: *
Allow: /

Sitemap: https://www.sanvicalama.cl/sitemap.xml
```

- [ ] **Step 3: Crear `netlify.toml` con cabeceras de seguridad**

Crear `Paginas web con SEO/sitio-sanvi/netlify.toml`:

```toml
# Configuracion de despliegue de Sanvi en Netlify.
# El sitio es estatico: no hay comando de build, solo publicacion de esta carpeta.

[build]
  publish = "."

# Las URLs del sitio son .html reales. Desactivar pretty_urls evita que Netlify
# redirija /servicios.html a /servicios y rompa los canonicals y el sitemap.
[build.processing.html]
  pretty_urls = false

[[headers]]
  for = "/*"
  [headers.values]
    X-Content-Type-Options = "nosniff"
    X-Frame-Options = "DENY"
    Referrer-Policy = "strict-origin-when-cross-origin"
    Permissions-Policy = "geolocation=(), camera=(), microphone=(), payment=(), interest-cohort=()"
    Strict-Transport-Security = "max-age=31536000; includeSubDomains; preload"
    Content-Security-Policy = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'; form-action 'self' https://wa.me; frame-ancestors 'none'; base-uri 'self'"

[[headers]]
  for = "/assets/css/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/assets/js/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/assets/img/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
```

Nota sobre `'unsafe-inline'` en `script-src`: es necesario por el único script inline del `<head>` (`document.documentElement.classList.add('js')`). Si más adelante se quiere una CSP estricta, mover esa línea a un archivo `.js` y eliminar `'unsafe-inline'`.

- [ ] **Step 4: Crear `_headers` para Cloudflare Pages**

Crear `Paginas web con SEO/sitio-sanvi/_headers`:

```
/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), camera=(), microphone=(), payment=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
  Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'; form-action 'self' https://wa.me; frame-ancestors 'none'; base-uri 'self'

/assets/*
  Cache-Control: public, max-age=31536000, immutable
```

- [ ] **Step 5: Crear el `README.md` del sitio**

Crear `Paginas web con SEO/sitio-sanvi/README.md`:

```markdown
# Sanvi — sitio web

Sitio estático de 4 páginas para Sanvi, enfermería e inyecciones a domicilio en Calama, Chile.
HTML/CSS/JS puro. Sin framework, sin build step, sin dependencias de runtime.

## Estructura

- `index.html` · `servicios.html` · `nosotros.html` · `contacto.html`
- `assets/css/base.css` — tokens de diseño, reset, tipografía, layout
- `assets/css/components.css` — header, nav, botones, tarjetas, tabla, FAQ, footer, FAB, formulario
- `assets/css/pages.css` — secciones concretas de cada página
- `assets/js/site.js` — nav móvil, sombra del header, formulario → WhatsApp (todo mejora progresiva)
- `assets/img/` — SVG propios y los tres PNG generados
- `sitemap.xml`, `robots.txt`, `netlify.toml`, `_headers`

Los verificadores viven en `../tools/` y **no** se despliegan.

## Ver el sitio en local

    python -m http.server 8080 --directory .

Abrir http://localhost:8080/index.html

## Verificar antes de publicar

    cd ..
    python tools/check_site.py sitio-sanvi --content
    python tools/check_links.py sitio-sanvi
    python tools/check_perf.py sitio-sanvi
    python "$HOME/.claude/plugins/cache/agricidaniel-claude-seo/claude-seo/2.2.5/hooks/validate-schema.py" sitio-sanvi/index.html < /dev/null

Los cuatro deben terminar sin errores.

## Regenerar los rasters de marca

    cd ..
    python tools/shoot.py tools/og/og.html         --out sitio-sanvi/assets/img/og-sanvi.png         --width 1200 --height 630
    python tools/shoot.py tools/og/logo.html       --out sitio-sanvi/assets/img/logo-sanvi.png       --width 512  --height 512
    python tools/shoot.py tools/og/touch-icon.html --out sitio-sanvi/assets/img/apple-touch-icon.png --width 180  --height 180

## Cambiar el dominio

El sitio usa `https://www.sanvicalama.cl` como dominio de trabajo en canonicals, og:url,
sitemap, robots y JSON-LD. Al comprar el dominio definitivo, ejecutar una sola vez desde
la raíz del proyecto:

    grep -rl "www.sanvicalama.cl" sitio-sanvi/ | xargs sed -i 's|www\.sanvicalama\.cl|DOMINIO-NUEVO|g'
    python tools/check_site.py sitio-sanvi --content

y actualizar `SITE` en `tools/check_site.py` y en `tools/check_links.py`.

## Desplegar

Netlify o Cloudflare Pages, publicando esta carpeta tal cual. Sin comando de build.
En Netlify, `netlify.toml` ya desactiva `pretty_urls` (indispensable: el sitio usa
URLs `.html` reales) y aplica las cabeceras de seguridad. En Cloudflare Pages las
cabeceras vienen de `_headers`.

## Pendientes post-lanzamiento (por orden de impacto)

1. **Google Business Profile.** Crear y verificar la ficha de Sanvi en Calama. Después:
   añadir al nodo `#business` del JSON-LD de las 4 páginas
   `"sameAs": ["https://www.google.com/maps/place/?q=place_id:PLACE_ID_REAL"]` y
   `"hasMap": "https://www.google.com/maps/place/?q=place_id:PLACE_ID_REAL"`.
   Hasta tener el Place ID real, no añadir nada: publicar un placeholder viola las
   políticas de datos estructurados.
2. **Número de registro sanitario.** Cuando esté disponible, publicarlo visible en
   `nosotros.html#equipo` y `index.html#equipo`, y añadir al `@graph` un nodo `Person`
   con `hasCredential` (`EducationalOccupationalCredential`, `credentialCategory: "license"`,
   `recognizedBy` Superintendencia de Salud). Es la mayor palanca de E-E-A-T del rubro.
3. **Fotos reales del equipo.** Reemplazar `assets/img/hero-cuidado.svg` y la ilustración
   de cobertura por fotografías propias en WebP con `srcset`. El markup ya lleva `width`,
   `height` y `alt` definitivos: sólo cambia el `src`.
4. **Reseñas.** Motor sostenido de 2 a 4 reseñas mensuales en GBP, pedidas por WhatsApp
   30–60 min después de cada atención. Cuando existan reseñas reales y visibles, sustituir
   la sección `#opiniones` de la home por testimonios reales con nombre, sector y fecha.
5. **Sectores de Calama.** Ampliar la lista de `#cobertura` con los sectores reales que
   atiende el negocio, en index.html y contacto.html.
```

- [ ] **Step 6: Verificar**

```bash
cd "/c/Users/PC/Desktop/claude/Paginas web con SEO"
python tools/check_links.py sitio-sanvi
python -c "import xml.dom.minidom,sys; xml.dom.minidom.parse('sitio-sanvi/sitemap.xml'); print('sitemap.xml: XML valido')"
```

Esperado: `check_links.py` sin ningún `WARN` ni error, terminando en `OK: todos los enlaces internos, anclas y assets resuelven.`; y `sitemap.xml: XML valido`.

Comprobar además que ninguna URL del sitemap devuelve 404 en local:

```bash
python -m http.server 8080 --directory sitio-sanvi &
for u in / /servicios.html /nosotros.html /contacto.html /sitemap.xml /robots.txt; do
  code=$(python -c "import urllib.request,sys;
try:
    print(urllib.request.urlopen('http://localhost:8080$u').status)
except Exception as e:
    print('FAIL', e)")
  echo "$u -> $code"
done
```

Esperado: las seis líneas terminan en `200`. Detener el servidor.

- [ ] **Step 7: Commit**

```bash
git add sitio-sanvi/sitemap.xml sitio-sanvi/robots.txt sitio-sanvi/netlify.toml sitio-sanvi/_headers sitio-sanvi/README.md
git commit -m "$(cat <<'EOF'
chore: SEO tecnico, cabeceras de seguridad y README de despliegue

Sitemap limpio con exactamente las 4 URLs canonicas, robots.txt con la linea
Sitemap, netlify.toml con pretty_urls desactivado y CSP/HSTS/nosniff, _headers
equivalente para Cloudflare Pages, y README con verificacion, cambio de dominio
y pendientes post-lanzamiento priorizados.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 9: QA final — accesibilidad, rendimiento y cierre

**Files:**
- Create: `Paginas web con SEO/tools/check_perf.py`
- Modify: cualquier archivo de `sitio-sanvi/` que la revisión obligue a corregir

**Interfaces:**
- Consumes: todo lo anterior.
- Produces: `tools/check_perf.py` — CLI: `python tools/check_perf.py <dir-sitio>`. Sale `0`/`1`. Reporta peso total por página, recursos bloqueantes de render, `<img>` sin dimensiones, scripts sin `defer` y ausencia de `preconnect` a las fuentes.

**Limitación conocida sobre Lighthouse, declarada por adelantado:** el runtime de `claude-seo` (`unlighthouse_run.py`, `pagespeed_check.py`, `capture_screenshot.py`) valida las URLs con `url_safety.validate_url_strict`, que **rechaza `localhost` y las IP privadas** por protección anti-SSRF, y además `playwright` no está instalado en esta máquina. Por lo tanto **no es posible medir Core Web Vitals reales con `claude-seo` antes de tener una URL pública**. Lo que sí se hace aquí: (a) intentar Lighthouse vía `npx` contra el servidor local, que sí acepta `localhost`; (b) si no hay red para `npx`, aplicar las heurísticas offline de `check_perf.py`; (c) dejar anotado que la medición real con `claude-seo` se ejecuta el día del despliegue, contra el dominio público.

---

- [ ] **Step 1: Escribir `tools/check_perf.py`**

Crear `Paginas web con SEO/tools/check_perf.py`:

```python
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
```

- [ ] **Step 2: Ejecutar las heurísticas de rendimiento**

```bash
cd "/c/Users/PC/Desktop/claude/Paginas web con SEO"
python tools/check_perf.py sitio-sanvi
```

Esperado: cuatro líneas `INFO` con los pesos y `OK: heuristicas de rendimiento superadas.` Si `og-sanvi.png` empuja el peso por encima de 400 KB, no está referenciado como `<img>` (sólo como `og:image`), así que no debe contar; si aparece el error, revisar que no se haya insertado como imagen en el body.

- [ ] **Step 3: Intentar Lighthouse contra el servidor local**

```bash
python -m http.server 8080 --directory sitio-sanvi &
npx --yes lighthouse@12 http://localhost:8080/index.html \
  --quiet --chrome-flags="--headless=new --no-sandbox" \
  --only-categories=performance,accessibility,best-practices,seo \
  --output=json --output-path="$TMPDIR/lh-home.json"
python -c "
import json,os
d=json.load(open(os.environ['TMPDIR']+'/lh-home.json',encoding='utf-8'))
for k,v in d['categories'].items():
    print(k, round(v['score']*100))
"
```

Esperado si hay red: cuatro puntuaciones, todas ≥ 90 (rendimiento ≥ 95 es alcanzable en un sitio así). Si `npx` falla por falta de red o de caché, **no reintentar**: dejar constancia de la limitación y pasar al paso 4, que ya cubre las causas raíz de forma determinista. Anotar en el mensaje de commit qué camino se tomó. Detener el servidor.

- [ ] **Step 4: Revisión de accesibilidad y UX con la skill `impeccable`**

Invocar la skill con este encargo textual:

> Revisa el sitio estático en `C:\Users\PC\Desktop\claude\Paginas web con SEO\sitio-sanvi\` (4 páginas HTML, 3 hojas CSS, 1 JS). Auditoría de accesibilidad WCAG 2.1 AA y de UX. Foco en: jerarquía visual del hero, orden de tabulación y visibilidad del foco, `aria-expanded`/`aria-controls` del menú móvil, semántica del acordeón `<details>`, etiquetado y mensajes de error del formulario de contacto, contraste real de los botones coral (`#0B2A3A` sobre `#FF6B57`) y de los badges, comportamiento del FAB de WhatsApp sobre contenido en móvil, y legibilidad de la tabla de precios en su versión apilada. No cambies la paleta, la tipografía ni la arquitectura de 4 páginas: son decisiones cerradas. Devuelve hallazgos accionables ordenados por severidad.

Aplicar las correcciones de severidad alta y media. Tras cada corrección, volver a ejecutar:

```bash
python tools/check_site.py sitio-sanvi --content
python tools/check_links.py sitio-sanvi
python tools/check_perf.py sitio-sanvi
```

- [ ] **Step 5: Recorrido manual de teclado y lector de pantalla**

Con el servidor local levantado, en Chrome, recorrer `index.html` sólo con teclado y confirmar punto por punto:

1. El primer `Tab` revela el enlace "Saltar al contenido" con contorno turquesa visible.
2. `Enter` sobre él lleva el foco al `<main id="main">`.
3. Con ventana a 390 px: `Tab` llega al botón hamburguesa, `Enter` lo abre, `aria-expanded` pasa a `true` en el inspector, `Tab` recorre los cuatro enlaces y el CTA, `Esc` lo cierra y devuelve el foco al botón.
4. Todos los `<summary>` del FAQ reciben foco visible y se abren con `Enter` y con `Espacio`.
5. Ningún elemento queda con el contorno de foco recortado por `overflow: hidden`.
6. En `contacto.html`, `Tab` recorre los cinco campos en orden visual y cada `<label>` activa su control al hacer clic.

Cualquier fallo se corrige antes de continuar.

- [ ] **Step 6: Batería final de capturas responsive**

```bash
python -m http.server 8080 --directory sitio-sanvi &
for p in index servicios nosotros contacto; do
  python tools/shoot.py "http://localhost:8080/$p.html" --out "$TMPDIR/qa-$p-390.png"  --width 390  --height 6000
  python tools/shoot.py "http://localhost:8080/$p.html" --out "$TMPDIR/qa-$p-1280.png" --width 1280 --height 5000
done
```

Leer las ocho capturas y confirmar: sin scroll horizontal en 390 px, sin texto solapado, sin líneas de más de ~75 caracteres en 1280 px, el FAB no tapa ningún CTA ni el último bloque de texto, y el footer oscuro muestra el NAP completo en las cuatro páginas. Detener el servidor.

- [ ] **Step 7: Verificación final consolidada**

```bash
cd "/c/Users/PC/Desktop/claude/Paginas web con SEO"
HOOK="/c/Users/PC/.claude/plugins/cache/agricidaniel-claude-seo/claude-seo/2.2.5/hooks/validate-schema.py"
python tools/check_site.py sitio-sanvi --content && \
python tools/check_links.py sitio-sanvi && \
python tools/check_perf.py sitio-sanvi && \
for f in index servicios nosotros contacto; do python "$HOOK" "sitio-sanvi/$f.html" < /dev/null || exit 1; done && \
echo "TODO VERDE"
```

Esperado: la última línea impresa es `TODO VERDE`. No declarar el trabajo terminado sin haber visto literalmente esa línea.

- [ ] **Step 8: Commit final**

```bash
git add tools/check_perf.py sitio-sanvi
git commit -m "$(cat <<'EOF'
chore: QA final de accesibilidad, rendimiento y correcciones

Anade check_perf.py con heuristicas offline de Core Web Vitals (peso de pagina,
recursos bloqueantes, dimensiones de imagen para CLS, defer, preconnect de
fuentes). Aplica las correcciones de accesibilidad y UX detectadas en la
revision con la skill impeccable y en el recorrido manual de teclado.

Limitacion registrada: claude-seo no puede medir Core Web Vitals sin URL
publica (url_safety rechaza localhost y playwright no esta instalado). La
medicion real se ejecuta el dia del despliegue contra el dominio publico.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

## Auto-revisión del plan

**1. Cobertura del spec.** Contexto de negocio → Tarea 3 (home) y 5 (nosotros). Servicios y precios → Tareas 3, 4 y 7. Aprendizajes de la auditoría: postal code y `addressCountry` corregidos → Tarea 7 paso 5; `sameAs` con Place ID → omitido deliberadamente y documentado en el README (Tarea 8); CSS inline masivo → tres hojas externas verificadas por `check_perf.py`; imágenes rotas → `check_links.py` verifica existencia y `check_perf.py` exige dimensiones; cero cabeceras de seguridad → `netlify.toml` y `_headers` (Tarea 8); `/test` indexable → sitemap con exactamente cuatro URLs verificadas por `check_links.py`; 1.200–1.500 palabras → umbrales de `MIN_WORDS` en `check_site.py`; precios visibles → Tareas 3 y 4; SXO "above the fold con precio + credenciales + WhatsApp" → hero estructura B en Tarea 3. Sistema visual (paleta, tipografía, hero B, imágenes reemplazables) → Tareas 1, 2 y 3. Arquitectura de 4 páginas con metadatos propios → Tarea 1 (heads) y Tareas 3–6 (contenido). Sección de credenciales liviana → Tareas 3 y 5. Datos estructurados → Tarea 7. Stack técnico → Constraints globales, Tareas 1, 2 y 8. QA antes de publicar (impeccable, Lighthouse, schema 0 errores) → Tarea 9. Modelo de ejecución Sonnet para el código → decisión del agente que despacha, fuera del alcance del plan. Fuera de alcance del spec (GBP, registro sanitario, dominio, loop de auditoría) → listados como pendientes en el README, sin tareas.

**2. Escaneo de placeholders.** Sin "TBD", "TODO", "implementar después" ni "similar a la Tarea N". Todos los pasos de código llevan el código íntegro. Las dos únicas referencias cruzadas —el `@graph` de `servicios.html` que copia los nodos del paso 1, y el de `contacto.html` que copia los del paso 3— nombran el bloque exacto a copiar y enumeran textualmente los nodos que cambian, con su JSON completo. El header y el footer se escriben una sola vez (Tarea 2, paso 9) porque ahí se instalan en las cuatro páginas; las Tareas 3–6 sólo reemplazan `<main>`, así que no hay ningún bloque omitido.

**3. Consistencia de tipos y nombres.** `check_site.py` usa `--content` en las Tareas 3–9, nunca `--strict`. Las claves de `CANONICAL` y `MIN_WORDS` coinciden con los cuatro nombres de archivo. Los `name` del formulario (`nombre`, `servicio`, `sector`, `horario`, `mensaje`) son los mismos en el HTML de la Tarea 6 y en `site.js` de la Tarea 2. Los `id` de sección de la Tarea 4 (`#inyeccion-intramuscular`, `#inyeccion-intravenosa`, `#curacion-simple`, `#curacion-compleja`) coinciden con los `href` emitidos en las Tareas 2 y 3 y con los `url` de los `Service` de la Tarea 7; los `@id` de esos `Service` llevan el sufijo `-service` para no colisionar con los anclas del DOM, y el `OfferCatalog` los referencia con ese mismo sufijo. `shoot.py` expone `--out/--width/--height` y así se invoca en las Tareas 2, 3, 4, 5 y 9. Las clases producidas por `components.css` y `pages.css` son exactamente las consumidas por las Tareas 3–6.