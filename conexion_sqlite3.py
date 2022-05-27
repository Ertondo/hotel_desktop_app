###################################################################################
# REALIZA LA CONEXION CON LA DB Y DEFINE LOS METODOS DEL CRUD
# @Autor: Gustavo Armitano
# Email: gustavoarmitano@gmail.com
#
# METODOS: 
#           - inserta_pasajero
#           - mostrar_pasajero
#           - buscar_pasajero_nombre
#           - buscar_pasajero_dni
#           - editar_pasajero 
#           - eliminar_pasajero
#           - consultar_estado_habitaciones 
#           - consultar_registro
###################################################################################

import sqlite3

#Clase principal de conexión y desarrollo de la DB
class Conectar_db():

    #Método constructor
    def __init__(self):
        self.conexion = sqlite3.connect("./DataBase/dbAppRes.db")
        
    #TODO
        """PARA MAS ADELANTE
                USAR args Y kargs PARA QUE LAS CONSULTAS SIRVAN PARA TODAS LAS TABLAS
        def inserta_datos(self, args):
            bla....bla....bla
            return
        
        """
    
    #Agrega nuevos PASAJEROS
    def inserta_pasajero(self, dni, nombre, localidad, provincia, telefono, email, vehiculo, patente, estado, observaciones):
        #Abre el objeto cursor de la instacia de clase conexion
        cursor = self.conexion.cursor()
        #Guarda la consulta en un String
        consulta = ''' INSERT INTO pasajeros (id_pasajero, nombre, localidad, provincia, telefono, email, vehiculo, patente, estado, observaciones) 
                       VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')'''.format(dni, nombre, localidad, provincia, telefono, email, vehiculo, patente, estado, observaciones)
        #Ejecuta la consulta por medio de cursor
        cursor.execute(consulta)
        #Actualiza los datos en la DB
        self.conexion.commit()
        #Cierra la conexión
        cursor.close()
       
        return

    #Devuelve datos para mostrar    
    def mostrar_pasajero(self):
        cursor = self.conexion.cursor()
        consulta = '''SELECT * FROM pasajeros'''
        cursor.execute(consulta)
        #El método flechall trae todos los registros y fletchone trae de a uno
        datos = cursor.fetchall()
        return datos

    def buscar_pasajero_nombre(self, nombre):
        #nombre = str(nombre).upper
        cursor = self.conexion.cursor()
        consulta = ''' SELECT * FROM pasajeros WHERE nombre='{}' '''.format(nombre)
        cursor.execute(consulta)
        #El método flechall trae todos los registros y fletchone trae de a uno
        dato = cursor.fetchone()
        #Si el dato no existe le aviso
        if dato==[]:
            print("None")
            return dato
        else:
            print("Dato: ",dato)
            return dato

    def buscar_pasajero_dni(self, dni):

        cursor = self.conexion.cursor()
        consulta = ''' SELECT * FROM pasajeros WHERE id_pasajero='{}' '''.format(dni)
        cursor.execute(consulta)
        #El método flechall trae todos los registros y fletchone trae de a uno
        dato = cursor.fetchone()

        return dato

    def editar_pasajero(self, direccion, dni):
        #Abre el objeto cursor de la instacia de clase conexion
        cursor = self.conexion.cursor()
        #Guarda la consulta en un String
        consulta = ''' UPDATE PASAJEROS SET direccion='{}' WHERE id_pasajero='{}' '''.format(direccion, dni)
        #Ejecuta la consulta por medio de cursor
        cursor.execute(consulta)
        #Cantidad de actualizados
        cambios = cursor.rowcount
        #Actualiza los datos en la DB
        self.conexion.commit()
        #Cierra la conexión
        cursor.close()
        #Modifica el retorno de acuerdo al resultado
        if cambios:
            return "Actualización exitosa"
        else:
            return "Hubo un problema"

    def eliminar_pasajero(self, dni):
        #Abre el objeto cursor de la instacia de clase conexion
        cursor = self.conexion.cursor()
        #Guarda la consulta en un String
        consulta = ''' DELETE FROM PASAJEROS WHERE id_pasajero='{}' '''.format(dni)
        #Ejecuta la consulta por medio de cursor
        cursor.execute(consulta)
        #Cantidad de actualizados
        #cambios = cursor.rowcount()
        #Actualiza los datos en la DB
        self.conexion.commit()
        #Cierra la conexión
        cursor.close()
        return
    
    def consultar_estado_habitaciones(self):
        cursor = self.conexion.cursor()
        consulta = '''SELECT HABITACIONES.id_habitacion, HABITACIONES.estado, HABITACIONES.tipo FROM HABITACIONES'''
        cursor.execute(consulta)
        #El método flechall trae todos los registros y fletchone trae de a uno
        datos = cursor.fetchall()
        return datos
            
    def consultar_registro(self, habitacion):
        cursor = self.conexion.cursor()
        consulta = '''SELECT REGISTRO.referencia, PASAJEROS.nombre FROM REGISTRO, PASAJEROS WHERE REGISTRO.id_habitacion={} AND REGISTRO.id_pasajero1=PASAJEROS.id_pasajero'''.format(habitacion)
        cursor.execute(consulta)
        #El método flechall trae todos los registros y fletchone trae de a uno
        datos = cursor.fetchone()
        return datos
            