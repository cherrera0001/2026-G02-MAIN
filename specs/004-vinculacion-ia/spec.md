# Feature Specification: 004-vinculacion-ia

**Feature Branch**: `sdd/004-vinculacion-ia`  
**Created**: 2026-10-16  
**Status**: Bloqueada por Ausencia de Protocolo Metodológico y Fuentes de IA  
**Input**: Requisitos de vinculación semántica entre oferta formativa y sectores productivos, e índices de exposición/complementariedad con IA. Issues relacionados: #2, #7, #29, #31, #32, #33, #34, #35.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Tabla Puente Área Formativa a Sector Productivo (Priority: P1 - BLOQUEADA)
Como analista ministerial, quiero consultar qué áreas de formación profesional y técnica se vinculan con cada sector económico, conociendo si la asociación fue generada algorítmicamente o validada por un experto humano, para diseñar líneas temáticas pertinentes de tesis.

**Why this priority**: Conecta la oferta de talento con las necesidades industriales (P-HU03 / R2). Resuelve el problema fundamental de que las carreras se clasifican en CINE-UNESCO y las empresas en CIIU.

**Independent Test**: Consultar `core.vinculo_area_sector`. Exigir que todo registro tenga `puntaje BETWEEN 0 AND 1`, `metodo IN ('manual', 'semantico')` y `estado IN ('sugerido', 'revisado', 'rechazado')`.

**Acceptance Scenarios**:
1. **Given** una carrera (ej. Agronomía) y un sector (ej. Agricultura), **When** se evalúa el vínculo, **Then** el sistema presenta el puntaje de afinidad y la justificación metodológica documentada.
2. **Given** una vinculación puramente semántica (modelo de lenguaje / embeddings), **When** se presenta en la plataforma, **Then** queda explícitamente etiquetada como `sugerido` hasta que una revisión manual fije su estado como `revisado`.

---

### User Story 2 - Protocolo de Validación y Calibración de Similitud Semántica (Priority: P2)
Como científico de datos del equipo, quiero contrastar el algoritmo de vinculación semántica contra una muestra representativa etiquetada manualmente, para asegurar que la precisión supere el umbral fijado antes de poblar la base.

**Why this priority**: Evita alucinaciones o asociaciones absurdas (ej. vincular Filosofía con Minería por artefactos léxicos). Cumple el criterio de reproducibilidad y rigor empírico (#31, #34).

**Independent Test**: Ejecutar el script de evaluación comparando predicciones algorítmicas vs ground truth manual sobre una muestra de tamaño $n \ge 50$ fijada a priori.

**Acceptance Scenarios**:
1. **Given** la matriz de confusión del contraste, **When** la métrica de concordancia (F1-score o Kappa de Cohen) es inferior al umbral mínimo acordado (ej. 0.75), **Then** el vínculo no se promueve a producción y se bloquea su uso en el ranking.

---

### User Story 3 - Indicador de Exposición y Complementariedad con IA (Priority: P1 - BLOQUEADA)
Como investigador de mercado laboral, quiero disponer de un índice objetivo de exposición ocupacional o complementariedad tecnológica a la Inteligencia Artificial por área de conocimiento, para orientar los subsidios donde el impacto transformador sea mayor.

**Why this priority**: Da sentido a la misión de "Brújula IA Regional". Sin este indicador, el programa subsidiaría tesis convencionales sin componente tecnológico (#29, #35).

**Independent Test**: Consultar `core.indicador_area`. Si no existe fuente pública verificada (ej. OIT, FMI, Felten et al.), la tabla debe permanecer vacía y el criterio debe declararse como "sin evidencia".

**Acceptance Scenarios**:
1. **Given** que no se ha validado una fuente metodológica de exposición a IA a nivel de carrera en Chile, **When** se evalúa el modelo, **Then** el sistema declara explícitamente "Sin Evidencia" y no inventa puntajes aleatorios.

---

## Edge Cases

- ¿Qué ocurre si un área formativa es transversal (ej. Ingeniería Comercial o Informática) y se relaciona con todos los sectores? El puntaje de afinidad debe reflejar la intensidad relativa de absorción laboral y no saturar la matriz con unos binarios genéricos.
- ¿Qué ocurre si los índices internacionales de IA (OIT/FMI) están mapeados a códigos ISCO-08 y no a áreas educativas chilenas? Se requiere una doble tabla puente (ISCO-08 -> CINE-UNESCO -> SIES), propagando el error de aproximación.

## Requirements *(mandatory)*

### Functional Requirements
- **FR-004-1**: La tabla `core.vinculo_area_sector` DEBE almacenar clave compuesta `(id_area_generica, id_sector)` con puntaje continuo en $[0, 1]$.
- **FR-004-2**: Todo registro en `core.vinculo_area_sector` DEBE consignar método ('manual', 'semantico'), estado ('sugerido', 'revisado', 'rechazado') y justificación textual.
- **FR-004-3**: La tabla `core.indicador_area` DEBE enlazar a `core.indicador` con su respectivo `id_fuente` y `tipo_evidencia`.
- **FR-004-4**: Se DEBE fijar el protocolo de evaluación previa con tamaño muestral y umbral cuantitativo antes de ejecutar la carga automática.

### Key Entities
- **core.vinculo_area_sector**: Matriz relacional de articulación formativa-productiva.
- **core.indicador_area**: Caracterización del potencial y riesgo tecnológico por disciplina.

## Success Criteria *(mandatory)*

### Measurable Outcomes
- **SC-004-1**: Elaboración de la ficha técnica de fuentes internacionales de IA (#29).
- **SC-004-2**: Protocolo de validación aprobado con muestra mínima de 50 pares área-sector (#31).
- **SC-004-3**: Cero afirmaciones sobre "complementariedad con IA" que carezcan de cita a fuente y fecha.

## Assumptions
- Los índices de exposición a IA provenientes de economías desarrolladas requieren calibración para la estructura ocupacional de Chile y sus regiones.
