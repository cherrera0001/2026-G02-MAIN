# Tasks: 001-gobernanza-fuentes

**Input**: `specs/001-gobernanza-fuentes/spec.md` y `plan.md`

## Phase 1: Setup & Data Ingestion
- [x] T001 [P] [US1] [#18] Preservar archivos originales en `data/oferta/` y `data/geo/` sin microdatos en Git.
- [x] T002 [US1] [#20] Extraer y registrar fuentes en `gob.fuente` (`src/pipeline/construir_bd.py`).
- [x] T003 [US1] [#20] Computar hash SHA-256 e insertar lote en `gob.carga` (`src/pipeline/construir_bd.py`).

## Phase 2: Quality Assurance & Privacy Gates
- [x] T004 [US2] [#20] Implementar control `sin_datos_personales = 0` sobre `information_schema.columns`.
- [x] T005 [US2] [#20] Implementar control `titulos_conservados = 1` y `cargas_huerfanas = 0`.
- [x] T006 [US2] [#20] Implementar mecanismo atómico de sustitución de base (`.tmp.duckdb -> brujula.duckdb`).

## Phase 3: Research & External Sources Evaluation
- [ ] T007 [P] [US3] [#23] Completar ficha técnica ENADEL (SENCE) en `docs/fuentes/`.
- [ ] T008 [P] [US3] [#24] Completar ficha técnica Estrategias Regionales de Desarrollo (ERD).
- [ ] T009 [P] [US3] [#25] Completar ficha técnica PIB Regional (Banco Central).
- [ ] T010 [P] [US3] [#26] Completar ficha técnica Estadísticas de Empresas (SII).
- [ ] T011 [P] [US3] [#27] Completar ficha técnica Encuesta Nacional de Empleo (INE).
- [ ] T012 [US3] [#28] Elaborar inventario comparativo y dictamen de viabilidad de fuentes externas.
