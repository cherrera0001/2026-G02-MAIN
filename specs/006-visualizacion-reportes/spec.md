# Feature Specification: 006-visualizacion-reportes

**Feature Branch**: `sdd/006-visualizacion-reportes`  
**Created**: 2026-10-16  
**Status**: En Propuesta / Capa de Datos Parcialmente Disponible  
**Input**: Requisitos de interfaz analítica territorial (mapas, tablas, filtros) y generador de reportes ejecutivos reproducibles para autoridades ministeriales. Issues relacionados: #10, #15, #17, #44, #45, #46, #47.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Visualización Territorial de Oferta e Inmuebles IES (Priority: P1)
Como analista ministerial, quiero explorar un mapa interactivo y tablas de sedes e inmuebles de educación superior vinculados a los titulados de su comuna, para conocer la distribución espacial del talento y la infraestructura universitaria regional.

**Why this priority**: Entrega la promesa de visualización territorial del MVP sustentándose en datos ya existentes en `mart.sedes_geo` (#44).

**Independent Test**: Consultar `mart.sedes_geo` y renderizar los puntos georreferenciados del corte validado en un componente cartográfico, verificando que muestre institución, comuna, región y volumen de titulados comunales asociados.

**Acceptance Scenarios**:
1. **Given** la capa de inmuebles georreferenciados, **When** el usuario selecciona una región, **Then** el mapa encuadra las sedes de esa región y detalla los títulos generados en la comuna respectiva.
2. **Given** que un inmueble no tuvo titulados en 2025 (cantidad calculada para el corte), **When** se visualiza su ficha, **Then** el sistema muestra explícitamente `sin dato de oferta para este periodo` si el valor es NULL; mostrar cero solo si está observado sin ocultar la infraestructura física.

---

### User Story 2 - Generador Automatizado de Reportes Ejecutivos (Priority: P1)
Como responsable del programa, quiero generar desde código un reporte reproducible en PDF o Markdown estructurado con recomendaciones territoriales, donde cada cifra cite su fuente oficial, fecha y limitaciones metodológicas, para sustentar la convocatoria ante autoridades del Ministerio.

**Why this priority**: Es el entregable clave de cierre del MVP (P-HU06 / #46). Permite a personas no técnicas acceder a la evidencia analítica sin operar código ni bases de datos.

**Independent Test**: Ejecutar el script generador de reportes (`python -m src.reportes.generar`) y validar el documento resultante contra la lista de comprobación de calidad (#47).

**Acceptance Scenarios**:
1. **Given** la ejecución del generador, **When** se inspecciona el reporte generado, **Then** el 100% de las tablas y gráficos contienen leyenda con Organismo, Año del dato, cobertura territorial y fecha de extracción.
2. **Given** la auditoría del documento, **When** se evalúa la privacidad, **Then** el reporte no expone microdatos ni celdas bajo el umbral de secreto estadístico.

---

### User Story 3 - Explorador Interactivo de Prioridades y Escenarios (Priority: P2 - BLOQUEADA)
Como analista de políticas públicas, quiero interactuar con los escenarios de ponderación del ranking mediante controles de interfaz (deslizadores de pesos, selectores de región), para visualizar cómo se desplazan las prioridades territoriales.

**Why this priority**: Facilita la deliberación informada del comité técnico ministerial (#45). Bloqueada hasta la resolución de las capacidades 003, 004 y 005.

**Independent Test**: Modificar los controles deslizantes de pesos en la interfaz (asegurando suma 1) y comprobar que la tabla de resultados se actualice reactivamente en menos de 1 segundo.

**Acceptance Scenarios**:
1. **Given** la interfaz web (Streamlit), **When** el usuario ajusta el peso de "Demanda Regional", **Then** el ranking se recalcula al vuelo mostrando las variaciones de posición relativa.

---

## Edge Cases

- ¿Qué sucede si la persona consulta la aplicación desde un dispositivo sin conexión a internet? Los mapas base no deben fallar catastróficamente; la interfaz debe ofrecer visualización tabular o gráfica vectorial alternativa si los azulejos (tiles) cartográficos remotos no cargan.
- ¿Qué ocurre si un usuario descarga los datos desde la interfaz web? La exportación en CSV/Excel debe entregar agregados filtrados por secreto estadístico, manteniendo los metadatos de fuente en los encabezados.

## Requirements *(mandatory)*

### Functional Requirements
- **FR-006-1**: La interfaz DEBE construirse en Streamlit como MVP analítico unificado conectado directamente a DuckDB local.
- **FR-006-2**: La vista cartográfica DEBE consumir `mart.sedes_geo`, declarando la cobertura de la unión calculada para el corte, sin sumar totales repetidos por inmueble.
- **FR-006-3**: El generador de reportes DEBE ejecutarse por línea de comandos de manera 100% reproducible y sin intervención manual.
- **FR-006-4**: El reporte DEBE someterse a la lista de comprobación de calidad (#47): verificación de fuentes, fechas, ausencia de microdatos y lenguaje accesible para tomadores de decisión.

### Key Entities
- **mart.sedes_geo**: Capa geoespacial que articula inmuebles físicos con la masa crítica de oferta formativa comunal.
- **reporte_ejecutivo**: Documento estructurado reproducible que sintetiza diagnósticos, evidencias y limitaciones.

## Success Criteria *(mandatory)*

### Measurable Outcomes
- **SC-006-1**: Generación del reporte ejecutivo reproducible en menos de 5 segundos desde la terminal.
- **SC-006-2**: 100% de cumplimiento en la lista de comprobación del reporte (#47).
- **SC-006-3**: Cero microdatos o rutas locales expuestas en la interfaz web pública o reportes descargables.

## Assumptions
- Streamlit es la interfaz oficial aprobada del MVP (ADR-002; D7 / #17 decidida por el responsable), descartando el desarrollo de APIs complejas o microservicios para la fase actual.

## Ampliación aprobada del MVP Streamlit (2026-10-16)
Las historias originales US-001 (mapa), US-002 (reporte) y US-003 (escenarios) se conservan. Los números de rendimiento anteriores son objetivos pendientes de medición. La interfaz no habilita escenarios por tener tablas vacías creadas.

### US-004 — Vista general (P1)
Como analista quiero conocer alcance territorial y cobertura para interpretar la evidencia disponible.
Aceptación: dado un corte validado, al abrir Inicio se muestran periodo, cobertura y totales obtenidos del dominio; sin base o con controles fallidos se informa indisponibilidad, sin cifras de ejemplo ni trazas con rutas locales.

### US-005 — Filtros y oferta (P1)
Como analista quiero filtrar región, institución y carrera para examinar oferta comparable.
Aceptación: al combinar filtros se aplica su intersección con parámetros SQL; limpiar restaura el corte. Carrera se identifica como área genérica comparable, sin confundirla con programa SIES. Una selección sin filas muestra «sin datos» y nunca cero imputado. Los totales coinciden con `mart.oferta` para el mismo periodo y filtros. Se diferencia modalidad no presencial y no se interpreta como residencia.

### US-006 — Demanda y contexto productivo (P1, condicionada)
Como analista quiero consultar indicadores verificados para contextualizar la oferta.
Aceptación: con fuentes aceptadas y controles aprobados se muestran unidad, periodo, cobertura y naturaleza de evidencia; sin esas fuentes se muestra «fuente pendiente de validar» y no se representa un indicador sintético. No se presenta oferta como demanda.

### US-007 — Explicación y faltantes (P1)
Como revisor quiero ver criterios, ponderaciones y evidencia faltante para auditar un resultado.
Aceptación: mientras 005 está bloqueada, Ranking informa cada bloqueo y deshabilita cálculo, sliders y descarga de ranking. Con ejecución validada, muestra versión, pesos, aportes, normalización y sensibilidad desde el dominio; el total se reconstruye con tolerancia definida en 005. Los nulos conservan su significado y se distinguen de cero y de supresión. No se adopta renormalización de faltantes sin validación metodológica.

### US-008 — Procedencia (P1)
Como revisor quiero inspeccionar procedencia para reproducir cifras.
Aceptación: cada vista y reporte enlaza catálogo, organismo, URL, periodo, fecha de carga y hash del lote; una fecha de publicación no disponible se declara desconocida, sin sustituirla silenciosamente por fecha de carga. La cobertura de mapa distingue inmueble de institución-comuna y no atribuye títulos individuales a cada inmueble.

### US-009 — Exportación segura (P1)
Como responsable quiero descargar agregados del corte consultado con su procedencia.
Aceptación: sin política de divulgación y umbral D6 aprobados, CSV/Excel y reporte publicable permanecen bloqueados con motivo. Con autorización, se exporta exclusivamente una lista de columnas agregadas, filtros, periodo y metadatos; se aplica supresión primaria y secundaria para impedir reconstrucción por totales y filtros; se neutralizan celdas interpretables como fórmulas. No salen microdatos, rutas ni credenciales. El contenido coincide con los agregados visibles autorizados.

### FR adicionales
- FR-006-5: navegación Inicio, Oferta/Mapa, Demanda, Ranking y Fuentes/Exportación conserva filtros de sesión y permite volver a Inicio sin error.
- FR-006-6: errores de base ausente, corrupta, bloqueada o esquema incompatible se muestran de forma controlada; no se crea una base vacía ni se ejecuta el pipeline desde la UI.
- FR-006-7: las fórmulas y reglas de publicación residen fuera de los componentes Streamlit; se invalida caché al cambiar hash de datos, versión o filtros.
- FR-006-8: las pruebas cubren inicio, navegación, filtros, nulos, métricas, exportaciones, lectura y reproducibilidad, contrastando UI contra DuckDB y manteniendo pruebas matemáticas independientes.
