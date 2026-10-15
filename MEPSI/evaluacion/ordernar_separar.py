# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 14:16:28 2025

@author: Xavier Contla
"""
import os
import pandas as pd
from PyPDF2 import PdfReader, PdfWriter

# Archivos de entrada

archivo_ordenar= 'Ordernar_Separar.xlsx'
nombre_pdf='MEPSI_SALUDANIMAL_20272.pdf' 

ruta_princial = './MEPSI/2027_2/'
#posgrado ='UAEM/'
posgrado='UDP/6OCTUBRE/SALUD_ANIMAL/'
folder_resultados='pdfs/'


pdf_path = ruta_princial + posgrado + folder_resultados + nombre_pdf # Cambia esto al nombre de tu archivo PDF
excel_path = ruta_princial + posgrado + folder_resultados + archivo_ordenar # Cambia esto al nombre de tu archivo Excel
output_base_folder = ruta_princial + posgrado + folder_resultados + 'separados/'     # Carpeta raíz donde guardar todo
paginas_por_archivo = 3

# Leer el Excel
df = pd.read_excel(excel_path)

# Validaciones de columnas
required_columns = {'nombre', 'carpeta', 'subcarpeta'}
if not required_columns.issubset(df.columns):
    raise Exception("El Excel debe tener columnas: 'nombre', 'carpeta' y 'subcarpeta'.")

# Leer el PDF
reader = PdfReader(pdf_path)

# Validar que haya el mismo número de páginas y filas
total_esperado = len(df) * paginas_por_archivo
if len(reader.pages) != total_esperado:
    raise Exception(f"El PDF tiene {len(reader.pages)} páginas pero el Excel tiene {len(df)} filas.")

# Procesar cada fila
for i, row in df.iterrows():
    nombre_archivo = str(row['nombre']).strip()
    carpeta = str(row['carpeta']).strip()
    subcarpeta = str(row['subcarpeta']).strip() if pd.notna(row['subcarpeta']) else ''

    # Construir ruta destino
    if subcarpeta:
        ruta_destino = os.path.join(output_base_folder, carpeta, subcarpeta)
    else:
        ruta_destino = os.path.join(output_base_folder, carpeta)

    # Crear carpeta si no existe
    
    print( "#################")
    print(ruta_destino)
    
    print( "#################")
    
    os.makedirs(ruta_destino, exist_ok=True)

    # Crear y guardar nueva página PDF
    writer = PdfWriter()
           
    inicio = i * paginas_por_archivo
    fin = inicio + paginas_por_archivo
    
    #writer.add_page(reader.pages[i])
    
    for pagina in range(inicio, fin):
       writer.add_page(reader.pages[pagina])
    
    path_final = os.path.join(ruta_destino, f"{nombre_archivo}.pdf")
    with open(path_final, 'wb') as f_out:
        writer.write(f_out)

    print(f"✅ Guardado: {path_final}")

print("\n🎉 Proceso finalizado con éxito.")
