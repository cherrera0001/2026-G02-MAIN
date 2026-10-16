# Feature Specification: 001-gobernanza-fuentes

**Feature Branch**: `sdd/001-gobernanza-fuentes`  
**Created**: 2026-10-16  
**Status**: Implementada y Auditada (Fase 1 / Fase 4)  
**Input**: Requisitos de gobierno de datos, trazabilidad criptográfica, auditoría de fuentes y minimización de privacidad. Issues relacionados: #18, #23, #24, #25, #26, #27, #28.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Catálogo y Trazabilidad Criptográfica de Ingesta (Priority: P1)
Como ingeniero de datos del proyecto, quiero registrar el origen, metadata, URL oficial y hash criptográfico SHA-256 de cada archivo ingresado, para garantizar que los datos procesados provengan de fuentes públicas verificables y no hayan sufrido alteraciones.

**Why this priority**: Es la base innegociable de la Constitución SDD (Principios I, II y IV). Sin trazabilidad criptográfica, ninguna cifra posterior es científicamente defendible.

**Independent Test**: Ejecutar `construir_bd.py` y consultar `SELECT count(*) FROM gob.carga WHERE sha256 IS NOT NULL AND filas_leidas > 0`. Debe coincidir exactamente con el número de fuentes extraídas y leídas.

**Acceptance Scenarios**:
1. **Given** un archivo de microdatos en `data/raw/`, **When** se ejecuta el pipeline, **Then** se calcula su SHA-256 y se inserta en `gob.carga` con fecha, filas y periodo.
2. **Given** una fuente externa sin catalogar, **When** se intenta registrar una carga con `id_fuente` no existente, **Then** la base rechaza la inserción por llave foránea `REFERENCES gob.fuente(id_fuente)`.

---

### User Story 2 - Control Automatizado de Calidad e Invariantes de Privacidad (Priority: P1)
Como revisor de QA y seguridad, quiero ejecutar controles de calidad automáticos bloqueantes en cada reconstrucción de la base, para impedir que errores de carga o microdatos personales se persistan en el sistema.

**Why this priority**: Cumple el mandato de privacidad (Constitución Principio V). Evita filtración de MRUN o fechas de nacimiento y previene corrupción de agregados.

**Independent Test**: Ejecutar la suite de controles en `gob.control_calidad`. El script aborta inmediatamente si un control marcado como `bloquea = True` no cumple su umbral.

**Acceptance Scenarios**:
1. **Given** el esquema DuckDB tras la ingesta, **When** se evalúa la consulta sobre `information_schema.columns` buscando nombres como `mrun`, `nac` o `edad`, **Then** el resultado debe ser estrictamente 0.
2. **Given** la carga de titulados, **When** se contrasta la suma de `core.titulacion.n_titulos` contra `filas_leidas` de Mineduc, **Then** la relación debe ser exactamente 1.0 (cero títulos perdidos).

---

### User Story 3 - Inventario y Veredicto de Fuentes Candidatas Externas (Priority: P2)
Como analista de fuentes, quiero disponer de una ficha estandarizada para cada fuente potencial (ENADEL, ERD, Banco Central, SII, INE), para que el equipo decida con evidencia si se integran o descartan.

**Why this priority**: Necesario para desbloquear las capacidades 003 y 004, conforme a la Decisión D4 (#14).

**Independent Test**: Validar que cada ficha en `docs/fuentes/` cumpla la estructura de `PLANTILLA_FICHA.md` y contenga veredicto (`usar`, `descartar`, `pendiente`) respaldado por URL y fecha de consulta.

**Acceptance Scenarios**:
1. **Given** una fuente de datos sin validar, **When** el analista completa su ficha, **Then** su estado inicial es `pendiente` y se documentan granularidad territorial y temporal.

---

## Edge Cases

- ¿Qué sucede si el archivo de origen descargado está corrupto o truncado? El cálculo del hash SHA-256 difiere del esperado y el control de calidad `titulos_conservados` detecta discrepancia de filas, abortando el reemplazo de la base de datos de producción (`brujula.duckdb`).
- ¿Qué ocurre si un organismo cambia la URL de descarga o publica con nuevo esquema de columnas? La carga de staging utiliza `union_by_name=true` y `all_varchar=true`, pero si faltan campos obligatorios (`comuna_sede`, `cat_periodo`, `cod_sies_obt_tit`), la validación SQL subsiguiente falla de forma controlada.

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001-1**: El sistema DEBE catalogar toda fuente en `gob.fuente` con campos obligatorios: organismo, URL, licencia, unidad territorial y declaración de datos personales.
- **FR-001-2**: El sistema DEBE registrar cada lote de ingesta en `gob.carga` calculando de forma determinística el hash SHA-256 del archivo físico leído.
- **FR-001-3**: El sistema DEBE registrar las evaluaciones de calidad en `gob.control_calidad` distinguiendo reglas `bloqueante` de `advertencia`.
- **FR-001-4**: El sistema DEBE garantizar que ninguna tabla en esquemas persistentes (`gob`, `core`, `mart`) contenga identificadores individuales directos o indirectos.
- **FR-001-5**: La base de datos DEBE reconstruirse en una base temporal (`.tmp.duckdb`) y únicamente reemplazar la base oficial tras la superación del 100% de los controles bloqueantes.

### Key Entities
- **gob.fuente**: Catálogo maestro de procedencia, titularidad y características de las fuentes de información.
- **gob.carga**: Registro histórico inmutable de archivos procesados, checksums, volumen de registros y marcas temporales.
- **gob.control_calidad**: Registro de auditoría con la ejecución de invariantes metodológicas y de datos.

## Success Criteria *(mandatory)*

### Measurable Outcomes
- **SC-001-1**: 100% de los archivos procesados cuentan con hash SHA-256 registrado en `gob.carga`.
- **SC-001-2**: 0 columnas con datos personales en esquemas persistentes comprobado por `sin_datos_personales = 0`.
- **SC-001-3**: Cero filas de microdatos persistidas en disco fuera de tablas temporales volátiles.
- **SC-001-4**: Pipeline reproducible en menos de 30 segundos en hardware estándar.

## Assumptions
- Los archivos fuente originales (`.rar`, `.zip`) se encuentran versionados o en almacenamiento local seguro (`data/oferta/`, `data/geo/`).
- DuckDB opera en modo archivo local individual (`brujula.duckdb`).
