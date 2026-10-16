"""Comprueba la ejecución real por WebSocket, no solo el HTML o /health."""

from __future__ import annotations

import argparse
import asyncio
import http.cookiejar
import json
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

from streamlit.proto.BackMsg_pb2 import BackMsg
from streamlit.proto.ForwardMsg_pb2 import ForwardMsg
from websockets.asyncio.client import connect


async def comprobar(url: str, cookie: str = "") -> dict:
    ws_url = url.replace("https://", "wss://").replace("http://", "ws://").rstrip("/") + "/_stcore/stream"
    headers = {"Origin": url.rstrip("/")}
    if cookie:
        headers["Cookie"] = cookie
    conexion = await connect(ws_url, additional_headers=headers, subprotocols=["streamlit"], open_timeout=20, max_size=20 * 1024 * 1024)
    try:
        solicitud = BackMsg()
        solicitud.rerun_script.query_string = ""
        await conexion.send(solicitud.SerializeToString())
        metricas = {}
        excepciones = []
        tipos = set()
        for _ in range(3000):
            mensaje = await asyncio.wait_for(conexion.recv(), timeout=60)
            if mensaje is None:
                raise RuntimeError("La conexión terminó antes de completar la ejecución")
            if not isinstance(mensaje, bytes):
                continue
            respuesta = ForwardMsg()
            respuesta.ParseFromString(mensaje)
            tipo = respuesta.WhichOneof("type")
            if tipo == "delta" and respuesta.delta.HasField("new_element"):
                elemento = respuesta.delta.new_element
                clase = elemento.WhichOneof("type")
                tipos.add(clase)
                if clase == "exception":
                    excepciones.append(elemento.exception.type)
                if clase == "metric":
                    metricas[elemento.metric.label] = elemento.metric.body
            if tipo == "script_finished":
                if excepciones:
                    raise RuntimeError("Excepciones en la app: " + ", ".join(excepciones))
                if metricas.get("Total Titulaciones") != "328.998":
                    raise RuntimeError("La app no entregó la métrica de titulaciones esperada")
                return {"ejecucion_completa": True, "metricas": metricas, "componentes": sorted(tipos)}
        raise RuntimeError("No se recibió el fin de ejecución")
    finally:
        await conexion.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", help="Servidor existente; si se omite, inicia Streamlit local")
    args = parser.parse_args()
    if args.url:
        jar = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
        with opener.open(args.url, timeout=25) as respuesta:
            if respuesta.status != 200:
                raise RuntimeError("La URL no está disponible")
        cookie = "; ".join(f"{c.name}={c.value}" for c in jar)
        print(json.dumps(asyncio.run(comprobar(args.url, cookie)), ensure_ascii=True))
        return
    raiz = Path(__file__).resolve().parents[1]
    with socket.socket() as socket_libre:
        socket_libre.bind(("127.0.0.1", 0))
        puerto = socket_libre.getsockname()[1]
    url = f"http://127.0.0.1:{puerto}"
    with tempfile.TemporaryFile() as log:
        proceso = subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", "app.py", "--server.headless=true",
             "--server.address=127.0.0.1", f"--server.port={puerto}", "--browser.gatherUsageStats=false"],
            cwd=raiz, stdout=log, stderr=log,
        )
        try:
            for _ in range(100):
                if proceso.poll() is not None:
                    raise RuntimeError("El servidor Streamlit terminó antes del arranque")
                try:
                    with urllib.request.urlopen(url + "/_stcore/health", timeout=1) as respuesta:
                        if respuesta.read() == b"ok":
                            break
                except OSError:
                    pass
                time.sleep(0.2)
            else:
                raise RuntimeError("El servidor no inició dentro del plazo")
            print(json.dumps(asyncio.run(comprobar(url)), ensure_ascii=True))
        finally:
            proceso.terminate()
            try:
                proceso.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proceso.kill()
                proceso.wait(timeout=5)


if __name__ == "__main__":
    main()

