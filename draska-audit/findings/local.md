# Auditoría SEO Local — draska.ueniweb.com

**URL:** https://draska.ueniweb.com/
**Fecha del análisis:** 2026-09-05
**Propósito:** investigación competitiva / de referencia para replicar tácticas en un sitio nuevo del mismo rubro (inyecciones y enfermería a domicilio, Calama, Chile). No es un plan de corrección de este sitio.
**Método:** render con Playwright (`render_page.py --mode always`), extracción de JSON-LD, del payload interno `window.__PRELOAD_DATA__` de UENI, `robots.txt`, `sitemap.xml`, páginas de servicio y `/reviews`, verificación de tipos en schema.org.

---

## 1. Score SEO Local: 34/100

| Dimensión | Peso | Score | Aporte | Justificación breve |
|---|---|---|---|---|
| Señales GBP | 25% | 35/100 | 8.75 | Perfil vinculado pero `is_verified: false` / `VERIFICATION_PENDING`; sin horarios; sin embed de mapa; sin posts ni evidencia de fotos |
| Reviews y reputación | 20% | 30/100 | 6.00 | 4.9★ con 8 reviews, pero última reseña 2024-05-09 (~28 meses); 0% de respuestas; 6/8 sin texto |
| SEO local on-page | 20% | 45/100 | 9.00 | Ciudad en title/H1/H2/meta y "Áreas cubiertas", pero one-pager con páginas de servicio vacías y meta duplicada |
| NAP y citaciones | 15% | 30/100 | 4.50 | Dos nombres de negocio en conflicto, código postal inválido, dirección sin número, 1 sola citación verificable |
| Schema local | 10% | 40/100 | 4.00 | `LocalBusiness` genérico, `sameAs` malformado, sin `areaServed`, horarios ni catálogo de servicios |
| Enlaces y autoridad local | 10% | 20/100 | 2.00 | Subdominio de `ueniweb.com`, sin dominio propio, sin backlinks locales, referencia saliente a dominio muerto |
| **Total** | **100%** | | **34.25 → 34/100** | |

**Tipo de negocio detectado:** SAB (Service-Area Business) con **fuga de señales de híbrido**. `areas_covered: "Calama"`, copy "a domicilio", pero publica calle sin número ("Punta Arenas"), código postal y un enlace `maps.google.com/?q=Punta Arenas, Calama, 139000`.

**Vertical detectado:** Salud / enfermería domiciliaria (YMYL). Señales: "técnicos en enfermería de nivel superior", "inscritos en la superintendencia de salud", "prestadores individuales de la salud", "prescripción médica", nombres de fármacos (Neurobionta, anticonceptivo inyectable), precios por procedimiento.

> Recordatorio del estudio de Search Atlas: ~55.2% de la varianza del ranking en el local pack se explica por proximidad al usuario, algo fuera de control de cualquier optimización. Todo lo de abajo actúa sobre el ~45% restante.

---

## 2. Datos duros extraídos (no visibles a simple vista)

El sitio es un UENI y filtra en el HTML un objeto `window.__PRELOAD_DATA__` con el estado real del negocio. Hallazgos:

| Campo | Valor |
|---|---|
| GBP `gmb_id` | `15785350868928182190` |
| `place_id` | `ChIJFfyXTPEJrJYRzcBJnjIC7wA` |
| CID | `67274935861100749` → `https://maps.google.com/?cid=67274935861100749` |
| `account_id` GBP | `100238524862445600752` |
| **`is_verified`** | **`false`** |
| **`status`** | **`VERIFICATION_PENDING`** |
| `build_by_ueni` / `by_ueni` | `true` (perfil creado por el proveedor del sitio, no por el dueño) |
| `is_connected` / `edit_allowed` | `true` / `true` |
| `is_duplicate` | `false` |
| Última sincronización GBP | `2024-05-09` (Places API: `2024-05-03`) |
| Rating GMB | 4.9 con 8 reseñas |
| Rating snapshot Places | 4.8 con 5 reseñas (snapshot más antiguo) |
| `opening_hours` | `[]` (vacío) |
| `areas_covered` | `"Calama"` |
| `employees_count` | `2-3` |
| Owner (impressum) | Hedra Corante |
| Email registrado | `hectoremprendimiento9@gmail.com` |
| Servicios y precios | Inyección anticonceptiva $10.000 · Inyección Neurobionta $12.000 (c/3) · Inyección medicamento $10.000 (CLP) |
| Pagos | Efectivo / transferencia |

**Lección táctica #0:** los constructores tipo UENI/Wix/GoDaddy exponen el estado real del GBP del competidor en el HTML. Es la vía más barata de inteligencia competitiva local: `place_id`, CID, conteo de reseñas, estado de verificación y horarios sin usar la API de Places.

---

## 3. Naming de GBP — el hallazgo central

### Qué están haciendo

| Fuente | Nombre |
|---|---|
| JSON-LD `name` | INYECCIÓN A DOMICILIO CALAMA |
| `og:site_name` | INYECCIÓN A DOMICILIO CALAMA |
| H1 | INYECCIÓN A DOMICILIO CALAMA |
| Impressum `registered_name` | INYECCIÓN A DOMICILIO CALAMA |
| `<title>` / meta / marca real | **Draska** - Enfermería a domicilio \| Calama |
| Slug del dominio | `draska` |
| Facebook | Inyecciones a domicilio |
| GBP | No verificable sin API (probablemente "INYECCIÓN A DOMICILIO CALAMA") |

Es un patrón **EMD-name**: keyword exacta de alto intent (`inyección a domicilio`) + ciudad (`Calama`), sin marca. La marca real (Draska) queda relegada al title tag.

### Evaluación

**Por qué funciona:** la coincidencia keyword-en-el-nombre sigue siendo de las señales de relevancia más correlacionadas del local pack, y en un mercado pequeño como Calama (competencia mínima, pocas fichas del rubro) basta para copar el pack de "inyecciones a domicilio calama". El nombre además rellena por sí solo el anchor de todas las citaciones.

**Por qué es frágil:**
1. Viola las directrices de representación de GBP (el nombre debe ser el del mundo real; ciudad y servicio genérico no van en el nombre).
2. Es editable por cualquier tercero vía "Sugerir un cambio"; un competidor puede normalizar el nombre a "Draska" y borrar de un golpe toda la relevancia construida.
3. **Agravante crítico:** la ficha figura como **no verificada** (`VERIFICATION_PENDING`). Un nombre keyword-stuffed en una ficha no verificada es el perfil de riesgo más alto para suspensión o edición automática; también bloquea posts, mensajes y edición fina del área de servicio.
4. Genera inconsistencia NAP estructural: dos nombres distintos conviviendo en el mismo sitio impiden construir citaciones coherentes en cualquier directorio.

### Qué replicar en el sitio nuevo (versión defendible)

- Nombre GBP = **marca + descriptor real usado en la señalética/uniforme/publicidad**, sin ciudad. Ej.: `Draska Enfermería a Domicilio`. Google permite el descriptor si es parte del branding real (fotos del uniforme, tarjetas y flyers sirven como evidencia si te piden reverificación).
- La ciudad se captura por otras vías, no por el nombre: área de servicio del GBP, categoría, servicios listados en la ficha, texto de las reseñas, páginas de servicio por sector y el title tag.
- Título en el sitio sí puede ser agresivo (`Inyecciones a Domicilio en Calama | Draska`): el title tag no está sujeto a las directrices de GBP.
- Ese naming honesto pierde ~un escalón de relevancia inicial pero es el único que sobrevive a una verificación por video, que es hoy el cuello de botella real para SAB de salud.

---

## 4. Categorías de GBP probables y recomendadas

No es posible leer la categoría real sin Places API / DataForSEO (ver limitaciones). Inferencia por contenido, servicios y taxonomía interna UENI (`standard_cat: 01200_00200_00700` para las inyecciones):

**Probable actual (una sola, elegida por UENI al crear la ficha):** "Servicio de atención médica a domicilio" (*Home health care service*) o, menos probable, "Enfermero/a" o "Centro médico".

**Recomendado para el sitio nuevo:**

| Rol | Categoría | Razón |
|---|---|---|
| **Primaria** | Servicio de atención médica a domicilio (*Home health care service*) | Es la única categoría del set de salud que Google trata como servicio a domicilio nativo; habilita bien el área de servicio sin dirección visible |
| Alternativa primaria | Enfermero/a (*Nurse*) / Enfermero/a especializado/a | Úsala solo si el prestador es persona natural inscrita, y si el volumen de búsqueda local de "enfermera a domicilio" supera al de "inyecciones" |
| Secundaria | Centro de vacunación / Servicio de vacunación | Captura la intención de inyectables y vacunas |
| Secundaria | Agencia de enfermería | Refuerzo semántico |
| **Evitar** | Centro médico, Clínica, Consultorio | Implican establecimiento con público; contradicen el modelo SAB y son la vía rápida a suspensión por dirección no elegible |

La categoría primaria es el factor de ranking local #1 y la categoría equivocada es el factor negativo #1: la decisión de una sola línea que más mueve la aguja. Antes de fijarla, revisar con qué categoría rankean las 3 fichas del top del pack en Calama y espejarla.

---

## 5. Señales de área de servicio (SAB)

**Lo que hacen bien:**
- Bloque explícito "Áreas cubiertas: Calama" (H2 dedicado, renderizado en el HTML servidor).
- Ciudad repetida en H1, H2, title, meta description, nombre y `addressLocality`.
- `og:locale: es_CL`, `<html lang="es">`, `time_zone: America/Santiago`, `currency_code: CLP`.
- CTAs de conversión SAB correctas: `tel:` y `wa.me/56978833741` en header persistente (WhatsApp es el canal dominante en Chile).

**Lo que hacen mal (y hay que invertir en el sitio nuevo):**

1. **Dirección parcial publicada.** Muestran "Punta Arenas, Calama, 139000" (calle sin número) y un enlace a Google Maps con esa cadena. Para un SAB sin local de atención al público, publicar una dirección residencial parcial es incoherente y, si coincide con la dirección oculta del GBP, es causal de suspensión. Un SAB no debe mostrar dirección: debe mostrar área de servicio.
2. **Código postal inválido:** `139000` (6 dígitos). Chile usa 7 dígitos; el de Calama es `1390000`. Está propagado a JSON-LD, impressum y al enlace de mapa. Un dato NAP incorrecto replicado en todas las fuentes.
3. **Área de servicio de un solo token.** "Calama" y nada más. Sin comunas/sectores vecinos, sin barrios, sin radio, sin Chuquicamata ni localidades del Loa. La cobertura granular es lo que permite rankear en consultas de barrio y alimenta a los LLM con contexto geográfico.
4. **Sin horarios en absoluto** (`opening_hours: []`). Para un servicio que compite en urgencia ("¿quién me inyecta hoy?"), no declarar horarios pierde el filtro "Abierto ahora" y la ventaja de la inmediatez.
5. **Sin embed de mapa**, sin enlace por CID a la ficha, sin `hasMap`. No hay ningún puente sitio→GBP salvo el botón "Añadir opinión".

**Pila de señales SAB a replicar:** `areaServed` en schema con `City` + `GeoCircle` con radio real · página madre "Cobertura" con lista de sectores enlazada desde el footer · horarios declarados en sitio y GBP · frase de proximidad ("llegamos a tu domicilio en Calama en X minutos") · área de servicio del GBP limitada a lo que realmente se cubre (no inflarla: diluye la relevancia por punto).

---

## 6. Reviews — el punto más débil y la mayor oportunidad

**Estado:** 4.9★ / 8 reseñas (GMB). La página `/reviews` publica solo 6 (Google filtra las dos más antiguas).

**Cronología completa:**

| Fecha | ★ | Autor | Texto | Respuesta |
|---|---|---|---|---|
| 2020-10-24 | 5 | hector huidobro | — | No |
| 2021-05-07 | 5 | Hedra Corante | — | No |
| 2023-10-13 | 4 | Raúl Mendizábal Castillo | — | No |
| 2024-04-28 | 5 | Yamile Gomez | "Excelente servicio" | No |
| 2024-05-01 | 5 | EDNA BONILLA | "Exelente servicio" | No |
| 2024-05-06 | 5 | Luis Gonzalo Barrios Ortiz | — | No |
| 2024-05-09 | 5 | Enzo jofre | — | No |
| 2024-05-09 | 5 | Alejandro Jesús Ortiz Peña | — | No |

**Diagnóstico:**

1. **Velocidad muerta.** Última reseña hace ~28 meses (≈850 días). Contra la regla de los 18 días de Sterling Sky (el ranking se despeña si pasan ~3 semanas sin reseñas nuevas), este perfil lleva ~47 ciclos sin señal. Es, de lejos, la mayor debilidad explotable del competidor.
2. **Patrón de ráfaga.** 5 reseñas en 11 días (28-abr a 9-may 2024) tras 6 meses de silencio, y luego nada. Es la firma clásica de una campaña puntual de solicitud; los filtros anti-spam de Google la detectan y suele venir seguida de purgas (de hecho el snapshot de Places registraba solo 5 de las 8).
3. **0% de tasa de respuesta.** Ninguna de las 8 respondida. Se pierde texto adicional indexable con keywords y ciudad, y la señal de negocio activo.
4. **6 de 8 sin texto.** Rating puro no aporta relevancia semántica. Las dos con texto dicen "Excelente servicio" (una con falta de ortografía) — cero keywords de servicio, cero mención de Calama, cero mención de "inyección", "enfermera" o "domicilio".
5. **Dos reseñas del propio círculo.** El autor de la reseña de 2020 y la dueña registrada en el impressum (Hedra Corante, 2021) figuran como reseñadores. Son autoreseñas: violación explícita de políticas y motivo probable de que Google las filtre de la vista pública.
6. **Reseñas exclusivamente de Google.** Cero en Facebook, Doctoralia u otras plataformas; sin diversidad de fuentes, que es lo que hoy alimenta la visibilidad en respuestas de IA.

**A replicar (bien hecho):** el único acierto es el enlace directo `search.google.com/local/writereview?placeid=…` embebido en el sitio y un H2 "Opiniones". Copiar eso, pero conectado a un flujo real: pedir reseña por WhatsApp 30-60 min después de cada atención, con guion que sugiera mencionar servicio + sector ("me pusieron la Neurobionta en Villa Ayquina"), cadencia sostenida de 2-4 reseñas/mes en vez de ráfagas, y respuesta a todas dentro de 24-48 h sin confirmar jamás datos clínicos del paciente.

---

## 7. Auditoría de consistencia NAP

| Elemento | JSON-LD | HTML visible | Impressum | Meta / title | Facebook | Veredicto |
|---|---|---|---|---|---|---|
| **Name** | INYECCIÓN A DOMICILIO CALAMA | INYECCIÓN A DOMICILIO CALAMA (H1) | INYECCIÓN A DOMICILIO CALAMA | Draska - Enfermería a domicilio \| Calama | Inyecciones a domicilio | ❌ **3 nombres distintos** |
| **Address** | Punta Arenas, Calama, 139000, CHILE | Punta Arenas, Calama, 139000 | Punta Arenas Calama 139000 | — | n/d | ⚠️ Consistente entre sí pero **inválida**: sin número + CP de 6 dígitos + `addressCountry: "CHILE"` (debe ser ISO `CL`) |
| **Phone** | +56978833741 | tel:+56 9 7883 3741 / wa.me/56978833741 | +56978833741 | — | n/d | ✅ Consistente (el `tel:` con espacios no es E.164 estricto, defecto menor) |
| **Geo** | -22.4703921 / -68.9293679 | — | — | — | — | ⚠️ 7 decimales (la recomendación es 5); coherente con Calama |
| **Email** | — | — | hectoremprendimiento9@gmail.com | — | — | ⚠️ Gmail genérico, sin correo de dominio: debilita E-E-A-T en un vertical YMYL |

**Citaciones detectadas (Tier 1 adaptado a Chile):**

| Fuente | Estado |
|---|---|
| Google Business Profile | Presente pero **no verificado** |
| Facebook | Presente (`/Inyecciones-a-domicilio-106866317602750`, responde 200; contenido tras muro de login, no verificable) |
| Instagram | Ausente |
| Doctoralia / Superintendencia de Salud (registro de prestadores individuales) | No detectada, pese a que el copy afirma inscripción en la Superintendencia — **credencial reclamada pero no enlazada ni verificable** |
| Amarillas Chile, Yapo, Bing Places, Apple Maps, Waze | No detectadas |
| Yelp / BBB | Irrelevantes en el mercado chileno |

**Bandera roja adicional:** el copy remite a `www.sanivida.cl` como fuente de "más información". El dominio **no resuelve DNS** (NXDOMAIN): enlace saliente muerto hacia lo que probablemente fue una propiedad hermana. Referencia rota en un contexto YMYL.

---

## 8. Validación de schema local

JSON-LD actual (bloque único, válido sintácticamente):

```json
{"@context":"https://schema.org","@type":"LocalBusiness","@id":"https://draska.ueniweb.com",
 "name":"INYECCIÓN A DOMICILIO CALAMA",
 "address":{"@type":"PostalAddress","streetAddress":"Punta Arenas","addressLocality":"Calama","postalCode":"139000","addressCountry":"CHILE"},
 "geo":{"@type":"GeoCoordinates","latitude":-22.4703921,"longitude":-68.9293679},
 "url":"https://draska.ueniweb.com","telephone":"+56978833741","priceRange":"$",
 "sameAs":["https://www.facebook.com/Inyecciones-a-domicilio-106866317602750","ChIJFfyXTPEJrJYRzcBJnjIC7wA"]}
```

| Propiedad | Estado | Nota |
|---|---|---|
| `@type` | ⚠️ Genérico | `LocalBusiness` en un negocio sanitario: se pierde toda la desambiguación de entidad |
| `name`, `address`, `telephone`, `url`, `@id`, `geo` | ✅ Presentes | `@id` sin barra final vs canónica con barra: inconsistencia trivial |
| `addressCountry` | ❌ | `"CHILE"` debe ser `"CL"` (ISO 3166-1 alpha-2) |
| `postalCode` | ❌ | `139000` inválido; Calama = `1390000` |
| `geo` precisión | ⚠️ | 7 decimales; la recomendación es 5 |
| **`sameAs[1]`** | ❌ | `"ChIJFfyXTPEJrJYRzcBJnjIC7wA"` es un Place ID crudo, **no una URL**: `sameAs` exige URL. Rompe la validación estricta y no vincula nada |
| `areaServed` / `serviceArea` | ❌ Ausente | Omisión más grave para un SAB |
| `openingHoursSpecification` | ❌ Ausente | |
| `hasOfferCatalog` / `makesOffer` | ❌ Ausente | Tienen 3 servicios con precio en CLP y no los marcan |
| `image` / `logo` | ❌ Ausente | 9 imágenes en el sitio, ninguna en el schema |
| `aggregateRating` / `review` | ❌ Ausente | Ver matiz abajo |
| `hasMap`, `paymentAccepted`, `currenciesAccepted`, `knowsLanguage` | ❌ Ausentes | |
| Schema en páginas de servicio | ❌ Ausente | Las URLs `/services/...` no llevan ningún JSON-LD |
| BreadcrumbList | ⚠️ | El widget `BreadcrumbListSchema` existe en el CMS pero no emite bloque en el home |

### `LocalBusiness` vs `MedicalBusiness` vs `HomeHealthCareService` — recomendación

**Verificado contra schema.org (2026-09-05):**
- `https://schema.org/MedicalBusiness` → **200, existe.** Jerarquía: `Thing > Place > LocalBusiness > MedicalBusiness`. Uso: 100K-1M dominios.
- `https://schema.org/Nursing` → **200, existe.** Es simultáneamente subtipo de `MedicalBusiness` y miembro de la enumeración `MedicalSpecialty`. Uso: <1K dominios (raro pero legítimo).
- `https://schema.org/HomeHealthCareService` → **404. NO existe en schema.org.** "Home health care service" es una **categoría de Google Business Profile**, no un tipo de schema. Es una confusión frecuente: úsala en el GBP, nunca como `@type`.

**Recomendación para el sitio nuevo:** tipado múltiple `["MedicalBusiness","Nursing"]`, que es válido y hereda todas las propiedades de `LocalBusiness`. Evitar `MedicalClinic` / `Hospital` (implican establecimiento físico; contradicen el modelo SAB) y evitar `Physician` (el prestador es técnico/enfermero, no médico: sobredeclarar credenciales en YMYL es contraproducente).

```json
{
  "@context": "https://schema.org",
  "@type": ["MedicalBusiness", "Nursing"],
  "@id": "https://tudominio.cl/#business",
  "name": "Draska Enfermería a Domicilio",
  "url": "https://tudominio.cl/",
  "telephone": "+56900000000",
  "medicalSpecialty": "Nursing",
  "areaServed": [
    {"@type": "City", "name": "Calama", "containedInPlace": {"@type": "AdministrativeArea", "name": "Región de Antofagasta"}},
    {"@type": "GeoCircle", "geoMidpoint": {"@type": "GeoCoordinates", "latitude": -22.47039, "longitude": -68.92937}, "geoRadius": "15000"}
  ],
  "openingHoursSpecification": [
    {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"], "opens": "08:00", "closes": "22:00"}
  ],
  "hasOfferCatalog": {
    "@type": "OfferCatalog", "name": "Enfermería a domicilio",
    "itemListElement": [
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Inyección anticonceptiva a domicilio"}, "price": "10000", "priceCurrency": "CLP"}
    ]
  },
  "currenciesAccepted": "CLP",
  "paymentAccepted": "Efectivo, Transferencia",
  "knowsLanguage": "es-CL",
  "sameAs": ["https://www.google.com/maps?cid=TU_CID", "https://www.facebook.com/tupagina", "https://www.instagram.com/tucuenta"],
  "hasMap": "https://www.google.com/maps?cid=TU_CID"
}
```

**Notas de implementación:**
- Sin local de atención al público, **omitir `address`** o dejar solo `addressLocality`/`addressRegion`/`addressCountry: "CL"`. Nunca la calle del domicilio del prestador.
- **No añadir `aggregateRating` propio.** El marcado de reseñas autorreferido en `LocalBusiness`/`Organization` no es elegible para rich results desde 2019 y es una infracción de las directrices de spam. Las estrellas del pack salen del GBP, no del schema. Es justo la "táctica" que conviene NO copiar.
- Añadir `Service` schema propio en cada página de servicio, con `provider: {"@id": ".../#business"}` y `areaServed`.

---

## 9. Calidad de páginas de servicio / localización

Sitio de una ubicación; no aplica auditoría multi-local, pero las páginas de servicio son el punto ciego mayor **y la oportunidad más grande para el sitio nuevo**, porque las páginas de servicio dedicadas son el factor #1 de SEO local orgánico y el #2 de visibilidad en IA.

Sitemap: 17 URLs (home, 3 servicios, 3 "about-us", `/reviews`, `/services`, `/products`, `/booking`, legales, y una página huérfana **`/test`**, indexable y enlazada en el menú principal).

Auditoría de `/services/enfermeria-a-domicilio/inyeccion-anticonceptiva-26634345`:

| Criterio | Resultado |
|---|---|
| Contenido único | ❌ Prácticamente nulo: H1 + precio + botón "Reservar". Sin descripción (`description: null` en el CMS) |
| Meta description | ❌ Idéntica a la del home (duplicada en todo el sitio) |
| Ciudad en H1 / título | ❌ H1 = "INYECCIÓN ANTICONCEPTIVA", sin "Calama" ni "a domicilio" |
| Schema | ❌ Ninguno |
| Enlazado interno | ⚠️ Solo "Servicios relacionados" autogenerado |
| Prueba del intercambio (doorway) | ❌ **Falla**: intercambiando el nombre del servicio la página sería indistinguible. Son plantillas de catálogo, no páginas de servicio |

Texto total del home: ~1.800 caracteres, con partes en mayúsculas sostenidas y contenido enciclopédico genérico sobre anticonceptivos ("5 millones de mujeres... China, India") que no aporta relevancia local alguna.

**A construir en el sitio nuevo:** una página por servicio × intención (`/inyecciones-a-domicilio-calama`, `/inyeccion-anticonceptiva-calama`, `/neurobionta-a-domicilio-calama`, `/toma-de-presion-a-domicilio-calama`, `/enfermera-a-domicilio-calama`), cada una con 600-1.000 palabras únicas, precio, tiempo de respuesta, requisitos (receta médica), FAQ con `FAQPage` schema, foto propia y `Service` schema. Añadir una página de cobertura con sectores de Calama enlazada desde el footer.

---

## 10. Acciones priorizadas (para el sitio nuevo)

| # | Prioridad | Acción | Fundamento |
|---|---|---|---|
| 1 | **Crítica** | Crear y **verificar** el GBP como SAB (dirección oculta, área de servicio Calama), con nombre marca+descriptor sin ciudad | Ficha del competidor sin verificar: ventana abierta. La verificación por video es hoy el cuello de botella real |
| 2 | **Crítica** | Fijar categoría primaria "Servicio de atención médica a domicilio" tras espejar la de las 3 fichas del top del pack; secundarias: vacunación, enfermería | Categoría primaria = factor #1; categoría errónea = factor negativo #1 |
| 3 | **Crítica** | Motor de reseñas sostenido: solicitud por WhatsApp post-atención, 2-4/mes constantes, guion que induzca a mencionar servicio + sector, respuesta a todas en 24-48 h | El competidor lleva ~28 meses sin reseñas nuevas; superarlo en velocidad es el atajo más rápido al pack |
| 4 | **Alta** | Dominio propio `.cl` (no subdominio de constructor) con NAP único y consistente en todas las fuentes | El competidor tiene techo de autoridad por vivir en `ueniweb.com` |
| 5 | **Alta** | Páginas de servicio dedicadas (5-6) con contenido único, precio, FAQ y `Service` schema | Factor #1 de SEO local orgánico y #2 de visibilidad IA; el competidor tiene stubs vacíos |
| 6 | **Alta** | Schema `["MedicalBusiness","Nursing"]` con `areaServed` (City + GeoCircle), `openingHoursSpecification`, `hasOfferCatalog`, `sameAs` con URLs válidas y `hasMap` por CID. Sin `aggregateRating` propio | El competidor usa `LocalBusiness` genérico con `sameAs` roto y sin área de servicio |
| 7 | **Alta** | Declarar horarios reales (sitio + GBP), incluyendo disponibilidad de fin de semana/urgencia | El competidor tiene `opening_hours` vacío: pierde el filtro "Abierto ahora" en un rubro de urgencia |
| 8 | **Media** | Citaciones en fuentes chilenas del vertical: registro público de prestadores individuales de la Superintendencia de Salud (enlazado y verificable), Doctoralia, Amarillas, Bing Places, Apple Maps, Waze, Instagram | 3 de los 5 factores principales de visibilidad en IA son de citaciones; el competidor solo tiene Facebook |
| 9 | **Media** | E-E-A-T sanitario: nombre y número de registro del prestador, credenciales, protocolo de insumos y requisito de receta, correo con dominio propio | Vertical YMYL; el competidor reclama registro en la Superintendencia sin evidencia enlazable |
| 10 | **Baja** | Página de cobertura con sectores y villas de Calama; fotos propias geoetiquetadas y subidas al GBP con cadencia; posts semanales en GBP | Refuerzo de relevancia geográfica más allá del nombre; el competidor no publica nada desde 2024 |

---

## 11. Limitaciones

- **No se pudo leer el GBP en vivo.** `maps.google.com/?cid=67274935861100749` y `google.com/maps` requieren ejecución de JS interactiva y devuelven un shell vacío incluso con Playwright. Categoría real, horarios, fotos, posts, atributos y conteo actual de reseñas **no verificados** — todo lo relativo a la ficha proviene del payload del sitio, con última sincronización **2024-05-09** (más de 2 años de antigüedad). El estado "no verificado" podría haber cambiado desde entonces.
- **SERPs no accesibles.** DuckDuckGo (HTML y Lite) devolvió challenge anti-bot (HTTP 202) y Bing devolvió resultados irrelevantes en francés. No se pudo comprobar posiciones reales en el local pack, cuota de voz, ni presencia en directorios vía `site:`.
- **Sin herramientas de pago.** Sin DataForSEO/Places API/BrightLocal no hay: auditoría real de citaciones (NAP en N directorios), volumen de búsqueda local, grid de rankings por proximidad, ni histórico de reseñas eliminadas.
- **Facebook no verificable.** La página responde 200 pero el contenido está tras muro de login: no se pudo cotejar NAP ni actividad.
- **Backlinks no evaluados.** Sin acceso a un índice de enlaces, la dimensión de autoridad local se puntuó por proxies (subdominio de constructor, ausencia de citaciones, dominio saliente muerto).
- **Nota de contexto:** dos de las 8 reseñas provienen de personas vinculadas al negocio (la dueña registrada en el impressum y un autor cuyo nombre coincide con el patrón del correo del titular). Se reporta como observación factual de higiene de reseñas, no como acusación.

---

## 12. Resumen ejecutivo

`draska.ueniweb.com` puntúa **34/100** en SEO local. Es un SAB de enfermería a domicilio en Calama que apuesta todo a una táctica: usar la keyword exacta como nombre de negocio, "INYECCIÓN A DOMICILIO CALAMA". Funciona en un mercado con poca competencia, pero es frágil: viola las directrices de nombre de GBP, es editable por cualquier competidor y, sobre todo, la ficha figura como **no verificada** (`VERIFICATION_PENDING`), la combinación de mayor riesgo de suspensión.

La debilidad explotable es la reputación: 4.9★ con solo 8 reseñas, **la última de mayo de 2024** (~28 meses), 0% de respuestas, 6 sin texto y dos del propio círculo. Contra la regla de los 18 días, ese perfil está muerto. Sumado a ello: sin horarios, páginas de servicio vacías que fallan la prueba de doorway, código postal inválido, dos nombres de negocio en conflicto y `LocalBusiness` genérico con `sameAs` malformado.

Para el sitio nuevo: nombre marca+descriptor verificable, categoría primaria correcta, motor de reseñas sostenido, páginas de servicio reales y schema `["MedicalBusiness","Nursing"]` con `areaServed`. Ojo: `HomeHealthCareService` **no existe** en schema.org (404) — es una categoría de GBP, no un `@type`.
