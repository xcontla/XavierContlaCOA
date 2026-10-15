-- =====================================================================
-- MEPSI (versión Spring MVC + Hibernate + AngularJS)
-- Consultas de SOLO LECTURA para obtener cifras de operación
-- que se usarán en la propuesta del Concurso de Oposición (prueba 2)
-- y en la propuesta de análisis de datos (prueba 3).
--
-- Tablas: usuario, usuariorol, rol, usuario_datos_alumno,
--         usuario_examen, usuario_respuesta, cat_examen,
--         examen_pregunta, pregunta, opcion
-- Secciones (cat_examen.id_examen):
--   1 = P-I  Sección A   2 = P-I  Sección B
--   3 = P-II Sección A   4 = P-II Sección B   5 = P-II Sección C
--   6 = P-III Sección A  7 = P-III Sección B  8 = P-III Sección C
--
-- Sugerencia: exportar cada resultado a CSV / Excel y enviármelo.
-- =====================================================================


-- ---------------------------------------------------------------------
-- Q0. Volumen de la base de datos (filas y tamaño por tabla)
-- ---------------------------------------------------------------------
SELECT table_name                                   AS tabla,
       table_rows                                   AS filas_aprox,
       ROUND((data_length + index_length)/1024/1024, 2) AS tamano_mb
FROM   information_schema.tables
WHERE  table_schema = DATABASE()
ORDER  BY (data_length + index_length) DESC;


-- ---------------------------------------------------------------------
-- Q1. Catálogo de secciones y número de reactivos y opciones cargados
-- ---------------------------------------------------------------------
SELECT ce.id_examen,
       ce.c_nombreExamen,
       ce.b_status,
       COUNT(DISTINCT ep.id_examen_pregunta) AS reactivos_bd,
       COUNT(o.id_opcion)                    AS opciones_bd
FROM   cat_examen ce
LEFT JOIN examen_pregunta ep ON ep.id_examen = ce.id_examen
LEFT JOIN opcion o           ON o.id_examen_pregunta = ep.id_examen_pregunta
GROUP  BY ce.id_examen, ce.c_nombreExamen, ce.b_status
ORDER  BY ce.id_examen;


-- ---------------------------------------------------------------------
-- Q2. Usuarios registrados por rol y estatus
-- ---------------------------------------------------------------------
SELECT r.c_nombreRol,
       u.b_status,
       COUNT(*) AS usuarios
FROM   usuario u
JOIN   usuariorol ur ON ur.id_usuario = u.id_usuario
JOIN   rol r         ON r.id_rol      = ur.id_rol
GROUP  BY r.c_nombreRol, u.b_status;


-- ---------------------------------------------------------------------
-- Q3. Aspirantes por año de registro (cobertura histórica)
-- ---------------------------------------------------------------------
SELECT YEAR(uda.d_creacion) AS anio,
       COUNT(*)             AS aspirantes_registrados
FROM   usuario_datos_alumno uda
GROUP  BY YEAR(uda.d_creacion)
ORDER  BY anio;


-- ---------------------------------------------------------------------
-- Q4. Aspirantes por posgrado al que desean ingresar y nivel
--     (maestría / doctorado / especialidad)
-- ---------------------------------------------------------------------
SELECT YEAR(uda.d_creacion)   AS anio,
       uda.c_nivel,
       uda.c_posgrado_ingresar,
       COUNT(*)               AS aspirantes
FROM   usuario_datos_alumno uda
GROUP  BY YEAR(uda.d_creacion), uda.c_nivel, uda.c_posgrado_ingresar
ORDER  BY anio, aspirantes DESC;


-- ---------------------------------------------------------------------
-- Q5. Perfil sociodemográfico: sexo, nacionalidad y edad al registro
-- ---------------------------------------------------------------------
SELECT YEAR(uda.d_creacion) AS anio,
       uda.c_sexo,
       COUNT(*)                                                         AS aspirantes,
       ROUND(AVG(TIMESTAMPDIFF(YEAR, uda.d_fechaNacimiento, uda.d_creacion)), 1) AS edad_promedio,
       MIN(TIMESTAMPDIFF(YEAR, uda.d_fechaNacimiento, uda.d_creacion))  AS edad_min,
       MAX(TIMESTAMPDIFF(YEAR, uda.d_fechaNacimiento, uda.d_creacion))  AS edad_max
FROM   usuario_datos_alumno uda
GROUP  BY YEAR(uda.d_creacion), uda.c_sexo
ORDER  BY anio, uda.c_sexo;

SELECT uda.c_nacionalidad, COUNT(*) AS aspirantes
FROM   usuario_datos_alumno uda
GROUP  BY uda.c_nacionalidad
ORDER  BY aspirantes DESC;


-- ---------------------------------------------------------------------
-- Q6. Avance por sección: iniciadas vs. concluidas (con respuestas)
-- ---------------------------------------------------------------------
SELECT ce.id_examen,
       ce.c_nombreExamen,
       COUNT(DISTINCT ue.id_usuario_examen)  AS secciones_iniciadas,
       COUNT(DISTINCT ur.id_usuario_examen)  AS secciones_concluidas,
       ROUND(100 * COUNT(DISTINCT ur.id_usuario_examen)
                 / NULLIF(COUNT(DISTINCT ue.id_usuario_examen), 0), 1) AS pct_conclusion
FROM   cat_examen ce
LEFT JOIN usuario_examen ue    ON ue.id_examen = ce.id_examen
LEFT JOIN usuario_respuesta ur ON ur.id_usuario_examen = ue.id_usuario_examen
GROUP  BY ce.id_examen, ce.c_nombreExamen
ORDER  BY ce.id_examen;


-- ---------------------------------------------------------------------
-- Q7. Aspirantes que completaron las 8 secciones (batería completa)
--     por año
-- ---------------------------------------------------------------------
SELECT anio,
       COUNT(*)                                  AS aspirantes_con_actividad,
       SUM(secciones_concluidas = 8)             AS bateria_completa,
       ROUND(100 * SUM(secciones_concluidas = 8) / COUNT(*), 1) AS pct_completa
FROM (
    SELECT ue.id_usuario,
           YEAR(MIN(ue.d_creacion))              AS anio,
           COUNT(DISTINCT ur.id_usuario_examen)  AS secciones_concluidas
    FROM   usuario_examen ue
    LEFT JOIN usuario_respuesta ur ON ur.id_usuario_examen = ue.id_usuario_examen
    GROUP  BY ue.id_usuario
) t
GROUP  BY anio
ORDER  BY anio;


-- ---------------------------------------------------------------------
-- Q8. Tiempo empleado por sección (minutos entre que se abre la
--     sección y se guardan las respuestas)
-- ---------------------------------------------------------------------
SELECT ce.id_examen,
       ce.c_nombreExamen,
       COUNT(*)                                                         AS casos,
       ROUND(AVG(TIMESTAMPDIFF(SECOND, ue.d_creacion, ur.d_creacion))/60, 1) AS min_promedio,
       ROUND(MIN(TIMESTAMPDIFF(SECOND, ue.d_creacion, ur.d_creacion))/60, 1) AS min_minimo,
       ROUND(MAX(TIMESTAMPDIFF(SECOND, ue.d_creacion, ur.d_creacion))/60, 1) AS min_maximo
FROM   usuario_examen ue
JOIN   usuario_respuesta ur ON ur.id_usuario_examen = ue.id_usuario_examen
JOIN   cat_examen ce        ON ce.id_examen = ue.id_examen
WHERE  TIMESTAMPDIFF(MINUTE, ue.d_creacion, ur.d_creacion) BETWEEN 0 AND 240  -- descarta atípicos
GROUP  BY ce.id_examen, ce.c_nombreExamen
ORDER  BY ce.id_examen;


-- ---------------------------------------------------------------------
-- Q9. Duración total de la aplicación por aspirante
--     (primera sección abierta -> última respuesta guardada)
-- ---------------------------------------------------------------------
SELECT ROUND(AVG(minutos), 1) AS min_promedio,
       MIN(minutos)           AS min_minimo,
       MAX(minutos)           AS min_maximo,
       COUNT(*)               AS aspirantes
FROM (
    SELECT ue.id_usuario,
           TIMESTAMPDIFF(MINUTE, MIN(ue.d_creacion), MAX(ur.d_creacion)) AS minutos
    FROM   usuario_examen ue
    JOIN   usuario_respuesta ur ON ur.id_usuario_examen = ue.id_usuario_examen
    GROUP  BY ue.id_usuario
    HAVING COUNT(DISTINCT ue.id_examen) = 8
) t
WHERE minutos BETWEEN 0 AND 600;


-- ---------------------------------------------------------------------
-- Q10. Días de aplicación: aspirantes que iniciaron por día
--      (para identificar jornadas masivas)
-- ---------------------------------------------------------------------
SELECT DATE(ue.d_creacion)         AS fecha,
       COUNT(DISTINCT ue.id_usuario) AS aspirantes_activos
FROM   usuario_examen ue
GROUP  BY DATE(ue.d_creacion)
ORDER  BY aspirantes_activos DESC
LIMIT  30;


-- ---------------------------------------------------------------------
-- Q11. Concurrencia: picos de aspirantes activos por hora y por
--      ventana de 10 minutos (dimensionamiento del servidor)
-- ---------------------------------------------------------------------
SELECT DATE_FORMAT(ue.d_creacion, '%Y-%m-%d %H:00') AS hora,
       COUNT(DISTINCT ue.id_usuario)                AS aspirantes_activos,
       COUNT(*)                                     AS secciones_abiertas
FROM   usuario_examen ue
GROUP  BY DATE_FORMAT(ue.d_creacion, '%Y-%m-%d %H:00')
ORDER  BY aspirantes_activos DESC
LIMIT  20;

SELECT CONCAT(DATE_FORMAT(ur.d_creacion, '%Y-%m-%d %H:'),
              LPAD(FLOOR(MINUTE(ur.d_creacion)/10)*10, 2, '0')) AS ventana_10min,
       COUNT(*)                                                 AS envios_respuestas
FROM   usuario_respuesta ur
GROUP  BY ventana_10min
ORDER  BY envios_respuestas DESC
LIMIT  20;


-- ---------------------------------------------------------------------
-- Q12. Distribución por hora del día (en qué horario se aplica)
-- ---------------------------------------------------------------------
SELECT HOUR(ue.d_creacion)            AS hora_del_dia,
       COUNT(DISTINCT ue.id_usuario)  AS aspirantes
FROM   usuario_examen ue
GROUP  BY HOUR(ue.d_creacion)
ORDER  BY hora_del_dia;


-- ---------------------------------------------------------------------
-- Q13. Tamaño de las cadenas de respuesta por sección
--      (verifica que el número de caracteres corresponda a reactivos;
--       P-II Sección A guarda 2 caracteres por reactivo)
-- ---------------------------------------------------------------------
SELECT ue.id_examen,
       MIN(CHAR_LENGTH(ur.c_respuesta)) AS long_min,
       ROUND(AVG(CHAR_LENGTH(ur.c_respuesta)), 1) AS long_prom,
       MAX(CHAR_LENGTH(ur.c_respuesta)) AS long_max,
       COUNT(*)                         AS registros
FROM   usuario_respuesta ur
JOIN   usuario_examen ue ON ue.id_usuario_examen = ur.id_usuario_examen
GROUP  BY ue.id_examen
ORDER  BY ue.id_examen;


-- ---------------------------------------------------------------------
-- Q14. Muestra anónima de cadenas de respuesta (5 por sección)
--      para documentar el formato de almacenamiento. SIN datos
--      personales.
-- ---------------------------------------------------------------------
SELECT ue.id_examen,
       LEFT(ur.c_respuesta, 60) AS respuesta_muestra
FROM   usuario_respuesta ur
JOIN   usuario_examen ue ON ue.id_usuario_examen = ur.id_usuario_examen
WHERE  ur.id_respuesta IN (
         SELECT id_respuesta FROM (
           SELECT ur2.id_respuesta,
                  ROW_NUMBER() OVER (PARTITION BY ue2.id_examen ORDER BY ur2.id_respuesta) AS rn
           FROM   usuario_respuesta ur2
           JOIN   usuario_examen ue2 ON ue2.id_usuario_examen = ur2.id_usuario_examen
         ) x WHERE rn <= 5)
ORDER  BY ue.id_examen;
-- Nota: ROW_NUMBER() requiere MySQL 8. Si el servidor es 5.x avísame
-- y te paso la versión alternativa.


-- ---------------------------------------------------------------------
-- Q15. Datos para el análisis (prueba 3): distribución de respuestas
--      por posición de reactivo en la P-III Sección B (escala 1-4).
--      Cambia el id_examen y la longitud para otras secciones.
-- ---------------------------------------------------------------------
SELECT n.pos                                    AS reactivo,
       SUBSTRING(ur.c_respuesta, n.pos, 1)      AS respuesta,
       COUNT(*)                                 AS frecuencia
FROM   usuario_respuesta ur
JOIN   usuario_examen ue ON ue.id_usuario_examen = ur.id_usuario_examen
JOIN  (SELECT a.N + b.N * 10 + 1 AS pos
       FROM (SELECT 0 N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4
             UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) a,
            (SELECT 0 N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4
             UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9
             UNION SELECT 10 UNION SELECT 11) b) n
       ON n.pos <= CHAR_LENGTH(ur.c_respuesta)
WHERE  ue.id_examen = 7
GROUP  BY n.pos, respuesta
ORDER  BY n.pos, respuesta;


-- ---------------------------------------------------------------------
-- Q16. Tabla de procesamiento (usuario_procesa_datos): registros
--      completos vs incompletos
-- ---------------------------------------------------------------------
SELECT YEAR(d_creacion) AS anio,
       b_completo,
       COUNT(*)         AS registros
FROM   usuario_procesa_datos
GROUP  BY YEAR(d_creacion), b_completo
ORDER  BY anio, b_completo;


-- ---------------------------------------------------------------------
-- Q17. Versión del motor (para describir la plataforma)
-- ---------------------------------------------------------------------
SELECT VERSION() AS version_mysql, @@character_set_database AS charset, @@max_connections AS max_conexiones;
