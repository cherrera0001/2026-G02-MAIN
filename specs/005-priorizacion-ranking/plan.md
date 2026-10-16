# Implementation Plan: 005-priorizacion-ranking

**Branch**: `sdd/005-priorizacion-ranking` | **Date**: 2026-10-16 | **Spec**: [spec.md](spec.md)

## Summary
Diseñar el motor de ranking multicriterio reproducible y extensible, incorporando persistencia histórica (`ejecucion_ranking`, `resultado_ranking`, `aporte_criterio`) y análisis de sensibilidad de pesos, manteniendo el cálculo bloqueado hasta que los datos empíricos existan.

## Technical Context
- **Language/Version**: Python 3.12+ (uv)
- **Primary Dependencies**: DuckDB >= 1.1, scipy / numpy para análisis de sensibilidad
- **Storage**: DuckDB (`core.criterio`, `core.escenario`, `core.peso` + tablas de resultado)
- **Status**: BLOQUEADA CIENTÍFICAMENTE

## Constitution Check
- [x] Principio I: Evidencia verificable antes de conclusiones.
- [x] Principio VII: Transparencia y deconstrucción del modelo de priorización.
- [x] Principio VIII: Incertidumbre y análisis de sensibilidad (mínimo 3 escenarios).
- [x] Principio X: Decisiones reservadas a autoridades humanas.

## Project Structure
```text
specs/005-priorizacion-ranking/
├── spec.md
├── plan.md
└── tasks.md
```
