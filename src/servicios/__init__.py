"""API pública diferida de los servicios analíticos."""

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


def __getattr__(nombre: str):
    if nombre in __all__:
        from .carga import cargar_consultas

        return getattr(cargar_consultas(), nombre)
    raise AttributeError(f"El paquete {__name__} no contiene {nombre}")
