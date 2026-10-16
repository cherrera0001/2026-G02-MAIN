# Implementation Plan: 004-vinculacion-ia

**Branch**: `sdd/004-vinculacion-ia` | **Date**: 2026-10-16 | **Spec**: [spec.md](spec.md)

## Summary
Diseñar e implementar el protocolo de vinculación semántica entre áreas formativas y sectores productivos (`core.vinculo_area_sector`) y la ingesta del indicador de exposición a IA (`core.indicador_area`), manteniendo trazabilidad y auditoría.

## Technical Context
- **Language/Version**: Python 3.12+
- **Primary Dependencies**: scikit-learn / sentence-transformers (propuesta técnica para similitud)
- **Storage**: DuckDB (`core.vinculo_area_sector`, `core.indicador_area`)
- **Status**: BLOQUEADA (0 filas)

## Constitution Check
- [x] Principio I: Evidencia verificable antes de conclusiones.
- [x] Principio III: Separación estricta entre métodos manuales y algorítmicos.
- [x] Principio IV: Reproducibilidad en el cálculo de similitud.

## Project Structure
```text
specs/004-vinculacion-ia/
├── spec.md
├── plan.md
└── tasks.md
```
