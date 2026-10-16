"""Regresión de arranque con servidor real, sesión y resultados DuckDB."""

import json
import subprocess
import sys
from pathlib import Path


def test_arranque_real_entrega_datos_y_componentes():
    raiz = Path(__file__).resolve().parents[1]
    resultado = subprocess.run(
        [sys.executable, "scripts/verificar_arranque.py"],
        cwd=raiz, check=False, capture_output=True, text=True, timeout=90,
    )
    assert resultado.returncode == 0, resultado.stdout + resultado.stderr
    evidencia = json.loads(resultado.stdout)
    assert evidencia["ejecucion_completa"]
    assert evidencia["metricas"]["Total Titulaciones"] == "328.998"
    assert evidencia["metricas"]["Regiones Cubiertas"] == "16"
    assert {"dataframe", "vega_lite_chart", "deck_gl_json_chart"} <= set(evidencia["componentes"])
