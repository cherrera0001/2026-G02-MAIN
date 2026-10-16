# Informe de validación y decisiones pendientes — 2026-10-16

## Alcance ejecutado
Preparación SDD y configuración del Project existente. No se ejecutó `/speckit-implement`, no se desplegó una aplicación y no se cambió el pipeline, el esquema ni las dependencias. Se preservaron los archivos SDD no versionados que ya estaban en el directorio al comenzar.

## Evidencia local
- Python del entorno existente: DuckDB 1.5.6; Streamlit no instalado. Las pruebas de inicio, navegación, filtros de UI, errores visuales y descarga quedan pendientes de TASK-001 a TASK-010; no se declaran aprobadas.
- Consulta en lectura de `gob.control_calidad`: ocho controles, todos cumplen: cargas_huerfanas, comunas_sin_cut, inmuebles_cargados, niveles_pendientes, regiones, sin_datos_personales, titulos_con_punto, titulos_conservados. Es evidencia de la base existente, no una reconstrucción nueva del pipeline.
- `SUM(n_titulos)` en `mart.oferta` y `core.titulacion`: 328998 en ambos. Cinco selecciones parametrizadas repetidas mantienen el mismo resultado en el mismo corte. Esto no demuestra reproducibilidad de reconstrucción en otra máquina.
- `core.indicador_region_sector`: cero filas. No hay base para poblar demanda ni activar ranking con resultados ficticios.
- Diseño revisado contra `db/schema.sql`: el mapa repite totales por institución/comuna, no contiene área genérica y sus uniones sin correspondencia devuelven NULL. El contrato evita doble conteo y atribución incorrecta.
- Documentación oficial de AppTest consultada: https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest . Su compatibilidad instalada y las interacciones disponibles se comprobarán tras fijar la dependencia.

## GitHub
Se confirmó identidad `cherrera0001`, permiso ADMIN del repositorio y Project 6 `PVT_kwHOASvtSs4Bl2ei`, ya vinculado. La identidad activa persistente se mantuvo sin cambios: la credencial del propietario solo se aplicó en memoria a los procesos de consulta/sincronización. No se leyó `.env`.

Se inspeccionaron los proyectos del propietario y los 47 issues iniciales abiertos/cerrados; se reutilizan #44–#47 para tareas equivalentes y #10 como historia existente. Las tareas nuevas solo cubren descomposición no equivalente. La matriz canónica está en [tasks.md](tasks.md). No se cierra ningún issue ni se acredita implementación finalizada.

Status incorpora Backlog, Ready, In Progress, In Review, Blocked, Done conservando IDs. Priority incluye P0–P3; Size conserva XS/S/M/L y XL histórico para evitar pérdida de datos. Feature SDD es texto. Assignees y Milestone ya existen como campos nativos y no se asignan sin compromiso.

La creación de Iteración se intentó con calendario vacío; GraphQL exige `startDate` y rechazó la operación. No se inventa una fecha de sprint. Sprint histórico se conserva; falta aprobar calendario y crear el campo de iteración con sus fechas. Las tareas permanecen sin responsable ni milestone nuevos.

Los enlaces `blob/main` de los issues anticipan rutas de artefactos locales; no estarán disponibles en GitHub hasta que el equipo versione e integre los cambios. Cada issue advierte esta limitación. No se hizo commit ni push.

## Decisiones pendientes y puertas
- #11 D1: unidad del ranking; bloquea grano y motor.
- #12 D2: regiones incluidas; no se asume una región piloto.
- #13 D3: elegibilidad; explorar oferta no equivale a elegibilidad aprobada.
- #14 D4 y features 003/004: fuentes de demanda/productividad/IA, licencias y aprobación verificable.
- #15 D5: usuario principal y alcance del producto.
- #16 D6: umbral y política de divulgación, supresión secundaria y control de reconstrucción por filtros; bloquea exportación y publicación.
- #18 D8: política de versionado de comprimidos.
- Metodología 005: normalización, faltantes, ponderaciones, desempates y sensibilidad requieren aceptación científica; pruebas independientes de la UI.
- Calendario de iteraciones, responsables y milestones: sin compromiso aprobado.
- D7/#17 deja de ser decisión tecnológica pendiente: Streamlit aprobado por el responsable en ADR-002. Se registra sin cerrar automáticamente el issue.

La consistencia del diseño permite preparar desarrollo incremental, no habilitar todas las funcionalidades ni publicar datos. Las tareas de ranking y divulgación conservan sus bloqueos explícitos.

## Verificación final
Diez tareas con ID único, issue abierto y exactamente un ítem correspondiente en Project 6, comprobados por API. Reutilizadas #44–#47; nuevas #49–#54. Se verificó enlace inverso a tasks.md en los diez issues. Matriz local sin duplicados y enlaces locales de plan/contratos/ADR válidos. `git diff --check` sin errores. La comprobación de enlaces de GitHub queda condicionada a la integración de los archivos locales.
