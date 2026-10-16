# Reporte de Auditoría Crítica y Diagnóstico de Evolución
## Plataforma Analítica: Brújula IA Regional

**Fecha de Evaluación**: Octubre 2026  
**Versión y Commit Auditado**: `b04cbb1` (`main`)  
**URL de Inspección en Producción**: https://brujula-ia-regional.streamlit.app/  
**Entorno de Auditoría**: Chrome DevTools MCP (Headless Chrome) en resolución Escritorio (1280x900) y Móvil (390x844).

---

## 1. Resumen Ejecutivo del Diagnóstico

La aplicación desplegada en producción cumple con el objetivo preliminar de conectar Streamlit con DuckDB y renderizar las 5 áreas requeridas sin fallos de ejecución. Sin embargo, desde la perspectiva de una **plataforma analítica gubernamental de soporte a decisiones de inversión pública**, presenta debilidades críticas en su experiencia de usuario, diseño de información, comunicación de incertidumbre y riqueza visual.

Actualmente, el sistema funciona como un "visor de tablas DuckDB con filtros básicos", en lugar de una herramienta de inteligencia territorial guiada por preguntas de política pública.

---

## 2. Inventario de Hallazgos Clasificados por Severidad (P0 a P3)

| ID | Categoría | Severidad | Pantalla / Componente | Hallazgo Crítico | Consecuencia para el Usuario | Solución Comprobable |
| :--- | :--- | :---: | :--- | :--- | :--- | :--- |
| **H-01** | **Arquitectura de Información** | **P0** | Global / Navegación | Pestañas genéricas desconectadas de las preguntas del analista de políticas públicas. | El usuario no tiene un flujo de trabajo lógico para pasar del panorama nacional al detalle territorial y a la especialización. | Reorganizar en 6 vistas analíticas orientadas a preguntas: Panorama Nacional, Explorador Territorial, Oferta Formativa, Especialización (LQ), Metodología y Priorización. |
| **H-02** | **Interacción y Filtros** | **P1** | Tab 2 (Explorador) | Los filtros estaban confinados a una pestaña interna y no gobernaban globalmente la aplicación. | Al cambiar a "Especialización" o "Mapa", se perdía el contexto analítico del territorio seleccionado. | Centralizar los filtros jerárquicos en una barra lateral (`st.sidebar`) permanente y persistente. |
| **H-03** | **Visualización Científica** | **P1** | Tab 2 y 4 | Uso de `st.bar_chart` rudimentario sin tooltips, sin ejes formateados y sin ordenamiento de magnitudes. | Imposibilidad de comparar regiones con precisión o inspeccionar valores de inmediato sin descargar datos. | Implementar visualizaciones interactivas con **Altair** (barras horizontales ordenadas, tooltips, etiquetas de porcentaje y formato chileno). |
| **H-04** | **Ciencia de Datos / LQ** | **P1** | Tab 4 (Especialización) | El cálculo de $LQ$ mostraba solo el resultado final sin descomponer el numerador ($T_{ra}/T_r$) ni el denominador ($T_a/T_{total}$). Valores extremos ($LQ > 50$) desconcertaban al usuario. | El analista no podía auditar si un $LQ$ alto se debía a ventaja comparativa real o a un artefacto de celda pequeña (ej. $n=9$ en Arica). | Desglosar la fórmula completa, mostrar numerador y denominador observados, y graficar un *lollipop/scatter plot* con línea $LQ=1.0$ diferenciando celdas pequeñas ($n < \tau$). |
| **H-05** | **Cartografía y Espacio** | **P1** | Tab 3 (Mapa) | `st.map` nativo presentaba puntos monótonos sin leyenda, sin diferenciar tipos de IES y sin tooltips interactivos al posar el cursor. | El mapa operaba como un adorno visual sin utilidad analítica para identificar la institución o comuna del punto. | Implementar mapa interactivo con **PyDeck** o capas enriquecidas, tooltips con nombre de la sede, tipo de institución y títulos comunales generados. |
| **H-06** | **Comunicación de Incertidumbre** | **P2** | Tab 1, 3, 4 | Las advertencias metodológicas eran textos estáticos (`st.caption` o `st.warning`) sin taxonomía epistemológica clara. | Ambigüedad entre lo que es un dato censal verificado, una estimación matemática y una limitación de cobertura. | Etiquetar formalmente cada sección con la taxonomía: `[OBSERVADO]`, `[DERIVADO]`, `[HIPÓTESIS]` y `[NO DISPONIBLE]`. |
| **H-07** | **Accesibilidad y WCAG 2.2** | **P2** | General / Tablas | Números mostrados en tablas sin formateo chileno (ej. `231261` en vez de `231.261`), generando fatiga cognitiva en números de 6 dígitos. | Dificultad de lectura rápida para usuarios con déficit visual o en pantallas de baja resolución. | Aplicar formateo chileno de miles con punto (`.`) a todas las columnas numéricas y KPI de la interfaz. |
| **H-08** | **Diseño Institucional / UI** | **P3** | Header y Layout | Aspecto por defecto de Streamlit sin identidad institucional sobria (parecía un prototipo académico informal). | Poca credibilidad visual para autoridades del Ministerio de Economía o evaluadores externos. | Incorporar cabecera institucional sobria (estilo Gobierno de Chile), paleta de colores institucional accesible y métricas contextualizadas. |

---

## 3. Auditoría Estadística y Científica de los Indicadores

### 3.1. Población Censal y Conservación de Títulos
- **Universo**: 328.998 personas tituladas en la educación superior chilena (SIES / Mineduc 2025).
- **Integridad**: Verificada al 100% en `core.titulacion` y `mart.oferta`.
- **Riesgo**: Ningún filtro o join multiplica títulos. Se conserva la invariante de suma idéntica (`sum(n_titulos) == 328.998`).

### 3.2. Descalce Espacio-Temporal y Sesgo de Modalidad
- **Descalce temporal**: Las coordenadas de las sedes provienen del catastro IDE Chile 2020, mientras que los títulos corresponden a 2025 (desfase de 5 años). En ese periodo pueden haber abierto o cerrado sedes.
- **Sedes sin correspondencia**: 49 sedes reportadas por Mineduc no figuran en el catastro físico 2020 de la IDE.
- **Modalidad no presencial**: El 25.08% de los títulos (82.525) se impartieron en modalidad no presencial. De ellos, el 82.4% están asignados a la sede administrativa en la Región Metropolitana. **Prohibición estricta**: No se puede inferir el lugar de residencia del titulado a partir de la sede administrativa.

### 3.3. Estabilidad del Cociente de Especialización ($LQ$)
- **Definición Operacional**:
  $$LQ_{ra} = \frac{T_{ra} / T_r}{T_a / T_{total}}$$
- **Hallazgo estadístico**: En celdas con $T_a$ bajo a nivel nacional (ej. áreas de nicho con menos de 20 graduados en el país), el denominador se vuelve diminuto, catapultando el $LQ$ a valores de 80.0 o 98.0 con apenas 7 a 9 graduados en la región.
- **Control requerido**: Regla de supresión o alerta para celdas con $T_{ra} < \tau$ (donde $\tau$ es el umbral de estabilidad ajustable por el analista, típicamente $\tau \in [5, 20]$).

---

## 4. Estrategia de Rediseño y Mejoras

1. **Servicios de Dominio Enriquecidos**: Agregar funciones analíticas en `src/servicios/consultas_oferta.py` que retornen desagregaciones por tipo de institución, niveles, participación nacional y componentes desglosados de $LQ$.
2. **Sistema Visual en Streamlit**:
   - Barra lateral permanente con filtros jerárquicos integrados y botón de reinicio.
   - Pestañas analíticas orientadas a decisiones:
     - `🌐 1. Panorama Nacional`
     - `🗺️ 2. Explorador Territorial`
     - `🎓 3. Oferta y Niveles Formativos`
     - `📐 4. Especialización (LQ)`
     - `🛡️ 5. Metodología y Trazabilidad`
     - `⚖️ 6. Priorización Multicriterio (Transparencia)`
   - Visualizaciones interactivas en Altair con tooltips completos y paleta institucional.
   - Botones de exportación a CSV en todas las tablas clave.
3. **Validación y Pruebas**:
   - Ampliar la suite de pytest para validar los nuevos servicios y componentes visuales.
   - Capturar evidencias visuales posteriores para la matriz de evaluación antes/después.
