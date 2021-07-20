from datetime import timedelta

from flask import Flask,render_template,request,redirect,url_for,flash,session,abort
from flask_bootstrap import Bootstrap
from modelo.Dao import db,Categoria
from flask_login import login_required,login_user,logout_user,current_user,LoginManager
app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://user_shopitesz:Cadete0420@@localhost/shopitesz'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='Cl4v3'

#Implementación de la gestion de usuarios con flask-login
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='mostrar_login'
login_manager.login_message='¡ Tu sesión expiró !'
login_manager.login_message_category="info"

@app.route("/")
def inicio():
    #return "Bienvenido a la tienda en linea Shipitesz
    return render_template('principal.html')
@app.route("/validarSesion")
def validarSesion():
    return render_template('usuarios/login.html')

@app.route("/Registrarse")
def Registrarse():
    return render_template('usuarios/registrarCuenta.html')

@app.route("/productos")
def Productos():
    return render_template('productos/consultaGeneral.html')

@app.route("/tarjeta")
def tarjeta():
    return render_template('Tarjeta/Tarjeta.html')

@app.route("/ticket")
def ticket():
    return render_template('Tarjeta/Ticket.html')

@app.route("/carrito")
def carrito():
    return render_template('pedidos/pagDetallesPedidos.html')

@app.route("/pedidos")
def Pedidos():
    return render_template('pedidos/pagPedidos.html')

@app.route("/Detallepedidos")
def DetallesPedidos():
    return render_template('pedidos/pagDetallesPedidos.html')

@app.route("/ProductosDescripcion1")
def Descripcion1():
    return render_template('productos/ProductosDescripcion/CAMISAANDROID.html')

@app.route("/ProductosDescripcion2")
def Descripcion2():
    return render_template('productos/ProductosDescripcion/CAMISACARRERA.html')

@app.route("/ProductosDescripcion3")
def Descripcion3():
    return render_template('productos/ProductosDescripcion/CAMISAGAMER.html')



@app.route("/Categorias")
def consultaCategorias():
    cat=Categoria()
    render_template('categorias/consultaGeneral.html',categorias=cat.consultaGeneral())



@app.route("/login",methods=['POST'])
def login():
    correo=request.form['correo']
    return "Validando al usuario"+correo

if __name__=='__main__':
    db.init_app(app) #Inicializando BD - pasa configuracion de la URL de la BD
    app.run(debug=True)
