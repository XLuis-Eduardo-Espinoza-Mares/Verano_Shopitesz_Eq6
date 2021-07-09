from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
app = Flask(__name__)
Bootstrap(app)

@app.route("/")
def inicio():
    #return "Bienvenido a la tienda en linea Shipitesz
    return render_template('principal.html')

@app.route("/validarSesion")
def validarSesion():
    return render_template('usuarios/login.html')

@app.route("/productos")
def Productos():
    return render_template('productos/consultaGeneral.html')

@app.route("/ProductosDescripcion1")
def Descripcion1():
    return render_template('productos/ProductosDescripcion/CAMISAANDROID.html')

@app.route("/ProductosDescripcion2")
def Descripcion2():
    return render_template('productos/ProductosDescripcion/CAMISACARRERA.html')

@app.route("/ProductosDescripcion3")
def Descripcion3():
    return render_template('productos/ProductosDescripcion/CAMISAGAMER.html')

@app.route("/login",methods=['POST'])
def login():
    correo=request.form['correo']
    return "Validando al usuario"+correo
if __name__=='__main__':
    app.run(debug=True)
