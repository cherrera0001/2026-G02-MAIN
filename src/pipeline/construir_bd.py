"""Reconstruye data/processed/brujula.duckdb desde los archivos de data/.

Uso:  uv run python -m src.pipeline.construir_bd

La base se borra y se vuelve a crear en cada ejecución: no hay estado que
mantener a mano. La estructura sale de db/schema.sql. Los microdatos de
titulados solo pasan por tablas temporales; lo que queda en disco es agregado.
"""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path

import duckdb
from dbfread import DBF

RAIZ = Path(__file__).resolve().parents[2]
RAW = RAIZ / "data" / "raw"
BD = RAIZ / "data" / "processed" / "brujula.duckdb"
ESQUEMA = RAIZ / "db" / "schema.sql"

FUENTES = [
    ("mineduc_titulados", "Titulados en educación superior", "Mineduc",
     "https://datosabiertos.mineduc.cl/titulados-en-educacion-superior/", None, "sede (región, provincia, comuna)", True,
     "Una fila por título obtenido. Trae mrun enmascarado, fecha de nacimiento y género: solo se persisten conteos."),
    ("geoportal_ies", "Establecimientos de educación superior", "IDE Chile",
     "https://www.geoportal.cl/geoportal/catalog/download/0dde8427-113a-356a-bace-ed4d51ddcb05", "CC-BY", "punto (lat, lon)", False,
     "Capa de 2020. No trae código de sede: se cruza por institución y comuna."),
    ("ckan_instalaciones", "Categoría geoespacial: instalaciones y edificaciones", "IDE Chile",
     "https://datos.gob.cl/api/3/action/package_show?id=categoria-geoespacial-instalaciones-y-edificaciones", "CC-BY", "punto", False,
     "Catálogo de 7 capas de servicios públicos. Aún no se carga."),
    ("mop_infraestructura", "Infraestructura MOP", "Ministerio de Obras Públicas",
     "https://geomop.mop.gob.cl/descargas/", None, "línea / punto", False,
     "Red vial, puentes, puertos y aeropuertos. Aún no se carga."),
]

# Código oficial -> nombre usado por Mineduc en region_sede.
REGIONES_MINEDUC = {
    1: "Tarapacá", 2: "Antofagasta", 3: "Atacama", 4: "Coquimbo", 5: "Valparaíso",
    6: "Lib. Gral. B. O'Higgins", 7: "Maule", 8: "Biobío", 9: "La Araucanía", 10: "Los Lagos",
    11: "Aysén", 12: "Magallanes", 13: "Metropolitana", 14: "Los Ríos", 15: "Arica y Parinacota", 16: "Ñuble",
}

# Propuesta inicial; los niveles 'pendiente' son una decisión abierta del equipo.
ELEGIBLE_TESIS = {
    "Profesional Con Licenciatura": "si",
    "Magister": "si",
    "Doctorado": "si",
    "Diplomado (desde un semestre)": "no",
    "Postítulo": "no",
}


def sha256(ruta: Path) -> str:
    h = hashlib.sha256()
    with ruta.open("rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def extraer_rar(rar: Path, destino: Path) -> None:
    candidatos = [
        ("unrar", ["x", "-o+", "-idq"]),
        (r"C:\Program Files\WinRAR\UnRAR.exe", ["x", "-o+", "-idq"]),
        ("7z", ["x", "-y", "-bso0"]),
        (r"C:\Program Files\7-Zip\7z.exe", ["x", "-y", "-bso0"]),
    ]
    for exe, args in candidatos:
        ruta = shutil.which(exe) or (exe if Path(exe).is_file() else None)
        if not ruta:
            continue
        salida = [f"-o{destino}"] if "7z" in Path(ruta).name.lower() else [f"{destino}{'/' if not str(destino).endswith(('/', chr(92))) else ''}"]
        subprocess.run([ruta, *args, str(rar), *salida], check=True)
        return
    sys.exit(f"No se encontró unrar ni 7-Zip para extraer {rar.name}. Instala uno o extrae el archivo a {destino}.")


def preparar_raw() -> tuple[list[Path], Path]:
    """Extrae los comprimidos del repositorio a data/raw si aún no están."""
    oferta, geo = RAW / "oferta", RAW / "geo"
    oferta.mkdir(parents=True, exist_ok=True)
    geo.mkdir(parents=True, exist_ok=True)
    for rar in sorted((RAIZ / "data" / "oferta").glob("*.rar")):
        marca = oferta / f".{rar.stem}.extraido"
        if not marca.exists():
            print(f"Extrayendo {rar.name} ...")
            extraer_rar(rar, oferta)
            marca.touch()
    if not list(geo.glob("*.dbf")):
        for z in (RAIZ / "data" / "geo").glob("*.zip"):
            zipfile.ZipFile(z).extractall(geo)
    csvs, dbfs = sorted(oferta.glob("*.csv")), sorted(geo.glob("*.dbf"))
    if not csvs or not dbfs:
        sys.exit("Faltan datos en data/raw (se esperaba al menos un CSV de titulados y un DBF de sedes).")
    return csvs, dbfs[0]


def cargar_staging(con: duckdb.DuckDBPyConnection, csvs: list[Path], dbf: Path) -> None:
    lista = ", ".join(f"'{c.as_posix()}'" for c in csvs)
    con.execute(f"""
        CREATE TEMP TABLE stg_tit AS
        SELECT * REPLACE (upper(strip_accents(trim(comuna_sede))) AS comuna_sede),
               trim(comuna_sede) AS comuna_original,
               parse_filename(filename) AS archivo
        FROM read_csv([{lista}], delim=';', header=true, all_varchar=true, union_by_name=true, filename=true)
    """)
    con.execute("""
        CREATE TEMP TABLE stg_geo (anio INTEGER, cod_inst INTEGER, tipo_inst VARCHAR, nombre_inst VARCHAR,
            nombre_inmueble VARCHAR, cod_region INTEGER, region VARCHAR, cod_provincia INTEGER, provincia VARCHAR,
            cod_comuna INTEGER, comuna VARCHAR, direccion VARCHAR, numero INTEGER, referencia VARCHAR,
            latitud DOUBLE, longitud DOUBLE)
    """)
    # Los nombres de campo del DBF llevan tildes y Ñ: se leen por posición.
    filas = [list(r.values()) for r in DBF(dbf, encoding="utf-8")]
    con.executemany(f"INSERT INTO stg_geo VALUES ({', '.join('?' * 16)})", filas)


def poblar(con: duckdb.DuckDBPyConnection, csvs: list[Path], dbf: Path) -> None:
    con.executemany("INSERT INTO gob.fuente VALUES (?, ?, ?, ?, ?, ?, ?, ?)", FUENTES)

    ahora = datetime.now()
    cargas = [(i, "mineduc_titulados", c.name, sha256(c)) for i, c in enumerate(csvs, start=1)]
    for id_carga, fuente, archivo, hash_ in cargas:
        periodo, filas = con.execute(
            "SELECT min(cat_periodo)::INTEGER, count(*) FROM stg_tit WHERE archivo = ?", [archivo]).fetchone()
        con.execute("INSERT INTO gob.carga VALUES (?, ?, ?, ?, ?, ?, ?)",
                    [id_carga, fuente, archivo, hash_, periodo, filas, ahora])
    id_geo = len(cargas) + 1
    con.execute("INSERT INTO gob.carga VALUES (?, 'geoportal_ies', ?, ?, (SELECT min(anio) FROM stg_geo), (SELECT count(*) FROM stg_geo), ?)",
                [id_geo, dbf.name, sha256(dbf), ahora])

    con.executemany(
        "INSERT INTO core.region SELECT ?, (SELECT any_value(region) FROM stg_geo WHERE cod_region = ?), ?",
        [(cod, cod, nombre) for cod, nombre in REGIONES_MINEDUC.items()])

    con.execute("""
        INSERT INTO core.comuna
        WITH tit AS (
            SELECT DISTINCT comuna_sede AS nombre_norm, comuna_original AS nombre, provincia_sede AS provincia, r.cod_region
            FROM stg_tit JOIN core.region r ON r.nombre_mineduc = region_sede
        ), geo AS (
            SELECT DISTINCT upper(strip_accents(trim(comuna))) AS nombre_norm, comuna AS nombre, provincia, cod_region, cod_comuna
            FROM stg_geo
        )
        SELECT row_number() OVER (ORDER BY nombre_norm), any_value(geo.cod_comuna),
               coalesce(any_value(geo.nombre), any_value(tit.nombre)), nombre_norm,
               coalesce(any_value(geo.provincia), any_value(tit.provincia)),
               coalesce(any_value(geo.cod_region), any_value(tit.cod_region))
        FROM tit FULL JOIN geo USING (nombre_norm)
        GROUP BY nombre_norm
    """)

    # Unos pocos códigos traen más de un nombre o tipo: se conserva el más frecuente.
    con.execute("""
        INSERT INTO core.institucion
        SELECT cod_inst::INTEGER, mode(nomb_inst), mode(tipo_inst_1), mode(tipo_inst_2), mode(tipo_inst_3)
        FROM stg_tit GROUP BY 1
    """)
    con.execute("""
        INSERT INTO core.institucion
        SELECT cod_inst, mode(nombre_inst), NULL, mode(tipo_inst), NULL
        FROM stg_geo WHERE cod_inst NOT IN (SELECT cod_inst FROM core.institucion) GROUP BY 1
    """)
    con.execute("""
        INSERT INTO core.sede
        SELECT cod_inst::INTEGER, cod_sede::INTEGER, mode(nomb_sede), any_value(c.id_comuna)
        FROM stg_tit JOIN core.comuna c ON c.nombre_norm = comuna_sede GROUP BY 1, 2
    """)
    con.execute("""
        INSERT INTO core.inmueble
        SELECT row_number() OVER (ORDER BY g.cod_inst, g.cod_comuna, g.nombre_inmueble, g.latitud, g.longitud),
               g.cod_inst, g.nombre_inmueble, c.id_comuna,
               nullif(trim(concat_ws(' ', g.direccion, nullif(g.numero, 0)::VARCHAR)), ''), g.latitud, g.longitud, g.anio
        FROM stg_geo g JOIN core.comuna c ON c.cod_cut = g.cod_comuna
    """)

    con.execute("CREATE TEMP TABLE elegible (nombre VARCHAR, valor VARCHAR)")
    con.executemany("INSERT INTO elegible VALUES (?, ?)", list(ELEGIBLE_TESIS.items()))
    con.execute("""
        INSERT INTO core.nivel_carrera
        SELECT row_number() OVER (ORDER BY nivel_carrera_1), nivel_carrera_1, any_value(nivel_carrera_2),
               any_value(nivel_global), coalesce(any_value(e.valor), 'pendiente')
        FROM stg_tit LEFT JOIN elegible e ON e.nombre = nivel_carrera_1 GROUP BY nivel_carrera_1
    """)
    con.execute("""
        INSERT INTO core.area_generica
        SELECT row_number() OVER (ORDER BY area_generica), area_generica FROM (SELECT DISTINCT area_generica FROM stg_tit)
    """)
    con.execute("""
        INSERT INTO core.programa
        SELECT cod_sies_obt_tit, cod_inst::INTEGER, cod_sede::INTEGER, cod_carrera::INTEGER, nomb_carrera,
               n.id_nivel, a.id_area_generica, area_conocimiento, cine_f_13_area, cine_f_13_subarea,
               jornada, modalidad, tipo_plan_carr, try_cast(dur_total_carr AS INTEGER)
        FROM stg_tit s
        JOIN core.nivel_carrera n ON n.nombre = s.nivel_carrera_1
        JOIN core.area_generica a ON a.nombre = s.area_generica
        QUALIFY row_number() OVER (PARTITION BY cod_sies_obt_tit ORDER BY cat_periodo DESC) = 1
    """)
    con.execute("""
        INSERT INTO core.titulacion
        SELECT s.cat_periodo::INTEGER, s.cod_sies_obt_tit, s.gen_alu::INTEGER, count(*), c.id_carga
        FROM stg_tit s JOIN gob.carga c ON c.archivo = s.archivo
        GROUP BY ALL
    """)


def controles(con: duckdb.DuckDBPyConnection) -> bool:
    """Registra los controles de calidad en gob.control_calidad. Devuelve False si falla uno bloqueante."""
    reglas = [
        ("titulos_conservados", "Títulos en core.titulacion / filas leídas de titulados", "= 1",
         "SELECT (SELECT sum(n_titulos) FROM core.titulacion) / (SELECT sum(filas_leidas) FROM gob.carga WHERE id_fuente = 'mineduc_titulados')",
         lambda v: v == 1, True),
        ("regiones", "Regiones con titulados", "= 16",
         "SELECT count(DISTINCT cod_region) FROM mart.oferta", lambda v: v == 16, True),
        ("sin_datos_personales", "Columnas persistentes con identificadores o fechas de nacimiento", "= 0",
         "SELECT count(*) FROM information_schema.columns WHERE table_schema IN ('gob','core','mart') AND (column_name ILIKE '%mrun%' OR column_name ILIKE '%nac%' OR column_name ILIKE '%edad%')",
         lambda v: v == 0, True),
        ("inmuebles_cargados", "Inmuebles cargados / filas de la capa geo", "= 1",
         "SELECT (SELECT count(*) FROM core.inmueble) / (SELECT filas_leidas FROM gob.carga WHERE id_fuente = 'geoportal_ies')",
         lambda v: v == 1, True),
        ("cargas_huerfanas", "Filas de core.titulacion cuyo id_carga no existe en gob.carga", "= 0",
         "SELECT count(*) FROM core.titulacion t WHERE NOT EXISTS (SELECT 1 FROM gob.carga c WHERE c.id_carga = t.id_carga)",
         lambda v: v == 0, True),
        ("comunas_sin_cut", "Comunas con titulados que no están en la capa geo (sin código territorial)", "informativo",
         "SELECT count(*) FROM core.comuna WHERE cod_cut IS NULL", lambda v: True, False),
        ("titulos_con_punto", "Proporción de títulos presenciales o semipresenciales cuya institución tiene un inmueble en la comuna", ">= 0.95",
         """SELECT sum(n_titulos) FILTER (WHERE EXISTS (SELECT 1 FROM core.inmueble m WHERE m.cod_inst = s.cod_inst AND m.id_comuna = s.id_comuna)) / sum(n_titulos)
            FROM core.titulacion t JOIN core.programa p USING (cod_programa) JOIN core.sede s USING (cod_inst, cod_sede)
            WHERE p.modalidad <> 'No Presencial'""",
         lambda v: v >= 0.95, False),
        ("niveles_pendientes", "Proporción de títulos en niveles con elegibilidad de tesis pendiente de decisión", "informativo",
         "SELECT sum(n_titulos) FILTER (WHERE elegible_tesis = 'pendiente') / sum(n_titulos) FROM mart.oferta", lambda v: True, False),
    ]
    ok = True
    for regla, descripcion, umbral, sql, prueba, bloquea in reglas:
        valor = con.execute(sql).fetchone()[0]
        valor = float(valor) if valor is not None else None
        cumple = valor is not None and prueba(valor)
        con.execute("INSERT INTO gob.control_calidad VALUES (?, ?, ?, ?, ?, ?)",
                    [regla, descripcion, valor, umbral, cumple, "bloqueante" if bloquea else "advertencia"])
        ok = ok and (cumple or not bloquea)
        print(f"  [{'ok' if cumple else 'FALLA' if bloquea else 'aviso'}] {regla}: {valor:.4g} (esperado {umbral})")
    return ok


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    csvs, dbf = preparar_raw()
    BD.parent.mkdir(parents=True, exist_ok=True)
    temporal = BD.with_suffix(".tmp.duckdb")
    temporal.unlink(missing_ok=True)

    con = duckdb.connect(str(temporal))
    con.execute(ESQUEMA.read_text(encoding="utf-8"))
    cargar_staging(con, csvs, dbf)
    poblar(con, csvs, dbf)
    print("Controles de calidad:")
    ok = controles(con)
    for tabla in ("region", "comuna", "institucion", "sede", "inmueble", "nivel_carrera", "area_generica", "programa", "titulacion"):
        print(f"  core.{tabla}: {con.execute(f'SELECT count(*) FROM core.{tabla}').fetchone()[0]} filas")
    con.close()

    if not ok:
        sys.exit(f"Un control bloqueante falló; la base anterior no se reemplazó. Revisa {temporal}.")
    temporal.replace(BD)
    print(f"Base lista: {BD.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
