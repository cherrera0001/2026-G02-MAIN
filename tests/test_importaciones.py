"""Verificación de importaciones públicas y carga de módulos."""

import importlib
import subprocess
import sys
from pathlib import Path

from src.servicios.carga import FUNCIONES_PUBLICAS


def test_importaciones_publicas_en_proceso_nuevo():
    codigo = (
        "from src.servicios.carga import cargar_consultas; "
        "m = cargar_consultas(); "
        "import src.app.streamlit_app; "
        "assert m.__name__ == 'src.servicios.consultas_oferta'"
    )
    resultado = subprocess.run(
        [sys.executable, "-c", codigo],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert resultado.returncode == 0, resultado.stderr


def test_api_de_consultas_disponible():
    modulo = importlib.import_module("src.servicios.consultas_oferta")
    assert all(callable(getattr(modulo, nombre)) for nombre in FUNCIONES_PUBLICAS)
