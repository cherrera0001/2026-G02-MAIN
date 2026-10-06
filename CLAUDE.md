# Brújula IA Regional — contexto para Claude Code

## Producto

Proyecto del Grupo 02 del curso «Proyectos en Tecnología». Simula una consultoría al Ministerio de Economía: priorizar con evidencia dónde focalizar el cofinanciamiento de memorias y tesis aplicadas con IA. El MVP declarado en `README.md` es un ranking, una visualización por región y un reporte. La herramienta orienta una convocatoria: no evalúa postulaciones, no administra fondos y no promete impacto causal.

## Qué existe hoy

- `src/pipeline/construir_bd.py`: único código. Extrae los comprimidos, agrega y construye la base DuckDB.
- `db/schema.sql`: única definición de la estructura (esquemas `gob`, `core`, `mart`).
- `data/oferta/`, `data/geo/`: comprimidos originales versionados. `data/demanda/`: solo un README con enlaces de entorno físico.
- `data/raw/`, `data/processed/`: extraídos y base generada; fuera de Git.
- `docs/`: auditoría de historias, diseño MER/MR y arquitectura (propuestas, no acuerdos), `docs/fuentes/PLANTILLA_FICHA.md` y `docs/BACKLOG.md` (índice del backlog publicado en GitHub).
- `.github/ISSUE_TEMPLATE/`: plantillas «User Story template» (etiqueta `user story`) y «Tarea template» (etiqueta `tarea`). Su campo `type` no aplica: el repositorio no tiene tipos de issue.
- `.claude/agents/`: subagentes del proyecto.

Solo hay datos de oferta (titulados 2025) y sedes (2020). Las tablas de demanda, sectores, indicadores, vínculos, criterios y pesos están vacías. No existen ranking, servicios, API, app, notebooks, pruebas ni CI: no escribas como si existieran.

## Comandos

Desde la raíz, en PowerShell:

```powershell
uv sync                                        # instala dependencias según uv.lock
uv run python -m src.pipeline.construir_bd     # reconstruye data/processed/brujula.duckdb
uvx ruff check .                               # lint (ruff no es dependencia del proyecto)
```

El pipeline necesita `unrar`, WinRAR o 7-Zip para extraer el `.rar`. Borra y recrea la base en cada ejecución; si falla un control bloqueante, no reemplaza la base anterior. No hay pruebas automatizadas: los controles de calidad de `gob.control_calidad` son la verificación disponible (consulta en `README.md`, sección B).

## Convenciones

- Idioma: español en código, comentarios, documentación y commits. Ruff con líneas de 140.
- La estructura de la base cambia solo en `db/schema.sql`; el pipeline la aplica.
- Toda fuente se registra en `gob.fuente` y toda carga en `gob.carga` (archivo, hash, periodo, filas).
- Un dato faltante queda nulo y se declara. No se imputa ni se interpreta como evidencia en contra.
- Toda cifra distingue su naturaleza: observado, inferido o propuesto (`core.indicador.tipo_evidencia`).
- Ninguna afirmación sobre datos sin el código que la reproduce. Toda cifra mostrada lleva fuente, fecha y cobertura.
- Ramas `tipo/descripcion-corta`; commits pequeños que explican el porqué.

## Privacidad de datos

- El CSV de titulados es microdato (`mrun` enmascarado, fecha de nacimiento, género). Solo pasa por tablas temporales; lo persistente es agregado. El control `sin_datos_personales` debe seguir en 0.
- No leas, imprimas ni copies `.env` ni `chat-wsp/`. No copies su contenido a ningún archivo versionable.
- No agregues a Git `data/raw/`, `data/processed/`, `.venv/`, cachés ni archivos personales. No muestres filas individuales de titulados en salidas, reportes o documentación.
- No escribas nombres de personas ni rutas personales en archivos versionables.

## Decisiones de producto: consultar antes de resolver

Estas decisiones son del equipo. Si una tarea depende de una, detente, propone una opción con su razón y espera respuesta. No la cierres en el código ni en la documentación.

1. Unidad del ranking: región × área/carrera × institución, o carrera × sector en una región piloto.
2. Regiones incluidas.
3. Niveles de formación elegibles (`ELEGIBLE_TESIS` en el pipeline es una propuesta inicial).
4. Fuentes de demanda, productividad y exposición a IA. Ninguna está validada.
5. Usuario principal.

También siguen abiertas: tratamiento de la modalidad no presencial, umbral de supresión de celdas pequeñas, tecnología de la interfaz y si los comprimidos de datos deben seguir versionados. El detalle está en `docs/COHERENCIA_HISTORIAS.md`, sección 6. Cada decisión tiene un issue con etiqueta `decisión` (D1 a D8, enlazados en `docs/BACKLOG.md`): ahí se anota la opción elegida, la fecha y el motivo; después se actualizan README y este archivo, y solo entonces el código.

## Backlog en GitHub

- Project «Brújula IA Regional — Backlog»: https://github.com/users/cherrera0001/projects/6 (número 6, propietario `cherrera0001`, vinculado al repositorio). `Status` conserva las opciones por defecto de GitHub: `Backlog`, `Ready`, `In progress`, `In review`, `Done`. Campos propios: `Peso` (número 0–5), `Tipo` (Historia / Tarea / Decisión / Investigación), `Modelo Claude` (Opus / Sonnet / Haiku), `Sprint` (Pendiente / Sprint 1 / Sprint 2), `Horas estimadas` y `Esfuerzo real` (números). `Priority`, `Size`, `Estimate`, `Start date` y `Target date` vienen de la plantilla de GitHub y no se usan.
- Etiquetas: `user story`, `tarea`, `decisión`, `investigación`, `propuesta` (lo que el repositorio no acredita como aprobado por el equipo).
- `docs/BACKLOG.md` es el índice: historia, peso global, tareas, pesos, modelo y enlaces. Se actualiza cada vez que cambia el backlog.

### Proceso para una historia

1. **Revisar GitHub antes de escribir.** `gh issue list --state all --limit 500 --json number,title` y `gh project item-list 6 --owner cherrera0001 --limit 500`. Si existe un issue equivalente (mismo enunciado o misma necesidad), se actualiza y se vincula; no se duplica.
2. **Conservar lo documentado.** Enunciado y criterios se copian tal como están en README o `docs/`. Sin criterios: «criterios pendientes de validar». Si no consta aprobación del equipo: etiqueta `propuesta`. No se inventan acuerdos.
3. **Puntuar la historia (0–5)** con la escala del README (sección D): un solo valor para el esfuerzo agregado de cumplir todos sus criterios, con una frase que diga qué lo impulsa. No es promedio ni suma de tareas. Si una decisión del equipo la bloquea, el peso queda «pendiente» y se enlaza el issue de decisión.
4. **Dividir en tareas** pequeñas, comprobables y necesarias para los criterios. Cada tarea lleva: resultado concreto, historia relacionada, criterios que cubre, peso 0–5 con justificación, modelo sugerido con motivo, dependencias, comprobación o evidencia de término, y horas solo si hay fundamento (si no, «por estimar»). Ninguna tarea queda con peso 5: se divide.
5. **Elegir el modelo** según la guía de abajo y anotarlo en el issue y en el campo `Modelo Claude`.
6. **Crear y vincular.** Historia: `gh issue create --label "user story" --body-file <archivo>` siguiendo la estructura de la plantilla. Tarea: igual con `--label tarea --parent <número de la historia>` (sub-issue). Luego `gh project item-add 6 --owner cherrera0001 --url <url>` y fijar `Status = Backlog`, `Tipo`, `Modelo Claude`, `Peso` y `Sprint = Pendiente` con `gh project item-edit 6 --owner cherrera0001 --url <url> --field <campo> --value <opción>` (o `--number <n>`), un campo por llamada.
7. **Decisiones pendientes** se registran como issue con etiqueta `decisión`, `Tipo = Decisión`, peso 0: pregunta, opciones documentadas en el repositorio, qué bloquea y cómo se registra. Nunca se convierten en requisito ni se cierran en código: lo que depende de ellas se parametriza o se rotula propuesta.
8. **Backlog y nada más.** Historias y tareas nuevas quedan en `Backlog`, sin persona ni sprint. Solo el equipo las mueve, asigna o compromete. Al cerrar una tarea se registra `Esfuerzo real`; la comparación con la estimación sirve para estimar mejor, no para evaluar personas.

### Modelo de Claude Code

Comprobado en Claude Code 2.1.290: `claude --model` acepta los alias `fable`, `opus` y `sonnet` o el nombre completo de un modelo; `/model` dentro de la sesión muestra lo disponible. No configures un alias que la instalación no muestre ni cambies la configuración global.

- **Opus** (o el modelo de mayor capacidad que muestre `/model`): decisiones de arquitectura, historias ambiguas con impacto amplio, conflictos de alcance y revisión final de riesgos.
- **Sonnet**: análisis de historias, descomposición en tareas, estimación, documentación y la mayoría del trabajo técnico.
- **Haiku** (solo si `/model` lo ofrece; si no, Sonnet): inventarios, etiquetado mecánico, detección preliminar de duplicados y tareas pequeñas, verificando siempre el resultado.

### Análisis por issue: tipo, peso y modelo

Asignación vigente al 5 de octubre de 2026 (47 issues). El peso es el de la escala 0–5; «pendiente» = historia bloqueada por una decisión del equipo. Reparto: Opus 10, Sonnet 36, Haiku 1. Cuando una tarea de Sonnet tope con una decisión de diseño no prevista, se consulta con Opus antes de implementar; lo que Haiku produzca se verifica con Sonnet o por una persona. Si cambia el backlog, se actualiza esta tabla junto con `docs/BACKLOG.md`.

| Issue | Clave | Tipo | Peso | Modelo | Por qué ese modelo |
|---|---|---|---|---|---|
| #1 | R1 | Historia | pendiente | Opus | Historia ambigua con impacto amplio sobre el resto del backlog; conviene el modelo de mayor capacidad para redactar la reformulación y revisar riesgos |
| #2 | R2 | Historia | pendiente | Opus | Historia ambigua («entender», «problemas») que requiere reformulación con impacto en el modelo de datos y en las fuentes |
| #3 | R3 | Historia | pendiente | Opus | Conflicto de alcance (plataforma de vinculación frente a herramienta analítica) que conviene resolver con una revisión de riesgos antes de invertir trabajo |
| #4 | R4 | Historia | pendiente | Sonnet | Historia clara y sostenida por datos existentes; el análisis y la reformulación son trabajo estándar |
| #5 | P-HU01 | Historia | 3 | Sonnet | Trabajo técnico conocido sobre SQL y el pipeline existentes; no requiere decisiones de arquitectura |
| #6 | P-HU02 | Historia | 4 | Sonnet | Análisis documental y redacción de fichas con búsqueda web; trabajo estándar del agente `analista-fuentes` |
| #7 | P-HU03 | Historia | 5 | Opus | Ambigüedad metodológica e impacto amplio (define el puente carrera–sector del que depende el ranking); diseñar el método y el protocolo de validación |
| #8 | P-HU04 | Historia | 4 | Opus | Definir criterios, normalización y «evidencia insuficiente» es una decisión de diseño con impacto amplio; la implementación se delega a Sonnet por tarea |
| #9 | P-HU05 | Historia | 3 | Sonnet | Análisis cuantitativo estándar y código acotado una vez que existe el ranking |
| #10 | P-HU06 | Historia | 4 | Sonnet | Vistas y generador de reporte con bibliotecas conocidas; la tecnología (#17) la decide el equipo |
| #11 | D1 | Decisión | 0 | Opus | Decisión de arquitectura del producto con impacto en casi todo el backlog; preparar opciones y consecuencias |
| #12 | D2 | Decisión | 0 | Sonnet | Decisión acotada; basta un resumen de cobertura por región desde la base |
| #13 | D3 | Decisión | 0 | Sonnet | Decisión de alcance con cifras ya disponibles; preparar la tabla de títulos por nivel y modalidad es trabajo estándar |
| #14 | D4 | Decisión | 0 | Opus | Mayor riesgo del proyecto y consecuencias sobre el método; revisar las fichas y el plan alternativo |
| #15 | D5 | Decisión | 0 | Opus | Conflicto de alcance que redefine la mitad de las historias del README; análisis de impacto |
| #16 | D6 | Decisión | 0 | Sonnet | Decisión acotada apoyada en una consulta de distribución de celdas |
| #17 | D7 | Decisión | 0 | Opus | Decisión de arquitectura; comparar opciones con sus consecuencias de despliegue, privacidad y mantenimiento |
| #18 | D8 | Decisión | 0 | Sonnet | Decisión acotada; comparación de opciones estándar |
| #19 | T-P-HU01-1 | Tarea | 2 | Sonnet | Edición de pipeline y SQL con solución conocida |
| #20 | T-P-HU01-2 | Tarea | 2 | Sonnet | Código Python y SQL acotado |
| #21 | T-P-HU01-3 | Tarea | 2 | Sonnet | Código acotado con regla clara |
| #22 | T-P-HU01-4 | Tarea | 1 | Sonnet | Redacción breve con una consulta SQL; Haiku bastaría para redactar, la verificación se revisa con Sonnet |
| #23 | T-P-HU02-1 | Investigación | 2 | Sonnet | Análisis documental con búsqueda web (`analista-fuentes`) |
| #24 | T-P-HU02-2 | Investigación | 2 | Sonnet | Análisis documental con búsqueda web (`analista-fuentes`) |
| #25 | T-P-HU02-3 | Investigación | 2 | Sonnet | Análisis documental con búsqueda web (`analista-fuentes`) |
| #26 | T-P-HU02-4 | Investigación | 2 | Sonnet | Análisis documental con búsqueda web (`analista-fuentes`) |
| #27 | T-P-HU02-5 | Investigación | 2 | Sonnet | Análisis documental con búsqueda web (`analista-fuentes`) |
| #28 | T-P-HU02-6 | Investigación | 2 | Sonnet | Síntesis con criterio; Haiku puede preparar el borrador de la tabla y Sonnet revisarlo |
| #29 | T-P-HU03-1 | Investigación | 2 | Sonnet | Lectura técnica de metodologías y redacción de fichas con búsqueda web |
| #30 | T-P-HU03-2 | Tarea | 2 | Sonnet | Cambio de pipeline con patrón existente (`FUENTES`, `gob.carga`) |
| #31 | T-P-HU03-3 | Tarea | 1 | Sonnet | Redacción metodológica estándar |
| #32 | T-P-HU03-4 | Tarea | 3 | Sonnet | Clasificación razonada con justificaciones; el modelo propone, el equipo revisa |
| #33 | T-P-HU03-5 | Tarea | 3 | Sonnet | Método de similitud conocido; si la elección de técnica resulta ambigua, consultar con Opus antes de implementar |
| #34 | T-P-HU03-6 | Tarea | 2 | Sonnet | Análisis cuantitativo estándar |
| #35 | T-P-HU03-7 | Tarea | 2 | Sonnet | Cambio de pipeline y documentación con patrón conocido |
| #36 | T-P-HU04-1 | Tarea | 2 | Opus | Define la lógica del producto con impacto amplio y ambigüedad (qué cuenta como evidencia) |
| #37 | T-P-HU04-2 | Tarea | 2 | Sonnet | Edición de SQL y pipeline con patrón conocido (`ingeniero-datos`) |
| #38 | T-P-HU04-3 | Tarea | 3 | Sonnet | Implementación del método definido en #36; sin decisiones nuevas de diseño |
| #39 | T-P-HU04-4 | Tarea | 2 | Sonnet | Código acotado de verificación |
| #40 | T-P-HU04-5 | Tarea | 2 | Sonnet | Documentación técnica estándar |
| #41 | T-P-HU05-1 | Tarea | 1 | Sonnet | Redacción metodológica estándar |
| #42 | T-P-HU05-2 | Tarea | 2 | Sonnet | Código acotado |
| #43 | T-P-HU05-3 | Tarea | 2 | Sonnet | Análisis cuantitativo acotado |
| #44 | T-P-HU06-1 | Tarea | 3 | Sonnet | Vista con bibliotecas conocidas una vez elegida la tecnología |
| #45 | T-P-HU06-2 | Tarea | 3 | Sonnet | Interfaz con el patrón definido en #44 |
| #46 | T-P-HU06-3 | Tarea | 3 | Sonnet | Generación de documento a partir de datos con bibliotecas conocidas |
| #47 | T-P-HU06-4 | Tarea | 1 | Haiku | Verificación mecánica de un documento (fuente/fecha, enlaces, términos prohibidos), revisada después por una persona |

### Definición de terminado de un issue

- Criterios de aceptación comprobables sin interpretación (entrada y salida esperada).
- Vínculos correctos: tarea con su historia padre, historia con sus decisiones, todos en el Project.
- Peso explicado en una frase; horas estimadas solo con fundamento; modelo sugerido con motivo.
- Evidencia de término en el issue: comando y salida, enlace al archivo o captura sin datos personales.
- Estado del Project coherente con el trabajo real; `Esfuerzo real` registrado al cerrar.

Este archivo orienta el trabajo: no reemplaza las historias aprobadas por el equipo ni autoriza a cerrar las decisiones reservadas a él.

## Definición de terminado

- El pipeline corre completo desde la raíz y pasan los controles bloqueantes.
- `uvx ruff check .` no suma avisos nuevos.
- El cambio queda documentado donde corresponde (README, ficha de fuente o comentario del esquema).
- `git status` no muestra datos, secretos ni archivos ignorados entre lo que se va a versionar.
- Lo que es propuesta o está pendiente queda rotulado como tal.
- Los cambios quedan locales para revisión: no hagas commit, push, merge ni comandos destructivos (`git reset --hard`, `git clean`, `git checkout --`) sin pedido explícito. Issues y Project se crean o editan solo con pedido explícito y siguiendo «Backlog en GitHub»; ramas remotas, milestones y asignaciones, nunca sin pedido.
