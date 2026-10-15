# Prueba 3: hallazgos preliminares de las consultas A1 a A6 (14-oct-2026)

## A1. Deriva de normas (PROUNAM e INVOCA, por año)
- Si las normas estuvieran vigentes, cada escala tendría media de ≈ 50 y DE de ≈ 15. No es así:
  - **Aptitud verbal** baja de 50.9 (2019) a **44.3** (2026).
  - **Reconocimiento de palabras**: 58 a 61 entre 2019 y 2023; baja a 51.5 en 2024 y a 47.4 en 2026.
  - **Ensamble de formas**: 37.6 a 38.0 en 2021-2022; 49 desde 2024.
  - **Discriminación de figuras**: DE de 21 a 23 hasta 2022 (debería ser 15); 14.3 desde 2024.
  - **Criptogramas**: DE de ≈ 10 hasta 2023 y ≈ 15.6 desde 2024.
  - → El salto de 2024 en DF, EF, CG y RP sugiere que **las normas se actualizaron en 2024** (por confirmar).
  - **2022** (año de transición de calendario): numérica 43.4, uso del lenguaje 43.3, potencial académico 42.9, con DE de ≈ 20; la población de ese año fue distinta.
- INVOCA, tendencia de los intereses: **ecología** baja de 55.3 a 44.9 y **biológicas** de 54.0 a 47.0; **servicio social** de 53.6 a 48.4. Hay un cambio generacional de intereses que las normas no reflejan.
- Papel (2019) frente a línea (2020): diferencias de 1 a 2 puntos en la mayoría de las escalas (AV +1.8, DF −2.2, EF −1.8, AN +1.0): no se observa un efecto fuerte del modo de aplicación.

## A2. Diferencias por sexo y subsistema (n ≈ 202 mil)
- INVOCA: diferencias grandes por sexo (≈ 0.5 a 0.9 DE): mecánico (H 58.4 frente a M 45.4), ciencias físicas (55.2 frente a 45.5), cálculo (52.8 frente a 47.5); en mujeres: artístico (54.7 frente a 46.4), servicio social (54.4 frente a 46.8), literario, ecología, biológicas y expresión oral.
- PROUNAM: aptitud mecánica (H +6), numérica (H +3 a +5), uso del lenguaje (M +5 a +6), reconocimiento de palabras (M +2).
- La ENP puntúa más alto que el CCH en casi todas las aptitudes (de +1 a +3).
- → El reporte en papel incluía **normas por sexo**; el sistema usa una sola norma. Propuesta: normas diferenciadas por sexo y por subsistema, o al menos reportar el percentil dentro del grupo.

## A3. Aptitud verbal, 2025 (n = 31,724)
- **Solo 34 de los 40 reactivos tienen una opción correcta activa** (faltan 4, 8, 11, 24, 30 y 37). ¿Son reactivos anulados o falta la clave? Si falta la clave, esos reactivos no suman a nadie. **→ Preguntar a Xavier.**
- KR-20 = **0.623** (por debajo del 0.70 reportado en el desarrollo).
- Dificultad entre 0.22 y 0.93: 5 reactivos muy fáciles (p > 0.90: 9, 19, 20, 34 y 10) y 3 muy difíciles (p < 0.35: 6, 39 y 38).

## A4. MEPSI, confiabilidad
- P-II B (uso del lenguaje, 24 reactivos): KR-20 = **0.927**; P-I B (razonamiento abstracto, 36 reactivos): KR-20 = **0.926**. Excelente.
- P-II B: dificultad de 0.42 a 0.88; ningún reactivo extremo.

## A5. MEPSI P-III B (escala de 1 a 4)
- Varios reactivos concentran más del 80 % en la categoría 4 (4, 11, 17, 19) o en la 1 (16: 79 %; 3: 70 %; 10: 68 %), lo que indica baja variabilidad o deseabilidad social. Son candidatos a revisar en un análisis factorial.

## A6. Congruencia aptitud-interés (2025)
- Las combinaciones más frecuentes son coherentes: numérica con cálculo (923), mecánica con mecánico (798), ensamble con mecánico (736), uso del lenguaje con literario (378).
- Falta el porcentaje de congruencia por área (en Python, con el mapeo de escalas a las cuatro áreas UNAM).

## Pendiente
- Carpetas `primer_analisis` (piloto en Python del PROUNAM) y `resultados_mepsi` (archivo consolidado).
- Confirmar: ¿se actualizaron las normas en 2024? ¿qué pasa con los 6 reactivos de aptitud verbal sin clave?
