# Auditoría SEO Técnico — https://draska.ueniweb.com/

**Fecha:** 2026-09-05
**Objetivo:** benchmark competitivo. NO se corrige este sitio (es de un tercero). Se extraen prácticas replicables y errores a evitar para un sitio nuevo del mismo rubro (enfermería / inyecciones a domicilio, Calama, Chile) con mejor diseño.
**Plataforma:** Ueni (builder SaaS) sobre subdominio `*.ueniweb.com`, servido tras Cloudflare.
**Score técnico:** **66 / 100**

---

## 0. Nota de metodología

| Herramienta | Resultado |
|---|---|
| `claude-seo run sitemap_discovery.py` | OK — 3 sitemaps declarados, 3 validados `200 / urlset` |
| `claude-seo run render_page.py --mode auto` | OK — `is_spa=false`, HTML crudo suficiente (2.03 MB) |
| `claude-seo run parse_html.py` | OK |
| `claude-seo run preload_check.py` | OK — score 50 |
| `claude-seo run agent_ux_check.py` | OK — score 85 |
| `claude-seo run pagespeed_check.py` | **NO DISPONIBLE** — cuota PSI agotada (7 reintentos con backoff de 60 s). CrUX requiere `GOOGLE_API_KEY` no configurada. |

**Consecuencia:** no hay datos de campo (CrUX) ni de laboratorio (Lighthouse). Todos los hallazgos de Core Web Vitals de este informe son **riesgos inferidos por inspección de código fuente y medición de red directa (curl)**, no métricas medidas. Se marcan explícitamente como `[INFERIDO]`. Antes de tomar decisiones de arquitectura basadas en la sección 6, conviene re-ejecutar `pagespeed_check.py` cuando la cuota se reponga.

---

## 1. Tabla resumen por categoría

| # | Categoría | Estado | Nota |
|---|---|---|---|
| 1 | Crawlability | **PASS** | robots.txt abierto, 3 sitemaps válidos |
| 2 | Indexability | **PARCIAL** | canonicals correctos, pero página `/test` indexable y títulos duplicados |
| 3 | Security (headers) | **FAIL** | cero cabeceras de seguridad |
| 4 | URL Structure | **PARCIAL** | limpias y sin redirecciones, pero slugs en inglés + IDs numéricos + subdominio ajeno |
| 5 | Mobile | **PARCIAL** | responsive real, pero `user-scalable=no` |
| 6 | Core Web Vitals | **RIESGO ALTO** `[INFERIDO]` | 2.03 MB de HTML, 1.3 MB de CSS inline, srcset roto |
| 7 | Structured Data | **PARCIAL** | LocalBusiness + Service + OfferCatalog presentes, con errores de validez |
| 8 | JS Rendering | **PASS** | SSR real, paridad con Googlebot |
| 9 | IndexNow | **FAIL** | no implementado |

---

## 2. Hallazgos por categoría

### 2.1 Crawlability — PASS

`robots.txt` completo:

```
User-agent: *
Sitemap: https://ueniweb.com/sitemap/draska.xml
Sitemap: https://draska.ueniweb.com/sitemap.xml
Sitemap: https://ueniweb.com/sitemap-last-1000.xml
```

No hay ninguna línea `Disallow`. Todo abierto. `sitemap_discovery.py` validó los tres (`status_code: 200`, `kind: urlset`, `valid: true`); dos son `cross_host: true`.

**Por qué declara 3 sitemaps — respuesta concreta (investigado, no supuesto):**

1. `https://draska.ueniweb.com/sitemap.xml` — 17 URLs, el sitemap propio del negocio.
2. `https://ueniweb.com/sitemap/draska.xml` — **byte-por-byte idéntico al anterior**. Es el mismo sitemap servido desde el dominio raíz de la plataforma. No aporta URLs nuevas; su función es que las URLs de draska cuelguen también del host `ueniweb.com`, que tiene mucha más autoridad y frecuencia de rastreo que un subdominio recién creado. Es *sitemap hosting cruzado* para heredar crawl rate.
3. `https://ueniweb.com/sitemap-last-1000.xml` — **no contiene ninguna URL de draska**. Contiene 1.000 URLs de **195 hosts distintos** (otros clientes de Ueni: `609jerseys.com`, `action-roofing.ueniweb.com`, `acu-na.com`…), con `lastmod` regenerado en tiempo real (rango observado: `14:25` → `19:05` del mismo día). Es un *firehose* de frescura a nivel plataforma: un cebo de rastreo compartido que atrae al bot al dominio raíz. Draska solo entra en esa lista durante la ventana inmediatamente posterior a una edición de su web.

**Conclusión clave:** los 3 sitemaps **no son una estrategia del negocio**, son fontanería de la plataforma Ueni para agrupar crawl budget entre miles de sitios. Un sitio propio no puede ni debe replicar el nº 3.

### 2.2 Indexability — PARCIAL

Lo que está bien:
- Canonical self-referencing, absoluto y HTTPS en todas las páginas comprobadas (`/`, `/test`, `/services`, `/services/enfermeria-a-domicilio/inyeccion-neurobionta-26634346`).
- Sin `meta robots` (`parse_html` → `meta_robots: null`) → indexable por defecto. Correcto para un sitio que quiere posicionar.
- `<html lang="es">` correcto, `og:locale = es_CL` correcto para Chile.
- 404 real (código `404`) en URLs inexistentes — no hay soft-404.
- Sin hreflang (`hreflang: []`). Correcto: sitio monolingüe. No aplica delegación a `seo-hreflang`.

Lo que está mal:
- **`/test` está publicada, es indexable, tiene canonical propio, está en el sitemap y además aparece como ítem del menú de navegación** (el texto SSR incluye literalmente `... Ubicación CONTACTO test Compartir`). Es una página basura de pruebas expuesta al índice y enlazada desde todo el sitio.
- **Título duplicado:** `/services` usa exactamente el mismo `<title>` que la home (`Draska - Enfermería a domicilio | Calama`). Canibalización directa.
- `/test` hereda la meta description de la home → descripción duplicada.
- Contenido fino: 567 palabras en la home (`word_count: 567`) y solo 3.822 caracteres de texto visible SSR.

### 2.3 Security — FAIL (0/6)

Volcado completo de cabeceras de respuesta (`curl -sSI --compressed`):

```
HTTP/2 200
content-type: text/html; charset=utf-8
server: cloudflare
vary: Accept-Encoding
last-modified: Sat, 05 Sep 2026 18:42:08 GMT
x-render-cache: LASTNOTMODIFIED
x-ueni-region: us1p
cache-control: public, no-cache
cf-cache-status: DYNAMIC
content-encoding: br
```

Ausentes las seis: `Strict-Transport-Security`, `Content-Security-Policy`, `X-Content-Type-Options`, `X-Frame-Options` / `frame-ancestors`, `Referrer-Policy`, `Permissions-Policy`.

Solo hay un paliativo a nivel de documento: `<meta name="referrer" content="origin">`, que es más débil que una cabecera `Referrer-Policy` y no protege recursos no-HTML.

HTTPS en sí está bien:
- Certificado `CN = ueniweb.com`, emisor Google Trust Services WE1, válido `2026-07-13` → `2026-10-11`. Verificación TLS limpia (`ssl_verify_result=0`).
- HTTP → HTTPS con `301` correcto a `https://draska.ueniweb.com/`.
- Handshake TLS ~135-160 ms.
- HTTP/2. **No se negoció HTTP/3** pese a estar tras Cloudflare, y no hay cabecera `alt-svc`.

Ojo: sin HSTS, ese `301` es vulnerable a stripping en la primera visita.

**Fuga de dato personal:** el HTML expone `business:contact_data:email = hectoremprendimiento9@gmail.com` en un `<meta>` en claro, mientras que los `mailto:` del cuerpo sí están ofuscados vía `/cdn-cgi/l/email-protection` de Cloudflare. La protección anti-scraping es inconsistente y el meta tag anula el resto.

### 2.4 URL Structure — PARCIAL

Bien:
- URLs limpias, sin parámetros, sin extensiones, minúsculas, con guiones.
- **Cero redirecciones en la home** (`num_redirects=0`). Sin cadenas.
- Sin conflicto trailing-slash (`/services` responde `200` directo).
- Jerarquía legible: `/services/enfermeria-a-domicilio/inyeccion-neurobionta-26634346`.

Mal:
- **Sufijos de ID numérico** en cada slug (`-26634346`, `-5651740`). Ruido, no aportan nada semántico y delatan el builder.
- **Slugs de sistema en inglés en un sitio en español:** `/about-us/`, `/services/`, `/reviews`, `/booking`, `/privacy-policy`, `/terms-and-conditions`, `/merchant-policies`, `/return-and-refund-policy`. Mezcla incoherente (`/about-us/quienes-somos-5651740`).
- **El activo no es propio.** Vive en `draska.ueniweb.com`. Toda la autoridad construida es intransferible: si Ueni cierra la cuenta, se pierde el dominio, el historial y los enlaces. `www.draska.ueniweb.com` ni siquiera resuelve (`000`).
- `/return-and-refund-policy` en un negocio de enfermería a domicilio: página de plantilla irrelevante, indexable.

### 2.5 Mobile — PARCIAL

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
```

- `width=device-width` y `viewport-fit=cover` correctos.
- **`maximum-scale=1.0` + `user-scalable=no` bloquean el zoom de pinza.** Fallo de accesibilidad (WCAG 1.4.4) y auditoría fallida garantizada en Lighthouse. Crítico en un sector sanitario con usuarios mayores.
- `format-detection: telephone=no` desactiva la autodetección de teléfonos, pero sí hay enlaces `tel:+56 9 7883 3741` y `https://wa.me/56978833741` explícitos — decisión correcta.
- CSS responsive real: 1.172 media queries, breakpoints en 321/575/576/600/768/769/960/991/992/1200/1280/1920 px.
- `agent_ux_check.py` → **score 85**. 9 botones reales, 55 anclas reales, **0 widgets `div` con `onclick`**, 7 landmarks semánticos, 0 inputs sin label. Único fallo: 5 nodos interactivos sin nombre accesible (−15). Semántica HTML notablemente buena para un builder.

### 2.6 Core Web Vitals — RIESGO ALTO `[INFERIDO]`

Umbrales de referencia: LCP ≤ 2,5 s · INP ≤ 200 ms · CLS ≤ 0,1.

**Medición de red real:**

| Métrica | Valor |
|---|---|
| TTFB (5 muestras) | 0,375 / 0,383 / 0,390 / 0,409 / 0,419 s — muy estable |
| Conexión TCP | ~0,06-0,09 s |
| TLS | ~0,13-0,16 s |
| HTML comprimido (brotli) | **330.037 bytes** |
| HTML descomprimido | **2.030.170 caracteres** |
| Texto visible SSR | 3.822 caracteres |

**Composición del documento:**

| Bloque | Tamaño | % del doc |
|---|---|---|
| CSS inline (50 `<style>`) | **1.305.410 chars** | **64,3 %** |
| Markup del `<body>` | 236.145 chars | 11,6 % |
| JS inline (47 `<script>`) | 78.895 chars | 3,9 % |
| `window.__PRELOAD_DATA_` | 76.445 chars | 3,8 % |
| `window.__PRELOAD_TRANSLATIONS_` | 51.079 chars | 2,5 % |

El bloque `<style>` más grande pesa 339.370 chars por sí solo. Hay 1.373 `!important`.

**Riesgos derivados:**

1. **`[INFERIDO]` LCP / FCP — bloqueo por parseo de CSS.** ~1,3 MB de CSS inline en el `<head>` deben descomprimirse y parsearse antes del primer pixel. El TTFB excelente (0,38 s) queda neutralizado por el coste de parseo en CPU, que es lo que domina en móviles de gama media en Calama. Ratio texto/HTML: 3.822 / 2.030.170 = **0,19 %**.
2. **CRÍTICO — `srcset` de la imagen LCP parcialmente roto (404).** El `<link rel="preload" as="image">` del héroe declara 12 candidatos. Verificados uno a uno (2 intentos cada uno, resultado estable):

   | Candidato | Resultado |
   |---|---|
   | `c769_384a` (769w) | **404** (9 bytes) |
   | `c1538_768a` (1538w) | **404** (9 bytes) |
   | `c2307_1152a` (2307w) | **404** (9 bytes) |
   | `c496_500a` (496w) | 200 — 14.136 B |
   | `c992_1000a` (992w) | 200 — ~40 KB |
   | `c1400_1000a`, `c4032_1500a` | 200 — ~40 KB |

   El atributo es `imagesizes="(max-width: 769px) 769px, (max-width: 992px) 496px, ..."`. En un móvil (≤769 px CSS) el slot declarado es 769 px; con DPR 2-3 el navegador selecciona el candidato de 1538w o 2307w — **ambos 404**. Es decir, **la ruta móvil de la imagen LCP falla**. Peor: los 404 se sirven con `cache-control: max-age=31536000`, cacheando el fallo un año, y `cf-cache-status: HIT`. El `href` por defecto del preload apunta a `c4032_1500a` (4032 px de ancho) para un slot de 769 px.
3. **`[INFERIDO]` INP — 43 scripts externos.** Todos desde `s.uenicdn.com`, con hash de build compartido. Preloads de `vendors.js` y `painter.js` como `as="script"`.
4. **CLS — mitigado parcialmente.** 26 declaraciones `aspect-ratio` y `font-display: swap` en 20 de 21 `@font-face`. Pero **0 imágenes con `width`/`height` explícitos** y **0 `loading="lazy"`** en todo el documento.
5. **10 preloads de fuentes simultáneos** (5 pesos de Montserrat + 5 de Lato). Compiten por ancho de banda con la imagen LCP en la misma ventana de arranque.
6. **HTML no cacheable en el borde:** `cache-control: public, no-cache` + `cf-cache-status: DYNAMIC`. Cada visita golpea el origen.
7. `preload_check.py` → **score 50**. Sin `speculationrules`, sin prerender. Señales de bfcache limpias (sin `no-store`, sin listeners `unload`/`beforeunload`).
8. Preload de `https://api.maptiler.com/maps/streets/style.json?key=...` como `as="style"` — un mapa interactivo de terceros priorizado en el arranque. **La API key de MapTiler viaja en claro en el HTML.**

### 2.7 Structured Data — PARCIAL

JSON-LD `LocalBusiness` en la home:

```json
{"@context":"https://schema.org","@type":"LocalBusiness","@id":"https://draska.ueniweb.com",
 "name":"INYECCIÓN A DOMICILIO CALAMA",
 "address":{"@type":"PostalAddress","streetAddress":"Punta Arenas","addressLocality":"Calama","postalCode":"139000","addressCountry":"CHILE"},
 "geo":{"@type":"GeoCoordinates","latitude":-22.4703921,"longitude":-68.9293679},
 "url":"https://draska.ueniweb.com","telephone":"+56978833741","priceRange":"$",
 "sameAs":["https://www.facebook.com/Inyecciones-a-domicilio-106866317602750","ChIJFfyXTPEJrJYRzcBJnjIC7wA"]}
```

Las páginas de servicio escalan bien: incluyen `Service`, `LocalBusiness`, `PostalAddress`, `OfferCatalog` (×2) y `Offer` (×2).

Errores concretos:
- **`sameAs` inválido:** el segundo valor `ChIJFfyXTPEJrJYRzcBJnjIC7wA` es un Google Place ID en crudo, no una URL. `sameAs` exige URLs. Rompe la validación.
- **`addressCountry: "CHILE"`** — debe ser el código ISO 3166-1 alpha-2: `"CL"`.
- **Tipo demasiado genérico:** `LocalBusiness` pudiendo usar `MedicalBusiness` / `Nursing`, más preciso para el sector.
- Faltan: `image`, `openingHoursSpecification`, `areaServed`, `aggregateRating` (la página muestra "8 Opiniones powered by Google" pero **no las marca en schema** — se pierde la estrella en SERP), `hasOfferCatalog` en la home.
- Inconsistencia menor `@id` (`...com`) vs canonical (`...com/`).
- **Sin `og:image` y sin ninguna Twitter Card** (`twitter_card: {}`, 0 ocurrencias de `twitter:`). Cada vez que alguien comparte el enlace por WhatsApp — canal dominante en Chile para este servicio — sale sin miniatura. Y el sitio incluye botones de compartir a Facebook y Twitter que producen previsualizaciones vacías.

### 2.8 JavaScript Rendering — PASS

- `render_page.py --mode auto` no necesitó Playwright: **`is_spa: false`**. HTML pre-renderizado en servidor.
- Contenido crítico presente en el HTML crudo: `<h1>INYECCIÓN A DOMICILIO CALAMA</h1>`, los 6 `<h2>`, los 5 `<h3>`, el texto de servicios, el teléfono y los enlaces.
- **Paridad con Googlebot verificada:** fetch con UA de Googlebot Smartphone → `200`, mismo `<title>`, mismo canonical, mismo `<h1>`. Delta de tamaño 5,71 % (variación de A/B del builder, no cloaking).
- React Helmet gestiona el `<head>` pero **sus etiquetas ya vienen serializadas en la respuesta** (`data-react-helmet="true"` presente en el HTML crudo). No dependen de hidratación.
- Solo 1 `<noscript>`, 1 `<iframe>`, 222 SVG inline (iconografía sin peticiones extra — bien).

### 2.9 IndexNow — FAIL

No implementado. `/indexnow.txt` → `404`. Sin fichero de clave en la raíz. Bing, Yandex y Naver dependen del rastreo pasivo.

---

## 3. Issues priorizados

### Critical
1. **`srcset` de la imagen LCP roto en la ruta móvil** — 3 de 12 candidatos devuelven 404, incluidos los dos que un móvil selecciona (1538w, 2307w). 404 cacheados un año.
2. **Cero cabeceras de seguridad** — faltan las 6 (HSTS, CSP, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy).
3. **Página `/test` indexable, en el sitemap y enlazada en el menú global.**

### High
4. **2,03 MB de HTML con 1,3 MB de CSS inline (64 %)** para 567 palabras. Ratio texto/HTML 0,19 %. `[INFERIDO]` riesgo de LCP/FCP.
5. **`user-scalable=no` + `maximum-scale=1.0`** — bloquea el zoom. Fallo WCAG 1.4.4 en sector salud.
6. **Sin `og:image` ni Twitter Cards** — cero preview al compartir por WhatsApp/Facebook.
7. **Dependencia total de un subdominio ajeno** (`*.ueniweb.com`). Autoridad intransferible.
8. **Título duplicado** entre `/` y `/services`.

### Medium
9. `sameAs` con Place ID en crudo y `addressCountry: "CHILE"` no ISO → schema inválido.
10. `aggregateRating` ausente pese a mostrar 8 reseñas de Google.
11. 43 scripts externos + GTM. `[INFERIDO]` riesgo de INP.
12. HTML no cacheable en borde (`no-cache` / `DYNAMIC`).
13. Slugs de sistema en inglés + sufijos de ID numérico.
14. 10 preloads de fuentes compitiendo con la imagen LCP.
15. 0 imágenes con `width`/`height`; 0 `loading="lazy"`.
16. Email en claro en `<meta>` pese a ofuscar los `mailto:`.
17. API key de MapTiler expuesta en el HTML.

### Low
18. IndexNow no implementado.
19. Sin `speculationrules` (`preload_check` score 50).
20. Sin HTTP/3 / `alt-svc` estando tras Cloudflare.
21. 5 nodos interactivos sin nombre accesible (`agent_ux_check` 85/100).
22. Sin directivas para crawlers de IA en `robots.txt`.
23. Páginas de plantilla irrelevantes indexables (`/return-and-refund-policy` en un negocio de enfermería).
24. 1.373 `!important` en el CSS.

---

## 4. QUÉ REPLICAR (ordenado por impacto/esfuerzo)

**R1. SSR real, no CSR.** Es la base de todo lo que le funciona. El HTML crudo ya trae `<title>`, canonical, `<h1>`, JSON-LD y todo el copy. Usa React Helmet pero serializado en servidor. → Astro, Next.js en modo estático/SSG o cualquier generador estático. Verificar siempre con `render_page.py --mode auto` que devuelva `is_spa: false`.

**R2. Carga diferida de GTM/Analytics — la mejor práctica del sitio.** Copiar el patrón literalmente. El propio comentario del código lo explica:

```js
var evts=['pointerdown','keydown','touchstart','wheel','scroll']; var opts={passive:true};
evts.forEach(function(e){w.addEventListener(e,loadGtm,opts)});
w.addEventListener('load',function(){setTimeout(loadGtm,3500)});
```

Mantiene ~330 KB de `gtm.js` + `gtag` + analytics fuera de la ruta crítica, con un stub de `dataLayer` que encola eventos hasta la primera interacción (o 3,5 s tras `load` como fallback). Impacto directo en INP y TBT sin perder medición.

**R3. Estructura de encabezados geolocalizada.** `<h1>INYECCIÓN A DOMICILIO CALAMA</h1>` — servicio + ciudad, en el H1, sin adornos de marca. `<title>` = `Draska - Enfermería a domicilio | Calama`. Los H2/H3 cubren la intención transaccional local: Servicios, Facilidades, Opiniones, Ubicación, Áreas cubiertas. **Esto es probablemente la causa principal de que posicione pese a lo simple.**

**R4. Una página por servicio, con slug descriptivo y schema propio.** `/services/enfermeria-a-domicilio/inyeccion-neurobionta-...`, `.../inyeccion-anticonceptiva-...`, `.../inyeccion-medicamento-...`. Cada una con `<title>` único (`INYECCIÓN NEUROBIONTA - Enfermería a domicilio - Draska...`) y JSON-LD `Service` + `OfferCatalog` + `Offer`. Captura long-tail ("inyección neurobionta Calama"). Replicar el patrón **pero sin los IDs numéricos y con slugs en español**.

**R5. `LocalBusiness` con NAP + geo.** Nombre, dirección, `postalCode`, `telephone` en E.164 (`+56978833741`), `geo` con lat/long reales de Calama, `priceRange`. Corregir los errores de la sección 2.7.

**R6. Preload de la imagen LCP con `fetchpriority="high"` + `imagesrcset` + `imagesizes`.** El patrón es correcto; **la ejecución de Ueni está rota**. Replicar la técnica y **validar cada candidato del srcset con un `curl` de estado antes de publicar**.

**R7. `font-display: swap` en todos los `@font-face`** (20 de 21 lo tienen) + `aspect-ratio` en contenedores de imagen (26 declaraciones). Buen control de CLS. **Pero reducir a 2 pesos por familia, no 10 preloads.**

**R8. Contacto de fricción cero.** `tel:` + `https://wa.me/56978833741` visibles, con `format-detection: telephone=no` para controlar el render. WhatsApp es el canal de conversión de este rubro en Chile.

**R9. HTML semántico + botones reales.** 9 `<button>` y 55 `<a>` reales, **0 `div` con `onclick`**, 7 landmarks, 0 inputs sin label → `agent_ux_check` 85/100. Crítico para accesibilidad y para agentes de IA que naveguen el sitio.

**R10. Higiene básica de red:** 301 HTTP→HTTPS sin cadenas, cero redirecciones en la home, canonical absoluto autorreferencial en todas las páginas, 404 reales, brotli activo, CDN con TTFB ~0,38 s estable, 222 SVG inline en vez de peticiones de iconos.

**R11. Sitemap propio + declarado en robots.txt.** Un solo `sitemap.xml` con `lastmod` **honesto**. Esa parte sí es replicable (los otros dos no lo son).

---

## 5. QUÉ EVITAR / MEJORAR en el sitio nuevo

**E1. No repliques los 3 sitemaps.** Está demostrado que es fontanería de plataforma: el nº 2 es un duplicado byte-a-byte del nº 1 en otro host, y el nº 3 no contiene ninguna URL de draska (1.000 URLs de 195 negocios ajenos). Para un sitio propio: **un sitemap, declarado en `robots.txt` y enviado por Search Console.** Añadir un segundo sitemap con las mismas URLs en otro host no aporta nada si no controlas ese host con autoridad.

**E2. Dominio propio desde el día uno.** `draskaenfermeria.cl` o similar. Ese subdominio es el mayor riesgo estructural del sitio de referencia. Si algún día migra, pierde todo.

**E3. Presupuesto de peso estricto.** Objetivo: **< 100 KB de HTML comprimido** (draska: 330 KB) y **< 250 KB descomprimido** (draska: 2,03 MB). Ratio texto/HTML > 10 % (draska: 0,19 %). Critical CSS inline ≤ 14 KB, el resto en hoja externa cacheable.

**E4. Nunca `user-scalable=no`.** Usar exactamente:
```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
```

**E5. Implementar las 6 cabeceras de seguridad** (trivial en Cloudflare Transform Rules, Netlify `_headers` o Vercel `headers`):
```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
Content-Security-Policy: default-src 'self'; img-src 'self' https: data:; script-src 'self' https://www.googletagmanager.com
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), camera=(), microphone=(), interest-cohort=()
```

**E6. Añadir `og:image` (1200×630) + `twitter:card=summary_large_image`.** Imprescindible para WhatsApp. Es una omisión gratuita en draska.

**E7. Cero páginas de prueba/plantilla en producción.** Ni `/test`, ni política de devoluciones en un negocio de enfermería. Si algo debe existir sin indexarse: `noindex` **y** fuera del sitemap **y** fuera del menú.

**E8. Un `<title>` único por URL.** Auditar duplicados antes de publicar.

**E9. Slugs íntegramente en español, sin IDs.** `/servicios/inyeccion-anticonceptiva-calama`, `/nosotros`, `/opiniones`, `/reservar`. Cada slug es una oportunidad de keyword local desperdiciada en draska.

**E10. Validar cada candidato de `srcset` en CI.** El fallo más caro de draska. Además, servir **AVIF/WebP con negociación por `Accept`** — el CDN de Ueni devuelve JPEG idéntico aunque el cliente anuncie `image/avif,image/webp`. Y añadir `width`/`height` explícitos + `loading="lazy"` en todo lo que esté bajo el pliegue.

**E11. Cachear el HTML en el borde.** Draska usa `cache-control: public, no-cache` con `cf-cache-status: DYNAMIC`. Un sitio estático de servicios debe ir a `s-maxage` alto con purga en el deploy.

**E12. Ampliar y corregir el schema:**
- `@type: MedicalBusiness` (o `Nursing`) en vez de `LocalBusiness`.
- `addressCountry: "CL"` (ISO), no `"CHILE"`.
- `sameAs` **solo con URLs**. El Place ID va en `hasMap`, nunca en `sameAs`.
- Añadir `openingHoursSpecification`, `areaServed` (Calama y localidades cubiertas), `image`, `aggregateRating` con reseñas reales, `hasOfferCatalog`.
- Validar con `claude-seo run schema_generate.py` y el hook `validate-schema.py`.

**E13. Contenido: superar las 567 palabras.** Draska posiciona *a pesar de* su contenido fino, seguramente por baja competencia local. Un competidor con 1.200-1.500 palabras útiles (preparación previa, tipos de inyección, cobertura por barrio, precios, FAQ) más FAQ schema lo desplaza sin esfuerzo. **Es la oportunidad más grande del análisis.**

**E14. Implementar IndexNow** (draska: `/indexnow.txt` → 404). Fichero de clave en raíz + envío en cada deploy con `claude-seo run indexnow_submit.py`.

**E15. Gestión de crawlers de IA en `robots.txt`.** Draska no tiene ninguna directiva. Decidir explícitamente política para `GPTBot`, `ClaudeBot`, `PerplexityBot`, `Google-Extended`, `CCBot`. Para un negocio local, **permitirlos** suele convenir (visibilidad en respuestas de IA).

**E16. No expongas claves ni emails en el HTML.** Draska filtra la API key de MapTiler y el email en un `<meta>` en claro. Usa un mapa estático o un embed diferido tras interacción; el mapa interactivo de MapTiler es un lujo caro en la ruta crítica de una landing local.

**E17. Extras baratos que draska no tiene:** `speculationrules` para prerender de `/servicios/*` y `/contacto`, HTTP/3, y ≤ 2 pesos de fuente.

---

## 6. Findings estructurados (audit-data.json — categoría Technical SEO)

```json
{
  "category": "Technical SEO",
  "url": "https://draska.ueniweb.com/",
  "audit_date": "2026-09-05",
  "score": 66,
  "purpose": "competitive_benchmark",
  "data_limitations": ["pagespeed_check.py unavailable: PSI quota exhausted after 7 retries", "crux_history.py unavailable: GOOGLE_API_KEY not configured", "all CWV findings are source-inspection inferences, not measurements"],
  "categories": {
    "crawlability": {"status": "pass", "sitemaps_declared": 3, "sitemaps_valid": 3, "robots_disallow_rules": 0, "ai_crawler_directives": false},
    "indexability": {"status": "partial", "canonical": "self-referencing-absolute", "meta_robots": null, "hreflang": [], "issues": ["/test indexable and in sitemap and in global nav", "duplicate title between / and /services", "thin content 567 words"]},
    "security": {"status": "fail", "https": true, "hsts": false, "csp": false, "x_content_type_options": false, "x_frame_options": false, "referrer_policy_header": false, "permissions_policy": false, "cert_issuer": "Google Trust Services WE1", "cert_expires": "2026-10-11", "http_to_https_301": true, "http3": false, "leaks": ["maptiler_api_key_in_html", "email_in_plaintext_meta"]},
    "url_structure": {"status": "partial", "redirect_chains": 0, "clean_urls": true, "issues": ["numeric ID suffixes in slugs", "english system slugs on spanish site", "third-party subdomain dependency"]},
    "mobile": {"status": "partial", "viewport_present": true, "user_scalable_no": true, "media_queries": 1172, "agent_ux_score": 85},
    "core_web_vitals": {"status": "risk_high", "evidence": "inferred", "ttfb_median_s": 0.39, "html_bytes_br": 330037, "html_chars_raw": 2030170, "inline_css_chars": 1305410, "inline_css_pct": 64.3, "text_to_html_ratio_pct": 0.19, "external_scripts": 43, "font_preloads": 10, "images_with_dimensions": 0, "lazy_loaded_images": 0, "aspect_ratio_declarations": 26, "font_display_swap": 20, "preload_check_score": 50, "broken_srcset_candidates": ["c769_384a", "c1538_768a", "c2307_1152a"], "broken_srcset_cache_control": "max-age=31536000", "edge_cacheable_html": false},
    "structured_data": {"status": "partial", "types": ["LocalBusiness", "Service", "OfferCatalog", "Offer", "PostalAddress", "GeoCoordinates"], "errors": ["sameAs contains raw Google Place ID not a URL", "addressCountry CHILE not ISO CL"], "missing": ["og:image", "twitter_card", "aggregateRating", "openingHoursSpecification", "areaServed", "image"]},
    "js_rendering": {"status": "pass", "is_spa": false, "ssr": true, "googlebot_parity": true, "googlebot_size_delta_pct": 5.71},
    "indexnow": {"status": "fail", "key_file": false, "probe_status": 404}
  },
  "issue_counts": {"critical": 3, "high": 5, "medium": 9, "low": 7}
}
```
