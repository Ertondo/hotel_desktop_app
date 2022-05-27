#####################################################################    
########    INTERFAZ DE REGISTRO DE HABITACIONES    #################
#####################################################################   

from vistas.Ui_ventana_registro_pasajeros import *
from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox
import conexion_sqlite3

lista_temp=[]

class Ventana(QDialog):
    def __init__(self, parent=None):
        super().__init__()

        #Instancio la clase ventana_registro_pasajero y llamo al metodo de inicio
        self.ventana_registro = Ventana_registro_pasajeros()
        self.ventana_registro.setupUi(self)
        
        #Dejo el foco en el dni
        self.ventana_registro.lineEdit_dni.setFocus(True)
        
        #Instancia de la conexion a la DB
        self.datos_DB = conexion_sqlite3.Conectar_db() 
        
        self.ventana_registro.btn_cancelar.clicked.connect(self.close)
        self.ventana_registro.btn_finalizar.clicked.connect(self.ocupar_habitacion)
        #Verifica que lo ingresado ya este carrgado en la DB
        self.ventana_registro.lineEdit_dni.editingFinished.connect(lambda: self.buscar_dni(self.ventana_registro.lineEdit_dni.text()))  
        
    
    def buscar_dni(self, dato):
        """#Si dato no esta vacio, busca el dni en la DB y llama al QMessagebox en caso de que exista

        Args:
            dato (str): dni ingresado en el lineEdit_dni
        """
        #Si la casiila tiene datos, lo busco en la DB
        if dato!="":
            resultado = self.datos_DB.buscar_pasajero_dni(dato)
       
        #Si existe, muestra mensaje
            if resultado!=None:
                self.ventana_registro.lineEdit_dni.clear()            
                print ("encontrado: ",resultado[1]) 
                self.msg_advertencia(resultado)
                self.ventana_registro.lineEdit_dni.setFocus()
            else:
                print("Nada")
            #return
        
        else:
            self.ventana_registro.lineEdit_dni.clear()
            self.ventana_registro.lineEdit_nombre.clear()              
            self.ventana_registro.lineEdit_dni.setFocus()
            return   
        
    #Mensaje de aviso por dato ya registrado
    def msg_advertencia(self, resultado):

        msg2=QMessageBox(self)
        msg2.setIcon(QMessageBox.Information)
        msg2.setWindowTitle("Documento encontrado en la BD")
        msg2.setText("¿Desea registrarlo en la habitación?")
        msg2.setInformativeText("""Documento: {}\nNombre: {}\nLocalidad: {}""".format(resultado[0],resultado[1],resultado[2]))
        msg2.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        result=msg2.exec_()
        
        if result == QMessageBox.Ok:

            #Carga la cantidad de filas actuales
            rowcount = self.ventana_registro.tabla_mostrar_pasajeros.rowCount()
            print("OK", rowcount) 
            #Muestra los datos en la tabla
            self.ventana_registro.tabla_mostrar_pasajeros.insertRow(rowcount)
            self.ventana_registro.tabla_mostrar_pasajeros.setItem(rowcount,0,QtWidgets.QTableWidgetItem(resultado[0]))
            self.ventana_registro.tabla_mostrar_pasajeros.setItem(rowcount,1,QtWidgets.QTableWidgetItem(resultado[1]))        
            self.ventana_registro.tabla_mostrar_pasajeros.setItem(rowcount,2,QtWidgets.QTableWidgetItem(resultado[2]))
            self.ventana_registro.tabla_mostrar_pasajeros.setItem(rowcount,3,QtWidgets.QTableWidgetItem(resultado[3]))        
                
            #Carga cada pasajero en un temporal, hasta confirmar 
            lista_temp.append((resultado[0]))
            lista_temp.append(resultado[1])        
            lista_temp.append(resultado[2])
            lista_temp.append(resultado[3])
            print("FinalOk")
            msg2.close()
        else:
            print("Finalcancel")
            msg2.close()  
        return

    #TODO Guardo los datos del pasajero en la DB
    def ocupar_habitacion(self):  
        print(lista_temp)       
        # for filas in range(0,len(datos_pasajeros)):        
        #     self.datos_DB.inserta_pasajero(datos_pasajeros[filas][0], datos_pasajeros[filas][1], datos_pasajeros[filas][2], datos_pasajeros[filas][3], 'telefono', 'email', 'vehiculo', 'patente', "activo", "observaciones")
    
    #Captura el evento de cierre de la ventana               
    def closeEvent(self, event):
        resultado = QMessageBox.information(self,"Si cierra se perderá toda la información", "¿Desea salir?",QMessageBox.Ok | QMessageBox.Cancel)
        if resultado==QMessageBox.Ok: 
            print(resultado)
            event.accept()
        else: 
            event.ignore()