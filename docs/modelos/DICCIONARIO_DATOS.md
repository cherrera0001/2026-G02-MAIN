# Diccionario de Datos, Cardinalidades e Ingeniería Inversa — Brújula IA Regional

**Base de Datos**: DuckDB (`data/processed/brujula.duckdb`)  
**Esquema Fuente DDL**: `db/schema.sql`  
**Pipeline de Construcción**: `src/pipeline/construir_bd.py`  
**Fecha de Auditoría**: 2026-10-16  

---

## 1. Cadena de Transformación y Trazabilidad

$$\text{MER Conceptual} \longrightarrow \text{Modelo Relacional} \longrightarrow \text{SQL Físico (DDL)} \longrightarrow \text{Pipeline ETL Python} \longrightarrow \text{Datos Resultantes (DuckDB)}$$

### Análisis de Brechas entre Niveles
1. **Conceptual vs Físico**:
   - Relaciones inter-esquema: En el MER conceptual, `core.titulacion` y `core.indicador_*` tienen relaciones de dependencia con `gob.carga`, y `core.indicador` con `gob.fuente`. Físicamente, DuckDB no soporta llaves foráneas entre esquemas distintos (`gob` y `core`). Estas referencias son **lógicas** en el DDL y se verifican mediante controles de calidad (`cargas_huerfanas = 0`).
   - Persistencia del Ranking: En el MER conceptual existen entidades de ejecución y resultado del ranking. En el SQL físico actual (`db/schema.sql`) **no existen físicamente**; solo existen catálogos de `core.criterio`, `core.escenario` y `core.peso`. Se definen como tablas propuestas (`core.ejecucion_ranking`, `core.resultado_ranking`, `core.aporte_criterio`).
2. **Físico vs Pipeline**:
   - `core.comuna`: Se puebla mediante un `FULL OUTER JOIN` entre las comunas de titulados (Mineduc) y las comunas de la capa geo (Geoportal), resolviendo diferencias léxicas con `upper(strip_accents(trim(comuna)))`.
   - `core.programa`: El pipeline carga el programa deduplicando con `QUALIFY row_number() OVER (PARTITION BY cod_sies_obt_tit ORDER BY cat_periodo DESC) = 1`.
   - `core.institucion`: En caso de inconsistencia en nombres o clasificaciones, el pipeline toma el valor más frecuente (`mode(nomb_inst)`).
3. **Pipeline vs Datos Reales**:
   - Se procesaron 328.998 filas brutas de titulados y 1.297 filas de inmuebles.
   - En la base generada, 100% de los títulos fueron conservados exactamente (`sum(n_titulos) = 328.998`).
   - Las tablas de demanda (`core.sector`, `core.indicador`, `core.indicador_region_sector`, `core.indicador_area`, `core.vinculo_area_sector`) y ranking (`core.criterio`, `core.escenario`, `core.peso`) tienen actualmente **0 filas**.

---

## 2. Diccionario de Datos por Esquema y Tabla

### 2.1 Esquema `gob` (Gobierno de Datos)

#### Tabla: `gob.fuente`
Catálogo de fuentes primarias utilizadas en el sistema.
- **Grano**: 1 fila por fuente de datos registrada.
- **Filas actuales**: 4 fuentes registradas (`mineduc_titulados`, `geoportal_ies`, `ckan_instalaciones`, `mop_infraestructura`).

| Columna | Tipo | Nulos | PK/FK | Descripción |
|---|---|---|---|---|
| `id_fuente` | VARCHAR | NO | PK | Identificador único de la fuente (ej. `mineduc_titulados`) |
| `nombre` | VARCHAR | NO | - | Nombre descriptivo oficial de la fuente |
| `organismo` | VARCHAR | NO | - | Institución pública o privada proveedora |
| `url` | VARCHAR | NO | - | Enlace de descarga o documentación |
| `licencia` | VARCHAR | SÍ | - | Licencia legal (ej. CC-BY, Open Data) |
| `unidad_territorial` | VARCHAR | SÍ | - | Cobertura espacial (nacional, punto, región) |
| `contiene_datos_personales` | BOOLEAN | NO | - | Flag de privacidad (True si el origen trae microdatos) |
| `notas` | VARCHAR | SÍ | - | Restricciones de uso o advertencias técnicas |

#### Tabla: `gob.carga`
Lotes de ingesta procesados con verificación criptográfica SHA-256.
- **Grano**: 1 fila por archivo procesado en un periodo.
- **Filas actuales**: 2 filas (1 CSV Mineduc + 1 DBF Geoportal).

| Columna | Tipo | Nulos | PK/FK | Descripción |
|---|---|---|---|---|
| `id_carga` | INTEGER | NO | PK | Secuencial único del lote |
| `id_fuente` | VARCHAR | NO | FK -> `gob.fuente` | Fuente a la que pertenece el archivo |
| `archivo` | VARCHAR | NO | - | Nombre del archivo físico procesado |
| `sha256` | VARCHAR | NO | - | Hash criptográfico SHA-256 del archivo inmutable |
| `periodo` | INTEGER | SÍ | - | Año o corte temporal de los datos |
| `filas_leidas` | BIGINT | NO | - | Cantidad de registros leídos en bruto |
| `fecha_carga` | TIMESTAMP | NO | - | Marca de tiempo exacta del procesamiento |

#### Tabla: `gob.control_calidad`
Resultados de la auditoría de calidad e invariantes del pipeline.
- **Grano**: 1 fila por regla evaluada en cada construcción.
- **Filas actuales**: 8 reglas registradas.

| Columna | Tipo | Nulos | PK/FK | Descripción |
|---|---|---|---|---|
| `regla` | VARCHAR | NO | PK | Nombre clave de la regla (ej. `sin_datos_personales`) |
| `descripcion` | VARCHAR | NO | - | Glosa de lo que evalúa la prueba |
| `valor` | DOUBLE | SÍ | - | Valor numérico obtenido en la ejecución |
| `umbral` | VARCHAR | SÍ | - | Condición de aprobación esperada |
| `cumple` | BOOLEAN | NO | - | Resultado booleano de la verificación |
| `detalle` | VARCHAR | SÍ | - | Severidad: `bloqueante` o `advertencia` |

---

### 2.2 Esquema `core` (Modelo Relacional Normalizado)

#### Tabla: `core.region`
Catálogo territorial de las 16 regiones de Chile.
- **Grano**: 1 fila por región oficial (código 1 al 16).
- **Filas actuales**: 16 filas.

| Columna | Tipo | Nulos | PK/FK | Descripción |
|---|---|---|---|---|
| `cod_region` | INTEGER | NO | PK | Código oficial INE/SUBDERE (1 a 16) |
| `nombre` | VARCHAR | NO | UNIQUE | Nombre oficial según la IDE Geoportal |
| `nombre_mineduc` | VARCHAR | NO | UNIQUE | Nombre como figura en `region_sede` de Mineduc |

#### Tabla: `core.comuna`
Catálogo comunal normalizado que cruza Mineduc y Geoportal.
- **Grano**: 1 fila por comuna normalizada.
- **Filas actuales**: 120 comunas con oferta formativa.

| Columna | Tipo | Nulos | PK/FK | Descripción |
|---|---|---|---|---|
| `id_comuna` | INTEGER | NO | PK | Secuencial único generado por el pipeline |
| `cod_cut` | INTEGER | SÍ | UNIQUE | Código Único Territorial (nulo en 20 comunas) |
| `nombre` | VARCHAR | NO | - | Nombre estándar con grafía oficial |
| `nombre_norm` | VARCHAR | NO | UNIQUE | Nombre en mayúsculas sin tilde para cruce |
| `provincia` | VARCHAR | SÍ | - | Nombre de la provincia |
| `cod_region` | INTEGER | NO | FK -> `core.region` | Región a la que pertenece |

#### Tabla: `core.institucion`
Catálogo de Instituciones de Educación Superior (IES).
- **Grano**: 1 fila por institución oficial SIES.
- **Filas actuales**: 144 instituciones.

| Columna | Tipo | Nulos | PK/FK | Descripción |
|---|---|---|---|---|
| `cod_inst` | INTEGER | NO | PK | Código SIES único de la institución |
| `nombre` | VARCHAR | NO | - | Nombre oficial más frecuente |
| `tipo_inst_1` | VARCHAR | SÍ | - | Tipo principal (Universidades / IP / CFT) |
| `tipo_inst_2` | VARCHAR | SÍ | - | Subtipo institucional 2 |
| `tipo_inst_3` | VARCHAR | SÍ | - | Subtipo institucional 3 |

#### Tabla: `core.sede`
Sedes académicas operadas por las IES.
- **Grano**: 1 fila por par `(cod_inst, cod_sede)`.
- **Filas actuales**: 481 sedes.

| Columna | Tipo | Nulos | PK/FK | Descripción |
|---|---|---|---|---|
| `cod_inst` | INTEGER | NO | PK, FK -> `institucion` | Institución que opera la sede |
| `cod_sede` | INTEGER | NO | PK | Código de sede (único solo dentro de la institución) |
| `nombre` | VARCHAR | NO | - | Nombre de la sede (ej. Casa Central, Campus San Joaquín) |
| `id_comuna` | INTEGER | NO | FK -> `comuna` | Comuna donde se localiza la sede |

#### Tabla: `core.inmueble`
Puntos georreferenciados de infraestructura de IES.
- **Grano**: 1 fila por inmueble/edificio individual.
- **Filas actuales**: 1.297 inmuebles.

| Columna | Tipo | Nulos | PK/FK | Descripción |
|---|---|---|---|---|
| `id_inmueble` | INTEGER | NO | PK | Secuencial del inmueble en la capa geo |
| `cod_inst` | INTEGER | NO | FK -> `institucion` | Institución propietaria o usufructuaria |
| `nombre` | VARCHAR | SÍ | - | Nombre del inmueble o campus |
| `id_comuna` | INTEGER | NO | FK -> `comuna` | Comuna de localización |
| `direccion` | VARCHAR | SÍ | - | Dirección postal normalizada |
| `latitud` | DOUBLE | NO | - | Latitud geográfica EPSG:4326 |
| `longitud` | DOUBLE | NO | - | Longitud geográfica EPSG:4326 |
| `anio` | INTEGER | SÍ | - | Año de levantamiento catastral (2020) |

#### Tabla: `core.nivel_carrera`
Categorización de niveles de formación académica y elegibilidad de tesis.
- **Grano**: 1 fila por nivel de carrera SIES.
- **Filas actuales**: 9 niveles.

| Columna | Tipo | Nulos | PK/FK | Descripción |
|---|---|---|---|---|
| `id_nivel` | INTEGER | NO | PK | Secuencial único |
| `nombre` | VARCHAR | NO | UNIQUE | Nombre nivel 1 (ej. Profesional Con Licenciatura) |
| `grupo` | VARCHAR | SÍ | - | Grupo de nivel 2 |
| `nivel_global` | VARCHAR | NO | - | Pregrado, Posgrado, Postítulo |
| `elegible_tesis` | VARCHAR | NO | CHECK | `'si'`, `'no'`, `'pendiente'` |

#### Tabla: `core.area_generica`
Agrupación curricular comparable entre instituciones.
- **Grano**: 1 fila por área genérica oficial SIES.
- **Filas actuales**: 285 áreas.

| Columna | Tipo | Nulos | PK/FK | Descripción |
|---|---|---|---|---|
| `id_area_generica` | INTEGER | NO | PK | Secuencial único |
| `nombre` | VARCHAR | NO | UNIQUE | Nombre del área genérica (ej. Ingeniería Civil en Computación) |

#### Tabla: `core.programa`
Oferta académica detallada por programa/versión institucional.
- **Grano**: 1 fila por código SIES de programa (`cod_sies_obt_tit`).
- **Filas actuales**: 15.469 programas.

| Columna | Tipo | Nulos | PK/FK | Descripción |
|---|---|---|---|---|
| `cod_programa` | VARCHAR | NO | PK | Código SIES que identifica unívocamente el programa |
| `cod_inst` | INTEGER | NO | FK -> `sede` | Institución |
| `cod_sede` | INTEGER | NO | FK -> `sede` | Sede |
| `cod_carrera` | INTEGER | SÍ | - | Código interno carrera (admite nulos en 352 casos) |
| `nombre_carrera` | VARCHAR | NO | - | Nombre específico del título |
| `id_nivel` | INTEGER | NO | FK -> `nivel_carrera` | Nivel formativo |
| `id_area_generica` | INTEGER | NO | FK -> `area_generica` | Área genérica comparable |
| `area_conocimiento`| VARCHAR | SÍ | - | Gran área OCDE |
| `cine_f_13_area` | VARCHAR | SÍ | - | Área específica clasificación CINE-F 2013 |
| `cine_f_13_subarea`| VARCHAR | SÍ | - | Subárea CINE-F 2013 |
| `jornada` | VARCHAR | SÍ | - | Diurna, Vespertina, A Distancia |
| `modalidad` | VARCHAR | SÍ | - | Presencial, Semipresencial, No Presencial |
| `tipo_plan` | VARCHAR | SÍ | - | Plan regular, especial, continuidad |
| `duracion_sem` | INTEGER | SÍ | - | Duración formal de la carrera en semestres |

#### Tabla: `core.titulacion` (Tabla de Hechos)
Hechos agregados de titulación. No contiene registros individuales de personas.
- **Grano**: periodo × `cod_programa` × género.
- **Filas actuales**: 26.359 registros que totalizan 328.998 títulos.

| Columna | Tipo | Nulos | PK/FK | Descripción |
|---|---|---|---|---|
| `periodo` | INTEGER | NO | PK | Año de titulación (2025) |
| `cod_programa` | VARCHAR | NO | PK, FK -> `programa` | Código SIES del programa académico |
| `genero` | INTEGER | NO | PK | Código gen_alu Mineduc (1: Masculino, 2: Femenino) |
| `n_titulos` | INTEGER | NO | CHECK > 0 | Cantidad de personas tituladas en esa combinación |
| `id_carga` | INTEGER | NO | FK lógica -> `gob.carga` | Lote de ingesta del cual se originó el registro |

---

### 2.3 Esquema `mart` (Vistas Analíticas de Consumo)

#### Vista: `mart.oferta`
Consolida la oferta a la unidad del MVP: periodo × región × área genérica × institución × nivel × modalidad.
- **Definición SQL**: Agrupa `core.titulacion` haciendo joins con `programa`, `sede`, `comuna`, `region`, `institucion`, `area_generica` y `nivel_carrera`.
- **Propósito**: Evaluación de masa crítica y filtros por elegibilidad.
- **Filas**: 15.011 combinaciones únicas. Total títulos: 328.998.

#### Vista: `mart.especializacion`
Calcula el Cociente de Especialización Territorial ($LQ$) por región y área genérica.
- **Fórmula**:
  $$LQ_{ra} = \frac{T_{ra} / \sum_{a} T_{ra}}{\sum_{r} T_{ra} / \sum_{r,a} T_{ra}}$$
- **Propósito**: Identificar disciplinas con ventaja comparativa regional revelada sin sesgo de volumen absoluto de Santiago.

#### Vista: `mart.sedes_geo`
Articula las coordenadas puntuales de los inmuebles con el volumen total de titulados de la institución en la comuna respectiva.
- **Propósito**: Renderizado en mapa interactivo de sedes y cobertura.
- **Filas**: 1.297 inmuebles (201 sin titulados en la comuna en 2025).

---

## 3. Hallazgos de la Auditoría y Pruebas Empíricas

A continuación se registran las pruebas cuantitativas ejecutadas sobre `data/processed/brujula.duckdb`:

### Hallazgo 1: Duplicaciones en Llaves Primarias y Unicidad
- **Resultado**: PASÓ (0 duplicados).
- **Evidencia SQL**:
  ```sql
  SELECT periodo, cod_programa, genero, count(*) 
  FROM core.titulacion GROUP BY 1,2,3 HAVING count(*) > 1; -- 0 filas
  SELECT cod_programa, count(*) 
  FROM core.programa GROUP BY 1 HAVING count(*) > 1; -- 0 filas
  SELECT cod_inst, cod_sede, count(*) 
  FROM core.sede GROUP BY 1,2 HAVING count(*) > 1; -- 0 filas
  ```

### Hallazgo 2: Integridad Referencial y Pérdida de Registros
- **Resultado**: PASÓ en oferta (0 registros huérfanos, 100% cuadre).
- **Evidencia SQL**:
  ```sql
  -- Títulos huérfanos sin programa
  SELECT count(*) FROM core.titulacion t 
  WHERE NOT EXISTS (SELECT 1 FROM core.programa p WHERE p.cod_programa = t.cod_programa); -- 0
  
  -- Programas huérfanos sin sede
  SELECT count(*) FROM core.programa p 
  WHERE NOT EXISTS (SELECT 1 FROM core.sede s WHERE s.cod_inst = p.cod_inst AND s.cod_sede = p.cod_sede); -- 0
  
  -- Cuadre de suma de títulos
  SELECT (SELECT sum(n_titulos) FROM core.titulacion) - (SELECT sum(n_titulos) FROM mart.oferta); -- 0
  ```

### Hallazgo 3: Comunas sin Código Único Territorial (CUT)
- **Resultado**: ADVERTENCIA / DEFECTO DE DATOS.
- **Descripción**: 20 comunas con titulados no están presentes en la capa geográfica del Geoportal 2020, por lo que quedan con `cod_cut IS NULL`. Esto afecta a 1.459 titulados.
- **Evidencia SQL**:
  ```sql
  SELECT count(*) FROM core.comuna WHERE cod_cut IS NULL; -- 20 comunas
  SELECT sum(t.n_titulos) 
  FROM core.titulacion t 
  JOIN core.programa p USING (cod_programa) 
  JOIN core.sede s USING (cod_inst, cod_sede) 
  JOIN core.comuna c USING (id_comuna) 
  WHERE c.cod_cut IS NULL; -- 1.459 títulos
  ```

### Hallazgo 4: Brecha Temporal entre Oferta e Infraestructura
- **Resultado**: ADVERTENCIA METODOLÓGICA.
- **Descripción**: La oferta formativa (`core.titulacion`) corresponde al periodo censal 2025, mientras que el catastro de inmuebles y coordenadas (`core.inmueble`) data del año 2020. Existe un descalce temporal de 5 años.
- **Evidencia SQL**:
  ```sql
  SELECT min(periodo), max(periodo) FROM core.titulacion; -- 2025, 2025
  SELECT min(anio), max(anio) FROM core.inmueble;         -- 2020, 2020
  ```

### Hallazgo 5: Sedes Académicas sin Coordenadas en la Capa Geo
- **Resultado**: DEFECTO DE ENTORNO FÍSICO.
- **Descripción**: De las 481 sedes institucionales de Mineduc, 49 sedes (10.18%) no tienen ningún inmueble asociado en la comuna según la capa geoespacial.
- **Evidencia SQL**:
  ```sql
  SELECT count(*) FROM core.sede s 
  WHERE NOT EXISTS (SELECT 1 FROM core.inmueble m WHERE m.cod_inst = s.cod_inst AND m.id_comuna = s.id_comuna); -- 49 sedes
  ```

### Hallazgo 6: Distorsión Territorial por Modalidad No Presencial
- **Resultado**: HALLAZGO CRÍTICO PARA EL RANKING.
- **Descripción**: Los programas no presenciales representan 82.525 títulos (25.08% del país). El 82.37% (67.976 títulos) están asignados a la Región Metropolitana por estar radicada allí la casa central, lo que distorsiona severamente la ubicación real de los egresados si no se filtran.
- **Evidencia SQL**:
  ```sql
  SELECT modalidad, sum(n_titulos), round(sum(n_titulos)*100.0/328998, 2) 
  FROM mart.oferta GROUP BY 1;
  -- No Presencial: 82.525 (25.08%) | Presencial: 231.261 (70.29%) | Semipresencial: 15.212 (4.62%)
  ```

### Hallazgo 7: Criterio Abierto de Elegibilidad de Tesis
- **Resultado**: BLOQUEO DE FOCALIZACIÓN (Decisión D3).
- **Descripción**: 147.571 títulos (44.85% de la oferta nacional) corresponden a niveles formativos clasificados como `'pendiente'` (Técnicos de Nivel Superior y Profesionales sin Licenciatura). Si se excluyen, la población objetivo se reduce drásticamente.
- **Evidencia SQL**:
  ```sql
  SELECT elegible_tesis, sum(n_titulos), round(sum(n_titulos)*100.0/328998, 2) 
  FROM mart.oferta GROUP BY 1;
  -- si: 116.053 (35.27%) | no: 65.374 (19.87%) | pendiente: 147.571 (44.85%)
  ```

### Hallazgo 8: Inestabilidad del Cociente de Especialización en Celdas Pequeñas
- **Resultado**: HALLAZGO ESTADÍSTICO CRÍTICO.
- **Descripción**: En disciplinas con pocos graduados a nivel nacional, un número minúsculo de títulos regionales infla artificialmente el Cociente de Especialización (LQ) a valores extremos (hasta 98.15 en Mecatrónica Arica con solo 9 titulados). Esto exige un umbral mínimo de masa crítica ($\tau \ge 5$ o $\tau \ge 10$) para evitar distorsiones en el ranking.
- **Evidencia SQL**:
  ```sql
  SELECT region, area_generica, n_titulos, round(cociente_especializacion, 2) 
  FROM mart.especializacion ORDER BY cociente_especializacion DESC LIMIT 3;
  -- Arica y Parinacota | Ingeniería en Mecatrónica | n=9 | LQ=98.15
  -- Aysén | Secretariado Ejecutivo | n=7 | LQ=80.33
  -- Ñuble | Otros Profesionales de Humanidades | n=13 | LQ=63.73
  ```

### Hallazgo 9: Estado de Tablas de Demanda, IA y Ranking
- **Resultado**: BLOQUEO COMPLETO POR FALTA DE DATOS.
- **Descripción**: Todas las tablas de demanda, sectores, indicadores, vínculos y ranking tienen 0 registros.
- **Evidencia SQL**:
  ```sql
  SELECT 'core.' || table_name, count 
  FROM (
    SELECT 'sector' AS table_name, (SELECT count(*) FROM core.sector) AS count UNION ALL
    SELECT 'indicador', (SELECT count(*) FROM core.indicador) UNION ALL
    SELECT 'indicador_region_sector', (SELECT count(*) FROM core.indicador_region_sector) UNION ALL
    SELECT 'indicador_area', (SELECT count(*) FROM core.indicador_area) UNION ALL
    SELECT 'vinculo_area_sector', (SELECT count(*) FROM core.vinculo_area_sector) UNION ALL
    SELECT 'criterio', (SELECT count(*) FROM core.criterio) UNION ALL
    SELECT 'escenario', (SELECT count(*) FROM core.escenario) UNION ALL
    SELECT 'peso', (SELECT count(*) FROM core.peso)
  ); -- Todos los conteos son estrictamente 0
  ```
