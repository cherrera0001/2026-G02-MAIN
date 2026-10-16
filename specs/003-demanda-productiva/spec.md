# Feature Specification: 003-demanda-productiva

**Feature Branch**: `sdd/003-demanda-productiva`  
**Created**: 2026-10-16  
**Status**: Bloqueada Científicamente por Ausencia de Fuentes Validadas  
**Input**: Requisitos de evidencia pública de demanda laboral, vocación productiva regional y prioridades económicas territoriales. Issues relacionados: #6, #14, #23, #24, #25, #26, #27, #28, #30.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Catálogo Sectorial Estándar (Priority: P1)
Como arquitecto de datos, quiero disponer de una clasificación sectorial estandarizada (CIIU4.CL) en `core.sector`, para vincular homogéneamente la información económica y laboral de diversas fuentes.

**Why this priority**: Sin un estándar de codificación sectorial común, no se pueden cruzar datos del Banco Central, SII, INE y SENCE.

**Independent Test**: Consultar `core.sector` y verificar unicidad de `(clasificacion, codigo)` y cobertura de las ramas económicas principales.

**Acceptance Scenarios**:
1. **Given** una rama productiva oficial (ej. Silvoagropecuaria, Minería, Servicios Informáticos), **When** se consulta `core.sector`, **Then** existe un registro con su código CIIU y descripción normalizada.

---

### User Story 2 - Ingesta de Indicadores de Demanda y Especialización Económica (Priority: P1 - BLOQUEADA)
Como analista del Ministerio de Economía, quiero consultar indicadores observables de demanda laboral (SENCE/ENADEL), ocupación regional (INE/ENE), dinamismo empresarial (SII) y PIB regional (Banco Central), para cuantificar la vocación productiva real de cada región.

**Why this priority**: Requisito indispensable para fundamentar las áreas de cofinanciamiento en las prioridades productivas reales de los territorios (P-HU02).

**Independent Test**: Comprobar que `core.indicador_region_sector` contenga datos con trazabilidad a `gob.carga` y que cada cifra declare si es `observado` o `inferido`.

**Acceptance Scenarios**:
1. **Given** fuentes oficiales de demanda cargadas, **When** se consulta una región y sector, **Then** se obtienen los valores empíricos sin imputaciones artificiales.
2. **Given** que las fuentes no están validadas o presentan descalce temporal/territorial, **When** se evalúa la capacidad de cálculo, **Then** el sistema emite el estado `BLOCKED` documentando formalmente las razones del bloqueo (Decisión D4 / #14).

---

## Edge Cases

- ¿Qué ocurre si una región no tiene registro en una fuente muestral (ej. ENADEL no cubre sectores rurales en Aysén)? El valor se almacena como `NULL`. Está estrictamente prohibido imputar valores ficticios o usar medias nacionales como si fueran locales (Constitución Principios I y III).
- ¿Qué ocurre si la clasificación de actividades difiere entre el SII y el Banco Central? La tabla `core.sector` almacena la clasificación de origen (`clasificacion`), requiriendo una tabla puente metodológica previa a cualquier unión.

## Requirements *(mandatory)*

### Functional Requirements
- **FR-003-1**: El sistema DEBE mantener en `core.sector` la estructura normalizada de clasificación económica con clave primaria única.
- **FR-003-2**: El sistema DEBE exigir en `core.indicador` la definición metodológica, unidad, id de fuente y tipo de evidencia ('observado', 'inferido', 'propuesto').
- **FR-003-3**: El sistema DEBE registrar en `core.indicador_region_sector` el valor a granularidad `(id_indicador, cod_region, id_sector, periodo)`.
- **FR-003-4**: Ante ausencia de fuentes verificadas, el sistema DEBE registrar formalmente el estado de investigación como `BLOCKED`, impidiendo la generación de rankings con variables ficticias.

### Key Entities
- **core.sector**: Catálogo oficial de actividades económicas y sectores productivos.
- **core.indicador**: Metadata y definición conceptual de métricas económicas y laborales.
- **core.indicador_region_sector**: Panel territorial-sectorial de variables de demanda y valor agregado.

## Success Criteria *(mandatory)*

### Measurable Outcomes
- **SC-003-1**: Publicación de las fichas de investigación comparativa (#23 a #28) evaluando cobertura, periodicidad y licencia.
- **SC-003-2**: Cero filas con datos simulados o inventados en `core.indicador_region_sector`.
- **SC-003-3**: Dictamen fundado de la Decisión D4 (#14) antes de admitir cualquier factor económico en la fórmula de priorización.

## Assumptions
- Las fuentes de demanda requerirán acuerdos institucionales o descarga de microdatos externos no incluidos en el repositorio base.
- Las tablas permanecen con 0 filas hasta que el equipo humano apruebe formalmente la ingesta.
