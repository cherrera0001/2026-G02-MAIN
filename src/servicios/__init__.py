"""Capa de servicios desacoplada de la base de datos DuckDB."""

from src.servicios.consultas_oferta import (
    conectar,
    filtrar_oferta,
    obtener_controles_calidad,
    obtener_especializacion,
    obtener_opciones_filtros,
    obtener_resumen_general,
    obtener_sedes_geo,
    obtener_trazabilidad_fuentes,
)

__all__ = [
    "conectar",
    "filtrar_oferta",
    "obtener_controles_calidad",
    "obtener_especializacion",
    "obtener_opciones_filtros",
    "obtener_resumen_general",
    "obtener_sedes_geo",
    "obtener_trazabilidad_fuentes",
]
