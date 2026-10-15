-- =====================================================================
-- PROUNAM II e INVOCA (Portal OAE, poe_2022: Spring MVC + JPA + AngularJS)
-- Consultas de SOLO LECTURA para la Prueba 1 (y para la Prueba 3)
-- Esquema: portaloae · Compatibles con MySQL 5.7 (sin funciones de ventana)
--
-- Sugerencia: guardar cada resultado como CSV en COA\PROUNAM\consultas\
-- con el nombre de la consulta (p01.csv, p02.csv, ...).
-- =====================================================================


-- P01. Volumen de la base de datos (filas y tamaño por tabla)
SELECT table_name AS tabla, table_rows AS filas_aprox,
       ROUND((data_length + index_length)/1024/1024, 2) AS tamano_mb
FROM   information_schema.tables
WHERE  table_schema = DATABASE()
ORDER  BY (data_length + index_length) DESC;


-- P02. Catálogo de exámenes, partes y secciones con reactivos y opciones
SELECT ce.id_examen, ce.c_nombreExamen,
       cp.id_parte, cp.c_nombreParte,
       cs.id_seccion, cs.c_nombreSeccion,
       COUNT(DISTINCT ep.id_examen_pregunta) AS reactivos,
       COUNT(o.id_opcion)                    AS opciones
FROM   examen_pregunta ep
JOIN   cat_examen ce ON ce.id_examen  = ep.id_examen
JOIN   cat_parte  cp ON cp.id_parte   = ep.id_parte
JOIN   cat_seccion cs ON cs.id_seccion = ep.id_seccion
LEFT JOIN opcion o ON o.id_examen_pregunta = ep.id_examen_pregunta
GROUP  BY ce.id_examen, ce.c_nombreExamen, cp.id_parte, cp.c_nombreParte, cs.id_seccion, cs.c_nombreSeccion
ORDER  BY ce.id_examen, cp.id_parte, cs.id_seccion;


-- P03. Escalas de resultado (PROUNAM, INVOCA, Herrera y Montes)
SELECT 'PROUNAM' AS instrumento, id_rslt_prounam AS id, c_acronimo, c_nombre_resultado, b_status FROM cat_resultado_prounam
UNION ALL
SELECT 'INVOCA', id_rslt_invoca, c_acronimo, c_nombre_resultado, b_status FROM cat_resultado_invoca
UNION ALL
SELECT 'HyM', id_cat_hym, c_acronimo, c_nombre_resultado, b_status FROM cat_resultado_herreraymontes;


-- P04. Usuarios por rol y estatus
SELECT r.c_nombreRol, u.b_status, COUNT(*) AS usuarios
FROM   usuario u
JOIN   usuario_rol ur ON ur.id_usuario = u.id_usuario
JOIN   cat_rol r      ON r.id_rol      = ur.id_rol
GROUP  BY r.c_nombreRol, u.b_status
ORDER  BY r.c_nombreRol, u.b_status;


-- P05. Cuentas creadas por año (autorregistro y altas)
SELECT YEAR(d_creacion) AS anio, COUNT(*) AS cuentas_creadas
FROM   usuario
GROUP  BY YEAR(d_creacion)
ORDER  BY anio;


-- P06. Alumnos UNAM vs. otras instituciones
SELECT uda.b_isUnam, COUNT(*) AS alumnos
FROM   usuario_datos_academicos uda
GROUP  BY uda.b_isUnam;


-- P07. Alumnos por escuela/plantel (UNAM)
SELECT ef.id_cvefac, ef.c_nombreEscFac, COUNT(*) AS alumnos
FROM   usuario_datos_academicos uda
JOIN   carrera_facultad cf      ON cf.id_carr_escfac = uda.id_carr_escfac
JOIN   cat_escuela_facultad ef  ON ef.id_cvefac      = cf.id_cvefac
GROUP  BY ef.id_cvefac, ef.c_nombreEscFac
ORDER  BY alumnos DESC;


-- P08. Perfil: género y edad al registro
SELECT YEAR(udp.d_creacion) AS anio, udp.c_genero,
       COUNT(*) AS alumnos,
       ROUND(AVG(TIMESTAMPDIFF(YEAR, udp.d_fechaNacimiento, udp.d_creacion)), 1) AS edad_prom
FROM   usuario_datos_personales udp
GROUP  BY YEAR(udp.d_creacion), udp.c_genero
ORDER  BY anio, udp.c_genero;


-- P09. Aplicaciones calificadas por año e instrumento
--      (alumnos distintos con resultados; base para la cobertura histórica)
SELECT YEAR(d_aplicacion) AS anio, 'PROUNAM' AS instrumento, COUNT(DISTINCT id_usuario) AS alumnos
FROM   usuario_resultado_prounam GROUP BY YEAR(d_aplicacion)
UNION ALL
SELECT YEAR(d_aplicacion), 'INVOCA', COUNT(DISTINCT id_usuario)
FROM   usuario_resultado_invoca GROUP BY YEAR(d_aplicacion)
UNION ALL
SELECT YEAR(d_aplicacion), 'HyM', COUNT(DISTINCT id_usuario)
FROM   usuario_resultado_hym GROUP BY YEAR(d_aplicacion)
ORDER  BY anio, instrumento;


-- P10. Aplicación en línea vs. carga masiva (lectura óptica / CSV) por año.
--      En línea = el alumno tiene secciones abiertas en usuario_examen.
SELECT YEAR(urp.d_aplicacion) AS anio,
       SUM(ue.id_usuario IS NOT NULL) AS en_linea,
       SUM(ue.id_usuario IS NULL)     AS carga_masiva
FROM  (SELECT id_usuario, MIN(d_aplicacion) AS d_aplicacion
       FROM usuario_resultado_prounam GROUP BY id_usuario) urp
LEFT JOIN (SELECT DISTINCT id_usuario FROM usuario_examen) ue ON ue.id_usuario = urp.id_usuario
GROUP  BY YEAR(urp.d_aplicacion)
ORDER  BY anio;


-- P11. Avance por sección: abiertas vs. con respuestas guardadas
SELECT ue.id_examen, ue.id_parte, ue.id_seccion, cs.c_nombreSeccion,
       COUNT(DISTINCT ue.id_usuario_examen)  AS secciones_abiertas,
       COUNT(DISTINCT urr.id_usuario_examen) AS con_respuesta,
       ROUND(100 * COUNT(DISTINCT urr.id_usuario_examen) / COUNT(DISTINCT ue.id_usuario_examen), 1) AS pct
FROM   usuario_examen ue
JOIN   cat_seccion cs ON cs.id_seccion = ue.id_seccion
LEFT JOIN usuario_respuesta_renglon urr ON urr.id_usuario_examen = ue.id_usuario_examen
GROUP  BY ue.id_examen, ue.id_parte, ue.id_seccion, cs.c_nombreSeccion
ORDER  BY ue.id_examen, ue.id_parte, ue.id_seccion;


-- P12. Tiempo real por sección (minutos de apertura a envío)
SELECT ue.id_examen, ue.id_seccion, cs.c_nombreSeccion, COUNT(*) AS casos,
       ROUND(AVG(TIMESTAMPDIFF(SECOND, ue.d_creacion, urr.d_creacion))/60, 1) AS min_prom,
       ROUND(MAX(TIMESTAMPDIFF(SECOND, ue.d_creacion, urr.d_creacion))/60, 1) AS min_max
FROM   usuario_examen ue
JOIN   usuario_respuesta_renglon urr ON urr.id_usuario_examen = ue.id_usuario_examen
JOIN   cat_seccion cs ON cs.id_seccion = ue.id_seccion
WHERE  TIMESTAMPDIFF(MINUTE, ue.d_creacion, urr.d_creacion) BETWEEN 0 AND 240
GROUP  BY ue.id_examen, ue.id_seccion, cs.c_nombreSeccion
ORDER  BY ue.id_examen, ue.id_seccion;


-- P13. Batería completa por año (alumnos con todas las secciones del
--      PROUNAM y del INVOCA contestadas en línea)
SELECT anio,
       COUNT(*)                         AS alumnos_en_linea,
       SUM(sec_prounam >= 10)           AS prounam_completo,
       SUM(sec_invoca >= 1)             AS invoca_completo
FROM (
  SELECT ue.id_usuario, YEAR(MIN(ue.d_creacion)) AS anio,
         COUNT(DISTINCT CASE WHEN ue.id_examen = 1 AND urr.id_usuario_examen IS NOT NULL THEN ue.id_seccion END) AS sec_prounam,
         COUNT(DISTINCT CASE WHEN ue.id_examen = 2 AND urr.id_usuario_examen IS NOT NULL THEN ue.id_seccion END) AS sec_invoca
  FROM   usuario_examen ue
  LEFT JOIN usuario_respuesta_renglon urr ON urr.id_usuario_examen = ue.id_usuario_examen
  GROUP  BY ue.id_usuario
) t
GROUP BY anio ORDER BY anio;
-- Nota: si el PROUNAM tiene un número de secciones distinto de 10,
-- ajusta el ">= 10" con el resultado de P02.


-- P14. Días de mayor actividad (alumnos que abrieron secciones)
SELECT DATE(d_creacion) AS fecha, COUNT(DISTINCT id_usuario) AS alumnos
FROM   usuario_examen
GROUP  BY DATE(d_creacion)
ORDER  BY alumnos DESC
LIMIT  30;


-- P15. Picos por hora y por ventana de 10 minutos
SELECT DATE_FORMAT(d_creacion, '%Y-%m-%d %H:00') AS hora,
       COUNT(DISTINCT id_usuario) AS alumnos, COUNT(*) AS secciones_abiertas
FROM   usuario_examen
GROUP  BY hora ORDER BY alumnos DESC LIMIT 20;

SELECT CONCAT(DATE_FORMAT(d_creacion, '%Y-%m-%d %H:'),
              LPAD(FLOOR(MINUTE(d_creacion)/10)*10, 2, '0')) AS ventana_10min,
       COUNT(*) AS envios
FROM   usuario_respuesta_renglon
GROUP  BY ventana_10min ORDER BY envios DESC LIMIT 20;


-- P16. Distribución por hora del día
SELECT HOUR(d_creacion) AS hora, COUNT(DISTINCT id_usuario) AS alumnos
FROM   usuario_examen
GROUP  BY HOUR(d_creacion) ORDER BY hora;


-- P17. Consulta de resultados por los alumnos (lecturas, descargas, correos)
SELECT COUNT(*)              AS alumnos_con_bitacora,
       SUM(n_lectura > 0)    AS consultaron_en_pantalla,
       SUM(n_descarga > 0)   AS descargaron_pdf,
       SUM(n_correo > 0)     AS pidieron_correo,
       SUM(n_lectura)        AS total_lecturas,
       SUM(n_descarga)       AS total_descargas,
       SUM(n_correo)         AS total_correos
FROM   alumno_bitacora_resultados;


-- P18. Uso del módulo de orientadores
SELECT YEAR(d_creacion) AS anio,
       COUNT(DISTINCT id_usuario_orientador) AS orientadores_activos,
       COUNT(DISTINCT id_usuario_alumno)     AS alumnos_consultados,
       COUNT(*)                              AS consultas
FROM   orientador_bitacora
GROUP  BY YEAR(d_creacion) ORDER BY anio;


-- P19. Códigos de acceso generados por periodo
SELECT n_year, n_month, COUNT(*) AS codigos
FROM   cat_codigo
GROUP  BY n_year, n_month ORDER BY n_year, n_month;


-- P20. Cuestionario sociodemográfico contestado
SELECT COUNT(*) AS alumnos_con_sociodemografico FROM usuario_sociodemografico_renglon;


-- P21. Estadísticos de puntuaciones estandarizadas por escala
--      (insumo para la Prueba 3; NO incluye datos personales)
SELECT 'PROUNAM' AS instrumento, c.c_acronimo, c.c_nombre_resultado,
       COUNT(*) AS n, ROUND(AVG(t.n_valor), 2) AS media, ROUND(STDDEV(t.n_valor), 2) AS de,
       ROUND(MIN(t.n_valor), 1) AS minimo, ROUND(MAX(t.n_valor), 1) AS maximo
FROM   usuario_tt_prounam t JOIN cat_resultado_prounam c ON c.id_rslt_prounam = t.id_rslt_prounam
GROUP  BY c.c_acronimo, c.c_nombre_resultado
UNION ALL
SELECT 'INVOCA', c.c_acronimo, c.c_nombre_resultado,
       COUNT(*), ROUND(AVG(t.n_valor), 2), ROUND(STDDEV(t.n_valor), 2),
       ROUND(MIN(t.n_valor), 1), ROUND(MAX(t.n_valor), 1)
FROM   usuario_tt_invoca t JOIN cat_resultado_invoca c ON c.id_rslt_invoca = t.id_rslt_invoca
GROUP  BY c.c_acronimo, c.c_nombre_resultado;


-- P22. Catálogo de orientación: carreras con perfil de aptitudes/intereses
SELECT (SELECT COUNT(*) FROM cat_carrera WHERE b_status = 1)      AS carreras_activas,
       (SELECT COUNT(DISTINCT id_carrera) FROM carrera_aptitudes) AS carreras_con_aptitudes,
       (SELECT COUNT(DISTINCT id_carrera) FROM carrera_intereses) AS carreras_con_intereses,
       (SELECT COUNT(*) FROM norma_prounam WHERE b_status = 1)    AS normas_prounam_activas,
       (SELECT COUNT(*) FROM norma_invoca  WHERE b_status = 1)    AS normas_invoca_activas;


-- P23. Bitácora de administración (operaciones por tipo)
SELECT c_operacion, COUNT(*) AS operaciones
FROM   admin_bitacora GROUP BY c_operacion ORDER BY operaciones DESC;


-- P24. Versión del motor
SELECT VERSION() AS version_mysql, @@character_set_database AS charset, @@max_connections AS max_conexiones;
