# Feature Specification: 005-priorizacion-ranking

**Feature Branch**: `sdd/005-priorizacion-ranking`  
**Created**: 2026-10-16  
**Status**: Bloqueada Científica y Arquitecturalmente  
**Input**: Requisitos de ordenamiento multicriterio transparente, reconstrucción de puntajes, persistencia de ejecuciones y análisis de robustez ante variación de pesos. Issues relacionados: #1, #8, #9, #11, #36, #37, #38, #39, #40, #41, #42, #43.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Resolución de la Unidad de Análisis del Ranking (Priority: P1 - BLOQUEADA)
Como Product Owner y comité técnico ministerial, quiero definir formalmente la unidad de análisis del ranking (Decisión D1 / #11), resolviendo la contradicción entre la unidad del README (región × área genérica × institución) y la propuesta del piloto (carrera × sector en región piloto), para fijar el grano relacional del algoritmo.

**Why this priority**: Es la decisión estructural que rige todo el producto. Si la unidad es por institución, responde a *quién financiar*; si es por sector, responde a *qué tema investigar*. Ambas no son sustituibles sin un modelo anidado formal.

**Independent Test**: Verificar que la definición de unidad esté ratificada por escrito y que la clave primaria de los resultados refleje unívocamente dicha tupla.

**Acceptance Scenarios**:
1. **Given** la decisión D1 formalizada, **When** se evalúa el grano del modelo, **Then** todas las especificaciones y vistas dependientes se alinean a una sola fuente de verdad sin ambigüedades.

---

### User Story 2 - Algoritmo Multicriterio Transparente y Reconstruible (Priority: P1 - BLOQUEADA)
Como analista del Ministerio, quiero que el puntaje final de cada combinación se obtenga mediante una suma ponderada normalizada con desglose por criterio, para auditar y justificar públicamente por qué una opción quedó priorizada.

**Why this priority**: Exigencia legal y ética de la política pública (Constitución Principio VII). El Estado no puede adjudicar fondos mediante modelos opacos.

**Independent Test**: Ejecutar el script de reconstrucción (#39) sobre cualquier registro: $Score = \sum_{i} w_i \cdot \text{Norm}(x_i)$. La diferencia absoluta entre el puntaje guardado y el reconstruido debe ser menor a $10^{-6}$.

**Acceptance Scenarios**:
1. **Given** un conjunto de criterios normalizados en $[0, 1]$ y un vector de pesos con $\sum w_i = 1$, **When** se calcula el ranking, **Then** el sistema almacena la posición, el puntaje global y la contribución exacta ($w_i \cdot \tilde{x}_i$) de cada factor.
2. **Given** una combinación con ausencia de datos en un criterio, **When** se calcula su valor, **Then** los nulos no se penalizan artificialmente con 0; se documenta como "evidencia insuficiente" y se recalcula con pesos renormalizados.

---

### User Story 3 - Análisis de Sensibilidad y Estabilidad de Escenarios (Priority: P2 - BLOQUEADA)
Como responsable del programa ministerial, quiero evaluar la estabilidad de las recomendaciones ante al menos tres escenarios de ponderación (base, pro-demanda regional, pro-adopción IA), para defender las decisiones con evidencia robusta y no arbitraria.

**Why this priority**: Cumple el Principio VIII de la Constitución. Distingue opciones que lideran consistentemente de aquellas que son artefactos de la elección de pesos (#41, #42, #43).

**Independent Test**: Calcular la correlación de rangos de Spearman ($\rho$) y el solapamiento del Top-10 entre escenarios. Clasificar cada recomendación como "robusta" si permanece en el decil superior en todos los escenarios, o "sensible" si oscila significativamente.

**Acceptance Scenarios**:
1. **Given** el escenario base y dos escenarios alternativos, **When** se ejecuta la comparación, **Then** el sistema genera un informe cuantitativo de robustez y rotula las combinaciones sensibles.

---

## Edge Cases

- ¿Qué ocurre si dos combinaciones obtienen exactamente el mismo puntaje final? Se deben definir criterios explícitos de desempate determinísticos (ej. mayor volumen de titulados o mayor cociente de especialización territorial), sin recurrir a ordenamientos aleatorios.
- ¿Qué ocurre si un criterio tiene sentido inverso ("menor es mejor", ej. tasa de desempleo)? El esquema en `core.criterio.sentido` prevé `'menor_es_mejor'`. La normalización debe invertir la escala: $\tilde{x} = \frac{\max(x) - x}{\max(x) - \min(x)}$.

## Requirements *(mandatory)*

### Functional Requirements
- **FR-005-1**: El sistema DEBE resolver formalmente la Decisión D1 antes de activar el motor de cálculo.
- **FR-005-2**: El esquema DEBE extenderse incorporando tablas físicas de persistencia histórica: `ejecucion_ranking`, `resultado_ranking` y `aporte_criterio`.
- **FR-005-3**: Los pesos en `core.peso` DEBEN satisfacer estrictamente la restricción de normalización $\sum_{i} w_i = 1.0$ dentro de cada escenario.
- **FR-005-4**: El algoritmo DEBE aislar el efecto de faltantes, impidiendo que la carencia de datos se interprete como puntaje cero.
- **FR-005-5**: El sistema DEBE emitir estado `BLOCKED` y rechazar la publicación de un ranking oficial mientras las fuentes empíricas de demanda e IA no estén cargadas y validadas.

### Key Entities
- **core.criterio**: Definición de dimensiones evaluadas y su sentido de optimización.
- **core.escenario**: Configuración de supuestos metodológicos y perfiles de ponderación.
- **core.peso**: Distribución paramétrica de pesos por criterio dentro de un escenario.
- **core.ejecucion_ranking** *(propuesta)*: Metadata de corrida (fecha, commit, versión, hash de datos).
- **core.resultado_ranking** *(propuesta)*: Posición, puntaje y clasificación de robustez.
- **core.aporte_criterio** *(propuesta)*: Desglose vectorial de la contribución al puntaje total.

## Success Criteria *(mandatory)*

### Measurable Outcomes
- **SC-005-1**: 100% de los puntajes auditables mediante script de reconstrucción determinística.
- **SC-005-2**: Correlación de rangos de Spearman ($\rho$) y métricas de solapamiento Top-N calculadas entre 3 escenarios.
- **SC-005-3**: Bloqueo estricto del cálculo hasta que se satisfagan los requisitos de datos mínimos.

## Assumptions
- No se publicará un ranking unilateral o arbitrario sin acuerdo formal del usuario principal (Ministerio).

## Integración aprobada con SDD-006
La UI oficial es Streamlit (ADR-002), consumidora de resultados del dominio y DuckDB, sin fórmulas en widgets. El bloqueo FR-005-5 se expone en UI y exportaciones. La política de faltantes, renormalización, desempates y sensibilidad descrita arriba requiere validación metodológica antes de ejecutarse; no constituye aprobación científica por estar escrita. Las pruebas de reconstrucción matemática permanecen independientes de AppTest.
