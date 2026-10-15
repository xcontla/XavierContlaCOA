
# -*- coding: utf-8 -*-

"""
INTERPRETACIONES_MEPSI.py

Archivo de interpretaciones del MEPSI
Autor: Pedro Xavier Contla Romero
"""



# ==========================================================
# FUNCIONES
# ==========================================================

def normaliza_percentil(valor):

    if valor >= 100:
        return 100

    if valor <= 0:
        return 0

    return valor


def obtener_interpretacion(codigo, valor):

    valor = normaliza_percentil(valor)

    if codigo not in interpretaciones:
        return '', ''

    for item in interpretaciones[codigo]:

        if item['min'] <= valor <= item['max']:

            return item['rango'], item['interpretacion']

    return '', ''


def obtener_interpretacion_completa(codigo, valor):

    valor = normaliza_percentil(valor)

    if codigo not in interpretaciones:
        return None

    for item in interpretaciones[codigo]:

        if item['min'] <= valor <= item['max']:
            return item

    return None

def obtener_dimension(codigo):
       
    if codigo not in interpretacion_general:
        return ''
    
    return interpretacion_general[codigo]['dimension']

def obtener_subescala(codigo):
       
    if codigo not in interpretacion_general:
        return ''

    return interpretacion_general[codigo]['subescala']



interpretacion_general = {
    
    'TARAR2' : {'dimension': 'Aptitudes', 'subescala': 'Razonamiento Abstracto'},
    'TARVAN' : {'dimension': 'Aptitudes', 'subescala': 'Razonamiento Verbal'},
    'TARVUL' : {'dimension': 'Aptitudes', 'subescala': 'Uso del Lenguaje'},
    'TARVCL' : {'dimension': 'Aptitudes', 'subescala': 'Comprensión Lectora'},
    'TDCAA' : {'dimension': 'Aptitudes', 'subescala': 'Aptitud Académica'},
    'TPCSO' : {'dimension': 'Ajuste a Normas Sociales', 'subescala': 'Control Social'},
    'TPDES' : {'dimension': 'Ajuste a Normas Sociales', 'subescala': 'Deseabilidad Social'},
    'TPMEN' : {'dimension': 'Ajuste a Normas Sociales', 'subescala': 'Mentiras'},
    'TPEYN' : {'dimension': 'Ajuste a Normas Sociales', 'subescala': 'Estabilidad y Apego a Normas'},
    'TDCAS' : {'dimension': 'Ajuste a Normas Sociales', 'subescala': 'Ajuste Social'},
    'TPDPP' : {'dimension': 'Desviación de Normas', 'subescala': 'Desajuste'},
    'TPIMP' : {'dimension': 'Desviación de Normas', 'subescala': 'Impulsividad'},
    'TLDYP' : {'dimension': 'Desviación de Normas', 'subescala': 'Negativismo'},
    'TLMAQ' : {'dimension': 'Desviación de Normas', 'subescala': 'Manipula Social'},
    'TDCDS' : {'dimension': 'Desviación de Normas', 'subescala': 'Desviación Social'},
    'TMOAL' : {'dimension': 'Aspectos Potenciadores', 'subescala': 'Orientación al Logro'},
    'TMAEF' : {'dimension': 'Aspectos Potenciadores', 'subescala': 'Autoeficacia'},
    'TMMAE' : {'dimension': 'Aspectos Potenciadores', 'subescala': 'Maestría'},
    'TMLID' : {'dimension': 'Aspectos Potenciadores', 'subescala': 'Liderazgo'},
    'TMAES' : {'dimension': 'Aspectos Potenciadores', 'subescala': 'Autoestima'},
    'TDCMP' : {'dimension': 'Aspectos Potenciadores', 'subescala': 'Aspectos Potenciadores'},
    'TMTEF' : {'dimension': 'Aspectos Limitadores', 'subescala': 'Temor al Fracaso'},
    'TMETR' : {'dimension': 'Aspectos Limitadores', 'subescala': 'Evitar Trabajo Retador'},
    'TMMOR' : {'dimension': 'Aspectos Limitadores', 'subescala': 'Morosidad'},
    'TPINS' : {'dimension': 'Aspectos Limitadores', 'subescala': 'Incomodidad Social'},
    'TPINP' : {'dimension': 'Aspectos Limitadores', 'subescala': 'Inseguridad Personal'},
    'TDCML' : {'dimension': 'Aspectos Limitadores', 'subescala': 'Aspectos Limitadores'},
    
    
    
    }


interpretaciones = {

    # ==========================================================
    # APTITUDES
    # ==========================================================

    'TARAR2': [
        {
            'min': 0,
            'max': 10,
            'rango': 'Extremadamente Bajo',
            'interpretacion': 'Grandes dificultades para razonar visual y abstractamente.'
        },
        {
            'min': 11,
            'max': 25,
            'rango': 'Muy Bajo',
            'interpretacion': 'Baja capacidad para detectar patrones, relacionar eventos.'
        },
        {
            'min': 26,
            'max': 35,
            'rango': 'Bajo',
            'interpretacion': 'Limitado pensamiento abstracto.'
        },
        {
            'min': 36,
            'max': 65,
            'rango': 'Medio',
            'interpretacion': 'Capacidad funcional para razonamiento abstracto.'
        },
        {
            'min': 66,
            'max': 75,
            'rango': 'Alto',
            'interpretacion': 'Buena capacidad de pensamiento abstracto.'
        },
        {
            'min': 76,
            'max': 90,
            'rango': 'Muy Alto',
            'interpretacion': 'Alta capacidad para resolver problemas complejos.'
        },
        {
            'min': 91,
            'max': 100,
            'rango': 'Extremadamente Alto',
            'interpretacion': 'Razonamiento abstracto sobresaliente.'
        }
    ],

    'TARVAN': [
        {
            'min': 0,
            'max': 10,
            'rango': 'Extremadamente Bajo',
            'interpretacion': 'Dificultad severa para razonar con lenguaje.'
        },
        {
            'min': 11,
            'max': 25,
            'rango': 'Muy Bajo',
            'interpretacion': 'Baja habilidad verbal.'
        },
        {
            'min': 26,
            'max': 35,
            'rango': 'Bajo',
            'interpretacion': 'Limitado razonamiento verbal.'
        },
        {
            'min': 36,
            'max': 65,
            'rango': 'Medio',
            'interpretacion': 'Capacidad verbal adecuada.'
        },
        {
            'min': 66,
            'max': 75,
            'rango': 'Alto',
            'interpretacion': 'Buen uso del lenguaje para razonar.'
        },
        {
            'min': 76,
            'max': 90,
            'rango': 'Muy Alto',
            'interpretacion': 'Razonamiento verbal destacado.'
        },
        {
            'min': 91,
            'max': 100,
            'rango': 'Extremadamente Alto',
            'interpretacion': 'Habilidad verbal excepcional.'
        }
    ],

    'TARVUL': [
        {
            'min': 0,
            'max': 10,
            'rango': 'Extremadamente Bajo',
            'interpretacion': 'Manejo muy deficiente del español como lenguaje escrito.'
        },
        {
            'min': 11,
            'max': 25,
            'rango': 'Muy Bajo',
            'interpretacion': 'Dificultades relevantes para redactar y expresarse por escrito en español.'
        },
        {
            'min': 26,
            'max': 35,
            'rango': 'Bajo',
            'interpretacion': 'Errores frecuentes en escritura y redacción en español.'
        },
        {
            'min': 36,
            'max': 65,
            'rango': 'Medio',
            'interpretacion': 'Uso adecuado del lenguaje escrito y redacción en español.'
        },
        {
            'min': 66,
            'max': 75,
            'rango': 'Alto',
            'interpretacion': 'Buena capacidad de sintaxis, gramática y de redacción en español.'
        },
        {
            'min': 76,
            'max': 90,
            'rango': 'Muy Alto',
            'interpretacion': 'Dominio avanzado del lenguaje escrito y redacción en español.'
        },
        {
            'min': 91,
            'max': 100,
            'rango': 'Extremadamente Alto',
            'interpretacion': 'Excelencia para expresarse por escrito y redactar en español.'
        }
    ],

    'TARVCL': [
        {
            'min': 0,
            'max': 10,
            'rango': 'Extremadamente Bajo',
            'interpretacion': 'Graves dificultades para comprender textos.'
        },
        {
            'min': 11,
            'max': 25,
            'rango': 'Muy Bajo',
            'interpretacion': 'Comprensión de textos limitada.'
        },
        {
            'min': 26,
            'max': 35,
            'rango': 'Bajo',
            'interpretacion': 'Problemas para extraer ideas clave.'
        },
        {
            'min': 36,
            'max': 65,
            'rango': 'Medio',
            'interpretacion': 'Comprensión adecuada.'
        },
        {
            'min': 66,
            'max': 75,
            'rango': 'Alto',
            'interpretacion': 'Buena capacidad de análisis de lectura.'
        },
        {
            'min': 76,
            'max': 90,
            'rango': 'Muy Alto',
            'interpretacion': 'Lectura crítica y reflexiva.'
        },
        {
            'min': 91,
            'max': 100,
            'rango': 'Extremadamente Alto',
            'interpretacion': 'Comprensión lectora sobresaliente.'
        }
    ],
    
        
    'TDCAA': [
        {
            'min': 0,
            'max': 10,
            'rango': 'Extremadamente Bajo',
            'interpretacion': 'Presenta limitaciones significativas en habilidades cognitivas básicas. Podría no resultar un aspirante apto.'
        },
        {
            'min': 11,
            'max': 25,
            'rango': 'Muy Bajo',
            'interpretacion': 'Evidencia un nivel muy limitado de razonamiento y comprensión. Podría no resultar un aspirante apto.'
        },
        {
            'min': 26,
            'max': 35,
            'rango': 'Bajo',
            'interpretacion': 'Evidencia un nivel limitado de razonamiento y comprensión.  Podría no resultar un aspirante apto, contrastar con otras pruebas'
        },
        {
            'min': 36,
            'max': 65,
            'rango': 'Medio',
            'interpretacion': 'Presenta un nivel adecuado de aptitudes intelectuales; cuenta con los recursos necesarios para afrontar tareas académicas de posgrado.'
        },
        {
            'min': 66,
            'max': 75,
            'rango': 'Alto',
            'interpretacion': 'Denota buenas capacidades de razonamiento y comprensión; su potencial de aprendizaje es favorable.'
        },
        {
            'min': 76,
            'max': 90,
            'rango': 'Muy Alto',
            'interpretacion': 'Sobresale en habilidades cognitivas complejas; demuestra facilidad para el análisis, la síntesis y la resolución de problemas.'
        },
        {
            'min': 91,
            'max': 100,
            'rango': 'Extremadamente Alto',
            'interpretacion': 'Refleja un nivel excepcional de razonamiento y comprensión; posee un alto potencial académico y capacidad de adaptación intelectual.'
        }
    ],
    

    # ==========================================================
    # AJUSTE A NORMAS SOCIALES
    # ==========================================================

    'TPCSO': [
        {
            'min': 0,
            'max': 10,
            'rango': 'Extremadamente Bajo',
            'interpretacion': 'Desconexión con normas grupales.'
        },
        {
            'min': 11,
            'max': 25,
            'rango': 'Muy Bajo',
            'interpretacion': 'Bajo ajuste social.'
        },
        {
            'min': 26,
            'max': 35,
            'rango': 'Bajo',
            'interpretacion': 'Dificultades para adecuarse a expectativas.'
        },
        {
            'min': 36,
            'max': 65,
            'rango': 'Medio',
            'interpretacion': 'Nivel adecuado de ajuste social.'
        },
        {
            'min': 66,
            'max': 75,
            'rango': 'Alto',
            'interpretacion': 'Buena adherencia a normas.'
        },
        {
            'min': 76,
            'max': 90,
            'rango': 'Muy Alto',
            'interpretacion': 'Conformidad marcada.'
        },
        {
            'min': 91,
            'max': 100,
            'rango': 'Extremadamente Alto',
            'interpretacion': 'Posible pérdida de individualidad.'
        }
    ],
    
    
    'TPDES': [
        {
            'min': 0,
            'max': 10,
            'rango': 'Extremadamente Bajo',
            'interpretacion': 'No se preocupa por agradar'
        },
        {
            'min': 11,
            'max': 25,
            'rango': 'Muy Bajo',
            'interpretacion': 'Baja necesidad de aceptación'
        },
        {
            'min': 26,
            'max': 35,
            'rango': 'Bajo',
            'interpretacion': 'Presentación sincera.'
        },
        {
            'min': 36,
            'max': 65,
            'rango': 'Medio',
            'interpretacion': 'Presentación equilibrada.'
        },
        {
            'min': 66,
            'max': 75,
            'rango': 'Alto',
            'interpretacion': 'Busca activamente ser aceptado.'
        },
        {
            'min': 76,
            'max': 90,
            'rango': 'Muy Alto',
            'interpretacion': 'Deseabilidad elevada.'
        },
        {
            'min': 91,
            'max': 100,
            'rango': 'Extremadamente Alto',
            'interpretacion': 'Imagen posiblemente exagerada.'
        }
    ],
    
    
    
    
    
    'TPMEN': [
        {
            'min': 0,
            'max': 10,
            'rango': 'Extremadamente Bajo',
            'interpretacion': 'Alto nivel de sinceridad o baja autoestima.'
        },
        {
            'min': 11,
            'max': 25,
            'rango': 'Muy Bajo',
            'interpretacion': 'Se muestra con mucha apertura.'
        },
        {
            'min': 26,
            'max': 35,
            'rango': 'Bajo',
            'interpretacion': 'Poca distorsión de autoimagen.'
        },
        {
            'min': 36,
            'max': 65,
            'rango': 'Medio',
            'interpretacion': 'Presentación equilibrada.'
        },
        {
            'min': 66,
            'max': 75,
            'rango': 'Alto',
            'interpretacion': 'Tendencia a mostrar una mejor imagen. (Se recomienda tomar los resultados con reserva)'
        },
        {
            'min': 76,
            'max': 90,
            'rango': 'Muy Alto',
            'interpretacion': 'Posible ocultamiento de dificultades, defensivo. (Se recomienda tomar los resultados con mucha reserva)'
        },
        {
            'min': 91,
            'max': 100,
            'rango': 'Extremadamente Alto',
            'interpretacion': 'Perfil inválido o muy defensivo.'
        }
    ],
        
    
    
    'TPEYN': [
        {
            'min': 0,
            'max': 10,
            'rango': 'Extremadamente Bajo',
            'interpretacion': 'Inconstante en el seguimiento de normas.	'
        },
        {
            'min': 11,
            'max': 25,
            'rango': 'Muy Bajo',
            'interpretacion': 'Baja estructura interna.'
        },
        {
            'min': 26,
            'max': 35,
            'rango': 'Bajo',
            'interpretacion': 'Variable adherencia a reglas.'
        },
        {
            'min': 36,
            'max': 65,
            'rango': 'Medio',
            'interpretacion': 'Estabilidad normativa funcional.'
        },
        {
            'min': 66,
            'max': 75,
            'rango': 'Alto',
            'interpretacion': 'Seguimiento consistente de normas.'
        },
        {
            'min': 76,
            'max': 90,
            'rango': 'Muy Alto',
            'interpretacion': 'Alta necesidad de estructura.'
        },
        {
            'min': 91,
            'max': 100,
            'rango': 'Extremadamente Alto',
            'interpretacion': 'Rigidez en la adhesión a normas.'
        }
    ],
    
    'TDCAS': [
        {
            'min': 0,
            'max': 10,
            'rango': 'Extremadamente Bajo',
            'interpretacion': 'Muestra franca dificultad para adaptarse a las normas; puede evidenciar actitudes de rechazo o desafío a la autoridad.'
        },
        {
            'min': 11,
            'max': 25,
            'rango': 'Muy Bajo',
            'interpretacion': 'Presenta escaso ajuste social; tiende a la independencia o resistencia ante estructuras formales.'
        },
        {
            'min': 26,
            'max': 35,
            'rango': 'Bajo',
            'interpretacion': 'Se adapta parcialmente a las normas; podría cuestionar la autoridad o mostrar actitudes inconformes.'
        },
        {
            'min': 36,
            'max': 65,
            'rango': 'Medio',
            'interpretacion': 'Muestra un equilibrio entre autonomía personal y respeto a las normas; se considera un nivel funcional.'
        },
        {
            'min': 66,
            'max': 75,
            'rango': 'Alto',
            'interpretacion': 'Denota buena adaptación y cooperación en entornos normativos; responde adecuadamente a la convivencia grupal.'
        },
        {
            'min': 76,
            'max': 90,
            'rango': 'Muy Alto',
            'interpretacion': 'Refleja una marcada orientación al cumplimiento de normas y roles; podría ser algo rígido o tratando de dar buena impresión'
        },
        {
            'min': 91,
            'max': 100,
            'rango': 'Extremadamente Alto',
            'interpretacion': 'Indica una adhesión excesiva a las normas que puede traducirse en rigidez, falta de espontaneidad en contextos sociales o franca inflación de la imagen'
        }
    ],

    # ==========================================================
    # Desviación de norma
    # ==========================================================

    'TDCDS': [
        {
            'min': 0,
            'max': 10,
            'rango': 'Extremadamente Bajo',
            'interpretacion': 'Refleja un comportamiento social altamente adaptativo, con respeto por normas y límites establecidos. Podría mostrar alta conformidad social'
        },
        {
            'min': 11,
            'max': 25,
            'rango': 'Muy Bajo',
            'interpretacion': 'Denota estabilidad conductual y responsabilidad social; actúa dentro de los parámetros esperados. Podría tener cierta tendencia a la complacencia social'
        },
        {
            'min': 26,
            'max': 35,
            'rango': 'Bajo',
            'interpretacion': 'Muestra independencia y pensamiento crítico sin transgredir las normas sociales.'
        },
        {
            'min': 36,
            'max': 65,
            'rango': 'Medio',
            'interpretacion': 'Presenta autonomía moderada; puede cuestionar reglas sin manifestar conductas problemáticas.'
        },
        {
            'min': 66,
            'max': 75,
            'rango': 'Alto',
            'interpretacion': 'Sugiere cierta tendencia a la impulsividad o inconformidad frente a las normas sociales.'
        },
        {
            'min': 76,
            'max': 90,
            'rango': 'Muy Alto',
            'interpretacion': 'Indica posibles dificultades de ajuste social o comportamientos que desafían convenciones establecidas, buscando beneficio propio.'
        },
        {
            'min': 91,
            'max': 100,
            'rango': 'Extremadamente Alto',
            'interpretacion': 'Manifiesta patrones de oposición, manipulación o desajuste social marcados; puede evidenciar conflictos interpersonales.'
        }
    ],
    
    'TPDPP': [
        {
            'min': 0,
            'max': 10,
            'rango': 'Extremadamente Bajo',
            'interpretacion': 'Actitud prosocial estable.	'
        },
        {
            'min': 11,
            'max': 25,
            'rango': 'Muy Bajo',
            'interpretacion': 'Conducta social adecuada.	'
        },
        {
            'min': 26,
            'max': 35,
            'rango': 'Bajo',
            'interpretacion': 'Poca tendencia a transgresión.	'
        },
        {
            'min': 36,
            'max': 65,
            'rango': 'Medio',
            'interpretacion': 'Independencia con respeto a normas.	'
        },
        {
            'min': 66,
            'max': 75,
            'rango': 'Alto',
            'interpretacion': 'Inconformidad moderada.	'
        },
        {
            'min': 76,
            'max': 90,
            'rango': 'Muy Alto',
            'interpretacion': 'Actitudes desafiantes frecuentes.	'
        },
        {
            'min': 91,
            'max': 100,
            'rango': 'Extremadamente Alto',
            'interpretacion': 'Conducta social disruptiva.	'
        }
    ],
    
    
    'TPIMP': [
        {
            'min': 0,
            'max': 10,
            'rango': 'Extremadamente Bajo',
            'interpretacion': 'Control emocional muy alto.	'
        },
        {
            'min': 11,
            'max': 25,
            'rango': 'Muy Bajo',
            'interpretacion': 'Alta inhibición y reflexión.	'
        },
        {
            'min': 26,
            'max': 35,
            'rango': 'Bajo',
            'interpretacion': 'Buena regulación de impulsos.	'
        },
        {
            'min': 36,
            'max': 65,
            'rango': 'Medio',
            'interpretacion': 'Impulsividad ocasional/contextualizada	'
        },
        {
            'min': 66,
            'max': 75,
            'rango': 'Alto',
            'interpretacion': 'Dificultad para inhibir respuestas.	'
        },
        {
            'min': 76,
            'max': 90,
            'rango': 'Muy Alto',
            'interpretacion': 'Reactividad emocional marcada.	'
        },
        {
            'min': 91,
            'max': 100,
            'rango': 'Extremadamente Alto',
            'interpretacion': 'Impulsividad excesiva.	'
        }
    ],
    
    
    'TLDYP': [
        {
            'min': 0,
            'max': 10,
            'rango': 'Extremadamente Bajo',
            'interpretacion': 'Actitud muy positiva hacia el esfuerzo.	'
        },
        {
            'min': 11,
            'max': 25,
            'rango': 'Muy Bajo',
            'interpretacion': 'Cree en el valor del cambio.	'
        },
        {
            'min': 26,
            'max': 35,
            'rango': 'Bajo',
            'interpretacion': 'Motivación saludable.	'
        },
        {
            'min': 36,
            'max': 65,
            'rango': 'Medio',
            'interpretacion': 'Cuestionamiento equilibrado.	'
        },
        {
            'min': 66,
            'max': 75,
            'rango': 'Alto',
            'interpretacion': 'Actitud crítica hacia el estudio.	'
        },
        {
            'min': 76,
            'max': 90,
            'rango': 'Muy Alto',
            'interpretacion': 'Desvalorización del esfuerzo.	'
        },
        {
            'min': 91,
            'max': 100,
            'rango': 'Extremadamente Alto',
            'interpretacion': 'Postura pesimista constante.	'
        }
    ],
    
    
    
    
    'TLMAQ': [
        {
            'min': 0,
            'max': 10,
            'rango': 'Extremadamente Bajo',
            'interpretacion': 'Conducta muy ética y transparente. Ingenuidad	'
        },
        {
            'min': 11,
            'max': 25,
            'rango': 'Muy Bajo',
            'interpretacion': 'Baja tendencia a influir en otros. 	'
        },
        {
            'min': 26,
            'max': 35,
            'rango': 'Bajo',
            'interpretacion': 'Honestidad habitual.	'
        },
        {
            'min': 36,
            'max': 65,
            'rango': 'Medio',
            'interpretacion': 'Uso ocasional de estrategias para beneficio personal.	'
        },
        {
            'min': 66,
            'max': 75,
            'rango': 'Alto',
            'interpretacion': 'Tendencia a la manipulación interpersonal para sacar ventaja.	'
        },
        {
            'min': 76,
            'max': 90,
            'rango': 'Muy Alto',
            'interpretacion': 'Manipulación evidente. Coerción o manipulación	'
        },
        {
            'min': 91,
            'max': 100,
            'rango': 'Extremadamente Alto',
            'interpretacion': 'Instrumentalización habitual de otros.	'
        }
    ],
    
    # ==========================================================
    # Aspectos Potenciadores
    # ==========================================================
    
    
    
    
    'TMOAL': [
        {
            'min': 0,
            'max': 10,
            'rango': 'Extremadamente Bajo',
            'interpretacion': 'No se fija metas.	'
        },
        {
            'min': 11,
            'max': 25,
            'rango': 'Muy Bajo',
            'interpretacion': 'Metas poco ambiciosas.	'
        },
        {
            'min': 26,
            'max': 35,
            'rango': 'Bajo',
            'interpretacion': 'Limitada orientación a resultados.	'
        },
        {
            'min': 36,
            'max': 65,
            'rango': 'Medio',
            'interpretacion': 'Motivación media por alcanzar logros.	'
        },
        {
            'min': 66,
            'max': 75,
            'rango': 'Alto',
            'interpretacion': 'Compromiso con metas.	'
        },
        {
            'min': 76,
            'max': 90,
            'rango': 'Muy Alto',
            'interpretacion': 'Deseo elevado de superación.	'
        },
        {
            'min': 91,
            'max': 100,
            'rango': 'Extremadamente Alto',
            'interpretacion': 'Alta orientación a resultados.	'
        }
    ],
    
    
    
    'TMAEF': [
        {
            'min': 0,
            'max': 10,
            'rango': 'Extremadamente Bajo',
            'interpretacion': 'Baja percepción de capacidad.	'
        },
        {
            'min': 11,
            'max': 25,
            'rango': 'Muy Bajo',
            'interpretacion': 'Inseguridad ante retos.	'
        },
        {
            'min': 26,
            'max': 35,
            'rango': 'Bajo',
            'interpretacion': 'Autoeficacia limitada.	'
        },
        {
            'min': 36,
            'max': 65,
            'rango': 'Medio',
            'interpretacion': 'Confianza funcional.	'
        },
        {
            'min': 66,
            'max': 75,
            'rango': 'Alto',
            'interpretacion': 'Buena percepción de competencia.	'
        },
        {
            'min': 76,
            'max': 90,
            'rango': 'Muy Alto',
            'interpretacion': 'Alta autoeficacia.	'
        },
        {
            'min': 91,
            'max': 100,
            'rango': 'Extremadamente Alto',
            'interpretacion': 'Seguridad personal excepcional.	'
        }
    ],
    
    
    
    
    'TMMAE': [
        {
            'min': 0,
            'max': 10,
            'rango': 'Extremadamente Bajo',
            'interpretacion': 'Poco interés por el dominio académico.	'
        },
        {
            'min': 11,
            'max': 25,
            'rango': 'Muy Bajo',
            'interpretacion': 'Escaso deseo de aprender a profundidad.	'
        },
        {
            'min': 26,
            'max': 35,
            'rango': 'Bajo',
            'interpretacion': 'Baja motivación académica.	'
        },
        {
            'min': 36,
            'max': 65,
            'rango': 'Medio',
            'interpretacion': 'Motivación aceptable.	'
        },
        {
            'min': 66,
            'max': 75,
            'rango': 'Alto',
            'interpretacion': 'Fuerte compromiso con el aprendizaje.	'
        },
        {
            'min': 76,
            'max': 90,
            'rango': 'Muy Alto',
            'interpretacion': 'Deseo de excelencia académica.	'
        },
        {
            'min': 91,
            'max': 100,
            'rango': 'Extremadamente Alto',
            'interpretacion': 'Alto impulso por la maestría.	'
        }
    ],
    
    
    
    
    'TMLID': [
        {
            'min': 0,
            'max': 10,
            'rango': 'Extremadamente Bajo',
            'interpretacion': 'Evita roles de dirección.	'
        },
        {
            'min': 11,
            'max': 25,
            'rango': 'Muy Bajo',
            'interpretacion': 'Poca iniciativa grupal.	'
        },
        {
            'min': 26,
            'max': 35,
            'rango': 'Bajo',
            'interpretacion': 'Disposición limitada a coordinar.	'
        },
        {
            'min': 36,
            'max': 65,
            'rango': 'Medio',
            'interpretacion': 'Liderazgo funcional ocasional/contextual.	'
        },
        {
            'min': 66,
            'max': 75,
            'rango': 'Alto',
            'interpretacion': 'Capacidad para guiar a otros.	'
        },
        {
            'min': 76,
            'max': 90,
            'rango': 'Muy Alto',
            'interpretacion': 'Alta disposición a liderar.	'
        },
        {
            'min': 91,
            'max': 100,
            'rango': 'Extremadamente Alto',
            'interpretacion': 'Liderazgo sobresaliente.	'
        }
    ],
    
    
    
    
    'TMAES': [
        {
            'min': 0,
            'max': 10,
            'rango': 'Extremadamente Bajo',
            'interpretacion': 'Autoimagen muy deteriorada.	'
        },
        {
            'min': 11,
            'max': 25,
            'rango': 'Muy Bajo',
            'interpretacion': 'Frecuente autocrítica.	'
        },
        {
            'min': 26,
            'max': 35,
            'rango': 'Bajo',
            'interpretacion': 'Inseguridad persistente.	'
        },
        {
            'min': 36,
            'max': 65,
            'rango': 'Medio',
            'interpretacion': 'Autoaceptación funcional.	'
        },
        {
            'min': 66,
            'max': 75,
            'rango': 'Alto',
            'interpretacion': 'Buena valoración personal.	'
        },
        {
            'min': 76,
            'max': 90,
            'rango': 'Muy Alto',
            'interpretacion': 'Autoestima elevada.	'
        },
        {
            'min': 91,
            'max': 100,
            'rango': 'Extremadamente Alto',
            'interpretacion': 'Alta seguridad interna.	'
        }
    ],
    
    
    
    
    'TDCMP': [
        {
            'min': 0,
            'max': 10,
            'rango': 'Extremadamente Bajo',
            'interpretacion': 'Carece de recursos motivacionales y autoconfianza; puede mostrar desinterés por el logro académico.'
        },
        {
            'min': 11,
            'max': 25,
            'rango': 'Muy Bajo',
            'interpretacion': 'Presenta baja motivación y escasa percepción de eficacia personal; requiere apoyo para mantener objetivos.'
        },
        {
            'min': 26,
            'max': 35,
            'rango': 'Bajo',
            'interpretacion': 'Muestra motivación inconstante y limitada seguridad en sus capacidades; su compromiso puede ser variable.'
        },
        {
            'min': 36,
            'max': 65,
            'rango': 'Medio',
            'interpretacion': 'Posee un nivel adecuado de motivación y confianza; cuenta con recursos suficientes para sostener su desempeño.'
        },
        {
            'min': 66,
            'max': 75,
            'rango': 'Alto',
            'interpretacion': 'Denota orientación clara hacia el logro y buena autoconfianza; tiende a perseverar ante los retos.'
        },
        {
            'min': 76,
            'max': 90,
            'rango': 'Muy Alto',
            'interpretacion': 'Evidencia alta motivación, sentido de eficacia y liderazgo positivo en contextos académicos y sociales.'
        },
        {
            'min': 91,
            'max': 100,
            'rango': 'Extremadamente Alto',
            'interpretacion': 'Presenta un perfil de alta autoexigencia y orientación al éxito; puede mostrar tendencia al perfeccionismo desadaptativo o sobrecarga.'
        }
    ],
    
    
    # ==========================================================
    # Aspectos Limitadores
    # ==========================================================
    
    
    
    
    'TDCML': [
        {
            'min': 0,
            'max': 10,
            'rango': 'Extremadamente Bajo',
            'interpretacion': 'No se observan factores que limiten su desempeño; muestra buena estabilidad emocional y académica.'
        },
        {
            'min': 11,
            'max': 25,
            'rango': 'Muy Bajo',
            'interpretacion': 'Evidencia mínima presencia de factores limitantes; mantiene equilibrio emocional y social.'
        },
        {
            'min': 26,
            'max': 35,
            'rango': 'Bajo',
            'interpretacion': 'Presenta ocasionales dificultades ante la presión o el error, sin que afecten significativamente su desempeño.'
        },
        {
            'min': 36,
            'max': 65,
            'rango': 'Medio',
            'interpretacion': 'Muestra un nivel moderado de limitaciones; puede experimentar inseguridad o procrastinación en ciertos contextos. Es un perfil funcional.'
        },
        {
            'min': 66,
            'max': 75,
            'rango': 'Alto',
            'interpretacion': 'Indica presencia de factores emocionales o conductuales que podrían interferir parcialmente con su desempeño.'
        },
        {
            'min': 76,
            'max': 90,
            'rango': 'Muy Alto',
            'interpretacion': 'Refleja dificultades marcadas en la gestión emocional o motivacional; puede requerir acompañamiento o contención.'
        },
        {
            'min': 91,
            'max': 100,
            'rango': 'Extremadamente Alto',
            'interpretacion': 'Manifiesta altos niveles de inseguridad, evitación o temor al fracaso; su funcionamiento puede verse significativamente comprometido.'
        }
    ],
    
    
    
    
    'TMTEF': [
        {
            'min': 0,
            'max': 10,
            'rango': 'Extremadamente Bajo',
            'interpretacion': 'Tolerancia muy alta al error.'
        },
        {
            'min': 11,
            'max': 25,
            'rango': 'Muy Bajo',
            'interpretacion': 'Poca ansiedad por fallar.	'
        },
        {
            'min': 26,
            'max': 35,
            'rango': 'Bajo',
            'interpretacion': 'Aceptación funcional del error.	'
        },
        {
            'min': 36,
            'max': 65,
            'rango': 'Medio',
            'interpretacion': 'Preocupación controlada.	'
        },
        {
            'min': 66,
            'max': 75,
            'rango': 'Alto',
            'interpretacion': 'Ansiedad frente al fracaso.	'
        },
        {
            'min': 76,
            'max': 90,
            'rango': 'Muy Alto',
            'interpretacion': 'Temor persistente a equivocarse.	'
        },
        {
            'min': 91,
            'max': 100,
            'rango': 'Extremadamente Alto',
            'interpretacion': 'Miedo paralizante al fracaso.	'
        }
    ],
    
    
    
    
    'TMETR': [
        {
            'min': 0,
            'max': 10,
            'rango': 'Extremadamente Bajo',
            'interpretacion': 'Busca desafíos activamente.	'
        },
        {
            'min': 11,
            'max': 25,
            'rango': 'Muy Bajo',
            'interpretacion': 'Alta disposición al esfuerzo.	'
        },
        {
            'min': 26,
            'max': 35,
            'rango': 'Bajo',
            'interpretacion': 'Afronta lo difícil con decisión.	'
        },
        {
            'min': 36,
            'max': 65,
            'rango': 'Medio',
            'interpretacion': 'Evasión ocasional de retos.	'
        },
        {
            'min': 66,
            'max': 75,
            'rango': 'Alto',
            'interpretacion': 'Evita tareas difíciles.	'
        },
        {
            'min': 76,
            'max': 90,
            'rango': 'Muy Alto',
            'interpretacion': 'Rechaza lo exigente.	'
        },
        {
            'min': 91,
            'max': 100,
            'rango': 'Extremadamente Alto',
            'interpretacion': 'Evita sistemáticamente el esfuerzo.	'
        }
    ],
    
    
    
    
    'TMMOR': [
        {
            'min': 0,
            'max': 10,
            'rango': 'Extremadamente Bajo',
            'interpretacion': 'Cumplimiento sistemático.	'
        },
        {
            'min': 11,
            'max': 25,
            'rango': 'Muy Bajo',
            'interpretacion': 'Puntualidad constante.	'
        },
        {
            'min': 26,
            'max': 35,
            'rango': 'Bajo',
            'interpretacion': 'Demoras poco frecuentes.	'
        },
        {
            'min': 36,
            'max': 65,
            'rango': 'Medio',
            'interpretacion': 'Morosidad moderada.	'
        },
        {
            'min': 66,
            'max': 75,
            'rango': 'Alto',
            'interpretacion': 'Tendencia a postergar tareas.	'
        },
        {
            'min': 76,
            'max': 90,
            'rango': 'Muy Alto',
            'interpretacion': 'Procrastinación marcada y frecuente	'
        },
        {
            'min': 91,
            'max': 100,
            'rango': 'Extremadamente Alto',
            'interpretacion': 'Grave dificultad para cumplir plazos.	'
        }
    ],
    
    
    'TPINS': [
        {
            'min': 0,
            'max': 10,
            'rango': 'Extremadamente Bajo',
            'interpretacion': 'Sociabilidad muy alta.	'
        },
        {
            'min': 11,
            'max': 25,
            'rango': 'Muy Bajo',
            'interpretacion': 'Buena adaptación grupal.	'
        },
        {
            'min': 26,
            'max': 35,
            'rango': 'Bajo',
            'interpretacion': 'Interacción funcional.	'
        },
        {
            'min': 36,
            'max': 65,
            'rango': 'Medio',
            'interpretacion': 'Ansiedad social ocasional.	'
        },
        {
            'min': 66,
            'max': 75,
            'rango': 'Alto',
            'interpretacion': 'Tensión en situaciones sociales.	'
        },
        {
            'min': 76,
            'max': 90,
            'rango': 'Muy Alto',
            'interpretacion': 'Evita interacciones grupales.	'
        },
        {
            'min': 91,
            'max': 100,
            'rango': 'Extremadamente Alto',
            'interpretacion': 'Alta incomodidad y retraimiento.	'
        }
    ],
    
    
    
    'TPINP': [
        {
            'min': 0,
            'max': 10,
            'rango': 'Extremadamente Bajo',
            'interpretacion': 'Alta confianza personal.	'
        },
        {
            'min': 11,
            'max': 25,
            'rango': 'Muy Bajo',
            'interpretacion': 'Seguridad estable en relaciones.	'
        },
        {
            'min': 26,
            'max': 35,
            'rango': 'Bajo',
            'interpretacion': 'Autoimagen sólida.	'
        },
        {
            'min': 36,
            'max': 65,
            'rango': 'Medio',
            'interpretacion': 'Autoconfianza fluctuante.	'
        },
        {
            'min': 66,
            'max': 75,
            'rango': 'Alto',
            'interpretacion': 'Dudas frecuentes sobre sí mismo.	'
        },
        {
            'min': 76,
            'max': 90,
            'rango': 'Muy Alto',
            'interpretacion': 'Miedo al juicio ajeno.	'
        },
        {
            'min': 91,
            'max': 100,
            'rango': 'Extremadamente Alto',
            'interpretacion': 'Inseguridad interpersonal severa.	'
        }
    ],
    
    

}


