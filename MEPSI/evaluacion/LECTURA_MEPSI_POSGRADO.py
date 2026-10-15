# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 13:56:32 2024

@author: Xavier Contla
"""

import csv
import pandas as pd
import NORMAS_MEPSI
import math
import interpretacion_mepsi
#import os

ruta_principal = 'D:/DGOAE/2026/MEPSI/'
# ruta_posgrado = '2027_2/UDP/6OCTUBRE/SALUD_ANIMAL/'
ruta_posgrado = '2027_2/UAEM/'
nombre_archivo_csv = 'MEPSI_UAEM_20272.csv'
nombre_archivo_excel_resumen = 'MEPSI_UAEM_20272(Resumen).xlsx'
nombre_archivo_excel = 'MEPSI_UAEM_20272.xlsx' 

normas = NORMAS_MEPSI.norma_uaem_pciencias

interpretaciones = interpretacion_mepsi.interpretaciones
infogeneral = interpretacion_mepsi.interpretacion_general


def redondea(val):
    vd = val - int(val)
    if vd >= 0.5:
        return math.ceil(val)
    else:
        return round(val)


def generate_string_representation(value):
    if value < 1:
        return 'N.A.'
    return "|" * int(value)

def revisa_array(respuesta,indices):
    s = 0
    for indice in indices:
        s = s + int(respuesta[indice-1])
     
   
    return s   


def califica_P1A(respuesta): #12
    s = 0
    
    print(respuesta,len(respuesta))
    if len(respuesta) == 12:
        for x,y in zip(respuesta,'845125637876'):
            if x == y:
                s = s + 1
                
    else :
        print("P1A - No tiene la longitud")
    return s

def califica_P1B(respuesta):
    s = 0
    
    print(respuesta,len(respuesta))
    if len(respuesta) == 36:
        for x,y in zip(respuesta,'517431618456212467388763727565485132'):
            if x == y:
                s = s + 1
                
    else :
        print("P1B - No tiene la longitud")
    
    return s

def califica_P1C(respuesta):
    suma = 0
    print(respuesta,len(respuesta))
    if len(respuesta) == 40:
        for x,y in zip(respuesta,'BDCACACC*BADDEDCBCEACBACBDACAEB*D*ABCEAD'):
            if x == y:
                suma = suma + 1
            elif y == '*' :
                suma = suma + 1
    else :
        print("P1C - No tiene la longitud")
    return suma

def califica_P2A(respuesta):
    index = 0    
    s = 0
    print(respuesta,len(respuesta))
    if len(respuesta) == 34:
        correcto = False
        for x,y in zip(respuesta,'2A2B1B1C1A3D3A3B1C1C1C1D2A2C2A1B1A'):
            if index % 2 == 0 :
                if x == y:
                    correcto = True
                else:
                    correcto = False
            else:
                if x == y and correcto:                    
                    s = s + 1
                else:
                    s = s + 0
            
            index = index + 1
    else :
        print("P2A - No tiene la longitud")
    return s

def califica_P2B(respuesta):
    s = 0
    print(respuesta,len(respuesta))
    if len(respuesta) == 24:
        for x,y in zip(respuesta,'DCBEDCCAEEBEBDCCCADAADDD'):
            if x == y:
                s = s + 1
    else :
        print("P2B - No tiene la longitud")

    return s        
                

def califica_P2C(respuesta):
    s = 0
    print(respuesta,len(respuesta))
    if len(respuesta) == 15:
        for x,y in zip(respuesta,'ACBADAAABDBCDCD'):
            if x == y:
               s = s + 1
    else :
        print("P2C - No tiene la longitud")
        return 0
    return s



# *****************************************************************                                                                                                            
# * III.A.PERSONALIDAD:                                           * 
# * PEYN                                                          *
# * [7,9,14,15,21,27,34,42,54,61,76,82,83,87,89,92,94]            *
# * PINP                                                          *
# * [2,10,28,30,37,43,50,63,70,78,84]                             *
# * PINS                                                          *
# * [25,40,55,68,75,81,88,93,96]                                  *
# * PIMP                                                          *
# * [4,31,45,65,79,91]                                            *
# * PDES                                                          *
# * [6,41,33,46,59,66,73,80,86]                                  *
# * PMEN                                                          *
# * [8,16,20,26,32,36,44,48,64,72,77,95]                         *
# * PDPP                                                          *
# * [1,3,5,11,12,13,17,18,19,22,23,24,29,35,38,39,47,49,51,52,53,*
# *  56,57,58,60,62,67,69,71,74,85,90,92,97,98,99,100,101,102,103,*
# *  104,105,106,107,108,109,110,111,112,113]                     *
# * PCSO  = PDES + PMEN                                           *
# *                                                               *
# *                                                               *
# *****************************************************************  


def califica_P3A(respuesta):
    
    V_value = [2,4,5,10,11,12,13,14,17,18,21,22,23,24,25,27,28,29,30,31,37,38,40,42,43,45,47,50,51,52,54,55,56,57,58,61,63,65,68,70,76,78,79,84,89,91,92,93,96,99,103,104,107,110,113]
    F_value = [1,3,6,7,8,9,15,16,19,20,26,32,33,34,35,36,39,41,44,46,48,49,53,59,60,62,64,66,67,69,71,72,73,74,75,77,80,81,82,83,85,86,87,88,90,94,95,97,98,100,101,102,105,106,108,109,111,112]
   
    res_array = [*respuesta]
    
    print(respuesta,len(respuesta))
    if len(respuesta) == 113:
        for index in V_value:
            if respuesta[index-1] == 'V':
                res_array[index-1] = '1'
            else:
                res_array[index-1] = '0'
        for index in F_value:
            if respuesta[index-1] == 'F':
                res_array[index-1] = '1'
            else:                
                res_array[index-1] = '0'

    else :
        print("P3A - No tiene la longitud")
        return 0,0,0,0,0,0,0,0
    PEYN = revisa_array(res_array,[7,9,14,15,21,27,34,42,54,61,76,82,83,87,89,92,94])
    PINP = revisa_array(res_array,[2,10,28,30,37,43,50,63,70,78,84] )
    PINS = revisa_array(res_array,[25,40,55,68,75,81,88,93,96])
    PIMP = revisa_array(res_array,[4,31,45,65,79,91])
    PDES = revisa_array(res_array,[6,41,33,46,59,66,73,80,86] )
    PMEN = revisa_array(res_array,[8,16,20,26,32,36,44,48,64,72,77,95])
    PDPP = revisa_array(res_array,[1,3,5,11,12,13,17,18,19,22,23,24,29,35,38,39,47,49,51,52,53,56,57,58,60,62,67,69,71,74,85,90,92,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113])

    PCSO = PDES + PMEN 
          
    return PEYN,PINP,PINS,PIMP,PDES,PMEN,PDPP,PCSO


    
    

# *****************************************************************                                                                                                            
# * III.B. Motivadores:                                           * 
# * AUTOESTIMA MAES                                               *
# * (1,8,20,33,46,59,64,66,68,72,75,76,77,79,80,82)               *
# * AUTOEFICACIA MAEF                                             *
# * (14,26,39,52,63,65,67,69,71,73)                               *
# * TEMOR AL FRACASO                                              *
# * (2,9,15,21,27,34,40,47,53,60)                                 *
# * EVITACION DEL TRABAJO                                         *
# * (3,10,16,22,28,35,41,48,54,61)                                *
# * MAESTRIA                                                      *
# * (4,11,17,23,29,36,42,49,55)                                   *
# * ORIENTACION AL LOGRO                                          *
# * (5,12,19,24,30,37,44,50)                                      *
# * MOROSIDAD                                                     *
# * (6,13,25,31,38,45,51,57,62)                                   *
# * LIDERAZGO                                                     *
# * (7,18,32,43,56,58,74,78)                                      *
# *                                                               *
# *****************************************************************             
def califica_P3B(respuesta):
    
    i_value = [20,59,76,82]
    
    print(respuesta,len(respuesta))
    
    res_arrayp2c = [*respuesta]
    
    if len(res_arrayp2c) == 82:
        for i in i_value:
            if res_arrayp2c[i-1] == '4' :
                res_arrayp2c[i-1] = '1'
            elif res_arrayp2c[i-1] == '3' :
                res_arrayp2c[i-1] = '2'
            elif res_arrayp2c[i-1] == '2' :
                res_arrayp2c[i-1] = '3'
            elif res_arrayp2c[i-1] == '4' :
                res_arrayp2c[i-1] = '1'
    else :
        print("P3B - No tiene la longitud")
        return 0,0,0,0,0,0,0,0
    #r_array = [*respuesta]
    
    respuesta = "".join(res_arrayp2c)
    
    MAES = revisa_array(respuesta,[1,8,20,33,46,59,64,66,68,72,75,76,77,79,80,82])
    MAEF = revisa_array(respuesta,[14,26,39,52,63,65,67,69,71,73])
    MTEF = revisa_array(respuesta,[2,9,15,21,27,34,40,47,53,60])
    METR = revisa_array(respuesta,[3,10,16,22,28,35,41,48,54,61])
    MMAE = revisa_array(respuesta,[4,11,17,23,29,36,42,49,55])
    MOAL = revisa_array(respuesta,[5,12,19,24,30,37,44,50])
    MMOR = revisa_array(respuesta,[6,13,25,31,38,45,51,57,62])
    MLID = revisa_array(respuesta,[7,18,32,43,56,58,74,78])
    
    
        
    return MAES, MAEF, MTEF, METR, MMAE, MOAL, MMOR, MLID


# *****************************************************************                                                                                                            
# * III.C. Sociales                                               * 
# * LDYP                                                          *
# * (1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41)   *
# * LMAQ                                                          *
# * (2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40)     *
# *                                                               *
# *****************************************************************   
def califica_P3C(respuesta):
    print('califica_P3C', respuesta,len(respuesta))
        
    i_value = [3, 6, 8, 12, 14, 18, 20, 21, 22, 28, 32, 34, 41]
    
    res_arrayp3c = [*respuesta]
    
    if len(res_arrayp3c) == 45:
        for i in i_value:
            if res_arrayp3c[i-1] == '4' :
                res_arrayp3c[i-1] = '1'
            elif res_arrayp3c[i-1] == '3' :
                res_arrayp3c[i-1] = '2'
            elif res_arrayp3c[i-1] == '2' :
                res_arrayp3c[i-1] = '3'
            elif res_arrayp3c[i-1] == '4' :
                res_arrayp3c[i-1] = '1'
    else :
         print("P2A - No tiene la longitud")
         return 0,0
     
    respuesta = "".join(res_arrayp3c)
    print('califica_P3C', respuesta,len(respuesta))
    
    LDYP = revisa_array(respuesta,[1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41])
    LMAQ = revisa_array(respuesta,[2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40])
    
    
    
    return LDYP, LMAQ

# Función para procesar la columna c_respuestas
def procesar_respuestas(respuestas):
    # Reducir múltiples espacios a uno solo y luego dividir por espacios
    respuestas_sin_multiples_espacios = ' '.join(respuestas.split())
    respuestas_separadas = respuestas_sin_multiples_espacios.split(' ')
    
    # Crear 7 variables con las respuestas
    if len(respuestas_separadas) >= 7:
        variable1 = respuestas_separadas[0]
        variable2 = respuestas_separadas[1]
        variable3 = respuestas_separadas[2]
        variable4 = respuestas_separadas[3]
        variable5 = respuestas_separadas[4]
        variable6 = respuestas_separadas[5]
        variable7 = respuestas_separadas[6]
    else:
        # Manejar el caso en el que no haya suficientes respuestas
        variable1, variable2, variable3, variable4, variable5, variable6, variable7 = '', '', '', '', '', '', ''

    return [variable1, variable2, variable3, variable4, variable5, variable6, variable7]


# Nombre del archivo CSV
archivo_csv = ruta_principal + ruta_posgrado + nombre_archivo_csv

# Lista para almacenar los datos procesados
datos_procesados = []

# Leer el archivo CSV
with open(archivo_csv, newline='', encoding='utf-8') as csvfile:
    # Crear un lector de CSV
    lector_csv = csv.reader(csvfile, delimiter=',')

    i = 0
    # Iterar sobre las filas del CSV
    for fila in lector_csv:
        if i == 0:   
            i = 1
            continue
    
        
        # Obtener las variables procesadas
        id_usuario, c_apPaterno, c_apMaterno, c_nombres, c_sexo, c_num_cuenta, c_posgrado_ingresar, c_nivel, c_respuestas, b_completo, d_creacion, d_modificacion = fila
        array_respuestas = procesar_respuestas(c_respuestas)

        # Agregar los datos procesados a la lista
        datos_procesados.append((id_usuario, c_apPaterno, c_apMaterno, c_nombres, c_sexo, c_num_cuenta, 
                                 c_posgrado_ingresar, c_nivel, array_respuestas, b_completo, d_creacion, d_modificacion))

index = 0
combined_df = []
# Imprimir los datos procesados
for datos in datos_procesados:
    
    
    print(index + 1, "Número")
    array_respuestas = datos[8]
    ARAR1 = califica_P1A(array_respuestas[0][0:12])
    ARAR2 = califica_P1B(array_respuestas[0][12:])
    ARVAN = califica_P2A(array_respuestas[1])
    ARVUL = califica_P2B(array_respuestas[2])
    ARVCL = califica_P2C(array_respuestas[3])
    PEYN, PINP, PINS, PIMP, PDES, PMEN, PDPP, PCSO = califica_P3A(array_respuestas[4])
    MAES, MAEF, MTEF, METR, MMAE, MOAL, MMOR, MLID = califica_P3B(array_respuestas[5])
    LDYP, LMAQ = califica_P3C(array_respuestas[6])
    
    TARAR2 = redondea(( (ARAR2 - normas[0][0]) /normas[0][1]) * 15 + 50  )
    TARVAN = redondea(( (ARVAN - normas[1][0]) /normas[1][1]) * 15 + 50  )
    TARVUL = redondea(( (ARVUL - normas[2][0]) /normas[2][1]) * 15 + 50  )
    TARVCL = redondea(( (ARVCL - normas[3][0]) /normas[3][1]) * 15 + 50  )

    TPEYN = redondea(( (PEYN - normas[4][0]) /normas[4][1]) * 15 + 50  )
    TPINP = redondea(( (PINP - normas[5][0]) /normas[5][1]) * 15 + 50  )
    TPINS = redondea(( (PINS - normas[6][0]) /normas[6][1]) * 15 + 50  )
    TPIMP = redondea(( (PIMP - normas[7][0]) /normas[7][1]) * 15 + 50  )
    TPDES = redondea(( (PDES - normas[8][0]) /normas[8][1]) * 15 + 50  )
    TPMEN = redondea(( (PMEN - normas[9][0]) /normas[9][1]) * 15 + 50  )
    TPDPP = redondea(( (PDPP - normas[10][0]) /normas[10][1]) * 15 + 50  )
    TPCSO = redondea(( (PCSO - normas[11][0]) /normas[11][1]) * 15 + 50  )

    TMAES = redondea(( (MAES - normas[12][0]) /normas[12][1]) * 15 + 50  )
    TMAEF = redondea(( (MAEF - normas[13][0]) /normas[13][1]) * 15 + 50  )
    TMTEF = redondea(( (MTEF - normas[14][0]) /normas[14][1]) * 15 + 50  )
    TMETR = redondea(( (METR - normas[15][0]) /normas[15][1]) * 15 + 50  )
    TMMAE = redondea(( (MMAE - normas[16][0]) /normas[16][1]) * 15 + 50  )
    TMOAL = redondea(( (MOAL - normas[17][0]) /normas[17][1]) * 15 + 50  )
    TMMOR = redondea(( (MMOR - normas[18][0]) /normas[18][1]) * 15 + 50  )
    TMLID = redondea(( (MLID - normas[19][0]) /normas[19][1]) * 15 + 50  )

    TLDYP = redondea(( (LDYP - normas[20][0]) /normas[20][1]) * 15 + 50  )
    TLMAQ = redondea(( (LMAQ - normas[21][0]) /normas[21][1]) * 15 + 50  )

    TDCAA = redondea((TARAR2 + TARVAN + TARVUL + TARVCL) / 4)
    TDCAS = redondea((TPCSO + TPDES + TPMEN + TPEYN) / 4)
    TDCDS = redondea((TPDPP + TPIMP + TLDYP + TLMAQ) / 4)
    TDCMP = redondea((TMOAL + TMAEF + TMMAE + TMLID + TMAES) / 5)
    TDCML = redondea((TMTEF + TMETR + TMMOR + TPINS + TPINP) / 5)
    
    TDCAA_RANGO, INT_TDCAA  = interpretacion_mepsi.obtener_interpretacion('TDCAA', TDCAA)
    TARAR2_RANGO,INT_TARAR2 = interpretacion_mepsi.obtener_interpretacion('TARAR2', TARAR2)
    TARVAN_RANGO,INT_TARVAN = interpretacion_mepsi.obtener_interpretacion('TARVAN', TARVAN)
    TARVUL_RANGO,INT_TARVUL = interpretacion_mepsi.obtener_interpretacion('TARVUL', TARVUL)
    TARVCL_RANGO,INT_TARVCL = interpretacion_mepsi.obtener_interpretacion('TARVCL', TARVCL)
    
    
    TDCAS_RANGO,INT_TDCAS = interpretacion_mepsi.obtener_interpretacion('TDCAS', TDCAS)
    TPCSO_RANGO,INT_TPCSO = interpretacion_mepsi.obtener_interpretacion('TPCSO', TPCSO)
    TPDES_RANGO,INT_TPDES = interpretacion_mepsi.obtener_interpretacion('TPDES', TPDES)
    TPMEN_RANGO, INT_TPMEN = interpretacion_mepsi.obtener_interpretacion('TPMEN', TPMEN)
    TPEYN_RANGO,INT_TPEYN = interpretacion_mepsi.obtener_interpretacion('TPEYN', TPEYN)
    
    
    TDCDS_RANGO,INT_TDCDS = interpretacion_mepsi.obtener_interpretacion('TDCDS', TDCDS)
    TPDPP_RANGO,INT_TPDPP = interpretacion_mepsi.obtener_interpretacion('TPDPP', TPDPP)
    TPIMP_RANGO,INT_TPIMP = interpretacion_mepsi.obtener_interpretacion('TPIMP', TPIMP)
    TLDYP_RANGO,INT_TLDYP = interpretacion_mepsi.obtener_interpretacion('TLDYP', TLDYP)
    TLMAQ_RANGO,INT_TLMAQ = interpretacion_mepsi.obtener_interpretacion('TLMAQ', TLMAQ)
    
    
    TMOAL_RANGO,INT_TMOAL = interpretacion_mepsi.obtener_interpretacion('TMOAL', TMOAL)
    TMAEF_RANGO,INT_TMAEF = interpretacion_mepsi.obtener_interpretacion('TMAEF', TMAEF)
    TMMAE_RANGO,INT_TMMAE = interpretacion_mepsi.obtener_interpretacion('TMMAE', TMMAE)
    TMLID_RANGO,INT_TMLID = interpretacion_mepsi.obtener_interpretacion('TMLID', TMLID)
    TMAES_RANGO,INT_TMAES = interpretacion_mepsi.obtener_interpretacion('TMAES', TMAES)
    TDCMP_RANGO,INT_TDCMP = interpretacion_mepsi.obtener_interpretacion('TDCMP', TDCMP)
    
    
    TDCML_RANGO,INT_TDCML = interpretacion_mepsi.obtener_interpretacion('TDCML', TDCML)
    TMTEF_RANGO,INT_TMTEF = interpretacion_mepsi.obtener_interpretacion('TMTEF', TMTEF)
    TMETR_RANGO,INT_TMETR = interpretacion_mepsi.obtener_interpretacion('TMETR', TMETR)
    TMMOR_RANGO,INT_TMMOR = interpretacion_mepsi.obtener_interpretacion('TMMOR', TMMOR)
    TPINS_RANGO,INT_TPINS = interpretacion_mepsi.obtener_interpretacion('TPINS', TPINS)
    TPINP_RANGO,INT_TPINP = interpretacion_mepsi.obtener_interpretacion('TPINP', TPINP)
    
    

    print(TARAR2, TARVAN, TARVUL, TARVCL, 
          TPEYN,TPINP,TPINS,TPIMP,TPDES,TPMEN,TPDPP,TPCSO,
          TMAES, TMAEF, TMTEF, TMETR, TMMAE, TMOAL, TMMOR, TMLID,
          TDCAA, TDCAS, TDCDS, TDCMP, TDCML)

    

    index = index + 1
                
    data = {
    'FOLIO': datos[0],
    'FOLIO_ENTIDAD': datos[5],
    'NOMBRE': datos[1] +' ' +datos[2] +' ' + datos[3],
    'PROGRAMA': datos[6],
    'NIVEL': datos[7],
    'AREA':'CU',
    'TIPO':'A',
    'SEXO':datos[4],
    'TARAR2':100 if TARAR2 >= 100 else (0 if TARAR2 <= 1 else TARAR2) , 
    'TARVAN':100 if TARVAN >= 100 else (0 if TARVAN <= 1 else TARVAN),
    'TARVUL':100 if TARVUL >= 100 else (0 if TARVUL <= 1 else TARVUL),
    'TARVCL':100 if TARVCL >= 100 else (0 if TARVCL <= 1 else TARVCL),

    'TPEYN' :100 if TPEYN >= 100 else (0 if TPEYN <= 1 else TPEYN), 
    'TPINP' :100 if TPINP >= 100 else (0 if TPINP <= 1 else TPINP), 
    'TPINS' :100 if TPINS >= 100 else (0 if TPINS <= 1 else TPINS), 
    'TPIMP' :100 if TPIMP >= 100 else (0 if TPIMP <= 1 else TPIMP), 
    'TPDES' :100 if TPDES >= 100 else (0 if TPDES <= 1 else TPDES), 
    'TPMEN' :100 if TPMEN >= 100 else (0 if TPMEN <= 1 else TPMEN), 
    'TPCSO' :100 if TPCSO >= 100 else (0 if TPCSO <= 1 else TPCSO), 
    'TPDPP' :100 if TPDPP >= 100 else (0 if TPDPP <= 1 else TPDPP), 

    'TMAES' :100 if TMAES >= 100 else (0 if TMAES <= 1 else TMAES), 
    'TMAEF' :100 if TMAEF >= 100 else (0 if TMAEF <= 1 else TMAEF), 
    'TMTEF' :100 if TMTEF >= 100 else (0 if TMTEF <= 1 else TMTEF), 
    'TMETR' :100 if TMETR >= 100 else (0 if TMETR <= 1 else TMETR), 
    'TMMAE' :100 if TMMAE >= 100 else (0 if TMMAE <= 1 else TMMAE), 
    'TMOAL' :100 if TMOAL >= 100 else (0 if TMOAL <= 1 else TMOAL), 
    'TMMOR' :100 if TMMOR >= 100 else (0 if TMMOR <= 1 else TMMOR), 
    'TMLID' :100 if TMLID >= 100 else (0 if TMLID <= 1 else TMLID), 

    'TLDYP' :100 if TLDYP >= 100 else (0 if TLDYP <= 1 else TLDYP), 
    'TLMAQ' :100 if TLMAQ >= 100 else (0 if TLMAQ <= 1 else TLMAQ), 

    'TDCAA' :100 if TDCAA >= 100 else (0 if TDCAA <= 1 else TDCAA), 
    'TDCAS' :100 if TDCAS >= 100 else (0 if TDCAS <= 1 else TDCAS), 
    'TDCDS' :100 if TDCDS >= 100 else (0 if TDCDS <= 1 else TDCDS), 
    'TDCMP' :100 if TDCMP >= 100 else (0 if TDCMP <= 1 else TDCMP), 
    'TDCML' :100 if TDCML >= 100 else (0 if TDCML <= 1 else TDCML),
    
    'DIMENSION1': interpretacion_mepsi.obtener_dimension('TDCAA'),
    'TDCAA_RANGO' :TDCAA_RANGO ,'INT_TDCAA' :INT_TDCAA, 'TDCAA_SUBESCALA':interpretacion_mepsi.obtener_subescala('TDCAA'),
    'TARAR2_RANGO':TARAR2_RANGO,'INT_TARAR2':INT_TARAR2,'TARAR2_SUBESCALA':interpretacion_mepsi.obtener_subescala('TARAR2'),
    'TARVAN_RANGO':TARVAN_RANGO,'INT_TARVAN':INT_TARVAN,'TARVAN_SUBESCALA':interpretacion_mepsi.obtener_subescala('TARVAN'),
    'TARVUL_RANGO':TARVUL_RANGO,'INT_TARVUL':INT_TARVUL,'TARVUL_SUBESCALA':interpretacion_mepsi.obtener_subescala('TARVUL'),
    'TARVCL_RANGO':TARVCL_RANGO,'INT_TARVCL':INT_TARVCL,'TARVCl_SUBESCALA':interpretacion_mepsi.obtener_subescala('TARVCL'),

    'DIMENSION2': interpretacion_mepsi.obtener_dimension('TDCAS'),
    'TDCAS_RANGO':TDCAS_RANGO, 'INT_TDCAS':INT_TDCAS,'TDCAS_SUBESCALA':interpretacion_mepsi.obtener_subescala('TDCAS'),
    'TPCSO_RANGO':TPCSO_RANGO, 'INT_TPCSO':INT_TPCSO,'TPCSO_SUBESCALA':interpretacion_mepsi.obtener_subescala('TPCSO'),
    'TPDES_RANGO':TPDES_RANGO, 'INT_TPDES':INT_TPDES,'TPDES_SUBESCALA':interpretacion_mepsi.obtener_subescala('TPDES'),
    'TPMEN_RANGO':TPMEN_RANGO, 'INT_TPMEN':INT_TPMEN,'TPMEN_SUBESCALA':interpretacion_mepsi.obtener_subescala('TPMEN'),
    'TPEYN_RANGO':TPEYN_RANGO, 'INT_TPEYN':INT_TPEYN,'TPEYN_SUBESCALA':interpretacion_mepsi.obtener_subescala('TPEYN'),
    
    
    'DIMENSION3': interpretacion_mepsi.obtener_dimension('TDCDS'),
    'TDCDS_RANGO':TDCDS_RANGO,'INT_TDCDS':INT_TDCDS,'TDCDS_SUBESCALA':interpretacion_mepsi.obtener_subescala('TDCDS'),
    'TPDPP_RANGO':TPDPP_RANGO,'INT_TPDPP':INT_TPDPP,'TPDPP_SUBESCALA':interpretacion_mepsi.obtener_subescala('TPDPP'),
    'TPIMP_RANGO':TPIMP_RANGO,'INT_TPIMP':INT_TPIMP,'TPIMP_SUBESCALA':interpretacion_mepsi.obtener_subescala('TPIMP'),
    'TLDYP_RANGO':TLDYP_RANGO,'INT_TLDYP':INT_TLDYP,'TLDYP_SUBESCALA':interpretacion_mepsi.obtener_subescala('TLDYP'),
    'TLMAQ_RANGO':TLMAQ_RANGO,'INT_TLMAQ':INT_TLMAQ,'TLMAQ_SUBESCALA':interpretacion_mepsi.obtener_subescala('TLMAQ'),


    'DIMENSION4': interpretacion_mepsi.obtener_dimension('TDCMP'),
    'TDCMP_RANGO':TDCMP_RANGO,'INT_TDCMP':INT_TDCMP,'TDCMP_SUBESCALA':interpretacion_mepsi.obtener_subescala('TDCMP'),
    'TMOAL_RANGO':TMOAL_RANGO,'INT_TMOAL':INT_TMOAL,'TMOAL_SUBESCALA':interpretacion_mepsi.obtener_subescala('TMOAL'),
    'TMAEF_RANGO':TMAEF_RANGO,'INT_TMAEF':INT_TMAEF,'TMAEF_SUBESCALA':interpretacion_mepsi.obtener_subescala('TMAEF'),
    'TMMAE_RANGO':TMMAE_RANGO,'INT_TMMAE':INT_TMMAE,'TMMAE_SUBESCALA':interpretacion_mepsi.obtener_subescala('TMMAE'),
    'TMLID_RANGO':TMLID_RANGO,'INT_TMLID':INT_TMLID,'TMLID_SUBESCALA':interpretacion_mepsi.obtener_subescala('TMLID'),
    'TMAES_RANGO':TMAES_RANGO,'INT_TMAES':INT_TMAES,'TMAES_SUBESCALA':interpretacion_mepsi.obtener_subescala('TMAES'),
    

    'DIMENSION5': interpretacion_mepsi.obtener_dimension('TDCML'),
    'TDCML_RANGO':TDCML_RANGO,'INT_TDCML':INT_TDCML,'TDCML_SUBESCALA':interpretacion_mepsi.obtener_subescala('TDCML'),
    'TMTEF_RANGO':TMTEF_RANGO,'INT_TMTEF':INT_TMTEF,'TMTEF_SUBESCALA':interpretacion_mepsi.obtener_subescala('TMTEF'),
    'TMETR_RANGO':TMETR_RANGO,'INT_TMETR':INT_TMETR,'TMETR_SUBESCALA':interpretacion_mepsi.obtener_subescala('TMETR'),
    'TMMOR_RANGO':TMMOR_RANGO,'INT_TMMOR':INT_TMMOR,'TMMOR_SUBESCALA':interpretacion_mepsi.obtener_subescala('TMMOR'),
    'TPINS_RANGO':TPINS_RANGO,'INT_TPINS':INT_TPINS,'TPINS_SUBESCALA':interpretacion_mepsi.obtener_subescala('TPINS'),
    'TPINP_RANGO':TPINP_RANGO,'INT_TPINP':INT_TPINP,'TPINP_SUBESCALA':interpretacion_mepsi.obtener_subescala('TPINP')


 
    }   

    combined_df.append(data)


print(combined_df)

df = pd.DataFrame(combined_df)



# Recode and round numeric variables
numeric_vars = ['TARAR2', 'TARVAN', 'TARVUL', 'TARVCL', 'TPEYN', 'TPINP', 'TPINS', 'TPIMP', 'TPDES',
                 'TPMEN', 'TPCSO', 'TPDPP', 'TMAES', 'TMAEF', 'TMTEF', 'TMETR', 'TMMAE', 'TMOAL',
                 'TMMOR', 'TMLID', 'TLDYP', 'TLMAQ', 'TDCAA', 'TDCAS', 'TDCDS', 'TDCMP', 'TDCML']

excel_path = ruta_principal + ruta_posgrado  + nombre_archivo_excel_resumen
df.to_excel(excel_path, index=False)

string_vars = [f'G{var}' for var in numeric_vars]
for var in string_vars:
        df[var] = df[var[1:]].apply(generate_string_representation)

# Save to Excel
excel_path = ruta_principal + ruta_posgrado + nombre_archivo_excel
df.to_excel(excel_path, index=False)
print("Documento guardado exitosamente. excel")





'''

# Crear el DataFrame
data = {
    'Dimensiones': ['Aptitud Académica', 'Razonamiento Abstracto', 'Razonamiento Verbal', 'Uso del Lenguaje', 'Comprensión Lectora',
                     'Ajuste a las Normas Referenciales (sociales)', 'Control Social', 'Deseabilidad Social', 'Mentiras', 'Estabilidad y Normas',
                     'Desviación de las Normas Referenciales (sociales)', 'Desajuste', 'Impulsividad', 'Negativismo', 'Manipulación Social',
                     'Aspectos Potencializadores', 'Orientación al Logro', 'Autoeficacia', 'Maestría', 'Liderazgo', 'Autoestima',
                     'Aspectos Limitadores', 'Temor al Fracaso', 'Evitación del Trabajo Retador', 'Morosidad', 'Incomodidad Social',
                     'Inseguridad Personal'],
    'Puntaje': ['TDCAA', 'TARAR2', 'TARVAN', 'TARVUL', 'TARVCL', 'TDCAS', 'TPCSO', 'TPDES', 'TPMEN', 'TPEYN',
                'TDCDS', 'TPDPP', 'TPIMP', 'TLDYP', 'TLMAQ', 'TDCMP', 'TMOAL', 'TMAEF', 'TMMAE', 'TMLID', 'TMAES',
                'TDCML', 'TMTEF', 'TMETR', 'TMMOR', 'TPINS', 'TPINP']
}



# Crear el documento Word
doc = Document()

# Añadir encabezado
doc.add_heading('UNIVERSIDAD NACIONAL AUTÓNOMA DE', level=1)
doc.add_heading('Manual de Evaluación Psicológica (MEPSI)', level=2)
doc.add_heading('REPORTE INDIVIDUAL DE RESULTADOS', level=2)

# Agregar datos individuales
doc.add_paragraph('Nombre: NOMBRE')
doc.add_paragraph('Programa: PROGRAMA (AREA)')
doc.add_paragraph('Folio de control: FOLIO')
doc.add_paragraph('Fecha de evaluación: 12 de septiembre de 2023')

# Crear tabla
table = doc.add_table(rows=1, cols=3)
table.style = 'Table Grid'
hdr_cells = table.rows[0].cells
hdr_cells[0].text = 'Dimensiones'
hdr_cells[1].text = 'Puntaje'

for index, row in df.iterrows():
    row_cells = table.add_row().cells
    row_cells[0].text = row['Dimensiones']
    row_cells[1].text = row['Puntaje']

# Agregar pie de página
doc.add_paragraph('N.A. = No Aplica, se presenta cuando el alumno no completo el mínimo de respuestas para hacer válidos los valores de la prueba.')
doc.add_paragraph('FECHA DE IMPRESIÓN: 13 de septiembre de 2023')
doc.add_paragraph('DIRECCIÓN GENERAL DE ORIENTACIÓN Y ATENCIÓN EDUCATIVA')
doc.add_paragraph('DEPARTAMENTO DE INSTRUMENTOS DE ORIENTACIÓN, TEL 56 22 04 30')

# Guardar documento
doc.save('D:/DGOAE/2024/MEPSI/2025-1/marzo/UdPUNAM/Evaluacion/PCML/WordDocsreporte_resultados.docx')
'''

print("Data saved successfully.")

 

            
        
