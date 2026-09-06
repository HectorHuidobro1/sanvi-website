# Auditoría de Contenido y E-E-A-T — draska.ueniweb.com

**Fecha del análisis:** 2026-09-05
**URL auditada:** https://draska.ueniweb.com/
**Tipo de página:** Home single-page (cumple simultáneamente rol de home + service page + contacto)
**Sector:** Enfermería / inyecciones a domicilio, Calama (Chile) — **YMYL de salud (barra E-E-A-T más alta)**
**Método:** `render_page.py --mode auto --json`; scoring E-E-A-T ejecutado sobre `extracted_text` (trafilatura), no sobre HTML crudo.

---

## 1. Puntuación global

| Métrica | Valor | Umbral | Estado |
|---|---|---|---|
| **Content Quality Score** | **34 / 100** | 70 | Falla |
| **E-E-A-T ponderado** | **28.5 / 100** | 65 | Falla |
| **AI Citation Readiness** | **21 / 100** | 60 | Falla |
| Palabras (main content) | 266 | 500 (home) / 800 (servicio) | Falla (-47% / -67%) |
| Caracteres (main content) | 1.827 | — | Muy delgado |
| Fernández Huerta (legibilidad ES) | 53,4 ("algo difícil") | 60-70 | Marginal |
| Longitud media de frase | 10,6 palabras | 15-20 | Fragmentado |
| Densidad "Calama" | 1,50% | 0,5-2,5% | OK (natural) |
| Densidad "enfermería" | 1,88% | 0,5-2,5% | OK (natural) |
| Bloques schema válidos | 1 (LocalBusiness) | — | Insuficiente |
| Imágenes con `alt` | 0 de las detectadas | 100% | Falla |
| Frescura declarada | `og:updated_time` 2026-04-11 | — | Falsa señal (ver 3.4) |

**Nota metodológica:** los pesos E-E-A-T (20/25/25/30) son el modelo interno de este skill, no de Google. Google no publica pesos numéricos; solo afirma que *"trust is most important"*. Los mínimos de palabras son **pisos de cobertura temática**, no objetivos: Google ha confirmado que el conteo de palabras **no es un factor de ranking directo**.

---

## 2. Desglose E-E-A-T

### 2.1 Experience — 25/100 (peso 20%) → aporta 5,0 pts

**Presente**
- 8 reseñas con nombre y fecha (2020-2024) renderizadas en la home.
- Descripción de un procedimiento real y de sus límites operativos.

**Ausente / roto**
- **6 de las 8 reseñas no tienen texto**: solo nombre + fecha. Las dos únicas con contenido son `"Exelente servicio"` (con falta ortográfica) y `"Excelente servicio"`. Cero detalle, cero especificidad, cero valor probatorio.
- Una de las reseñas está firmada por `hector huidobro` (24-10-2020), nombre que coincide con el propietario del email de contacto (`hectoremprendimiento9@gmail.com`). **Reseña autoreferencial aparente = riesgo directo de Trust bajo QRG**; debe eliminarse.
- **Cero fotografías del personal, del maletín, del proceso o de la atención.** Solo 1 `<img>` en el documento y un banner de stock genérico (asset de 2020).
- Ni un solo caso, testimonio extendido, número de pacientes atendidos, años de operación, ni anécdota de terreno.
- No hay nombre propio de ningún profesional en toda la página.

### 2.2 Expertise — 30/100 (peso 25%) → aporta 7,5 pts

**Presente**
- Declaración de calificación: *"técnicos en enfermería de nivel superior, inscritos en la superintendencia de salud"* y *"prestadores individuales de la salud"*. Es la señal más fuerte del sitio.
- Contenido educativo mínimo por servicio (mecanismo de acción anticonceptivo, composición de Neurobionta = B1/B6/B12).
- **Disclaimer clínico correcto**: exige prescripción médica y aclara que no vende insumos ni medicamentos. Esto es un acierto real y poco común en el rubro.

**Ausente / roto**
- **La credencial no es verificable.** Chile tiene un registro público (Registro Nacional de Prestadores Individuales de Salud, Superintendencia de Salud) con número por profesional. El sitio no publica ni número de registro, ni RUT, ni nombre del titular, ni enlace al registro. Una afirmación de credencial sin verificación posible es, en QRG YMYL, casi equivalente a no tener credencial.
- **Cero autoría.** Ningún `author`, ninguna bio, ninguna firma. En YMYL de salud esto es el defecto más caro del sitio.
- El párrafo de anticonceptivos inyectables (*"Alrededor de 5 millones de mujeres utilizan inyectables combinados mensuales en el mundo y su uso se ha difundido principalmente en china, algunos países de América latina e india..."*) tiene registro académico/institucional ajeno al resto de la página y **no cita fuente**. Es contenido de terceros sin atribución: riesgo de duplicado y de Trust.
- Bloque de Neurobionta **íntegramente en MAYÚSCULAS**, con afirmación vaga y no clínica (*"entrega beneficios positivos para nuestro cuerpo"*). No hay indicaciones, contraindicaciones, dosis, vía, ni advertencias.
- Errores que erosionan percepción de competencia profesional: `QUIENES SOMOS` (sin `¿` ni tilde), `Exelente`, `mas información`, `por que`, `numero`, `china`/`india` en minúscula, `Acercate` sin tilde en la meta description.
- Inconsistencia de voz: el cuerpo dice *"Somos un grupo"* (plural) y la meta description dice *"Oferto inyecciones"* (singular, primera persona). El lector no sabe si es un equipo o una persona.

### 2.3 Authoritativeness — 22/100 (peso 25%) → aporta 5,5 pts

**Presente**
- Perfil de Google Business con Place ID asociado (`ChIJFfyXTPEJrJYRzcBJnjIC7wA`) y página de Facebook enlazada.
- Historial: contenido e imágenes de 2020 → ~6 años de continuidad de la entidad.

**Ausente / roto**
- **Subdominio de constructor (`*.ueniweb.com`).** Techo estructural de autoridad: no se construye entidad de marca propia, no hay email corporativo, no hay control del dominio y toda señal de marca se diluye en el host.
- **Enlace saliente a `www.sanivida.cl`** con el texto *"mas información aquí"*. Se está derivando tráfico y contexto a otra entidad comercial del mismo rubro desde la sección de servicios. Confunde a Google sobre qué entidad presta el servicio y regala señal.
- **Triple identidad de marca**: `<title>` dice "Draska", `<h1>` y `og:site_name` dicen "INYECCIÓN A DOMICILIO CALAMA", y el contenido remite a "Sanivida". Tres nombres, ninguna entidad consolidada.
- `sameAs` incluye el Place ID crudo (`ChIJ...`) como si fuera URL. **Es inválido**: `sameAs` requiere URLs. Debe ser `https://www.google.com/maps/place/?q=place_id:ChIJ...`.
- Cero menciones, cero directorios sectoriales, cero citations NAP fuera de Google, cero prensa local, cero convenios (isapres, clínicas, farmacias, empresas mineras de la zona).
- Email en `gmail.com` con alias `hectoremprendimiento9` — señal de negocio no consolidado.

### 2.4 Trustworthiness — 35/100 (peso 30%) → aporta 10,5 pts

**Presente**
- HTTPS, teléfono visible (+56 9 7883 3741), WhatsApp, email, formulario con reCAPTCHA, comuna declarada.
- **Transparencia de precios**: $10.000 inyección anticonceptiva, $12.000 Neurobionta, $10.000 inyección de medicamento. Excelente señal de confianza y de intención transaccional.
- Schema `LocalBusiness` válido con `geo`, `telephone`, `address`.
- Disclaimer de receta médica obligatoria.

**Ausente / roto**
- **NAP defectuoso**: `streetAddress: "Punta Arenas"` con `addressLocality: "Calama"`. Sin número, y "Punta Arenas" es además el nombre de otra ciudad chilena → ambigüedad de entidad. `postalCode: 139000` tiene 6 dígitos; los códigos postales chilenos tienen 7 (Calama ≈ 1390000). **Dato incorrecto en el schema.**
- **Sin horarios de atención** en la página ni en el schema (`openingHoursSpecification` ausente). Para un servicio a domicilio bajo demanda es la información operativa #1 que busca el usuario.
- **Sin registro sanitario verificable, sin RUT, sin razón social, sin representante legal.**
- Sin política de privacidad propia: solo la de UENI. En un servicio de salud se recogen **datos sensibles** (Ley 19.628); la falta de política propia y de consentimiento informado es un fallo legal y de Trust.
- Sin protocolo de bioseguridad, sin mención de manejo de residuos cortopunzantes (REAS), sin insumos estériles de un solo uso, sin seguro de responsabilidad civil.
- Sin política de cancelación, sin tiempo de respuesta comprometido, sin cobertura horaria de urgencia.
- El precio "12.000 Neurobionta / POR CADA 3 INYECCIÓN" es ambiguo: no se entiende si son $12.000 el pack de 3 o $12.000 cada una. Ambigüedad de precio = fricción de conversión y señal de descuido.
- Reseña aparentemente propia (ver 2.1).

### 2.5 Cálculo

| Factor | Peso | Score | Aporte |
|---|---|---|---|
| Experience | 20% | 25 | 5,0 |
| Expertise | 25% | 30 | 7,5 |
| Authoritativeness | 25% | 22 | 5,5 |
| Trustworthiness | 30% | 35 | 10,5 |
| **Total** | 100% | — | **28,5 / 100** |

---

## 3. Hallazgos adicionales

### 3.1 Contenido delgado y cobertura temática
266 palabras de contenido principal cubriendo 3 servicios, la sección "quiénes somos", precios, cobertura y contacto. Cada servicio recibe entre 20 y 55 palabras. No existe blog, ni FAQ, ni página interna alguna: es una arquitectura de **una sola URL**. La cobertura temática es del orden del 10-15% de lo que exige el cluster "enfermería a domicilio".

### 3.2 Duplicación
- Las 8 reseñas se renderizan **dos veces** en el DOM (carrusel duplicado) → duplicación interna de contenido y ruido para extractores.
- El párrafo de anticoncepción hormonal aparenta ser copia literal de material institucional/académico sin atribución.

### 3.3 Legibilidad y formato
- Fernández Huerta 53,4 → "algo difícil" para un contenido de salud dirigido a público general; el objetivo debería ser 65-75.
- Bloques completos en MAYÚSCULAS (servicios, Neurobionta) → penaliza comprensión, escaneabilidad y percepción profesional.
- Jerarquía de encabezados irregular: H1 → H2 → H3, pero los H2 de UENI (`Servicios`, `Facilidades`, `Opiniones`, `Áreas cubiertas`) son etiquetas de plantilla sin keyword, y los H3 de contenido real cuelgan del H2 equivocado.
- 0 atributos `alt`. 0 listas semánticas (`<ul>`) para los servicios: se usan guiones dentro de un párrafo.

### 3.4 Frescura
`og:updated_time` y `publication_date` reportan **2026-04-11**, pero el contenido y los assets son de 2020 y las reseñas más recientes de mayo 2024. La fecha proviene del republicado de la plataforma, no de una actualización editorial. **Señal de frescura falsa**: no hay ningún "actualizado el" visible para el usuario ni cambios sustantivos de contenido.

### 3.5 Evaluación de contenido AI (criterios QRG sept-2025)
**No hay marcadores de contenido generado por IA.** El texto es claramente humano: errores ortográficos, cambios de voz, mayúsculas inconsistentes, registro irregular. Los riesgos QRG presentes son de otra naturaleza:
- Contenido de terceros sin atribución (párrafo de anticonceptivos).
- Ausencia total de autoría en contenido YMYL de salud.
- Reseña plausiblemente autoreferencial.
- Página que enlaza a una entidad comercial distinta desde su propia sección de servicios.

Recordatorio: el Helpful Content System se integró al core en el update de marzo 2024 y ya no opera como clasificador independiente; la helpfulness se evalúa dentro de cada core update.

### 3.6 AI Citation Readiness — 21/100

| Criterio | Score | Nota |
|---|---|---|
| Hechos citables y autocontenidos | 30 | Existen (precios, composición de Neurobionta, cobertura) pero en MAYÚSCULAS y sin sujeto explícito |
| Datos estructurados | 25 | Solo LocalBusiness. Sin `Service`, `Offer`, `Person`, `FAQPage`, `MedicalWebPage`, `openingHours` |
| Jerarquía clara | 25 | H2/H3 de plantilla, sin correspondencia con las entidades reales |
| Formato extractable (listas, tablas, definiciones) | 10 | Ninguna lista semántica, ninguna tabla, ninguna definición en formato "X es Y" |
| Autoría y fecha | 0 | Inexistentes |
| Cobertura de preguntas (FAQ) | 5 | Ninguna pregunta explícita respondida |
| Entidad inequívoca | 20 | Tres nombres de marca compitiendo |
| **Total** | **21** | |

Un LLM que responda *"¿dónde pongo una inyección a domicilio en Calama?"* puede extraer el teléfono y poco más. No puede citar quién presta el servicio, con qué credencial, en qué horario, ni en qué condiciones.

---

## 4. Por qué este contenido delgado rankea igualmente

No rankea *por* el contenido. Rankea **a pesar** de él, por seis razones acumuladas:

1. **El nombre del negocio es la keyword exacta.** `INYECCIÓN A DOMICILIO CALAMA` está en el nombre de la entidad, en `og:site_name` y en el `<h1>`. En local pack, la coincidencia de la query con el nombre del negocio en Google Business Profile sigue siendo uno de los factores de mayor peso. Es un caso de libro de EMB (exact-match business name).
2. **El ranking es de Google Business Profile, no del sitio.** El `sameAs` con Place ID revela una ficha verificada con reseñas fechadas entre 2020 y 2024. En consultas locales de servicio, la ficha hace el trabajo pesado y el sitio solo debe confirmar relevancia y no romper nada.
3. **Competencia prácticamente nula.** Calama (~180 mil habitantes) con un nicho de volumen bajo. La mayoría de los competidores opera solo por WhatsApp/Facebook, sin sitio web. Google rankea el mejor resultado *disponible*, no el mejor resultado *posible*.
4. **Coincidencia perfecta de intención transaccional.** La query es "quiero que alguien venga a inyectarme". La página entrega en el primer scroll: qué, dónde, cuánto cuesta, a qué teléfono llamar. Cero fricción, cero contenido de relleno. Paradójicamente, la delgadez ayuda: no hay ruido entre la intención y la conversión.
5. **Antigüedad y estabilidad de la entidad.** ~6 años de existencia continua con NAP estable y flujo de reseñas.
6. **Higiene técnica suficiente.** HTTPS, mobile-first, GTM diferido, canonical correcto, schema LocalBusiness válido, `og:locale es_CL`, coordenadas geográficas exactas.

**Conclusión estratégica:** la posición actual es defendible solo mientras nadie invierta en el nicho. Es un ranking **frágil**: depende de una ventaja de nombre y de la ausencia de competencia, no de un foso de contenido. Un sitio nuevo con E-E-A-T real y arquitectura de cluster lo desplaza en 4-8 meses, y además captura decenas de queries de long tail que este sitio ni siquiera puede responder.

---

## 5. Recomendaciones priorizadas para el sitio NUEVO

### Tier 0 — Fundaciones (antes de escribir una línea)

| # | Acción | Por qué |
|---|---|---|
| 0.1 | **Dominio propio .cl** (ej. `enfermeriadomicilio-calama.cl` o marca + `.cl`). Nunca subdominio de constructor. | Sin esto hay un techo de autoridad que ningún contenido supera. |
| 0.2 | **Email corporativo** `contacto@dominio.cl`. Retirar el gmail de todos los metadatos. | Trust básico en salud. |
| 0.3 | **Nombre de marca único** usado de forma idéntica en `<title>`, `<h1>`, GBP, schema, redes y facturación. Un solo nombre. | El sitio auditado pierde señal por tener tres. |
| 0.4 | **GBP verificado** con categoría primaria correcta, horarios, zona de servicio y fotos reales. | Es el motor real del ranking local. |
| 0.5 | NAP exacto y consistente: razón social, RUT, dirección real con número, comuna, código postal de 7 dígitos. | El sitio auditado tiene el schema con datos incorrectos. |

### Tier 1 — Páginas críticas (semanas 1-4)

| Prioridad | Página | URL sugerida | Palabras objetivo | Objetivo |
|---|---|---|---|---|
| P0 | Home | `/` | 700-900 | Intención transaccional + prueba de confianza inmediata |
| P0 | Inyecciones intramusculares a domicilio | `/inyecciones-a-domicilio-calama/` | 900-1.200 | Cabecera del cluster, keyword principal |
| P0 | Quiénes somos / Equipo | `/equipo/` | 600-800 | Núcleo de Expertise + Experience |
| P0 | Ficha individual por profesional | `/equipo/[nombre-apellido]/` | 400-600 c/u | Autoría verificable, `Person` + `hasCredential` |
| P0 | Precios y coberturas | `/precios/` | 500-700 | Trust + conversión + tabla extractable por LLM |
| P0 | Contacto / Agendar | `/agendar/` | 300-400 | Conversión, horarios, tiempos de respuesta |
| P1 | Inyección anticonceptiva mensual | `/inyeccion-anticonceptiva-domicilio-calama/` | 900-1.200 | Servicio de mayor recurrencia |
| P1 | Neurobionta / complejo B | `/inyeccion-neurobionta-domicilio-calama/` | 900-1.200 | Alto volumen de búsqueda de marca |
| P1 | Control de signos vitales | `/control-signos-vitales-domicilio-calama/` | 800-1.000 | |
| P1 | FAQ general | `/preguntas-frecuentes/` | 800-1.200 | Motor de citación por IA |
| P1 | Cobertura y zonas | `/cobertura-calama/` | 500-600 | Refuerzo hiperlocal |

### Tier 2 — Confianza y legalidad (semanas 3-6)

| Página | URL | Contenido |
|---|---|---|
| Protocolo de bioseguridad | `/protocolo-bioseguridad/` | Insumos estériles de un solo uso, manejo de cortopunzantes y residuos REAS (DS N°6/2009 MINSAL), lavado de manos, técnica aséptica, trazabilidad |
| Credenciales y verificación | `/credenciales/` | Número de Registro Nacional de Prestadores Individuales de Salud por profesional + enlace directo al buscador de la Superintendencia + títulos + certificaciones (RCP/BLS, IAAS) |
| Política de privacidad y datos de salud | `/privacidad/` | Ley 19.628 (datos sensibles), qué se recoge, cuánto se conserva, con quién se comparte |
| Consentimiento informado | `/consentimiento-informado/` | Ley 20.584 de derechos y deberes del paciente |
| Aviso médico y política editorial | `/aviso-medico/` | Quién escribe, quién revisa, con qué frecuencia se actualiza, qué fuentes se usan |
| Términos, cancelación y reembolsos | `/terminos/` | Política de cancelación, no-show, cobertura de urgencias |

### Tier 3 — Autoridad temática (mes 2 en adelante)

Blog `/recursos/`, 2 artículos al mes, 1.500+ palabras, cada uno firmado por un TENS con número de registro:

1. "Inyección intramuscular en el glúteo: por qué la técnica correcta importa" (Experience: relato de terreno)
2. "Anticonceptivo inyectable mensual: qué esperar el primer mes" (con contraindicaciones y cuándo consultar)
3. "Neurobionta: qué es, para qué se indica y cuándo NO debe usarse"
4. "Cómo verificar si tu enfermero está registrado en la Superintendencia de Salud" (guía paso a paso, alto potencial de enlaces)
5. "Presión arterial en casa: cómo medirla bien y qué valores preocupan"
6. "Qué debes tener listo antes de que llegue el enfermero a domicilio" (checklist)

> **Nota de delegación:** si se plantea generar páginas por sector/población de forma programática (`/inyecciones-a-domicilio/[sector]/`), **no se hace en esta fase** y debe evaluarse con el sub-skill `seo-programmatic`. Con menos de 8-10 sectores diferenciables en Calama, el riesgo de doorway pages supera el beneficio. Una sola página `/cobertura-calama/` con la lista de sectores es la opción correcta.

### Tier 4 — Datos estructurados

```json
{
  "@context": "https://schema.org",
  "@type": ["HomeHealthCareService", "MedicalBusiness"],
  "@id": "https://dominio.cl/#organizacion",
  "name": "NOMBRE ÚNICO DE MARCA",
  "medicalSpecialty": "Nursing",
  "address": { "@type": "PostalAddress", "streetAddress": "Calle 000", "addressLocality": "Calama", "addressRegion": "Antofagasta", "postalCode": "1390000", "addressCountry": "CL" },
  "geo": { "@type": "GeoCoordinates", "latitude": -22.4703921, "longitude": -68.9293679 },
  "areaServed": { "@type": "City", "name": "Calama" },
  "telephone": "+56978833741",
  "email": "contacto@dominio.cl",
  "openingHoursSpecification": [
    { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "08:00", "closes": "21:00" },
    { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday","Sunday"], "opens": "09:00", "closes": "20:00" }
  ],
  "employee": [{
    "@type": "Person",
    "name": "Nombre Apellido",
    "jobTitle": "Técnico en Enfermería de Nivel Superior",
    "hasCredential": {
      "@type": "EducationalOccupationalCredential",
      "credentialCategory": "Registro Nacional de Prestadores Individuales de Salud",
      "identifier": "NÚMERO-DE-REGISTRO",
      "recognizedBy": { "@type": "GovernmentOrganization", "name": "Superintendencia de Salud de Chile" }
    }
  }],
  "makesOffer": [{
    "@type": "Offer",
    "itemOffered": { "@type": "Service", "name": "Inyección intramuscular a domicilio" },
    "priceSpecification": { "@type": "PriceSpecification", "price": "10000", "priceCurrency": "CLP" }
  }],
  "sameAs": [
    "https://www.google.com/maps/place/?q=place_id:PLACE_ID",
    "https://www.facebook.com/PAGINA",
    "https://www.instagram.com/PERFIL"
  ]
}
```

Adicionalmente: `Service` en cada página de servicio, `FAQPage` en FAQ y en el bloque FAQ de cada servicio, `MedicalWebPage` con `reviewedBy` en el contenido educativo, `BreadcrumbList` en todo el sitio.

**Advertencias de honestidad técnica:**
- Google **descontinuó** los rich results de FAQ para la mayoría de sitios (agosto 2023). `FAQPage` se implementa igualmente porque sigue siendo el formato que mejor extraen los LLM y los AI Overviews.
- El marcado `Review`/`AggregateRating` **sobre el propio negocio y alojado en su propio sitio** es contenido autoreferencial y **no es elegible** para rich results según la política de Google. Se implementa por valor de usuario y de citación por IA, no esperando estrellas en la SERP. Las estrellas se ganan en Google Business Profile.

---

## 6. Ejemplos de copy orientado a E-E-A-T y conversión

### 6.1 Title y meta description (Home)

```
Title:  Inyecciones a Domicilio en Calama | TENS Registrados | Atención en 60 min
Meta:   Enfermeros técnicos de nivel superior registrados en la Superintendencia
        de Salud. Inyecciones intramusculares, anticonceptivo mensual y control
        de signos vitales en tu casa, en Calama. Desde $10.000. Llega en 60 min.
```

Contraste con el sitio auditado: cambia "Oferto inyecciones con profesionalidad y cuidado" (adjetivos vacíos, primera persona incoherente) por credencial + tiempo + precio (hechos verificables y citables).

### 6.2 H1 y hero

```
H1: Inyecciones a domicilio en Calama, aplicadas por TENS registrados

Aplicamos tu inyección intramuscular en tu casa, con receta médica vigente,
insumos estériles de un solo uso y retiro del material cortopunzante.
Somos técnicos en enfermería de nivel superior inscritos en el Registro
Nacional de Prestadores Individuales de Salud de la Superintendencia de Salud.

[ Verificar nuestro registro ]   [ Agendar por WhatsApp ]

Tiempo promedio de llegada: 45-70 minutos · Lunes a domingo, 08:00 a 21:00
Desde $10.000 · Boleta electrónica · Efectivo, transferencia y débito
```

### 6.3 Bloque de credenciales verificables (el diferenciador #1)

```
### Puedes verificar quién te atiende, antes de que llegue

María Fernanda Rojas Aguilera
Técnico en Enfermería de Nivel Superior
Registro Superintendencia de Salud N.º 000000
Título: INACAP Calama, 2018
Certificaciones vigentes: RCP Básico (2025) · Prevención de IAAS (2025)
7 años de experiencia · más de 4.000 administraciones intramusculares

→ Verificar este registro en el buscador de la Superintendencia de Salud

Publicamos el número de registro de cada profesional de nuestro equipo.
Si alguien ofrece inyecciones a domicilio y no puede darte el suyo,
no lo dejes entrar a tu casa.
```

Ese último párrafo es simultáneamente Experience (postura de alguien del rubro), Trust y un imán de enlaces.

### 6.4 Página de servicio — estructura y apertura

```
H1: Inyección anticonceptiva mensual a domicilio en Calama

Aplicamos tu anticonceptivo inyectable mensual en tu domicilio, el mismo día
que corresponde según tu ciclo, por $10.000 y con boleta.
Necesitas tener a mano tu receta médica vigente y la ampolla; nosotros
llevamos la jeringa, la aguja, el antiséptico y el contenedor de residuos.

H2: Qué incluye el servicio
- Verificación de tu receta médica y de la fecha correcta de aplicación
- Aplicación intramuscular con técnica aséptica
- Control de presión arterial sin costo adicional
- Registro de la fecha y recordatorio para tu próxima dosis
- Retiro del material cortopunzante en contenedor normado

H2: Qué NO incluye
No vendemos ni suministramos medicamentos. Por normativa, la venta de
fármacos corresponde exclusivamente a farmacias autorizadas. Debes tener
la ampolla y la receta médica vigente antes de la visita.

H2: Cuándo debe aplicarse el inyectable mensual
[contenido educativo con fuente citada]

H2: Efectos frecuentes y cuándo consultar a tu médico
[contenido educativo con fuente citada]

H2: Preguntas frecuentes
[6-8 preguntas]

---
Escrito por María Fernanda Rojas, TENS, Registro N.º 000000
Revisado clínicamente: marzo 2026 · Última actualización: marzo 2026
Este contenido es informativo y no reemplaza la indicación de tu médico.
```

El bloque "Qué NO incluye" es una de las señales de Trust más subestimadas: **decir lo que no haces genera más confianza que ampliar lo que sí haces.** El sitio auditado ya tiene ese instinto correcto; solo lo tiene mal redactado y enterrado.

### 6.5 FAQ optimizada para citación por IA

Formato obligatorio: pregunta en la forma exacta en que la escribe el usuario, y **primera frase de la respuesta autocontenida y citable sin contexto**.

```
¿Necesito receta médica para una inyección a domicilio en Calama?
Sí. En Chile se exige receta médica vigente para administrar cualquier
medicamento inyectable, incluidos los anticonceptivos mensuales y el
complejo B. Nosotros verificamos la receta antes de aplicar y, si no la
tienes, no realizamos el procedimiento y no cobramos la visita.

¿Cuánto cuesta una inyección a domicilio en Calama?
Una inyección intramuscular a domicilio en Calama cuesta $10.000 e incluye
insumos estériles, aplicación y retiro del material cortopunzante. El
medicamento no está incluido y debe aportarlo el paciente.

¿Cuánto se demoran en llegar?
El tiempo promedio de llegada dentro del radio urbano de Calama es de
45 a 70 minutos entre las 08:00 y las 21:00.

¿Qué hacen con la jeringa después?
Retiramos todo el material cortopunzante en un contenedor normado y lo
eliminamos según el reglamento de residuos de establecimientos de atención
de salud (DS N.º 6/2009 MINSAL). Nunca dejamos agujas en tu basura
domiciliaria.

¿Cómo sé que quien me atiende es realmente enfermero?
Cada profesional de nuestro equipo publica su número de Registro Nacional
de Prestadores Individuales de Salud, que puedes consultar gratis en el
sitio de la Superintendencia de Salud antes de agendar. Además llegamos
con credencial y uniforme identificado.
```

### 6.6 Prueba social con especificidad

En vez de "Excelente servicio":

```
"Mi mamá tiene 78 años y trasladarla al consultorio para el complejo B
era un problema cada mes. Llamé un domingo a las 9 de la mañana y a las
10:15 ya estaban en la casa. Le tomaron la presión sin que yo lo pidiera
y me avisaron que estaba un poco alta para que la lleváramos al médico."

— Carolina M., sector Villa Ayquina, Calama · Marzo 2026
Servicio: Inyección de complejo B + control de signos vitales
```

Nombre, sector, fecha, servicio y un detalle imposible de inventar. Eso es Experience.

### 6.7 Bloque de conversión con reducción de riesgo

```
Agenda en 30 segundos por WhatsApp

1. Escríbenos y envíanos una foto de tu receta
2. Te confirmamos hora de llegada y precio final antes de salir
3. Pagas al terminar: efectivo, transferencia o débito, con boleta

Si tu receta no está vigente o el medicamento no corresponde,
te lo decimos por WhatsApp y no se cobra nada.

[ Escribir por WhatsApp ]   [ Llamar ahora ]
```

### 6.8 Correcciones de copy a no repetir del sitio auditado

| Problema en draska.ueniweb.com | Corrección |
|---|---|
| Párrafos completos en MAYÚSCULAS | Sentence case en todo el sitio |
| "Exelente", "mas información", "por que", "numero", "QUIENES SOMOS" | Revisión ortográfica completa; en salud, un typo cuesta credibilidad |
| "Somos" vs "Oferto" | Una sola voz, en plural, consistente en todo el sitio |
| "entrega beneficios positivos para nuestro cuerpo" | Indicaciones concretas, dosis, vía, contraindicaciones y fuente |
| Párrafo de anticonceptivos sin fuente | Reescribir con voz propia y citar (MINSAL, ICMER, OMS) |
| Enlace saliente a otra empresa del rubro | Nunca. Los enlaces salientes van a fuentes de autoridad sanitaria |
| "cualquier inconveniente será de su propia responsabilidad" | Redacción hostil y legalmente débil. Sustituir por consentimiento informado formal |
| Precio "12.000 POR CADA 3 INYECCIÓN" | Tabla de precios inequívoca: unitario y pack, ambos explícitos |

---

## 7. Hoja de ruta priorizada

| Fase | Semanas | Entregables | Impacto esperado |
|---|---|---|---|
| **F1 — Fundación** | 1-2 | Dominio .cl, email corporativo, GBP verificado con fotos reales, NAP consistente, home + servicio principal + equipo + precios + contacto | Paridad competitiva |
| **F2 — Diferenciación E-E-A-T** | 3-6 | Fichas individuales con registro verificable, páginas de bioseguridad/credenciales/privacidad/consentimiento, 3 páginas de servicio restantes, FAQ, schema completo | Superación del incumbente en Trust |
| **F3 — Autoridad temática** | 7-16 | 2 artículos/mes firmados y revisados, cobertura de zonas, captación de reseñas reales con texto (objetivo: 25+ en GBP), citations NAP en directorios chilenos | Long tail + defensa del ranking |
| **F4 — Mantenimiento** | Continuo | Revisión clínica semestral con fecha visible, actualización de precios, incorporación de nuevos servicios (curaciones, toma de muestras, sondas) | Frescura real, no falsa |

**Métricas objetivo a 6 meses:** Content Quality Score ≥ 75, E-E-A-T ≥ 70, AI Citation Readiness ≥ 65, 12+ URLs indexadas, 25+ reseñas con texto en GBP.

---

## 8. Findings estructurados (para `audit-data.json` → categoría Content Quality)

```json
{
  "category": "content_quality",
  "url": "https://draska.ueniweb.com/",
  "analyzed_at": "2026-09-05",
  "scores": {
    "content_quality": 34,
    "eeat_weighted": 28.5,
    "eeat_experience": 25,
    "eeat_expertise": 30,
    "eeat_authoritativeness": 22,
    "eeat_trustworthiness": 35,
    "ai_citation_readiness": 21
  },
  "metrics": {
    "word_count": 266,
    "char_count": 1827,
    "word_count_floor_homepage": 500,
    "word_count_floor_service": 800,
    "readability_fernandez_huerta": 53.4,
    "avg_words_per_sentence": 10.6,
    "keyword_density_calama_pct": 1.50,
    "keyword_density_enfermeria_pct": 1.88,
    "images_with_alt": 0,
    "schema_blocks_valid": 1,
    "schema_types": ["LocalBusiness", "PostalAddress", "GeoCoordinates"],
    "reviews_total": 8,
    "reviews_with_text": 2,
    "internal_pages": 1,
    "is_spa": false,
    "declared_update_date": "2026-04-11",
    "actual_content_vintage": "2020"
  },
  "findings": [
    { "id": "cq-001", "severity": "critical", "title": "Contenido delgado en página YMYL de salud", "detail": "266 palabras cubriendo home, 3 servicios, precios y contacto. 47% bajo el piso de home y 67% bajo el de service page.", "recommendation": "Arquitectura de cluster: home 700-900 + una service page 900-1200 por servicio." },
    { "id": "cq-002", "severity": "critical", "title": "Cero autoría en contenido médico", "detail": "Ningún profesional identificado, sin bio, sin firma, sin fecha de revisión clínica.", "recommendation": "Página /equipo/ + ficha individual + firma con nombre y registro en cada contenido educativo." },
    { "id": "cq-003", "severity": "critical", "title": "Credencial sanitaria no verificable", "detail": "Se afirma inscripción en la Superintendencia de Salud sin número de registro, sin RUT y sin enlace al registro público.", "recommendation": "Publicar N.º de Registro Nacional de Prestadores Individuales de Salud por profesional + enlace directo al buscador oficial + schema Person/hasCredential." },
    { "id": "cq-004", "severity": "critical", "title": "Datos NAP incorrectos en schema", "detail": "streetAddress 'Punta Arenas' sin número dentro de addressLocality 'Calama'; postalCode 139000 con 6 dígitos (Chile usa 7).", "recommendation": "Corregir dirección con número, agregar addressRegion Antofagasta y postalCode de 7 dígitos." },
    { "id": "cq-005", "severity": "high", "title": "Identidad de marca fragmentada en tres nombres", "detail": "'Draska' en title, 'INYECCIÓN A DOMICILIO CALAMA' en h1/og:site_name, 'Sanivida' referenciado en el cuerpo.", "recommendation": "Consolidar en un único nombre en title, h1, schema, GBP y redes." },
    { "id": "cq-006", "severity": "high", "title": "Enlace saliente a entidad comercial del mismo rubro", "detail": "'mas información aquí: www.sanivida.cl' dentro de la sección de servicios.", "recommendation": "Eliminar. Los enlaces salientes deben ir a autoridades sanitarias (MINSAL, Superintendencia, OMS)." },
    { "id": "cq-007", "severity": "high", "title": "Contenido de terceros sin atribución", "detail": "El párrafo sobre anticonceptivos inyectables mensuales presenta registro académico ajeno al resto y no cita fuente.", "recommendation": "Reescribir con voz propia y citar fuente explícita." },
    { "id": "cq-008", "severity": "high", "title": "Ausencia de horarios de atención", "detail": "Sin horarios en la página ni openingHoursSpecification en el schema, en un servicio a domicilio bajo demanda.", "recommendation": "Publicar horarios visibles + tiempo promedio de llegada + openingHoursSpecification." },
    { "id": "cq-009", "severity": "high", "title": "Prueba social sin valor probatorio", "detail": "6 de 8 reseñas sin texto; una firmada con el mismo nombre asociado al email de contacto del negocio.", "recommendation": "Retirar la reseña autoreferencial. Captar testimonios con sector, fecha, servicio y detalle concreto." },
    { "id": "cq-010", "severity": "high", "title": "Sin política de privacidad ni consentimiento informado propios", "detail": "Solo aparecen las políticas del constructor UENI, pese a recogerse datos de salud (sensibles, Ley 19.628).", "recommendation": "Publicar privacidad propia, consentimiento informado (Ley 20.584) y aviso médico/política editorial." },
    { "id": "cq-011", "severity": "medium", "title": "Señal de frescura falsa", "detail": "og:updated_time 2026-04-11 sobre contenido y assets de 2020; reseñas más recientes de 2024.", "recommendation": "Fechas de publicación y revisión visibles, con actualización editorial real y no republicado de plataforma." },
    { "id": "cq-012", "severity": "medium", "title": "Formato no extractable por IA", "detail": "Bloques íntegros en mayúsculas, sin listas semánticas, sin tablas, sin FAQ, sin definiciones autocontenidas.", "recommendation": "Sentence case, listas <ul>, tabla de precios, FAQPage con respuestas citables en la primera frase." },
    { "id": "cq-013", "severity": "medium", "title": "Cero atributos alt en imágenes", "detail": "Ninguna imagen detectada declara alt.", "recommendation": "Alt descriptivo en todas las imágenes; incorporar fotos reales del equipo y del material." },
    { "id": "cq-014", "severity": "medium", "title": "sameAs con Place ID crudo inválido", "detail": "'ChIJFfyXTPEJrJYRzcBJnjIC7wA' se declara en sameAs, que exige URLs.", "recommendation": "Usar https://www.google.com/maps/place/?q=place_id:ChIJ..." },
    { "id": "cq-015", "severity": "medium", "title": "Errores ortográficos en contenido YMYL", "detail": "'Exelente', 'mas información', 'por que', 'numero', 'QUIENES SOMOS' sin signo ni tilde, 'Acercate' en meta description.", "recommendation": "Revisión ortográfica integral; en salud los errores erosionan expertise percibida." },
    { "id": "cq-016", "severity": "medium", "title": "Precio ambiguo", "detail": "'INYECCIÓN NEUROBIONTA 12.000 $ / POR CADA 3 INYECCIÓN' no distingue precio unitario de pack.", "recommendation": "Tabla de precios con unitario y pack explícitos + schema Offer/priceSpecification." },
    { "id": "cq-017", "severity": "low", "title": "Duplicación interna del bloque de reseñas", "detail": "Las 8 reseñas se renderizan dos veces en el DOM por el carrusel.", "recommendation": "Renderizar una sola vez o clonar por CSS/JS sin duplicar en el DOM." },
    { "id": "cq-018", "severity": "low", "title": "Incoherencia de voz narrativa", "detail": "El cuerpo usa plural ('Somos un grupo') y la meta description usa singular ('Oferto inyecciones').", "recommendation": "Unificar en primera persona plural en todo el sitio." }
  ],
  "ai_content_assessment": {
    "ai_generated_likelihood": "low",
    "qrg_sept_2025_flags": [
      "unattributed_third_party_content",
      "no_author_on_ymyl_health_content",
      "likely_self_authored_review",
      "outbound_link_to_competing_commercial_entity"
    ],
    "note": "No se detectan marcadores de generación por IA. El texto presenta errores ortográficos, cambios de registro y mayúsculas inconsistentes propios de redacción humana no editada. Los riesgos QRG son de atribución y transparencia, no de origen automatizado."
  },
  "ranking_hypothesis": [
    "exact_match_business_name_en_gbp_y_h1",
    "ranking_impulsado_por_google_business_profile_verificado",
    "competencia_local_practicamente_inexistente_en_calama",
    "coincidencia_perfecta_de_intencion_transaccional",
    "antiguedad_y_estabilidad_de_entidad_desde_2020",
    "higiene_tecnica_suficiente_https_mobile_schema_canonical"
  ],
  "competitive_verdict": "Ranking frágil. Sostenido por ventaja de nombre y vacío competitivo, no por un foso de contenido. Desplazable en 4-8 meses por un sitio con E-E-A-T verificable y arquitectura de cluster."
}
```
