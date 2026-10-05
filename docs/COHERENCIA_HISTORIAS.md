# Coherencia de las historias de usuario — Brújula IA Regional (Grupo 02)

**Fecha:** 5 de octubre de 2026. **Tipo de documento:** auditoría independiente; todo lo que aquí se recomienda es **propuesta para validar por el equipo, no un acuerdo**.

**Fuentes leídas:** `README.md`; `chat-wsp/G2 proyectos en tecnología/ANALISIS_CHAT_PROYECTO.md`; `.github/ISSUE_TEMPLATE/user-story-template.md`; y de `docs/PROMPT_AGENTES_BRUJULA_IA.md` solo las secciones de datos y de descarga. No abrí los archivos de datos: los hechos sobre datos se toman de ese documento, no los verifiqué de nuevo.

**Convención:** «el chat dice» remite al análisis del chat; «propongo» es elaboración mía. IDs: R1–R4 son las historias del README; M-, F- y D- son los IDs provisionales del análisis del chat; P- son los que propongo.

## 1. Veredicto general

El backlog no es coherente todavía, pero el problema es acotado: hay **dos productos distintos mezclados**. Uno es una herramienta analítica para el Ministerio (paquete de Mathias, M-HU01 a M-HU06), bien redactada y comprobable; el otro es el programa de cofinanciamiento visto por sus beneficiarios (estudiante, docente, empresa), que ninguna herramienta de análisis puede entregar. El README declara un MVP de ranking **región × carrera × institución**, pero la única historia con criterios que construye un ranking lo hace sobre **carrera × sector en una región piloto**, y dos de las cuatro historias del README son de empresa, que no es destinataria del MVP. Con los datos del repositorio hoy solo se puede cumplir la parte de oferta (titulados y sedes); todo lo que dependa de demanda, vocación productiva o complementariedad con IA está bloqueado por fuentes externas sin verificar. Ninguna historia cubre la «visualización por región» ni el «reporte con recomendaciones» que el MVP promete.

## 2. Evaluación por historia

Veredictos posibles: coherente / coherente con ajustes / fuera del MVP / no verificable. «Datos»: **hoy** (se cumple con el repositorio), **externa** (depende de fuentes no verificadas), **no analítica** (una herramienta de análisis no puede cumplirla).

### 2.1 Las cuatro historias del README

| ID | Cita | Veredicto | Datos | Problema principal | Ajuste propuesto |
|---|---|---|---|---|---|
| R1 (= F-H05) | «quiero saber dónde focalizar los recursos disponibles» | Coherente con ajustes | Externa | Es una épica, no una historia: no dice qué se ordena ni con qué criterio. Su «para» («que la inversión pública llegue donde más ayuda») es un resultado de política, no comprobable al cerrar un sprint. | Convertirla en la historia de ranking (P-HU04) con la unidad del MVP explícita y un «para» de decisión: «para decidir los focos de la convocatoria». |
| R2 (= F-H06) | «entender qué problemas de los sectores productivos pueden abordar los estudiantes de cada carrera» | Coherente con ajustes | Externa | No hay datos de «problemas» ni de «estudiantes»: hay titulados históricos. «Entender» no es comprobable. Se solapa con M-HU03. | Fundirla con M-HU03: vínculo área de formación × sector, etiquetado como propuesta y no como desafío confirmado (P-HU03). |
| R3 (= F-H09) | «quiero probar mejoras con IA y automatización con costo y riesgo acotados» | Fuera del MVP | No analítica | Describe un beneficio del programa, no algo que se sepa, analice o prediga. No hay datos de empresas ni de desafíos. | Sacarla del backlog y llevarla a la visión como beneficio esperado del programa. |
| R4 (= F-H10) | «saber qué talento se forma cerca de mí y en qué áreas» | Coherente con ajustes | Hoy | Es, paradójicamente, la más factible con los datos (titulados + ubicación de sedes), pero su usuario es la empresa y el MVP entrega un reporte «para el Ministerio». | Conservar la capacidad (mapa de oferta por territorio) cambiando el usuario a analista del Ministerio (P-HU01 y P-HU06); la vista para empresas queda fuera. |

### 2.2 Paquete revisado de Mathias (M-HU01 a M-HU07, v2)

| ID | Cita | Veredicto | Datos | Problema principal | Ajuste propuesto |
|---|---|---|---|---|---|
| M-HU01 | «consultar los titulados por carrera e institución en la región piloto» | Coherente con ajustes | Hoy | «Carrera» es ambiguo (5.598 nombres frente a 285 áreas genéricas); «periodo» supone serie y el repositorio solo trae 2025; no dice qué niveles conducen a tesis ni qué hacer con la modalidad no presencial. | Fijar área genérica como «carrera», declarar niveles incluidos, tratar no presencial y no limitar a una región (el dato cubre las 16). |
| M-HU02 | «consultar las prioridades productivas y las necesidades de competencias documentadas» | Coherente con ajustes | Externa | Todo su contenido depende de fuentes que nadie ha verificado. Es la historia que desbloquea a M-HU03 y M-HU04, pero está planificada como una más. | Tratarla como investigación con decisión de salida (seguir / ranking solo de oferta) y hacerla primera, no quinta. |
| M-HU03 | «consultar relaciones justificadas entre carreras y necesidades sectoriales» | Coherente con ajustes | Externa | Buen criterio de contraste con revisión manual, pero sin tamaño de muestra ni umbral: no se puede declarar terminada. «Habilidades complementarias a la IA» no tiene fuente. | Fijar muestra, métrica y umbral antes de calcular; declarar la fuente del indicador de IA o marcarlo «sin evidencia». |
| M-HU04 | «ranking de combinaciones de carrera y sector en la región piloto» | Coherente con ajustes | Externa | Contradice la unidad del MVP: omite región e institución. Sus criterios de aceptación son los mejores del backlog. | Decidir la unidad (ver §3, n.º 1) y reescribir el enunciado conservando los criterios. |
| M-HU05 | «revisar la evidencia y el cálculo detrás de una recomendación» | Coherente | Depende de M-HU04 | No es independiente: sin ranking no existe. Encaja bien con la exigencia de reproducibilidad del curso. | Mantenerla o absorberla como criterio de trazabilidad del ranking. |
| M-HU06 | «ajustar los pesos de los criterios para comprobar qué recomendaciones se mantienen» | Coherente | Depende de M-HU04 | Redactada como función («ajustar») y no como pregunta analítica. Daniel la puso segunda en prioridad aunque es la última en poder construirse. | Reformular: «quiero saber qué tan estable es el ranking ante cambios de pesos». |
| M-HU07 | «consultar las condiciones de ejecución conocidas y pendientes» (opcional) | Fuera del MVP | No analítica | Tutoría, contraparte y plazo no están en ninguna fuente: sería un registro manual, es decir, gestión del programa. | Dejarla fuera; conservar solo su regla («la falta de información no es inviabilidad») como criterio del ranking. |

### 2.3 Demás historias de Feña y Daniel, agrupadas por usuario

| Usuario | Historias | Veredicto | Problema principal | Ajuste propuesto |
|---|---|---|---|---|
| Ministerio | F-H02: «ranking de regiones, carreras e instituciones prioritarias» | Coherente con ajustes | Es la única que coincide literalmente con la unidad del MVP, pero no tiene criterios y Daniel la puso séptima de diez. Dato: externa. | Usarla como enunciado del ranking y heredar los criterios de M-HU04. |
| Ministerio | F-H01: «respaldo de que el programa tiene factibilidad de aplicación» | No verificable | «Proyección segura y confiable» no tiene definición observable. | Descartarla como historia; lo comprobable ya está en M-HU05 y M-HU06. |
| Estudiante | F-H03, D-H01, F-H07 | Fuera del MVP | Son beneficios del programa («titularme a tiempo», «financiamiento directo»). No hay datos de estudiantes actuales, gratuidad ni desafíos. No analítica. | Mover a la visión como beneficiario; no son usuarios de la herramienta. |
| Docente o tutor | M-HT01, D-H02, F-H08 | Fuera del MVP | M-HT01 y D-H02 piden un resultado («que las tesis se vinculen a desafíos reales») y no un análisis. F-H08 sí es analítica, pero es M-HU03 vista por otro usuario. | Fuera; F-H08 puede quedar como vista futura de P-HU03. |
| Empresa | F-H04: «acceder a talento y soluciones de IA […] sin asumir todo el costo» | Fuera del MVP | Igual que R3: beneficio del programa. No analítica. | Mover a la visión. |

## 3. Incoherencias entre historias, de la que más bloquea a la que menos

1. **Unidad del ranking.** El MVP del README dice «región × carrera × institución»; M-HU04 dice «carrera y sector en la región piloto»; F-H02 dice «regiones, carreras e instituciones». No son intercambiables: el primero responde *dónde y a quién* dirigir fondos, el segundo *qué temas* priorizar dentro de un territorio ya elegido. Mientras no se decida, no se puede cerrar ningún criterio del ranking.
2. **Alcance geográfico.** Cuatro historias de Mathias fijan «región piloto» (elegida antes y fuera del producto); la visión del README habla de «todo el país» y de comparar regiones. Una región piloto vuelve imposible un ranking que incluya la dimensión región.
3. **El núcleo del producto depende de datos que no existen en el repositorio.** M-HU02, M-HU03, M-HU04 y R1/R2 necesitan demanda, vocación productiva y complementariedad con IA. Ninguna historia tiene como objetivo conseguir y validar esas fuentes, ni hay un plan si no aparecen. La plantilla del curso exige fuentes «identificadas, documentadas y validadas».
4. **Las historias del README no son las que el equipo priorizó.** Las cuatro del README (F-H05, F-H06, F-H09, F-H10) se escribieron después del ranking de diez de Daniel y no figuran en él; los seis primeros lugares de ese ranking (paquete de Mathias) no están en el README. El backlog visible y el backlog priorizado son conjuntos casi disjuntos.
5. **Prioridad contra dependencias.** Daniel ordena M-HU04 primero, M-HU06 segunda y M-HU01 sexta; Mathias planifica M-HU01 a M-HU03 en el primer sprint y M-HU04 a M-HU06 en el segundo. El orden de valor es defendible, pero el de construcción es el inverso. Además Daniel priorizó la v1 y Mathias publicó la v2 minutos después: el chat no dice cuál rige.
6. **Usuario.** El MVP tiene un destinatario (Ministerio, en dos roles: analista y responsable). En el chat hay cinco usuarios; tres de ellos (estudiante, docente, empresa) son beneficiarios del programa, no de la herramienta. El alcance que escribió Mathias («no evalúa postulaciones ni administra fondos») es incompatible con D-H01 o R3.
7. **Entregables del MVP sin historia.** «Visualización por región» y «reporte con recomendaciones» no aparecen en ninguna historia. M-HU05 (ficha de evidencia) es lo más cercano, y no es ni mapa ni reporte.
8. **«Carrera» e «institución» sin definir.** Ninguna historia dice si carrera es el nombre (5.598 valores) o el área genérica (285), ni si institución incluye IP y CFT (los datos sí los traen), ni qué niveles hacen tesis o memoria. La dimensión institución del MVP solo aparece como filtro en M-HU01.
9. **Qué se financia.** La visión del README habla de «subsidios públicos orientados al desarrollo de habilidades de IA»; el MVP y las historias, de cofinanciamiento de tesis. El chat ya registra la ambigüedad de «programa». Afecta qué titulados cuentan.
10. **Duplicados y solapes.** R1 = F-H05 ≈ F-H02 ≈ M-HU04; R2 = F-H06 ≈ M-HU03 ≈ F-H08; F-H03 ≈ D-H01 ≈ F-H07; M-HT01 ≈ D-H02; F-H04 se divide en F-H09 y F-H10; F-H01 ≈ M-HU05 + M-HU07. Hay unas ocho necesidades reales tras veintisiete textos.
11. **Promesas sin dato.** El README pone «especial énfasis en beneficiarios de gratuidad» y varias historias hablan de «estudiantes»; el repositorio no tiene gratuidad ni matrícula actual. Los criterios de M-HU01 ya lo advierten, pero los enunciados de R2 y del grupo de estudiantes lo contradicen.

## 4. Encaje con la plantilla y la Definition of Done del curso

La plantilla pide una historia analítica: «quiero [saber/aprender/predecir/analizar algo], para poder [lograr un objetivo de negocio o tomar una decisión]».

- **Encajan en el verbo:** R1, R2, R4, F-H02, F-H08 («saber», «entender») y el paquete de Mathias con «consultar», que es aceptable aunque describe una pantalla más que una pregunta.
- **No encajan:** R3 («probar»), M-HU06 («ajustar»), D-H01 («acceder a un financiamiento»), M-HT01 y D-H02 («que las tesis se vinculen…»). Son acciones o deseos, no preguntas analíticas.
- **El «para» falla en casi todas las de Feña y Daniel:** enuncian un efecto social (cerrar la brecha, titularse a tiempo, mejorar la productividad) que el producto no puede demostrar. El propio chat advierte que no se debe prometer impacto causal.

Contra la Definition of Done:

| Ítem del curso | Estado en el backlog actual |
|---|---|
| Hipótesis de negocio establecida | Ninguna historia la enuncia. Falta en todas. |
| Fuentes identificadas, documentadas y validadas | Solo cumplible hoy para oferta y sedes. Demanda e IA: sin fuente validada. |
| Limpieza reproducible | No aparece como criterio en ninguna historia; hay que añadirlo (unión titulados–sedes, normalización de comunas). |
| Resultados respaldados por código reproducible | M-HU05 lo cubre para el ranking («reconstruir el puntaje»). |
| Métricas del modelo o del análisis documentadas | Solo M-HU03 (contraste manual, sin umbral) y M-HU06 (cambios de posición). Faltan métricas definidas. |
| Conclusiones en formato accesible | Ninguna historia: falta el reporte y la visualización. |

## 5. Conjunto recomendado para el MVP (propuesta para validar)

**Supuestos de esta propuesta, que el equipo debe aceptar o cambiar:** usuario único Ministerio (analista y responsable); unidad del ranking región × área genérica × institución, como dice el README; el sector entra como atributo de la región y no como dimensión del ranking; alcance nacional para oferta, con evidencia de demanda tan amplia como las fuentes permitan. Si el equipo decide carrera × sector en región piloto, P-HU04 se reescribe y P-HU06 pierde el mapa comparativo.

Los números citados (filas, celdas, cobertura de la llave) provienen del documento de datos del repositorio.

**P-HU01 — Oferta de titulados.** Como analista del Ministerio, quiero saber cuántos titulados hay por región, área genérica, institución y nivel, para decidir qué combinaciones tienen masa suficiente para entrar en la convocatoria. *Proviene de:* M-HU01, R4/F-H10. *Datos:* hoy.
- La tabla agregada se genera con un script desde el archivo de titulados 2025 y sus totales cuadran con el total de filas de la fuente.
- Queda escrito qué niveles se incluyen como conducentes a tesis o memoria y cómo se trata la modalidad no presencial, con el número de títulos que cada regla excluye.
- Cada celda muestra volumen y un indicador normalizado (por ejemplo, cociente de especialización regional), de modo que la Región Metropolitana no domine solo por tamaño.
- No se publica ningún microdato y las celdas bajo un umbral mínimo acordado se agrupan o suprimen; se declara que son titulados históricos, no estudiantes disponibles.

**P-HU02 — Evidencia de demanda y vocación productiva.** Como analista del Ministerio, quiero saber qué evidencia pública existe sobre sectores prioritarios y demanda por región, para decidir qué criterios pueden entrar al ranking. *Proviene de:* M-HU02, parte de R2/F-H06. *Datos:* externa; es la historia que desbloquea el resto.
- Existe un inventario de fuentes candidatas con cobertura regional, nivel de detalle, fecha, licencia y forma de descarga, y cada una queda marcada como utilizable o descartada con su motivo.
- Para cada región y sector incluidos se muestra fuente y fecha, y se distingue prioridad estratégica declarada de demanda laboral observada.
- Donde no hay evidencia (en particular sobre necesidades de IA) se indica expresamente; nunca se rellena con supuestos.
- La historia cierra con una decisión registrada: ranking con criterios de demanda, o ranking solo de oferta declarado como tal.

**P-HU03 — Vínculo entre áreas de formación y sectores.** Como analista del Ministerio, quiero saber qué áreas de formación se relacionan con cada sector prioritario y con qué grado de complementariedad con IA, para proponer líneas temáticas de la convocatoria. *Proviene de:* M-HU03, R2/F-H06, F-H08. *Datos:* externa; depende de P-HU02.
- Cada vínculo muestra área, sector, línea temática y si es sugerencia automática o revisión del equipo.
- Antes de calcular se fijan el tamaño de la muestra de revisión manual, la métrica y el umbral de aceptación; el resultado obtenido se informa.
- Ningún vínculo se presenta como desafío empresarial confirmado.
- El indicador de complementariedad o exposición a IA declara fuente y nivel de agregación, o se marca «sin evidencia».

**P-HU04 — Ranking de focalización.** Como responsable del programa, quiero saber qué combinaciones región × área genérica × institución tienen mayor prioridad, para decidir los focos de la convocatoria de cofinanciamiento. *Proviene de:* R1/F-H05, F-H02, M-HU04, M-HU05. *Datos:* depende de P-HU01 a P-HU03.
- Cada combinación muestra posición, puntaje y contribución de cada criterio, y el puntaje se puede reconstruir desde los datos y las reglas publicadas.
- Están documentadas las reglas de cálculo, la normalización y el tratamiento de datos faltantes; la falta de información no se interpreta como baja prioridad.
- Las combinaciones con evidencia insuficiente se señalan según una definición escrita de «insuficiente».
- Se aclara que el ranking orienta la convocatoria y no selecciona tesis ni garantiza su calidad o impacto.

**P-HU05 — Estabilidad del ranking.** Como responsable del programa, quiero saber qué recomendaciones se mantienen al cambiar los pesos de los criterios, para decidir cuáles puedo defender con independencia de mis preferencias. *Proviene de:* M-HU06. *Datos:* depende de P-HU04.
- Se comparan al menos tres escenarios de pesos sobre los mismos datos, con un escenario base que se puede restablecer.
- Se informa una métrica de estabilidad (por ejemplo, correlación de rangos y entradas y salidas de las cinco primeras posiciones).
- Cada recomendación queda clasificada como robusta o sensible a los pesos según una regla escrita.

**P-HU06 — Visualización regional y reporte.** Como responsable del programa, quiero ver las prioridades por región y recibir un reporte con recomendaciones, para presentar y justificar los focos ante el Ministerio. *Proviene de:* MVP del README (sin historia hoy), R4/F-H10, M-HU05. *Datos:* la capa de oferta se cumple hoy; la de prioridades depende de P-HU04.
- Un mapa o vista por región muestra la oferta por sede, usando la unión titulados–sedes con su cobertura declarada.
- El reporte se genera desde el código, lista los focos recomendados con su evidencia y limitaciones, y cabe en un formato legible por alguien no técnico.
- Toda cifra del reporte indica fuente y fecha.

**Quedarían fuera del MVP en esta propuesta:** R3/F-H09, F-H04, F-H01, M-HU07 y todas las historias de estudiante y docente. No se descartan como ideas: describen a los beneficiarios del programa y pueden vivir en la visión.

**Orden sugerido:** P-HU01 y P-HU02 primero y en paralelo (P-HU02 es el mayor riesgo); la capa de oferta de P-HU06 puede mostrarse en el primer incremento. P-HU03, P-HU04, P-HU05 y el reporte, después. Las fechas de sprint citadas en el chat no están contrastadas con el syllabus.

## 6. Decisiones que el equipo debe tomar antes de aceptar el backlog

1. **Unidad del ranking:** región × carrera × institución (README) o carrera × sector dentro de una región (M-HU04). Define casi todo lo demás.
2. **Alcance geográfico:** una región piloto (¿cuál y con qué criterio?), varias, o las dieciséis.
3. **Usuario del MVP:** solo Ministerio, o también empresa, docente y estudiante. Si es solo Ministerio, corregir el README, donde la mitad de las historias son de empresa.
4. **Qué significa «carrera» y qué titulados cuentan:** área genérica o nombre de carrera; qué niveles conducen a tesis o memoria; si entran IP y CFT; qué hacer con la modalidad no presencial.
5. **Fuentes externas y plan alternativo:** quién verifica las fuentes de demanda, vocación productiva e IA, con qué plazo, y qué se entrega si no sirven (¿ranking solo de oferta?).
6. **Qué se financia:** cofinanciamiento de tesis o subsidios de formación en IA; alinear la visión del README con el MVP.
7. **Criterios y pesos:** quién los aprueba y qué significa «evidencia insuficiente».
8. **Validación del vínculo automático:** tamaño de muestra, métrica y umbral, fijados antes de ver resultados.
9. **Priorización vigente:** si rige el orden de Daniel (hecho sobre la v1), cómo se concilia con las dependencias y si la v2 de Mathias sustituye a la v1.
10. **M-HU07 y el énfasis en gratuidad:** incluir, excluir o declarar expresamente como no medible con los datos disponibles.
11. **Las cuatro historias del README:** reemplazarlas, o mantenerlas como épicas y colgar de ellas las historias con criterios.
