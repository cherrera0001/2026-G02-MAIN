### About

Este repositorio contiene informacion publica sobre las caracteristicas de la titulacion en Universidades, asi como su ubicacion, red de vialidad y otros servicios publicos, asi como indicaciones sobre otras fuentes de datos (e.g. OpenStreetMap).

### Guía del repositorio

- [Estado actual y decisiones pendientes](#estado-actual-y-decisiones-pendientes)
- [A. Cómo empezar y usar Claude Code](#a-cómo-empezar-y-usar-claude-code)
- [B. Cómo trabajar con los datos](#b-cómo-trabajar-con-los-datos)
- [C. Cómo versionar los cambios](#c-cómo-versionar-los-cambios)
- [D. Cómo administrar el GitHub Project](#d-cómo-administrar-el-github-project)
- [E. Cómo mantener el backlog con Claude Code](#e-cómo-mantener-el-backlog-con-claude-code)
- [Cambios de esta versión](#cambios-de-esta-versión)

### Visión del producto

Como contraparte a la consultoria del Ministerio de Economia, se necesita utilizar la información disponible en este repositorio, junto con datos adicionales sobre los focos de desarrollo estrategico regional por industria, para identificar de manera objetiva qué carreras podrían beneficiarse en mayor medida de los subsidios públicos orientados al desarrollo de habilidades de IA complementarias, a nivel regional. Esto permitirá priorizar la asignación de recursos, focalizando los apoyos en aquellas carreras e industrias que presentan mayores necesidades según criterios basados en datos y evidencia territorial.

### Objetivos
- Acceso a bases de datos relevantes sobre la oferta y demanda laboral, desarrollo regional estrategico y su entorno físico.
- Herramientas o scripts que permitan analizar y cruzar la información de manera eficiente usando modelos de Aprendizaje Automatico.
- Visualizaciones o reportes que faciliten la toma de decisiones para la asignación de subsidios.

### Colocar MVP en 1 o 2 parrafos:
El programa busca cerrar la brecha entre la oferta de capital humano y las demandas del sector productivo mediante el cofinanciamiento de memorias y tesis de pregrado y postgrado aplicadas a desafíos industriales concretos. A través de un incentivo económico directo a estudiantes y tutores, la iniciativa conecta el talento emergente —con especial énfasis en beneficiarios de gratuidad de diversas disciplinas— con empresas locales que requieren incorporar soluciones tecnológicas, automatización y herramientas de Inteligencia Artificial en sus procesos productivos.

La focalización y asignación de los recursos se sustentará en un modelo analítico territorial que cruza la oferta de graduados por institución con las vocaciones productivas y el nivel de exposición/complementariedad tecnológica de cada región. De este modo, la política pública del Ministerio no reparte fondos de forma genérica, sino que canaliza la inversión estratégica hacia proyectos de I+D aplicada que aumenten la productividad local, aseguren inserción laboral de alto valor agregado y reduzcan el descalce de competencias en todo el país.

### MVP:
Una herramienta de priorización que entrega un ranking de combinaciones región × carrera × institución para focalizar el cofinanciamiento de tesis aplicadas, con una visualización por región y un reporte con recomendaciones para el Ministerio.

### Historias de usuario:

1. Como responsable del programa, quiero saber dónde focalizar los recursos disponibles, para que la inversión pública llegue donde más ayuda a cerrar la brecha entre formación y necesidades productivas.
   
-Criterios de aceptación:
-Tareas:

2. Como analista del Ministerio, quiero entender qué problemas de los sectores productivos pueden abordar los estudiantes de cada carrera, para orientar temas de tesis donde la IA aporte valor.

-Criterios de aceptación:
-Tareas:

3. Como empresa local, quiero probar mejoras con IA y automatización con costo y riesgo acotados, para decidir si vale la pena una inversión mayor. 

-Criterios de aceptación:
-Tareas:

4. Como empresa local, quiero saber qué talento se forma cerca de mí y en qué áreas, para encontrar colaboradores sin grandes desplazamientos.

-Criterios de aceptación:
-Tareas:

### Entregables
### Sprint 1: 

---

## Estado actual y decisiones pendientes

### Qué existe hoy (observado en el repositorio)

- Un pipeline, [src/pipeline/construir_bd.py](src/pipeline/construir_bd.py), que construye una base DuckDB con la estructura de [db/schema.sql](db/schema.sql).
- Datos cargados: oferta (titulados 2025) y sedes de educación superior (2020).
- Las tablas de demanda, sectores, indicadores, vínculos área–sector, criterios y pesos están definidas en el esquema pero vacías.
- No existen todavía: ranking, visualización, reporte, aplicación web, API, pruebas automatizadas ni integración continua.
- Las cuatro historias de este README no tienen criterios de aceptación ni tareas. En GitHub están registradas como issues con «criterios pendientes de validar», junto con las seis historias propuestas en `docs/COHERENCIA_HISTORIAS.md` (etiqueta `propuesta`), sus tareas y las decisiones abiertas. El índice está en [docs/BACKLOG.md](docs/BACKLOG.md).

### Documentos de análisis (propuestas, no acuerdos)

- [docs/COHERENCIA_HISTORIAS.md](docs/COHERENCIA_HISTORIAS.md): auditoría de las historias y conjunto propuesto para el MVP.
- [docs/MER_MR_ARQUITECTURA_PLATAFORMA.md](docs/MER_MR_ARQUITECTURA_PLATAFORMA.md): modelo de datos y arquitectura propuesta.
- [docs/PROMPT_AGENTES_BRUJULA_IA.md](docs/PROMPT_AGENTES_BRUJULA_IA.md): planteamiento inicial de agentes y backlog semilla. Propone más agentes y tecnologías (FastAPI, polars, Parquet) que los que el repositorio usa hoy; la base agentica vigente es la de la sección A.

### Decisiones que solo el equipo puede cerrar

| Decisión | Estado |
|---|---|
| Unidad del ranking: región × área/carrera × institución, o carrera × sector en una región piloto | Pendiente |
| Regiones incluidas | Pendiente |
| Niveles de formación elegibles | Pendiente. El pipeline trae una propuesta inicial (`ELEGIBLE_TESIS`); con ella, el 44,85 % de los títulos queda en niveles sin decidir |
| Fuentes de demanda, productividad y exposición a IA | Pendiente. Ninguna está en el repositorio ni validada |
| Usuario principal | Pendiente |

Otras decisiones abiertas: tratamiento de la modalidad no presencial, umbral para suprimir celdas pequeñas, tecnología de la interfaz, y si los comprimidos de datos deben seguir versionados (ver sección B). El detalle está en la sección 6 de [docs/COHERENCIA_HISTORIAS.md](docs/COHERENCIA_HISTORIAS.md).

---

## A. Cómo empezar y usar Claude Code

### Requisitos

| Herramienta | Para qué | Cómo comprobarla |
|---|---|---|
| Git | Versionar | `git --version` |
| [uv](https://docs.astral.sh/uv/) | Entorno Python y dependencias. El proyecto pide Python 3.12 o superior; uv lo instala si falta | `uv --version` |
| `unrar`, WinRAR o 7-Zip | Extraer el `.rar` de titulados. El pipeline los busca en el PATH y en `C:\Program Files\WinRAR\` y `C:\Program Files\7-Zip\` | — |
| [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) | Trabajar con los agentes | `claude --version` |
| GitHub CLI (opcional) | Abrir Pull Requests y administrar el Project desde la terminal | `gh --version` |

Esta guía se comprobó con Claude Code 2.1.290, uv 0.12.17, Git 2.56 y GitHub CLI 2.100 en Windows con PowerShell.

### Instalación

```powershell
git clone https://github.com/cherrera0001/2026-G02-MAIN.git
cd 2026-G02-MAIN
uv sync
```

`uv sync` crea `.venv/` con las versiones de `uv.lock`. El proyecto no usa variables de entorno: no hace falta crear `.env`.

### Iniciar Claude Code

Siempre desde la raíz del repositorio, para que cargue [CLAUDE.md](CLAUDE.md) y los agentes de [.claude/agents/](.claude/agents/):

```powershell
claude
```

Dentro de la sesión, `/agents` muestra los agentes disponibles.

### Agentes del proyecto

| Agente | Cuándo usarlo | Qué no hace |
|---|---|---|
| `product-owner` | Redactar o revisar historias, criterios de aceptación y tareas con peso y horas; revisar la coherencia del alcance | No modifica datos ni código; no cierra decisiones del equipo |
| `analista-fuentes` | Inventariar y evaluar una fuente y su licencia; redactar su ficha | No declara validada una fuente sin evidencia; no descarga datos al repositorio |
| `ingeniero-datos` | Cambiar el pipeline, el esquema o los controles de calidad | No persiste ni publica microdatos; no carga fuentes sin decisión de uso |
| `cientifico-datos` | Indicadores, vínculos área–sector, ranking y sensibilidad | No mezcla observado, inferido y propuesto; no elige unidad ni pesos por el equipo |
| `revisor-qa` | Antes de versionar: reproducibilidad, lint, documentación y seguridad del diff | No corrige código ajeno ni cambia decisiones del Product Owner |

No hay agente de interfaz: el repositorio no tiene aplicación y la tecnología de la interfaz es una decisión abierta.

Formas de delegar:

- **Pedirlo en el mensaje.** Por ejemplo: «Usa el agente `revisor-qa` para revisar los cambios pendientes antes de que haga commit». Claude Code también puede delegar por su cuenta cuando la tarea coincide con la descripción de un agente.
- **Abrir la sesión completa como un agente:**

  ```powershell
  claude --agent product-owner
  ```

Cada agente declara las herramientas que puede usar; por ejemplo, `product-owner` no tiene terminal. Las rutas que cada agente puede modificar son instrucciones, no un bloqueo técnico: por eso hay que revisar los cambios.

### Revisar cambios antes de aceptarlos

1. En el modo por defecto, Claude Code pide confirmación antes de editar un archivo o ejecutar un comando, y muestra el cambio propuesto. Léelo antes de aceptar.
2. Para tareas grandes, pide primero un plan (el modo plan se alterna con `Shift+Tab`) y aprueba el plan antes de que edite.
3. Al terminar, revisa lo que quedó en disco:

   ```powershell
   git status
   git diff
   ```

4. Pide a `revisor-qa` una revisión antes de hacer commit.

No se recomienda `--dangerously-skip-permissions`: esa opción elimina todas las confirmaciones, de modo que Claude Code edita archivos y ejecuta comandos sin preguntar. Solo tiene sentido en un entorno aislado y confiable, con el trabajo respaldado en Git y sin datos que no se puedan recuperar.

---

## B. Cómo trabajar con los datos

### Inventario de fuentes

Ninguna fuente tiene todavía una ficha en `docs/fuentes/` ni una decisión de uso registrada por el equipo. «Cargada» significa que el pipeline la lee y pasa sus controles; no significa que el equipo la haya validado para el ranking.

| Fuente | Organismo | Dónde está | Estado |
|---|---|---|---|
| [Titulados en educación superior](https://datosabiertos.mineduc.cl/titulados-en-educacion-superior/), 2025 | Mineduc | `data/oferta/Titulados-Ed-Superior-2025.rar` | Cargada: 328.998 filas, 16 regiones. Solo un periodo. Licencia sin registrar. Contiene microdatos; el pipeline solo persiste conteos |
| [Establecimientos de educación superior](https://geoportal.cl/geoportal/catalog/35554/Establecimientos%20de%20Educaci%C3%B3n%20Superior), 2020 | IDE Chile | `data/geo/*.zip` | Cargada: 1.297 inmuebles. No trae código de sede: se une por institución y comuna. Licencia CC-BY según el catálogo del pipeline, sin ficha que lo respalde |
| [Instalaciones y edificaciones](https://datos.gob.cl/dataset/categoria-geoespacial-instalaciones-y-edificaciones) | IDE Chile | Solo el enlace, en `data/demanda/README.md` | No se carga. Sin evaluar |
| [Infraestructura MOP](https://geomop.mop.gob.cl/descargas/) | Ministerio de Obras Públicas | Solo el enlace, en `data/demanda/README.md` | No se carga. Sin evaluar |
| Demanda laboral, productividad o vocación productiva regional, exposición a IA | — | No están en el repositorio | Sin fuente. Los documentos de `docs/` nombran candidatas; todas siguen pendientes de verificar |

La carpeta `data/demanda/` no contiene demanda laboral: sus enlaces son de entorno físico (infraestructura y edificación pública).

### Proponer una nueva fuente

1. Copia [docs/fuentes/PLANTILLA_FICHA.md](docs/fuentes/PLANTILLA_FICHA.md) como `docs/fuentes/<id_fuente>.md`.
2. Completa todos los campos: URL, organismo, licencia, fecha de consulta, formato, cobertura temporal y territorial, granularidad, campos útiles y limitaciones. Lo que no se pudo comprobar se escribe «sin comprobar».
3. Deja la decisión de uso en **pendiente**. El agente `analista-fuentes` puede redactar la ficha.
4. El equipo decide «usar» o «descartar» y anota fecha y motivo en la ficha.
5. Solo con decisión «usar» se incorpora la fuente al pipeline (agente `ingeniero-datos`): registro en `gob.fuente`, carga en `gob.carga` y un control de calidad por cada unión nueva.

### Dónde van los archivos originales

- Los comprimidos que ya están versionados quedan donde están: `data/oferta/*.rar` y `data/geo/*.zip`. El pipeline los extrae a `data/raw/oferta/` y `data/raw/geo/`.
- Como alternativa, se puede dejar el CSV ya extraído en `data/raw/oferta/` y el `.dbf` en `data/raw/geo/`.
- Los archivos de una fuente nueva van en `data/raw/<capa>/`, que está fuera de Git. No se agregan comprimidos nuevos al repositorio sin decisión del equipo.
- El pipeline lee todos los CSV de `data/raw/oferta/`, pero solo se ha ejecutado con el periodo 2025: cargar más años requiere comprobarlo.

### Ejecutar el pipeline

```powershell
uv run python -m src.pipeline.construir_bd
```

- Salida: `data/processed/brujula.duckdb` (unos 15 MB, fuera de Git).
- La base se borra y se recrea en cada ejecución. Si falla un control bloqueante, la base anterior no se reemplaza y queda `brujula.tmp.duckdb` para revisar.
- La ejecución imprime los controles de calidad y el número de filas por tabla.

### Reproducir desde un clon limpio

```powershell
git clone https://github.com/cherrera0001/2026-G02-MAIN.git
cd 2026-G02-MAIN
uv sync
uv run python -m src.pipeline.construir_bd
```

Requiere un extractor de `.rar` instalado. El clon ya trae los dos comprimidos, así que no hace falta descargar nada.

### Revisar controles de calidad y cobertura

Controles registrados en la última ejecución:

```powershell
uv run python -c "import duckdb; duckdb.connect('data/processed/brujula.duckdb', read_only=True).sql('SELECT regla, valor, umbral, cumple, detalle FROM gob.control_calidad').show(max_width=160)"
```

Archivos cargados, con periodo, filas y hash:

```powershell
uv run python -c "import duckdb; duckdb.connect('data/processed/brujula.duckdb', read_only=True).sql('SELECT id_fuente, archivo, periodo, filas_leidas, left(sha256, 12) AS sha256_inicio FROM gob.carga').show(max_width=160)"
```

| Control | Tipo | Qué mide | Valor en la última ejecución |
|---|---|---|---|
| `titulos_conservados` | Bloqueante | Títulos agregados / filas leídas | 1 |
| `regiones` | Bloqueante | Regiones con titulados | 16 |
| `sin_datos_personales` | Bloqueante | Columnas persistentes con identificadores o fechas de nacimiento | 0 |
| `inmuebles_cargados` | Bloqueante | Inmuebles cargados / filas de la capa | 1 |
| `cargas_huerfanas` | Bloqueante | Títulos sin carga registrada | 0 |
| `comunas_sin_cut` | Aviso | Comunas con titulados que no están en la capa de sedes | 20 |
| `titulos_con_punto` | Aviso | Títulos presenciales o semipresenciales cuya institución tiene un inmueble en la comuna | 0,9637 |
| `niveles_pendientes` | Aviso | Títulos en niveles con elegibilidad sin decidir | 0,4485 |

### Qué queda fuera de Git y de cualquier publicación

- `data/raw/` (archivos extraídos, incluido el CSV de titulados) y `data/processed/` (base generada).
- `.env`, `.venv/`, cachés y `chat-wsp/` (conversación del equipo, con nombres y datos personales).
- Microdatos: `mrun`, fecha de nacimiento, edad y filas individuales no se persisten en la base ni se muestran en reportes, documentación, capturas o una futura aplicación. Solo se publican agregados.
- Antes de publicar cualquier resultado, el equipo debe decidir si suprime o agrupa celdas con pocos casos.

**Para revisar por el equipo:** `data/oferta/Titulados-Ed-Superior-2025.rar` ya está versionado y contiene los microdatos de origen (dato abierto de Mineduc). Mantenerlo o retirarlo del repositorio es una decisión pendiente; retirarlo obligaría a descargar el archivo antes de ejecutar el pipeline.

---

## C. Cómo versionar los cambios

Comandos para PowerShell, uno por línea, desde la raíz del repositorio.

### 1. Revisar el estado y actualizar

```powershell
git status
git switch main
git pull --ff-only origin main
```

Si `git status` muestra cambios sin versionar, no hace falta descartarlos: el paso siguiente los lleva a la rama nueva.

### 2. Crear una rama descriptiva

```powershell
git switch -c docs/base-agentica-claude
```

Formato sugerido: `tipo/descripcion-corta`, con tipos como `docs`, `feat`, `fix` o `datos`.

### 3. Agregar archivos explícitamente

Nombra cada archivo o carpeta; evita `git add .` y `git add -A`, que pueden incluir archivos no deseados.

```powershell
git add CLAUDE.md README.md .gitignore
git add .claude/agents
git add docs/fuentes/PLANTILLA_FICHA.md
git add db/schema.sql
```

### 4. Verificar qué se incluirá

```powershell
git status
git diff --staged --stat
git diff --staged
```

Comprueba que no aparezcan `.env`, `chat-wsp/`, `data/raw/`, `data/processed/` ni `.venv/`. Para confirmar que una ruta está ignorada:

```powershell
git check-ignore -v .env chat-wsp data/raw data/processed
```

Para sacar del staging un archivo agregado por error, sin perder sus cambios:

```powershell
git restore --staged <archivo>
```

### 5. Commits pequeños y con propósito

Un commit por cambio lógico, con un mensaje que explique el porqué:

```powershell
git commit -m "fix: permite cod_carrera nulo para que el pipeline cargue la fuente completa"
```

Si hay cambios de distinta naturaleza, repite los pasos 3 a 5 para cada grupo.

### 6. Subir la rama y abrir el Pull Request

```powershell
git push -u origin docs/base-agentica-claude
```

Abre el Pull Request desde la página del repositorio en GitHub (botón «Compare & pull request») o, con GitHub CLI:

```powershell
gh pr create --base main --fill
```

Pide revisión a otra persona del equipo antes de fusionar.

### Un archivo ignorado que ya estaba versionado

Agregar una ruta a `.gitignore` no retira los archivos que ya están en Git. Para ver si una ruta está versionada:

```powershell
git ls-files <ruta>
```

Para dejar de versionar un archivo sin borrarlo del disco:

```powershell
git rm --cached <archivo>
git commit -m "chore: deja de versionar <archivo>"
```

Esto lo retira de los commits siguientes, pero el archivo sigue en la historia anterior. Si contenía un secreto, hay que cambiar ese secreto; reescribir la historia es una operación aparte que el equipo debe acordar.

---

## D. Cómo administrar el GitHub Project

El Project existe: **[Brújula IA Regional — Backlog](https://github.com/users/cherrera0001/projects/6)** (número 6, propietario `cherrera0001`), vinculado al repositorio. Era un tablero vacío sin nombre creado desde la pestaña Projects del repositorio; el 5 de octubre de 2026 se renombró y se le agregaron los campos de abajo con GitHub CLI. Para dar acceso al equipo: en el Project, menú **⋯** → **Settings** → **Manage access** (paso de la interfaz web, no recorrido en esta tarea).

### Estados y vistas

1. El campo **Status** conserva las opciones por defecto de GitHub: `Backlog`, `Ready`, `In progress`, `In review`, `Done`. Equivalen a Backlog, Por hacer, En curso, En revisión y Hecho. Si el equipo quiere los nombres en español, se cambian desde la web (configuración del campo); la CLI no edita opciones de `Status`.
2. Vista **Board**, agrupada por `Status`: para el trabajo diario.
3. Vista **Table**: para estimar y revisar; conviene agruparla por `Sprint` o por `Tipo` y mostrar la suma de `Peso` y de `Horas estimadas`. Las vistas se configuran desde la web; no se verificaron en esta tarea.

### Campos

Campos creados con `gh project field-create` (comprobados con `gh project field-list 6 --owner cherrera0001`):

| Campo | Tipo | Uso |
|---|---|---|
| `Peso` | Número (0 a 5) | Esfuerzo relativo de la historia o la tarea, según la escala de abajo |
| `Tipo` | Selección única: Historia, Tarea, Decisión, Investigación | Qué es la tarjeta |
| `Modelo Claude` | Selección única: Opus, Sonnet, Haiku | Modelo de Claude Code sugerido para trabajar el issue (ver sección E) |
| `Sprint` | Selección única: Pendiente, Sprint 1, Sprint 2 | `Pendiente` hasta que el equipo comprometa la tarjeta |
| `Horas estimadas` | Número | Estimación de tiempo, independiente del peso; vacío si no hay fundamento |
| `Esfuerzo real` | Número | Horas reales, registradas al cerrar la tarea |

`Priority`, `Size`, `Estimate`, `Start date` y `Target date` vienen de la plantilla de GitHub y no se usan. La CLI no crea campos de tipo iteración; si el equipo prefiere `Sprint` como iteración con fechas, se cambia desde la web. Las fechas de cada sprint se toman del programa del curso; este repositorio no las confirma.

### Escala de peso y esfuerzo

| Peso | Significado |
|---|---|
| 0 | Decisión o registro sin esfuerzo de construcción; puede tener horas de reunión, pero no horas de desarrollo |
| 1 | Hasta 1 hora; cambio acotado y conocido |
| 2 | 2–3 horas; solución conocida |
| 3 | Aproximadamente media jornada; incertidumbre moderada |
| 4 | Aproximadamente una jornada o cambio entre varias piezas |
| 5 | Más de una jornada o alta incertidumbre; dividir en tareas menores antes de iniciar |

Reglas de uso:

- `Peso` y `Horas estimadas` son campos separados. El peso es una escala relativa de complejidad y esfuerzo; las horas son una estimación de tiempo. Un peso no se convierte automáticamente en una cantidad exacta de horas.
- Una historia tiene un **peso global** propio (un solo valor 0–5 para cumplir todos sus criterios), explicado en una frase. No es el promedio ni la suma de sus tareas: una tarea difícil no se esconde detrás de varias fáciles.
- Al cerrar cada tarea se registra el esfuerzo real en `Esfuerzo real`. Comparar la estimación con la realidad sirve para mejorar las estimaciones siguientes, no para evaluar ni penalizar a las personas.

### Historias, criterios y tareas

1. **Cada historia es un issue.** En el repositorio: **Issues** → **New issue** → plantilla «User Story template» (etiqueta `user story`). Los criterios de aceptación se escriben en el cuerpo como lista de casillas, junto con la Definition of Done de la plantilla. Lo que el equipo no ha aprobado lleva además la etiqueta `propuesta`.
2. **Cada tarea es un issue vinculado.** Desde el issue de la historia, usa **Create sub-issue** con la plantilla «Tarea template» (etiqueta `tarea`); con GitHub CLI, `gh issue create --parent <número de la historia>`.
3. **Agrega los issues al Project** desde el panel lateral del issue (**Projects**) y completa `Tipo`, `Peso`, `Modelo Claude` y `Sprint = Pendiente`; `Horas estimadas` solo si hay fundamento.
4. Las plantillas están en [.github/ISSUE_TEMPLATE/](.github/ISSUE_TEMPLATE/). Usan el campo `type`, que requiere tipos de issue configurados por el dueño del repositorio; este repositorio no los tiene, así que bastan las etiquetas.
5. **Las decisiones del equipo** son issues con etiqueta `decisión` y peso 0. No son requisitos: registran la pregunta, las opciones documentadas y qué bloquean.

### Mover el trabajo por el tablero

| Estado | Cuándo |
|---|---|
| `Backlog` | Historia, tarea o decisión registrada, aún sin comprometer. Todo lo nuevo entra aquí |
| `Ready` (Por hacer) | Comprometida para el sprint por el equipo, con peso, horas y responsable |
| `In progress` (En curso) | Alguien la está trabajando en una rama; conviene una tarea a la vez por persona |
| `In review` (En revisión) | Tiene Pull Request abierto que referencia el issue (`Closes #123`) |
| `Done` (Hecho) | Pull Request fusionado, criterios de aceptación marcados y `Esfuerzo real` registrado |

Solo el equipo mueve tarjetas fuera de `Backlog`: Claude Code las deja ahí.

### Cerrar el sprint

1. **Demo:** mostrar el incremento funcionando con datos reales, historia por historia, contra sus criterios de aceptación.
2. **Evidencias:** en cada historia, enlazar los Pull Requests y dejar el comando o la salida que demuestra cada criterio. Una historia pasa a `Hecho` solo si cumple su Definition of Done.
3. **Retrospectiva:** comparar `Horas estimadas` con `Esfuerzo real` por tarea, registrar qué funcionó y qué cambiar, y convertir las mejoras en tareas del sprint siguiente.
4. Lo no terminado vuelve al Backlog o pasa al sprint siguiente, con su estimación revisada.

### GitHub CLI

Requiere el permiso `project` en el token (`gh auth status` lo muestra; `gh auth refresh -s project` lo agrega). Estos comandos se ejecutaron el 5 de octubre de 2026 con GitHub CLI 2.100 para dejar el Project como está:

```powershell
gh project edit 6 --owner cherrera0001 --title "Brújula IA Regional — Backlog"
gh project field-create 6 --owner cherrera0001 --name "Peso" --data-type NUMBER
gh project field-create 6 --owner cherrera0001 --name "Tipo" --data-type SINGLE_SELECT --single-select-options "Historia,Tarea,Decisión,Investigación"
gh project field-create 6 --owner cherrera0001 --name "Modelo Claude" --data-type SINGLE_SELECT --single-select-options "Opus,Sonnet,Haiku"
gh project field-create 6 --owner cherrera0001 --name "Sprint" --data-type SINGLE_SELECT --single-select-options "Pendiente,Sprint 1,Sprint 2"
gh project field-create 6 --owner cherrera0001 --name "Horas estimadas" --data-type NUMBER
gh project field-create 6 --owner cherrera0001 --name "Esfuerzo real" --data-type NUMBER
gh label create "user story" --color 0E8A16 --description "Historia de usuario (plantilla User Story)"
gh label create "tarea" --color 1D76DB --description "Tarea vinculada a una historia (plantilla Tarea)"
gh label create "decisión" --color D93F0B --description "Decisión reservada al equipo; no es un requisito"
gh label create "investigación" --color FBCA04 --description "Investigación o verificación de fuentes"
gh label create "propuesta" --color BFD4F2 --description "Contenido propuesto, pendiente de validar por el equipo"
```

Para consultar el tablero y sus campos desde la terminal:

```powershell
gh project view 6 --owner cherrera0001
gh project field-list 6 --owner cherrera0001
gh project item-list 6 --owner cherrera0001 --limit 100
```

`gh project field-create` solo admite texto, selección única, fecha y número: un campo de tipo iteración y las opciones de `Status` se configuran desde la web.

---

## E. Cómo mantener el backlog con Claude Code

Comandos para PowerShell desde la raíz del repositorio. Los de `gh` se comprobaron en esta instalación (GitHub CLI 2.100) o en su ayuda (`gh <comando> --help`).

### 1. Iniciar Claude Code y pedir un agente

```powershell
claude
```

Dentro de la sesión, `/agents` lista los agentes del proyecto y `/model` muestra los modelos disponibles. Para el backlog, pide el agente en el mensaje: «Usa el agente `product-owner` para revisar la historia X y proponer sus tareas con peso». Para abrir toda la sesión como un agente:

```powershell
claude --agent product-owner
```

Claude Code lee [CLAUDE.md](CLAUDE.md), donde está el proceso completo (sección «Backlog en GitHub»). `product-owner` redacta en texto y no toca GitHub; crear o editar issues se le pide a la sesión principal de forma explícita.

### 2. Revisar el backlog de historias y tareas

- Índice con pesos, modelos y enlaces: [docs/BACKLOG.md](docs/BACKLOG.md).
- En GitHub: historias con la etiqueta `user story`, tareas con `tarea`, decisiones con `decisión`. Lo no aprobado por el equipo lleva `propuesta`.
- Desde la terminal:

```powershell
gh issue list --label "user story" --limit 50
gh issue list --label tarea --limit 100
gh issue list --label "decisión" --limit 20
gh issue view <numero>
```

Cada tarea aparece como sub-issue de su historia; en la web, la historia muestra el progreso de sus sub-issues.

### 3. Interpretar el puntaje 0–5

La escala está en la sección D. Resumen: 0 decisión sin construcción · 1 hasta 1 h · 2 unas 2–3 h · 3 media jornada · 4 una jornada o varias piezas · 5 más de una jornada o incertidumbre alta (se divide antes de empezar).

- **Peso** es esfuerzo relativo y sirve para comparar y ordenar. Lo lleva cada tarea y cada historia (peso global, con una frase que dice qué lo impulsa).
- **Horas estimadas** es tiempo, se registra aparte y solo cuando hay fundamento; hoy todas dicen «por estimar».
- **Esfuerzo real** se anota al cerrar. Se compara con la estimación para estimar mejor la próxima vez, no para evaluar a nadie.

Distribución actual: historias propuestas con peso global 3 a 5; tareas de 1 a 3 (ninguna de 5); decisiones en 0; las cuatro historias del README en «pendiente» hasta que el equipo cierre D1, D4 o D5.

**Modelo de Claude Code sugerido por tipo de trabajo.** Cada issue lo indica en su cuerpo y en el campo `Modelo Claude`; la tabla completa, con el motivo de cada caso, está en [CLAUDE.md](CLAUDE.md) («Análisis por issue»).

| Tipo de trabajo | Modelo | Issues |
|---|---|---|
| Decisiones de arquitectura y de alcance, historias ambiguas con impacto amplio, definición de criterios, revisión final de riesgos | Opus | #1, #2, #3, #7, #8, #11, #14, #15, #17, #36 |
| Análisis y reformulación de historias, descomposición, estimación, documentación, pipeline y SQL, fichas de fuentes, cálculo e informes | Sonnet | los 36 restantes |
| Verificación mecánica, inventarios y borradores de tablas, revisados después por Sonnet o por una persona | Haiku (si `/model` lo ofrece; si no, Sonnet) | #47; apoyo en #22 y #28 |

### 4. Consultar el Project y mover tarjetas

Tablero: https://github.com/users/cherrera0001/projects/6. Desde la terminal, `gh project item-list 6 --owner cherrera0001 --limit 100`.

Todo lo que entra queda en `Backlog`. Se mueve a `Ready` solo cuando el equipo compromete la tarjeta para un sprint (y entonces se completan `Sprint`, `Horas estimadas` y responsable); a `In progress` cuando alguien empieza a trabajarla en una rama. Desde la terminal, un campo por llamada (sintaxis tomada de `gh project item-edit --help`):

```powershell
gh project item-edit 6 --owner cherrera0001 --url https://github.com/cherrera0001/2026-G02-MAIN/issues/<numero> --field "Status" --value "Ready"
gh project item-edit 6 --owner cherrera0001 --url https://github.com/cherrera0001/2026-G02-MAIN/issues/<numero> --field "Horas estimadas" --number 3
```

### 5. Sumar una nueva historia sin duplicar

1. Escribirla con el formato de la plantilla: «Como [stakeholder], quiero [saber/analizar algo], para poder [decidir algo]».
2. Validar los criterios de aceptación con el equipo: cada uno con entrada y salida comprobables. Si aún no están validados, el issue dice «criterios pendientes de validar» y lleva la etiqueta `propuesta`.
3. Buscar duplicados antes de crear: `gh issue list --state all --search "<palabras clave>"` y revisar [docs/BACKLOG.md](docs/BACKLOG.md). Si existe una historia equivalente, se actualiza esa.
4. Pedir a Claude Code (o hacerlo a mano) la descomposición en tareas con peso 0–5 justificado, modelo sugerido, dependencias y evidencia de término; ninguna tarea con peso 5.
5. Crear la historia y sus tareas:

```powershell
gh issue create --label "user story" --title "[User Story] ..." --body-file historia.md
gh issue create --label tarea --parent <numero de la historia> --title "[Tarea] ..." --body-file tarea.md
gh project item-add 6 --owner cherrera0001 --url https://github.com/cherrera0001/2026-G02-MAIN/issues/<numero>
gh project item-edit 6 --owner cherrera0001 --url https://github.com/cherrera0001/2026-G02-MAIN/issues/<numero> --field "Status" --value "Backlog"
gh project item-edit 6 --owner cherrera0001 --url https://github.com/cherrera0001/2026-G02-MAIN/issues/<numero> --field "Tipo" --value "Historia"
gh project item-edit 6 --owner cherrera0001 --url https://github.com/cherrera0001/2026-G02-MAIN/issues/<numero> --field "Peso" --number 3
gh project item-edit 6 --owner cherrera0001 --url https://github.com/cherrera0001/2026-G02-MAIN/issues/<numero> --field "Modelo Claude" --value "Sonnet"
gh project item-edit 6 --owner cherrera0001 --url https://github.com/cherrera0001/2026-G02-MAIN/issues/<numero> --field "Sprint" --value "Pendiente"
```

6. Agregar la historia y sus tareas a [docs/BACKLOG.md](docs/BACKLOG.md).

### 6. Registrar una decisión pendiente sin convertirla en requisito

Crear un issue con la etiqueta `decisión` (`Tipo = Decisión`, peso 0) que diga: la pregunta, las opciones tal como están documentadas en el repositorio, qué historias o tareas bloquea y cómo se registrará la decisión. Las tareas que dependen de ella se parametrizan (el valor es un dato, no código) o se rotulan `propuesta`. Cuando el equipo decide: anota opción, fecha y motivo en el issue, lo cierra, actualiza la tabla «Decisiones que solo el equipo puede cerrar» de este README y `CLAUDE.md`, y recién entonces abre la tarea que lo lleva al código. Las ocho decisiones abiertas hoy (D1 a D8) están enlazadas en [docs/BACKLOG.md](docs/BACKLOG.md).

### 7. Proponer una fuente nueva

Sigue «Proponer una nueva fuente» de la sección B: ficha desde [docs/fuentes/PLANTILLA_FICHA.md](docs/fuentes/PLANTILLA_FICHA.md) con URL, organismo, licencia (y dónde figura), cobertura temporal y territorial, granularidad, datos personales y limitaciones; lo no comprobado se escribe «sin comprobar»; decisión de uso `pendiente`. Los archivos descargados van a `data/raw/<capa>/`, que está en `.gitignore`; no se agregan comprimidos nuevos al repositorio sin decisión del equipo. Cada ficha se registra como tarea de `Tipo = Investigación` bajo la historia que la necesita (hoy, las de P-HU02 y P-HU03).

### 8. Revisar los cambios y preparar commit y PR a mano

Claude Code no hace commit ni push en este repositorio. Antes de versionar:

```powershell
git status
git diff
git diff --stat
```

Luego los pasos de la sección C: crear rama `tipo/descripcion-corta`, agregar archivos por nombre (nunca `git add .`), revisar `git diff --staged`, commit con el porqué, `git push -u origin <rama>` y Pull Request con revisión de otra persona. Comprueba que no entren `.env`, `chat-wsp/`, `data/raw/`, `data/processed/` ni `.venv/`.

### 9. Qué cambió en esta tarea y qué se validó

Ver [Cambios de esta versión](#cambios-de-esta-versión). Los cambios se versionaron en la rama `docs/backlog-github` con un Pull Request hacia `main`, siguiendo la sección C; la fusión queda a cargo del equipo.

---

## Cambios de esta versión

Cambios versionados en la rama `docs/backlog-github`, pendientes de revisión y fusión por el equipo mediante Pull Request.

| Archivo | Cambio | Propósito |
|---|---|---|
| [CLAUDE.md](CLAUDE.md) | Nuevo | Contexto del producto, comandos, convenciones, privacidad, decisiones que se consultan, proceso del backlog, guía de modelos y definición de terminado |
| [.claude/agents/](.claude/agents/) | Nuevo (5 archivos) | Agentes `product-owner`, `analista-fuentes`, `ingeniero-datos`, `cientifico-datos` y `revisor-qa` |
| [docs/fuentes/PLANTILLA_FICHA.md](docs/fuentes/PLANTILLA_FICHA.md) | Nuevo | Ficha para proponer y evaluar fuentes |
| [docs/BACKLOG.md](docs/BACKLOG.md) | Nuevo | Índice del backlog publicado: historias, pesos, tareas, modelos y enlaces a los issues |
| [db/schema.sql](db/schema.sql) | Modificado | `core.programa.cod_carrera` admite nulos |
| `.gitignore` | Modificado | Ignora `.claude/settings.local.json` |
| `README.md` | Modificado | Secciones de estado, A, B, C, D, E y esta tabla; el contenido anterior se conserva |

**En GitHub (no son archivos del repositorio):** Project 6 renombrado y con campos nuevos; cinco etiquetas; issues de historias, tareas y decisiones en `Backlog`. El detalle, con números y enlaces, está en [docs/BACKLOG.md](docs/BACKLOG.md).

**Corrección del pipeline.** El pipeline fallaba con `NOT NULL constraint failed: programa.cod_carrera`: 5.471 filas de la fuente (352 programas) traen ese campo vacío. La columna no es llave ni la usa ninguna vista, así que ahora admite nulos, de acuerdo con la regla del proyecto de no imputar.

**No se crearon** un agente de interfaz ni skills: no hay aplicación en el repositorio y el único procedimiento repetible (la ficha de fuente) queda cubierto por la plantilla.

**Validaciones ejecutadas**

- Pipeline completo en el repositorio y en un clon limpio temporal: termina con «Base lista» y los 8 controles se cumplen.
- Comandos de consulta de controles y cargas de la sección B, ejecutados en PowerShell.
- `uvx ruff check .`: 1 aviso que ya existía (`DTZ005` en `construir_bd.py`, fecha sin zona horaria), sin corregir.
- Claude Code 2.1.290 reconoce los cinco agentes del proyecto; `claude --help` muestra los alias de modelo `fable`, `opus` y `sonnet`.
- Enlaces relativos de este README comprobados contra los archivos.
- Backlog en GitHub (5 de octubre de 2026): `gh auth status` con permiso `project`; Project 6 renombrado y con campos nuevos (`gh project field-list`); etiquetas creadas (`gh label list`); issues creados con `gh issue create`, vinculados con `--parent` y agregados al Project con `gh project item-add`; campos fijados por GraphQL (`gh api graphql`, mutación `updateProjectV2ItemFieldValue`); verificación final con `gh project item-list` de que todas las tarjetas están en `Backlog`.

**Sin validar o pendiente**

- No hay pruebas automatizadas ni integración continua.
- Los pasos de la interfaz web de GitHub (acceso del equipo, vistas, nombres de `Status`) no se recorrieron en esta tarea.
- `gh project item-edit` por nombre de campo se documenta según su ayuda; la carga masiva usó GraphQL.
- No se crearon milestones, ramas remotas ni asignaciones: los sprints y los roles no están confirmados en el repositorio.
- La disponibilidad de un modelo Haiku en esta instalación no se comprobó (`/model` en sesión); si no está, se usa Sonnet.
- Las licencias y las URL de las fuentes no se volvieron a comprobar.
