"""API pública diferida de los servicios analíticos."""

from .carga import FUNCIONES_PUBLICAS

__all__ = FUNCIONES_PUBLICAS


def __getattr__(nombre: str):
    if nombre in __all__:
        from .carga import cargar_consultas

        return getattr(cargar_consultas(), nombre)
    raise AttributeError(f"El paquete {__name__} no contiene {nombre}")
