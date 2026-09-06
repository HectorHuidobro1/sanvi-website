# Análisis SXO — "inyección a domicilio Calama" / "enfermería a domicilio Calama"

**URL de referencia analizada:** https://draska.ueniweb.com/
**Fecha del análisis:** 2026-09-05
**Alcance:** SERP LatAm para el patrón `inyecciones a domicilio [ciudad]` (Chile, Perú, México)
**Objetivo:** determinar qué page-type premia Google en este nicho y qué estructura de landing conviene a un sitio **nuevo**, replicable a cualquier ciudad.

---

## 0. Metodología y evidencia recogida

| Paso | Herramienta | Resultado |
|---|---|---|
| Render de la página objetivo | `claude-seo run render_page.py --mode always --json` | HTTP 200, `is_spa: false`, render OK, 0 errores de consola |
| Parseo SEO | `claude-seo run parse_html.py` | Title, meta, H1-H3, 1 imagen, 1 bloque schema, 567 palabras |
| SERP research | 5 consultas WebSearch (CL / PE / MX / genérico precio / genérico FAQ) | 40+ resultados orgánicos clasificados |
| Análisis de competidores | WebFetch estructural | `enfermerasatodahora.com` (Lima), `medplussalud.cl` (Santiago), `mdcare.cl` (Santiago), `enfermerosgabriel.com/ciudades/cdmx/inyecciones/` (CDMX) |

---

## 1. HALLAZGO PRINCIPAL — No hay mismatch de page-type: hay **mismatch de profundidad y de confianza**

**Severidad: MEDIA (page-type) / CRÍTICA (contenido + trust)**

Lo contraintuitivo del caso Draska es lo más valioso del análisis:

> **Draska rankea *porque acertó el page-type y la entidad local*, no a pesar de ser básica.**
> Su ventaja no es el contenido: es que es una **Local Service Page** con `LocalBusiness` schema, NAP, geo-coordenadas, área de cobertura declarada, teléfono clicable, `wa.me` y — señal decisiva — un **Google Place ID real en `sameAs`** (`ChIJFfyXTPEJrJYRzcBJnjIC7wA`), es decir, una Ficha de Empresa de Google vinculada. En un mercado de baja competencia (Calama, ~180k hab.), eso basta para dominar.

Traducción operativa para un sitio nuevo: **el page-type y la entidad local valen más que el diseño**. Pero Draska no escalaría ni convertiría en una ciudad competitiva, y ahí es donde se pierde el negocio (ver §5 y §6).

### Clasificación con la taxonomía (`page-type-taxonomy.md`)

**Página objetivo (Draska):** tipo **7 — Local Page**, con solapamiento de tipo **5 — Service Page**.
Prioridad de clasificación aplicada: regla 2 ("dirección física + geo → Local"). Señales presentes: `PostalAddress` (Punta Arenas, Calama, CL), `GeoCoordinates` (-22.4704, -68.9294), sección "Áreas cubiertas: Calama", `tel:` y `wa.me` en el DOM, `priceRange: "$"`.

**Consenso del SERP:** tipo **Local Service Page** (híbrido Local + Service) con **~70 % de confianza**.

---

## 2. Análisis del SERP — qué premia Google en `inyecciones a domicilio [ciudad]`

### 2.1 Muestra clasificada (agregada CL / PE / MX)

| # | Resultado | Mercado | Page-type | Profundidad est. | Señales |
|---|---|---|---|---|---|
| 1 | `inyeccionesadomicilio.cl` | CL | Local Service Page (dominio semi-EMD) | media | EMD, home = landing de servicio |
| 2 | `inyeccionessantiago.cl` | CL | Local Service Page (EMD + ciudad) | media | EMD ciudad, dirección Las Condes |
| 3 | `medplussalud.cl/inyecciones-a-domicilio/` | CL | **Local Service Page** | alta (~1.500 pal.) | Precio "desde $50.000", 300+ reseñas Google 4,9★, 33 comunas listadas, acreditaciones, proceso 3 pasos |
| 4 | `mdcare.cl/inyecciones-a-domicilio/` | CL | **Local Service Page** | alta | "Insumos incluidos", 10 años, enfermeras acreditadas Superintendencia, 40+ comunas, convenios Fonasa/Isapres, FAQ, horarios |
| 5 | `enfermeriatucasa.cl/inyecciones-a-domicilio-intramuscular-y-sub-cutanea/` | CL | Local Service Page (silo por procedimiento) | media-alta | URL por tipo de inyección |
| 6 | `enfermerasatudomicilio.cl/inyecciones.html` | CL | Local Service Page multi-ciudad | media | Título con 4 ciudades (Concepción, Talcahuano, San Pedro, Chiguayante) |
| 7 | `especialistaenheridas.cl/enfermera-inyecciones-vacunas-domicilio-antofagasta` | CL | **Local Service Page templada por ciudad** | media | URL `[servicio]-[ciudad]`, hermana en La Serena/Coquimbo |
| 8 | **`draska.ueniweb.com`** | CL | Local Service Page (mínima) | **baja (567 pal.)** | Schema LocalBusiness, GBP vinculada |
| 9 | `yapo.cl/paginas/servicios/inyecciones-a-domicilio` | CL | **Directorio / clasificados** | n/a | Agregador |
| 10 | `evisos.cl/inyecciones-a-domicilio.htm` | CL | **Directorio / clasificados** | n/a | Agregador |
| 11 | `doctoralia.cl/enfermero/antofagasta` | CL | **Directorio vertical salud** | n/a | "Los 20 enfermeros más recomendados" |
| 12 | `cronoshare.cl/.../enfermeria-a-domicilio/antofagasta` | CL | Marketplace de servicios | n/a | Cotizador |
| 13 | `enfermerasatodahora.com/inyectables-a-domicilio/` | PE | **Local Service Page** | alta | 2.000+ clientes, 5+ años, 30+ profesionales, logo MINSA, 6 fotos, testimonios, 4 FAQ, form + 24/7 |
| 14 | `enfermerosgabriel.com/ciudades/cdmx/inyecciones/` | MX | **Local Service Page escalada por ciudad** | muy alta (~2.000 pal.) | Tabla de precios ($490/$790 MXN), 16 alcaldías + colonias, 9 FAQ, NOM-022-SSA3-2012, OMS |
| 15 | `inyeccionesadomicilio.com` (CDMX) | MX | Local Service Page (EMD) | media | EMD exacto |
| 16 | `facebook.com/inyecciones.a.domicilio.CDMX` | MX | Perfil social | n/a | Entidad social |
| 17 | `health-athome.com/procedimientos/`, `apusalud.com`, `serviciosaunclick.com` | PE | Local Service Page | media-alta | 24/7, cotización por WhatsApp |

### 2.2 Consenso del SERP

| Page-type | Cuota aprox. | Lectura |
|---|---|---|
| **Local Service Page (propiedad del prestador)** | **~70 %** | **Formato dominante y objetivo** |
| Directorio / marketplace / clasificados (Yapo, Evisos, Doctoralia, Cronoshare, Milanuncios) | ~25 % | Ocupan hueco donde no hay oferta local optimizada |
| Perfil social (Facebook) | ~5 % | Entidad, no landing |
| **Blog Post** | **0 %** | Google **no** premia contenido informativo aquí |
| **Sitio corporativo de clínica / hospital** | **~0 %** | Las clínicas grandes **no** rankean para esta consulta |
| Product Page / Comparison Page | 0 % | Intención no comercial-e-commerce |

**Conclusión dura:**
- Google **no premia** artículos de blog médicos, ni webs institucionales de clínicas, ni páginas educativas sobre "cómo poner una inyección". Kaiser, Hartford Healthcare y similares aparecen sólo para consultas informativas puras ("preguntas frecuentes sobre autoadministración"), nunca para la consulta transaccional local.
- Google **sí premia**: (a) landings de servicio de PYMES locales con señales de entidad, (b) directorios cuando la oferta local es débil.
- El **local pack + GBP** es el activo #1. Draska es la prueba: 567 palabras, 1 imagen y sección de reseñas vacía, y aun así rankea con GBP vinculada.

### 2.3 Features del SERP observadas / inferidas

| Feature | Estado | Evidencia |
|---|---|---|
| Local pack / mapa | **Muy probable** (no verificable con esta herramienta) | Place ID en `sameAs` de Draska; predominio de agregadores locales; competidores estructurados como fichas |
| "Cerca de mí" como modificador | **Confirmado** | URLs y H1 competidores: `inyecciones-a-domicilio-cerca-de-mi/`, FAQ "¿Necesito inyecciones a domicilio cerca de mi?" |
| PAA (temas recurrentes) | **Confirmado por proxy** (FAQ replicadas en 4 competidores) | ¿Necesito receta? · ¿Cuánto cuesta? · ¿Incluye insumos/medicamento? · ¿Es seguro? · ¿Atienden 24 horas? · ¿Qué comunas/distritos cubren? · ¿Aplican antibióticos? · ¿Aceptan Fonasa/Isapre? |
| Modificador precio | **Confirmado** | Rango CL $5.000–$50.000; MX desde $450–$790; consultas "cuánto cuesta" con volumen propio |
| Modificador urgencia | **Confirmado** | "24 horas", "24/7", "rápido y seguro", "enfermero asignado en 15 minutos" |
| Anuncios | Baja densidad, presencia de marketplaces | Cronoshare/Doctoralia compran esta demanda |
| Featured snippet | Ausente en la consulta transaccional | Oportunidad: FAQ estructurada + tabla de precios |

---

## 3. User stories derivadas de señales del SERP

Formato de `user-story-framework.md`. Cada historia cita la señal observada.

**US-1 — Usuaria de anticonceptivo inyectable mensual (decisión, recurrente)**
> Como **mujer con anticonceptivo inyectable mensual**, quiero **agendar mi pinchazo en la fecha exacta sin ir al consultorio**, porque **si me atraso pierdo cobertura anticonceptiva y eso me genera ansiedad real**, pero me bloquea **no saber el precio ni si puedo reservar la misma fecha todos los meses**.
> *Señal: H3 "ANTICONCEPTIVOS INYECTABLES MENSUALES" en Draska; "inyección anticonceptiva" listada en mdcare.cl y enfermerosgabriel.com; PAA-proxy "¿cuánto cuesta?".*
> **Barrera:** sensibilidad al precio + falta de recurrencia agendable.

**US-2 — Cuidador/a de adulto mayor con movilidad reducida (consideración)**
> Como **hijo/a que cuida a un adulto mayor postrado**, quiero **un profesional acreditado que venga a casa hoy**, porque **trasladar a mi papá a un consultorio es doloroso y arriesgado**, pero me bloquea **no saber si son enfermeros reales o improvisados**.
> *Señal: enfermera.io — "personas con movilidad reducida, adultos mayores o pacientes debilitados"; enlaces internos "Cuidado del Adulto Mayor" en enfermerasatodahora.com; Clinical Plus con "enfermería post-operatoria".*
> **Barrera:** brecha de confianza (credenciales).

**US-3 — Paciente con indicación médica urgente (decisión, alta intención)**
> Como **paciente que salió del médico con una receta de antibiótico IM para hoy**, quiero **que alguien llegue en menos de una hora**, porque **la dosis tiene horario**, pero me bloquea **no saber si atienden ahora ni cuánto demoran en llegar**.
> *Señal: "24 horas"/"24/7" en 5 competidores (enfermerasatodahora, serviciosaunclick, health-athome, medplussalud, Clinical Plus); "enfermero asignado en 15 minutos" (medplussalud); "Atención 7:00 a.m. a 10:00 p.m." (enfermerosgabriel).*
> **Barrera:** presión de tiempo — la página no promete SLA.

**US-4 — Comparador de precio (consideración)**
> Como **persona sin previsión o con presupuesto ajustado**, quiero **saber cuánto cuesta antes de escribir**, porque **no quiero exponerme a un cobro sorpresa en mi casa**, pero me bloquea **que casi nadie publica precio y el rango va de $5.000 a $50.000**.
> *Señal: consultas "precio"/"cuánto cuesta" con resultados dedicados (cronoshare "¿Cuánto cobra una enfermera a domicilio? Precios 2026", enfermera.io/precios/); enfermerosgabriel publica tabla $490/$790 MXN; medplussalud "desde $50.000"; mdcare vende "Insumos Incluidos" como diferenciador de precio.*
> **Barrera:** opacidad de precio — **la mayor fricción de conversión del nicho**.

**US-5 — Escéptico de seguridad y legalidad (awareness → consideración)**
> Como **persona que nunca ha contratado esto**, quiero **verificar que es legal y seguro dejar entrar a alguien a inyectarme**, porque **he leído sobre infecciones y falsos profesionales**, pero me bloquea **no ver registro sanitario, nombre real ni reseñas verificables**.
> *Señal: "inscritos en la superintendencia de salud" (Draska), "Enfermeras Acreditadas Superintendencia de Salud" (mdcare), logo MINSA (Perú), cita a NOM-022-SSA3-2012 y a la OMS (México); PAA-proxy "¿es seguro?" y "¿necesito receta?".*
> **Barrera:** brecha de confianza — es una consulta **YMYL de salud**.

**US-6 — Verificador de cobertura de zona (decisión)**
> Como **residente de un barrio periférico**, quiero **confirmar que llegan a mi dirección**, porque **ya me han dicho "no cubrimos esa zona" después de explicar todo**, pero me bloquea **que la página sólo dice el nombre de la ciudad**.
> *Señal: los 4 competidores analizados listan zonas granulares — 33 comunas (medplussalud), 40+ comunas + Rancagua/Machalí (mdcare), 16 alcaldías + colonias + zona conurbada (enfermerosgabriel). Draska sólo dice "Áreas cubiertas: Calama".*
> **Barrera:** brecha de información geográfica.

Cobertura de journey: awareness (US-5), consideración (US-2, US-4, US-5), decisión (US-1, US-3, US-6). ✔

---

## 4. Scoring por persona — página de referencia (Draska)

### Fichas de persona (derivadas de §2 y §3)

1. **Ana, usuaria de anticonceptivo mensual** — decisión, recurrente, ansiedad por fecha. *Evidencia: H3 anticonceptivos + servicio listado por 3 competidores.*
2. **Carla, cuidadora de adulto mayor** — consideración, escéptica sobre credenciales. *Evidencia: copy de movilidad reducida + silos "adulto mayor".*
3. **Rodrigo, paciente con receta urgente** — decisión, presión de tiempo. *Evidencia: claims 24/7 y SLA de 15 min.*
4. **Paula, comparadora de precio** — consideración, sensible al costo. *Evidencia: SERP dedicado a precios + tablas de competidores.*
5. **Jorge, escéptico de seguridad (YMYL)** — awareness, desconfianza. *Evidencia: acreditaciones, normativas, PAA "¿es seguro?".*
6. **Nadia, verificadora de cobertura** — decisión, geográfica. *Evidencia: listados de comunas/alcaldías/distritos.*

### Tabla de puntuación

| Persona | Relevancia | Claridad | Confianza | Acción | Total | Rating |
|---|---|---|---|---|---|---|
| Ana — anticonceptivo mensual | 22/25 | 14/25 | 9/25 | 14/25 | **59/100** | Needs Work |
| Nadia — cobertura de zona | 15/25 | 13/25 | 10/25 | 12/25 | **50/100** | Needs Work |
| Jorge — escéptico seguridad | 14/25 | 12/25 | 11/25 | 12/25 | **49/100** | Needs Work |
| Rodrigo — urgencia hoy | 12/25 | 8/25 | 9/25 | 15/25 | **44/100** | Needs Work |
| Carla — cuidadora adulto mayor | 10/25 | 10/25 | 9/25 | 12/25 | **41/100** | Needs Work |
| **Paula — comparadora de precio** | **8/25** | **6/25** | **10/25** | **12/25** | **36/100** | **Critical Mismatch** |

**Evidencia concreta de los scores bajos:**
- Sección "Opiniones" del DOM **vacía**, con un único registro de texto `test` → la señal de prueba social no sólo falta, sino que **daña** la confianza si se renderiza.
- **1 sola imagen** en toda la página (favicon-tier), sin fotos del equipo ni del procedimiento.
- **Cero precios.** Peor: el copy dice "El servicio no incluye la venta de insumos y medicamentos" sin decir cuánto cuesta el servicio → refuerza la objeción de Paula sin resolverla.
- Sin horarios de atención visibles ni `openingHoursSpecification` en el schema → Rodrigo no puede saber si atienden ahora.
- "Áreas cubiertas: Calama" a secas, sin poblaciones ni radio → Nadia queda sin respuesta.
- Bloques en MAYÚSCULAS de párrafo completo ("LA NEUROBIONTA ES UNA SUSTANCIA COMPUESTA POR...") → penaliza legibilidad móvil.
- Contenido irrelevante para la conversión: párrafo sobre "5 millones de mujeres usan inyectables combinados… su uso se ha difundido en China, India" → contenido enciclopédico que **no** responde a ninguna user story.
- Enlace saliente a `www.sanivida.cl` como "más información" → fuga de tráfico a un tercero desde el cuerpo del texto.
- Email de contacto expuesto de tipo personal (`hectoremprendimiento9@gmail.com`) → señal de informalidad en un rubro YMYL.

**Persona más débil: Paula — comparadora de precio (36/100).**
**Fix recomendado:** insertar bajo el hero una tabla `Precios 2026` con 4 filas (Inyección IM $X.000 · Anticonceptivo mensual $X.000 · Multivitamínico/Neurobionta $X.000 · Control de signos vitales $X.000), fila "Recargo nocturno/festivo +$X.000" y línea "El valor no incluye el medicamento; puedes comprarlo en farmacia y nosotros lo aplicamos". Marcar con `Service` + `priceSpecification`.

**Problema sistémico (todas las personas): dimensión Confianza, 9–11/25.** Ninguna persona encuentra nombres reales, número de registro, fotos ni reseñas verificables. En un nicho YMYL de salud esto es el techo estructural del sitio.

---

## 5. SXO Gap Score — Draska (referencia)

> Este puntaje es **independiente** del SEO Health Score.

| Dimensión | Puntaje | Evidencia |
|---|---|---|
| **Page Type** (0-15) | **12** | Local Service Page correcta: `LocalBusiness` + NAP + geo + área cubierta + `tel:` + `wa.me`. Alineada con el 70 % del SERP. Le falta la capa `Service`. |
| **Content Depth** (0-15) | **4** | 567 palabras vs. 1.500–2.000 de medplussalud / enfermerosgabriel. Sin FAQ, sin precios, sin proceso, sin listado de zonas. Parte del contenido es relleno enciclopédico. |
| **UX Signals** (0-15) | **6** | WhatsApp y teléfono presentes (bien), pero: reseñas vacías con "test", MAYÚSCULAS en bloque, sin horarios, sin CTA repetido, sin sticky bar. Plantilla UENI difiere GTM correctamente (positivo en performance). |
| **Schema** (0-15) | **6** | Sólo `LocalBusiness` + `PostalAddress` + `GeoCoordinates` (539 bytes, válido). **Faltan:** `openingHoursSpecification`, `areaServed`, `Service`+`offers`, `FAQPage`, `aggregateRating`, subtipo `MedicalBusiness`/`HomeHealthCareService`. Positivo: `sameAs` con Place ID de GBP + Facebook. |
| **Media** (0-15) | **2** | 1 imagen total. Sin fotos de profesionales, sin foto del maletín/insumos, sin video, sin mapa embebido funcional. |
| **Authority** (0-15) | **5** | Subdominio de plataforma (`ueniweb.com`), sin dominio propio → cero equity acumulable y branding débil. Claim de Superintendencia de Salud sin número de registro. GBP vinculada (+), Facebook (+), enlace saliente a sanivida.cl (−). |
| **Freshness** (0-10) | **5** | `last-modified` reciente y `publication_date` 2026-04-11 detectada, pero sin fechas visibles al usuario ni señales de actualización de precios/servicios. |
| **SXO GAP SCORE** | **40/100** | **Needs Work** — rankea por entidad local en mercado de baja competencia, no por calidad de experiencia. |

**Lectura estratégica:** Draska es un techo bajo disfrazado de éxito. Su posición es defendible sólo mientras nadie publique en Calama una Local Service Page completa. Un sitio nuevo con la estructura de §6 la desplaza en 2–4 meses.

---

## 6. Recomendación de page-type y arquitectura para un sitio NUEVO

### 6.1 Page-type objetivo

**Local Service Page** = híbrido tipo 7 (Local) + tipo 5 (Service), con capa transaccional de WhatsApp.

No construir: blog médico como activo principal, home corporativa genérica, ni página multi-servicio sin ciudad. El SERP demuestra que ninguno de esos formatos ocupa posiciones comerciales.

### 6.2 Arquitectura de URLs replicable a N ciudades

Modelo validado por `enfermerosgabriel.com` (México, escalado a 7+ ciudades) y `especialistaenheridas.cl` (Chile, Antofagasta + La Serena/Coquimbo):

```
/                                            → Home = landing nacional del servicio principal
/inyecciones-a-domicilio/                    → Pilar de servicio (nacional)
/inyecciones-a-domicilio/calama/             → ★ Página dinero: servicio × ciudad
/inyecciones-a-domicilio/antofagasta/
/inyecciones-a-domicilio/iquique/
/enfermeria-a-domicilio/calama/              → Servicio hermano × misma ciudad
/servicios/anticonceptivo-inyectable/calama/ → Long tail de alta conversión (US-1)
/servicios/neurobionta-multivitaminico/calama/
/precios/                                    → Captura de "cuánto cuesta" (US-4)
/nosotros/                                   → E-E-A-T: nombres, registros, fotos
/blog/                                       → Soporte, NO activo principal
```

Reglas:
- **Dominio propio**, nunca subdominio de plataforma. Los EMD parciales funcionan bien en este nicho (`inyeccionesadomicilio.cl`, `inyeccionessantiago.cl` rankean), pero prioriza marca + palabra: p.ej. `enfermeriaencasa.cl`.
- **Una GBP por ciudad**, configurada como *service area business* (sin dirección visible, con radio de cobertura). Es el activo #1 del nicho.
- **Contenido único por ciudad obligatorio**: nombres reales de barrios/poblaciones, precios locales, nombre del profesional que atiende esa ciudad, reseñas de esa ciudad. Sin esto, Google lo trata como doorway pages y el escalado se cae entero.
- Meta title patrón: `Inyecciones a Domicilio en [Ciudad] | Enfermería 24h — [Marca]`
- Meta description patrón: `Enfermeros/as inscritos en [autoridad sanitaria]. Llegamos a tu casa en [Ciudad] en menos de [X] min. Desde $[precio]. Agenda por WhatsApp.`

### 6.3 Estructura de la landing (mobile-first, 375 px)

#### ABOVE THE FOLD (primeros ~600 px — todo esto debe verse sin scroll)

| Orden | Elemento | Contenido concreto |
|---|---|---|
| 1 | Barra sticky superior | Logo (izq) + botón verde **"WhatsApp"** (der) — visible en todo el scroll |
| 2 | **H1** | `Inyecciones a domicilio en Calama` |
| 3 | Subtítulo | `Enfermería a domicilio. Llegamos a tu casa en menos de 60 minutos.` |
| 4 | **3 chips de prueba** (fila horizontal, iconos) | `✔ Inscritos en Superintendencia de Salud` · `⏱ Llegamos en 60 min` · `💲 Desde $12.000` |
| 5 | **CTA primario** | Botón verde ancho completo: **"Pedir hora por WhatsApp"** → `https://wa.me/569XXXXXXXX?text=Hola%2C%20necesito%20una%20inyecci%C3%B3n%20a%20domicilio%20en%20Calama` (mensaje precargado, reduce fricción a un tap) |
| 6 | **CTA secundario** | Botón outline: **"Llamar ahora +56 9 XXXX XXXX"** → `tel:` |
| 7 | Línea de micro-confianza | `★ 4,9 · 37 reseñas en Google · Atención todos los días 08:00–22:00` |

> Regla dura: **precio + tiempo de llegada + acreditación + WhatsApp deben estar visibles sin scroll.** Son las cuatro barreras de US-1 a US-6 resueltas en la primera pantalla.

#### ORDEN DE SECCIONES (post-fold)

| # | Sección | Qué contiene | User story que resuelve |
|---|---|---|---|
| 1 | **Precios transparentes** | Tabla: Inyección IM/SC $12.000 · Anticonceptivo mensual $12.000 · Neurobionta/multivitamínico $14.000 · Suero/EV $25.000 · Control de signos vitales $10.000. Nota: *"El valor cubre la administración; el medicamento lo compras tú en farmacia."* + `Recargo nocturno (22:00–08:00) +$5.000` | **US-4** (persona más débil → va primero) |
| 2 | **Qué incluye / Requisitos** | Dos columnas ✔/✘: incluye jeringa, aguja, algodón, alcohol, guantes estériles, desecho de corto-punzantes / no incluye el medicamento. Requisito: **receta médica vigente** (foto por WhatsApp basta) | US-4, US-5 |
| 3 | **Servicios** (cards con icono) | Anticonceptivo inyectable mensual · Multivitamínico (Neurobionta) · Antibiótico IM · Insulina/anticoagulante · Control de signos vitales · Curaciones simples · Toma de muestras. Cada card enlaza a su URL long-tail | US-1, US-2 |
| 4 | **Cómo funciona — 3 pasos** | 1) Escríbenos por WhatsApp con tu receta · 2) Confirmamos hora y dirección · 3) Llegamos y aplicamos. Con tiempos: *"Respuesta en menos de 5 minutos"* | US-3 |
| 5 | **Zonas de cobertura en Calama** | Lista granular de 15–25 sectores reales (Villa Ayquina, Kamac Mayu, Villa Alemania, Sector Norte, Chuquicamata, Las Vegas, Río Loa, Balmaceda…) + mapa con radio + línea *"¿No ves tu sector? Escríbenos igual"* | **US-6** |
| 6 | **Quiénes te atienden** (E-E-A-T) | Foto real, nombre completo, título (TENS / Enfermero/a Universitario/a), **número de registro en Superintendencia de Salud**, años de experiencia | **US-5, US-2** |
| 7 | **Reseñas reales** | Widget de Google Reviews con nombre y sector del reseñador (`María, Villa Ayquina`). Mínimo 5 visibles. **Nunca placeholders** | US-5 |
| 8 | **Preguntas frecuentes** (acordeón, 8–10) | ¿Necesito receta médica? · ¿Cuánto cuesta? · ¿Incluye el medicamento? · ¿Es seguro? · ¿Atienden de noche/fines de semana? · ¿Cuánto demoran en llegar? · ¿Qué sectores de Calama cubren? · ¿Aplican antibióticos? · ¿Aceptan Fonasa/Isapre? · ¿Puedo agendar todos los meses la misma fecha? | US-1 a US-6 + captura de PAA |
| 9 | **CTA final + formulario corto** | Repite el botón WhatsApp + formulario de 4 campos (Nombre · WhatsApp · Servicio · Dirección). Sin campos opcionales | Todas |
| 10 | **Footer NAP + enlaces** | Nombre, teléfono, correo con dominio propio (`contacto@dominio.cl`), horarios, enlaces a otras ciudades y servicios, aviso legal | Consistencia NAP |

#### Señales de confianza obligatorias (checklist YMYL)

- [ ] Nombre completo + credencial + **número de registro sanitario** de cada profesional
- [ ] Foto real del equipo (no stock)
- [ ] Reseñas de Google embebidas y actualizadas
- [ ] Horarios explícitos + estado "abierto ahora"
- [ ] Política de insumos estériles y desecho de corto-punzantes
- [ ] Exigencia de receta médica declarada de forma visible (protege y da autoridad)
- [ ] Correo con dominio propio (no Gmail personal)
- [ ] Convenios/reembolsos si aplican (Fonasa, Isapres, seguros)
- [ ] Página `/nosotros/` con historia y años de operación

#### Stack de schema recomendado

```
MedicalBusiness (o HomeHealthCareService)
├── name, url, telephone, email, image[], logo
├── address (PostalAddress) + geo (GeoCoordinates)
├── areaServed: [City "Calama", + Place por cada sector]
├── openingHoursSpecification (7 días, con horas reales)
├── priceRange
├── sameAs: [GBP Place ID, Facebook, Instagram]
├── aggregateRating (SOLO si hay reseñas reales verificables)
└── hasOfferCatalog → OfferCatalog
    └── Service (× cada servicio)
        ├── name, description, serviceType, provider
        ├── areaServed
        └── offers → Offer + priceSpecification (price, priceCurrency CLP)
FAQPage (con las 8–10 preguntas del bloque 8)
Person (× cada profesional: name, jobTitle, hasCredential)
BreadcrumbList
```

---

## 7. Wireframes IST / SOLL

### IST — https://draska.ueniweb.com/

```
IST: draska.ueniweb.com
├── ABOVE FOLD
│   ├── H1: "INYECCIÓN A DOMICILIO CALAMA"  (todo en mayúsculas)
│   ├── H2: "ENFERMERÍA A DOMICILIO CALAMA"
│   └── [sin precio · sin horario · sin CTA visible garantizado · sin prueba social]
├── MAIN CONTENT (567 palabras totales)
│   ├── H3 "¿QUIENES SOMOS?" — TENS inscritos en Superintendencia, lista de 3 servicios,
│   │   disclaimer de insumos, requisito de receta, enlace saliente a sanivida.cl (~150 pal.)
│   ├── H3 "ANTICONCEPTIVOS INYECTABLES MENSUALES" — contenido enciclopédico
│   │   ("5 millones de mujeres… China, India") (~120 pal.)  ← relleno, no convierte
│   └── H3 "INYECCIÓN DE MULTIVITAMINICO" — párrafo en MAYÚSCULAS sobre B1/B6/B12 (~60 pal.)
├── SUPPORTING
│   ├── H2 "Servicios" → 1 ítem: "Enfermería a domicilio"
│   ├── H2 "Facilidades" → sin contenido útil
│   ├── H2 "Opiniones"  → VACÍA (único registro: "test")   ← daña la confianza
│   ├── H2 "Enviar Mensaje" → "Responderemos lo antes posible"  (sin SLA)
│   ├── H2 "Áreas cubiertas" → "Calama"  (una palabra)
│   └── H3 "CONTACTO" → tel:+56978833741 · wa.me/56978833741 · gmail personal
└── FOOTER — compartir por email, marca UENI

Media: 1 imagen · Schema: LocalBusiness/PostalAddress/GeoCoordinates (539 B)

Ausente respecto de lo que el SERP espera:
- Tabla de precios       → el 100 % de los competidores fuertes la tiene o da "desde $"
- FAQ + FAQPage schema   → 4 de 4 competidores analizados la tienen
- Listado de zonas       → competidores listan 16–40 comunas/alcaldías
- Reseñas reales         → medplussalud: 300+ reseñas 4,9★
- Horarios + "abierto ahora" → mdcare y enfermerosgabriel los publican
- Fotos del equipo       → enfermerasatodahora tiene galería de 6
- Proceso de 3 pasos     → medplussalud y enfermerosgabriel lo tienen
- Credencial verificable → nº de registro sanitario, no sólo el claim
```

### SOLL — Local Service Page para sitio nuevo

```html
<header>  <!-- sticky, 56px -->
  Logo | Botón verde "WhatsApp"
</header>

<section class="hero">  <!-- ABOVE FOLD, ≤600px móvil -->
  H1: "Inyecciones a domicilio en Calama"
  Sub: "Enfermería a domicilio. Llegamos a tu casa en menos de 60 minutos."
  Chips: [✔ Superintendencia de Salud] [⏱ 60 min] [💲 Desde $12.000]
  CTA-1: "Pedir hora por WhatsApp"  → wa.me/…?text=Hola, necesito una inyección a domicilio en Calama
  CTA-2: "Llamar +56 9 XXXX XXXX"   → tel:
  Trust: "★ 4,9 · 37 reseñas en Google · Todos los días 08:00–22:00"
</section>

<section id="precios">   <!-- resuelve la persona más débil, va primero -->
  H2: "Precios 2026 — sin sorpresas"
  Tabla 5 filas + nota de insumos + recargo nocturno
  CTA inline: "Consultar mi caso por WhatsApp"
</section>

<section id="incluye">
  H2: "Qué incluye y qué necesitas"  → dos columnas ✔ / ✘ + requisito de receta
</section>

<section id="servicios">
  H2: "Servicios de enfermería a domicilio en Calama"
  7 cards con enlace a URL long-tail propia
</section>

<section id="como-funciona">
  H2: "Cómo funciona — en 3 pasos"  → 1) Escribe  2) Confirmamos  3) Llegamos
  Micro-copy: "Respondemos en menos de 5 minutos"
</section>

<section id="cobertura">
  H2: "Sectores de Calama donde atendemos"
  Lista de 15–25 sectores reales + mapa + "¿No ves tu sector? Escríbenos igual"
</section>

<section id="equipo">   <!-- E-E-A-T -->
  H2: "Quién te va a atender"
  Foto real + nombre + título + Nº registro Superintendencia + años de experiencia
</section>

<section id="resenas">
  H2: "Lo que dicen nuestros pacientes en Calama"
  Widget Google Reviews, 5+ visibles, con nombre y sector
</section>

<section id="faq">
  H2: "Preguntas frecuentes"  → acordeón de 8–10 · marcado FAQPage
</section>

<section class="final-cta">
  H2: "Agenda tu inyección a domicilio hoy"
  Botón WhatsApp + formulario de 4 campos (Nombre · WhatsApp · Servicio · Dirección)
</section>

<footer>
  NAP completo · horarios · contacto@dominio.cl ·
  Otras ciudades: Antofagasta | Iquique | Tocopilla ·
  Otros servicios: Curaciones | Suero | Toma de muestras
</footer>

<!-- CTA flotante WhatsApp, esquina inf. derecha, visible en todo el scroll -->
```

---

## 8. Prioridades de acción

### Para el sitio de referencia (Draska), en orden de impacto

1. **Migrar a dominio propio** y redirigir 301 desde el subdominio UENI. Sin esto, todo lo demás tiene techo. *(Authority 5/15)*
2. **Publicar precios** en tabla, arriba del pliegue. Ataca la persona más débil (36/100). *(Content Depth, US-4)*
3. **Eliminar la reseña "test" y conectar reseñas reales de Google.** Una sección de reseñas vacía es peor que no tenerla. *(Trust, sistémico)*
4. **Añadir bloque de equipo** con nombre, foto y número de registro de la Superintendencia. *(YMYL, US-5)*
5. **Sustituir el relleno enciclopédico** (China/India, párrafos en mayúsculas) por FAQ de 8–10 preguntas con `FAQPage`. *(Content Depth + captura PAA)*
6. **Expandir "Áreas cubiertas"** de "Calama" a 15–25 sectores nombrados. *(US-6)*
7. **Añadir `openingHoursSpecification`, `areaServed`, `Service`+`offers` y subtipo `MedicalBusiness`** al schema. *(Schema 6/15)*
8. **Añadir 6–10 imágenes reales** (equipo, maletín, insumos estériles, atención). *(Media 2/15)*
9. **Botón WhatsApp flotante persistente** con mensaje precargado. *(Action)*
10. **Reemplazar el Gmail personal** por correo con dominio propio y quitar el enlace saliente a sanivida.cl del cuerpo. *(Trust)*

### Para un sitio nuevo (orden de construcción)

1. GBP por ciudad como *service area business* + primeras 10 reseñas reales (esto solo ya compite con Draska)
2. Dominio propio + una Local Service Page completa por ciudad según §6.3
3. Schema stack de §6.3
4. Long-tail por servicio (`/servicios/anticonceptivo-inyectable/[ciudad]/`) — alta intención, baja competencia
5. Página `/precios/` para capturar "cuánto cuesta"
6. Citations locales: Yapo, Evisos, Doctoralia, Cronoshare, Facebook — el SERP muestra que estos directorios rankean; estar en ellos captura la demanda que no llega al sitio
7. Blog **sólo** como soporte de autoridad temática, nunca como página dinero

---

## 9. Limitaciones del análisis

- **Local pack no verificable directamente.** La herramienta WebSearch devuelve resultados orgánicos, no el mapa. Su presencia se infiere (con alta confianza) del Place ID en el `sameAs` de Draska, del predominio de agregadores locales y del modificador "cerca de mí" en URLs y FAQ de competidores. **Verificar manualmente** en Google con geolocalización en Calama.
- **PAA y AI Overview no observados directamente.** Los temas de PAA se reconstruyeron por proxy a partir de las FAQ replicadas en 4 competidores independientes de 3 países — método robusto, pero no equivale a leer la caja PAA real.
- **Posiciones exactas no disponibles.** Se analizó composición y tipología del SERP, no ranking numérico. No hay datos de volumen de búsqueda ni de dificultad de keyword.
- **`especialistaenheridas.cl` devolvió 404/contenido vacío** en el fetch estructural; se clasificó por su título y patrón de URL.
- **`inyeccionessantiago.cl` no resolvió DNS** en el momento del análisis (`ENOTFOUND`); se clasificó por título de SERP.
- **Métricas de rendimiento y Core Web Vitals no medidas** (sin CrUX/PSI en esta ejecución). La plantilla UENI difiere GTM correctamente, lo que sugiere un baseline aceptable, pero no está confirmado.
- **Precios locales de Calama no verificados.** Los rangos citados provienen de proveedores de Santiago, Lima y CDMX; los importes del wireframe son ilustrativos y deben ajustarse al mercado real.
- **Reseñas y GBP de Draska no auditadas** (número, puntuación, frecuencia). Requiere revisión manual de la ficha.

---

## 10. Referencias cruzadas

| Hallazgo | Skill recomendada |
|---|---|
| Brechas E-E-A-T severas en nicho YMYL de salud (sin autor, sin credenciales verificables, sin reseñas) | `/seo content` |
| Faltan `Service`, `FAQPage`, `openingHoursSpecification`, `areaServed`, `aggregateRating`, subtipo `MedicalBusiness` | `/seo schema` |
| Intención local dominante; GBP es el activo #1 del nicho; una ficha por ciudad como *service area business* | `/seo local` |
| Contenido delgado (567 palabras) con relleno no convertidor | `/seo page` |

---

*¿Quieres un informe en PDF? Usa `/seo google report`.*

**Fuentes SERP consultadas:** [medplussalud.cl](https://medplussalud.cl/inyecciones-a-domicilio/) · [mdcare.cl](https://mdcare.cl/inyecciones-a-domicilio/) · [enfermerasatodahora.com](https://enfermerasatodahora.com/inyectables-a-domicilio/) · [enfermerosgabriel.com](https://www.enfermerosgabriel.com/ciudades/cdmx/inyecciones/) · [enfermeriatucasa.cl](https://enfermeriatucasa.cl/) · [especialistaenheridas.cl](https://especialistaenheridas.cl/enfermera-inyecciones-vacunas-domicilio-antofagasta) · [doctoralia.cl](https://www.doctoralia.cl/enfermero/antofagasta) · [cronoshare.cl](https://www.cronoshare.cl/servicios/enfermeria-a-domicilio/region-de-antofagasta/antofagasta) · [yapo.cl](https://www.yapo.cl/paginas/servicios/inyecciones-a-domicilio) · [enfermera.io](https://enfermera.io/servicios-enfermeria-a-domicilio/inyecciones-a-domicilio/) · [draska.ueniweb.com](https://draska.ueniweb.com/)
