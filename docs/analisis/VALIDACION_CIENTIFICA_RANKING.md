# Validación Científica y Metodológica del Modelo de Priorización (Ranking)

**Estado**: **BLOCKED (BLOQUEADO CIENTÍFICAMENTE)**  
**Área**: Ciencia de Datos Aplicada a Políticas Públicas / Economía Laboral  
**Fecha de Dictamen**: 2026-10-16  
**Veredicto**: **No es metodológicamente defendible ni éticamente admisible calcular un ranking oficial de focalización en el estado actual de los datos.** El repositorio cuenta con evidencia sólida de oferta formativa e infraestructura, pero **carece en un 100% de datos empíricos de demanda laboral regional, vocación productiva sectorial y complementariedad tecnológica con Inteligencia Artificial.**

---

## 1. Fundamentación del Veredicto de Bloqueo (BLOCKED)

Un sistema de priorización para asignación de recursos públicos debe satisfacer estándares mínimos de validez de constructo, reproducibilidad y justicia distributiva. En el estado actual del repositorio:

1. **Ausencia Total de Factores de Demanda y Tecnología**:
   - `core.indicador_region_sector`: 0 filas (demanda laboral, empleo, PIB regional, vacíos de competencias).
   - `core.indicador_area`: 0 filas (índices de exposición o complementariedad ocupacional con IA).
   - `core.vinculo_area_sector`: 0 filas (matriz puente entre disciplinas académicas y sectores productivos).
2. **Riesgo de Asignación Espuria**:
   - Si se computara un ranking hoy, el cálculo solo podría operar sobre el volumen de titulados y el cociente de especialización (oferta pura). Calcular un "ranking con IA" asignando pesos ficticios a tablas vacías constituiría una mala práctica científica severa y vulneraría el Principio I de la Constitución SDD ("Evidencia verificable antes de conclusiones").
3. **Decisiones Críticas de Dominio No Resueltas**:
   - Decisión D1 (#11): Conflicto de la unidad de análisis (¿Se prioriza a una institución o a un sector temático?).
   - Decisión D3 (#13): El 44.85% de los graduados (147.571 personas) está en niveles formativos con elegibilidad 'pendiente'.
   - Decisión D6 (#16): Inestabilidad extrema del Cociente de Especialización en celdas pequeñas (LQ > 90 con solo 9 titulados).

---

## 2. Marco Conceptual y Formalización del Modelo

### 2.1 Distinción Estricta de Dimensiones del Problema

Para evitar ambigüedades, se separan conceptualmente los 6 elementos del dominio:

| Dimensión | Naturaleza | Fuente Primaria | Grano | Estado en BD |
|---|---|---|---|---|
| **1. Oferta Educativa** | Observada (Censal) | SIES / Mineduc | Región × Institución × Programa | **Disponible (100%)** |
| **2. Demanda Laboral** | Observada / Muestral | SENCE (ENADEL) / INE (ENE) | Región × Sector × Ocupación | **Bloqueada (0%)** |
| **3. Vocación Productiva** | Observada (Económica) | Banco Central / SII / ERD | Región × Rama de Actividad | **Bloqueada (0%)** |
| **4. Exposición / IA** | Inferida / Modelo | OIT / FMI / Felten et al. | Ocupación (ISCO) / Disciplina | **Bloqueada (0%)** |
| **5. Elegibilidad Formativa** | Regla de Política | Ministerio de Economía | Nivel de Carrera / Modalidad | **Parcial (Decisión D3)** |
| **6. Impacto de Tesis** | Criterio Cualitativo | Convocatoria / Evaluación Pares | Proyecto Individual | **Fuera de la BD** |

> [!IMPORTANT]
> **El modelo analítico no mide ni predice el impacto de una tesis individual.** La plataforma mide la **propensión territorial y disciplinaria** a generar proyectos pertinentes; la calidad intrínseca y viabilidad técnica de una tesis específica es resorte exclusivo de la comisión evaluadora de la convocatoria.

---

### 2.2 Definición Formal de la Unidad de Análisis y Población Objetivo

#### Unidad de Análisis ($u$)
Se propone formalmente adoptar la unidad del README (ratificando la opción ministerial de la Decisión D1):
$$u = (r, a, i)$$
Donde:
- $r \in \{1, \dots, 16\}$: Código oficial de la Región.
- $a \in \{1, \dots, 285\}$: Área Genérica de formación (SIES).
- $i \in \{1, \dots, 144\}$: Institución de Educación Superior (SIES).

*Justificación*: Permite al Ministerio orientar los convenios de cofinanciamiento directamente hacia convenios con IES con presencia comprobada en el territorio.

#### Población Objetivo Elegible ($\mathcal{P}$)
Conjunto de programas académicos $p \in \text{core.programa}$ que satisfacen:
$$\mathcal{P} = \{ p \mid \text{elegible\_tesis}(p) = \text{'si'} \land \text{modalidad}(p) \neq \text{'No Presencial'} \}$$

Si la Decisión D3 aprueba incorporar títulos técnicos, $\mathcal{P}$ se expande automáticamente mediante el parámetro del pipeline.

---

## 3. Formulación Matemática del Índice de Priorización ($S_u$)

Cuando las fuentes de datos estén integradas, el puntaje compuesto de la unidad $u = (r, a, i)$ se definirá como una función aditiva ponderada multidimensional:

$$S_u = \sum_{k=1}^{K} w_k \cdot \tilde{X}_{k}(u)$$

Sujeto a las restricciones:
$$\sum_{k=1}^{K} w_k = 1, \quad w_k \ge 0 \quad \forall k \in \{1, \dots, K\}$$
$$\tilde{X}_{k}(u) \in [0, 1] \quad \forall k, u$$

### 3.1 Criterios de la Función ($X_k$)

1. **Criterio 1: Especialización y Masa Crítica de Oferta ($X_{\text{oferta}}$)**
   - *Definición*: Combinación del volumen logarítmico de titulados elegibles ($T_{u}$) y el cociente de especialización corregido ($LQ_{ra}$):
     $$X_{\text{oferta}}(u) = \alpha \cdot \ln(1 + T_{u}) + (1-\alpha) \cdot \min(LQ_{ra}, LQ_{\max})$$
   - *Sentido*: Mayor es mejor. Se acota $LQ$ a un percentil superior (ej. $LQ_{\max} = 5.0$) para evitar el sesgo de celdas con $n < 10$.

2. **Criterio 2: Relevancia y Dinamismo Productivo Regional ($X_{\text{productivo}}$)**
   - *Definición*: Participación del sector en el PIB regional ponderada por el vínculo formativo:
     $$X_{\text{productivo}}(u) = \sum_{s \in \mathcal{S}} V(a, s) \cdot \left( \frac{\text{PIB}_{r, s}}{\text{PIB}_{r}} \right)$$
     Donde $V(a, s) \in [0, 1]$ es el puntaje de afinidad en `core.vinculo_area_sector`.
   - *Sentido*: Mayor es mejor.

3. **Criterio 3: Demanda y Absorción Laboral Insatisfecha ($X_{\text{demanda}}$)**
   - *Definición*: Tasa de vacantes difíciles de cubrir o crecimiento del empleo formal en el sector en la región $r$:
     $$X_{\text{demanda}}(u) = \sum_{s \in \mathcal{S}} V(a, s) \cdot \text{DificultadContratacion}_{r, s}$$
   - *Sentido*: Mayor es mejor.

4. **Criterio 4: Complementariedad y Exposición a Inteligencia Artificial ($X_{\text{IA}}$)**
   - *Definición*: Índice de complementariedad tecnológica de las ocupaciones asociadas al área formativa:
     $$X_{\text{IA}}(u) = I_{\text{IA}}(a)$$
     Tomado de `core.indicador_area`.
   - *Sentido*: Mayor es mejor (premia áreas donde la IA complementa y amplifica la productividad humana frente a áreas de mera sustitución rutinaria).

---

### 3.2 Reglas de Normalización

Para garantizar comparabilidad entre variables de distinta escala y unidades (monetarias, recuentos, porcentajes):

1. **Normalización Min-Max Acotada (Trimming a Percentiles $P_1$ y $P_{99}$)**:
   $$\tilde{X}_k(u) = \frac{X_k(u) - P_1(X_k)}{P_{99}(X_k) - P_1(X_k)}$$
   Truncando valores fuera de $[0, 1]$. Esto evita que un valor extremo destruya la varianza del resto del país.
2. **Sentido Inverso**:
   Si un criterio $j$ es de costo o desfavorabilidad (`sentido = 'menor_es_mejor'`, ej. tasa de desempleo local):
   $$\tilde{X}_j(u) = 1 - \tilde{X}_j(u)$$

---

### 3.3 Tratamiento Científico de Datos Faltantes (Missing Data)

**Regla de Oro Constitucional (Principio I y III)**: La falta de información **no es evidencia de baja prioridad ni penalización con 0**.

Si para una unidad $u$ el criterio $k$ es no observable ($X_k(u) = \text{NULL}$):
1. **Renormalización de Pesos Activos**:
   Se recalcula el puntaje utilizando únicamente los criterios con evidencia empírica disponible:
   $$S_u = \frac{\sum_{k \in \mathcal{K}_{\text{obs}}(u)} w_k \cdot \tilde{X}_k(u)}{\sum_{k \in \mathcal{K}_{\text{obs}}(u)} w_k}$$
2. **Índice de Confiabilidad de Evidencia ($C_u$)**:
   Se computa y reporta obligatoriamente la proporción de masa de pesos observada:
   $$C_u = \sum_{k \in \mathcal{K}_{\text{obs}}(u)} w_k$$
   Si $C_u < 0.60$ (más del 40% del modelo no tiene datos), la unidad queda catalogada como **"Evidencia Insuficiente"** y se excluye del ranking de adjudicación directa, mostrándose en una lista separada de diagnóstico de vacíos de información pública.

---

## 4. Análisis de Sensibilidad, Incertidumbre y Robustez

El ranking no reportará una única ordenación rígida. Para auditar la estabilidad:

### 4.1 Escenarios de Ponderación Predefinidos

| Criterio ($k$) | Escenario Base ($E_0$) | Escenario Pro-Territorio ($E_1$) | Escenario Pro-IA ($E_2$) |
|---|---|---|---|
| $w_{\text{oferta}}$ | 0.25 | 0.35 | 0.15 |
| $w_{\text{productivo}}$ | 0.25 | 0.35 | 0.15 |
| $w_{\text{demanda}}$ | 0.25 | 0.20 | 0.20 |
| $w_{\text{IA}}$ | 0.25 | 0.10 | 0.50 |
| **Suma** | **1.00** | **1.00** | **1.00** |

### 4.2 Métricas de Estabilidad y Clasificación

Para cada unidad $u$:
- Sea $R_s(u)$ la posición en el ranking bajo el escenario $s \in \{E_0, E_1, E_2\}$.
- **Correlación de Rangos Global**: Se evalúa la matriz de correlación de Spearman $\rho(E_i, E_j)$.
- **Clasificación de Robustez**:
  - **Recomendación Robusta**: Si la unidad se mantiene dentro del cuartil superior ($Q_4$) en los tres escenarios:
    $$\max_{s} R_s(u) \le N \times 0.25$$
  - **Recomendación Sensible**: Si la oscilación en posición supera el 20% del total de filas evaluadas ($|R_{E_1}(u) - R_{E_2}(u)| > 0.20 \times N$). Toda recomendación sensible exige una advertencia explícita en el reporte ministerial.

---

## 5. Hoja de Ruta para Desbloquear el Ranking

Para transicionar el estado de **BLOCKED** a **READY**:

1. **Paso 1**: El Product Owner y la contraparte ministerial deben cerrar formalmente la **Decisión D1** (Unidad del ranking) y la **Decisión D3** (Niveles formativos elegibles).
2. **Paso 2**: Completar las fichas de fuente externa (#23 a #28) y formalizar la ingesta de al menos una fuente oficial de vocación económica territorial (SII o Banco Central).
3. **Paso 3**: Adoptar un índice validado internacionalmente de exposición/complementariedad ocupacional a la IA (OIT/FMI) y diseñar la tabla puente ISCO-CINE (#29, #35).
4. **Paso 4**: Extender físicamente el esquema DuckDB con las tablas `core.ejecucion_ranking`, `core.resultado_ranking` y `core.aporte_criterio`.
5. **Paso 5**: Implementar el script de reconstrucción (#39) y ejecutar las pruebas de estabilidad antes de presentar cualquier reporte oficial.
