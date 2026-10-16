# Implementation Plan: 003-demanda-productiva

**Branch**: `sdd/003-demanda-productiva` | **Date**: 2026-10-16 | **Spec**: [spec.md](spec.md)

## Summary
Diseñar e implementar la ingesta controlada de indicadores de demanda laboral y vocación productiva territorial, manteniendo el estado BLOCKED hasta que las fuentes sean validadas por el equipo humano.

## Technical Context
- **Language/Version**: Python 3.12+ (uv)
- **Primary Dependencies**: DuckDB >= 1.1, pandas/polars para fuentes externas
- **Storage**: DuckDB (`core.sector`, `core.indicador`, `core.indicador_region_sector`)
- **Status**: BLOQUEADA (0 filas)

## Constitution Check
- [x] Principio I: Evidencia verificable antes de conclusiones (No inventar datos de demanda).
- [x] Principio III: Separación de observación, estimación y propuesta.
- [x] Principio X: Decisiones reservadas a responsables humanos (Decisión D4 / #14).

## Project Structure
```text
specs/003-demanda-productiva/
├── spec.md
├── plan.md
└── tasks.md
```
