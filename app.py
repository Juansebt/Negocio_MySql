from flask import Flask, request, render_template
import pymysql as mysql

#crear objeto de tipo flask
app = Flask(__name__)

app.config['UPLOAD_FOLDER']='./static/images'

#conexión a base de datos
userBD = "root"
passBD = ""
baseDatos = "mi_negocio"
host = "localhost"
miConexion = mysql.connect(host=host,user=userBD,passwd=passBD,db=baseDatos)

#Raiz del sitio
@app.route("/")
def inicio():
    return render_template("inicio.html")

from controlador.controllerCategoria import *
from controlador.controllerProducto import *

#iniciar el servidor web
if __name__=='__main__':
    app.run(port=3000,debug=True)
    