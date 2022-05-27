
from flask import Flask, jsonify, request
from datetime import datetime
import sqlite3


app = Flask(__name__)


@app.route('/query', methods=['GET'])
def query():
    try:
        conexion = sqlite3.connect("./DataBase/dbAppRes.db")
    except Error as e:
        return {"message": "Conection failed"}

    cursor = conexion.cursor()
    consulta = '''SELECT HABITACIONES.id_habitacion, HABITACIONES.estado, HABITACIONES.tipo FROM HABITACIONES'''
    cursor.execute(consulta)
    #El método flechall trae todos los registros y fletchone trae de a uno
    datos = cursor.fetchall()
    cursor.close() 
    conexion.close()       
    for x in range(0,21):
        datos_dic = {"Habitación:": datos[x][0], "Estado:": datos[x][1],"Tipo:": datos[x][2]}
        
    return jsonify({"Habitación:": datos[0][0], "Estado:": datos[0][1],"Tipo:": datos[0][2]})

    
if __name__=="__main__":
    app.run(debug=True, port=5000)