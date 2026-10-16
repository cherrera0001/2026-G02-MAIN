"""Brújula IA Regional — Plataforma de Inteligencia Territorial.

Herramienta analítica de soporte a la decisión de política pública para la
priorización territorial del cofinanciamiento de memorias y tesis aplicadas con IA.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ruta canónica única, válida al ejecutar app.py o esta entrada directamente.
RAIZ_REPOSITORIO = Path(__file__).resolve().parents[2]
if str(RAIZ_REPOSITORIO) not in sys.path:
    sys.path.insert(0, str(RAIZ_REPOSITORIO))

import altair as alt
import pandas as pd
import streamlit as st

from src.servicios.carga import cargar_consultas

consultas = cargar_consultas()

# -----------------------------------------------------------------------------
# Configuración general de la página
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Brújula IA Regional — Inteligencia Territorial",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -----------------------------------------------------------------------------
# Caché de consultas analíticas (TTL = 1 hora)
# -----------------------------------------------------------------------------
@st.cache_data(ttl=3600)
def cargar_resumen():
    return consultas.obtener_resumen_general()


@st.cache_data(ttl=3600)
def cargar_filtros():
    return consultas.obtener_opciones_filtros()


@st.cache_data(ttl=3600)
def cargar_trazabilidad():
    return consultas.obtener_trazabilidad_fuentes()


@st.cache_data(ttl=3600)
def cargar_controles():
    return consultas.obtener_controles_calidad()


@st.cache_data(ttl=3600)
def cargar_distribucion_regional():
    return consultas.obtener_distribucion_regional()


@st.cache_data(ttl=3600)
def cargar_distribucion_niveles():
    return consultas.obtener_distribucion_niveles()


@st.cache_data(ttl=3600)
def cargar_distribucion_tipos_inst():
    return consultas.obtener_distribucion_tipos_inst()


@st.cache_data(ttl=3600)
def cargar_estado_priorizacion():
    return consultas.obtener_estado_priorizacion()


# -----------------------------------------------------------------------------
# Funciones auxiliares de formato chileno y exportación
# -----------------------------------------------------------------------------
def fmt_miles(val: float | None) -> str:
    """Formatea números enteros con separador de miles '.' de uso oficial en Chile."""
    if val is None or pd.isna(val):
        return "0"
    return f"{round(val):,}".replace(",", ".")


def fmt_pct(val: float | None) -> str:
    """Formatea valores porcentuales con dos decimales."""
    if val is None or pd.isna(val):
        return "0,00%"
    return f"{val:.2f}%".replace(".", ",")


# -----------------------------------------------------------------------------
# Aplicación Principal
# -----------------------------------------------------------------------------
def main():
    # -------------------------------------------------------------------------
    # 1. Cabecera Institucional y Metadatos de Gobernanza
    # -------------------------------------------------------------------------
    st.title("🧭 Brújula IA Regional — Explorador Territorial")
    st.markdown(
        "**Herramienta de soporte a la decisión para la priorización territorial "
        "del cofinanciamiento de memorias y tesis aplicadas con IA.**"
    )

    # Banner de Rigor Metodológico y Gobernanza Activa
    st.info(
        "ℹ️ **Estado Metodológico**: Este incremento visualiza exclusivamente la **oferta formativa censal (Mineduc 2025)** "
        "y la **infraestructura de sedes (IDE Chile 2020)**. El ranking multicriterio y los factores de demanda económica e IA "
        "permanecen **formalmente BLOQUEADOS** hasta contar con fuentes externas validadas. "
        "No se infiere causalidad ni empleabilidad a partir de los datos mostrados."
    )

    # -------------------------------------------------------------------------
    # 2. Barra Lateral: Controles y Filtros Jerárquicos de Alcance
    # -------------------------------------------------------------------------
    filtros = cargar_filtros()

    st.sidebar.header("🎯 Alcance y Filtros de Análisis")
    st.sidebar.caption("Los filtros aplicados gobiernan las vistas territoriales y de oferta.")

    # Selector de Región
    lista_regiones = ["Todas"] + [r["nombre"] for r in filtros["regiones"]]
    sel_region = st.sidebar.selectbox("Región", lista_regiones, index=0)
    cod_reg = next((r["codigo"] for r in filtros["regiones"] if r["nombre"] == sel_region), None)

    # Selector de Comuna (cascada dependiente de la región)
    if cod_reg is not None:
        comunas_disp = [c for c in filtros["comunas"] if c["cod_region"] == cod_reg]
    else:
        comunas_disp = filtros["comunas"]
    lista_comunas = ["Todas"] + [c["nombre"] for c in comunas_disp]
    sel_comuna = st.sidebar.selectbox("Comuna", lista_comunas, index=0)
    id_comuna = next((c["codigo"] for c in comunas_disp if c["nombre"] == sel_comuna), None)

    # Selector de Institución
    lista_inst = ["Todas"] + [i["nombre"] for i in filtros["instituciones"]]
    sel_inst = st.sidebar.selectbox("Institución", lista_inst, index=0)
    cod_i = next((i["codigo"] for i in filtros["instituciones"] if i["nombre"] == sel_inst), None)

    # Selector de Área Genérica
    lista_areas = ["Todas"] + [a["nombre"] for a in filtros["areas"]]
    sel_area = st.sidebar.selectbox("Área Genérica de Formación", lista_areas, index=0)
    id_a = next((a["codigo"] for a in filtros["areas"] if a["nombre"] == sel_area), None)

    # Selector de Modalidad con advertencia
    sel_mod = st.sidebar.selectbox("Modalidad", ["Todas"] + filtros["modalidades"], index=0)
    if sel_mod == "No Presencial":
        st.sidebar.warning("⚠️ La modalidad No Presencial radica sus títulos en la sede administrativa central.")

    # Selector de Elegibilidad
    sel_eleg = st.sidebar.selectbox("Elegibilidad de Tesis", ["Todos", "si", "no", "pendiente"], index=0)
    if sel_eleg == "pendiente":
        st.sidebar.caption("⚠️ Categoría bajo revisión ministerial (Decisión D3).")

    st.sidebar.divider()
    st.sidebar.markdown(
        "**Fuentes Oficiales Integradas**:\n"
        "- 🎓 Titulados 2025: SIES / Mineduc\n"
        "- 🏛️ Sedes e Inmuebles 2020: IDE Chile\n"
        "- 🔒 Privacidad: Cero datos personales"
    )

    # -------------------------------------------------------------------------
    # 3. Navegación por Vistas Analíticas Orientadas a Decisiones
    # -------------------------------------------------------------------------
    tab_panorama, tab_explorador, tab_oferta, tab_lq, tab_trazabilidad, tab_priorizacion = st.tabs([
        "📊 Vista General",
        "🔍 Explorador Territorial",
        "🎓 Oferta Formativa",
        "📈 Especialización (LQ)",
        "🛡️ Trazabilidad y Calidad",
        "⚖️ Priorización (Bloqueada)",
    ])

    # -------------------------------------------------------------------------
    # VISTA 1: PANORAMA NACIONAL
    # -------------------------------------------------------------------------
    with tab_panorama:
        st.subheader("Métricas Macro del Sistema (Periodo Censal 2025)")
        st.markdown(
            "**`[OBSERVADO]`** Distribución global de la masa crítica de personas tituladas en la educación superior chilena, "
            "cobertura de instituciones, programas académicos e infraestructura catastrada."
        )

        resumen = cargar_resumen()

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total Titulaciones", fmt_miles(resumen["total_titulaciones"]))
        col2.metric("Instituciones (IES)", fmt_miles(resumen["total_instituciones"]))
        col3.metric("Regiones Cubiertas", fmt_miles(resumen["total_regiones"]))
        col4.metric("Programas Académicos", fmt_miles(resumen["total_programas"]))
        col5.metric("Inmuebles Catastrados", fmt_miles(resumen["total_inmuebles"]))

        st.divider()

        # Gráfico Altair 1: Distribución Regional Nacional
        col_g1, col_g2 = st.columns([3, 2])

        with col_g1:
            st.markdown("#### Distribución de Titulados por Región")
            df_reg = cargar_distribucion_regional()

            chart_reg = (
                alt.Chart(df_reg)
                .mark_bar()
                .encode(
                    x=alt.X("n_titulos:Q", title="Total de Personas Tituladas"),
                    y=alt.Y("region:N", sort="-x", title="Región"),
                    color=alt.Color("pct_nacional:Q", scale=alt.Scale(scheme="blues"), legend=None),
                    tooltip=[
                        alt.Tooltip("region:N", title="Región"),
                        alt.Tooltip("n_titulos:Q", title="Titulados", format=","),
                        alt.Tooltip("pct_nacional:Q", title="% Nacional", format=".2f"),
                        alt.Tooltip("n_instituciones:Q", title="IES con Oferta"),
                        alt.Tooltip("n_inmuebles:Q", title="Inmuebles Físicos"),
                    ],
                )
                .properties(height=420)
            )
            st.altair_chart(chart_reg, use_container_width=True)

        with col_g2:
            st.markdown("#### Composición por Tipo de Institución")
            df_tipos = cargar_distribucion_tipos_inst()
            chart_tipos = (
                alt.Chart(df_tipos)
                .mark_arc(innerRadius=60)
                .encode(
                    theta=alt.Theta("titulos:Q"),
                    color=alt.Color(
                        "tipo_inst_1:N",
                        scale=alt.Scale(scheme="tableau10"),
                        legend=alt.Legend(title="Tipo de IES", orient="bottom"),
                    ),
                    tooltip=[
                        alt.Tooltip("tipo_inst_1:N", title="Tipo"),
                        alt.Tooltip("titulos:Q", title="Titulados", format=","),
                        alt.Tooltip("pct_nacional:Q", title="Participación (%)", format=".2f"),
                        alt.Tooltip("n_instituciones:Q", title="Cantidad IES"),
                    ],
                )
                .properties(height=320)
            )
            st.altair_chart(chart_tipos, use_container_width=True)

            st.caption(
                "**`[OBSERVADO]`** Las Universidades concentran el 59,1% de los títulos, "
                "mientras que los IP y CFT representan conjuntamente el 40,9% restante."
            )

        st.divider()

        # Tablas agregadas de modalidades y elegibilidad
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.markdown("#### Distribución por Modalidad de Impartición")
            df_mod = resumen["distribucion_modalidad"].copy()
            df_mod["titulos_fmt"] = df_mod["titulos"].apply(fmt_miles)
            df_mod["pct_fmt"] = df_mod["pct"].apply(fmt_pct)
            st.dataframe(
                df_mod[["modalidad", "titulos_fmt", "pct_fmt"]].rename(
                    columns={"modalidad": "Modalidad", "titulos_fmt": "Titulados", "pct_fmt": "% del Total"}
                ),
                width="stretch",
                hide_index=True,
            )
            st.caption(
                "⚠️ **Nota metodológica `[OBSERVADO]`**: El 25.08% de los títulos corresponden a modalidad 'No Presencial'. "
                "El 82.4% de estos títulos están radicados administrativamente en la Región Metropolitana, "
                "lo que no refleja el lugar de residencia del estudiante."
            )

        with col_m2:
            st.markdown("#### Clasificación según Elegibilidad de Tesis")
            df_eleg = resumen["distribucion_elegibilidad"].copy()
            df_eleg["titulos_fmt"] = df_eleg["titulos"].apply(fmt_miles)
            df_eleg["pct_fmt"] = df_eleg["pct"].apply(fmt_pct)
            st.dataframe(
                df_eleg[["elegible_tesis", "titulos_fmt", "pct_fmt"]].rename(
                    columns={"elegible_tesis": "Elegibilidad", "titulos_fmt": "Titulados", "pct_fmt": "% del Total"}
                ),
                width="stretch",
                hide_index=True,
            )
            st.caption(
                "⚠️ **Decisión D3 Pendiente `[NO DISPONIBLE]`**: El 44.85% de los títulos (Técnicos de Nivel Superior "
                "y Profesionales sin Licenciatura) se encuentran en estado 'pendiente' a la espera de definición por el Ministerio."
            )

    # -------------------------------------------------------------------------
    # VISTA 2: EXPLORADOR TERRITORIAL Y MAPA
    # -------------------------------------------------------------------------
    with tab_explorador:
        st.subheader("Explorador Territorial de Oferta e Infraestructura")
        st.markdown(
            "**`[OBSERVADO / DERIVADO]`** Análisis desagregado según los filtros de alcance activos en la barra lateral."
        )

        # Consulta con los filtros de la barra lateral
        df_filtrada = consultas.filtrar_oferta(
            cod_region=cod_reg,
            id_comuna=id_comuna,
            cod_inst=cod_i,
            id_area_generica=id_a,
            modalidad=sel_mod,
            elegible_tesis=sel_eleg,
        )

        # Métricas del territorio filtrado
        total_filtro = int(df_filtrada["n_titulos"].sum()) if not df_filtrada.empty else 0
        pct_filtro = (total_filtro * 100.0 / 328998) if total_filtro > 0 else 0.0

        c_f1, c_f2, c_f3 = st.columns(3)
        c_f1.metric("Títulos Filtrados", fmt_miles(total_filtro))
        c_f2.metric("Participación Nacional", fmt_pct(pct_filtro))
        c_f3.metric("Combinaciones Encontradas", fmt_miles(len(df_filtrada)))

        st.divider()

        # Mapa de Sedes
        st.markdown("#### 🗺️ Infraestructura Universitaria Georreferenciada")
        st.caption(
            "Localización de los 1.297 inmuebles catastrados por la IDE Chile (Capa 2020), "
            "vinculados al volumen de graduados de la institución en la comuna."
        )

        datos_geo = consultas.obtener_sedes_geo(cod_region=cod_reg, id_comuna=id_comuna, cod_inst=cod_i)
        df_geo = datos_geo["df_puntos"].copy()

        m1, m2, m3 = st.columns(3)
        m1.metric("Puntos Georreferenciados Mostrados", fmt_miles(len(df_geo)))
        m2.metric("Inmuebles sin oferta en 2025", fmt_miles(datos_geo["inmuebles_sin_oferta_periodo"]), help="Inmuebles físicos donde la IES no registró titulados en 2025 (ej. sedes administrativas o de investigación)")
        m3.metric("Sedes sin correspondencia geográfica", fmt_miles(datos_geo["sedes_sin_correspondencia_geo"]), help="49 sedes de Mineduc que no poseen punto en el catastro 2020 de la IDE")

        if not df_geo.empty:
            df_mapa = df_geo.rename(columns={"latitud": "latitude", "longitud": "longitude"})[["latitude", "longitude"]].copy()
            # Asignación de tamaño proporcional para legibilidad
            df_mapa["size"] = df_geo["titulos_comuna"].clip(lower=50, upper=3000)
            st.map(df_mapa, latitude="latitude", longitude="longitude", size="size", zoom=4)
        else:
            st.warning("No hay sedes con coordenadas válidas para la combinación actual de filtros.")

        st.warning(
            "⚠️ **Limitación Espacial Crítica `[HIPÓTESIS]`**: Desfase de 5 años entre el catastro físico (2020) y los títulos (2025). "
            "En carreras no presenciales, la ubicación de la sede no representa el lugar de residencia de los estudiantes."
        )

        st.divider()

        # Tabla detallada con descarga CSV
        st.markdown("#### Detalle de Registros de Oferta Filtrada")
        if not df_filtrada.empty:
            # Formateo numérico para vista amigable
            df_tabla = df_filtrada.copy()
            df_tabla["n_titulos"] = df_tabla["n_titulos"].apply(fmt_miles)

            _, col_csv = st.columns([4, 1])
            with col_csv:
                csv_bytes = df_filtrada.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Exportar CSV",
                    data=csv_bytes,
                    file_name="oferta_formativa_filtrada.csv",
                    mime="text/csv",
                    help="Descargar los registros actualmente filtrados en formato CSV",
                )

            st.dataframe(df_tabla, width="stretch", hide_index=True)
        else:
            st.warning("No se encontraron registros para los filtros seleccionados.")

    # -------------------------------------------------------------------------
    # VISTA 3: OFERTA FORMATIVA Y NIVELES
    # -------------------------------------------------------------------------
    with tab_oferta:
        st.subheader("Estructura de la Oferta Formativa por Nivel Académico")
        st.markdown(
            "**`[OBSERVADO]`** Desglose de titulaciones según grado académico y elegibilidad de proyectos de tesis."
        )

        df_niveles = cargar_distribucion_niveles()

        # Gráfico Altair de Niveles
        chart_niveles = (
            alt.Chart(df_niveles)
            .mark_bar()
            .encode(
                x=alt.X("n_titulos:Q", title="Total Titulados"),
                y=alt.Y("nivel:N", sort="-x", title="Nivel Académico"),
                color=alt.Color(
                    "elegible_tesis:N",
                    scale=alt.Scale(domain=["si", "no", "pendiente"], range=["#10B981", "#EF4444", "#F59E0B"]),
                    legend=alt.Legend(title="Elegibilidad Tesis"),
                ),
                tooltip=[
                    alt.Tooltip("nivel:N", title="Nivel"),
                    alt.Tooltip("n_titulos:Q", title="Titulados", format=","),
                    alt.Tooltip("pct_nacional:Q", title="% Nacional", format=".2f"),
                    alt.Tooltip("n_programas:Q", title="Programas"),
                    alt.Tooltip("elegible_tesis:N", title="Elegible"),
                ],
            )
            .properties(height=360)
        )
        st.altair_chart(chart_niveles, use_container_width=True)

        st.divider()

        # Top 10 áreas con mayor masa crítica en el territorio seleccionado
        st.markdown("#### Top 10 Áreas Genéricas de Formación con Mayor Masa Crítica")
        df_top_areas = consultas.obtener_top_areas(cod_region=cod_reg, limit=10)

        chart_top_areas = (
            alt.Chart(df_top_areas)
            .mark_bar()
            .encode(
                x=alt.X("n_titulos:Q", title="Titulados"),
                y=alt.Y("area_generica:N", sort="-x", title="Área de Conocimiento"),
                color=alt.value("#2563EB"),
                tooltip=[
                    alt.Tooltip("area_generica:N", title="Área"),
                    alt.Tooltip("n_titulos:Q", title="Titulados", format=","),
                    alt.Tooltip("pct:Q", title="Participación (%)", format=".2f"),
                ],
            )
            .properties(height=320)
        )
        st.altair_chart(chart_top_areas, use_container_width=True)

    # -------------------------------------------------------------------------
    # VISTA 4: ESPECIALIZACIÓN TERRITORIAL (LQ)
    # -------------------------------------------------------------------------
    with tab_lq:
        st.subheader("Cociente de Especialización Territorial (Location Quotient)")
        st.markdown(
            """
            **`[DERIVADO]`** El **Cociente de Especialización ($LQ$)** mide la intensidad relativa con que una región forma titulados 
            en un área disciplinaria específica, comparándola contra el promedio nacional:
            $$LQ_{ra} = \\frac{T_{ra} / T_r}{T_a / T_{total}} = \\frac{P_{ra}}{P_a}$$
            - **$LQ > 1,0$**: Mayor concentración de graduados en esa disciplina que el promedio nacional (ventaja comparativa observada).
            - **$LQ = 1,0$**: Concentración idéntica al promedio nacional.
            - **$LQ < 1,0$**: Menor concentración relativa.
            """
        )

        col_slider, col_stats = st.columns([2, 3])
        with col_slider:
            umbral_celda = st.slider(
                "Umbral de estabilidad para celdas pequeñas (mínimo de titulados observados)",
                min_value=1,
                max_value=20,
                value=5,
                help="Las celdas con recuentos inferiores a este umbral son marcadas como inestables debido a que denominadores pequeños inflan artificialmente el LQ.",
            )

        datos_lq = consultas.obtener_especializacion(
            cod_region=cod_reg,
            id_area_generica=id_a,
            umbral_celda_pequena=umbral_celda,
        )
        df_lq = datos_lq["df_especializacion"]

        with col_stats:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Celdas Analizadas", fmt_miles(datos_lq["total_celdas"]))
            c2.metric("Mediana LQ", f"{datos_lq['mediana_lq']:.2f}")
            c3.metric("LQ Máximo", f"{datos_lq['max_lq']:.2f}", help="Valores extremos suelen deberse a celdas pequeñas con denominadores muy bajos")
            c4.metric("Celdas Pequeñas", fmt_miles(datos_lq["celdas_pequenas_count"]), help="Celdas con n < umbral aplicado")

        st.caption(
            "⚠️ **Distinción Científica Obligatoria `[DERIVADO vs NO DISPONIBLE]`**: "
            "Un $LQ$ alto refleja especialización formativa histórica en oferta, "
            "**no una necesidad económica insatisfecha ni demanda de mercado**. La demanda laboral real requiere fuentes del INE/SENCE actualmente no integradas."
        )

        st.divider()

        # Gráfico Lollipop / Scatter de LQ con línea de referencia
        if not df_lq.empty:
            df_graf_lq = df_lq.head(30).copy()

            chart_puntos = (
                alt.Chart(df_graf_lq)
                .mark_circle(size=90)
                .encode(
                    x=alt.X("cociente_especializacion:Q", title="Cociente de Especialización (LQ)"),
                    y=alt.Y("area_generica:N", sort="-x", title="Área de Conocimiento"),
                    color=alt.Color(
                        "es_celda_pequena:N",
                        scale=alt.Scale(domain=[False, True], range=["#1E40AF", "#EF4444"]),
                        legend=alt.Legend(title="Estabilidad Muestral", labelExpr="datum.value ? 'Inestable (n < τ)' : 'Robusta'"),
                    ),
                    tooltip=[
                        alt.Tooltip("region:N", title="Región"),
                        alt.Tooltip("area_generica:N", title="Área"),
                        alt.Tooltip("cociente_especializacion:Q", title="Valor LQ", format=".2f"),
                        alt.Tooltip("t_ra:Q", title="Titulados en Región (Tra)", format=","),
                        alt.Tooltip("t_r:Q", title="Total Región (Tr)", format=","),
                        alt.Tooltip("t_a:Q", title="Total País Área (Ta)", format=","),
                        alt.Tooltip("pct_region:Q", title="% en Región", format=".2f"),
                        alt.Tooltip("pct_nacional:Q", title="% en País", format=".2f"),
                    ],
                )
            )

            # Línea de referencia en LQ = 1.0
            linea_ref = (
                alt.Chart(pd.DataFrame({"x": [1.0]}))
                .mark_rule(color="#9CA3AF", strokeDash=[4, 4], size=2)
                .encode(x="x:Q")
            )

            st.altair_chart((chart_puntos + linea_ref).properties(height=500), use_container_width=True)

            # Tabla completa con todas las variables subyacentes
            st.markdown("#### Descomposición Matemática Completa del Indicador")
            _, col_exp = st.columns([4, 1])
            with col_exp:
                csv_lq = df_lq.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Exportar LQ (CSV)",
                    data=csv_lq,
                    file_name="especializacion_lq_descompuesta.csv",
                    mime="text/csv",
                )

            st.dataframe(
                df_lq[
                    [
                        "region",
                        "area_generica",
                        "n_titulos",
                        "t_ra",
                        "t_r",
                        "t_a",
                        "pct_region",
                        "pct_nacional",
                        "cociente_especializacion",
                        "es_celda_pequena",
                    ]
                ],
                width="stretch",
                hide_index=True,
            )
        else:
            st.info("No hay datos de especialización para el filtro seleccionado.")

    # -------------------------------------------------------------------------
    # VISTA 5: METODOLOGÍA, CALIDAD Y TRAZABILIDAD
    # -------------------------------------------------------------------------
    with tab_trazabilidad:
        st.subheader("Linaje Criptográfico de Fuentes (Esquema `gob`)")
        st.markdown(
            "**`[OBSERVADO]`** Registro inalterable de los archivos crudos procesados con sus correspondientes "
            "hashes criptográficos SHA-256 para garantizar reproducibilidad exacta."
        )

        df_traz = cargar_trazabilidad()
        st.dataframe(df_traz, width="stretch", hide_index=True)

        st.divider()

        st.subheader("Auditoría de Calidad e Invariantes del Pipeline")
        st.markdown(
            "**`[OBSERVADO]`** Evaluación automática de los 8 controles de calidad ejecutados durante la construcción de la base DuckDB."
        )

        df_cal = cargar_controles()
        st.dataframe(df_cal, width="stretch", hide_index=True)

        st.success(
            "✅ **Invariante de Privacidad y Minimización de Datos**: "
            "El control `sin_datos_personales = 0` certifica que ninguna columna identificatoria "
            "(MRUN, RUT, fecha de nacimiento, edad, dirección particular) existe en tablas persistentes de la plataforma."
        )

    # -------------------------------------------------------------------------
    # VISTA 6: PRIORIZACIÓN MULTICRITERIO (TRANSPARENCIA ACTIVA)
    # -------------------------------------------------------------------------
    with tab_priorizacion:
        st.subheader("Estado de la Priorización Multicriterio")
        st.error(
            "⛔ **MÓDULO FORMALMENTE BLOQUEADO POR RIGOR METODOLÓGICO**\n\n"
            "La plataforma prohíbe calcular o publicar rankings de priorización territorial hasta que existan "
            "fuentes verificadas de demanda laboral externa e índices de complementariedad con IA con respaldo ministerial."
        )

        st.markdown(
            """
            ### ¿Por qué no se calcula un ranking en esta fase?
            1. **Riesgo de Inferencia Espuria**: Calcular un score priorizado utilizando únicamente la oferta formativa "castiga" a las regiones sin universidades complejas o premia a territorios con inflación de títulos administrativos.
            2. **Falta de Demanda Laboral**: Las tablas de demanda (`core.indicador_region_sector`) y vinculación semántica (`core.vinculo_area_sector`) permanecen vacías (0 filas) hasta validar encuestas del INE (ENE) o registros de empresas del SII.
            3. **Consenso Humano en Políticas Públicas**: La ponderación de criterios (Decisión D1) corresponde exclusivamente a autoridades y evaluadores ministeriales, no a un algoritmo automatizado.
            """
        )

        st.divider()

        # Hoja de Ruta de Desbloqueo Responsable
        st.markdown("#### Matriz de Criterios y Dependencias para Desbloqueo")

        df_criterios_roadmap = pd.DataFrame([
            {
                "Criterio": "C1: Masa Crítica de Oferta",
                "Dimensión": "Capacidad formativa instalada",
                "Fuente Propuesta": "SIES / Mineduc 2025",
                "Estado de Datos": "🟢 Disponible y Verificado",
                "Dependencia": "Resuelta en el incremento actual",
            },
            {
                "Criterio": "C2: Infraestructura Habilitante",
                "Dimensión": "Inmuebles y sedes físicas",
                "Fuente Propuesta": "IDE Chile 2020",
                "Estado de Datos": "🟡 Parcial (desfase 5 años)",
                "Dependencia": "Requiere catastro actualizado",
            },
            {
                "Criterio": "C3: Demanda Laboral y Ocupacional",
                "Dimensión": "Necesidades productivas reales",
                "Fuente Propuesta": "INE (ENE) / BNE / SENCE",
                "Estado de Datos": "🔴 No Disponible (0 filas)",
                "Dependencia": "Investigaciones #27 y #28",
            },
            {
                "Criterio": "C4: Exposición y Complementariedad IA",
                "Dimensión": "Afinidad técnica con proyectos IA",
                "Fuente Propuesta": "Metodología OIT / FMI",
                "Estado de Datos": "🔴 No Disponible (0 filas)",
                "Dependencia": "Investigación #29",
            },
        ])

        st.dataframe(df_criterios_roadmap, width="stretch", hide_index=True)


if __name__ == "__main__":
    main()
