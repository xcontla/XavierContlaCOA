# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 10:55:03 2022

@author: Xavier Contla
"""

import pymysql
import paramiko
import pandas as pd
from sshtunnel import SSHTunnelForwarder
from os.path import expanduser
import bcrypt

home = expanduser('~')
#mypkey = paramiko.DSSKey.from_private_key_file('./sshkeys/id_dsa', 'AN2t18yB*' ) # ,os.environ.get('rsa_password')) #if your private key is not password protected, then remove everything after the path to your key
mypkey = paramiko.DSSKey.from_private_key_file('D:/DGOAE/ssh/ssh/sshs/sshkeys/id_dsa', 'AN2t18yB*' ) # ,os.environ.get('rsa_password')) #if your private key is not password protected, then remove everything after the path to your key

# comments are the fields in SequelPro
MySQL_hostname = 'localhost' #MySQL Host
sql_username = 'orienta'#Username 
sql_password = 'fO5haK_b' #os.environ.get('sql_password') #Password
sql_main_database = 'mepsi' #Database Name
sql_port = 3306
ssh_host = '132.247.22.53' #SSH Host
ssh_user = 'orienta' #SSH Username
ssh_port = 2259
sql_ip = '1.1.1.1.1'

####################
## SQL_INSERTS
# {id_usuario}, {username}, {email}, {password}
create_usuario_mepsi = "INSERT INTO mepsi.usuario(id_usuario,c_username,c_email,c_password,b_status) VALUES  (%s ,%s,%s,%s,1);"
create_urol_mepsi = "INSERT INTO mepsi.usuariorol(id_usuario,id_rol,d_creacion) VALUES (%s,%s,now());"
create_udata_mepsi = "INSERT INTO mepsi.usuario_datos_alumno (id_usuario,c_apPaterno,c_apMaterno,c_nombres,c_sexo,d_fechaNacimiento, c_nacionalidad,c_correo,c_num_cuenta,c_posgrado_ingresar,c_nivel,c_licenciatura,c_posgrado,d_creacion,d_modificacion) VALUES ( %s ,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now());"

get_usuario_mepsi = "SELECT * FROM mepsi.usuario WHERE c_username LIKE %s or c_email LIKE  %s;"
update_usuario_datos_alumno_mepsi = "UPDATE mepsi.usuario_datos_alumno SET c_num_cuenta = %s, c_posgrado_ingresar = %s, c_nivel = %s, c_licenciatura = %s, c_posgrado = %s  WHERE id_usuario = %s;"
get_last_user = "SELECT id_usuario FROM mepsi.usuario ORDER BY id_usuario DESC LIMIT 1;"
get_usuario = "SELECT * FROM mepsi.usuario where c_username = %s;"
#####################

# saltar registros
t = []
lista_archivos_mepsi = [
     
     'D:/DGOAE/2026/MEPSI/2027_2/HIMFG/1. MEPSI_Formato_aplicación_HIMFG.xlsx',
    # 'D:/DGOAE/2026/MEPSI/2027_2/UDP/6OCTUBRE/MEPSI_2027-2_PP Produccion y de la Salud Animal.xlsx',
    # 'D:/DGOAE/2026/MEPSI/2027_2/UAEM/1. MEPSI_Formato_aplicación 2027-1 DC Y MC.xlsx',
    ]

nombre_pestania_registro = 'registrar'#'individual'#


with open("./MEPSI/2027_2/HIMFG/Registro_PROUNAM_II_UNAM_HIMFG.txt","a") as f:
    for nombre_archivo in lista_archivos_mepsi:
      
        with SSHTunnelForwarder((ssh_host, ssh_port),ssh_username=ssh_user,ssh_pkey=mypkey, remote_bind_address=(MySQL_hostname, sql_port)) as tunnel:

            conn = pymysql.connect(host='127.0.0.1', user=sql_username,
                           passwd=sql_password, db=sql_main_database,
                           port=tunnel.local_bind_port)

            cursor = conn.cursor()            
            num_anteriores = []
            ids_anteriores = []
            archivo = pd.read_excel(nombre_archivo,nombre_pestania_registro,header=0, dtype={'num':str,'paterno':str,'materno':str,'nombre':str,'sexo':str,'nacionalidad':str,'correo':str,'numcuenta':str,'pingresar':str,'licenciatura':str,'pass':str,'nivel':str,'posgrado':str})
            print(nombre_archivo)
            cursor.execute(get_last_user)      
            id_usuario_pivote =  cursor.fetchone()
            print(str(id_usuario_pivote[0]) + " ultimo registrado")
            id_usuario = id_usuario_pivote[0] + 1
            print("id_usuario: ", id_usuario_pivote[0]," ", id_usuario)
            f.write(nombre_archivo + "\n")
            
            for a in archivo.iloc:
                print(a['num'])
                record_usuario = ((a['correo']).strip(),(a['correo']).strip())
                
                cursor.execute(get_usuario_mepsi, record_usuario )
                row = cursor.fetchall()
                if cursor.rowcount > 0:
                    id_usr = row[0][0]
                    num_anteriores.append(str(a.iloc[0]))
                    ids_anteriores.append(str(id_usr))
            
                    if id_usr <= id_usuario_pivote[0]:
                        actualiza_datos = (str(a['numcuenta']).upper(), str(a['pingresar']).upper(), str(a['nivel']).upper(), str(a['licenciatura']).upper(), str(a['posgrado']).upper(), id_usr)
                        cursor.execute(update_usuario_datos_alumno_mepsi,actualiza_datos) 
                           
                else :
                    print("password:" + a['pass'])
                    cadena_a_encriptar_bytes = (a['pass']).strip().encode('utf-8')
                    salt = bcrypt.gensalt(rounds=10)
                    cadena_encriptada = bcrypt.hashpw(cadena_a_encriptar_bytes, salt)
                    cadena_encriptada = cadena_encriptada.decode("utf-8").replace("$2b", "$2a")
                    
                    record_usuario = (id_usuario, str(a['correo']).strip() , (a['correo']).strip() , cadena_encriptada)
                    #record_usuario = (id_usuario, "MVZ"+str(a['numcuenta']).strip() , (a['correo']).strip() , cadena_encriptada)
                    cursor.execute(create_usuario_mepsi, record_usuario )
                    record_usuario_rol = (id_usuario, 1)
                    cursor.execute(create_urol_mepsi, record_usuario_rol)
                    record_usuario_data = (id_usuario, str(a['paterno']).upper(), str(a['materno']).upper(), str(a['nombre']).upper(), str(a['sexo']).upper(),  str(a['fechanac']).split(' ',1)[0] , str(a['nacionalidad']).upper(), (a['correo']).strip(), str(a['numcuenta']).upper(), str(a['pingresar']).upper(), str(a['nivel']).upper(), str(a['licenciatura']).upper(), str(a['posgrado']).upper())
                    cursor.execute(create_udata_mepsi, record_usuario_data)
                    id_usuario = id_usuario + 1
                
                
            print(ids_anteriores)
            print(num_anteriores)
            f.write(str(id_usuario_pivote[0]+ 1) +" and " + str(id_usuario-1) +"\n")
            for iid in ids_anteriores:      
                f.write(str(iid) + ", ")
            f.write("\n")
            for iid in num_anteriores:    
                f.write(str(iid) + ", ")
                
            f.write("\n")
            f.write(str(nombre_archivo) + "\n")
        
                        
            conn.commit()
            conn.close()
        

f.close();
    