# Tasks: 002-oferta-formativa

**Input**: `specs/002-oferta-formativa/spec.md` y `plan.md`

## Phase 1: Educational Offer Pipeline & Staging
- [x] T013 [US1] [#20] Reconstrucción de la tabla de oferta agregada con cuadre total de 328.998 títulos.
- [x] T014 [US1] [#20] Deduplicación y normalización de programas académicos por código SIES en `core.programa`.
- [x] T015 [US1] [#20] Normalización de comunas y resolución de llaves geográficas Mineduc–Geoportal.

## Phase 2: Business Logic & Policy Filters
- [x] T016 [US2] [#19] Clasificación inicial de niveles formativos en `core.nivel_carrera` mediante `ELEGIBLE_TESIS`.
- [ ] T017 [US2] [#13] Resolución formal de la Decisión D3 por el Product Owner (definición del 44.85% pendiente).
- [ ] T018 [US2] [#19] Parametrización en pipeline para filtrar títulos no presenciales (aislamiento de 82.525 títulos).

## Phase 3: Spatial Analysis & Normalization
- [x] T019 [US3] [#22] Implementación del cálculo del Cociente de Especialización en `mart.especializacion`.
- [ ] T020 [US3] [#21] [#16] Implementar supresión o agrupamiento paramétrico para celdas con $n < \tau$.
