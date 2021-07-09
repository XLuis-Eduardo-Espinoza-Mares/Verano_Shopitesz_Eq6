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

@app.route("/login",methods=['POST'])
def login():
    correo=request.form['correo']
    return "Validando al usuario"+correo
if __name__=='__main__':
    app.run(debug=True)
