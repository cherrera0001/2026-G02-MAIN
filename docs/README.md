# Índice Canónico de Documentación — Brújula IA Regional

Bienvenido a la documentación oficial y canónica del proyecto **Brújula IA Regional**, modernizado bajo el estándar **GitHub Spec Kit** (Spec-Driven Development).

---

## 1. Documentos Fundacionales y Gobernanza

- [**Constitución SDD**](../.specify/memory/constitution.md): Principios innegociables de desarrollo, privacidad, rigor empírico y gobernanza del proyecto.
- [**Contexto para Agentes (CLAUDE.md)**](../CLAUDE.md): Directrices operativas, límites de actuación de subagentes y definiciones de terminado.
- [**Registro de Decisiones Pendientes (ADR Log)**](decisiones/REGISTRO_DECISIONES_PENDIENTES.md): Seguimiento de las 8 decisiones de producto abiertas (D1 a D8).
- [**Backlog Reconciliado y Matriz de Trazabilidad**](BACKLOG_RECONCILIADO.md): Mapeo completo extremo a extremo de los 47 issues de GitHub contra especificaciones y base de datos.
- [**Índice Histórico de Backlog**](BACKLOG.md): Publicación del catálogo original de issues en GitHub Projects.

---

## 2. Especificaciones de Producto por Capacidad (Spec Kit)

Las especificaciones técnicas ejecutables, planes y tareas atómicas residen en el directorio `specs/`:

1. [**001 - Gobernanza y Linaje de Fuentes**](../specs/001-gobernanza-fuentes/spec.md) | [Plan](../specs/001-gobernanza-fuentes/plan.md) | [Tareas](../specs/001-gobernanza-fuentes/tasks.md)
2. [**002 - Oferta Formativa Territorial**](../specs/002-oferta-formativa/spec.md) | [Plan](../specs/002-oferta-formativa/plan.md) | [Tareas](../specs/002-oferta-formativa/tasks.md)
3. [**003 - Demanda y Vocación Productiva (BLOCKED)**](../specs/003-demanda-productiva/spec.md) | [Plan](../specs/003-demanda-productiva/plan.md) | [Tareas](../specs/003-demanda-productiva/tasks.md)
4. [**004 - Vinculación Semántica e IA (BLOCKED)**](../specs/004-vinculacion-ia/spec.md) | [Plan](../specs/004-vinculacion-ia/plan.md) | [Tareas](../specs/004-vinculacion-ia/tasks.md)
5. [**005 - Motor de Priorización y Ranking (BLOCKED)**](../specs/005-priorizacion-ranking/spec.md) | [Plan](../specs/005-priorizacion-ranking/plan.md) | [Tareas](../specs/005-priorizacion-ranking/tasks.md)
6. [**006 - Visualización Territorial y Reportes**](../specs/006-visualizacion-reportes/spec.md) | [Plan](../specs/006-visualizacion-reportes/plan.md) | [Tareas](../specs/006-visualizacion-reportes/tasks.md)

---

## 3. Modelos de Datos y Arquitectura Técnica

- [**MER Conceptual Editable (.drawio)**](modelos/mer_conceptual.drawio): Diagrama editable en diagrams.net con conceptos del dominio.
- [**Modelo Relacional Físico (DBML)**](modelos/modelo_relacional.dbml): Especificación DBML del esquema DuckDB y tablas de extensión propuestas.
- [**Diccionario de Datos y Auditoría Empírica**](modelos/DICCIONARIO_DATOS.md): Descripción campo a campo, granularidad, cardinalidades y consultas de hallazgos.
- [**Matriz de Entidades y Requisitos**](modelos/MATRIZ_ENTIDADES_REQUISITOS.md): Cruce relacional entre tablas de base de datos y requerimientos funcionales.
- [**Arquitectura Mínima del Sistema**](arquitectura/ARQUITECTURA_MINIMA.md): Diagramas C4 de contexto y contenedores, evaluación de Streamlit y flujos de datos.

---

## 4. Análisis Científico y Validación SDD

- [**Validación Científica del Ranking**](analisis/VALIDACION_CIENTIFICA_RANKING.md): Formulación matemática rigurosa, análisis de incertidumbre, tratamiento de faltantes y fundamentación del estado de bloqueo.
- [**Reporte de Validación SDD**](sdd/REPORTE_VALIDACION_SDD.md): Auditoría metodológica integral de Spec Kit con dictámenes PASS/FAIL/BLOCKED.
- [**Auditoría Histórica de Coherencia de Historias**](COHERENCIA_HISTORIAS.md): Análisis comparativo del backlog inicial y paquete de historias M-HU.
- [**Plantilla de Ficha de Fuente**](fuentes/PLANTILLA_FICHA.md): Estándar para registrar y evaluar fuentes candidatas externas.
