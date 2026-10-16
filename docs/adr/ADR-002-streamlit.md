# ADR-002 — Streamlit como interfaz del MVP
Estado: Aceptada por el responsable | Fecha: 2026-10-16

## Contexto y decisión
La base existente es Python >=3.12, DuckDB y uv, con un pipeline y marts agregados. Se adopta Streamlit como interfaz oficial del MVP analítico. No se reabre la selección de framework salvo incompatibilidad técnica demostrada.

## Consecuencias
Se conserva `src/pipeline/construir_bd.py` y `db/schema.sql`. La UI consume servicios de dominio y consultas DuckDB en lectura; no calcula fórmulas de ranking. No se requiere API ni otro almacén. Streamlit aún no está instalado: su versión compatible y AppTest se verifican al ejecutar TASK-001; esta decisión no afirma que ya exista una app.

No se despliega hasta aprobar qué datos pueden publicarse. El ranking sigue bloqueado hasta validar fuentes, unidad, criterios, ponderaciones y metodología. Véanse plan y contrato de datos de la feature 006.
