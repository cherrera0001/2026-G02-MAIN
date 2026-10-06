-- Modelo relacional de Brújula IA Regional (DuckDB).
-- La base se reconstruye completa desde data/raw con src/pipeline/construir_bd.py;
-- este archivo es la única definición de la estructura.
--
-- Capas:
--   gob   gobierno de datos: catálogo de fuentes, lotes de carga y controles de calidad
--   core  modelo relacional normalizado (lo que se consulta y se cruza)
--   mart  vistas agregadas que consume la API
-- Los microdatos (mrun, fecha de nacimiento, edad) solo existen en tablas temporales
-- durante la carga: ninguna tabla persistente los contiene.
-- DuckDB no admite llaves foráneas entre esquemas: las referencias de core hacia gob
-- (id_carga, id_fuente) van anotadas como comentario «-> gob.x» y las verifica un
-- control de calidad.

CREATE SCHEMA IF NOT EXISTS gob;
CREATE SCHEMA IF NOT EXISTS core;
CREATE SCHEMA IF NOT EXISTS mart;

-- ---------------------------------------------------------------- gob --

CREATE TABLE gob.fuente (
    id_fuente                 VARCHAR PRIMARY KEY,
    nombre                    VARCHAR NOT NULL,
    organismo                 VARCHAR NOT NULL,
    url                       VARCHAR NOT NULL,
    licencia                  VARCHAR,
    unidad_territorial        VARCHAR,
    contiene_datos_personales BOOLEAN NOT NULL,
    notas                     VARCHAR
);

CREATE TABLE gob.carga (
    id_carga       INTEGER PRIMARY KEY,
    id_fuente      VARCHAR NOT NULL REFERENCES gob.fuente (id_fuente),
    archivo       VARCHAR NOT NULL,
    sha256         VARCHAR NOT NULL,
    periodo        INTEGER,
    filas_leidas   BIGINT NOT NULL,
    fecha_carga    TIMESTAMP NOT NULL
);

CREATE TABLE gob.control_calidad (
    regla       VARCHAR PRIMARY KEY,
    descripcion VARCHAR NOT NULL,
    valor       DOUBLE,
    umbral      VARCHAR,
    cumple      BOOLEAN NOT NULL,
    detalle     VARCHAR
);

-- --------------------------------------------------------- territorio --

CREATE TABLE core.region (
    cod_region     INTEGER PRIMARY KEY,          -- código oficial (1 a 16)
    nombre         VARCHAR NOT NULL UNIQUE,      -- nombre oficial, según la capa del Geoportal
    nombre_mineduc VARCHAR NOT NULL UNIQUE       -- como aparece en region_sede de titulados
);

CREATE TABLE core.comuna (
    id_comuna   INTEGER PRIMARY KEY,
    cod_cut     INTEGER UNIQUE,                  -- código único territorial; nulo si la comuna no está en la capa geo
    nombre      VARCHAR NOT NULL,
    nombre_norm VARCHAR NOT NULL UNIQUE,         -- mayúsculas sin tildes: llave de cruce entre fuentes
    provincia   VARCHAR,
    cod_region  INTEGER NOT NULL REFERENCES core.region (cod_region)
);

-- -------------------------------------------------------------- oferta --

CREATE TABLE core.institucion (
    cod_inst    INTEGER PRIMARY KEY,             -- código SIES de la institución
    nombre      VARCHAR NOT NULL,
    tipo_inst_1 VARCHAR,                         -- Universidades / Institutos Profesionales / CFT
    tipo_inst_2 VARCHAR,
    tipo_inst_3 VARCHAR
);

CREATE TABLE core.sede (
    cod_inst  INTEGER NOT NULL REFERENCES core.institucion (cod_inst),
    cod_sede  INTEGER NOT NULL,                  -- solo es único dentro de la institución
    nombre    VARCHAR NOT NULL,
    id_comuna INTEGER NOT NULL REFERENCES core.comuna (id_comuna),
    PRIMARY KEY (cod_inst, cod_sede)
);

-- Punto georreferenciado de un inmueble. La capa no trae cod_sede: se relaciona
-- con la oferta por institución y comuna.
CREATE TABLE core.inmueble (
    id_inmueble INTEGER PRIMARY KEY,
    cod_inst    INTEGER NOT NULL REFERENCES core.institucion (cod_inst),
    nombre      VARCHAR,
    id_comuna   INTEGER NOT NULL REFERENCES core.comuna (id_comuna),
    direccion   VARCHAR,
    latitud     DOUBLE NOT NULL,
    longitud    DOUBLE NOT NULL,
    anio        INTEGER
);

CREATE TABLE core.nivel_carrera (
    id_nivel       INTEGER PRIMARY KEY,
    nombre         VARCHAR NOT NULL UNIQUE,      -- nivel_carrera_1
    grupo          VARCHAR,                      -- nivel_carrera_2
    nivel_global   VARCHAR NOT NULL,             -- Pregrado / Posgrado / Postítulo
    -- ¿El nivel termina en memoria o tesis? 'pendiente' = decisión abierta del equipo.
    elegible_tesis VARCHAR NOT NULL CHECK (elegible_tesis IN ('si', 'no', 'pendiente'))
);

-- La «carrera» comparable entre instituciones (285 valores frente a 5.598 nombres de carrera).
CREATE TABLE core.area_generica (
    id_area_generica INTEGER PRIMARY KEY,
    nombre           VARCHAR NOT NULL UNIQUE
);

-- Un programa es la combinación institución + sede + carrera + jornada + versión
-- que identifica el código SIES. Sus atributos dependen solo de ese código.
CREATE TABLE core.programa (
    cod_programa      VARCHAR PRIMARY KEY,       -- cod_sies_obt_tit
    cod_inst          INTEGER NOT NULL,
    cod_sede          INTEGER NOT NULL,
    cod_carrera       INTEGER,                   -- nulo en parte de los programas de la fuente (sin dato; no se imputa)
    nombre_carrera    VARCHAR NOT NULL,
    id_nivel          INTEGER NOT NULL REFERENCES core.nivel_carrera (id_nivel),
    id_area_generica  INTEGER NOT NULL REFERENCES core.area_generica (id_area_generica),
    area_conocimiento VARCHAR,
    cine_f_13_area    VARCHAR,
    cine_f_13_subarea VARCHAR,
    jornada           VARCHAR,
    modalidad         VARCHAR,                   -- 'No Presencial': la región de la sede no indica dónde vive la persona
    tipo_plan         VARCHAR,
    duracion_sem      INTEGER,
    FOREIGN KEY (cod_inst, cod_sede) REFERENCES core.sede (cod_inst, cod_sede)
);

-- Hecho: títulos obtenidos. Grano = periodo × programa × género. Sin personas.
CREATE TABLE core.titulacion (
    periodo      INTEGER NOT NULL,
    cod_programa VARCHAR NOT NULL REFERENCES core.programa (cod_programa),
    genero       INTEGER NOT NULL,               -- código gen_alu de Mineduc (1 o 2; ver diccionario de la fuente)
    n_titulos    INTEGER NOT NULL CHECK (n_titulos > 0),
    id_carga     INTEGER NOT NULL,  -- -> gob.carga
    PRIMARY KEY (periodo, cod_programa, genero)
);

-- ------------------------------------------- demanda y vínculo (vacías) --
-- Estructura definida; se pueblan cuando el equipo acepte las fuentes externas.

CREATE TABLE core.sector (
    id_sector     INTEGER PRIMARY KEY,
    codigo        VARCHAR NOT NULL,
    nombre        VARCHAR NOT NULL,
    clasificacion VARCHAR NOT NULL,              -- por ejemplo 'CIIU4.CL'
    UNIQUE (clasificacion, codigo)
);

CREATE TABLE core.indicador (
    id_indicador   VARCHAR PRIMARY KEY,
    nombre         VARCHAR NOT NULL,
    definicion     VARCHAR NOT NULL,
    unidad         VARCHAR,
    id_fuente      VARCHAR NOT NULL,  -- -> gob.fuente
    -- Toda cifra declara su naturaleza: no se mezclan datos con inferencias.
    tipo_evidencia VARCHAR NOT NULL CHECK (tipo_evidencia IN ('observado', 'inferido', 'propuesto'))
);

-- Demanda laboral, peso productivo o prioridad estratégica de un sector en una región.
CREATE TABLE core.indicador_region_sector (
    id_indicador VARCHAR NOT NULL REFERENCES core.indicador (id_indicador),
    cod_region   INTEGER NOT NULL REFERENCES core.region (cod_region),
    id_sector    INTEGER NOT NULL REFERENCES core.sector (id_sector),
    periodo      INTEGER NOT NULL,
    valor        DOUBLE,                         -- nulo = sin dato; nunca se imputa
    id_carga     INTEGER NOT NULL,  -- -> gob.carga
    PRIMARY KEY (id_indicador, cod_region, id_sector, periodo)
);

-- Exposición o complementariedad con IA de un área de formación.
CREATE TABLE core.indicador_area (
    id_indicador     VARCHAR NOT NULL REFERENCES core.indicador (id_indicador),
    id_area_generica INTEGER NOT NULL REFERENCES core.area_generica (id_area_generica),
    valor            DOUBLE,
    id_carga         INTEGER NOT NULL,  -- -> gob.carga
    PRIMARY KEY (id_indicador, id_area_generica)
);

-- Puente carrera–sector. Cada vínculo guarda cómo se obtuvo y si una persona lo revisó.
CREATE TABLE core.vinculo_area_sector (
    id_area_generica INTEGER NOT NULL REFERENCES core.area_generica (id_area_generica),
    id_sector        INTEGER NOT NULL REFERENCES core.sector (id_sector),
    puntaje          DOUBLE NOT NULL CHECK (puntaje BETWEEN 0 AND 1),
    metodo           VARCHAR NOT NULL CHECK (metodo IN ('manual', 'semantico')),
    estado           VARCHAR NOT NULL CHECK (estado IN ('sugerido', 'revisado', 'rechazado')),
    justificacion    VARCHAR,
    PRIMARY KEY (id_area_generica, id_sector)
);

-- ------------------------------------------------------------ ranking --

CREATE TABLE core.criterio (
    id_criterio VARCHAR PRIMARY KEY,
    nombre      VARCHAR NOT NULL,
    descripcion VARCHAR NOT NULL,
    sentido     VARCHAR NOT NULL CHECK (sentido IN ('mayor_es_mejor', 'menor_es_mejor'))
);

CREATE TABLE core.escenario (
    id_escenario INTEGER PRIMARY KEY,
    nombre       VARCHAR NOT NULL UNIQUE,
    descripcion  VARCHAR,
    es_base      BOOLEAN NOT NULL DEFAULT FALSE
);

-- Los pesos de un escenario suman 1 (lo valida la capa de servicios al guardar).
CREATE TABLE core.peso (
    id_escenario INTEGER NOT NULL REFERENCES core.escenario (id_escenario),
    id_criterio  VARCHAR NOT NULL REFERENCES core.criterio (id_criterio),
    peso         DOUBLE NOT NULL CHECK (peso BETWEEN 0 AND 1),
    PRIMARY KEY (id_escenario, id_criterio)
);

-- --------------------------------------------------------------- mart --

-- Oferta en la unidad del MVP: región × área genérica × institución, por nivel y periodo.
CREATE VIEW mart.oferta AS
SELECT t.periodo,
       r.cod_region,
       r.nombre            AS region,
       a.id_area_generica,
       a.nombre            AS area_generica,
       i.cod_inst,
       i.nombre            AS institucion,
       i.tipo_inst_1,
       n.nombre            AS nivel,
       n.elegible_tesis,
       p.modalidad,
       SUM(t.n_titulos)    AS n_titulos
FROM core.titulacion t
JOIN core.programa p      USING (cod_programa)
JOIN core.sede s          USING (cod_inst, cod_sede)
JOIN core.comuna c        USING (id_comuna)
JOIN core.region r        USING (cod_region)
JOIN core.institucion i   USING (cod_inst)
JOIN core.area_generica a USING (id_area_generica)
JOIN core.nivel_carrera n USING (id_nivel)
GROUP BY ALL;

-- Cociente de especialización: participación del área en la región dividida por su
-- participación en el país. Mayor que 1 = la región forma más de esa área que el promedio.
-- Corrige el sesgo de volumen de la Región Metropolitana.
CREATE VIEW mart.especializacion AS
WITH ra AS (
    SELECT periodo, cod_region, region, id_area_generica, area_generica, SUM(n_titulos) AS n
    FROM mart.oferta
    GROUP BY ALL
)
SELECT periodo, cod_region, region, id_area_generica, area_generica,
       n AS n_titulos,
       (n / SUM(n) OVER (PARTITION BY periodo, cod_region))
         / (SUM(n) OVER (PARTITION BY periodo, id_area_generica) / SUM(n) OVER (PARTITION BY periodo))
         AS cociente_especializacion
FROM ra;

-- Puntos para el mapa, con los títulos de la institución en esa comuna.
CREATE VIEW mart.sedes_geo AS
WITH oferta_inst_comuna AS (
    SELECT t.periodo, p.cod_inst, s.id_comuna, SUM(t.n_titulos) AS n_titulos
    FROM core.titulacion t
    JOIN core.programa p USING (cod_programa)
    JOIN core.sede s     USING (cod_inst, cod_sede)
    GROUP BY ALL
)
SELECT m.id_inmueble, m.cod_inst, i.nombre AS institucion, i.tipo_inst_1,
       m.nombre AS inmueble, c.nombre AS comuna, r.cod_region, r.nombre AS region,
       m.latitud, m.longitud, o.periodo,
       o.n_titulos AS n_titulos_inst_comuna   -- total de la institución en la comuna, no del inmueble
FROM core.inmueble m
JOIN core.institucion i USING (cod_inst)
JOIN core.comuna c      USING (id_comuna)
JOIN core.region r      USING (cod_region)
LEFT JOIN oferta_inst_comuna o USING (cod_inst, id_comuna);
