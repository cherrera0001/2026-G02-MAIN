# Feature Specification: 002-oferta-formativa

**Feature Branch**: `sdd/002-oferta-formativa`  
**Created**: 2026-10-16  
**Status**: Implementada en Base / Auditoría de Limitaciones Realizada  
**Input**: Requisitos de oferta territorial de titulados de educación superior, elegibilidad de tesis y normalización por especialización regional. Issues relacionados: #4, #5, #12, #13, #16, #19, #20, #21, #22.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Agregación de Titulados por Territorio y Carrera (Priority: P1)
Como analista del Ministerio de Economía, quiero consultar el número de titulados agregados por región, área genérica, institución y nivel formativo, para identificar qué combinaciones territoriales e institucionales poseen masa crítica de talento para la convocatoria.

**Why this priority**: Es el núcleo observable del sistema (P-HU01 / R4). Responde con datos censales verificables a la oferta existente.

**Independent Test**: Ejecutar consulta sobre `mart.oferta` y verificar que la suma total sea exactamente 328.998 títulos para el periodo 2025 y que cubra las 16 regiones de Chile.

**Acceptance Scenarios**:
1. **Given** la base DuckDB poblada, **When** se consulta `mart.oferta` agrupando por `cod_region, area_generica, institucion, nivel`, **Then** se obtienen los recuentos agregados sin ningún identificador personal.
2. **Given** una carrera específica, **When** se evalúa su cobertura, **Then** el sistema presenta el concepto estándar `area_generica` (285 valores) que permite comparabilidad entre las 144 instituciones.

---

### User Story 2 - Parametrización de Elegibilidad de Tesis y Modalidad No Presencial (Priority: P1)
Como responsable del programa, quiero parametrizar qué niveles formativos son conducentes a tesis/memoria y cómo se trata la modalidad no presencial, para que los recursos públicos no financien programas no elegibles ni se distorsione la localización territorial.

**Why this priority**: Esencial para la validez de las convocatorias (Decisiones D2 y D3). Actualmente el 44.85% de los títulos está en estado 'pendiente' y el 25.08% de los títulos son 'No Presencial' (82.4% concentrados en RM).

**Independent Test**: Filtrar `mart.oferta` aplicando `elegible_tesis = 'si'` y `modalidad <> 'No Presencial'` y medir la reducción exacta de títulos (población neta elegible).

**Acceptance Scenarios**:
1. **Given** títulos de postítulo o diplomados, **When** se evalúa `elegible_tesis`, **Then** devuelven 'no'.
2. **Given** programas técnicos o profesionales sin licenciatura, **When** se consulta su estado, **Then** reflejan 'pendiente' hasta que el Product Owner humano ratifique la decisión D3 (#13).
3. **Given** un programa no presencial con sede legal en Santiago cursado por alumnos en regiones, **When** se analiza la oferta territorial, **Then** el sistema permite aislar o excluir dicha modalidad para no inflar artificialmente a la RM.

---

### User Story 3 - Cociente de Especialización Territorial Normalizado (Priority: P2)
Como científico de datos de políticas públicas, quiero calcular el Cociente de Especialización (LQ) regional por área genérica, para corregir el sesgo de escala de la Región Metropolitana y visibilizar ventajas comparativas en regiones extremas.

**Why this priority**: Da cumplimiento al Principio VI de la Constitución. La RM concentra el 57% de los titulados brutos; sin LQ, el ranking priorizaría únicamente la capital.

**Independent Test**: Consultar `mart.especializacion`. Validar que $LQ_{ra} = \frac{T_{ra}/T_r}{T_a/T_{nacional}}$, verificando que el valor mediana sea ~1.23 y que las especializaciones regionales superen 1.0.

**Acceptance Scenarios**:
1. **Given** un área concentrada en una región (ej. Ingeniería Naval en Los Ríos), **When** se calcula el LQ, **Then** el valor resulta significativamente mayor a 1.0, reflejando especialización territorial.
2. **Given** celdas con volumen muy bajo (ej. 1 a 5 titulados), **When** se analiza el LQ, **Then** el sistema alerta sobre hiperinflación muestral y aplica reglas de supresión de celdas pequeñas (Decisión D6 / #16).

---

## Edge Cases

- ¿Qué ocurre con programas impartidos en comunas que no tienen código territorial CUT en la capa geo? El sistema preserva los títulos asociándolos a la comuna con `cod_cut IS NULL` y registra el control informativo `comunas_sin_cut = 20`.
- ¿Qué ocurre con títulos de instituciones fusionadas o cerradas? Se agrupan bajo su código institucional SIES preservando la serie histórica.

## Requirements *(mandatory)*

### Functional Requirements
- **FR-002-1**: El sistema DEBE mantener en `core.programa` la granularidad a nivel de código SIES con atributos de jornada, modalidad, duración y nivel.
- **FR-002-2**: El sistema DEBE clasificar cada nivel formativo en `core.nivel_carrera` con el campo `elegible_tesis` ('si', 'no', 'pendiente').
- **FR-002-3**: El sistema DEBE exponer la vista `mart.oferta` con agregación por periodo, región, área genérica, institución, nivel, modalidad y títulos totales.
- **FR-002-4**: El sistema DEBE calcular el cociente de especialización en `mart.especializacion` con ventana analítica sobre el universo nacional del periodo.
- **FR-002-5**: El sistema DEBE permitir filtrar celdas con $n < \tau$ (donde $\tau$ es el umbral de secreto estadístico y estabilidad, parametrizable entre 3 y 10).

### Key Entities
- **core.programa**: Oferta curricular de las IES identificada por código SIES.
- **core.nivel_carrera**: Clasificación de programas según grado académico y elegibilidad de tesis.
- **core.titulacion**: Hecho agregado de graduación por periodo, programa y género.
- **mart.oferta**: Vista analítica consolidada para evaluación de masa crítica.
- **mart.especializacion**: Vista de ventajas comparativas territoriales reveladas.

## Success Criteria *(mandatory)*

### Measurable Outcomes
- **SC-002-1**: Cuadre exacto del 100% de los títulos cargados (328.998 títulos en 2025).
- **SC-002-2**: Cobertura comprobada en las 16 regiones administrativas del país.
- **SC-002-3**: Exclusión o aislamiento comprobable del 100% de los 82.525 títulos no presenciales bajo parámetro de filtro territorial.
- **SC-002-4**: Identificación precisa del 44.85% de los títulos condicionados a la decisión D3.

## Assumptions
- Los datos de Mineduc 2025 son definitivos y oficiales.
- El área genérica SIES (285 categorías) es la unidad estándar de comparación curricular entre instituciones.
