# Implementation Plan: 001-gobernanza-fuentes

**Branch**: `sdd/001-gobernanza-fuentes` | **Date**: 2026-10-16 | **Spec**: [spec.md](spec.md)

## Summary
Implementar y auditar la capa de gobierno de datos, linaje criptográfico y controles de calidad automáticos sobre DuckDB en `src/pipeline/construir_bd.py` y `db/schema.sql`.

## Technical Context
- **Language/Version**: Python 3.12+ (uv)
- **Primary Dependencies**: DuckDB >= 1.1, dbfread >= 2.0
- **Storage**: DuckDB local (`data/processed/brujula.duckdb`), esquemas `gob` y `core`
- **Testing**: Invariantes en `gob.control_calidad`
- **Performance Goals**: Reconstrucción completa y validación en < 30 segundos

## Constitution Check
- [x] Principio I: Evidencia verificable antes de conclusiones (Cada dato parte de un archivo en `data/raw/`).
- [x] Principio II: Trazabilidad de fuentes (Hash SHA-256 persistido en `gob.carga`).
- [x] Principio IV: Reproducibilidad (Pipeline 100% determinístico sin estado previo).
- [x] Principio V: Privacidad (Control `sin_datos_personales = 0`).

## Project Structure
```text
specs/001-gobernanza-fuentes/
├── spec.md
├── plan.md
└── tasks.md

src/pipeline/
└── construir_bd.py

db/
└── schema.sql
```
