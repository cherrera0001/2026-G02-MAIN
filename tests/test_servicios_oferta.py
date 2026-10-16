"""Pruebas unitarias para la capa de servicios analíticos de oferta formativa.

Verifica:
- Lectura de DuckDB (Requisito 2)
- Funcionamiento de filtros (Requisito 3)
- Consistencia de totales (Requisito 4)
- Ausencia de duplicación por joins (Requisito 5)
- Comportamiento cuando faltan datos (Requisito 6)
- Visualización de sedes con coordenadas válidas (Requisito 7)
- Tratamiento de celdas pequeñas (Requisito 8)
- Protección de información sensible (Requisito 9)
- Ausencia de rankings calculados sin fundamento (Requisito 10)
"""

from __future__ import annotations

import duckdb
import pytest

from src.servicios.consultas_oferta import (
    BD_DEFAULT,
    conectar,
    filtrar_oferta,
    obtener_controles_calidad,
    obtener_especializacion,
    obtener_opciones_filtros,
    obtener_resumen_general,
    obtener_sedes_geo,
    obtener_trazabilidad_fuentes,
)


@pytest.fixture
def con_db():
    """Fixture de conexión de solo lectura a DuckDB."""
    con = conectar()
    yield con
    con.close()


# -----------------------------------------------------------------------------
# Requisito 2: Lectura de DuckDB
# -----------------------------------------------------------------------------
def test_lectura_duckdb(con_db: duckdb.DuckDBPyConnection):
    """Verifica que la base de datos DuckDB existe y contiene los esquemas y tablas esperados."""
    assert BD_DEFAULT.exists(), f"La base de datos no existe en {BD_DEFAULT}"

    # Verificar existencia de tablas en los esquemas principales
    tablas = [
        r[0]
        for r in con_db.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema IN ('gob', 'core', 'mart')"
        ).fetchall()
    ]
    assert len(tablas) > 0, "No se encontraron tablas en los esquemas del sistema"

    # Verificar existencia de esquemas principales
    esquemas = [r[0] for r in con_db.execute("SELECT schema_name FROM information_schema.schemata").fetchall()]
    assert "gob" in esquemas
    assert "core" in esquemas
    assert "mart" in esquemas


# -----------------------------------------------------------------------------
# Requisito 4: Consistencia de totales
# -----------------------------------------------------------------------------
def test_consistencia_totales():
    """Verifica que los totales macro del resumen coincidan exactamente con la línea base censal."""
    resumen = obtener_resumen_general()

    assert resumen["total_titulaciones"] == 328998, "El total de titulaciones debe ser exactamente 328.998"
    assert resumen["total_instituciones"] == 123, "Debe haber 123 instituciones con titulados en 2025"
    assert resumen["total_regiones"] == 16, "Debe haber 16 regiones político-administrativas"
    assert resumen["total_programas"] == 15469, "Debe haber 15.469 programas académicos registrados"
    assert resumen["total_inmuebles"] == 1297, "Debe haber 1.297 inmuebles catastrados"

    # Consistencia en distribución de modalidades
    df_mod = resumen["distribucion_modalidad"]
    assert df_mod["titulos"].sum() == 328998
    assert abs(df_mod["pct"].sum() - 100.0) < 0.1

    # Consistencia en distribución de elegibilidad
    df_eleg = resumen["distribucion_elegibilidad"]
    assert df_eleg["titulos"].sum() == 328998
    assert abs(df_eleg["pct"].sum() - 100.0) < 0.1


# -----------------------------------------------------------------------------
# Requisito 5: Ausencia de duplicación por joins
# -----------------------------------------------------------------------------
def test_ausencia_duplicacion_joins(con_db: duckdb.DuckDBPyConnection):
    """Verifica que ninguna vista o join genere multiplicación artificial de títulos."""
    total_hecho = con_db.execute("SELECT sum(n_titulos) FROM core.titulacion").fetchone()[0]
    total_mart_oferta = con_db.execute("SELECT sum(n_titulos) FROM mart.oferta").fetchone()[0]

    assert total_hecho == 328998
    assert total_mart_oferta == total_hecho, (
        f"mart.oferta ({total_mart_oferta}) no coincide con core.titulacion ({total_hecho})"
    )

    df_sin_filtro = filtrar_oferta()
    assert df_sin_filtro["n_titulos"].sum() == 328998


# -----------------------------------------------------------------------------
# Requisito 3: Funcionamiento de filtros
# -----------------------------------------------------------------------------
def test_funcionamiento_filtros():
    """Verifica el funcionamiento exacto de los filtros analíticos simples y combinados."""
    opciones = obtener_opciones_filtros()
    assert len(opciones["regiones"]) == 16
    assert len(opciones["instituciones"]) == 144
    assert len(opciones["comunas"]) > 0

    # Filtro por Región (ej. Región Metropolitana, cod=13)
    df_rm = filtrar_oferta(cod_region=13)
    assert not df_rm.empty
    assert (df_rm["region"].str.upper() == "REGIÓN METROPOLITANA DE SANTIAGO").all()
    assert df_rm["n_titulos"].sum() < 328998

    # Filtro por Modalidad 'Presencial'
    df_pres = filtrar_oferta(modalidad="Presencial")
    assert not df_pres.empty
    assert (df_pres["modalidad"] == "Presencial").all()

    # Filtro por Elegibilidad 'si'
    df_eleg_si = filtrar_oferta(elegible_tesis="si")
    assert not df_eleg_si.empty
    assert (df_eleg_si["elegible_tesis"] == "si").all()

    # Filtro por Comuna
    primera_comuna = opciones["comunas"][0]["codigo"]
    df_comuna = filtrar_oferta(id_comuna=primera_comuna)
    assert not df_comuna.empty
    assert "comuna" in df_comuna.columns


# -----------------------------------------------------------------------------
# Requisito 6: Comportamiento cuando faltan datos
# -----------------------------------------------------------------------------
def test_comportamiento_faltan_datos():
    """Verifica que consultas con filtros sin coincidencias retornen estructuras válidas y vacías."""
    # Código de región inexistente (999)
    df_vacio = filtrar_oferta(cod_region=999)
    assert df_vacio.empty
    assert "region" in df_vacio.columns
    assert "n_titulos" in df_vacio.columns

    # Institución inexistente (99999)
    df_inst_vacia = filtrar_oferta(cod_inst=99999)
    assert df_inst_vacia.empty

    # Filtro geo inexistente
    geo_vacio = obtener_sedes_geo(cod_region=999)
    assert geo_vacio["df_puntos"].empty
    assert geo_vacio["total_inmuebles"] == 1297


# -----------------------------------------------------------------------------
# Requisito 7: Visualización de sedes con coordenadas válidas
# -----------------------------------------------------------------------------
def test_visualizacion_sedes_coordenadas_validas():
    """Verifica la calidad y límites geográficos de las sedes e inmuebles."""
    geo_data = obtener_sedes_geo()
    df_geo = geo_data["df_puntos"]

    assert not df_geo.empty
    assert len(df_geo) == 1297

    # Coordenadas no nulas
    assert df_geo["latitud"].notna().all()
    assert df_geo["longitud"].notna().all()

    # Límites territoriales aproximados de Chile
    # Latitud entre -60° (Sur) y -17° (Norte)
    assert (df_geo["latitud"] >= -60.0).all() and (df_geo["latitud"] <= -17.0).all()
    # Longitud entre -80° y -65°
    assert (df_geo["longitud"] >= -80.0).all() and (df_geo["longitud"] <= -65.0).all()

    # 49 sedes Mineduc sin correspondencia en la capa física 2020
    assert geo_data["sedes_sin_correspondencia_geo"] == 49
    assert geo_data["anio_fuente_geo"] == 2020
    assert geo_data["anio_fuente_oferta"] == 2025


# -----------------------------------------------------------------------------
# Requisito 8: Tratamiento de celdas pequeñas
# -----------------------------------------------------------------------------
def test_tratamiento_celdas_pequenas():
    """Verifica que los cocientes LQ marquen rigurosamente celdas con bajo conteo muestral."""
    # Umbral por defecto tau = 5
    lq_data_5 = obtener_especializacion(umbral_celda_pequena=5)
    df_lq_5 = lq_data_5["df_especializacion"]

    assert not df_lq_5.empty
    assert "es_celda_pequena" in df_lq_5.columns

    celdas_pequenas_5 = df_lq_5[df_lq_5["es_celda_pequena"]]
    assert (celdas_pequenas_5["n_titulos"] < 5).all()

    celdas_grandes_5 = df_lq_5[~df_lq_5["es_celda_pequena"]]
    assert (celdas_grandes_5["n_titulos"] >= 5).all()

    # Umbral más estricto tau = 20
    lq_data_20 = obtener_especializacion(umbral_celda_pequena=20)
    df_lq_20 = lq_data_20["df_especializacion"]
    assert df_lq_20["es_celda_pequena"].sum() >= df_lq_5["es_celda_pequena"].sum()


# -----------------------------------------------------------------------------
# Requisito 9: Protección de información sensible
# -----------------------------------------------------------------------------
def test_proteccion_informacion_sensible(con_db: duckdb.DuckDBPyConnection):
    """Verifica que ningún identificador personal persista en la base analítica."""
    # 1. Auditoría del control de calidad interno
    df_controles = obtener_controles_calidad()
    ctrl_privacidad = df_controles[df_controles["regla"] == "sin_datos_personales"]
    assert not ctrl_privacidad.empty
    assert ctrl_privacidad.iloc[0]["valor"] == 0, "No debe haber columnas con datos personales"
    assert bool(ctrl_privacidad.iloc[0]["cumple"]) is True

    # 2. Inspección exhaustiva de todas las columnas de la base de datos
    columnas = con_db.execute(
        """
        SELECT table_schema, table_name, column_name
        FROM information_schema.columns
        WHERE table_schema IN ('core', 'mart')
        """
    ).fetchall()

    terminos_prohibidos = [
        "mrun", "rut", "nombre_alumno", "nombre_estudiante", "fecha_nacimiento",
        "edad", "direccion_personal", "telefono", "email"
    ]

    for schema, tabla, col in columnas:
        col_lower = col.lower()
        for prohibido in terminos_prohibidos:
            assert prohibido not in col_lower, (
                f"Columna sospechosa '{col}' en {schema}.{tabla} viola la política de privacidad"
            )


# -----------------------------------------------------------------------------
# Requisito 10: Ausencia de rankings calculados sin fundamento
# -----------------------------------------------------------------------------
def test_ausencia_rankings_sin_fundamento(con_db: duckdb.DuckDBPyConnection):
    """Verifica que no se calculen rankings multicriterio o índices inventados."""
    columnas_mart = [
        r[0].lower()
        for r in con_db.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_schema = 'mart'"
        ).fetchall()
    ]

    terminos_ranking = [
        "ranking", "score_ia", "puntaje_priorizacion", "demanda_estimada", "indice_prioridad"
    ]

    for col in columnas_mart:
        for termino in terminos_ranking:
            assert termino not in col, (
                f"Columna de ranking espuria '{col}' encontrada en mart; científicamente bloqueada"
            )

    # Tablas de demanda y vínculo deben estar vacías o no inferir ranking
    demanda_rows = con_db.execute("SELECT count(*) FROM core.indicador_region_sector").fetchone()[0]
    assert demanda_rows == 0, "core.indicador_region_sector debe permanecer vacía hasta validar fuentes de demanda"

    vinculo_rows = con_db.execute("SELECT count(*) FROM core.vinculo_area_sector").fetchone()[0]
    assert vinculo_rows == 0, "core.vinculo_area_sector debe permanecer vacía hasta validar matriz de vinculación"


# -----------------------------------------------------------------------------
# Trazabilidad
# -----------------------------------------------------------------------------
def test_trazabilidad_fuentes():
    """Verifica que la bitácora de auditoría registre los hashes SHA-256 de las fuentes."""
    df_traz = obtener_trazabilidad_fuentes()
    assert not df_traz.empty
    assert "sha256" in df_traz.columns
    assert df_traz["sha256"].notna().all()
    assert (df_traz["sha256"].str.len() == 64).all()


# -----------------------------------------------------------------------------
# Nuevos Servicios Analíticos (Panorama Nacional, Niveles, Áreas, Priorización)
# -----------------------------------------------------------------------------
def test_distribucion_regional():
    """Verifica la distribución regional agregada, consistencia censal e infraestructura."""
    from src.servicios.consultas_oferta import obtener_distribucion_regional

    df_reg = obtener_distribucion_regional()
    assert len(df_reg) == 16, "Deben estar presentes las 16 regiones de Chile"
    assert df_reg["n_titulos"].sum() == 328998, "La suma de titulados regionales debe ser 328.998"
    assert df_reg["n_inmuebles"].sum() == 1297, "La suma de inmuebles debe ser 1.297"
    assert abs(df_reg["pct_nacional"].sum() - 100.0) < 0.2


def test_distribucion_niveles():
    """Verifica la descomposición por nivel de carrera y elegibilidad de proyectos de tesis."""
    from src.servicios.consultas_oferta import obtener_distribucion_niveles

    df_niv = obtener_distribucion_niveles()
    assert len(df_niv) == 9, "Deben estar catalogados los 9 niveles formativos de Mineduc"
    assert df_niv["n_titulos"].sum() == 328998
    assert set(df_niv["elegible_tesis"].unique()) == {"si", "no", "pendiente"}


def test_distribucion_tipos_inst():
    """Verifica la distribución según tipo de IES (Universidades, IP, CFT)."""
    from src.servicios.consultas_oferta import obtener_distribucion_tipos_inst

    df_tipos = obtener_distribucion_tipos_inst()
    assert len(df_tipos) == 3
    assert df_tipos["n_titulos"].sum() == 328998
    assert set(df_tipos["tipo_inst_1"].str.lower().str.slice(0, 4)) == {"univ", "inst", "cent"}


def test_top_areas():
    """Verifica la consulta de top áreas genéricas con mayor masa crítica."""
    from src.servicios.consultas_oferta import obtener_top_areas

    df_top = obtener_top_areas(limit=10)
    assert len(df_top) == 10
    assert (df_top["n_titulos"] > 0).all()
    # Verificación con filtro de región
    df_top_rm = obtener_top_areas(cod_region=13, limit=5)
    assert len(df_top_rm) == 5
    assert df_top_rm["n_titulos"].sum() < 328998


def test_descomposicion_matematica_lq():
    """Verifica que el cálculo de LQ exponga rigurosamente sus variables subyacentes."""
    lq_res = obtener_especializacion(umbral_celda_pequena=5)
    df_lq = lq_res["df_especializacion"]

    columnas_esperadas = ["t_ra", "t_r", "t_a", "t_total", "pct_region", "pct_nacional", "cociente_especializacion"]
    for col in columnas_esperadas:
        assert col in df_lq.columns, f"Columna matemática '{col}' ausente en la descomposición de LQ"

    assert (df_lq["t_total"] == 328998).all(), "El total nacional de referencia debe ser exactamente 328.998"


def test_estado_priorizacion():
    """Verifica la gobernanza y justificación del bloqueo metodológico del ranking."""
    from src.servicios.consultas_oferta import obtener_estado_priorizacion

    estado = obtener_estado_priorizacion()
    assert estado["estado"] == "BLOQUEADO"
    assert estado["filas_demanda"] == 0
    assert estado["filas_vinculo"] == 0
    assert len(estado["decisiones_pendientes"]) >= 4

