# Implementation Plan: 006-visualizacion-reportes

**Branch**: `sdd/006-visualizacion-reportes` | **Date**: 2026-10-16 | **Spec**: [spec.md](spec.md)

## Summary
Implementar el prototipo de visualización espacial sobre `mart.sedes_geo` y el generador de reportes ejecutivos reproducibles para el Ministerio de Economía.

## Technical Context
- **Language/Version**: Python 3.12+ (uv)
- **Primary Dependencies**: Streamlit (evaluado), pydeck / folium, Jinja2 / weasyprint (reportes)
- **Storage**: Lectura in-process sobre DuckDB (`data/processed/brujula.duckdb`)
- **Status**: Implementado Incremento Funcional y Auditado Críticamente
- **Architecture**: Capa desacoplada `src/servicios/consultas_oferta.py` (DuckDB in-process) + UI declarativa `src/app/streamlit_app.py` (Altair + PyDeck + Streamlit).

## Constitution Check
- [x] Principio V: Privacidad (Cero microdatos o rutas locales en la UI o reportes).
- [x] Principio IX: Implementación incremental, reutilizando lo existente.
- [x] Principio X: Decisiones de política pública reservadas a responsables humanos.

## Project Structure
```text
specs/006-visualizacion-reportes/
├── spec.md
├── plan.md
├── tasks.md
└── validacion.md

src/
├── servicios/
│   ├── __init__.py
│   └── consultas_oferta.py
├── app/
│   └── streamlit_app.py
└── reportes/
    └── (generador CLI pendiente TASK-008)

tests/
├── test_servicios_oferta.py   # 16 pruebas unitarias de dominio
└── test_streamlit_app.py      # 5 pruebas AppTest de UI
```
