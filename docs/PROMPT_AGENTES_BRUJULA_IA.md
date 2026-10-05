# Prompt para construir el equipo de agentes — Brújula IA Regional

Pega este prompt en Claude Code, abierto en la raíz del repositorio del grupo (el clon de GitHub, no una copia descargada en ZIP).

---

## Contexto

Trabajas en el repositorio del Grupo 02 del curso «Proyectos en Tecnología» (Magíster en Ciencia de Datos). El encargo simula una consultoría al Ministerio de Economía: decidir con evidencia dónde focalizar el cofinanciamiento de memorias y tesis aplicadas que desarrollen habilidades complementarias a la IA.

El MVP declarado en `README.md` es una herramienta de priorización que entrega un ranking de combinaciones región × carrera × institución, una visualización por región y un reporte con recomendaciones. La herramienta orienta una convocatoria: no evalúa postulaciones, no administra fondos y no promete impacto causal sobre empleo o ingresos.

El curso evalúa el proceso tanto como el producto: historias de usuario, tareas estimadas, tablero Kanban al día, commits que explican el porqué y roles que rotan por sprint. El Sprint 1 se presenta el 17/10/2026 y el Sprint 2 el 31/10/2026 (fechas tomadas del chat del equipo; confírmalas con el syllabus antes de fijarlas en GitHub).

Lee antes de actuar: `README.md`, `.github/ISSUE_TEMPLATE/`, los `README.md` de `data/` y `chat-wsp/G2 proyectos en tecnología/ANALISIS_CHAT_PROYECTO.md` (historias propuestas, criterios de aceptación y preguntas abiertas del equipo).

## Lo que ya se sabe de los datos

Estos hechos se verificaron sobre los archivos del repositorio el 05/10/2026. No los vuelvas a derivar; sí comprueba que los archivos no hayan cambiado.

**Oferta — `data/oferta/Titulados-Ed-Superior-2025.rar`**
- Contiene un CSV de 189 MB (separador `;`, UTF-8), con 328.998 filas y 41 columnas, y el PDF con el diccionario de datos de Mineduc. GitHub rechaza archivos de más de 100 MB: el CSV extraído nunca se versiona.
- Una fila es un título obtenido por una persona. Incluye `mrun` (identificador enmascarado), fecha de nacimiento y género. Son microdatos: la plataforma solo expone agregados.
- Solo cubre el periodo 2025 (`cat_periodo`), con fechas de titulación entre 2025 y comienzos de 2026. Para ver tendencias hay que descargar más años desde Mineduc (la serie existe desde 2007).
- Incluye universidades (194.477), institutos profesionales (94.814) y centros de formación técnica (39.707). La duda del equipo sobre si faltaban IP y CFT queda resuelta: están.
- Tiene las 16 regiones. La Metropolitana concentra el 57 % de los titulados, así que un ranking por volumen bruto siempre la favorece: hay que normalizar (por ejemplo, con un cociente de especialización regional).
- `nomb_carrera` tiene 5.598 valores distintos; `area_generica` tiene 285 y es la mejor candidata a «carrera» comparable. La combinación región × área genérica × institución da 6.088 celdas.
- No todo titulado hace tesis o memoria. Hay 61.948 diplomados y 3.426 postítulos. Profesional con licenciatura, magíster y doctorado suman 116.053. Si entran las carreras profesionales sin licenciatura (55.015) y las técnicas (87.067) es una decisión del Product Owner.
- 82.525 títulos son de modalidad no presencial: su `region_sede` no indica dónde vive la persona.

**Territorio — `data/geo/layer_establecimientos_de_educacion_superior_*.zip`**
- Shapefile de puntos en EPSG:4326, con 1.297 inmuebles de 134 instituciones, año 2020, con región, provincia, comuna, dirección, latitud y longitud.
- No trae código de sede. Se une con titulados por `cod_inst` + comuna normalizada (sin tildes, en mayúsculas): esa llave cubre el 96,6 % de los titulados. Una institución puede tener varios inmuebles en la misma comuna.

**Entorno físico — `data/demanda/`**
- La carpeta no trae archivos, solo un `README.md` con dos enlaces a infraestructura y edificación pública. Pese al nombre de la carpeta, eso es entorno físico (vialidad, puertos, aeropuertos, servicios públicos) para caracterizar polos de desarrollo, no demanda laboral.
- Ambas fuentes se descargan sin scraper (ver la sección siguiente).

**Demanda laboral y exposición a IA — no están en el repositorio**
- Demanda laboral, vocación productiva regional y exposición o complementariedad con IA no existen en el repositorio ni en sus enlaces. Conseguirlas es el mayor riesgo del proyecto. Fuentes candidatas, todas por verificar en cobertura y nivel de detalle: ENADEL (SENCE), Estrategias Regionales de Desarrollo, PIB regional por actividad (Banco Central), estadísticas de empresas por región y rubro (SII), Encuesta Nacional de Empleo (INE), e índices publicados de exposición ocupacional a IA (OIT, FMI).

## Cómo se descargan las fuentes

Los cuatro enlaces de los `README.md` de `data/` se probaron el 05/10/2026. Ninguno necesita un scraper de navegador: todos ofrecen descarga directa o una API estándar. Lo que hace falta es un script de descarga reproducible con un manifiesto de fuentes (nombre, URL, formato, fecha de descarga, hash del archivo), que deje todo en `data/raw/`.

| Fuente | Mecanismo verificado | Notas |
|---|---|---|
| Titulados (Mineduc) | Descarga directa de un `.rar` por año, de 2007 a 2025: `https://datosabiertos.mineduc.cl/wp-content/uploads/2026/09/Titulados-Ed-Superior-<AÑO>.rar` | Unos 7 MB por año comprimido y cerca de 190 MB extraído. La ruta `2026/09` puede cambiar cuando Mineduc republique: obtén los enlaces leyendo la página `titulados-en-educacion-superior/` en lugar de fijarlos. Extraer `.rar` requiere `unrar` o 7-Zip instalado. |
| Sedes de educación superior (Geoportal / IDE Chile) | Descarga directa del ZIP: `https://www.geoportal.cl/geoportal/catalog/download/0dde8427-113a-356a-bace-ed4d51ddcb05`. También hay WFS que responde GeoJSON en `https://geoportal.cl/geoserver/Establecimientos_Educacion_Superior/ows` | El ZIP es el mismo archivo que ya está en `data/geo/`. |
| Instalaciones y edificaciones (datos.gob.cl) | API CKAN: `https://datos.gob.cl/api/3/action/package_show?id=categoria-geoespacial-instalaciones-y-edificaciones` | Devuelve la lista de recursos con sus URL. Son 7 shapefiles alojados en el Geoportal: educación superior, escolar y parvularia, bomberos (dos capas), carabineros y centros de SERNAM. Licencia CC-BY. No incluye empresas ni actividad económica. |
| Infraestructura MOP (geomop) | La página `descargas/` es una tabla HTML con unas 60 capas. Cada una enlaza tres archivos en Google Drive y un servicio ArcGIS REST en `https://rest-sit.mop.gob.cl/arcgis/rest/services/...` | Dos formas de bajar: (a) Drive, donde los archivos pequeños bajan directo y los grandes (por ejemplo Red Vial) devuelven una página de confirmación que hay que resolver, por ejemplo con la librería `gdown`; (b) ArcGIS REST con `/<capa>/query?where=1=1&outFields=*&f=json`, paginando con `resultOffset` porque el máximo es 1.000 registros por consulta. |

Capas del MOP útiles para este proyecto: Red Vial, Puentes, Infraestructura Portuaria y Red Aeroportuaria. El resto (embalses, aguas, obras hidráulicas) no aporta a la pregunta.

Descarga solo lo que una historia aceptada necesite. Las capas de infraestructura sirven para accesibilidad y proximidad, que es trabajo del Sprint 2.

## Decisiones abiertas (son del equipo humano)

No las resuelvas por tu cuenta. Propón una opción recomendada con su razón y espera respuesta.

1. Unidad del ranking: región × carrera × institución (README) o carrera × sector dentro de una región piloto (propuesta de Mathias).
2. Alcance geográfico: las 16 regiones o una región piloto.
3. Qué niveles de carrera cuentan como población de tesis o memoria.
4. Qué fuentes de demanda y de exposición a IA se aceptan como evidencia.
5. Usuario principal del MVP. Las historias de estudiante, docente y empresa describen una plataforma de vinculación que los datos actuales no sostienen.
6. Frontend: Streamlit (recomendado, el equipo trabaja en Python y quedan dos sprints cortos) o una aplicación web separada.

## Tu trabajo

### Paso 1 — Crea los agentes

Crea un archivo por agente en `.claude/agents/<nombre>.md`, con frontmatter `name`, `description` (cuándo usarlo) y `tools`, seguido de sus instrucciones. Cada agente debe recibir: el contexto de arriba que le concierne, qué carpetas le pertenecen, qué entrega y cómo se comprueba que terminó.

| Agente | Le pertenece | Entrega |
|---|---|---|
| `product-owner` | Issues, tablero, `README.md` (historias, sprints) | Historias verificadas, tareas con peso, tablero al día. No escribe código. |
| `analista-fuentes` | `data/*/README.md`, `docs/fuentes/` | Una ficha por fuente externa: URL, licencia, cobertura, años, unidad territorial, campos útiles, limitaciones y veredicto (usar, descartar). |
| `ingeniero-datos` | `src/pipeline/`, `data/raw/` y `data/processed/` (ambas fuera de git) | Scripts reproducibles: extraer, limpiar, agregar y unir. Salida en Parquet. Reporte de cobertura de cada unión. |
| `cientifico-datos` | `src/modelo/`, `notebooks/` | Índice multicriterio con pesos explícitos, análisis de sensibilidad, vínculo carrera–sector, estadística espacial. Cada métrica documentada. |
| `experto-backend` | `src/servicios/` | Lógica de dominio que la API consume: consultas sobre los Parquet (DuckDB), recálculo del ranking con pesos, ficha de evidencia. |
| `experto-api` | `src/api/` | API FastAPI con contrato OpenAPI. Solo agregados; ningún campo personal sale por la API. |
| `experto-frontend` | `app/` | Vistas de ranking, mapa, escenarios y ficha de evidencia, consumiendo la API. |
| `revisor-qa` | `tests/`, CI | Pruebas, verificación de reproducibilidad desde un clon limpio y revisión contra la Definition of Done. Solo lectura sobre el código ajeno. |

Reglas comunes a todos los agentes:
- Trabajan una tarea a la vez, ligada a un issue. Rama `tipo/numero-descripcion`, commit que explica el porqué, PR que cierra el issue.
- Ninguna afirmación sobre datos sin el código que la reproduce. Toda cifra mostrada al usuario lleva fuente, fecha y cobertura.
- Distinguen siempre dato observado, inferencia del modelo y propuesta del equipo.
- Si un dato falta, lo declaran. No lo imputan ni lo interpretan como evidencia en contra.
- No inventan requisitos: lo que no está en una historia aceptada se propone al `product-owner`.

Stack: Python 3.12 con `uv`, polars y DuckDB, geopandas, FastAPI, Streamlit con Plotly, pytest y ruff.

### Paso 2 — Verifica las historias de usuario

Con el agente `product-owner`, revisa las cuatro historias del `README.md` y las siete de Mathias (M-HU01 a M-HU07 en el análisis del chat). Para cada una responde:
- ¿Los datos disponibles o conseguibles permiten cumplirla? ¿Con qué campos?
- ¿Sus criterios de aceptación son comprobables con una demostración concreta (entrada y salida esperada)?
- ¿Cabe en el MVP o describe otra plataforma?

Punto de partida de esa verificación:

| Historia del README | Veredicto preliminar |
|---|---|
| 1. Responsable del programa: dónde focalizar | Factible. Es el ranking; depende de conseguir datos de demanda. Equivale a M-HU04 a M-HU06. |
| 2. Analista: qué problemas sectoriales aborda cada carrera | Factible solo con fuentes externas y una tabla puente carrera–sector. Equivale a M-HU02 y M-HU03. |
| 3. Empresa: probar mejoras con IA a costo acotado | No verificable con una herramienta analítica. Proponer sacarla del MVP o reformularla. |
| 4. Empresa: qué talento se forma cerca | Factible hoy con titulados y sedes. Equivale a M-HU01 más el mapa. |

Entrega un documento breve con el veredicto por historia y las preguntas que el equipo debe contestar. Detente y espera la aprobación del equipo antes del paso 3.

### Paso 3 — Monta la gestión en GitHub

Requiere que el equipo confirme el propietario y el nombre del repositorio. Muestra el listado completo de lo que vas a crear y espera un «sí» explícito: crear issues y tableros notifica a todo el equipo.

1. Milestones `Sprint 1` y `Sprint 2` con sus fechas de presentación.
2. Un GitHub Project con columnas Backlog, Por hacer, En curso, En revisión y Hecho, y los campos `Peso` (número), `Horas estimadas` (número), `Sprint` y `Rol`.
3. Un issue por historia con la plantilla `user-story-template.md` (etiqueta `user story`) y un issue por tarea con `tarea-template.md` (etiqueta `tarea`), enlazado como subtarea de su historia.
4. Actualiza el `README.md`: criterios de aceptación y tareas bajo cada historia, y el contenido de cada sprint.

**Escala de peso (0 a 5)** para cada tarea:

| Peso | Significado |
|---|---|
| 0 | Sin esfuerzo de construcción: registrar una decisión o un acuerdo. |
| 1 | Hasta una hora. Cambio acotado y sin incertidumbre. |
| 2 | Dos a tres horas. Se sabe cómo hacerlo. |
| 3 | Media jornada. Alguna incertidumbre técnica o de datos. |
| 4 | Una jornada. Toca varias piezas o depende de datos externos. |
| 5 | Más de una jornada o incertidumbre alta. Dividir antes de empezar. |

El peso de una historia es la suma de sus tareas. Registra además las horas estimadas, porque la rúbrica del curso las pide.

**Backlog semilla** (propuesta para validar, no acuerdo del equipo):

*Sprint 1 — datos integrados y comparación básica*

| Tarea | Rol | Peso |
|---|---|---|
| Registrar las decisiones de alcance (unidad, regiones, niveles de carrera) | product-owner | 0 |
| Estructura del repositorio, entorno `uv`, lint y pruebas en CI | revisor-qa | 2 |
| Script de descarga con manifiesto de fuentes (Mineduc por año, Geoportal, CKAN) y extracción a `data/raw/`, más diccionario de datos | ingeniero-datos | 3 |
| Limpieza y agregación de titulados a región × área genérica × institución × nivel | ingeniero-datos | 3 |
| Unión con sedes por institución y comuna, con reporte de cobertura | ingeniero-datos | 3 |
| Fichas de fuentes de demanda, estrategia regional y exposición a IA | analista-fuentes | 3 |
| Ingesta de la fuente elegida a una tabla sector × región con fuente y fecha | ingeniero-datos | 4 |
| Tabla puente área genérica–sector, versión manual revisada por el equipo | cientifico-datos | 3 |
| Índice v0: especialización de la oferta más prioridad regional, normalizado | cientifico-datos | 3 |
| Servicios de consulta de oferta, sedes y ranking | experto-backend | 3 |
| Endpoints de oferta, sedes (GeoJSON) y ranking | experto-api | 2 |
| Vista de oferta con tabla y mapa de sedes | experto-frontend | 3 |
| Vista de ranking por región | experto-frontend | 3 |
| Demo y presentación del Sprint 1 | product-owner | 2 |

*Sprint 2 — priorización explicable*

| Tarea | Rol | Peso |
|---|---|---|
| Indicador de exposición y complementariedad con IA por área | cientifico-datos | 4 |
| Vínculo semántico carrera–sector y contraste con una muestra revisada a mano | cientifico-datos | 5 (dividir) |
| Pesos ajustables y análisis de sensibilidad del ranking | cientifico-datos | 4 |
| Descarga de capas del MOP (red vial, puertos, aeropuertos) por ArcGIS REST o Drive | ingeniero-datos | 3 |
| Estadística espacial: proximidad de sedes y concentración territorial | cientifico-datos | 4 |
| Recalcular el ranking con pesos y comparar con el escenario base | experto-backend | 3 |
| Endpoints de escenarios y de ficha de evidencia | experto-api | 2 |
| Vista de escenarios y ficha de evidencia por recomendación | experto-frontend | 4 |
| Reporte con recomendaciones para el Ministerio | product-owner | 3 |
| Verificación de reproducibilidad desde un clon limpio | revisor-qa | 2 |

### Paso 4 — Construye por sprint

Con el backlog aprobado, toma las tareas del sprint en curso en orden de dependencia: datos, modelo, servicios, API, frontend. Delega cada una al agente dueño, haz que `revisor-qa` la revise contra los criterios de aceptación del issue y mueve la tarjeta. Al cerrar el sprint, entrega un incremento que se pueda demostrar con datos reales.

## Límites

- No subas a GitHub el CSV extraído ni `chat-wsp/` (contiene la conversación del equipo con nombres y datos personales). Agrégalos a `.gitignore`.
- No expongas `mrun`, fecha de nacimiento ni filas individuales en la API, el frontend o los reportes.
- No crees, cierres ni reasignes issues, ni hagas push o merge a `main`, sin confirmación del equipo.
- Las fechas, la ponderación de la evaluación y el rol de Scrum Master no están confirmados en el repositorio: pregúntalos, no los asumas.
