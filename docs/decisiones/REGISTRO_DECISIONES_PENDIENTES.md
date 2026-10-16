# Registro de Decisiones de Producto y Arquitectura Pendientes (ADR Log)

**Proyecto**: Brújula IA Regional (2026-G02-MAIN)  
**Fecha de Revisión**: 2026-10-16  
**Regla de Gobierno**: Ninguna de estas decisiones puede ser cerrada unilateralmente por un agente de IA ni por código sin la ratificación explícita del Product Owner y la contraparte del Ministerio de Economía.

---

## Índice de Decisiones (D1 a D8)

| ID | Issue GitHub | Decisión de Dominio | Opciones en Disputa | Impacto en el Sistema | Estado Actual |
|---|---|---|---|---|---|
| **D1** | [#11](https://github.com/cherrera0001/2026-G02-MAIN/issues/11) | **Unidad de análisis del ranking** | A) Región × Área Genérica × IES (README)<br/>B) Carrera × Sector en Región Piloto (Mathias) | Define la clave primaria del ranking y si se financia a una institución o a un tema sectorial. | **Abierta / Bloqueante** |
| **D2** | [#12](https://github.com/cherrera0001/2026-G02-MAIN/issues/12) | **Alcance territorial del MVP** | A) 16 Regiones del país (nacional)<br/>B) Una región piloto | Si se elige una región piloto, el ranking no puede incluir la dimensión región como factor de ordenamiento. | **Abierta** |
| **D3** | [#13](https://github.com/cherrera0001/2026-G02-MAIN/issues/13) | **Niveles formativos elegibles para tesis** | A) Solo Licenciatura, Magíster, Doctorado (35.27%)<br/>B) Incorporar Técnicos Superior y Prof. sin Licenciatura (44.85%) | Si se restringe a opción A, se excluye al 44.85% de los graduados del país (147.571 personas). | **Abierta / Bloqueante** |
| **D4** | [#14](https://github.com/cherrera0001/2026-G02-MAIN/issues/14) | **Fuentes de demanda, vocación e IA** | A) Esperar validación e ingesta externa (INE, SII, SENCE, OIT)<br/>B) Publicar ranking v0 solo de oferta formativa declarándolo como tal | Determina si el ranking evalúa demanda laboral o si se limita a visibilizar oferta y especialización. | **Abierta / Bloqueante** |
| **D5** | [#15](https://github.com/cherrera0001/2026-G02-MAIN/issues/15) | **Usuario principal del MVP** | A) Exclusivamente Ministerio de Economía (Analista y Responsable)<br/>B) También empresas locales, docentes y estudiantes | Excluye formalmente las historias R3/F-H09 y beneficios no analíticos del MVP. | **Consolidada en propuesta** (Ministerio) |
| **D6** | [#16](https://github.com/cherrera0001/2026-G02-MAIN/issues/16) | **Umbral de supresión de celdas pequeñas** | A) Umbral de secreto estadístico $\tau = 5$<br/>B) Umbral de estabilidad $\tau = 10$<br/>C) Sin supresión (reportar todo) | Evita estimaciones distorsionadas del Cociente de Especialización en celdas con $n \le 9$. | **Abierta** |
| **D7** | [#17](https://github.com/cherrera0001/2026-G02-MAIN/issues/17) | **Tecnología de la interfaz pública** | A) Streamlit (recomendada por simplicidad y plazos)<br/>B) FastAPI + frontend React | Define la arquitectura de despliegue y minimiza dependencias operativas para la entrega del MVP. | **Evaluada / En propuesta** (Streamlit) |
| **D8** | [#18](https://github.com/cherrera0001/2026-G02-MAIN/issues/18) | **Gestión de comprimidos de datos en Git** | A) Mantener archivos originales en Git (`data/oferta/*.rar`, `data/geo/*.zip`)<br/>B) Mover a Git LFS o almacenamiento blob externo con script de descarga | Los archivos pesan < 10 MB comprimidos, pero extraídos superan 189 MB (rechazados por GitHub). | **Abierta** |

---

## Detalle y Consecuencias de Cada Decisión

### D1: Unidad de Análisis del Ranking (#11)
- **Problema**: El `README.md` declara un ranking de *región × carrera × institución*. Sin embargo, la propuesta metodológica de Mathias (M-HU04) planteó *carrera × sector en una región piloto*.
- **Consecuencias**:
  - Si la unidad es por **Institución**, el subsidio se focaliza en convenios con universidades o centros de formación técnica concretos.
  - Si la unidad es por **Sector**, el ranking orienta las bases temáticas de los desafíos industriales, pero no indica a qué campus asignar recursos.
- **Opción recomendada por el equipo técnico**: Adoptar como unidad primaria del ranking **región × área genérica × institución** (README), incorporando el sector productivo como un atributo ponderador regional en la fórmula del puntaje.

### D3: Niveles Formativos Elegibles (#13)
- **Problema**: El diccionario actual `ELEGIBLE_TESIS` en `construir_bd.py` contiene:
  ```python
  ELEGIBLE_TESIS = {
      "Profesional Con Licenciatura": "si",
      "Magister": "si",
      "Doctorado": "si",
      "Diplomado (desde un semestre)": "no",
      "Postítulo": "no",
  }
  ```
  Dejando fuera de la regla (en estado `'pendiente'`) a 87.067 Técnicos de Nivel Superior y 55.015 Profesionales sin Licenciatura (44.85% de la masa nacional de egresados).
- **Consecuencias**: La política pública del Ministerio debe decidir si el cofinanciamiento admite memorias y proyectos de título técnicos aplicados a la empresa o si se restringe exclusivamente a licenciaturas y posgrados académicos.

### D4: Fuentes de Demanda y Plan Alternativo (#14)
- **Problema**: El repositorio no contiene fuentes de demanda laboral, PIB regional ni complementariedad con IA.
- **Consecuencias**:
  - Si las fuentes no se consiguen a tiempo para la entrega del Sprint 1, el equipo debe aprobar formalmente un **Plan de Contingencia**: publicar un **Índice Territorial de Oferta y Especialización Formativa** declarado explícitamente como tal, sin simular un ranking con factores inexistentes.

### D6: Umbral de Supresión de Celdas Pequeñas (#16)
- **Problema**: La auditoría empírica detectó que el Cociente de Especialización ($LQ$) alcanza valores anómalos de 98.15 en áreas con 9 graduados o 80.33 con 7 graduados.
- **Consecuencias**: Para proteger la robustez del modelo y la privacidad estadística, se recomienda fijar $\tau = 5$. Celdas con menos de 5 titulados en la región no entran al ranking o se agrupan en una categoría residual "Otros".

### D7: Tecnología de la Interfaz (#17)
- **Problema**: Elegir la tecnología para el MVP de visualización territorial y reportes.
- **Consecuencias**: Streamlit permite construir la aplicación en menos de 2 días de trabajo en Python puro conectado a DuckDB. FastAPI + React requeriría más de 2 semanas de desarrollo adicional y configuraciones complejas de despliegue. Se ratifica la recomendación de Streamlit para el MVP.
