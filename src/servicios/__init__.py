"""Capa de servicios desacoplada de la base de datos DuckDB."""

from src.servicios.consultas_oferta import (
    conectar,
    filtrar_oferta,
    obtener_controles_calidad,
    obtener_distribucion_niveles,
    obtener_distribucion_regional,
    obtener_distribucion_tipos_inst,
    obtener_especializacion,
    obtener_estado_priorizacion,
    obtener_opciones_filtros,
    obtener_resumen_general,
    obtener_sedes_geo,
    obtener_top_areas,
    obtener_trazabilidad_fuentes,
)

__all__ = [
    "conectar",
    "filtrar_oferta",
    "obtener_controles_calidad",
    "obtener_distribucion_niveles",
    "obtener_distribucion_regional",
    "obtener_distribucion_tipos_inst",
    "obtener_especializacion",
    "obtener_estado_priorizacion",
    "obtener_opciones_filtros",
    "obtener_resumen_general",
    "obtener_sedes_geo",
    "obtener_top_areas",
    "obtener_trazabilidad_fuentes",
]

