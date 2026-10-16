"""Punto de entrada principal para Streamlit Cloud y ejecución local."""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from src.app.streamlit_app import main

if __name__ == "__main__":
    main()
