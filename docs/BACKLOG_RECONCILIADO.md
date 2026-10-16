# Reconciliación del Backlog y Matriz de Trazabilidad Extremo a Extremo

**Proyecto**: Brújula IA Regional (2026-G02-MAIN)  
**Fecha**: 2026-10-16  
**Sistema de Registro Canónico**: GitHub Issues & GitHub Project [#6](https://github.com/users/cherrera0001/projects/6)  
**Marco Metodológico**: GitHub Spec Kit (Spec-Driven Development)  

---

## 1. Principio de Autoridad Única del Backlog

Para evitar que las especificaciones locales de Spec Kit (`specs/*/tasks.md`) y el repositorio de GitHub se conviertan en dos fuentes de verdad divergentes:

1. **Autoridad Operativa**:
   - **GitHub Issues y el GitHub Project** constituyen la **única autoridad sobre el estado oficial** (`Backlog`, `Ready`, `In progress`, `In review`, `Done`), asignaciones de personas, estimaciones de esfuerzo y asignación de Sprints.
2. **Rol de Spec Kit**:
   - Los archivos `specs/*/tasks.md` y `spec.md` son especificaciones técnicas ejecutables y listas de comprobación a nivel de ingeniería. Toda tarea técnica en Spec Kit consigna el número de Issue oficial de GitHub al que rinde cuentas (sintaxis: `[#ID] Tarea`).
3. **Regla de Cierre Innegociable**:
   - Ningún issue se moverá a `Done` ni se cerrará en GitHub sin **evidencia verificable de cumplimiento** (comando de terminal, salida sin datos personales, test automatizado pasando o documento de decisión ratificado).

---

## 2. Reconciliación de Duplicados Semánticos

La auditoría del producto identificó solapamientos históricos originados en la redacción inicial del `README.md` frente al backlog formalizado en GitHub:

| Concepto Original | Issue Inicial | Historia Propuesta SDD | Análisis de Reconciliación | Resolución Canónica |
|---|---|---|---|---|
| Dónde focalizar los recursos | [#1](https://github.com/cherrera0001/2026-G02-MAIN/issues/1) (R1) | [#8](https://github.com/cherrera0001/2026-G02-MAIN/issues/8) (P-HU04) | R1 es una épica genérica sin criterios comprobables. P-HU04 formaliza el algoritmo de ranking multicriterio. | R1 actúa como Épica de Negocio; su realización técnica se desglosa y audita exclusivamente a través de P-HU04 (#8) y sus tareas #36 a #40. |
| Problemas sectoriales y carreras | [#2](https://github.com/cherrera0001/2026-G02-MAIN/issues/2) (R2) | [#7](https://github.com/cherrera0001/2026-G02-MAIN/issues/7) (P-HU03) | R2 asume "problemas de empresas" no observables en los datos. P-HU03 redefine el desafío como vínculo semántico área formativa–sector económico. | R2 se reinterpreta y ejecuta a través de P-HU03 (#7) y las tareas #31 a #35. |
| Empresas: probar mejoras con IA | [#3](https://github.com/cherrera0001/2026-G02-MAIN/issues/3) (R3) | Fuera del MVP | Describe un beneficio transaccional de una empresa, no una funcionalidad analítica para el Ministerio. | Permanece en GitHub como registro histórico de alcance futuro (`Fuera del MVP`). No se asignan tareas de construcción para el MVP. |
| Talento formado cerca | [#4](https://github.com/cherrera0001/2026-G02-MAIN/issues/4) (R4) | [#5](https://github.com/cherrera0001/2026-G02-MAIN/issues/5) (P-HU01) y [#10](https://github.com/cherrera0001/2026-G02-MAIN/issues/10) (P-HU06) | R4 plantea la consulta desde la empresa local. Los datos y el destinatario corresponden al analista del Ministerio. | La capacidad analítica de oferta territorial se cubre en P-HU01 (#5) y la vista espacial en P-HU06 (#10 y #44). |

---

## 3. Matriz de Trazabilidad Extremo a Extremo

$$\text{Fuente} \to \text{Requisito} \to \text{Historia} \to \text{Modelo de Datos} \to \text{Transformación} \to \text{Prueba} \to \text{Resultado} \to \text{Issue}$$

| Issue | Tipo | Capacidad SDD | Fuente de Origen | Requisito Funcional | Entidad / Tabla BD | Transformación / Lógica | Prueba de Verificación | Estado Real |
|---|---|---|---|---|---|---|---|---|
| **#18** | Decisión | 001-gobernanza | Repositorio | D8 — Datos versionados | `data/oferta`, `data/geo` | Retención de comprimidos en Git | Git status / LFS check | Pendiente |
| **#23** | Investigación | 001-gobernanza | SENCE | Ficha ENADEL | `gob.fuente` | Ficha técnica estructurada | Inspección de `PLANTILLA_FICHA.md` | Pendiente |
| **#24** | Investigación | 001-gobernanza | Gob. Regionales | Ficha ERD | `gob.fuente` | Ficha técnica de prioridades | Inspección documental | Pendiente |
| **#25** | Investigación | 001-gobernanza | Banco Central | Ficha PIB Regional | `gob.fuente` | Ficha cuentas nacionales | Inspección documental | Pendiente |
| **#26** | Investigación | 001-gobernanza | SII | Ficha Empresas SII | `gob.fuente` | Ficha estadísticas rubros | Inspección documental | Pendiente |
| **#27** | Investigación | 001-gobernanza | INE | Ficha ENE Empleo | `gob.fuente` | Ficha encuesta de empleo | Inspección documental | Pendiente |
| **#28** | Investigación | 001-gobernanza | Múltiples | Inventario fuentes | `gob.fuente` | Matriz comparativa de viabilidad | Evaluación de cobertura y licencia | Pendiente |
| **#19** | Tarea | 002-oferta | Mineduc 2025 | FR-002-2 (Niveles y modalidad) | `core.nivel_carrera`, `core.programa` | Regla `ELEGIBLE_TESIS` y filtro | Conteo de excluidos por regla | Parcial (código inicial) |
| **#20** | Tarea | 002-oferta | Mineduc 2025 | FR-002-1 (Oferta reproducible) | `core.titulacion`, `mart.oferta` | Script agregación territorial | `titulos_conservados = 1` | Implementada / Probada |
| **#21** | Tarea | 002-oferta | Mineduc 2025 | FR-002-5 (Supresión celdas) | `mart.oferta`, `mart.especializacion` | Filtro paramétrico $n < \tau$ | Consulta de distribución de celdas | Pendiente |
| **#22** | Tarea | 002-oferta | Mineduc 2025 | FR-002-4 (Cociente especializ.) | `mart.especializacion` | Función ventana DuckDB (LQ) | Estadísticas de distribución LQ | Implementada / Probada |
| **#12** | Decisión | 002-oferta | Mineduc 2025 | D2 — Regiones incluidas | `core.region` | Selección 16 regiones vs piloto | `SELECT count(*) FROM core.region` | Pendiente |
| **#13** | Decisión | 002-oferta | Mineduc 2025 | D3 — Niveles elegibles | `core.nivel_carrera` | Inclusión/exclusión técnicos | Medición del 44.85% pendiente | Pendiente |
| **#16** | Decisión | 002-oferta | Mineduc 2025 | D6 — Umbral celdas | `mart.especializacion` | Fijación umbral secreto estadístico | Medición celdas $n < 5$ | Pendiente |
| **#30** | Tarea | 003-demanda | CIIU | FR-003-1 (Clasif. sectorial) | `core.sector` | Carga catálogo económico | `SELECT count(*) FROM core.sector` | Bloqueada (0 filas) |
| **#14** | Decisión | 003-demanda | Varias | D4 — Fuentes demanda e IA | `core.indicador` | Protocolo ante ausencia de datos | Dictamen de fuentes externas | Pendiente |
| **#29** | Investigación | 004-vinculacion | OIT / FMI | Ficha índices IA | `gob.fuente`, `core.indicador_area` | Ficha metodología internacional | Inspección de literatura | Pendiente |
| **#31** | Tarea | 004-vinculacion | Metodología | FR-004-4 (Protocolo vínculo) | `core.vinculo_area_sector` | Protocolo muestra y métrica | Documento de protocolo previo | Pendiente |
| **#32** | Tarea | 004-vinculacion | Manual | FR-004-2 (Tabla puente manual) | `core.vinculo_area_sector` | Etiquetado muestra de control | Conteo registros revisados | Pendiente |
| **#33** | Tarea | 004-vinculacion | Algorítmica | FR-004-1 (Vínculo semántico) | `core.vinculo_area_sector` | Script de embeddings / similitud | Pipeline determinístico reproducible | Bloqueada (0 filas) |
| **#34** | Tarea | 004-vinculacion | Validación | FR-004-4 (Contraste semántico) | Matriz de confusión | Cálculo de concordancia (Kappa/F1) | Comparación contra umbral | Bloqueada |
| **#35** | Tarea | 004-vinculacion | OIT / FMI | FR-004-3 (Indicador IA en área) | `core.indicador_area` | Ingesta indicador tecnológico | `SELECT count(*) FROM core.indicador_area` | Bloqueada (0 filas) |
| **#11** | Decisión | 005-ranking | Negocio | D1 — Unidad del ranking | `core.resultado_ranking` | Ratificación (región × área × IES) | Documento de acuerdo de dominio | Pendiente |
| **#36** | Tarea | 005-ranking | Metodología | Criterios y sentido del ranking | `core.criterio` | Definición "evidencia insuficiente" | Revisión técnica de criterios | Bloqueada |
| **#37** | Tarea | 005-ranking | Esquema BD | FR-005-2 (Extender esquema) | `core.ejecucion_ranking`, etc. | Migración DDL DuckDB | `information_schema.tables` | Pendiente |
| **#38** | Tarea | 005-ranking | Algorítmica | FR-005-3 (Cálculo ranking v0) | `core.resultado_ranking` | Algoritmo suma ponderada normalizada | Script de cálculo ejecutable | Bloqueada |
| **#39** | Tarea | 005-ranking | Auditoría | FR-005-1 (Script reconstrucción) | `core.aporte_criterio` | Deconstrucción determinística | Diferencia $< 10^{-6}$ | Bloqueada |
| **#40** | Tarea | 005-ranking | Documentación | Documentación reglas de cálculo | Guía metodológica | Redacción fórmula y normalización | Aprobación por revisor QA | Bloqueada |
| **#41** | Tarea | 005-ranking | Metodología | Definir métrica estabilidad | Matriz correlación | Reglas de clasificación robusta | Documento metodológico | Bloqueada |
| **#42** | Tarea | 005-ranking | Paramétrica | FR-005-3 (Escenarios y pesos) | `core.escenario`, `core.peso` | Carga 3 escenarios ($\sum w = 1$) | Restricción CHECK suma 1 | Bloqueada (0 filas) |
| **#43** | Tarea | 005-ranking | Evaluación | Comparar escenarios | Reporte sensibilidad | Correlación Spearman / Top-5 | Script reproducible de análisis | Bloqueada |
| **#15** | Decisión | 006-reportes | Producto | D5 — Usuario principal MVP | Alcance plataforma | Ratificación usuario Ministerio | Actualización README | Pendiente |
| **#17** | Decisión | 006-reportes | Arquitectura | D7 — Tecnología interfaz | Stack técnico | Selección Streamlit vs API | Decisión ADR aprobada | Pendiente |
| **#44** | Tarea | 006-reportes | Geoportal 2020 | FR-006-2 (Prototipo mapa oferta) | `mart.sedes_geo` | Componente cartográfico sedes | Renderizado de 1.297 puntos | Parcial (vista lista) |
| **#45** | Tarea | 006-reportes | UI | Vista prioridades regional | Interfaz web | Pantalla de ranking territorial | Prueba interactiva | Bloqueada |
| **#46** | Tarea | 006-reportes | Reporting | FR-006-3 (Generador de reporte) | Reporte PDF/Markdown | Script generación documental | Salida ejecutable sin errores | Pendiente |
| **#47** | Tarea | 006-reportes | Auditoría | FR-006-4 (Checklist del reporte) | Lista comprobación | Auditoría de fuente/fecha/privacidad | Check exhaustivo sin advertencias | Pendiente |

---

## 4. Estado de Cumplimiento Consolidado

- **Total de Issues Auditados**: 47 (10 Historias, 22 Tareas, 7 Investigaciones, 8 Decisiones).
- **Capacidades Operativas con Datos**:
  - `001-gobernanza-fuentes`: **Operativa en base** (trazabilidad y calidad funcionando).
  - `002-oferta-formativa`: **Operativa en base** (100% cuadre, 328.998 títulos, pendientes decisiones de exclusión).
- **Capacidades Bloqueadas Científicamente**:
  - `003-demanda-productiva`: **Bloqueada** (requiere ingesta externa de demanda y sectores).
  - `004-vinculacion-ia`: **Bloqueada** (requiere protocolo de vinculación e indicador IA).
  - `005-priorizacion-ranking`: **Bloqueada** (requiere cerrar D1, D3 y contar con factores 003 y 004).
  - `006-visualizacion-reportes`: **Parcial / Pendiente** (capa de datos espacial lista; interfaz y reportes pendientes de codificar).
