
-- ---------------------------------------------------------------------
-- A4. [mepsi] Reactivos y KR-20 de P-II B (uso del lenguaje, 24 reactivos)
--     y de P-I B (razonamiento abstracto, 36 reactivos).
--     Claves tomadas de los scripts de calificación de la DGOAE.
-- ---------------------------------------------------------------------
-- Tabla de números 1..40 (reutilizable)
-- A4a. Dificultad por reactivo, P-II B
SELECT n.pos AS reactivo, COUNT(*) AS n_casos,
       ROUND(AVG(SUBSTRING(ur.c_respuesta, n.pos, 1) = SUBSTRING('DCBEDCCAEEBEBDCCCADAADDD', n.pos, 1)), 3) AS p_acierto
FROM   usuario_respuesta ur
JOIN   usuario_examen ue ON ue.id_usuario_examen = ur.id_usuario_examen AND ue.id_examen = 4
JOIN  (SELECT a.N + b.N * 10 + 1 AS pos
       FROM (SELECT 0 N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4
             UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) a,
            (SELECT 0 N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3) b) n
       ON n.pos <= 24
WHERE  CHAR_LENGTH(ur.c_respuesta) = 24
GROUP  BY n.pos ORDER BY n.pos;

-- A4b. KR-20 de P-II B (id_examen 4, 24 reactivos) y P-I B (id_examen 2, 36 reactivos)
SELECT seccion, k, ROUND(sum_pq, 3) AS sum_pq, ROUND(var_total, 3) AS var_total,
       ROUND(media_total, 2) AS media_total,
       ROUND(k / (k - 1) * (1 - sum_pq / var_total), 3) AS kr20
FROM (
  SELECT 'P-II B' AS seccion, COUNT(*) AS k, SUM(p * (1 - p)) AS sum_pq
  FROM (SELECT n.pos, AVG(SUBSTRING(ur.c_respuesta, n.pos, 1) = SUBSTRING('DCBEDCCAEEBEBDCCCADAADDD', n.pos, 1)) AS p
        FROM usuario_respuesta ur
        JOIN usuario_examen ue ON ue.id_usuario_examen = ur.id_usuario_examen AND ue.id_examen = 4
        JOIN (SELECT a.N + b.N * 10 + 1 AS pos FROM
               (SELECT 0 N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) a,
               (SELECT 0 N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3) b) n ON n.pos <= 24
        WHERE CHAR_LENGTH(ur.c_respuesta) = 24
        GROUP BY n.pos) i
) x
JOIN (
  SELECT 'P-II B' AS seccion, VAR_POP(total) AS var_total, AVG(total) AS media_total
  FROM (SELECT ur.id_respuesta,
               SUM(SUBSTRING(ur.c_respuesta, n.pos, 1) = SUBSTRING('DCBEDCCAEEBEBDCCCADAADDD', n.pos, 1)) AS total
        FROM usuario_respuesta ur
        JOIN usuario_examen ue ON ue.id_usuario_examen = ur.id_usuario_examen AND ue.id_examen = 4
        JOIN (SELECT a.N + b.N * 10 + 1 AS pos FROM
               (SELECT 0 N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) a,
               (SELECT 0 N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3) b) n ON n.pos <= 24
        WHERE CHAR_LENGTH(ur.c_respuesta) = 24
        GROUP BY ur.id_respuesta) t
) y USING (seccion)
UNION ALL
SELECT seccion, k, ROUND(sum_pq, 3), ROUND(var_total, 3), ROUND(media_total, 2),
       ROUND(k / (k - 1) * (1 - sum_pq / var_total), 3)
FROM (
  SELECT 'P-I B' AS seccion, COUNT(*) AS k, SUM(p * (1 - p)) AS sum_pq
  FROM (SELECT n.pos, AVG(SUBSTRING(ur.c_respuesta, n.pos, 1) = SUBSTRING('517431618456212467388763727565485132', n.pos, 1)) AS p
        FROM usuario_respuesta ur
        JOIN usuario_examen ue ON ue.id_usuario_examen = ur.id_usuario_examen AND ue.id_examen = 2
        JOIN (SELECT a.N + b.N * 10 + 1 AS pos FROM
               (SELECT 0 N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) a,
               (SELECT 0 N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3) b) n ON n.pos <= 36
        WHERE CHAR_LENGTH(ur.c_respuesta) = 36
        GROUP BY n.pos) i
) x2
JOIN (
  SELECT 'P-I B' AS seccion, VAR_POP(total) AS var_total, AVG(total) AS media_total
  FROM (SELECT ur.id_respuesta,
               SUM(SUBSTRING(ur.c_respuesta, n.pos, 1) = SUBSTRING('517431618456212467388763727565485132', n.pos, 1)) AS total
        FROM usuario_respuesta ur
        JOIN usuario_examen ue ON ue.id_usuario_examen = ur.id_usuario_examen AND ue.id_examen = 2
        JOIN (SELECT a.N + b.N * 10 + 1 AS pos FROM
               (SELECT 0 N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) a,
               (SELECT 0 N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3) b) n ON n.pos <= 36
        WHERE CHAR_LENGTH(ur.c_respuesta) = 36
        GROUP BY ur.id_respuesta) t
) y2 USING (seccion);


-- ---------------------------------------------------------------------
-- A5. [mepsi] Distribución de respuestas en P-III B (escala 1 a 4),
--     primeros 20 reactivos: detecta respuestas sesgadas o reactivos
--     con poca variabilidad.
-- ---------------------------------------------------------------------
SELECT n.pos AS reactivo,
       SUM(SUBSTRING(ur.c_respuesta, n.pos, 1) = '1') AS r1,
       SUM(SUBSTRING(ur.c_respuesta, n.pos, 1) = '2') AS r2,
       SUM(SUBSTRING(ur.c_respuesta, n.pos, 1) = '3') AS r3,
       SUM(SUBSTRING(ur.c_respuesta, n.pos, 1) = '4') AS r4,
       SUM(SUBSTRING(ur.c_respuesta, n.pos, 1) NOT IN ('1','2','3','4')) AS otro
FROM   usuario_respuesta ur
JOIN   usuario_examen ue ON ue.id_usuario_examen = ur.id_usuario_examen AND ue.id_examen = 7
JOIN  (SELECT a.N + b.N * 10 + 1 AS pos
       FROM (SELECT 0 N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4
             UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) a,
            (SELECT 0 N UNION SELECT 1) b) n
GROUP  BY n.pos ORDER BY n.pos;