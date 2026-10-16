"""Regresión de arranque al actualizar una app con módulos ya cargados."""

import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.parametrize("entrada", ["app.py", "src/app/streamlit_app.py"])
def test_arranque_con_servicios_de_version_anterior(entrada):
    raiz = Path(__file__).resolve().parents[1]
    codigo = """
import sys
from pathlib import Path
from streamlit.testing.v1 import AppTest
import src.servicios.consultas_oferta as consultas
import src.servicios
if hasattr(src.servicios, "cargar_consultas"):
    delattr(src.servicios, "cargar_consultas")

# Un proceso que servía la app anterior conserva el módulo sin estas funciones.
for nombre in (
    'obtener_distribucion_regional', 'obtener_distribucion_niveles',
    'obtener_distribucion_tipos_inst', 'obtener_top_areas', 'obtener_estado_priorizacion',
):
    if hasattr(consultas, nombre):
        delattr(consultas, nombre)

app = AppTest.from_file(str(Path(sys.argv[1]).resolve()), default_timeout=30).run()
assert not app.exception, str(app.exception)
assert len(app.tabs) == 6
"""
    resultado = subprocess.run(
        [sys.executable, "-c", codigo, entrada],
        check=False,
        cwd=raiz,
        capture_output=True,
        text=True,
        timeout=90,
    )
    assert resultado.returncode == 0, resultado.stdout + resultado.stderr
