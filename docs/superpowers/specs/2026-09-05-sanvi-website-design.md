# Sanvi — sitio web de enfermería/inyecciones a domicilio (Calama)

Fecha: 2026-09-05

## Contexto de negocio

- **Marca:** Sanvi (rebrand de "Draska", mismo negocio real).
- **Rubro:** enfermería e inyecciones a domicilio.
- **Ubicación / cobertura:** Calama, Chile. Solo Calama por ahora (sin expansión a otras comunas todavía).
- **Teléfono / WhatsApp:** +56 9 7883 3741 (se mantiene el número actual).
- **Horario:** 8:00–21:00, con agendamiento de cita previo (no walk-in).
- **Sitio anterior:** https://draska.ueniweb.com/ (subdominio del builder Ueni). Se reemplaza por un sitio propio, mismo negocio, nuevo nombre/logo.

### Servicios y precios (CLP)

| Servicio | Precio |
|---|---|
| Inyección intramuscular (incluye multivitamínico/Neurobionta y anticonceptiva mensual) | $10.000 |
| Inyección intravenosa | $17.000 |
| Curación simple | $15.000 |
| Curación compleja | $33.000 |

Se descartaron del catálogo "control de signos vitales" y "sueroterapia/hidratación IV" (decisión explícita del negocio).

## Aprendizajes de la auditoría del competidor (Draska)

Se ejecutaron 5 auditorías especializadas (`claude-seo`) sobre draska.ueniweb.com, guardadas en `draska-audit/findings/` (technical.md, local.md, schema.md, content.md, sxo.md). Resumen de lo accionable:

- **Por qué rankea pese a ser básico:** H1/title con patrón "servicio + ciudad", schema `LocalBusiness` con NAP/geo, SSR real (paridad con Googlebot), página de baja competencia local, nombre de negocio = keyword exacta en Google Business Profile (táctica arriesgada, no la replicamos).
- **Fallas a NO repetir:** código postal inválido en el schema, `addressCountry` mal formateado, `sameAs` con un Place ID crudo (no URL), Google Business Profile nunca verificado, reseñas estancadas (última hace ~28 meses, varias vacías), CSS inline de 1.3MB, imágenes rotas en el tamaño que carga un celular, cero cabeceras de seguridad, página `/test` indexable en el sitemap.
- **Oportunidad clara:** con 1.200–1.500 palabras reales, precios visibles (el rubro entero los oculta) y señales E-E-A-T verificables, se desplaza a Draska en 4–8 meses estimados.
- **SXO:** Google premia aquí páginas tipo "Local Service" (no blogs). Above the fold debe llevar precio + credenciales + WhatsApp con mensaje precargado.

## Sistema visual

- **Paleta:** Turquesa como color base (`#0F9B8E` → `#14B8A6` → `#2DD4BF` en gradientes) + Coral (`#FF6B57`) como acento de acción (botones/CTA). Fondo claro `#F4FBFA`, texto oscuro `#0B2A3A`.
- **Personalidad:** moderna y dinámica — cálida pero fresca, no clínica-fría ni excesivamente corporativa.
- **Tipografía:** `Sora` para titulares (geométrica, moderna), `Inter` para cuerpo de texto (legibilidad). Google Fonts con `font-display: swap`.
- **Hero (above the fold):** estructura "B" — headline (servicio + ciudad) → badges de confianza (acreditación general del personal, horario 8am–9pm) → línea de precio ("Desde $10.000") → botón WhatsApp con mensaje precargado. Validado con el usuario vía companion visual (mockups A/B/C comparados, se eligió paleta A y estructura de hero B).
- **Imágenes:** generadas/stock de alta calidad por ahora (el negocio no tiene fotos reales todavía); diseñar los espacios para reemplazo fácil por fotos reales del equipo más adelante.

## Arquitectura del sitio (4 páginas)

1. **`/` (Home):** hero → tabla de precios de los 4 servicios → qué incluye/aviso de receta médica → resumen de los 4 servicios (con anclas a `/servicios`) → cómo funciona en 3 pasos → zona de cobertura (Calama) → equipo/credenciales (versión liviana, ver abajo) → reseñas reales → FAQ breve → CTA final WhatsApp.
2. **`/servicios`:** los 4 servicios en profundidad, cada uno con id-ancla propio (`#inyeccion-intramuscular`, `#inyeccion-intravenosa`, `#curacion-simple`, `#curacion-compleja`), incluyendo qué es, precio, duración estimada, requisitos (receta médica cuando aplique) y CTA propio.
3. **`/nosotros`:** historia breve, protocolo de bioseguridad/higiene, por qué elegir atención a domicilio vs. clínica, y la sección de credenciales del equipo.
4. **`/contacto`:** formulario simple, WhatsApp con mensaje precargado, horario, cobertura Calama, mapa simple.

Cada página con `<title>` y meta description propios, orientados a variantes de keyword local (evitando el error de Draska de metadatos casi vacíos en páginas internas).

### Sección de equipo/credenciales — decisión explícita

El negocio **no tiene aún** el número de registro ante la Superintendencia de Salud a mano (el hallazgo de mayor impacto E-E-A-T del reporte de contenido). Se implementa una **versión liviana**: descripción general ("técnicos en enfermería de nivel superior, registrados ante la autoridad sanitaria") sin número específico. Se deja preparado para actualizar con el número real y foto del equipo apenas estén disponibles — es la mejora de mayor prioridad post-lanzamiento.

## Datos estructurados (schema.org)

`@graph` con:

- `@type: MedicalBusiness` (no `LocalBusiness` genérico) + `additionalType`/`medicalSpecialty: Nursing`.
- NAP corregido: código postal real de Calama (`1390000`), `addressCountry: "CL"`.
- `areaServed: Calama`.
- `openingHoursSpecification`: 8:00–21:00 con agendamiento previo.
- `hasOfferCatalog` con 4 `Service`, cada uno con su `offers`/precio.
- `sameAs` con URL bien formada del perfil de Google Business (pendiente de creación/verificación del perfil — no repetir el error de Draska de dejarlo sin verificar).
- `image` apuntando a una imagen real del hero.
- Sin `AggregateRating` hasta tener reseñas reales (evitar reseñas falsas/vacías como Draska).

Ejemplo completo de JSON-LD de referencia en `draska-audit/findings/schema.md`.

## Stack técnico

- **HTML/CSS/JS puro, sin framework.** Decisión explícita tras discutir con el usuario: el aspecto visual lo define el CSS/diseño, no el framework; React agregaría bundle JS innecesario y empeoraría Core Web Vitals para un sitio de 4 páginas sin estado complejo. Reevaluar si el negocio escala a blog grande/multi-ciudad/panel admin.
- Imágenes responsivas (`srcset`, WebP), lazy-loading, `og:image` propio.
- CSS propio y compacto (evitar el CSS inline masivo de Draska).
- Scripts de terceros (si los hay) diferidos hasta primera interacción.
- Cabeceras de seguridad básicas vía configuración del hosting elegido (CSP, X-Content-Type-Options, etc.).
- Sitemap limpio desde el día 1, sin páginas de prueba indexables.
- Dominio y hosting: **por definir** (el usuario decidirá el dominio más adelante; sitio estático listo para Netlify/Vercel/Cloudflare Pages).

## QA antes de publicar

- Auditoría de UX/accesibilidad con la skill `impeccable`.
- Verificación de Core Web Vitals/Lighthouse con el runtime de `claude-seo`.
- Validación del schema JSON-LD (0 errores).

## Modelo de ejecución (preferencia del usuario)

- **Planeación/arquitectura:** agentes en modelo Opus.
- **Creación/código del sitio:** agentes en modelo Sonnet.

## Fuera de alcance de este spec (siguiente fase)

- Registro y verificación del Google Business Profile de Sanvi.
- Obtención del número de registro sanitario real y fotos reales del equipo.
- Elección y compra de dominio.
- El "loop" de auditoría SEO recurrente post-lanzamiento (`claude-seo`) hasta lograr posicionamiento en Google — se abordará una vez el sitio esté publicado.
