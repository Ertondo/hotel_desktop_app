###################################################################################
# Archivo de entrada a la app Hotel
# Python Version 3.9.11
# Inerfaz gráfica realizada en QtDesigner V 5.11.1 y PyQt5 V 5.15.6
# inicio.py
#     \____estado_inicial_habitaciones.py
#     \____registro_pasajeros.py
#     \____reservas.py
###################################################################################

#IMPORTO DESDE ARCHIVOS PROPIOS
import registro_pasajeros
from vistas.Ui_mainWindows import *
import conexion_sqlite3
#IMPORTO DESDE PYTHON
import sys
#IMPORTO DESDE PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

#Clase de la ventana principal de la app
class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        #ui es una instacia de la interfaz creada en QtDesigner
        self.ui = MainWindow()
        #Llamo al método principal de la interfaz
        self.ui.setupUi(self)
        
        self.registro = registro_pasajeros.Ventana()

        #Instacio una conexion con la DB y consulto el estado de las habitacion
        self.cnn = conexion_sqlite3.Conectar_db()
        self.estado_habitaciones = self.cnn.consultar_estado_habitaciones()

        #Respuesta a eventos de los botones        
        self.ui.btn_ocupa_1.clicked.connect(self.boton)            
        self.ui.btn_consulta_1.clicked.connect(self.boton_2)
        
        #Lla al método que inicializa los box de cada habitación
        self.inicializa_main_windows()

    """                 
        Estado inicial de habitaciones
        ------------------------------
        
        Estados posibles: LIBRE - OCUPADA - RESERVADA - EN REPARACION 
        Etiquetas: lbl_estado, lbl_referencia, lbl_ocupa_libera 
        estado_habitaciones(list): (numero de habitación, estado, tipo)
        Botones: btn_ocupa_n, btn_libera_n, btn_consulta_n
    """ 
          
    def inicializa_main_windows(self):
        # INICIALIZO ETIQUETAS Y BOTONES
        for nro in range(1,21):
            #Cargo los datos del registro
            registro_del_dia = self.cnn.consultar_registro(nro)
            
            #Completo el label de estado
            exec(f"self.ui.lbl_estado_{nro}.setText(self.estado_habitaciones[{nro-1}][1])")
            
            #Si la habitación no esta libre
            if registro_del_dia!=None:
                exec(f"self.ui.lbl_ocupa_libera_{nro}.setText(registro_del_dia[1])")
                exec(f"self.ui.lbl_referencia_{nro}.setText(registro_del_dia[0])")
                
            #Dehabilito los botones según el estado de la habitación    
            if self.estado_habitaciones[nro-1][1]=="OCUPADA":
                exec(f"self.ui.btn_ocupa_{nro}.setEnabled(False)")
                exec(f"self.ui.btn_libera_{nro}.setEnabled(True)")
                exec(f"self.ui.btn_consulta_{nro}.setEnabled(True)")                
            elif self.estado_habitaciones[nro-1][1]=="LIBRE":
                exec(f"self.ui.btn_ocupa_{nro}.setEnabled(True)")
                exec(f"self.ui.btn_libera_{nro}.setEnabled(False)")
                exec(f"self.ui.btn_consulta_{nro}.setEnabled(False)")    
            elif self.estado_habitaciones[nro-1][1]=="RESERVADA":
                exec(f"self.ui.btn_ocupa_{nro}.setEnabled(True)")
                exec(f"self.ui.btn_libera_{nro}.setEnabled(False)")
                exec(f"self.ui.btn_consulta_{nro}.setEnabled(True)")    
            elif self.estado_habitaciones[nro-1][1]=="EN REPARACION":
                exec(f"self.ui.btn_ocupa_{nro}.setEnabled(False)")
                exec(f"self.ui.btn_libera_{nro}.setEnabled(True)")
                exec(f"self.ui.btn_consulta_{nro}.setEnabled(True)") 
        return   
                                                                                                                
    #####################################################################    
    ########       EVENTOS DE LOS BOTONES         #######################
    #####################################################################   
    #TODO si cambio el estado de la habitacion debo traer los datos de ocupación para actualizar en INICIO 
    def boton(self) -> None:
        """
        Método del botón Ocupar 
        _parameters: 
        
        
        """ 
        self.registro.exec_()
        estado_boton = self.ui.btn_ocupa_libera.text()
        if estado_boton=="OCUPAR":
            #Abre la ventana de registro    
            self.registro.exec_()
            self.ui.lbl_3.setText("OCUPADA")
            #FIXME debo traer los datos del momento desde registro_pasajeros
            self.ui.lbl_3.setText(self.estado_habitaciones[0][1])
            self.ui.boton.setText("LIBERAR")
        elif estado_boton=="RESERVAR":
            pass 
        elif estado_boton=="REPARAR":
            pass    
        elif estado_boton=="LIBERAR":
            msg=QMessageBox.information(self.registro,"Importante","¿Seguro que desea liberar?",QMessageBox.Ok | QMessageBox.Cancel)
            if msg==QMessageBox.Ok:
                self.ui.lbl_3.setText("LIBRE")
                self.ui.lbl_2.setText("")
                self.ui.boton.setText("OCUPAR")
                return

                    
    def boton_2(self):
        msg=QMessageBox.information(self.registro,"Importante","¿Seguro que desea liberar?",QMessageBox.Ok | QMessageBox.Cancel)
        if msg==QMessageBox.Ok:
            # self.ui.lbl_5.setText("LIBRE")
            # self.ui.lbl_6.setText("Sin novedad") 
            # self.ui.boton_2.setText("OCUPAR")
            return
        
    def boton_4(self):
        estado = self.estado_habitaciones

        for var in range(0, len(estado)):
            if estado[var][1]=="OCUPADA":
                print(f"{estado[var][0]} - {self.cnn.consultar_registro(estado[var][0])}")
                
    #####################################################################    
    ########  METODOS DE LAS HABITACIONES         #######################
    #####################################################################    
    
    def ocupar_habitacion(self):
        pass
    
    def liberar_habitacion(self):
        pass
    
    def reservar_habitacion(self):
        pass
    
    #Captura el evento de cierre de la ventana           
    # def closeEvent(self, event):
    #     resultado = QMessageBox.information(self,"Esta intentando cerrar la ventana", "¿Desea salir?",QMessageBox.Ok | QMessageBox.Cancel)
    #     if resultado==QMessageBox.Ok: event.accept()
    #     else: event.ignore()
    #     return                
      
if __name__=="__main__":
    app=QApplication(sys.argv)
    vent = Ventana()
    vent.show()
    sys.exit(app.exec_())