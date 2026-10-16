# ADR-001 — GitHub Projects como sistema de seguimiento
Estado: Aceptada por el responsable | Fecha: 2026-10-16

## Contexto y decisión
Se necesita trazabilidad operacional del trabajo SDD sin crear otra autoridad de requisitos. Se adopta GitHub Projects y se reutiliza el Project 6 del propietario cherrera0001, vinculado a 2026-G02-MAIN: https://github.com/users/cherrera0001/projects/6 . La API confirmó su identidad `PVT_kwHOASvtSs4Bl2ei` y el acceso ADMIN del propietario.

## Consecuencias
`spec.md` define requisitos, `tasks.md` descompone y Issues/Projects siguen estado, prioridad, tamaño, responsable e iteración. Cada tarea conserva ID estable y URL del issue; el issue referencia la ruta y el ID. Se buscan equivalentes entre issues abiertos y cerrados antes de crear; no se cierran automáticamente. Los campos históricos se preservan. Las tareas nuevas entran en Backlog, sin asignar personas, fechas o compromisos no aprobados.

Convención: `[SDD-006][US-001][TASK-001] Descripción`; SDD identifica la feature (no se fuerza 001 para features diferentes). La matriz canónica está en `specs/006-visualizacion-reportes/tasks.md`. Los títulos históricos sin tarea equivalente mantienen su identidad.
