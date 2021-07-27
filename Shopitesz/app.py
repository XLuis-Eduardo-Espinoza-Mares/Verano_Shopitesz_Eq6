from datetime import timedelta

from flask import Flask, render_template, request,redirect,url_for,flash,session,abort
from flask_bootstrap import Bootstrap
from modelo.Dao import db, Categoria, Producto
app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://user_shopitesz:Cadete0420@localhost/shopitesz'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
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
def consultarProductos():
    #return "Retorna la lista de productos"
    producto=Producto()
    cat = Categoria()
    return render_template("productos/consultaGeneral.html",productos=producto.consultaGeneral(),categorias=cat.consultaGeneral())



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
@app.route("/compra")
def compra():
    return render_template('carrito/compra.html')



# CRUD Categorías
@app.route('/categorias')
def consultaCategorias():
    cat=Categoria()
    return render_template('categorias/consultaGeneral.html',categorias=cat.consultaGeneral())

@app.route('/Categorias/consultarImagen/<int:id>')
def consultarImagenCategoria(id):
    cat=Categoria()
    return cat.consultarImagen(id)
#FIN Categorías




@app.route("/login",methods=['POST'])
def login():
    correo=request.form['correo']
    return "Validando al usuario"+correo


if __name__=='__main__':
    db.init_app(app)    #Inicializando la BD
    app.run(debug=True)
