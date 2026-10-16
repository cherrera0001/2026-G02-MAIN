# Tareas y matriz tarea ↔ issue — SDD-006

Entrada: [spec.md](spec.md), [plan.md](plan.md), [data-model.md](data-model.md). Todas pendientes: casillas indican evidencia de aceptación, no sustituyen estado operacional de Projects. La preparación está autorizada; implementar exige resolver las dependencias indicadas.

## TASK-001
- [ ] TASK-001 [US-004] Preparar dependencias y armazón Streamlit.
- Archivos: `src/app/streamlit_app.py; pyproject.toml; uv.lock`.
- Depende de: ninguna.
- Aceptación: uv sync --locked y AppTest de inicio sin excepciones.
- Issue: [[SDD-006][US-004][TASK-001] #49](https://github.com/cherrera0001/2026-G02-MAIN/issues/49). Prioridad P1; tamaño S. Horas por estimar; sin responsable ni iteración comprometidos.

## TASK-002
- [ ] TASK-002 [US-005] Implementar consultas de oferta y servicios de dominio.
- Archivos: `src/data/queries/oferta.py; src/domain/indicadores/oferta.py`.
- Depende de: TASK-001.
- Aceptación: SQL parametrizado y totales iguales a mart.oferta con cada filtro.
- Issue: [[SDD-006][US-005][TASK-002] #50](https://github.com/cherrera0001/2026-G02-MAIN/issues/50). Prioridad P1; tamaño M. Horas por estimar; sin responsable ni iteración comprometidos.

## TASK-003
- [ ] TASK-003 [US-001] Implementar mapa y oferta filtrada.
- Archivos: `src/app/pages/oferta.py; src/app/components/filtros.py`.
- Depende de: TASK-002; D6 antes de divulgar.
- Aceptación: AppTest filtros y nulos; no duplicar totales por inmueble.
- Issue: [[SDD-006][US-001][TASK-003] #44](https://github.com/cherrera0001/2026-G02-MAIN/issues/44). Prioridad P1; tamaño M. Horas por estimar; sin responsable ni iteración comprometidos.

## TASK-004
- [ ] TASK-004 [US-006] Mostrar demanda verificada o su indisponibilidad.
- Archivos: `src/app/pages/demanda.py`.
- Depende de: TASK-002; fuentes 003 para indicadores reales.
- Aceptación: Sin fuentes aceptadas no hay indicadores ni resultados ficticios.
- Issue: [[SDD-006][US-006][TASK-004] #51](https://github.com/cherrera0001/2026-G02-MAIN/issues/51). Prioridad P1; tamaño S. Horas por estimar; sin responsable ni iteración comprometidos.

## TASK-005
- [ ] TASK-005 [US-007] Integrar ranking explicable con bloqueo metodológico.
- Archivos: `src/app/pages/ranking.py; src/app/services/consulta.py`.
- Depende de: TASK-003; 003/004/005 y D1 para activar cálculo.
- Aceptación: Bloqueo visible; pesos y aportes coinciden con ejecución validada; pruebas matemáticas #39 independientes.
- Issue: [[SDD-006][US-007][TASK-005] #45](https://github.com/cherrera0001/2026-G02-MAIN/issues/45). Prioridad P1; tamaño M. Horas por estimar; sin responsable ni iteración comprometidos.

## TASK-006
- [ ] TASK-006 [US-008] Integrar procedencia y fechas por vista.
- Archivos: `src/data/queries/fuentes.py; src/app/components/procedencia.py`.
- Depende de: TASK-002.
- Aceptación: Cada cifra tiene fuente, periodo y cobertura; no se expone archivo local.
- Issue: [[SDD-006][US-008][TASK-006] #52](https://github.com/cherrera0001/2026-G02-MAIN/issues/52). Prioridad P1; tamaño S. Horas por estimar; sin responsable ni iteración comprometidos.

## TASK-007
- [ ] TASK-007 [US-009] Aplicar política de divulgación y exportación.
- Archivos: `src/domain/privacidad.py; src/app/services/exportacion.py`.
- Depende de: TASK-002; TASK-006; D6 y aprobación de datos públicos.
- Aceptación: Bloqueo por defecto; columnas permitidas, supresión primaria/secundaria y neutralización de fórmulas.
- Issue: [[SDD-006][US-009][TASK-007] #53](https://github.com/cherrera0001/2026-G02-MAIN/issues/53). Prioridad P0; tamaño M. Horas por estimar; sin responsable ni iteración comprometidos.

## TASK-008
- [ ] TASK-008 [US-002] Generar reporte reproducible desde servicios.
- Archivos: `src/reportes/generar.py`.
- Depende de: TASK-005 para recomendaciones; TASK-006; TASK-007.
- Aceptación: Comando genera documento con procedencia y agregados autorizados; no inventa ranking.
- Issue: [[SDD-006][US-002][TASK-008] #46](https://github.com/cherrera0001/2026-G02-MAIN/issues/46). Prioridad P1; tamaño M. Horas por estimar; sin responsable ni iteración comprometidos.

## TASK-009
- [ ] TASK-009 [US-002] Verificar reporte y lenguaje de alcance.
- Archivos: `tests/integration/test_reportes.py`.
- Depende de: TASK-008.
- Aceptación: Lista #47 y lectura no técnica registradas; cero exposición de microdatos.
- Issue: [[SDD-006][US-002][TASK-009] #47](https://github.com/cherrera0001/2026-G02-MAIN/issues/47). Prioridad P1; tamaño S. Horas por estimar; sin responsable ni iteración comprometidos.

## TASK-010
- [ ] TASK-010 [US-004] Validar navegación, errores y equivalencia UI DuckDB.
- Archivos: `tests/app/test_streamlit.py; tests/integration/test_consultas.py`.
- Depende de: TASK-003; TASK-004; TASK-005; TASK-006; TASK-007; TASK-009.
- Aceptación: AppTest en versión fijada: inicio, todas las páginas, filtros, faltantes, errores y exportaciones; reproducibilidad del corte y comparación SQL.
- Issue: [[SDD-006][US-004][TASK-010] #54](https://github.com/cherrera0001/2026-G02-MAIN/issues/54). Prioridad P1; tamaño M. Horas por estimar; sin responsable ni iteración comprometidos.

## Orden de ejecución
001 → 002 → 003/004/006 → 007 → 005 → 008 → 009 → 010. Los bloqueos metodológicos y de privacidad prevalecen sobre este orden. 005 puede presentar el bloqueo antes de implementar el motor, pero su aceptación completa exige 005 validada.
