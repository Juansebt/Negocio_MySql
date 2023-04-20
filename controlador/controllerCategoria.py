from app import app,mysql,miConexion
from flask import Flask, render_template, request

@app.route("/vistaCategoria")
def vistaCategoria():
    return render_template("frmCategoria.html")

def listarCategorias():
    mensaje=""
    try:
        cursor = miConexion.cursor()
        consulta = "select * from categorias"
        resultado = cursor.execute(consulta)
        listarCategorias = cursor.fetchall()
        return listarCategorias
    except mysql.err as error:
        mensaje = error

@app.route("/agregarCategoria",methods=["POST"])
def agregarCategoria():
    mensaje=""
    estado=False
    try:
        nombre = request.form["txtNombre"]
        categoria = (nombre,)
        cursor = miConexion.cursor()
        consulta = "insert into categorias values(null,%s)"
        resultado = cursor.execute(consulta,categoria)
        miConexion.commit()
        if(cursor.rowcount == 1):
            mensaje = "Categoria agregada correctamente"
            estado = True
        else:
            mensaje = "Problemas al agregar la categoria"
    except miConexion.Error as error:
        miConexion.rollback()
        mensaje= f"Error al agregar categoria{error}"
        
    return render_template("frmCategoria.html",estado=estado,mensaje=mensaje)