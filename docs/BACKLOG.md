# Backlog de Brújula IA Regional

Índice del backlog publicado en GitHub el 5 de octubre de 2026. Fuente de las historias: `README.md` (R1–R4) y `docs/COHERENCIA_HISTORIAS.md` §5 (P-HU01–P-HU06, propuestas para validar). Las decisiones (D1–D8) son las de `CLAUDE.md` y de COHERENCIA §6. Nada proviene del chat del equipo.

- Project: [Brújula IA Regional — Backlog](https://github.com/users/cherrera0001/projects/6). Todas las tarjetas están en `Backlog`, con `Sprint = Pendiente`, sin persona asignada.
- Peso: escala 0–5 del README (sección D); relativo, no horas. Horas estimadas: «por estimar» en todos los issues (sin fundamento para estimarlas todavía). Esfuerzo real: se registra al cerrar.
- Modelo: sugerencia de modelo de Claude Code por issue (guía en `CLAUDE.md`). `propuesta` = el repositorio no acredita aprobación del equipo.

Este archivo es un índice: el contenido vigente es el de cada issue. Al cambiar el backlog, actualizar también esta tabla.

## Historias del README (R1–R4)

| Issue | Historia | Peso global | Modelo | Estado |
|---|---|---|---|---|
| [#1](https://github.com/cherrera0001/2026-G02-MAIN/issues/1) | R1 — Responsable del programa: dónde focalizar los recursos | pendiente | Opus | Criterios pendientes de validar. Bloqueada por las decisiones #11 (unidad del ranking) y #15 (usuario principal). Si el equipo acepta la reformulación #8, hereda su peso global (4). |
| [#2](https://github.com/cherrera0001/2026-G02-MAIN/issues/2) | R2 — Analista del Ministerio: qué problemas sectoriales aborda cada carrera | pendiente | Opus | Criterios pendientes de validar. Bloqueada por #14 (fuentes de demanda, productividad y exposición a IA) y #11. Si el equipo acepta #7, hereda su peso global (5). |
| [#3](https://github.com/cherrera0001/2026-G02-MAIN/issues/3) | R3 — Empresa local: probar mejoras con IA con costo y riesgo acotados | pendiente | Opus | Criterios pendientes de validar. Pendiente: la historia está propuesta fuera del MVP y la decisión #15 sigue abierta. No se estima trabajo de construcción porque no hay datos ni alcance que la sostengan. |
| [#4](https://github.com/cherrera0001/2026-G02-MAIN/issues/4) | R4 — Empresa local: qué talento se forma cerca y en qué áreas | pendiente | Sonnet | Criterios pendientes de validar. Bloqueada por #15 (usuario principal). Si el equipo acepta la reformulación, el trabajo queda cubierto por #5 (peso 3) y la capa de oferta de #10 (peso 4). |

## Historias propuestas (P-HU01–P-HU06) y sus tareas

### [#5](https://github.com/cherrera0001/2026-G02-MAIN/issues/5) P-HU01 — Oferta de titulados por región, área genérica, institución y nivel (propuesta)

**Peso global: 3** — Lo impulsa que la agregación ya existe en `mart.oferta` y `mart.especializacion`; el esfuerzo está en parametrizar niveles, modalidad y umbral sin cerrar decisiones, cuadrar totales y documentar (media jornada con incertidumbre moderada).

Modelo sugerido: Sonnet.

| Issue | Tarea | Tipo | Peso | Modelo |
|---|---|---|---|---|
| [#19](https://github.com/cherrera0001/2026-G02-MAIN/issues/19) | Parametrizar niveles elegibles y modalidad en el pipeline y medir los títulos que excluye cada regla | Tarea | 2 | Sonnet |
| [#20](https://github.com/cherrera0001/2026-G02-MAIN/issues/20) | Script reproducible de la tabla de oferta región × área genérica × institución × nivel con cuadre de totales | Tarea | 2 | Sonnet |
| [#21](https://github.com/cherrera0001/2026-G02-MAIN/issues/21) | Supresión o agrupación de celdas pequeñas parametrizada por umbral, con distribución de celdas para informar la decisión | Tarea | 2 | Sonnet |
| [#22](https://github.com/cherrera0001/2026-G02-MAIN/issues/22) | Documentar el cociente de especialización como indicador y verificar su cálculo | Tarea | 1 | Sonnet |

### [#6](https://github.com/cherrera0001/2026-G02-MAIN/issues/6) P-HU02 — Evidencia pública de demanda y vocación productiva por región (propuesta)

**Peso global: 4** — Cinco fuentes externas por verificar con un procedimiento conocido (plantilla de ficha) de 2–3 h cada una, más un inventario comparativo: una jornada larga de trabajo paralelizable. La incertidumbre está en el resultado (si las fuentes sirven), que se cierra en #14, no en el método.

Modelo sugerido: Sonnet.

| Issue | Tarea | Tipo | Peso | Modelo |
|---|---|---|---|---|
| [#23](https://github.com/cherrera0001/2026-G02-MAIN/issues/23) | Ficha de fuente: ENADEL (SENCE), demanda de ocupaciones y competencias | Investigación | 2 | Sonnet |
| [#24](https://github.com/cherrera0001/2026-G02-MAIN/issues/24) | Ficha de fuente: Estrategias Regionales de Desarrollo (sectores prioritarios declarados) | Investigación | 2 | Sonnet |
| [#25](https://github.com/cherrera0001/2026-G02-MAIN/issues/25) | Ficha de fuente: PIB regional por actividad económica (Banco Central) | Investigación | 2 | Sonnet |
| [#26](https://github.com/cherrera0001/2026-G02-MAIN/issues/26) | Ficha de fuente: estadísticas de empresas por región y rubro (SII) | Investigación | 2 | Sonnet |
| [#27](https://github.com/cherrera0001/2026-G02-MAIN/issues/27) | Ficha de fuente: Encuesta Nacional de Empleo (INE), ocupados por región y rama | Investigación | 2 | Sonnet |
| [#28](https://github.com/cherrera0001/2026-G02-MAIN/issues/28) | Inventario comparativo de fuentes de demanda y vocación productiva con veredicto propuesto | Investigación | 2 | Sonnet |

### [#7](https://github.com/cherrera0001/2026-G02-MAIN/issues/7) P-HU03 — Vínculo entre áreas de formación y sectores prioritarios (propuesta)

**Peso global: 5** — Incertidumbre alta: no hay fuente de sectores ni de IA validada, el método semántico no está definido y la aceptación depende de un contraste manual con umbral fijado de antemano. Más de una jornada en cualquier escenario; por eso se divide en siete tareas de peso 1 a 3.

Modelo sugerido: Opus.

| Issue | Tarea | Tipo | Peso | Modelo |
|---|---|---|---|---|
| [#29](https://github.com/cherrera0001/2026-G02-MAIN/issues/29) | Ficha de fuente: índices de exposición o complementariedad ocupacional con IA (OIT, FMI u otros) | Investigación | 2 | Sonnet |
| [#30](https://github.com/cherrera0001/2026-G02-MAIN/issues/30) | Proponer la clasificación sectorial de referencia y preparar la carga parametrizada de core.sector | Tarea | 2 | Sonnet |
| [#31](https://github.com/cherrera0001/2026-G02-MAIN/issues/31) | Protocolo de validación del vínculo área–sector: muestra, métrica y umbral fijados antes de calcular | Tarea | 1 | Sonnet |
| [#32](https://github.com/cherrera0001/2026-G02-MAIN/issues/32) | Tabla puente área genérica–sector, versión manual sobre la muestra (método manual, estado sugerido) | Tarea | 3 | Sonnet |
| [#33](https://github.com/cherrera0001/2026-G02-MAIN/issues/33) | Vínculo semántico área genérica–sector reproducible (método semantico) | Tarea | 3 | Sonnet |
| [#34](https://github.com/cherrera0001/2026-G02-MAIN/issues/34) | Contraste del vínculo semántico con la muestra manual e informe de la métrica según el protocolo | Tarea | 2 | Sonnet |
| [#35](https://github.com/cherrera0001/2026-G02-MAIN/issues/35) | Cargar el indicador de exposición o complementariedad con IA en core.indicador_area, o declararlo «sin evidencia» | Tarea | 2 | Sonnet |

### [#8](https://github.com/cherrera0001/2026-G02-MAIN/issues/8) P-HU04 — Ranking de focalización reproducible (propuesta)

**Peso global: 4** — Toca varias piezas (criterios, esquema, cálculo, reconstrucción, documentación) con una técnica conocida (suma ponderada normalizada), pero depende de decisiones abiertas y de criterios que hoy no tienen datos: una jornada si #11 y #14 están cerradas.

Modelo sugerido: Opus.

| Issue | Tarea | Tipo | Peso | Modelo |
|---|---|---|---|---|
| [#36](https://github.com/cherrera0001/2026-G02-MAIN/issues/36) | Proponer los criterios del ranking, su sentido y la definición de «evidencia insuficiente» | Tarea | 2 | Opus |
| [#37](https://github.com/cherrera0001/2026-G02-MAIN/issues/37) | Extender el esquema con ejecución, resultado y aporte por criterio del ranking | Tarea | 2 | Sonnet |
| [#38](https://github.com/cherrera0001/2026-G02-MAIN/issues/38) | Implementar el cálculo del ranking v0: normalización, suma ponderada y contribución por criterio; los nulos no penalizan | Tarea | 3 | Sonnet |
| [#39](https://github.com/cherrera0001/2026-G02-MAIN/issues/39) | Script de reconstrucción: recalcular el puntaje de una combinación desde datos y reglas publicadas y compararlo con el almacenado | Tarea | 2 | Sonnet |
| [#40](https://github.com/cherrera0001/2026-G02-MAIN/issues/40) | Documentar reglas de cálculo, normalización, faltantes, evidencia insuficiente y alcance del ranking | Tarea | 2 | Sonnet |

### [#9](https://github.com/cherrera0001/2026-G02-MAIN/issues/9) P-HU05 — Estabilidad del ranking ante cambios de pesos (propuesta)

**Peso global: 3** — Técnica conocida (correlación de rangos, solapamiento del top 5) sobre un ranking ya calculado; media jornada con incertidumbre moderada en la definición de la regla.

Modelo sugerido: Sonnet.

| Issue | Tarea | Tipo | Peso | Modelo |
|---|---|---|---|---|
| [#41](https://github.com/cherrera0001/2026-G02-MAIN/issues/41) | Definir la métrica de estabilidad y la regla robusta/sensible antes de calcular | Tarea | 1 | Sonnet |
| [#42](https://github.com/cherrera0001/2026-G02-MAIN/issues/42) | Escenarios de pesos en core.escenario y core.peso: base más al menos dos alternativos, suma 1 y restablecimiento | Tarea | 2 | Sonnet |
| [#43](https://github.com/cherrera0001/2026-G02-MAIN/issues/43) | Comparar escenarios: métrica de estabilidad, cambios en el top 5 y clasificación robusta/sensible, con informe reproducible | Tarea | 2 | Sonnet |

### [#10](https://github.com/cherrera0001/2026-G02-MAIN/issues/10) P-HU06 — Visualización regional y reporte con recomendaciones (propuesta)

**Peso global: 4** — Dos entregables distintos (vista por región y reporte generado desde código) en una tecnología aún no decidida; cada uno es media jornada y el conjunto supera una jornada si se suma la vista de prioridades.

Modelo sugerido: Sonnet.

| Issue | Tarea | Tipo | Peso | Modelo |
|---|---|---|---|---|
| [#44](https://github.com/cherrera0001/2026-G02-MAIN/issues/44) | Prototipo de vista de oferta por sede desde mart.sedes_geo, con cobertura declarada | Tarea | 3 | Sonnet |
| [#45](https://github.com/cherrera0001/2026-G02-MAIN/issues/45) | Vista de prioridades por región a partir del ranking | Tarea | 3 | Sonnet |
| [#46](https://github.com/cherrera0001/2026-G02-MAIN/issues/46) | Generador del reporte con recomendaciones desde código: focos, evidencia, limitaciones, fuente y fecha en cada cifra | Tarea | 3 | Sonnet |
| [#47](https://github.com/cherrera0001/2026-G02-MAIN/issues/47) | Lista de comprobación del reporte: toda cifra con fuente y fecha, sin microdatos, legible por persona no técnica | Tarea | 1 | Haiku |

## Decisiones del equipo (D1–D8)

Peso 0: registrar un acuerdo. No son requisitos.

| Issue | Decisión | Modelo para preparar opciones |
|---|---|---|
| [#11](https://github.com/cherrera0001/2026-G02-MAIN/issues/11) | D1 — Unidad del ranking | Opus |
| [#12](https://github.com/cherrera0001/2026-G02-MAIN/issues/12) | D2 — Regiones incluidas | Sonnet |
| [#13](https://github.com/cherrera0001/2026-G02-MAIN/issues/13) | D3 — Niveles de formación elegibles y tratamiento de la modalidad no presencial | Sonnet |
| [#14](https://github.com/cherrera0001/2026-G02-MAIN/issues/14) | D4 — Fuentes de demanda, productividad y exposición a IA; plan si no sirven | Opus |
| [#15](https://github.com/cherrera0001/2026-G02-MAIN/issues/15) | D5 — Usuario principal del MVP | Opus |
| [#16](https://github.com/cherrera0001/2026-G02-MAIN/issues/16) | D6 — Umbral de supresión o agrupación de celdas pequeñas | Sonnet |
| [#17](https://github.com/cherrera0001/2026-G02-MAIN/issues/17) | D7 — Tecnología de la interfaz | Opus |
| [#18](https://github.com/cherrera0001/2026-G02-MAIN/issues/18) | D8 — Mantener o retirar los comprimidos de datos versionados | Sonnet |

## Resumen

- 47 issues: 10 historias, 22 tareas, 7 investigaciones, 8 decisiones.
- Fuera del backlog por decisión de alcance pendiente: R3 (sin tareas). No se crearon tareas de API ni de interfaz: dependen de D7.
- Tareas de peso 5: ninguna. La historia P-HU03 lleva peso global 5 y está dividida en siete tareas de peso 1 a 3.
