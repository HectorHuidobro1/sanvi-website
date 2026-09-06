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

`tools/check_perf.py` se añade en una tarea posterior del proyecto (QA final de
rendimiento y accesibilidad). Si todavía no existe en este checkout, omitir esa
línea y verificar con los otros tres.

## Regenerar los rasters de marca

    cd ..
    python tools/shoot.py tools/og/og.html         --out sitio-sanvi/assets/img/og-sanvi.png         --width 1200 --height 630
    python tools/shoot.py tools/og/logo.html       --out sitio-sanvi/assets/img/logo-sanvi.png       --width 512  --height 512
    python tools/shoot.py tools/og/touch-icon.html --out sitio-sanvi/assets/img/apple-touch-icon.png --width 180  --height 180

## Estado del dominio (importante)

`https://www.sanvicalama.cl` es un **dominio de trabajo, todavía no registrado**.
Se usa como placeholder consistente en canonicals, `og:url`, sitemap, robots y
JSON-LD para que todo el SEO técnico esté ya cableado el día que exista un
dominio real. El sitio **no está desplegado** en ningún hosting todavía.

## Cambiar el dominio

Al comprar el dominio definitivo, ejecutar una sola vez desde la raíz del proyecto:

    grep -rl "www.sanvicalama.cl" sitio-sanvi/ | xargs sed -i 's|www\.sanvicalama\.cl|DOMINIO-NUEVO|g'
    python tools/check_site.py sitio-sanvi --content
    python tools/check_links.py sitio-sanvi

y actualizar manualmente la constante `SITE` en **ambos** archivos:

- `tools/check_site.py`
- `tools/check_links.py`

(Están duplicadas a propósito, no importadas de un módulo común; hay que tocar
las dos o los verificadores quedarán comprobando el dominio viejo.)

## Desplegar

Netlify o Cloudflare Pages, publicando esta carpeta tal cual. Sin comando de build.
En Netlify, `netlify.toml` ya desactiva `pretty_urls` (indispensable: el sitio usa
URLs `.html` reales) y aplica las cabeceras de seguridad. En Cloudflare Pages las
cabeceras vienen de `_headers`.

## Pendientes post-lanzamiento (por orden de impacto)

1. **Dominio real.** Registrar `sanvicalama.cl` (u otro dominio definitivo) y
   ejecutar el procedimiento de "Cambiar el dominio" de arriba.
2. **Google Business Profile.** Crear y verificar la ficha de Sanvi en Calama. Después:
   añadir al nodo `#business` del JSON-LD de las 4 páginas
   `"sameAs": ["https://www.google.com/maps/place/?q=place_id:PLACE_ID_REAL"]` y
   `"hasMap": "https://www.google.com/maps/place/?q=place_id:PLACE_ID_REAL"`.
   Hasta tener el Place ID real, no añadir nada: publicar un placeholder viola las
   políticas de datos estructurados.
3. **Número de registro sanitario.** Cuando esté disponible, publicarlo visible en
   `nosotros.html#equipo` y `index.html#equipo`, y añadir al `@graph` un nodo `Person`
   con `hasCredential` (`EducationalOccupationalCredential`, `credentialCategory: "license"`,
   `recognizedBy` Superintendencia de Salud). Es la mayor palanca de E-E-A-T del rubro.
4. **Fotos reales del equipo.** Reemplazar `assets/img/hero-cuidado.svg` y la ilustración
   de cobertura por fotografías propias en WebP con `srcset`. El markup ya lleva `width`,
   `height` y `alt` definitivos: sólo cambia el `src`.
5. **Reseñas.** Motor sostenido de 2 a 4 reseñas mensuales en GBP, pedidas por WhatsApp
   30–60 min después de cada atención. Cuando existan reseñas reales y visibles, sustituir
   la sección `#opiniones` de la home por testimonios reales con nombre, sector y fecha.
6. **Sectores de Calama.** Ampliar la lista de `#cobertura` con los sectores reales que
   atiende el negocio, en index.html y contacto.html.

Ninguno de estos puntos bloquea el despliegue inicial: el sitio funciona y valida
en verde con el dominio placeholder, pero no debe presentarse como "en vivo" ni
promocionarse públicamente hasta cubrir al menos el punto 1.
