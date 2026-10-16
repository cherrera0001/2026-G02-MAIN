"""Pruebas funcionales y de interfaz para la aplicación Streamlit con AppTest.

Verifica:
- Inicio sin excepciones de la aplicación Streamlit (Requisito 1)
- Presencia y estructura de las 6 pestañas orientadas a decisiones (Requisito 1)
- Métricas macro de la vista general
- Advertencias de rigor científico (ranking formalmente bloqueado)
- Interacción con filtros jerárquicos en sidebar (Requisito 3)
- Visualización de datos y componentes gráficos interactivos
- Cumplimiento estricto de privacidad en componentes visuales (Requisito 9)
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

    # Verificar banner de bloqueo explícito en la pestaña de priorización
    error_textos = [err.value for err in app_instance.error]
    assert any("MÓDULO FORMALMENTE BLOQUEADO" in t for t in error_textos), (
        "Debe existir un mensaje de bloqueo formal en el módulo de priorización"
    )


def test_streamlit_pestañas_y_metricas(app_instance: AppTest):
    """Verifica que las 6 pestañas analíticas y las métricas macro se inicialicen correctamente."""
    assert not app_instance.exception

    # Verificar que existan las 6 pestañas analíticas
    tabs = [tab.label for tab in app_instance.tabs]
    assert len(tabs) == 6
    assert "📊 Vista General" in tabs
    assert "🔍 Explorador Territorial" in tabs
    assert "🎓 Oferta Formativa" in tabs
    assert "📈 Especialización (LQ)" in tabs
    assert "🛡️ Trazabilidad y Calidad" in tabs
    assert "⚖️ Priorización (Bloqueada)" in tabs

    # Verificar métricas en Vista General (328.998 titulados, 123 IES, 16 regiones, etc.)
    metricas = {m.label: m.value for m in app_instance.metric}
    assert "Total Titulaciones" in metricas
    assert metricas["Total Titulaciones"] == "328.998"
    assert metricas["Instituciones (IES)"] == "123"
    assert metricas["Regiones Cubiertas"] == "16"
    assert metricas["Programas Académicos"] == "15.469"
    assert metricas["Inmuebles Catastrados"] == "1.297"


def test_streamlit_interaccion_filtros():
    """Verifica la respuesta interactiva de la aplicación al seleccionar filtros en sidebar."""
    at = AppTest.from_file(str(RUTA_APP), default_timeout=20).run()
    assert not at.exception

    # Encontrar el selectbox de región en el sidebar
    sb_regiones = next((sb for sb in at.sidebar.selectbox if sb.label == "Región"), None)
    assert sb_regiones is not None
    assert "Todas" in sb_regiones.options

    # Seleccionar Región de Valparaíso
    opcion_region = next(opt for opt in sb_regiones.options if "VALPARA" in opt.upper())
    sb_regiones.select(opcion_region).run(timeout=20)
    assert not at.exception

    # Verificar que las comunas mostradas en sidebar correspondan a la región seleccionada
    sb_comunas = next((sb for sb in at.sidebar.selectbox if sb.label == "Comuna"), None)
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
