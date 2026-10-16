"""Aplicación Streamlit: Explorador Territorial de Oferta Formativa.

Brújula IA Regional — Primer Incremento Funcional del MVP.
Permite explorar la masa crítica de titulados, infraestructura de sedes,
cocientes de especialización territorial (LQ) y trazabilidad de datos.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Asegurar que la raíz del repositorio esté en sys.path para despliegue en Streamlit Cloud
RAIZ_REPOSITORIO = Path(__file__).resolve().parents[2]
if str(RAIZ_REPOSITORIO) not in sys.path:
    sys.path.insert(0, str(RAIZ_REPOSITORIO))

import streamlit as st

from src.servicios.consultas_oferta import (
    filtrar_oferta,
    obtener_controles_calidad,
    obtener_especializacion,
    obtener_opciones_filtros,
    obtener_resumen_general,
    obtener_sedes_geo,
    obtener_trazabilidad_fuentes,
)

# Configuración de página
st.set_page_config(
    page_title="Brújula IA Regional — Explorador Territorial",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data(ttl=3600)
def cargar_resumen():
    return obtener_resumen_general()


@st.cache_data(ttl=3600)
def cargar_filtros():
    return obtener_opciones_filtros()


@st.cache_data(ttl=3600)
def cargar_trazabilidad():
    return obtener_trazabilidad_fuentes()


@st.cache_data(ttl=3600)
def cargar_controles():
    return obtener_controles_calidad()


def main():
    # Encabezado principal
    st.title("🧭 Brújula IA Regional — Explorador Territorial")
    st.markdown(
        "**Herramienta de soporte a la decisión para la priorización territorial "
        "del cofinanciamiento de memorias y tesis aplicadas con IA.**"
    )

    # Alerta ética y de rigor científico
    st.info(
        "ℹ️ **Estado Metodológico**: Este incremento visualiza exclusivamente la **oferta formativa censal (Mineduc 2025)** "
        "y la **infraestructura de sedes (IDE Chile 2020)**. El ranking multicriterio y los factores de demanda económica e IA "
        "permanecen **formalmente BLOQUEADOS** hasta contar con fuentes externas validadas. "
        "No se infiere causalidad ni empleabilidad a partir de los datos mostrados."
    )

    # Navegación por pestañas
    tab_resumen, tab_explorador, tab_mapa, tab_lq, tab_trazabilidad = st.tabs([
        "📊 Vista General",
        "🔍 Explorador Territorial",
        "🗺️ Mapa de Sedes",
        "📈 Especialización (LQ)",
        "🛡️ Trazabilidad y Calidad",
    ])

    # -------------------------------------------------------------------------
    # TAB 1: VISTA GENERAL
    # -------------------------------------------------------------------------
    with tab_resumen:
        st.subheader("Métricas Macro del Sistema (Periodo Censal 2025)")
        resumen = cargar_resumen()

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total Titulaciones", f"{resumen['total_titulaciones']:,}".replace(",", "."))
        col2.metric("Instituciones (IES)", resumen["total_instituciones"])
        col3.metric("Regiones Cubiertas", resumen["total_regiones"])
        col4.metric("Programas Académicos", f"{resumen['total_programas']:,}".replace(",", "."))
        col5.metric("Inmuebles Catastrados", f"{resumen['total_inmuebles']:,}".replace(",", "."))

        st.divider()

        col_izq, col_der = st.columns(2)
        with col_izq:
            st.markdown("#### Distribución por Modalidad de Impartición")
            df_mod = resumen["distribucion_modalidad"]
            st.dataframe(df_mod, width="stretch", hide_index=True)
            st.caption(
                "⚠️ **Nota metodológica**: El 25.08% de los títulos corresponden a modalidad 'No Presencial'. "
                "El 82.4% de estos títulos están radicados administrativamente en la Región Metropolitana, "
                "lo que no refleja el lugar de residencia del estudiante."
            )

        with col_der:
            st.markdown("#### Clasificación según Elegibilidad de Tesis")
            df_eleg = resumen["distribucion_elegibilidad"]
            st.dataframe(df_eleg, width="stretch", hide_index=True)
            st.caption(
                "⚠️ **Decisión D3 Pendiente**: El 44.85% de los títulos (Técnicos de Nivel Superior y Profesionales "
                "sin Licenciatura) se encuentran en estado 'pendiente' a la espera de definición por el Ministerio."
            )

    # -------------------------------------------------------------------------
    # TAB 2: EXPLORADOR TERRITORIAL
    # -------------------------------------------------------------------------
    with tab_explorador:
        st.subheader("Filtros Analíticos de Oferta")
        filtros = cargar_filtros()

        c1, c2, c3 = st.columns(3)
        with c1:
            lista_regiones = ["Todas"] + [r["nombre"] for r in filtros["regiones"]]
            sel_region = st.selectbox("Región", lista_regiones)
            cod_reg = next((r["codigo"] for r in filtros["regiones"] if r["nombre"] == sel_region), None)
        with c2:
            if cod_reg is not None:
                comunas_disp = [c for c in filtros["comunas"] if c["cod_region"] == cod_reg]
            else:
                comunas_disp = filtros["comunas"]
            lista_comunas = ["Todas"] + [c["nombre"] for c in comunas_disp]
            sel_comuna = st.selectbox("Comuna", lista_comunas)
            id_comuna = next((c["codigo"] for c in comunas_disp if c["nombre"] == sel_comuna), None)
        with c3:
            lista_inst = ["Todas"] + [i["nombre"] for i in filtros["instituciones"]]
            sel_inst = st.selectbox("Institución", lista_inst)
            cod_i = next((i["codigo"] for i in filtros["instituciones"] if i["nombre"] == sel_inst), None)

        c4, c5, c6 = st.columns(3)
        with c4:
            lista_areas = ["Todas"] + [a["nombre"] for a in filtros["areas"]]
            sel_area = st.selectbox("Área Genérica de Formación", lista_areas)
            id_a = next((a["codigo"] for a in filtros["areas"] if a["nombre"] == sel_area), None)
        with c5:
            sel_mod = st.selectbox("Modalidad", ["Todas"] + filtros["modalidades"])
        with c6:
            sel_eleg = st.selectbox("Elegibilidad de Tesis", ["Todos", "si", "no", "pendiente"])

        df_filtrada = filtrar_oferta(
            cod_region=cod_reg,
            id_comuna=id_comuna,
            cod_inst=cod_i,
            id_area_generica=id_a,
            modalidad=sel_mod,
            elegible_tesis=sel_eleg,
        )

        st.markdown(f"**Registros encontrados**: {len(df_filtrada):,} combinaciones | **Títulos totales filtrados**: {df_filtrada['n_titulos'].sum():,}".replace(",", "."))

        if not df_filtrada.empty:
            st.dataframe(df_filtrada, width="stretch", hide_index=True)

            # Gráfico de barras por región si no se seleccionó una
            if sel_region == "Todas":
                st.markdown("#### Titulaciones por Región (Filtro Activo)")
                df_reg_agg = df_filtrada.groupby("region")["n_titulos"].sum().reset_index().sort_values("n_titulos", ascending=False)
                st.bar_chart(df_reg_agg, x="region", y="n_titulos")
        else:
            st.warning("No se encontraron registros para los filtros seleccionados.")

    # -------------------------------------------------------------------------
    # TAB 3: MAPA DE SEDES
    # -------------------------------------------------------------------------
    with tab_mapa:
        st.subheader("Localización de Sedes e Inmuebles Universitarios")
        st.markdown(
            "Visualización geográfica de los 1.297 inmuebles catastrados por la IDE Chile (Capa 2020), "
            "vinculados a la oferta formativa comunal de la institución."
        )

        datos_geo = obtener_sedes_geo(cod_region=cod_reg, id_comuna=id_comuna, cod_inst=cod_i)
        df_geo = datos_geo["df_puntos"]

        m1, m2, m3 = st.columns(3)
        m1.metric("Puntos Georreferenciados Mostrados", len(df_geo))
        m2.metric("Inmuebles sin oferta en 2025", datos_geo["inmuebles_sin_oferta_periodo"], help="Inmuebles físicos donde la IES no registró titulados en 2025 (ej. oficinas, sedes administrativas)")
        m3.metric("Sedes sin correspondencia geográfica", datos_geo["sedes_sin_correspondencia_geo"], help="49 sedes de Mineduc que no poseen punto en el catastro 2020 de la IDE")

        if not df_geo.empty:
            df_mapa = df_geo.rename(columns={"latitud": "latitude", "longitud": "longitude"})[["latitude", "longitude"]]
            st.map(df_mapa, zoom=4)
            st.markdown("#### Detalle de Puntos Seleccionados")
            st.dataframe(
                df_geo[["institucion", "tipo_inst_1", "inmueble", "comuna", "region", "titulos_comuna"]],
                width="stretch",
                hide_index=True,
            )
        else:
            st.warning("No hay sedes con coordenadas válidas para la selección actual.")

        st.warning(
            "⚠️ **Limitación Espacial Importante**: Las coordenadas corresponden a la ubicación física de las sedes "
            "(año 2020) y los títulos a 2025 (descalce de 5 años). En programas no presenciales, la sede "
            "no representa el lugar geográfico donde residen los estudiantes."
        )

    # -------------------------------------------------------------------------
    # TAB 4: ESPECIALIZACIÓN TERRITORIAL (LQ)
    # -------------------------------------------------------------------------
    with tab_lq:
        st.subheader("Cociente de Especialización Territorial (Location Quotient)")
        st.markdown(
            """
            El **Cociente de Especialización ($LQ$)** mide la intensidad relativa con que una región forma titulados 
            en un área disciplinaria específica, comparándola contra el promedio nacional:
            $$LQ_{ra} = \\frac{T_{ra} / \\sum_a T_{ra}}{\\sum_r T_{ra} / \\sum_{r,a} T_{ra}}$$
            - **$LQ > 1.0$**: La región tiene mayor concentración de graduados en esa disciplina que el promedio del país (ventaja comparativa revelada).
            - **$LQ = 1.0$**: La concentración coincide con el promedio nacional.
            - **$LQ < 1.0$**: La región tiene menor concentración relativa.
            """
        )

        umbral_celda = st.slider("Umbral de alerta para celdas pequeñas (mínimo de titulados)", min_value=1, max_value=20, value=5)

        datos_lq = obtener_especializacion(
            cod_region=cod_reg,
            id_area_generica=id_a,
            umbral_celda_pequena=umbral_celda,
        )
        df_lq = datos_lq["df_especializacion"]

        c_lq1, c_lq2, c_lq3 = st.columns(3)
        c_lq1.metric("Celdas Analizadas", datos_lq["total_celdas"])
        c_lq2.metric("Mediana Nacional de LQ", f"{datos_lq['mediana_lq']:.2f}")
        c_lq3.metric("LQ Máximo Observado", f"{datos_lq['max_lq']:.2f}", help="Valores extremos suelen deberse a celdas pequeñas con denominadores muy bajos")

        st.caption(
            "⚠️ **Distinción Crítica**: Un $LQ$ alto refleja especialización formativa histórica acumulada, "
            "**no una necesidad económica insatisfecha**. La demanda laboral real requiere fuentes complementarias (SENCE/INE) actualmente no integradas."
        )

        if not df_lq.empty:
            st.dataframe(
                df_lq[["region", "area_generica", "n_titulos", "cociente_especializacion", "es_celda_pequena"]],
                width="stretch",
                hide_index=True,
            )
        else:
            st.info("No hay datos de especialización para el filtro seleccionado.")

    # -------------------------------------------------------------------------
    # TAB 5: TRAZABILIDAD Y CALIDAD
    # -------------------------------------------------------------------------
    with tab_trazabilidad:
        st.subheader("Linaje Criptográfico de Fuentes (Esquema `gob`)")
        df_traz = cargar_trazabilidad()
        st.dataframe(df_traz, width="stretch", hide_index=True)

        st.divider()
        st.subheader("Auditoría de Calidad e Invariantes del Pipeline")
        df_cal = cargar_controles()
        st.dataframe(df_cal, width="stretch", hide_index=True)

        st.success(
            "✅ **Invariante de Privacidad**: El control `sin_datos_personales = 0` certifica que "
            "ninguna columna identificatoria de personas (MRUN, fecha de nacimiento, edad) existe en tablas persistentes."
        )


if __name__ == "__main__":
    main()
