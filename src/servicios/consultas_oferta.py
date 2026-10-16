"""Módulo de consultas analíticas sobre la base DuckDB de Brújula IA Regional.

Capa de servicios desacoplada de la interfaz visual. Todas las consultas
operan en modo solo lectura sobre los esquemas 'gob', 'core' y 'mart'.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import duckdb
import pandas as pd

RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
BD_DEFAULT = RAIZ_PROYECTO / "data" / "processed" / "brujula.duckdb"


def conectar(db_path: Path | str | None = None) -> duckdb.DuckDBPyConnection:
    """Abre una conexión en modo solo lectura a la base DuckDB."""
    ruta = Path(db_path) if db_path else BD_DEFAULT
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró la base de datos DuckDB en: {ruta}")
    return duckdb.connect(str(ruta), read_only=True)


def obtener_resumen_general(db_path: Path | str | None = None) -> dict[str, Any]:
    """Retorna métricas macro de la base de datos para la vista general."""
    con = conectar(db_path)
    try:
        titulos = con.execute("SELECT sum(n_titulos) FROM mart.oferta").fetchone()[0] or 0
        instituciones = con.execute("SELECT count(DISTINCT cod_inst) FROM mart.oferta").fetchone()[0] or 0
        regiones = con.execute("SELECT count(DISTINCT cod_region) FROM mart.oferta").fetchone()[0] or 0
        programas = con.execute("SELECT count(DISTINCT cod_programa) FROM core.programa").fetchone()[0] or 0
        inmuebles = con.execute("SELECT count(*) FROM core.inmueble").fetchone()[0] or 0

        # Modalidades
        df_modalidad = con.execute(
            """
            SELECT modalidad, sum(n_titulos) AS titulos,
                   round(sum(n_titulos) * 100.0 / (SELECT sum(n_titulos) FROM mart.oferta), 2) AS pct
            FROM mart.oferta GROUP BY modalidad ORDER BY titulos DESC
            """
        ).df()

        # Elegibilidad
        df_elegibilidad = con.execute(
            """
            SELECT elegible_tesis, sum(n_titulos) AS titulos,
                   round(sum(n_titulos) * 100.0 / (SELECT sum(n_titulos) FROM mart.oferta), 2) AS pct
            FROM mart.oferta GROUP BY elegible_tesis ORDER BY titulos DESC
            """
        ).df()

        return {
            "total_titulaciones": int(titulos),
            "total_instituciones": int(instituciones),
            "total_regiones": int(regiones),
            "total_programas": int(programas),
            "total_inmuebles": int(inmuebles),
            "distribucion_modalidad": df_modalidad,
            "distribucion_elegibilidad": df_elegibilidad,
        }
    finally:
        con.close()


def obtener_opciones_filtros(db_path: Path | str | None = None) -> dict[str, list[dict[str, Any]]]:
    """Retorna las listas de valores únicos disponibles para los filtros de la interfaz."""
    con = conectar(db_path)
    try:
        regiones = con.execute(
            "SELECT cod_region, nombre FROM core.region ORDER BY cod_region"
        ).fetchall()
        instituciones = con.execute(
            "SELECT cod_inst, nombre FROM core.institucion ORDER BY nombre"
        ).fetchall()
        areas = con.execute(
            "SELECT id_area_generica, nombre FROM core.area_generica ORDER BY nombre"
        ).fetchall()
        comunas = con.execute(
            """
            SELECT DISTINCT c.id_comuna, c.nombre, c.cod_region
            FROM core.comuna c
            JOIN core.sede s USING (id_comuna)
            ORDER BY c.nombre
            """
        ).fetchall()
        modalidades = [
            r[0] for r in con.execute("SELECT DISTINCT modalidad FROM mart.oferta ORDER BY 1").fetchall()
        ]
        niveles = [
            r[0] for r in con.execute("SELECT DISTINCT nivel FROM mart.oferta ORDER BY 1").fetchall()
        ]

        return {
            "regiones": [{"codigo": r[0], "nombre": r[1]} for r in regiones],
            "comunas": [{"codigo": r[0], "nombre": r[1], "cod_region": r[2]} for r in comunas],
            "instituciones": [{"codigo": r[0], "nombre": r[1]} for r in instituciones],
            "areas": [{"codigo": r[0], "nombre": r[1]} for r in areas],
            "modalidades": modalidades,
            "niveles": niveles,
        }
    finally:
        con.close()


def filtrar_oferta(
    db_path: Path | str | None = None,
    cod_region: int | None = None,
    id_comuna: int | None = None,
    cod_inst: int | None = None,
    id_area_generica: int | None = None,
    modalidad: str | None = None,
    elegible_tesis: str | None = None,
) -> pd.DataFrame:
    """Filtra la oferta aplicando parámetros opcionales.

    Si id_comuna está presente, consulta a nivel comunal uniendo con core.sede y core.comuna.
    Si id_comuna es None, consulta directamente mart.oferta a nivel regional.
    """
    con = conectar(db_path)
    try:
        where_clauses = ["1=1"]
        params: list[Any] = []

        if cod_region is not None:
            where_clauses.append("r.cod_region = ?" if id_comuna is not None else "cod_region = ?")
            params.append(cod_region)
        if cod_inst is not None:
            where_clauses.append("i.cod_inst = ?" if id_comuna is not None else "cod_inst = ?")
            params.append(cod_inst)
        if id_area_generica is not None:
            where_clauses.append("a.id_area_generica = ?" if id_comuna is not None else "id_area_generica = ?")
            params.append(id_area_generica)
        if modalidad is not None and modalidad != "Todas":
            where_clauses.append("p.modalidad = ?" if id_comuna is not None else "modalidad = ?")
            params.append(modalidad)
        if elegible_tesis is not None and elegible_tesis != "Todos":
            where_clauses.append("n.elegible_tesis = ?" if id_comuna is not None else "elegible_tesis = ?")
            params.append(elegible_tesis)

        if id_comuna is not None:
            where_clauses.append("c.id_comuna = ?")
            params.append(id_comuna)
            sql = f"""
                SELECT r.nombre AS region, c.nombre AS comuna, i.nombre AS institucion,
                       i.tipo_inst_1, a.nombre AS area_generica, n.nombre AS nivel,
                       n.elegible_tesis, p.modalidad, SUM(t.n_titulos) AS n_titulos
                FROM core.titulacion t
                JOIN core.programa p      USING (cod_programa)
                JOIN core.sede s          USING (cod_inst, cod_sede)
                JOIN core.comuna c        USING (id_comuna)
                JOIN core.region r        USING (cod_region)
                JOIN core.institucion i   USING (cod_inst)
                JOIN core.area_generica a USING (id_area_generica)
                JOIN core.nivel_carrera n USING (id_nivel)
                WHERE {' AND '.join(where_clauses)}
                GROUP BY ALL
                ORDER BY n_titulos DESC
            """
        else:
            sql = f"""
                SELECT region, institucion, tipo_inst_1, area_generica, nivel,
                       elegible_tesis, modalidad, n_titulos
                FROM mart.oferta
                WHERE {' AND '.join(where_clauses)}
                ORDER BY n_titulos DESC
            """
        return con.execute(sql, params).df()
    finally:
        con.close()


def obtener_sedes_geo(
    db_path: Path | str | None = None,
    cod_region: int | None = None,
    id_comuna: int | None = None,
    cod_inst: int | None = None,
) -> dict[str, Any]:
    """Retorna las sedes con coordenadas geográficas válidas y estadísticas de cobertura espacial."""
    con = conectar(db_path)
    try:
        where_clauses = ["latitud IS NOT NULL AND longitud IS NOT NULL"]
        params: list[Any] = []

        if cod_region is not None:
            where_clauses.append("cod_region = ?")
            params.append(cod_region)
        if id_comuna is not None:
            # Obtener nombre de la comuna o id_comuna
            where_clauses.append("comuna = (SELECT nombre FROM core.comuna WHERE id_comuna = ?)")
            params.append(id_comuna)
        if cod_inst is not None:
            where_clauses.append("cod_inst = ?")
            params.append(cod_inst)

        sql = f"""
            SELECT id_inmueble, cod_inst, institucion, tipo_inst_1, inmueble,
                   comuna, cod_region, region, latitud, longitud,
                   coalesce(n_titulos_inst_comuna, 0) AS titulos_comuna
            FROM mart.sedes_geo
            WHERE {' AND '.join(where_clauses)}
            ORDER BY institucion, comuna
        """
        df_inmuebles = con.execute(sql, params).df()

        # Coberturas y advertencias
        total_inmuebles = con.execute("SELECT count(*) FROM core.inmueble").fetchone()[0]
        inmuebles_sin_oferta = con.execute(
            "SELECT count(*) FROM mart.sedes_geo WHERE n_titulos_inst_comuna IS NULL"
        ).fetchone()[0]
        sedes_sin_inmueble = con.execute(
            """
            SELECT count(*) FROM core.sede s
            WHERE NOT EXISTS (
                SELECT 1 FROM core.inmueble m
                WHERE m.cod_inst = s.cod_inst AND m.id_comuna = s.id_comuna
            )
            """
        ).fetchone()[0]

        return {
            "df_puntos": df_inmuebles,
            "total_inmuebles": int(total_inmuebles),
            "inmuebles_sin_oferta_periodo": int(inmuebles_sin_oferta),
            "sedes_sin_correspondencia_geo": int(sedes_sin_inmueble),
            "anio_fuente_geo": 2020,
            "anio_fuente_oferta": 2025,
        }
    finally:
        con.close()


def obtener_especializacion(
    db_path: Path | str | None = None,
    cod_region: int | None = None,
    id_area_generica: int | None = None,
    umbral_celda_pequena: int = 5,
) -> dict[str, Any]:
    """Retorna los cocientes de especialización (LQ) regional por área formativa con banderas de celda pequeña."""
    con = conectar(db_path)
    try:
        where_clauses = ["1=1"]
        params: list[Any] = []

        if cod_region is not None:
            where_clauses.append("cod_region = ?")
            params.append(cod_region)
        if id_area_generica is not None:
            where_clauses.append("id_area_generica = ?")
            params.append(id_area_generica)

        sql = f"""
            WITH ra AS (
                SELECT periodo, cod_region, region, id_area_generica, area_generica, SUM(n_titulos) AS n_titulos
                FROM mart.oferta
                GROUP BY ALL
            ),
            calc AS (
                SELECT cod_region, region, id_area_generica, area_generica,
                       n_titulos,
                       n_titulos AS t_ra,
                       SUM(n_titulos) OVER (PARTITION BY periodo, cod_region) AS t_r,
                       SUM(n_titulos) OVER (PARTITION BY periodo, id_area_generica) AS t_a,
                       SUM(n_titulos) OVER (PARTITION BY periodo) AS t_total,
                       round(n_titulos * 100.0 / SUM(n_titulos) OVER (PARTITION BY periodo, cod_region), 3) AS pct_region,
                       round(SUM(n_titulos) OVER (PARTITION BY periodo, id_area_generica) * 100.0 / SUM(n_titulos) OVER (PARTITION BY periodo), 3) AS pct_nacional,
                       (n_titulos / SUM(n_titulos) OVER (PARTITION BY periodo, cod_region))
                         / (SUM(n_titulos) OVER (PARTITION BY periodo, id_area_generica) / SUM(n_titulos) OVER (PARTITION BY periodo))
                         AS cociente_especializacion
                FROM ra
            )
            SELECT cod_region, region, id_area_generica, area_generica,
                   n_titulos, t_ra, t_r, t_a, t_total, pct_region, pct_nacional,
                   round(cociente_especializacion, 2) AS cociente_especializacion
            FROM calc
            WHERE {' AND '.join(where_clauses)}
            ORDER BY cociente_especializacion DESC
        """
        df = con.execute(sql, params).df()
        if not df.empty:
            df["es_celda_pequena"] = df["n_titulos"] < umbral_celda_pequena

        # Estadísticas de distribución
        stats = con.execute(
            """
            SELECT count(*) AS total_celdas,
                    min(cociente_especializacion) AS min_lq,
                    quantile_cont(cociente_especializacion, 0.5) AS med_lq,
                    max(cociente_especializacion) AS max_lq
            FROM mart.especializacion
            """
        ).fetchone()

        celdas_pequenas_total = int(df["es_celda_pequena"].sum()) if not df.empty else 0

        return {
            "df_especializacion": df,
            "total_celdas": stats[0],
            "min_lq": stats[1],
            "mediana_lq": stats[2],
            "max_lq": stats[3],
            "umbral_aplicado": umbral_celda_pequena,
            "celdas_pequenas_count": celdas_pequenas_total,
        }
    finally:
        con.close()


def obtener_trazabilidad_fuentes(db_path: Path | str | None = None) -> pd.DataFrame:
    """Retorna la bitácora de fuentes y lotes de carga registrados con sus hashes SHA-256."""
    con = conectar(db_path)
    try:
        sql = """
            SELECT f.id_fuente, f.nombre, f.organismo, c.archivo, c.periodo,
                   c.filas_leidas, c.sha256, c.fecha_carga, f.licencia,
                   f.contiene_datos_personales
            FROM gob.carga c
            JOIN gob.fuente f ON f.id_fuente = c.id_fuente
            ORDER BY c.id_carga
        """
        return con.execute(sql).df()
    finally:
        con.close()


def obtener_controles_calidad(db_path: Path | str | None = None) -> pd.DataFrame:
    """Retorna los resultados de los controles de calidad e invariantes de datos."""
    con = conectar(db_path)
    try:
        sql = """
            SELECT regla, descripcion, valor, umbral, cumple, detalle
            FROM gob.control_calidad
            ORDER BY regla
        """
        return con.execute(sql).df()
    finally:
        con.close()


def obtener_distribucion_regional(db_path: Path | str | None = None) -> pd.DataFrame:
    """Retorna la distribución nacional por región con recuentos e infraestructura."""
    con = conectar(db_path)
    try:
        sql = """
            WITH inm AS (
                SELECT cod_region, count(*) AS n_inmuebles
                FROM core.inmueble
                JOIN core.comuna USING (id_comuna)
                GROUP BY cod_region
            ),
            reg AS (
                SELECT r.cod_region, r.nombre AS region,
                       sum(t.n_titulos) AS n_titulos,
                       round(sum(t.n_titulos) * 100.0 / (SELECT sum(n_titulos) FROM mart.oferta), 2) AS pct_nacional,
                       count(DISTINCT p.cod_inst) AS n_instituciones,
                       count(DISTINCT p.cod_programa) AS n_programas
                FROM core.titulacion t
                JOIN core.programa p USING (cod_programa)
                JOIN core.sede s USING (cod_inst, cod_sede)
                JOIN core.comuna c USING (id_comuna)
                JOIN core.region r USING (cod_region)
                GROUP BY r.cod_region, r.nombre
            )
            SELECT reg.cod_region, reg.region, reg.n_titulos, reg.pct_nacional,
                   reg.n_instituciones, reg.n_programas,
                   coalesce(inm.n_inmuebles, 0) AS n_inmuebles
            FROM reg
            LEFT JOIN inm USING (cod_region)
            ORDER BY reg.n_titulos DESC
        """
        return con.execute(sql).df()
    finally:
        con.close()


def obtener_distribucion_niveles(db_path: Path | str | None = None) -> pd.DataFrame:
    """Retorna la desagregación de oferta por nivel formativo y estado de elegibilidad de tesis."""
    con = conectar(db_path)
    try:
        sql = """
            SELECT n.id_nivel, n.nombre AS nivel, n.elegible_tesis,
                   sum(t.n_titulos) AS n_titulos,
                   round(sum(t.n_titulos) * 100.0 / (SELECT sum(n_titulos) FROM mart.oferta), 2) AS pct_nacional,
                   count(DISTINCT t.cod_programa) AS n_programas
            FROM core.titulacion t
            JOIN core.programa p USING (cod_programa)
            JOIN core.nivel_carrera n USING (id_nivel)
            GROUP BY n.id_nivel, n.nombre, n.elegible_tesis
            ORDER BY n_titulos DESC
        """
        return con.execute(sql).df()
    finally:
        con.close()


def obtener_distribucion_tipos_inst(db_path: Path | str | None = None) -> pd.DataFrame:
    """Retorna la distribución de oferta según tipo de institución (Universidad, IP, CFT)."""
    con = conectar(db_path)
    try:
        sql = """
            SELECT i.tipo_inst_1,
                   sum(t.n_titulos) AS n_titulos,
                   round(sum(t.n_titulos) * 100.0 / (SELECT sum(n_titulos) FROM mart.oferta), 2) AS pct_nacional,
                   count(DISTINCT i.cod_inst) AS n_instituciones
            FROM core.titulacion t
            JOIN core.programa p USING (cod_programa)
            JOIN core.institucion i USING (cod_inst)
            GROUP BY i.tipo_inst_1
            ORDER BY n_titulos DESC
        """
        return con.execute(sql).df()
    finally:
        con.close()


def obtener_top_areas(
    db_path: Path | str | None = None,
    cod_region: int | None = None,
    limit: int = 10,
) -> pd.DataFrame:
    """Retorna las áreas genéricas de formación con mayor volumen de titulados."""
    con = conectar(db_path)
    try:
        where_clause = "WHERE r.cod_region = ?" if cod_region is not None else ""
        params = [cod_region] if cod_region is not None else []

        sql = f"""
            SELECT a.id_area_generica, a.nombre AS area_generica,
                   sum(t.n_titulos) AS n_titulos,
                   round(sum(t.n_titulos) * 100.0 / (
                       SELECT sum(n_titulos) FROM mart.oferta {'WHERE cod_region = ?' if cod_region is not None else ''}
                   ), 2) AS pct
            FROM core.titulacion t
            JOIN core.programa p USING (cod_programa)
            JOIN core.sede s USING (cod_inst, cod_sede)
            JOIN core.comuna c USING (id_comuna)
            JOIN core.region r USING (cod_region)
            JOIN core.area_generica a USING (id_area_generica)
            {where_clause}
            GROUP BY a.id_area_generica, a.nombre
            ORDER BY n_titulos DESC
            LIMIT {limit}
        """
        # Si se filtró por región, el subselect también lleva el parámetro
        all_params = params * 2 if cod_region is not None else params
        return con.execute(sql, all_params).df()
    finally:
        con.close()


def obtener_estado_priorizacion(db_path: Path | str | None = None) -> dict[str, Any]:
    """Retorna el estado de gobernanza y bloqueo metodológico del ranking multicriterio."""
    con = conectar(db_path)
    try:
        n_demanda = con.execute("SELECT count(*) FROM core.indicador_region_sector").fetchone()[0]
        n_vinculo = con.execute("SELECT count(*) FROM core.vinculo_area_sector").fetchone()[0]
        n_criterios = con.execute("SELECT count(*) FROM core.criterio").fetchone()[0]
        n_escenarios = con.execute("SELECT count(*) FROM core.escenario").fetchone()[0]

        return {
            "estado": "BLOQUEADO",
            "motivo": "Ausencia de fuentes de demanda laboral externa validadas e índices IA sin consenso ministerial",
            "filas_demanda": n_demanda,
            "filas_vinculo": n_vinculo,
            "criterios_definidos": n_criterios,
            "escenarios_definidos": n_escenarios,
            "decisiones_pendientes": ["D1 (Ponderación)", "D3 (Elegibilidad técnicos)", "D4 (Fuentes demanda)", "D6 (Umbrales territoriales)"],
        }
    finally:
        con.close()

