# Prueba 1: propuesta de diseño e implementación (índice v2)

**Título tentativo:** Diseño e implementación de un sistema automatizado para la aplicación masiva en línea de pruebas de orientación académico-vocacional en el bachillerato: PROUNAM II e INVOCA en el Portal de Orientación (POE)

**Plaza:** Técnico Académico Titular "A", T.C., área Cómputo, registro 33709-35, DGOAE
**Límite:** 25 cuartillas incluidos los anexos · primera persona · mismo formato que la prueba 2 (Carta, Arial 12, interlineado 1.5, márgenes de 2.5 cm)
**Sistema:** `D:\DGOAE\proyectos\poe\poe_2022` (Portal OAE: Spring MVC 4 + Spring Data JPA/Hibernate + AngularJS + MySQL, Java EE 7), desplegado en **el mismo servidor GlassFish 4.1 que MEPSI**

## Qué lo distingue de MEPSI (para no repetir la prueba 2)
| Aspecto | MEPSI (prueba 2) | PROUNAM / INVOCA (prueba 1) |
|---|---|---|
| Población | Cientos o miles por jornada, de posgrado | Generaciones completas de ENP y CCH (decenas de miles) |
| Modelo de aplicación (desde 2020) | Jornadas acordadas con cada programa | **Dos periodos masivos al año** (ENE-FEB: 2.º año del CCH, 5 planteles, ~3 semanas; OCT-NOV: ENP, 9 planteles, ~3 semanas) **+ aplicación bajo demanda todo el año** (el orientador habilita al alumno con el código del mes) |
| Alta | Script de Python desde Excel | **Autorregistro** con confirmación por correo + carga masiva de archivos |
| Acceso | Usuario y contraseña | Usuario + **código de acceso mensual** (`cat_codigo`: un código por mes y año; al validarlo se registra el permiso en `usuario_examen_permisos`) |
| Calificación | Fuera de línea (Python) | **Dentro del sistema**: aciertos → normas (media 50, DE 15) → índices compuestos |
| Resultado | PDF para el comité | **Reporte al alumno** (pantalla, PDF, correo) + **sugerencia de carreras** (aptitudes × intereses) |
| Roles | Aspirante | Alumno, **orientador** (por plantel), administrador, tester |
| Modelo de aplicación | Solo en línea | Transición: hasta 2019 en papel con lectura óptica (resultados cargados al portal con `ProunamMasivoService`); **desde 2020, solo en línea** |
| Pruebas de carga | No documentadas | **JMeter con 700 usuarios concurrentes** (`jmeter/POEMeter.jmx`) |
| Origen | Sistema específico | Concebido como **portal único de instrumentos de orientación**; en la práctica se consolidó con PROUNAM e INVOCA, y después se construyó MEPSI aparte |

## Estructura y presupuesto de cuartillas

| # | Sección | Cuart. | Contenido y fuente |
|---|---|---|---|
| 1 | Introducción | 1 | La orientación vocacional en el bachillerato UNAM; PROUNAM II (aptitudes) e INVOCA (intereses); objetivo y alcance |
| 2 | Antecedentes y justificación | 2 | Historia (adaptación del DAT en 1993-94, PROUNAM II e INVOCA en 2002-03 en la DGOSE) y aplicaciones masivas en papel: 11 a 13 mil exámenes por año en ENP y CCH, 250 a 370 grupos, 450 a 680 aplicadores, asistencia de 57 a 78 % (manual de certificación). **La última aplicación en papel fue en 2019; desde entonces solo es en línea.** Visión original de portal único de instrumentos. Datos de P05, P09 y P10 |
| 3 | Objetivos | 0.5 | General y específicos |
| 4 | Requerimientos y actores | 2 | Alumno, orientador, administrador. RF: autorregistro, datos personales, académicos y domiciliares, aviso de privacidad, código de acceso, 10 subpruebas cronometradas + INVOCA, recuperación de sección, calificación, reporte, sugerencia de carreras, sociodemográfico. RNF: decenas de miles de alumnos por periodo, menores de edad (datos sensibles), disponibilidad |
| 5 | La batería | 1.5 | Tabla de las subpruebas del PROUNAM II: verbal (40 / 20 min), numérica (30 / 25), razonamiento abstracto (30 / 15), mecánica (32 / 10), ensamble de formas (30 / 7), discriminación de figuras (45 / 3), reconocimiento de palabras (45 / 3), criptogramas (45 / 3), uso del lenguaje (40 / 20)… (confirmar con P02). INVOCA: 14 escalas de interés. Potencial académico e índices compuestos |
| 6 | Arquitectura | 2.5 | Capas MVC (como MEPSI) + elementos nuevos: eventos de Spring y `TaskExecutor` asíncrono para correos, Spring Session, servicios de estadísticas, módulos por rol. Diagrama de componentes por módulo (alumno, orientador, administración, público) |
| 7 | Base de datos | 3 | Unas 70 tablas en 5 grupos: usuarios y perfil; banco de reactivos (examen, parte, sección); aplicación y respuestas (`usuario_examen`, `usuario_respuesta_renglon`); resultados (crudos → `usuario_tt_*` estandarizados → `*_historico`); orientación (catálogo de carreras, áreas, aptitudes e intereses por carrera, normas). Diagrama ER por grupos |
| 8 | Diseño de la aplicación | 3 | Flujo del alumno: registro, confirmación, datos, código, instrucciones, subprueba con cronómetro y guardado por renglón. **Calificación automática:** `sumaAciertos` → `sumaPAyVP` (potencial académico y velocidad perceptual) → `calificaPROUNAM`/`calificaINVOCA` con normas → `UsuarioTt*`. **Sugerencia de carreras:** las 3 aptitudes y los 3 intereses más altos, cruzados con los perfiles de carrera y ordenados por suma y por distancia. Diagramas de secuencia y fragmentos de código |
| 9 | Seguridad y protección de datos | 1.5 | Código de acceso mensual entregado por el orientador (control de quién presenta la prueba); roles (ALUMNO, ORIENTADOR, ADMIN_*, TESTER), BCrypt, bloqueo tras 10 intentos, reCAPTCHA (4 intentos en 4 h), una sola sesión por usuario, migración de sesión, HSTS, aviso de privacidad con aceptación registrada, bitácoras de administración y de orientadores. Datos de menores de edad |
| 10 | Aplicación masiva y escalabilidad | 2 | Picos reales (P14 a P16), pool de HikariCP y executor (30), **calendario de aplicación: dos periodos masivos (CCH en enero y febrero, 5 planteles; ENP en octubre y noviembre, 9 planteles; unas 3 semanas cada uno) y aplicación bajo demanda el resto del año**; pruebas de carga con JMeter con 700 usuarios concurrentes, servidor compartido con MEPSI, **módulo «recupera»**: al principio la prueba era continua y no se separaba por subpruebas, así que si el alumno no terminaba el mismo día, al volver solo veía las subpruebas que le faltaban. Carga de resultados de lectura óptica como mecanismo de migración del histórico en papel |
| 11 | Módulos de orientador y administración | 1.5 | Los orientadores (de la DGOAE y de los planteles de bachillerato de la UNAM) consultan a los alumnos de su plantel, califica, descarga o envía PDF y compara aptitudes contra intereses. El administrador gestiona usuarios, carga archivos masivos, borra o reinicia pruebas, corrige datos y consulta estadísticas por año, trimestre, nivel y plantel |
| 12 | Resultados | 1 | Cobertura por año, porcentaje en línea frente a carga masiva, conclusión, consulta de resultados por los alumnos (P17) y uso por orientadores (P18) |
| 13 | Plan de implementación | 1 | Fases, piloto por plantel, pruebas de carga y Gantt |
| 14 | Mejoras propuestas | 1 | Cola de calificación, caché del catálogo de carreras, CSRF, UTF-8, tablero para orientadores, analítica (enlace con la prueba 3) |
| 15 | Conclusiones | 0.5 | |
| — | Referencias | 0.5 | |
| A | Anexos | 1 | Diccionario de datos resumido y servicios expuestos |
| | **Total** | **25** | |

## Respuestas de Xavier (14-oct-2026)
1. Última aplicación en papel: 2019. Desde entonces, solo en línea.
2. Mismo servidor GlassFish 4.1 que MEPSI.
3. Enfoque en PROUNAM e INVOCA; Herrera y Montes, talleres y eventos se mencionan en una línea. El portal se pensó para alojar todos los instrumentos, pero se quedó con PROUNAM e INVOCA, y MEPSI se hizo después.
4. Códigos de acceso: hay un código por mes y año (`cat_codigo`). **El orientador se lo da al alumno que acude a pedir asesoría**, así que el acceso a la prueba queda ligado al proceso de orientación y no es libre.
5. Orientadores: los de la DGOAE y los de los bachilleratos de la UNAM.
6. «Recupera»: al principio la prueba era continua; si el alumno no la terminaba el mismo día, al volver se le mostraban solo las subpruebas pendientes.
7. JMeter: 700 usuarios concurrentes.
8. Hay un informe con cifras por ciclo, pero por ahora no está disponible; se usarán las consultas.
9. Modelo de aplicación desde 2020, con dos modalidades: **(a) masiva**, en dos periodos al año: enero y febrero para el 2.º año del CCH (5 planteles, unas 3 semanas) y octubre y noviembre para la ENP (9 planteles, unas 3 semanas); **(b) bajo demanda**, cuando el alumno pide asesoría y el orientador le indica que puede presentar la prueba y le da el código del mes.

## Pendiente
- Resultados de las consultas P01 a P24 (CSV en `COA\PROUNAM\consultas`).
- (Opcional) El informe con cifras por ciclo, cuando lo tengas.
