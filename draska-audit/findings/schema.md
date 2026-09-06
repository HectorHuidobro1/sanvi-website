# Auditoría de Structured Data — https://draska.ueniweb.com/

- **Fecha:** 2026-09-05
- **URL auditada:** https://draska.ueniweb.com/ (HTTP 200, sin redirecciones)
- **Renderizado:** `render_page.py --mode auto` y `--mode always`. `is_spa: false` — el JSON-LD está **server-rendered** (idéntico en `raw_content` y en el DOM renderizado). No hay inyección vía React Helmet.
- **Rubro:** inyecciones / enfermería a domicilio (Calama, Región de Antofagasta, Chile)
- **Propósito:** benchmark competitivo para diseñar un schema superior en un sitio nuevo del mismo rubro.

---

## 1. Detección

| Formato | Bloques | Bytes | Tipos detectados |
|---|---|---|---|
| JSON-LD | 1 | 539 | `LocalBusiness`, `PostalAddress`, `GeoCoordinates` |
| Microdata | 0 | — | — |
| RDFa | 0 | — | — |

**Un único bloque JSON-LD, 10 propiedades de nivel raíz.** Es el schema por defecto que genera la plataforma UENI: sin personalización, sin grafo, sin servicios, sin horarios.

No existe: `Organization`, `WebSite`, `WebPage`, `BreadcrumbList`, `Service`, `OfferCatalog`, `Person`, `Review`.

---

## 2. Validación del bloque existente

Ejecutado con script propio (`validate.py`, checklist de 12 puntos) sobre el artefacto extraído con `--json-ld-output`.

**Resultado: JSON sintácticamente válido — 3 errores, 17 avisos.**

### Aciertos (9)

| Check | Estado |
|---|---|
| `@context` = `https://schema.org` (https, no http) | PASS |
| `@type` válido y no deprecado | PASS |
| Propiedades requeridas (`@type`, `name`, `address`) | PASS |
| `telephone` en formato E.164 (`+56978833741`) | PASS |
| Sin texto placeholder | PASS |
| URLs de `url` / `@id` absolutas | PASS |
| `geo` plausible para Calama (-22.4704, -68.9294) | PASS |
| Bloque server-rendered (indexable sin JS) | PASS |
| Un solo bloque, sin duplicados ni conflicto de entidades | PASS |

### Errores (3) — Critical

| # | Propiedad | Valor actual | Problema | Corrección |
|---|---|---|---|---|
| E1 | `address.addressCountry` | `"CHILE"` | No es ISO 3166-1 alpha-2. Google espera código de 2 letras; un string libre puede fallar la resolución geográfica. | `"CL"` |
| E2 | `address.postalCode` | `"139000"` | Código postal chileno inválido (6 dígitos; el formato es de 7). Calama = `1390000`. Le falta un dígito. | `"1390000"` |
| E3 | `sameAs[1]` | `"ChIJFfyXTPEJrJYRzcBJnjIC7wA"` | **Es un Google Place ID crudo metido dentro de `sameAs`, que exige URLs absolutas.** Valor de tipo inválido: no aporta reconciliación de entidad y ensucia el grafo. | `"https://www.google.com/maps/place/?q=place_id:ChIJFfyXTPEJrJYRzcBJnjIC7wA"` y además duplicarlo en `hasMap`. |

E3 es el error más interesante desde el punto de vista competitivo: el competidor **tiene** el Place ID (existe ficha de Google Business Profile) pero lo desperdicia por no formatearlo como URL. La conexión sitio ↔ ficha de Maps no se está declarando.

### Avisos relevantes (17)

- `address.addressRegion` ausente (debería ser `"Antofagasta"`).
- `address.streetAddress` = `"Punta Arenas"` — sin numeración y **ambiguo**: "Punta Arenas" es también una ciudad chilena a 3.000 km. Riesgo real de desambiguación errónea.
- `@id` idéntico a `url` y sin fragmento — impide construir un `@graph` enlazable.
- Propiedades recomendadas ausentes: `image`, `logo`, `description`, `email`, `openingHoursSpecification`, `areaServed`, `hasMap`, `aggregateRating`, `review`, `currenciesAccepted`, `paymentAccepted`, `makesOffer`, `hasOfferCatalog`.
- `@type` genérico (ver sección 3).

---

## 3. ¿Es `LocalBusiness` suficiente? — No

**Recomendación: `MedicalBusiness`.**

`MedicalBusiness` es subtipo directo de `LocalBusiness`, por lo que **hereda todas sus propiedades** (`address`, `geo`, `openingHoursSpecification`, `priceRange`, `aggregateRating`…) y **sigue siendo elegible para el rich result de LocalBusiness** en Google. No se pierde nada y se gana precisión semántica: se declara explícitamente que la entidad es un prestador de salud, algo relevante para clasificación YMYL y para motores generativos.

Estrategia de tipado recomendada:

```json
"@type": "MedicalBusiness",
"additionalType": [
  "https://schema.org/Nursing",
  "https://www.wikidata.org/wiki/Q1145306"
],
"medicalSpecialty": "Nursing"
```

Notas de decisión:

- **`Nursing` como `@type` directo**: existe en schema.org como subtipo de `MedicalBusiness`, pero es un término poco frecuente y de soporte irregular. Más seguro usarlo vía `additionalType` + `medicalSpecialty`, manteniendo `MedicalBusiness` como tipo principal.
- **No usar `MedicalClinic`**: implica instalación física. Este negocio es 100 % móvil (service-area business). Usarlo solo si en el futuro abren consulta con atención al público.
- **No usar `Physician`**: son técnicos de nivel superior en enfermería, no médicos. Declararlo sería una tergiversación en un contexto YMYL.
- **`availableService`** pertenece a `MedicalOrganization` (vía `MedicalClinic`/`Hospital`), no a `MedicalBusiness`. Por eso el catálogo se modela con `hasOfferCatalog` + `makesOffer` + nodos `Service`, válidos por herencia de `Organization` y ampliamente entendidos.

**Negocio sin dirección pública (SAB):** si en Google Business Profile la dirección está oculta y solo se declara zona de servicio, en el JSON-LD conviene omitir `streetAddress` y dejar `addressLocality` + `addressRegion` + `addressCountry`, apoyándose en `areaServed`. La coherencia NAP con la ficha de GBP manda por encima de la completitud del schema.

---

## 4. Brechas del competidor = oportunidades para el sitio nuevo

| Propiedad ausente | Impacto | Prioridad |
|---|---|---|
| `openingHoursSpecification` | Sin horarios no hay señal de "abierto ahora"; crítico en un servicio de urgencia domiciliaria. | Critical |
| `areaServed` / `serviceArea` | El negocio es *service-area*: sin esto no se declara la cobertura geográfica (Calama, provincia de El Loa, radio en km). Es la propiedad más importante que le falta. | Critical |
| `hasOfferCatalog` + `Service` | Sus 3 servicios (multivitamínicos/Neurobionta, anticonceptiva, signos vitales) están solo en texto plano. Ninguno es una entidad. Cero anclaje para búsquedas de intención específica ni para respuestas de IA. | Critical |
| `image` / `logo` | Google exige `image` para elegibilidad plena del panel de LocalBusiness. | Critical |
| `description` | Resumen de entidad para SERP y motores generativos. | High |
| `hasMap` + `sameAs` bien formado | Vincula sitio ↔ ficha de Maps. El competidor tiene el Place ID pero mal formateado. | High |
| `Person` + `hasCredential` | El competidor menciona en texto que están "inscritos en la superintendencia de salud" pero **no lo marca**. Formalizar la acreditación como `EducationalOccupationalCredential` es la mayor palanca de E-E-A-T disponible en este rubro YMYL. | High |
| `aggregateRating` / `review` | Ver caveat abajo. | Medium |
| `BreadcrumbList` / `WebSite` / `WebPage` | Rich result de breadcrumbs + grafo del sitio. | Medium |
| `paymentAccepted`, `currenciesAccepted`, `availableLanguage` | Señales de completitud. | Low |

### Caveat importante sobre reseñas

Google **ignora las reseñas autorreferenciales** (*self-serving*) marcadas en `LocalBusiness` y `Organization` y sus subtipos — lo que incluye `MedicalBusiness`. Marcar `aggregateRating` con reseñas alojadas en el propio sitio **no producirá estrellas en la SERP**. Se incluye en la plantilla porque sí aporta a la comprensión de entidad y a los motores generativos, pero:

1. Solo incluirlo si las reseñas están **visiblemente publicadas en la página**.
2. Nunca inventar valores: `aggregateRating` sin reseñas reales visibles viola las políticas de spam de datos estructurados.
3. El valor real de reputación se captura en **Google Business Profile**, no aquí.

### Caveat sobre `FAQPage`

Google retiró los rich results de FAQ para **todos** los sitios el 7 de mayo de 2026. Marcar `FAQPage` **ya no produce ninguna funcionalidad en la SERP**. Prioridad: **Info**.

- Añadirlo solo si se acepta que el beneficio en visibilidad AI/GEO **no está confirmado**.
- Si el sitio publica preguntas reales de usuarios con respuestas, el tipo correcto es **`QAPage`**, no `FAQPage`.
- **No usar `HowTo`** (rich results eliminados en septiembre de 2023) aunque se documente "cómo prepararse para la inyección".

Por eso la plantilla de la sección 6 **no incluye `FAQPage`**: el esfuerzo rinde más en las páginas de servicio.

---

## 5. Comparativa

| Dimensión | Competidor (draska) | Plantilla propuesta |
|---|---|---|
| Bloques / nodos | 1 nodo | 9 nodos en `@graph` |
| Bytes | 539 | ~11.000 |
| Tipo principal | `LocalBusiness` | `MedicalBusiness` + `additionalType` |
| Servicios modelados | 0 | 3 nodos `Service` + `OfferCatalog` |
| Cobertura geográfica | no declarada | `City` + `AdministrativeArea` + `GeoCircle` |
| Horarios | ninguno | `openingHoursSpecification` + festivos |
| Acreditación profesional | solo texto | `Person` + `hasCredential` (2) |
| Errores de validación | 3 | 0 |

---

## 6. JSON-LD mejorado — plantilla de partida

Validado con `validate_graph.py`: **0 errores**, 9 nodos, todas las referencias `@id` resueltas, sin tipos deprecados, fechas ISO 8601, URLs absolutas.

> **Antes de publicar, reemplazar los placeholders:** `ejemplo-enfermeria.cl`, `+56912345678`, `CHIJ_TU_PLACE_ID_REAL`, `Nombre Apellido`, `RNPI-000000`, `tu-pagina`, `tu-cuenta`. Publicar con placeholders viola las políticas de datos estructurados.

Colocar en el `<head>` de la home, server-rendered (no inyectar por JS):

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "MedicalBusiness",
      "@id": "https://www.ejemplo-enfermeria.cl/#business",
      "additionalType": [
        "https://schema.org/Nursing",
        "https://www.wikidata.org/wiki/Q1145306"
      ],
      "name": "Enfermería a Domicilio Calama",
      "alternateName": "Inyecciones a Domicilio Calama",
      "legalName": "Servicios de Enfermería Ejemplo SpA",
      "description": "Servicio móvil de enfermería a domicilio en Calama: inyecciones intramusculares, anticonceptivos inyectables, multivitamínicos (Neurobionta) y control de signos vitales. Técnicos en enfermería de nivel superior inscritos en la Superintendencia de Salud.",
      "url": "https://www.ejemplo-enfermeria.cl/",
      "logo": {
        "@type": "ImageObject",
        "@id": "https://www.ejemplo-enfermeria.cl/#logo",
        "url": "https://www.ejemplo-enfermeria.cl/img/logo.png",
        "width": 512,
        "height": 512,
        "caption": "Enfermería a Domicilio Calama"
      },
      "image": [
        "https://www.ejemplo-enfermeria.cl/img/enfermera-domicilio-calama-1x1.jpg",
        "https://www.ejemplo-enfermeria.cl/img/enfermera-domicilio-calama-4x3.jpg",
        "https://www.ejemplo-enfermeria.cl/img/enfermera-domicilio-calama-16x9.jpg"
      ],
      "telephone": "+56912345678",
      "email": "contacto@ejemplo-enfermeria.cl",
      "priceRange": "$$",
      "currenciesAccepted": "CLP",
      "paymentAccepted": "Efectivo, Transferencia bancaria, Tarjeta de débito, Tarjeta de crédito",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Av. Granaderos 1234, Oficina 5",
        "addressLocality": "Calama",
        "addressRegion": "Antofagasta",
        "postalCode": "1390000",
        "addressCountry": "CL"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": -22.4667,
        "longitude": -68.9333
      },
      "hasMap": "https://www.google.com/maps/place/?q=place_id:CHIJ_TU_PLACE_ID_REAL",
      "sameAs": [
        "https://www.facebook.com/tu-pagina",
        "https://www.instagram.com/tu-cuenta/",
        "https://www.google.com/maps/place/?q=place_id:CHIJ_TU_PLACE_ID_REAL"
      ],
      "areaServed": [
        {
          "@type": "City",
          "name": "Calama",
          "sameAs": "https://www.wikidata.org/wiki/Q233264"
        },
        {
          "@type": "AdministrativeArea",
          "name": "Provincia de El Loa"
        },
        {
          "@type": "GeoCircle",
          "geoMidpoint": {
            "@type": "GeoCoordinates",
            "latitude": -22.4667,
            "longitude": -68.9333
          },
          "geoRadius": "25000"
        }
      ],
      "serviceArea": {
        "@type": "GeoCircle",
        "geoMidpoint": {
          "@type": "GeoCoordinates",
          "latitude": -22.4667,
          "longitude": -68.9333
        },
        "geoRadius": "25000"
      },
      "openingHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday"
          ],
          "opens": "08:00",
          "closes": "21:00"
        },
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": [
            "Saturday",
            "Sunday"
          ],
          "opens": "09:00",
          "closes": "20:00"
        }
      ],
      "specialOpeningHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "opens": "00:00",
          "closes": "00:00",
          "validFrom": "2026-09-18",
          "validThrough": "2026-09-19"
        }
      ],
      "availableLanguage": [
        {
          "@type": "Language",
          "name": "Spanish",
          "alternateName": "es"
        }
      ],
      "medicalSpecialty": "Nursing",
      "isAcceptingNewPatients": true,
      "knowsAbout": [
        "Inyección intramuscular",
        "Anticonceptivos inyectables",
        "Vitaminas B1 B6 B12",
        "Control de signos vitales",
        "Curación de heridas",
        "Enfermería a domicilio"
      ],
      "employee": {
        "@id": "https://www.ejemplo-enfermeria.cl/#enfermera-jefa"
      },
      "contactPoint": [
        {
          "@type": "ContactPoint",
          "contactType": "customer service",
          "telephone": "+56912345678",
          "email": "contacto@ejemplo-enfermeria.cl",
          "availableLanguage": "es",
          "areaServed": "CL"
        }
      ],
      "hasOfferCatalog": {
        "@id": "https://www.ejemplo-enfermeria.cl/#catalogo"
      },
      "makesOffer": [
        {
          "@type": "Offer",
          "itemOffered": {
            "@id": "https://www.ejemplo-enfermeria.cl/servicios/inyeccion-multivitaminicos/#service"
          },
          "priceCurrency": "CLP",
          "price": "12000",
          "availability": "https://schema.org/InStock",
          "areaServed": {
            "@type": "City",
            "name": "Calama"
          }
        }
      ],
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "4.9",
        "reviewCount": "37",
        "bestRating": "5",
        "worstRating": "1"
      },
      "review": [
        {
          "@type": "Review",
          "author": {
            "@type": "Person",
            "name": "Carolina M."
          },
          "datePublished": "2026-08-14",
          "reviewRating": {
            "@type": "Rating",
            "ratingValue": "5",
            "bestRating": "5",
            "worstRating": "1"
          },
          "reviewBody": "Llegaron puntualmente a mi domicilio en Calama y la inyección fue rápida e indolora."
        }
      ],
      "potentialAction": [
        {
          "@type": "ReserveAction",
          "name": "Agendar visita a domicilio",
          "target": {
            "@type": "EntryPoint",
            "urlTemplate": "https://www.ejemplo-enfermeria.cl/agendar/",
            "actionPlatform": [
              "https://schema.org/DesktopWebPlatform",
              "https://schema.org/MobileWebPlatform"
            ]
          },
          "result": {
            "@type": "Reservation",
            "name": "Visita de enfermería a domicilio"
          }
        }
      ]
    },
    {
      "@type": "Person",
      "@id": "https://www.ejemplo-enfermeria.cl/#enfermera-jefa",
      "name": "Nombre Apellido",
      "jobTitle": "Técnico en Enfermería de Nivel Superior",
      "worksFor": {
        "@id": "https://www.ejemplo-enfermeria.cl/#business"
      },
      "url": "https://www.ejemplo-enfermeria.cl/equipo/nombre-apellido/",
      "image": "https://www.ejemplo-enfermeria.cl/img/equipo/nombre-apellido.jpg",
      "knowsLanguage": "es",
      "hasCredential": [
        {
          "@type": "EducationalOccupationalCredential",
          "credentialCategory": "degree",
          "name": "Técnico de Nivel Superior en Enfermería",
          "recognizedBy": {
            "@type": "CollegeOrUniversity",
            "name": "Instituto Profesional Ejemplo"
          }
        },
        {
          "@type": "EducationalOccupationalCredential",
          "credentialCategory": "license",
          "name": "Registro Nacional de Prestadores Individuales de Salud",
          "identifier": "RNPI-000000",
          "recognizedBy": {
            "@type": "GovernmentOrganization",
            "name": "Superintendencia de Salud de Chile",
            "url": "https://www.superdesalud.gob.cl/"
          }
        }
      ]
    },
    {
      "@type": "OfferCatalog",
      "@id": "https://www.ejemplo-enfermeria.cl/#catalogo",
      "name": "Servicios de enfermería a domicilio en Calama",
      "itemListElement": [
        {
          "@type": "Offer",
          "position": 1,
          "priceCurrency": "CLP",
          "price": "12000",
          "availability": "https://schema.org/InStock",
          "url": "https://www.ejemplo-enfermeria.cl/servicios/inyeccion-multivitaminicos/",
          "itemOffered": {
            "@id": "https://www.ejemplo-enfermeria.cl/servicios/inyeccion-multivitaminicos/#service"
          }
        },
        {
          "@type": "Offer",
          "position": 2,
          "priceCurrency": "CLP",
          "price": "12000",
          "availability": "https://schema.org/InStock",
          "url": "https://www.ejemplo-enfermeria.cl/servicios/inyeccion-anticonceptiva/",
          "itemOffered": {
            "@id": "https://www.ejemplo-enfermeria.cl/servicios/inyeccion-anticonceptiva/#service"
          }
        },
        {
          "@type": "Offer",
          "position": 3,
          "priceCurrency": "CLP",
          "price": "10000",
          "availability": "https://schema.org/InStock",
          "url": "https://www.ejemplo-enfermeria.cl/servicios/control-signos-vitales/",
          "itemOffered": {
            "@id": "https://www.ejemplo-enfermeria.cl/servicios/control-signos-vitales/#service"
          }
        }
      ]
    },
    {
      "@type": "Service",
      "@id": "https://www.ejemplo-enfermeria.cl/servicios/inyeccion-multivitaminicos/#service",
      "name": "Inyección de multivitamínicos (Neurobionta B1 B6 B12) a domicilio",
      "serviceType": "Administración de inyección intramuscular de complejo vitamínico B",
      "description": "Administración a domicilio de complejo vitamínico B1, B6 y B12 por técnico en enfermería titulado. Requiere prescripción médica vigente. No incluye la venta del medicamento.",
      "url": "https://www.ejemplo-enfermeria.cl/servicios/inyeccion-multivitaminicos/",
      "image": "https://www.ejemplo-enfermeria.cl/img/servicios/multivitaminicos.jpg",
      "provider": {
        "@id": "https://www.ejemplo-enfermeria.cl/#business"
      },
      "areaServed": {
        "@type": "City",
        "name": "Calama",
        "sameAs": "https://www.wikidata.org/wiki/Q233264"
      },
      "audience": {
        "@type": "PeopleAudience",
        "suggestedMinAge": 18
      },
      "termsOfService": "https://www.ejemplo-enfermeria.cl/condiciones/",
      "offers": {
        "@type": "Offer",
        "priceCurrency": "CLP",
        "price": "12000",
        "availability": "https://schema.org/InStock",
        "validFrom": "2026-01-01",
        "url": "https://www.ejemplo-enfermeria.cl/servicios/inyeccion-multivitaminicos/",
        "eligibleRegion": {
          "@type": "City",
          "name": "Calama"
        }
      }
    },
    {
      "@type": "Service",
      "@id": "https://www.ejemplo-enfermeria.cl/servicios/inyeccion-anticonceptiva/#service",
      "name": "Inyección anticonceptiva mensual y trimestral a domicilio",
      "serviceType": "Administración de anticonceptivo hormonal inyectable",
      "description": "Aplicación a domicilio de anticonceptivos inyectables mensuales o trimestrales por personal de enfermería titulado. Requiere prescripción médica vigente. No incluye la venta del medicamento.",
      "url": "https://www.ejemplo-enfermeria.cl/servicios/inyeccion-anticonceptiva/",
      "image": "https://www.ejemplo-enfermeria.cl/img/servicios/anticonceptiva.jpg",
      "provider": {
        "@id": "https://www.ejemplo-enfermeria.cl/#business"
      },
      "areaServed": {
        "@type": "City",
        "name": "Calama"
      },
      "audience": {
        "@type": "PeopleAudience",
        "suggestedGender": "https://schema.org/Female",
        "suggestedMinAge": 18
      },
      "offers": {
        "@type": "Offer",
        "priceCurrency": "CLP",
        "price": "12000",
        "availability": "https://schema.org/InStock",
        "url": "https://www.ejemplo-enfermeria.cl/servicios/inyeccion-anticonceptiva/"
      }
    },
    {
      "@type": "Service",
      "@id": "https://www.ejemplo-enfermeria.cl/servicios/control-signos-vitales/#service",
      "name": "Control de signos vitales a domicilio",
      "serviceType": "Control de presión arterial, frecuencia cardíaca, frecuencia respiratoria, temperatura y glicemia",
      "description": "Medición y registro a domicilio de presión arterial, frecuencia cardíaca, frecuencia respiratoria, temperatura y glicemia capilar, con informe escrito para su médico tratante.",
      "url": "https://www.ejemplo-enfermeria.cl/servicios/control-signos-vitales/",
      "image": "https://www.ejemplo-enfermeria.cl/img/servicios/signos-vitales.jpg",
      "provider": {
        "@id": "https://www.ejemplo-enfermeria.cl/#business"
      },
      "areaServed": {
        "@type": "City",
        "name": "Calama"
      },
      "offers": {
        "@type": "Offer",
        "priceCurrency": "CLP",
        "price": "10000",
        "availability": "https://schema.org/InStock",
        "url": "https://www.ejemplo-enfermeria.cl/servicios/control-signos-vitales/"
      }
    },
    {
      "@type": "WebSite",
      "@id": "https://www.ejemplo-enfermeria.cl/#website",
      "url": "https://www.ejemplo-enfermeria.cl/",
      "name": "Enfermería a Domicilio Calama",
      "inLanguage": "es-CL",
      "publisher": {
        "@id": "https://www.ejemplo-enfermeria.cl/#business"
      }
    },
    {
      "@type": "WebPage",
      "@id": "https://www.ejemplo-enfermeria.cl/#webpage",
      "url": "https://www.ejemplo-enfermeria.cl/",
      "name": "Enfermería e inyecciones a domicilio en Calama",
      "description": "Inyecciones intramusculares, anticonceptivos inyectables, multivitamínicos y control de signos vitales a domicilio en Calama.",
      "inLanguage": "es-CL",
      "isPartOf": {
        "@id": "https://www.ejemplo-enfermeria.cl/#website"
      },
      "about": {
        "@id": "https://www.ejemplo-enfermeria.cl/#business"
      },
      "primaryImageOfPage": {
        "@id": "https://www.ejemplo-enfermeria.cl/#logo"
      },
      "datePublished": "2026-09-05",
      "dateModified": "2026-09-05",
      "breadcrumb": {
        "@id": "https://www.ejemplo-enfermeria.cl/#breadcrumb"
      }
    },
    {
      "@type": "BreadcrumbList",
      "@id": "https://www.ejemplo-enfermeria.cl/#breadcrumb",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "name": "Inicio",
          "item": "https://www.ejemplo-enfermeria.cl/"
        },
        {
          "@type": "ListItem",
          "position": 2,
          "name": "Servicios",
          "item": "https://www.ejemplo-enfermeria.cl/servicios/"
        }
      ]
    }
  ]
}
</script>
```

### Notas de implementación

1. **Un solo `@graph` por página.** No repartir nodos en varios `<script>`; el grafo enlazado por `@id` es lo que permite a Google reconciliar la entidad.
2. **`@id` con fragmento** (`#business`, `#service`, `#webpage`). Es lo que el competidor no hace y lo que hace el grafo reutilizable entre páginas.
3. **Páginas de servicio individuales.** Cada `Service` del catálogo debe tener su propia URL con contenido real. En la página hija se repite ese nodo `Service` como principal, con `provider` apuntando por `@id` al negocio. Sin página real detrás, el nodo es hojarasca.
4. **Coherencia NAP absoluta** entre JSON-LD, texto visible, pie de página y Google Business Profile. Cualquier divergencia degrada la confianza.
5. **Precios:** los precios en `Offer` de servicios no generan rich result, pero alimentan respuestas de IA. Solo incluirlos si son reales y están publicados en la página.
6. **Todo lo marcado debe ser visible.** Horarios, servicios, precios y reseñas del JSON-LD deben aparecer en el HTML de cara al usuario.
7. **Prescripción médica:** el descargo de que se exige receta y de que no se venden medicamentos está en `description` y en cada `Service`. En un rubro YMYL esta transparencia es señal de confianza.
8. **Validar antes de desplegar** con Google Rich Results Test y Schema Markup Validator.

---

## 7. Hallazgos estructurados (para `audit-data.json`)

```json
{
  "category": "Schema / Structured Data",
  "url": "https://draska.ueniweb.com/",
  "audited_at": "2026-09-05",
  "detection": {
    "json_ld_blocks": 1,
    "microdata_blocks": 0,
    "rdfa_blocks": 0,
    "total_bytes": 539,
    "types": ["LocalBusiness", "PostalAddress", "GeoCoordinates"],
    "server_rendered": true,
    "is_spa": false
  },
  "validation": {
    "syntactically_valid": true,
    "error_count": 3,
    "warning_count": 17,
    "pass_count": 9
  },
  "findings": [
    {"id": "SCH-01", "severity": "critical", "property": "address.addressCountry", "issue": "Valor 'CHILE' no es ISO 3166-1 alpha-2", "fix": "Usar 'CL'"},
    {"id": "SCH-02", "severity": "critical", "property": "address.postalCode", "issue": "'139000' invalido; el codigo chileno es de 7 digitos", "fix": "Usar '1390000'"},
    {"id": "SCH-03", "severity": "critical", "property": "sameAs", "issue": "Google Place ID crudo 'ChIJFfyXTPEJrJYRzcBJnjIC7wA' donde se requiere URL absoluta", "fix": "https://www.google.com/maps/place/?q=place_id:ChIJFfyXTPEJrJYRzcBJnjIC7wA"},
    {"id": "SCH-04", "severity": "high", "property": "@type", "issue": "LocalBusiness generico para un prestador de salud", "fix": "MedicalBusiness + additionalType Nursing + medicalSpecialty"},
    {"id": "SCH-05", "severity": "critical", "property": "areaServed", "issue": "Ausente en un negocio de area de servicio", "fix": "City + AdministrativeArea + GeoCircle"},
    {"id": "SCH-06", "severity": "critical", "property": "openingHoursSpecification", "issue": "Ausente", "fix": "Anadir horarios por dia y festivos"},
    {"id": "SCH-07", "severity": "critical", "property": "hasOfferCatalog", "issue": "Tres servicios sin modelar como entidades", "fix": "OfferCatalog + nodos Service con Offer"},
    {"id": "SCH-08", "severity": "critical", "property": "image", "issue": "Ausente; requerida para elegibilidad plena de LocalBusiness", "fix": "Anadir 1x1, 4x3 y 16x9"},
    {"id": "SCH-09", "severity": "high", "property": "description", "issue": "Ausente", "fix": "Anadir descripcion de entidad"},
    {"id": "SCH-10", "severity": "high", "property": "hasCredential", "issue": "Inscripcion en Superintendencia de Salud solo en texto, no marcada", "fix": "Person + EducationalOccupationalCredential"},
    {"id": "SCH-11", "severity": "medium", "property": "address.streetAddress", "issue": "'Punta Arenas' sin numeracion y ambiguo con la ciudad homonima", "fix": "Anadir numero o omitir si es SAB"},
    {"id": "SCH-12", "severity": "medium", "property": "BreadcrumbList/WebSite/WebPage", "issue": "Ausentes", "fix": "Anadir grafo de sitio"},
    {"id": "SCH-13", "severity": "low", "property": "@id", "issue": "@id sin fragmento, identico a url", "fix": "Usar '#business' para permitir @graph"}
  ],
  "deprecated_types_recommended": [],
  "notes": [
    "FAQPage: sin rich result desde 2026-05-07. Prioridad Info; beneficio AI/GEO no confirmado.",
    "HowTo: no recomendar, rich results eliminados en 2023-09.",
    "Resenas autorreferenciales en LocalBusiness/MedicalBusiness son ignoradas por Google; no generan estrellas."
  ]
}
```

---

## 8. Plan de acción para el sitio nuevo

1. Implementar el `@graph` de la sección 6 en la home, server-rendered, con datos reales.
2. Crear las 3 páginas de servicio y replicar en cada una su nodo `Service` como entidad principal.
3. Reclamar y completar Google Business Profile; obtener el Place ID real y enlazarlo en `hasMap` y `sameAs`.
4. Publicar la credencial de la Superintendencia de Salud de forma visible y marcarla con `hasCredential`.
5. Publicar horarios y cobertura geográfica visibles, en paridad con el JSON-LD.
6. Validar con Rich Results Test y Schema Markup Validator antes del despliegue.
7. Considerar `QAPage` (no `FAQPage`) si se publican preguntas reales de pacientes.

---

## 9. Resumen ejecutivo

El competidor publica un único bloque JSON-LD de 539 bytes, server-rendered: un `LocalBusiness` genérico de 10 propiedades, generado por defecto por la plataforma UENI. Es sintácticamente válido, pero acumula 3 errores y 17 propiedades recomendadas ausentes. Los errores: `addressCountry` "CHILE" en vez de "CL", `postalCode` "139000" (falta un dígito; Calama es 1390000) y un Google Place ID crudo dentro de `sameAs`, que exige URLs absolutas — tiene ficha de Maps y desperdicia el enlace.

Las brechas críticas son estratégicas, no cosméticas: sin `areaServed` en un negocio a domicilio, sin `openingHoursSpecification`, sin `image` y sin ningún servicio modelado como entidad. Sus tres servicios existen solo como texto plano.

`LocalBusiness` no basta. `MedicalBusiness` hereda todas sus propiedades y conserva la elegibilidad del rich result, añadiendo precisión sanitaria; se refuerza con `additionalType` Nursing y `medicalSpecialty`.

La plantilla propuesta pasa de 1 a 9 nodos en un `@graph` enlazado por `@id`, con `OfferCatalog` más tres `Service`, cobertura geográfica, horarios y `hasCredential` de la Superintendencia de Salud — la mayor palanca de E-E-A-T del rubro. Valida con 0 errores.

`FAQPage` se descarta: sin rich results desde mayo de 2026.
