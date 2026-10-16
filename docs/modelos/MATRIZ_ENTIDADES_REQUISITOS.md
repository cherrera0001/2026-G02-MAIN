# Matriz de Correspondencia entre Entidades y Requisitos — Brújula IA Regional

Esta matriz establece la trazabilidad bidireccional entre los requisitos funcionales del producto, las historias de usuario reconstruidas (SDD) y las entidades del modelo de datos de DuckDB.

| Entidad / Vista DuckDB | Esquema | Grano / Clave Primaria | Requisitos Cubiertos | Historias SDD Asociadas | Estado Físico en BD |
|---|---|---|---|---|---|
| `fuente` | `gob` | `id_fuente` | FR-001-1, FR-001-2 | 001-US1, 001-US3 | Implementada (4 filas) |
| `carga` | `gob` | `id_carga` | FR-001-2, FR-001-4 | 001-US1, 001-US2 | Implementada (2 filas) |
| `control_calidad` | `gob` | `regla` | FR-001-3, FR-001-5 | 001-US2 | Implementada (8 reglas) |
| `region` | `core` | `cod_region` | FR-002-1, FR-002-3 | 002-US1, 006-US1 | Implementada (16 regiones) |
| `comuna` | `core` | `id_comuna` | FR-002-1, FR-006-2 | 002-US1, 006-US1 | Implementada (120 comunas) |
| `institucion` | `core` | `cod_inst` | FR-002-1, FR-002-3 | 002-US1, 006-US1 | Implementada (144 IES) |
| `sede` | `core` | `(cod_inst, cod_sede)` | FR-002-1, FR-006-2 | 002-US1, 006-US1 | Implementada (481 sedes) |
| `inmueble` | `core` | `id_inmueble` | FR-006-2 | 006-US1 | Implementada (1.297 puntos) |
| `nivel_carrera` | `core` | `id_nivel` | FR-002-2 | 002-US2 | Implementada (9 niveles) |
| `area_generica` | `core` | `id_area_generica` | FR-002-1, FR-004-1 | 002-US1, 004-US1 | Implementada (285 áreas) |
| `programa` | `core` | `cod_programa` | FR-002-1, FR-002-2 | 002-US1, 002-US2 | Implementada (15.469 programas) |
| `titulacion` | `core` | `(periodo, cod_programa, genero)` | FR-001-4, FR-002-1 | 001-US2, 002-US1 | Implementada (26.359 filas, 328.998 títulos) |
| `sector` | `core` | `id_sector` | FR-003-1 | 003-US1 | Vacía (0 filas) — Bloqueada |
| `indicador` | `core` | `id_indicador` | FR-003-2, FR-004-3 | 003-US2, 004-US3 | Vacía (0 filas) — Bloqueada |
| `indicador_region_sector` | `core` | `(id_indicador, cod_region, id_sector, periodo)` | FR-003-3 | 003-US2 | Vacía (0 filas) — Bloqueada |
| `indicador_area` | `core` | `(id_indicador, id_area_generica)` | FR-004-3 | 004-US3 | Vacía (0 filas) — Bloqueada |
| `vinculo_area_sector` | `core` | `(id_area_generica, id_sector)` | FR-004-1, FR-004-2 | 004-US1, 004-US2 | Vacía (0 filas) — Bloqueada |
| `criterio` | `core` | `id_criterio` | FR-005-3 | 005-US2 | Vacía (0 filas) — Bloqueada |
| `escenario` | `core` | `id_escenario` | FR-005-3 | 005-US3 | Vacía (0 filas) — Bloqueada |
| `peso` | `core` | `(id_escenario, id_criterio)` | FR-005-3 | 005-US2, 005-US3 | Vacía (0 filas) — Bloqueada |
| `mart.oferta` | `mart` | Vista analítica consolidada | FR-002-3 | 002-US1, 002-US2 | Implementada (15.011 filas) |
| `mart.especializacion` | `mart` | Vista de cociente territorial | FR-002-4, FR-002-5 | 002-US3 | Implementada (2.036 filas) |
| `mart.sedes_geo` | `mart` | Vista geográfica de oferta | FR-006-2 | 006-US1 | Implementada (1.297 filas) |
| `ejecucion_ranking` | `core` | `id_ejecucion` | FR-005-2 | 005-US2 | Propuesta (por crear) |
| `resultado_ranking` | `core` | `id_resultado` | FR-005-2 | 005-US2, 005-US3 | Propuesta (por crear) |
| `aporte_criterio` | `core` | `(id_resultado, id_criterio)` | FR-005-2 | 005-US2 | Propuesta (por crear) |
