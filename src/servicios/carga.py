"""Carga de la API de consultas en procesos Streamlit que sobreviven a actualizaciones."""

from importlib import import_module, reload
from threading import RLock
from types import ModuleType

_BLOQUEO_CARGA = RLock()


def cargar_consultas() -> ModuleType:
    """Recupera la API actual si un proceso conserva los servicios previos.

    Solo se recarga si faltan funciones públicas; no se ocultan errores de
    dependencias ni se importa el mismo archivo bajo un segundo nombre.
    """
    with _BLOQUEO_CARGA:
        modulo = import_module("src.servicios.consultas_oferta")
        if any(not callable(getattr(modulo, nombre, None)) for nombre in FUNCIONES_PUBLICAS):
            modulo = reload(modulo)
        faltantes = [nombre for nombre in FUNCIONES_PUBLICAS if not callable(getattr(modulo, nombre, None))]
        if faltantes:
            raise ImportError("API de servicios incompleta: " + ", ".join(faltantes))
        return modulo



FUNCIONES_PUBLICAS = [
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
