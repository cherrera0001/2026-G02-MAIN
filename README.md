# Brújula IA Regional

**Priorización territorial del cofinanciamiento de memorias y tesis aplicadas con Inteligencia Artificial**

[![Metodología: SDD](https://img.shields.io/badge/Metodolog%C3%ADa-GitHub%20Spec%20Kit-blue)](.specify/memory/constitution.md)
[![Python: 3.12+](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](pyproject.toml)
[![Database: DuckDB](https://img.shields.io/badge/Database-DuckDB-yellow.svg)](db/schema.sql)
[![Linter: Ruff](https://img.shields.io/badge/Linter-Ruff-black.svg)](https://github.com/astral-sh/ruff)
[![Licencia: Datos Abiertos](https://img.shields.io/badge/Licencia-Datos%20P%C3%BAblicos-green.svg)](gob.fuente)

---

## 1. Visión y Propósito del Producto

**Brújula IA Regional** simula una consultoría analítica para el **Ministerio de Economía**, diseñada para orientar con evidencia verificable la focalización territorial de subsidios de cofinanciamiento para memorias y tesis de educación superior aplicadas a desafíos productivos con componentes de Inteligencia Artificial (IA).

### El Problema
La inversión pública en capital humano avanzado suele asignarse de manera genérica, favoreciendo desproporcionadamente a la Región Metropolitana por tamaño bruto y desatendiendo las vocaciones productivas y el talento existente en regiones.

### La Solución (MVP)
Una herramienta analítica de soporte a la decisión que entrega:
1. **Diagnóstico Territorial de Oferta**: masa crítica y especialización de graduados por región, carrera e institución.
2. **Visualización Geoespacial**: mapa interactivo de sedes e inmuebles universitarios vinculados a la oferta formativa comunal.
3. **Reportes Ejecutivos Reproducibles**: informes generados desde código para autoridades públicas, con trazabilidad de fuentes y fechas en cada cifra.
4. **Ranking de Priorización Multicriterio**: ordenamiento transparente de combinaciones territoriales *(actualmente bloqueado científicamente hasta contar con fuentes externas validadas)*.

> [!IMPORTANT]
> **Alcance de Política Pública**: Esta herramienta orienta bases de convocatorias ministeriales. **No evalúa proyectos individuales, no selecciona tesis ni adjudica fondos**. La calidad intrínseca y mérito de cada postulación es resorte exclusivo de las comisiones evaluadoras.

---

## 2. Estado Actual del Sistema y Línea Base

El repositorio opera bajo una modernización controlada basada en **GitHub Spec Kit (SDD)**, preservando el código existente y distinguiendo rigurosamente lo que está implementado de lo que está bloqueado por falta de fuentes:

| Capacidad | Componente | Grano / Datos | Estado Operativo | Evidencia Verificable |
|---|---|---|---|---|
| **Oferta Educativa** | Mineduc / SIES 2025 | 328.998 títulos en 15.469 programas (16 regiones, 144 IES) | **IMPLEMENTADA Y PROBADA** | `gob.control_calidad.titulos_conservados = 1` |
| **Entorno Físico** | Geoportal IDE 2020 | 1.297 inmuebles IES con coordenadas lat/long | **IMPLEMENTADA Y PROBADA** | `gob.control_calidad.inmuebles_cargados = 1` |
| **Gobernanza y Privacidad** | Hash SHA-256 en DuckDB | Filtro en memoria; cero microdatos persistidos | **IMPLEMENTADA Y PROBADA** | `gob.control_calidad.sin_datos_personales = 0` |
| **Demanda y Sectores** | INE / SII / SENCE / BC | Panel regional de ocupación y valor agregado | **BLOQUEADA (0 filas)** | Requiere ingesta externa (Decisión D4 / #14) |
| **Vínculo y Exposición IA** | Índices OIT / FMI / CINE | Matriz puente área formativa–sector económico | **BLOQUEADA (0 filas)** | Requiere protocolo de calibración (#31) |
| **Ranking Multicriterio** | Función aditiva ponderada | Combinación región × área × institución | **BLOQUEADA CIENTÍFICAMENTE** | [Informe de Validación Científica](docs/analisis/VALIDACION_CIENTIFICA_RANKING.md) |
| **Visualización y Reporte** | Streamlit + Jinja2 | Dashboard interactivo y reporte reproducible | **EN DESARROLLO (ADR-002)** | Capa de datos lista en `mart.sedes_geo` |

---

## 3. Arquitectura y Stack Tecnológico

El sistema sigue una arquitectura monolítica modular en Python orientada al procesamiento analítico in-process:

- **Gestor de Entorno y Paquetes**: [`uv`](https://docs.astral.sh/uv/) (Astral) con Python >= 3.12 y locking determinístico en [`uv.lock`](uv.lock).
- **Motor de Base de Datos**: [DuckDB](https://duckdb.org/) embebido local (`data/processed/brujula.duckdb`). Procesa cientos de miles de registros en memoria en segundos con esquemas segregados:
  - `gob`: Linaje de fuentes, hashes SHA-256 de archivos y bitácora de controles de calidad.
  - `core`: Modelo relacional normalizado de territorio, instituciones, sedes y titulaciones.
  - `mart`: Vistas analíticas agregadas listas para consumo (`mart.oferta`, `mart.especializacion`, `mart.sedes_geo`).
- **Interfaz de Usuario (MVP)**: [Streamlit](https://streamlit.io/) aprobado como frontend oficial ([ADR-002](docs/adr/ADR-002-streamlit.md)) por su rapidez, desarrollo 100% Python y bajo acoplamiento.
- **Metodología de Desarrollo**: [GitHub Spec Kit](https://github.com/github/spec-kit) para especificaciones ejecutables (`specs/`) y seguimiento mediante [GitHub Project #6](https://github.com/users/cherrera0001/projects/6) ([ADR-001](docs/adr/ADR-001-github-projects.md)).

Diagramas C4 y flujos de datos completos disponibles en [**`docs/arquitectura/ARQUITECTURA_MINIMA.md`**](docs/arquitectura/ARQUITECTURA_MINIMA.md).

---

## 4. Estructura del Repositorio

```text
2026-G02-MAIN/
├── .specify/                    # Configuración, plantillas y scripts de GitHub Spec Kit
│   └── memory/constitution.md   # Constitución SDD del proyecto (10 principios obligatorios)
├── specs/                       # Especificaciones ejecutables por capacidad funcional
│   ├── 001-gobernanza-fuentes/  # Linaje, hashes SHA-256 e invariantes de calidad
│   ├── 002-oferta-formativa/    # Agregación de titulados, niveles y cociente de especialización
│   ├── 003-demanda-productiva/  # Clasificación CIIU y panel económico regional (BLOCKED)
│   ├── 004-vinculacion-ia/      # Tabla puente formativa-sectorial y métricas IA (BLOCKED)
│   ├── 005-priorizacion-ranking/# Motor multicriterio y análisis de estabilidad (BLOCKED)
│   └── 006-visualizacion-reportes/# Visualización de sedes y reporte ministerial
├── docs/                        # Documentación técnica, académica y metodológica
│   ├── README.md                # Índice canónico de documentación
│   ├── modelos/                 # MER (.drawio), Relacional (DBML), Diccionario de Datos
│   ├── arquitectura/            # Diagramas C4 y flujos DFD
│   ├── analisis/                # Validación científica y justificación de bloqueo del ranking
│   ├── decisiones/              # Registro formal de decisiones abiertas (D1 a D8)
│   ├── adr/                     # Architectural Decision Records ratificados (ADR-001, ADR-002)
│   └── sdd/                     # Reporte de validación SDD integral
├── data/                        # Datos fuente comprimidos (fuera de Git en processed)
│   ├── oferta/                  # Titulados-Ed-Superior-2025.rar (Mineduc)
│   ├── geo/                     # Shapefile de establecimientos de educación superior (IDE)
│   └── demanda/                 # Referencias y enlaces a fuentes físicas y de infraestructura
├── db/
│   └── schema.sql               # Única definición DDL de la estructura relacional DuckDB
├── src/
│   └── pipeline/
│       └── construir_bd.py      # Pipeline reproducible de extracción, normalización y carga
├── CLAUDE.md                    # Contexto y directrices operativas para agentes Claude Code
├── pyproject.toml               # Configuración del proyecto y dependencias
└── uv.lock                      # Registro estricto de versiones de dependencias
```

---

## 5. Guía de Inicio Rápido (Quickstart)

### Requisitos Previos
1. **Git**: Para control de versiones.
2. **`uv`**: Instalador y gestor de entornos Python ([Instrucciones de instalación](https://docs.astral.sh/uv/getting-started/installation/)).
3. **Extractor RAR**: `unrar`, WinRAR o 7-Zip en el PATH para descomprimir los microdatos de Mineduc.

### Instalación y Ejecución

1. **Clonar el repositorio**:
   ```powershell
   git clone https://github.com/cherrera0001/2026-G02-MAIN.git
   cd 2026-G02-MAIN
   ```

2. **Sincronizar el entorno Python**:
   ```powershell
   uv sync
   ```

3. **Reconstruir la base de datos DuckDB**:
   ```powershell
   uv run python -m src.pipeline.construir_bd
   ```
   *Salida esperada:*
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
   Base lista: data\processed\brujula.duckdb
   ```

4. **Verificar calidad del código (Linter)**:
   ```powershell
   uvx ruff check .
   ```

---

## 6. Historias de Usuario Reconciliadas y Backlog

El seguimiento operativo oficial se gestiona exclusivamente a través de **[GitHub Project #6](https://github.com/users/cherrera0001/projects/6)** y sus 47 issues asociados ([ADR-001](docs/adr/ADR-001-github-projects.md)). 

La trazabilidad completa se detalla en [**`docs/BACKLOG_RECONCILIADO.md`**](docs/BACKLOG_RECONCILIADO.md):

| Historia / Épica | Usuario | Descripción Sintética | Estado Real | Capacidad SDD |
|---|---|---|---|---|
| **R1 ([#1](https://github.com/cherrera0001/2026-G02-MAIN/issues/1))** | Responsable del Programa | Saber dónde focalizar los recursos disponibles | Épica desglosada en P-HU04 | `005-priorizacion-ranking` |
| **R2 ([#2](https://github.com/cherrera0001/2026-G02-MAIN/issues/2))** | Analista Ministerial | Problemas productivos abordables por cada carrera | Desglosada en P-HU03 | `004-vinculacion-ia` |
| **R3 ([#3](https://github.com/cherrera0001/2026-G02-MAIN/issues/3))** | Empresa Local | Probar mejoras con IA a costo y riesgo acotado | **Fuera del MVP** | Fuera de alcance analítico |
| **R4 ([#4](https://github.com/cherrera0001/2026-G02-MAIN/issues/4))** | Analista / Público | Diagnóstico de talento formado cerca territorialmente | Cubierta en P-HU01 / P-HU06 | `002-oferta-formativa` |
| **P-HU01 ([#5](https://github.com/cherrera0001/2026-G02-MAIN/issues/5))** | Analista Ministerial | Oferta de titulados por región, área genérica e IES | **Implementada en base** | `002-oferta-formativa` |
| **P-HU02 ([#6](https://github.com/cherrera0001/2026-G02-MAIN/issues/6))** | Analista Ministerial | Evidencia pública de demanda y vocación regional | **Bloqueada (D4)** | `003-demanda-productiva` |
| **P-HU03 ([#7](https://github.com/cherrera0001/2026-G02-MAIN/issues/7))** | Analista Ministerial | Vínculo justificado área formativa–sector económico | **Bloqueada** | `004-vinculacion-ia` |
| **P-HU04 ([#8](https://github.com/cherrera0001/2026-G02-MAIN/issues/8))** | Responsable del Programa | Ranking de focalización multicriterio reproducible | **Bloqueada científicamente** | `005-priorizacion-ranking` |
| **P-HU05 ([#9](https://github.com/cherrera0001/2026-G02-MAIN/issues/9))** | Responsable del Programa | Análisis de estabilidad del ranking ante cambio de pesos | **Bloqueada** | `005-priorizacion-ranking` |
| **P-HU06 ([#10](https://github.com/cherrera0001/2026-G02-MAIN/issues/10))** | Responsable del Programa | Visualización espacial y reporte con recomendaciones | **En desarrollo** | `006-visualizacion-reportes` |

---

## 7. Registro de Decisiones Abiertas (D1 a D8)

El equipo humano y la contraparte ministerial deben ratificar las siguientes decisiones documentadas en [**`docs/decisiones/REGISTRO_DECISIONES_PENDIENTES.md`**](docs/decisiones/REGISTRO_DECISIONES_PENDIENTES.md):

- **D1 ([#11](https://github.com/cherrera0001/2026-G02-MAIN/issues/11))**: Unidad del ranking (Región × Área Genérica × IES vs. Carrera × Sector en piloto).
- **D2 ([#12](https://github.com/cherrera0001/2026-G02-MAIN/issues/12))**: Cobertura geográfica nacional (16 regiones) vs. región piloto.
- **D3 ([#13](https://github.com/cherrera0001/2026-G02-MAIN/issues/13))**: Elegibilidad de tesis para el 44.85% de egresados en niveles técnicos y profesionales sin licenciatura.
- **D4 ([#14](https://github.com/cherrera0001/2026-G02-MAIN/issues/14))**: Fuentes de demanda y plan de contingencia ante falta de datos de IA.
- **D5 ([#15](https://github.com/cherrera0001/2026-G02-MAIN/issues/15))**: Usuario principal exclusivo (Ministerio de Economía).
- **D6 ([#16](https://github.com/cherrera0001/2026-G02-MAIN/issues/16))**: Umbral de secreto estadístico y estabilidad ($\tau = 5$).
- **D7 ([#17](https://github.com/cherrera0001/2026-G02-MAIN/issues/17))**: Ratificación de Streamlit para el despliegue del MVP analítico ([ADR-002](docs/adr/ADR-002-streamlit.md)).
- **D8 ([#18](https://github.com/cherrera0001/2026-G02-MAIN/issues/18))**: Retención de comprimidos en Git vs. almacenamiento blob externo.

---

## 8. Privacidad, Ética y Reproducibilidad

El desarrollo se rige por la **[Constitución SDD](.specify/memory/constitution.md)** del proyecto:
1. **Privacidad por Diseño**: Los microdatos individuales de titulados (MRUN, fecha de nacimiento, género individual) se procesan estrictamente en tablas temporales en memoria RAM. Ningún registro personal se persiste en disco ni se publica en Git.
2. **Evidencia Verificable**: Toda cifra mostrada en la plataforma, mapa o informe lleva cita a su organismo de origen, fecha del levantamiento y limitaciones de cobertura.
3. **Tratamiento Ético de Faltantes**: La carencia de datos en un territorio o disciplina **nunca se penaliza con puntaje cero ni se imputa con supuestos arbitrarios**. Se declara formalmente como "evidencia insuficiente".
