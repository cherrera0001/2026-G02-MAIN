# Implementation Plan: 002-oferta-formativa

**Branch**: `sdd/002-oferta-formativa` | **Date**: 2026-10-16 | **Spec**: [spec.md](spec.md)

## Summary
Estructurar y auditar la oferta formativa territorial en DuckDB a partir de las fuentes censales de Mineduc 2025 y Geoportal 2020, formalizando las vistas `mart.oferta` y `mart.especializacion`.

## Technical Context
- **Language/Version**: Python 3.12+ (uv)
- **Primary Dependencies**: DuckDB >= 1.1, dbfread >= 2.0
- **Storage**: DuckDB (`core.titulacion`, `core.programa`, `mart.oferta`, `mart.especializacion`)
- **Testing**: Pruebas de cuadre y no-nulidad

## Constitution Check
- [x] Principio III: Separación de observación y propuesta (Datos censales no imputados).
- [x] Principio VI: Comparabilidad territorial (Cálculo del Cociente de Especialización LQ).

## Project Structure
```text
specs/002-oferta-formativa/
├── spec.md
├── plan.md
└── tasks.md

src/pipeline/
└── construir_bd.py

db/
└── schema.sql
```
