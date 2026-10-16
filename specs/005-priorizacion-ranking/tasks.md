# Tasks: 005-priorizacion-ranking

**Input**: `specs/005-priorizacion-ranking/spec.md` y `plan.md`

## Phase 1: Domain Governance & Schema Extension
- [ ] T032 [US1] [#11] Formalizar la Decisión D1 sobre la unidad canónica del ranking.
- [ ] T033 [US2] [#37] Extender `db/schema.sql` con `ejecucion_ranking`, `resultado_ranking` y `aporte_criterio`.
- [ ] T034 [US2] [#36] Documentar definición formal de criterios, sentido y umbral de "evidencia insuficiente".

## Phase 2: Algorithm Implementation (BLOQUEADA POR DATOS)
- [ ] T035 [US2] [#42] Cargar 3 escenarios de pesos en `core.escenario` y `core.peso` validando $\sum w = 1$.
- [ ] T036 [US2] [#38] Implementar función de cálculo de suma ponderada normalizada v0 en Python/SQL.
- [ ] T037 [US2] [#39] Implementar script de reconstrucción determinística de puntajes auditables.
- [ ] T038 [US2] [#40] Documentar formalmente las reglas de normalización y tratamiento de faltantes.

## Phase 3: Uncertainty & Robustness Analysis
- [ ] T039 [US3] [#41] Definir métrica de estabilidad (Spearman $\rho$, solapamiento Top-k) y reglas robusto/sensible.
- [ ] T040 [US3] [#43] Implementar script de comparación de escenarios y reporte de sensibilidad.
