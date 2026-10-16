# Contrato de datos y servicios — SDD-006
No se modifica `db/schema.sql`. La futura UI lee una base previamente validada en modo read_only; nunca importa ni invoca el pipeline.

## Oferta y filtros
`consultar_oferta(periodo, regiones, instituciones, areas)` consume `mart.oferta`; IDs estables: cod_region, cod_inst, id_area_generica. Retorna filas agregadas y total de n_titulos al mismo grano/filtro. Los selectores se obtienen de dimensiones y del corte, usando parámetros SQL, sin concatenar entradas. No se incluye género en exportaciones por defecto.

## Mapa
`consultar_mapa(periodo, regiones, instituciones)` consume `mart.sedes_geo`. `n_titulos_inst_comuna` se repite en múltiples inmuebles: no se suma entre puntos. NULL es ausencia de correspondencia, no cero. La vista no tiene carrera: al filtrar área se muestra mapa de infraestructura rotulado «sin desagregación por carrera» y tabla de oferta filtrada aparte; no se atribuyen títulos de carrera a inmuebles sin contrato de unión validado. Fechas de inmuebles se obtienen de core.inmueble y se distinguen del periodo de títulos.

## Procedencia y aptitud
`consultar_fuentes()` lee gob.fuente/gob.carga con lista explícita de columnas públicas: no expone archivo local. Retorna organismo, URL, periodo, fecha_carga y SHA-256. Fecha de publicación/licencia no comprobadas se declaran. La aplicación comprueba gob.control_calidad antes de ofrecer resultados; tablas creadas o con filas no equivalen a fuente aceptada. La aprobación de demanda requiere ficha y evidencia vinculadas a 003.

## Ranking y divulgación
`consultar_estado_ranking()` devuelve bloqueos documentados; solo una ejecución validada de 005 puede devolver resultados, pesos y contribuciones. No se crean tablas propuestas de ranking en esta misión. `preparar_exportacion()` exige política aprobada, controla lista de columnas y supresiones, devuelve agregados/metadatos o motivo de bloqueo. La misma política se aplica a consultas visibles para evitar reconstrucción mediante filtros. Ningún dato restringido entra en cachés compartidas; claves incluyen corte, filtros y versión de política.

## Errores
Base ausente/corrupta, esquema incompatible, control fallido, fuente pendiente y selección vacía son estados distintos. Se muestran mensajes sanitizados; no se ocultan fallos como conjuntos vacíos ni se crean datos de sustitución.
