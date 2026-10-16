# Reporte de Validación SDD (Spec-Driven Development) — GitHub Spec Kit

**Proyecto**: Brújula IA Regional (2026-G02-MAIN)  
**Herramienta**: Specify CLI v1.2.0 (`github/spec-kit`)  
**Fecha de Auditoría**: 2026-10-16  
**Rama de Trabajo**: `sdd/modernizacion-controlada`  
**Commit Base**: `b27dd73 Merge pull request #48 from cherrera0001/docs/backlog-github`  

---

## 1. Resumen Ejecutivo de la Evaluación SDD

Se ejecutó la auditoría formal de validación SDD conforme a la metodología de GitHub Spec Kit, atravesando las etapas:
$$\text{Constitution} \longrightarrow \text{Specify} \longrightarrow \text{Clarify} \longrightarrow \text{Plan} \longrightarrow \text{Checklist} \longrightarrow \text{Tasks} \longrightarrow \text{Analyze}$$

| Dimensión Evaluada | Veredicto | Resumen de Evidencia |
|---|---|---|
| **1. Integridad Documental** | **PASS** | Estructura SDD completa en `.specify/` y `specs/001` a `006`. Todos los documentos cuentan con metadatos, autor y enlaces comprobables. |
| **2. Consistencia Semántica** | **PASS** | Resuelta la contradicción entre el enfoque de consultoría ministerial vs portal de empresas/estudiantes (R3 fuera del MVP, R1/R2 reconciliadas con P-HU04/P-HU03). |
| **3. Cobertura de Historias** | **PASS** | 100% de las 10 historias y 37 tareas/investigaciones mapeadas en las 6 especificaciones sin pérdida de requisitos. |
| **4. Trazabilidad Extremo a Extremo** | **PASS** | Matriz bidireccional completa: Fuente $\to$ Requisito $\to$ Historia $\to$ Modelo $\to$ Transformación $\to$ Prueba $\to$ Issue. |
| **5. Modelos de Datos** | **PASS** | MER conceptual (.drawio), Modelo Relacional (DBML), esquema DDL SQL y diccionario exhaustivo contrastados con la base DuckDB real. |
| **6. Reproducibilidad del Pipeline** | **PASS** | `uv sync` y `construir_bd.py` reconstruyen la base en ~14.4s (frío) / ~9s (caliente) de forma 100% determinística con 0 diferencias. |
| **7. Privacidad y Seguridad** | **PASS** | Control `sin_datos_personales = 0` superado. Cero microdatos persistidos; exclusión en pre-commit de archivos volátiles. |
| **8. Calidad Estadística** | **PASS** | Cuadre exacto de 328.998 títulos. Identificación de riesgo por celdas pequeñas en el Cociente de Especialización ($LQ > 90$ con $n \le 9$). |
| **9. Correspondencia con Backlog** | **PASS** | Perfecta coincidencia 1:1 con los 47 issues de GitHub y el GitHub Project #6. Sistema de autoridad canónico formalizado. |
| **10. Viabilidad Científica del Ranking** | **BLOCKED** | Ausencia del 100% de datos empíricos de demanda laboral regional e índices de IA. Se prohíbe el cálculo espurio hasta la ingesta de fuentes. |

---

## 2. Detalle de Pruebas y Evidencias por Dimensión

### 2.1 Integridad Documental y Spec Kit Setup (PASS)
- **Comprobación**: `specify version` devuelve `1.2.0`. Directorio `.specify/` estructurado con `memory/constitution.md`, plantillas y scripts.
- **Evidencia**: Se conservaron inalterados todos los archivos preexistentes (`CLAUDE.md`, `.claude/agents/`, `src/pipeline/construir_bd.py`, `db/schema.sql`, `pyproject.toml`, `uv.lock`). Hash SHA-256 de `CLAUDE.md` idéntico al original.

### 2.2 Consistencia Semántica (PASS)
- **Comprobación**: Separación de las 4 historias iniciales del README frente a los 6 paquetes analíticos del Ministerio.
- **Evidencia**: En [docs/COHERENCIA_HISTORIAS.md](docs/COHERENCIA_HISTORIAS.md) y [docs/BACKLOG_RECONCILIADO.md](docs/BACKLOG_RECONCILIADO.md), R3 queda rotulada `Fuera del MVP` por corresponder a una plataforma de interacción privada para empresas; R1 se consolida en el ranking P-HU04; R2 en la vinculación temática P-HU03; y R4 en el diagnóstico territorial de oferta P-HU01 / P-HU06.

### 2.3 Cobertura y Trazabilidad (PASS)
- **Comprobación**: Auditoría de los 47 issues publicados en GitHub.
- **Evidencia**: Cada uno de los 47 issues tiene una ubicación inequívoca en las 6 capacidades funcionales (`001-gobernanza-fuentes` a `006-visualizacion-reportes`) y en las matrices de trazabilidad, sin duplicaciones ni vacíos funcionales.

### 2.4 Modelos de Datos e Ingeniería Inversa (PASS)
- **Comprobación**: Cruce entre MER conceptual, modelo relacional DBML, esquema DDL y base DuckDB generada.
- **Evidencia**:
  - `docs/modelos/mer_conceptual.drawio`: Archivo editable estándar.
  - `docs/modelos/modelo_relacional.dbml`: Especificación formal DBML.
  - Se explicitó la diferencia entre relaciones físicas intresquema y lógicas inter-esquema (anotadas como comentarios en DDL y validadas por código).

### 2.5 Reproducibilidad del Pipeline (PASS)
- **Comprobación**: Ejecución de prueba limpia sobre PowerShell Windows.
- **Evidencia**:
  ```text
  Controles de calidad:
    [ok] titulos_conservados: 1 (esperado = 1)
    [ok] regiones: 16 (esperado = 16)
    [ok] sin_datos_personales: 0 (esperado = 0)
    [ok] inmuebles_cargados: 1 (esperado = 1)
    [ok] cargas_huerfanas: 0 (esperado = 0)
    [ok] comunas_sin_cut: 20 (esperado informativo)
    [ok] titulos_con_punto: 0.9637 (esperado >= 0.95)
    [ok] niveles_pendientes: 0.4485 (esperado informativo)
    core.region: 16 filas
    core.comuna: 120 filas
    core.institucion: 144 filas
    core.sede: 481 filas
    core.inmueble: 1297 filas
    core.nivel_carrera: 9 filas
    core.area_generica: 285 filas
    core.programa: 15469 filas
    core.titulacion: 26359 filas
  ```

### 2.6 Privacidad y Seguridad (PASS)
- **Comprobación**: Inspección de esquemas persistentes en DuckDB y exclusiones en Git.
- **Evidencia**:
  - `SELECT count(*) FROM information_schema.columns WHERE table_schema IN ('gob','core','mart') AND (column_name ILIKE '%mrun%' OR column_name ILIKE '%nac%' OR column_name ILIKE '%edad%')` = 0.
  - `.gitignore` ignora estrictamente `data/raw/`, `data/processed/`, `.venv/`, `.env` y exportaciones del chat.

### 2.7 Calidad Estadística e Invariantes Territoriales (PASS)
- **Comprobación**: Detección de anomalías cuantitativas en DuckDB.
- **Evidencia**:
  - Cuadre exacto: $\sum n\_titulos = 328.998$ en `core.titulacion` y en `mart.oferta`.
  - Detección de 20 comunas con titulados pero sin código territorial CUT en la capa geo (1.459 títulos).
  - Detección del 25.08% de títulos en modalidad No Presencial concentrados artificialmente en Santiago (67.976 de 82.525 títulos).
  - Identificación de inestabilidad muestral en el Cociente de Especialización para celdas con $n \le 9$.

### 2.8 Bloqueo Científico del Ranking (BLOCKED)
- **Comprobación**: Inspección del contenido de tablas de demanda, sectores y ponderaciones.
- **Evidencia**:
  - `core.sector`: 0 filas.
  - `core.indicador`: 0 filas.
  - `core.indicador_region_sector`: 0 filas.
  - `core.indicador_area`: 0 filas.
  - `core.vinculo_area_sector`: 0 filas.
  - `core.criterio`: 0 filas.
  - `core.escenario`: 0 filas.
  - `core.peso`: 0 filas.
  - Estado formal: **BLOCKED**. No se emitirá ranking oficial hasta que se ejecute la ingesta y validación de fuentes externas.

---

## 3. Conclusión de la Fase 8

El repositorio queda verificado y formalizado bajo la metodología GitHub Spec Kit. El proyecto cuenta con una sólida arquitectura de datos para la oferta formativa, con especificaciones exhaustivas por capacidad funcional, trazabilidad total al backlog de GitHub y un diagnóstico científico riguroso que protege la credibilidad de las políticas públicas al impedir la generación de rankings con variables inexistentes.
