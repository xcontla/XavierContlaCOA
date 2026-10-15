# Prueba 3: propuesta de análisis de datos (índice v1)

**Título tentativo:** Propuesta para el análisis de los datos generados por los sistemas PROUNAM II e INVOCA y MEPSI: de la aplicación masiva a la toma de decisiones en orientación educativa

**Límite:** 15 cuartillas incluidos los anexos · primera persona · mismo formato que las pruebas 1 y 2
**Convocatoria:** "Presentar por escrito y en un máximo de 15 cuartillas una propuesta para el análisis de datos de la información que arrojan los sistemas anteriores."

## Idea central
Ambos sistemas ya resuelven la **aplicación** y la **calificación**. Lo que falta es convertir los ~2.4 millones de puntuaciones del portal y las ~26 mil baterías de MEPSI en **conocimiento**: normas actualizadas, evidencia de calidad psicométrica, indicadores para orientadores y programas, y seguimiento de trayectorias. La propuesta parte de **hallazgos reales** que ya encontré en los datos (deriva de normas, problemas de calidad de captura, uso de resultados) para mostrar que es viable y necesaria.

## Estructura y presupuesto de cuartillas

| # | Sección | Cuart. | Contenido |
|---|---|---|---|
| 1 | Introducción y propósito | 0.5 | De sistemas transaccionales a una plataforma de análisis; quiénes usan los resultados |
| 2 | Inventario de datos | 1.5 | Tabla comparativa de las fuentes de ambos sistemas: respuestas por reactivo (cadenas), puntajes crudos y estandarizados, normas, datos sociodemográficos, bitácoras de uso y operación; volumen, granularidad, periodo y nivel de sensibilidad |
| 3 | Preguntas de análisis por actor | 1 | DGOAE (cobertura, calidad del instrumento), orientadores y planteles (perfiles de su población), programas de posgrado (perfil de aspirantes frente a la norma), investigación (validez, trayectorias) |
| 4 | Arquitectura analítica | 2 | ETL desde los dos esquemas MySQL a un almacén analítico con **modelo estrella** (hecho: puntuación por escala y aplicación; dimensiones: persona seudonimizada, tiempo, plantel o programa, escala, norma, modo de aplicación); proceso nocturno; Python (pandas, scipy, factor_analyzer) para psicometría; servicios Spring MVC y tableros AngularJS (coherente con la plataforma actual). Diagrama |
| 5 | Calidad de los datos | 1.5 | Hallazgos reales: MEPSI con 16 variantes de "sexo", fechas imposibles y 140 nacionalidades con duplicados; PROUNAM con PANT y VPNT estandarizados sin el factor de escala (valores de millones) y variantes de género. Reglas de validación, catálogos e indicadores de calidad por carga |
| 6 | Análisis descriptivo y de operación | 1.5 | Cobertura por año, plantel o programa; conclusión; tiempos frente a límites; horarios; consulta de resultados por los alumnos (61 mil, 98 mil descargas); uso por orientadores. Ejemplos con cifras reales |
| 7 | Análisis psicométrico | 2.5 | (a) **Análisis de reactivos**: dificultad y discriminación por reactivo; (b) **confiabilidad** (KR-20 o alfa) por escala y por cohorte; (c) **actualización de normas**: las medias estandarizadas del PROUNAM ya no son 50/15 (p. ej. ensamble de formas 44.8, reconocimiento de palabras 55.2, discriminación de figuras con DE de 18.9), es decir, las normas se desplazaron; (d) **equivalencia papel/línea** (2019 frente a 2020+); (e) **funcionamiento diferencial** por sexo y subsistema |
| 8 | Análisis para la orientación | 1.5 | Congruencia entre aptitudes e intereses, perfiles por conglomerados, seguimiento de las sugerencias de carrera, vínculo con la trayectoria (carrera de ingreso, egreso) para validez predictiva; en MEPSI, perfil de aspirantes por programa y relación con la decisión de admisión (con acuerdo del programa) |
| 9 | Visualización y reportes | 1 | Tableros por actor: institucional (DGOAE), plantel u orientador (heredero del "reporte para el profesor"), programa de posgrado; reporte de plantel frente a la norma |
| 10 | Ética, privacidad y gobierno de datos | 1 | Seudonimización, mínimo necesario, menores de edad, uso exclusivo para orientación (no para selección en PROUNAM), acuerdos con programas, conservación |
| 11 | Plan de trabajo | 0.5 | Fases y entregables (6 meses) |
| 12 | Conclusiones | 0.5 | |
| — | Referencias y anexo (consultas tipo) | 0.5 | |
| | **Total** | **15** | |

## Evidencia que ya tenemos
- PROUNAM, Q21: medias y DE de las puntuaciones estandarizadas por escala (n ≈ 202 mil).
- PROUNAM, Q09, Q13 a Q18: cobertura, picos, consulta de resultados, orientadores.
- MEPSI, consultas 1 a 13: cobertura, conclusión, tiempos por sección, calidad de sexo y nacionalidad.

## Lo que hace falta (consultas en `consultas_analisis.sql`)
Para que la sección 7 tenga números reales y no solo método:
- A1. Deriva de normas por año (PROUNAM).
- A2. Diferencias por sexo y subsistema (PROUNAM).
- A3. Dificultad por reactivo y KR-20 de una subprueba del PROUNAM (aptitud verbal, 2025).
- A4. Dificultad por reactivo y KR-20 de MEPSI P-II B (uso del lenguaje).
- A5. Distribución de respuestas en MEPSI P-III B (sesgos de respuesta). La comparación papel (2019) frente a línea sale de A1, por año.
- A6. Congruencia aptitud-interés (área del interés más alto frente a la aptitud más alta).

## Preguntas para Xavier
1. ¿Qué herramientas tienes disponibles o se usan en la DGOAE para análisis (Python, R, SPSS, Excel, Power BI, Tableau)? Las propondría como complemento, pero el tablero lo plantearía con el mismo stack (Spring MVC + AngularJS) por coherencia con la convocatoria.
2. ¿Conservas los Excel de resultados de MEPSI por programa (los que genera el script de calificación)? Con un par de ellos podría ilustrar el análisis de escalas de MEPSI sin tocar la base de datos.
3. ¿Existe algún vínculo, o se ha intentado, con datos de trayectoria (carrera a la que ingresó el alumno, o si el aspirante fue admitido al posgrado)? Aunque no exista, lo plantearía como línea futura.
