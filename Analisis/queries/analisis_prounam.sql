-- =====================================================================
-- Prueba 3 · Consultas de evidencia para la propuesta de análisis
-- SOLO LECTURA · MySQL 5.7 (sin funciones de ventana)
-- Guardar cada resultado como CSV en COA\ANALISIS\consultas\ (a1.csv, a2.csv, ...)
-- Las consultas A1, A2 y A3 van contra el esquema portaloae (PROUNAM);
-- A4 y A5 contra el esquema mepsi. A6 va contra portaloae.
-- Ninguna devuelve datos personales.
-- =====================================================================


-- ---------------------------------------------------------------------
-- A1. [portaloae] Deriva de normas: media y DE de la puntuación
--     estandarizada por escala y por año de aplicación.
--     (Si las normas estuvieran vigentes, todas rondarían 50 / 15.)
--     El filtro de rango excluye los PANT/VPNT mal escalados.
-- ---------------------------------------------------------------------
SELECT YEAR(t.d_aplicacion) AS anio, c.c_acronimo,
       COUNT(*) AS n, ROUND(AVG(t.n_valor), 2) AS media, ROUND(STDDEV_POP(t.n_valor), 2) AS de
FROM   usuario_tt_prounam t
JOIN   cat_resultado_prounam c ON c.id_rslt_prounam = t.id_rslt_prounam
WHERE  t.n_valor BETWEEN -100 AND 200
GROUP  BY YEAR(t.d_aplicacion), c.c_acronimo
UNION ALL
SELECT YEAR(t.d_aplicacion), c.c_acronimo,
       COUNT(*), ROUND(AVG(t.n_valor), 2), ROUND(STDDEV_POP(t.n_valor), 2)
FROM   usuario_tt_invoca t
JOIN   cat_resultado_invoca c ON c.id_rslt_invoca = t.id_rslt_invoca
GROUP  BY YEAR(t.d_aplicacion), c.c_acronimo
ORDER  BY 2, 1;


-- ---------------------------------------------------------------------
-- A2. [portaloae] Diferencias por subsistema (ENP / CCH) y sexo
-- ---------------------------------------------------------------------
SELECT CASE WHEN ef.c_nombreEscFac LIKE 'C.C.H.%' THEN 'CCH'
            WHEN ef.c_nombreEscFac LIKE 'E.N.P.%' THEN 'ENP' ELSE 'OTRO' END AS subsistema,
       CASE WHEN UPPER(TRIM(udp.c_genero)) LIKE 'F%' THEN 'F'
            WHEN UPPER(TRIM(udp.c_genero)) LIKE 'M%' THEN 'M' ELSE 'OTRO/ND' END AS sexo,
       c.c_acronimo,
       COUNT(*) AS n, ROUND(AVG(t.n_valor), 2) AS media, ROUND(STDDEV_POP(t.n_valor), 2) AS de
FROM   usuario_tt_prounam t
JOIN   cat_resultado_prounam c        ON c.id_rslt_prounam   = t.id_rslt_prounam
JOIN   usuario_datos_personales udp   ON udp.id_usuario      = t.id_usuario
JOIN   usuario_datos_academicos uda   ON uda.id_usuario      = t.id_usuario
JOIN   carrera_facultad cf            ON cf.id_carr_escfac   = uda.id_carr_escfac
JOIN   cat_escuela_facultad ef        ON ef.id_cvefac        = cf.id_cvefac
WHERE  t.n_valor BETWEEN -100 AND 200
GROUP  BY subsistema, sexo, c.c_acronimo
UNION ALL
SELECT CASE WHEN ef.c_nombreEscFac LIKE 'C.C.H.%' THEN 'CCH'
            WHEN ef.c_nombreEscFac LIKE 'E.N.P.%' THEN 'ENP' ELSE 'OTRO' END,
       CASE WHEN UPPER(TRIM(udp.c_genero)) LIKE 'F%' THEN 'F'
            WHEN UPPER(TRIM(udp.c_genero)) LIKE 'M%' THEN 'M' ELSE 'OTRO/ND' END,
       c.c_acronimo,
       COUNT(*), ROUND(AVG(t.n_valor), 2), ROUND(STDDEV_POP(t.n_valor), 2)
FROM   usuario_tt_invoca t
JOIN   cat_resultado_invoca c         ON c.id_rslt_invoca    = t.id_rslt_invoca
JOIN   usuario_datos_personales udp   ON udp.id_usuario      = t.id_usuario
JOIN   usuario_datos_academicos uda   ON uda.id_usuario      = t.id_usuario
JOIN   carrera_facultad cf            ON cf.id_carr_escfac   = uda.id_carr_escfac
JOIN   cat_escuela_facultad ef        ON ef.id_cvefac        = cf.id_cvefac
GROUP  BY 1, 2, 3
ORDER  BY 3, 1, 2;


-- ---------------------------------------------------------------------
-- A3. [portaloae] Análisis de reactivos y KR-20 de APTITUD VERBAL
--     (id_seccion = 5) en las aplicaciones de 2025.
--     Cambia id_seccion / año para otras subpruebas.
-- ---------------------------------------------------------------------
-- A3a. Dificultad (proporción de aciertos) por reactivo
SELECT CAST(ep.c_indice AS UNSIGNED) AS reactivo,
       COUNT(*) AS n,
       ROUND(AVG(UPPER(SUBSTRING(urr.c_respuesta_renglon, CAST(ep.c_indice AS UNSIGNED), 1))
                 = UPPER(TRIM(o.c_pos_indice))), 3) AS p_acierto
FROM   usuario_respuesta_renglon urr
JOIN   usuario_examen ue   ON ue.id_usuario_examen = urr.id_usuario_examen
                          AND ue.id_examen = 1 AND ue.id_seccion = 5
                          AND YEAR(ue.d_creacion) = 2025
JOIN   examen_pregunta ep  ON ep.id_examen = 1 AND ep.id_seccion = 5
JOIN   opcion o            ON o.id_examen_pregunta = ep.id_examen_pregunta
                          AND o.n_valor > 0 AND o.b_status = 1
GROUP  BY reactivo
ORDER  BY reactivo;

-- A3b. KR-20 = k/(k-1) * (1 - Σpq / varianza del total)
SELECT k, ROUND(sum_pq, 3) AS sum_pq, ROUND(var_total, 3) AS var_total,
       ROUND(media_total, 2) AS media_total,
       ROUND(k / (k - 1) * (1 - sum_pq / var_total), 3) AS kr20
FROM (
  SELECT COUNT(*) AS k, SUM(p * (1 - p)) AS sum_pq
  FROM (
    SELECT ep.id_examen_pregunta,
           AVG(UPPER(SUBSTRING(urr.c_respuesta_renglon, CAST(ep.c_indice AS UNSIGNED), 1))
               = UPPER(TRIM(o.c_pos_indice))) AS p
    FROM   usuario_respuesta_renglon urr
    JOIN   usuario_examen ue  ON ue.id_usuario_examen = urr.id_usuario_examen
                             AND ue.id_examen = 1 AND ue.id_seccion = 5
                             AND YEAR(ue.d_creacion) = 2025
    JOIN   examen_pregunta ep ON ep.id_examen = 1 AND ep.id_seccion = 5
    JOIN   opcion o           ON o.id_examen_pregunta = ep.id_examen_pregunta
                             AND o.n_valor > 0 AND o.b_status = 1
    GROUP  BY ep.id_examen_pregunta
  ) items
) a,
(
  SELECT VAR_POP(total) AS var_total, AVG(total) AS media_total
  FROM (
    SELECT urr.id_usuario_respuesta_renglon,
           SUM(UPPER(SUBSTRING(urr.c_respuesta_renglon, CAST(ep.c_indice AS UNSIGNED), 1))
               = UPPER(TRIM(o.c_pos_indice))) AS total
    FROM   usuario_respuesta_renglon urr
    JOIN   usuario_examen ue  ON ue.id_usuario_examen = urr.id_usuario_examen
                             AND ue.id_examen = 1 AND ue.id_seccion = 5
                             AND YEAR(ue.d_creacion) = 2025
    JOIN   examen_pregunta ep ON ep.id_examen = 1 AND ep.id_seccion = 5
    JOIN   opcion o           ON o.id_examen_pregunta = ep.id_examen_pregunta
                             AND o.n_valor > 0 AND o.b_status = 1
    GROUP  BY urr.id_usuario_respuesta_renglon
  ) t
) b;




-- ---------------------------------------------------------------------
-- A6. [portaloae] Congruencia aptitud-interés (aplicaciones de 2025):
--     cruce entre la aptitud más alta y el interés más alto de cada alumno.
-- ---------------------------------------------------------------------
SELECT ap.c_acronimo AS aptitud_mas_alta, it.c_acronimo AS interes_mas_alto, COUNT(*) AS alumnos
FROM (
  SELECT t.id_usuario, MIN(c.c_acronimo) AS c_acronimo
  FROM   usuario_tt_prounam t
  JOIN   cat_resultado_prounam c ON c.id_rslt_prounam = t.id_rslt_prounam
  JOIN  (SELECT id_usuario, MAX(n_valor) AS mx
         FROM usuario_tt_prounam
         WHERE id_rslt_prounam <= 9 AND YEAR(d_aplicacion) = 2025
         GROUP BY id_usuario) m ON m.id_usuario = t.id_usuario AND m.mx = t.n_valor
  WHERE  t.id_rslt_prounam <= 9 AND YEAR(t.d_aplicacion) = 2025
  GROUP  BY t.id_usuario
) ap
JOIN (
  SELECT t.id_usuario, MIN(c.c_acronimo) AS c_acronimo
  FROM   usuario_tt_invoca t
  JOIN   cat_resultado_invoca c ON c.id_rslt_invoca = t.id_rslt_invoca
  JOIN  (SELECT id_usuario, MAX(n_valor) AS mx
         FROM usuario_tt_invoca
         WHERE YEAR(d_aplicacion) = 2025
         GROUP BY id_usuario) m ON m.id_usuario = t.id_usuario AND m.mx = t.n_valor
  WHERE  YEAR(t.d_aplicacion) = 2025
  GROUP  BY t.id_usuario
) it ON it.id_usuario = ap.id_usuario
GROUP  BY ap.c_acronimo, it.c_acronimo
ORDER  BY alumnos DESC;
