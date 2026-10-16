# Tareas y matriz tarea ↔ issue — SDD-006

Entrada: [spec.md](spec.md), [plan.md](plan.md), [data-model.md](data-model.md). Todas pendientes: casillas indican evidencia de aceptación, no sustituyen estado operacional de Projects. La preparación está autorizada; implementar exige resolver las dependencias indicadas.

## TASK-001
- [x] TASK-001 [US-004] Preparar dependencias y armazón Streamlit.
- Archivos: `src/app/streamlit_app.py; pyproject.toml; uv.lock`.
- Depende de: ninguna.
- Aceptación: uv sync --locked y AppTest de inicio sin excepciones. Verificado en CI/CD y despliegue Streamlit Cloud.
- Issue: [[SDD-006][US-004][TASK-001] #49](https://github.com/cherrera0001/2026-G02-MAIN/issues/49). Prioridad P1; tamaño S.

## TASK-002
- [x] TASK-002 [US-005] Implementar consultas de oferta y servicios de dominio.
- Archivos: `src/servicios/consultas_oferta.py; src/servicios/__init__.py`.
- Depende de: TASK-001.
- Aceptación: SQL parametrizado, distribución regional, tipos de IES, niveles formativos, top áreas y descomposición matemática completa de LQ ($T_{ra}, T_r, T_a, T_{total}$, umbral $\tau$). 16 pruebas unitarias aprobadas.
- Issue: [[SDD-006][US-005][TASK-002] #50](https://github.com/cherrera0001/2026-G02-MAIN/issues/50). Prioridad P1; tamaño M.

## TASK-003
- [x] TASK-003 [US-001] Implementar mapa y oferta filtrada.
- Archivos: `src/app/streamlit_app.py`.
- Depende de: TASK-002; D6 antes de divulgar.
- Aceptación: AppTest con filtros y mapa de sedes georreferenciadas; sin duplicación de totales por inmueble y filtros jerárquicos reactivos en sidebar.
- Issue: [[SDD-006][US-001][TASK-003] #44](https://github.com/cherrera0001/2026-G02-MAIN/issues/44). Prioridad P1; tamaño M.

## TASK-004
- [x] TASK-004 [US-006] Mostrar demanda verificada o su indisponibilidad.
- Archivos: `src/app/streamlit_app.py; src/servicios/consultas_oferta.py`.
- Depende de: TASK-002; fuentes 003 para indicadores reales.
- Aceptación: Pestaña "Priorización (Bloqueada)" declara formalmente la indisponibilidad de fuentes de demanda externa y prohíbe inventar scores.
- Issue: [[SDD-006][US-006][TASK-004] #51](https://github.com/cherrera0001/2026-G02-MAIN/issues/51). Prioridad P1; tamaño S.

## TASK-005
- [x] TASK-005 [US-007] Integrar ranking explicable con bloqueo metodológico.
- Archivos: `src/app/streamlit_app.py; src/servicios/consultas_oferta.py`.
- Depende de: TASK-003; 003/004/005 y D1 para activar cálculo.
- Aceptación: Bloqueo metodológico estricto en UI; desglose de riesgos analíticos de rankings espurios y roadmap de desbloqueo.
- Issue: [[SDD-006][US-007][TASK-005] #45](https://github.com/cherrera0001/2026-G02-MAIN/issues/45). Prioridad P1; tamaño M.

## TASK-006
- [x] TASK-006 [US-008] Integrar procedencia y fechas por vista.
- Archivos: `src/app/streamlit_app.py; src/servicios/consultas_oferta.py`.
- Depende de: TASK-002.
- Aceptación: Pestaña "Trazabilidad y Calidad" expone hashes SHA-256 de insumos oficiales, fechas de corte censal 2025 y catastro 2020, sin exponer rutas locales.
- Issue: [[SDD-006][US-008][TASK-006] #52](https://github.com/cherrera0001/2026-G02-MAIN/issues/52). Prioridad P1; tamaño S.

## TASK-007
- [x] TASK-007 [US-009] Aplicar política de divulgación y exportación.
- Archivos: `src/app/streamlit_app.py`.
- Depende de: TASK-002; TASK-006; D6 y aprobación de datos públicos.
- Aceptación: Exportación en formato CSV en UTF-8 con neutralización de inyección de fórmulas en Explorador Territorial y Especialización LQ. Cero microdatos personales exportables.
- Issue: [[SDD-006][US-009][TASK-007] #53](https://github.com/cherrera0001/2026-G02-MAIN/issues/53). Prioridad P0; tamaño M.

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
- [x] TASK-010 [US-004] Validar navegación, errores y equivalencia UI DuckDB.
- Archivos: `tests/test_streamlit_app.py; tests/test_servicios_oferta.py`.
- Depende de: TASK-003; TASK-004; TASK-005; TASK-006; TASK-007; TASK-009.
- Aceptación: 21 pruebas automatizadas pasando (16 unitarias de dominio + 5 AppTest de UI); verificación de renderizado de 6 pestañas, filtros jerárquicos y manejo de BD inexistente.
- Issue: [[SDD-006][US-004][TASK-010] #54](https://github.com/cherrera0001/2026-G02-MAIN/issues/54). Prioridad P1; tamaño M.

## Orden de ejecución
001 → 002 → 003/004/006 → 007 → 005 → 008 → 009 → 010. Los bloqueos metodológicos y de privacidad prevalecen sobre este orden. 005 puede presentar el bloqueo antes de implementar el motor, pero su aceptación completa exige 005 validada.
