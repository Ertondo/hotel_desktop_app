import sqlite3    
    

conexion = sqlite3.connect("./DataBase/dbAppRes.db")


cursor = conexion.cursor()
consulta = '''SELECT HABITACIONES.id_habitacion, HABITACIONES.estado, HABITACIONES.tipo FROM HABITACIONES'''
cursor.execute(consulta)
#El método flechall trae todos los registros y fletchone trae de a uno
datos = cursor.fetchall()
cursor.close() 
conexion.close() 
 
for x in range(0,20):
    datos_dic = {"Habitación:": datos[x][0], "Estado:": datos[x][1],"Tipo:": datos[x][2]}
    
print(datos_dic)