# Constitución SDD — Brújula IA Regional
Versión: 2.0.0 | Ratificación y enmienda: 2026-10-16

## I. Evidencia científicamente verificable
Toda conclusión debe distinguir observación, inferencia y propuesta, declarar fuente, periodo, cobertura, limitaciones e incertidumbre y poder reproducirse. Los faltantes no equivalen a cero. La priorización requiere metodología validada, comparabilidad territorial y temporal, explicación de criterios y sensibilidad.

## II. Trazabilidad integral
Cada requisito debe enlazar su descomposición técnica, implementación y evidencia de aceptación mediante identificadores estables. Cada resultado debe conservar su linaje hasta las fuentes y transformaciones. Ningún trabajo se declara terminado sin evidencia verificable.

## III. Gestión mediante GitHub Projects
GitHub Projects es la plataforma oficial de gestión, priorización y seguimiento. Antes de crear proyectos o issues se inspeccionan los existentes y se reutilizan los equivalentes. No se cierran issues automáticamente.

## IV. Separación de autoridades
`spec.md` es autoridad de requisitos; `tasks.md`, de descomposición técnica; GitHub Issues y Projects, de seguimiento operacional. Se mantienen enlaces bidireccionales sin duplicar las descripciones completas. Los ADR registran decisiones arquitectónicas y los planes su aplicación.

## V. Pruebas reproducibles
Toda aceptación debe especificar entradas, procedimiento y resultado esperado. Se conservan versiones, parámetros y huellas de entradas; se compara el resultado analítico, no la identidad binaria de archivos con metadatos variables. Las pruebas de interfaz no sustituyen validaciones matemáticas, estadísticas ni de calidad de datos.

## VI. Tecnología mínima suficiente
Se preserva y extiende incrementalmente lo existente. No se reescriben pipelines ni se agregan sistemas paralelos sin incompatibilidad demostrada y decisión documentada. Se separan transformación, dominio, acceso a datos y presentación; las fórmulas no residen en componentes visuales.

## VII. Privacidad y minimización
Los microdatos solo pueden tratarse transitoriamente para obtener agregados autorizados. No se publican identificadores personales ni celdas que incumplan la política de divulgación. La publicación y exportación requieren validación explícita; ausencia de política implica bloqueo, no permiso.

## VIII. Decisiones humanas y alcance
La herramienta orienta focalización y no adjudica fondos ni demuestra impacto causal. Las decisiones metodológicas, elegibilidad, alcance y divulgación se reservan a responsables humanos y se registran antes de habilitar funciones dependientes.

## Gobernanza
Esta constitución prevalece sobre los artefactos de feature. Toda enmienda registra motivo, impacto y autorización del responsable; cambia versión mayor si altera principios, menor si los amplía y parche si aclara redacción. La revisión de cada incremento comprueba estos principios y sus evidencias.

Enmienda 2.0.0 autorizada por la misión del responsable: adopta Projects, separa autoridades y elimina de la constitución cifras, tablas físicas, herramientas de prueba y umbrales metodológicos transitorios. Su diseño aplicable permanece en especificaciones y planes.
