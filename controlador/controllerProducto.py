from app import app,mysql,miConexion
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import os

@app.route("/vistaProducto")
def vistaProducto():
    import controlador.controllerCategoria as cat
    listaCategorias = cat.listarCategorias()
    # listaCategorias = obtenerCategorias()
    producto = []
    print(listaCategorias)
    return render_template("frmProducto.html",listaCategorias=listaCategorias,producto=producto)


@app.route("/agregarProducto",methods=["POST"])
def agregarProducto():
    mensaje=""
    estado=False
    try:
        codigo = int(request.form["txtCodigo"])
        nombre = request.form["txtNombreP"]
        precio = int(request.form["txtPrecio"])
        categoria = int(request.form["cbCategoria"])
        producto = (codigo,nombre,precio,categoria)
        cursor = miConexion.cursor()
        consulta = "insert into productos values(null,%s,%s,%s,%s)"
        resultado = cursor.execute(consulta,producto)
        miConexion.commit()
        if(cursor.rowcount == 1):
            archivo = request.files["fileFoto"]
            nombreArchivo = secure_filename(archivo.filename)
            listaNombreArchivo = nombreArchivo.rsplit(".",1)
            extension = listaNombreArchivo[1].lower()
            
            #Obtener el ultimo id de la tabla producto
            productoConsultado = (codigo,)
            consultaID = "select idProducto from productos where proCodigo=%s"
            result = cursor.execute(consultaID,productoConsultado)
            idProducto = cursor.fetchone()[0]
            
            nuevoNombre = str(idProducto) + "." + extension
            
            #Guardar archivo en la carpeta
            archivo.save(os.path.join(app.config['UPLOAD_FOLDER'], nuevoNombre))
            
            mensaje = "Producto agregado correctamente"
            # producto = []
            # estado = True
            estadox,listaProductos = obtenerProductos()
            return render_template("listarProductos.html",mensaje=mensaje,listaProductos=listaProductos)
        else:
            mensaje = "Problemas al agregar el producto, por favor verificar!"
    except miConexion.Error as error:
        miConexion.rollback()
        mensaje= f"Error al agregar producto{error}"
        import controlador.controllerCategoria as cat
        listaCategorias = cat.listarCategorias()
        return render_template("frmProducto.html",estado=estado,mensaje=mensaje,listaCategorias=listaCategorias,producto=producto)
        
        
    # import controlador.controllerCategoria as cat
    # listaCategorias = cat.listarCategorias()
    # print(producto)
    # return render_template("frmProducto.html",estado=estado,mensaje=mensaje,listaCategorias=listaCategorias,producto=producto)

""""
def obtenerCategorias():
    cursor = miConexion.cursor()
    consulta = "select * from categorias"
    resultado = cursor.execute(consulta)
    listaCategorias = cursor.fetchall()
    return listaCategorias
"""

def obtenerProductos():
    try:
        cursor = miConexion.cursor()
        consulta = "select productos.*, categorias.catNombre from productos \
            inner join categorias on proCategoria=idCategoria"
        resultado = cursor.execute(consulta)
        productos = cursor.fetchall()
        return True,productos
    except mysql.Error as error:
        return False,error

@app.route("/listarProductos")
def listarProductos():
    estado,listaProductos = obtenerProductos()
    return render_template("listarProductos.html",listaProductos=listaProductos,estado=estado)

@app.route("/eliminar/<int:idProducto>",methods=["GET","POST"]) #eliminar metodo GET
def eliminar(idProducto):
    estado = False
    mensaje = ""
    try:
        # idProducto = request.args.get("idProducto")
        producto = (idProducto,)
        cursor = miConexion.cursor()
        consulta = "delete from productos where idProducto=%s"
        resultado = cursor.execute(consulta,producto)
        miConexion.commit()
        if(cursor.rowcount == 1):
            os.remove(app.config['UPLOAD_FOLDER']+"/"+str(idProducto)+".jpg")
            estado=True
            mensaje="Producto eliminado"
    except mysql.Error as error:
        miConexion.rollback()
        mensaje=error
    estado2,listaProductos = obtenerProductos()
    return render_template("listarProductos.html",listaProductos=listaProductos,estado=estado)

@app.route("/consultarProducto/<int:idProducto>")
def consultarProducto(idProducto):
    try:
        producto = (idProducto,)
        cursor = miConexion.cursor()
        consulta = consulta = "select productos.*, categorias.catNombre from productos \
            inner join categorias on proCategoria=idCategoria \
            where idProducto=%s"
        cursor.execute(consulta,producto)
        producto=cursor.fetchone()
        
        if(cursor.rowcount == 1):
            mensaje = "Datos del producto"
            import controlador.controllerCategoria as cat
            listaCategorias = cat.listarCategorias()
            return render_template("frmEditarProducto.html",producto=producto,listaCategorias=listaCategorias)
    except mysql.Error as error:
        mensaje = error
        return render_template("listarProductos")
    
@app.route("/actualizarProducto",methods=["POST"])
def actualizarProducto():
    mensaje = ""
    estado = True
    try:
        idProducto = int(request.form["idProducto"])
        #nuevos parametros
        nuevoCodigo = int(request.form["txtCodigo"])
        nuevoNombre = request.form["txtNombreP"]
        nuevoPrecio = int(request.form["txtPrecio"])
        nuevoCategoria = int(request.form["cbCategoria"])
        
        cursor = miConexion.cursor()
        productoActualizado = (nuevoCodigo,nuevoNombre,nuevoPrecio,nuevoCategoria,idProducto)
        
        consulta = "update productos set proCodigo=%s, proNombre=%s, proPrecio=%s, proCategoria=%s where idProducto=%s"
        resultado = cursor.execute(consulta,productoActualizado)
        miConexion.commit()
        
        # archivo = request.files["fileFoto"]
        # codigoAnterior = request.form["codigoAnterior"]
        
        # if(archivo):
        #     nombreArchivo = secure_filename(archivo.filename)
        #     print(nombreArchivo)
        #     extension = nombreArchivo.rsplit(".",1)[1].lower()
        #     nuevoNombreArchivo = str(nuevoCodigo)+"."+extension
        #     os.remove(app.config["UPLOAD_FOLDER"]+"/"+str(codigoAnterior)+".jpg")
        #     archivo.save(os.path.join(app.config["UPLOAD_FOLDER"],nuevoNombreArchivo))
        # elif(nuevoCodigo!=codigoAnterior):
        #     os.rename(app.config["UPLOAD_FOLDER"]+"/"+str(codigoAnterior)+".jpg",
        #                 app.config["UPLOAD-FOLDER"]+"/"+str(nuevoCodigo)+".jpg")
            
        if(cursor.rowcount == 1):
            print("Producto actualizado correctamente")
            estadox,listaProductos = obtenerProductos()
            return render_template("listarProductos.html",mensaje=mensaje,listaProductos=listaProductos)
        else:
            print("¡NO es posible actualizar el producto, por favor revisar...!")
    except mysql.Error as error:
        miConexion.rollback()
        mensaje=error
        import controlador.controllerCategoria as cat
        listaCategorias = cat.listarCategorias()
        productoActualizado = (idProducto,nuevoCodigo,nuevoNombre,nuevoPrecio,nuevoCategoria)
        return render_template("frmProducto.html",estado=estado,mensaje=mensaje,listaCategorias=listaCategorias,productoActualizado=productoActualizado)
        
    