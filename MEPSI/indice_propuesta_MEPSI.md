# Prueba 2: propuesta de diseño e implementación (índice v2)

**Título tentativo:** Diseño e implementación de un sistema automatizado para la aplicación masiva en línea de pruebas diagnósticas de selección de aspirantes a posgrado: el Manual de Evaluación Psicológica (MEPSI)

**Plaza:** Técnico Académico Titular "A", T.C., área Cómputo, registro 33709-35, DGOAE
**Límite:** 25 cuartillas **incluidos los anexos** (la portada y el índice no cuentan)
**Redacción:** primera persona ("diseñé", "desarrollé", "implementé")
**Tecnologías de la convocatoria:** Java J2EE · AngularJS · MySQL · Hibernate · Spring MVC, todas presentes en el sistema

## Estructura y presupuesto de cuartillas

| # | Sección | Cuart. | Contenido y fuente |
|---|---|---|---|
| 1 | Introducción | 1 | Problema, objetivo y alcance. MEPSI como servicio de la DGOAE a los programas de posgrado |
| 2 | Antecedentes y justificación | 1.5 | De la aplicación presencial en papel a la aplicación en línea (inicio en 2020, en pandemia). Costos, logística y errores de captura. Cifras: **31,695 aspirantes registrados de 2020 a 2026** (Q3) y decenas de programas de posgrado, de la UNAM y externos (Q4) |
| 3 | Objetivos | 0.5 | General y específicos |
| 4 | Requerimientos y actores | 2 | Actores: aspirante, coordinación del programa, DGOAE (Depto. de Instrumentos de Orientación). Requerimientos funcionales y no funcionales: concurrencia, seguridad, integridad, confidencialidad (Lineamientos de Protección de Datos Personales UNAM, 2019) |
| 5 | La batería MEPSI | 1.5 | Tabla de las 8 secciones con reactivos, tiempos y formato de respuesta; 22 escalas en 5 dimensiones (Aptitudes, Ajuste a normas sociales, Desviación de normas, Aspectos potenciadores, Aspectos limitadores) |
| 6 | Arquitectura del sistema | 2.5 | Diagrama de capas: AngularJS (SPA, ngRoute, angular-timer) → Spring MVC (controladores JSON) → servicios → Spring Data JPA + Hibernate → MySQL 5.7. GlassFish 4.1 (Java EE 7), HikariCP. Diagrama de despliegue con los procesos fuera de línea en Python |
| 7 | Diseño de la base de datos | 2.5 | Diagrama ER de las 13 tablas. Banco de reactivos parametrizable (`cat_examen` → `examen_pregunta` → `pregunta`/`opcion`). Una cadena de respuestas por sección, cuya longitud valida la integridad (Q13: 100 % de los registros tienen la longitud esperada). Volumen: ~200 mil respuestas, 31 MB (Q0) |
| 8 | Diseño e implementación de la aplicación | 3 | Backend: controladores, servicios y DAO, mapeo JPA. Frontend: módulo AngularJS. Diagramas de secuencia: (a) abrir una sección (crea `usuario_examen` y aleatoriza opciones), (b) guardar respuestas (idempotente; P-II A intercala dos renglones) y (c) comprobante PDF con QR (iText) |
| 9 | Seguridad | 1.5 | Spring Security (BCrypt, roles, `@PreAuthorize`), bloqueo tras 10 intentos fallidos, reCAPTCHA, máximo 2 sesiones, aleatorización de opciones, aviso de privacidad, acceso a la BD solo por túnel SSH |
| 10 | Ciclo de operación: alta, aplicación y calificación | 3 | **Flujo completo:** (1) el programa llena el formato Excel (hoja "registrar"); (2) un script en Python valida, cifra la contraseña con BCrypt y da de alta usuario, rol y datos por túnel SSH; (3) aplicación en línea; (4) extracción de `usuario_procesa_datos`; (5) calificación en Python: claves de respuesta, escalas, **puntuación T = 50 + 15·z** con normas por programa (31 grupos normativos) y rangos de interpretación; (6) reporte individual con combinación de correspondencia en Word y separación de PDFs por aspirante y carpeta. Diagrama de actividades |
| 11 | Aplicación masiva: operación y escalabilidad | 1.5 | Picos medidos: **1,704 aspirantes en un día** (14-abr-2026) y **1,664 en una hora** (Q10 y Q11). El 75 % de la actividad ocurre entre las 9 y las 13 h (Q12). Pool de conexiones (30) frente a `max_connections` (1,200), recursos estáticos, contingencias y reanudación |
| 12 | Resultados | 1 | Más de 26 mil aplicaciones; **98.3 a 99.7 % de baterías completas** por año (Q7); duración promedio de 112 min (Q9); tiempos reales por sección frente a los límites (Q8) |
| 13 | Plan de implementación | 1 | Metodología incremental, fases y Gantt (análisis, diseño, construcción, piloto, liberación, operación) |
| 14 | Mejoras propuestas | 1 | Validación con catálogos en la carga (los datos muestran texto libre: 30+ variantes de "sexo", fechas de nacimiento imposibles, nacionalidades duplicadas); módulo administrativo de periodos y programas; calificación integrada al sistema; secretos fuera del código; bitácora |
| 15 | Conclusiones | 0.5 | |
| — | Referencias | 0.5 | |
| A | Anexos | 1 | Diccionario de datos resumido y lista de endpoints |
| | **Total** | **25** | |

## Datos clave obtenidos de las consultas (14-oct-2026)
- **Registrados por año:** 2020: 1,706 · 2021: 5,290 · 2022: 4,047 · 2023: 5,412 · 2024: 5,737 · 2025: 4,913 · 2026: 4,590
- **Secciones:** entre 26,462 y 26,727 registros de respuesta; conclusión de 99.9 a 100 %
- **Tiempo promedio por sección (min):** P1A 4.4 · P1B 31.3 · P2A 5.9 · P2B 9.6 · P2C 14.5 · P3A 12.7 · P3B 10.9 · P3C 8.4
- **Servidor:** MySQL 5.7.31, charset latin1, max_connections 1,200; GlassFish 4.1
- Las secciones 1 y 2 no tienen reactivos en la BD porque se sirven como imágenes (P1SA*/P1SB*).

## Pendientes / por confirmar
1. ¿Desde qué año opera MEPSI y para qué entidades? Infiero que los primeros registros son de **nov-2020** y que atiende a programas de posgrado UNAM (Unidad de Posgrado) y externos (UAEM, HIMFG). ¿Es correcto?
2. ¿Cómo se llena `usuario_procesa_datos`? ¿Hay un procedimiento o consulta que concatene las 8 cadenas? No está en la carpeta `evaluacion`.
3. Los picos de 3,000 envíos en 10 minutos a horas inusuales (p. ej. 2021-08-19 23:50) parecen **cargas o migraciones masivas**, no aplicaciones reales. ¿Lo confirmas?
4. ¿El reporte individual se genera siempre con la combinación de correspondencia en Word (`MEPSI_CORRESPONDECIA INTERPRETACION.docx`) y después con `ordernar_separar.py`?
