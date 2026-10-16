"""Pruebas funcionales y de interfaz para la aplicación Streamlit con AppTest.

Verifica:
- Inicio sin excepciones de la aplicación Streamlit (Requisito 1)
- Presencia y estructura de pestañas funcionales
- Métricas macro de la vista general
- Advertencias de rigor científico (ranking formalmente bloqueado)
- Interacción con filtros analíticos
- Cumplimiento de privacidad en componentes visuales
"""

from __future__ import annotations

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

RUTA_APP = Path(__file__).resolve().parents[1] / "src" / "app" / "streamlit_app.py"


@pytest.fixture(scope="module")
def app_instance():
    """Instancia compartida inicializada de la aplicación con timeout suficiente."""
    at = AppTest.from_file(str(RUTA_APP), default_timeout=20).run()
    return at


def test_inicio_streamlit_app(app_instance: AppTest):
    """Verifica que la aplicación Streamlit cargue y se ejecute sin excepciones no controladas (Requisito 1)."""
    assert not app_instance.exception, f"Se produjeron excepciones al iniciar la aplicación: {app_instance.exception}"
    assert app_instance.title[0].value == "🧭 Brújula IA Regional — Explorador Territorial"


def test_streamlit_advertencia_bloqueo_ranking(app_instance: AppTest):
    """Verifica que la aplicación presente visiblemente la advertencia de ranking bloqueado (Requisito 10)."""
    assert not app_instance.exception

    # Verificar que existe el info alert con la restricción metodológica
    info_textos = [info.value for info in app_instance.info]
    assert any("formalmente BLOQUEADOS" in t for t in info_textos), (
        "La aplicación debe advertir que el ranking multicriterio y demanda están formalmente bloqueados"
    )
    assert any("No se infiere causalidad ni empleabilidad" in t for t in info_textos)


def test_streamlit_pestañas_y_metricas(app_instance: AppTest):
    """Verifica que las 5 pestañas canónicas y las métricas macro se inicialicen correctamente."""
    assert not app_instance.exception

    # Verificar pestañas
    tabs = [tab.label for tab in app_instance.tabs]
    assert len(tabs) == 5
    assert "📊 Vista General" in tabs
    assert "🔍 Explorador Territorial" in tabs
    assert "🗺️ Mapa de Sedes" in tabs
    assert "📈 Especialización (LQ)" in tabs
    assert "🛡️ Trazabilidad y Calidad" in tabs

    # Verificar métricas en Vista General (328.998 titulados, 123 IES, 16 regiones, etc.)
    metricas = {m.label: m.value for m in app_instance.metric}
    assert "Total Titulaciones" in metricas
    assert metricas["Total Titulaciones"] == "328.998"
    assert metricas["Instituciones (IES)"] == "123"
    assert metricas["Regiones Cubiertas"] == "16"
    assert metricas["Programas Académicos"] == "15.469"
    assert metricas["Inmuebles Catastrados"] == "1.297"



def test_streamlit_interaccion_filtros():
    """Verifica la respuesta interactiva de la aplicación al seleccionar filtros."""
    at = AppTest.from_file(str(RUTA_APP), default_timeout=20).run()
    assert not at.exception

    # Encontrar el selectbox de región
    sb_regiones = next((sb for sb in at.selectbox if sb.label == "Región"), None)
    assert sb_regiones is not None
    assert "Todas" in sb_regiones.options

    # Seleccionar Región de Valparaíso (o la segunda opción disponible)
    opcion_region = next(opt for opt in sb_regiones.options if "VALPARA" in opt.upper())
    sb_regiones.select(opcion_region).run(timeout=20)
    assert not at.exception

    # Verificar que las comunas mostradas correspondan a la región seleccionada
    sb_comunas = next((sb for sb in at.selectbox if sb.label == "Comuna"), None)
    assert sb_comunas is not None
    assert "Todas" in sb_comunas.options
    assert len(sb_comunas.options) > 1


def test_streamlit_proteccion_privacidad_ui(app_instance: AppTest):
    """Verifica que ningún elemento renderizado contenga términos identificatorios personales."""
    assert not app_instance.exception

    terminos_prohibidos = ["mrun", "rut", "nombre_alumno", "nombre_estudiante", "fecha_nacimiento"]

    # Revisar textos y captions
    for md in app_instance.markdown:
        md_lower = md.value.lower()
        for t in terminos_prohibidos:
            assert t not in md_lower, f"Término personal '{t}' expuesto en markdown UI"

    for cap in app_instance.caption:
        cap_lower = cap.value.lower()
        for t in terminos_prohibidos:
            assert t not in cap_lower, f"Término personal '{t}' expuesto en caption UI"

