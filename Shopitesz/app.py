from datetime import timedelta

from flask import Flask, render_template, request,redirect,url_for,flash,session,abort
from flask_bootstrap import Bootstrap
from modelo.Dao import db, Categoria, Producto
app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://user_shopitesz:Shopitesz.123@localhost/shopitesz'
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


#incio de CRUD DE PRODUCTOS


@app.route("/productos")
def consultarProductos():
    #return "Retorna la lista de productos"
    producto=Producto()
    cat = Categoria()
    return render_template("productos/consultaGeneral.html",productos=producto.consultaGeneral(),categorias=cat.consultaGeneral())

@app.route('/productos/consultarEspecificaciones/<int:id>')
def consultarEspecificionesProducto(id):
    prod=Producto()
    return prod.consultarEspecificaciones(id)

@app.route('/productos/consultarNombre/<int:id>')
def consultarNombreProducto(id):
    prod=Producto()
    return prod.consultarNombre(id)

@app.route('/productos/consultarImagen/<int:id>')
def consultarImagenProducto(id):
    prod=Producto()
    return prod.consultarImagen(id)

@app.route('/productos/nuevo')
def nuevoProducto():
            cat = Categoria()
            return render_template('productos/agregar.html', cat=cat.consultaGeneral())

@app.route("/productos/agregar",methods=['post'])
def agregarProducto():
                try:
                    prod=nuevoProducto();
                    prod.idCategoria=request.form['Categoria']
                    prod.nombre=request.form['nombre']
                    prod.descripcion=request.form['descripcion']
                    prod.precioVenta=request.form['precioventa']
                    prod.existencia=request.form['existencia']
                    prod.foto=request.files['foto'].stream.read()
                    prod.especificaciones=request.files['especificaciones'].stream.read()
                    prod.estatus ='Activo'
                    prod.agregar()
                    flash('!Producto agregado con exito!')
                except:
                    flash('! Error al agregar producto !')
                return redirect(url_for('consultarProductos'))


@app.route('/productos/<int:id>')
def consultaProductos(id):
        prod=Producto()
        cat=Categoria()
        return render_template('productos/editar.html',prod=prod.consultaIndividuall(id),cat=cat.consultaGeneral())


@app.route('/productos/editar',methods=['POST'])

def editarProducto():

        try:
            prod=Producto()
            prod.idProducto = request.form['id']
            prod.idCategoria=request.form['Categoria']
            prod.nombre=request.form['nombre']
            prod.descripcion = request.form['descripcion']
            prod.precioVenta = request.form['precioVenta']
            prod.existencia = request.form['existencia']
            especificaciones=request.files['especificaciones'].stream.read()
            foto=request.files['foto'].stream.read()
            if foto:
                prod.foto = foto
            if especificaciones:
                prod.especificaciones = especificaciones
            prod.estatus = request.form['estatus']
            prod.editar()
            flash('! Producto editado con éxito !')
        except:
            flash('! Error al editar el producto !')

        return redirect(url_for('consultarProductos'))



@app.route('/productos/eliminar/<int:id>')
def eliminarProductos(id):

        try:
            prod=Producto()
            prod.eliminacionLogica(id)
            flash('Producto eliminado con exito')
        except:
            flash('Error al eliminar el producto')

        return redirect(url_for('consultarProductos'))


@app.route('/productos/eliminacionfisica/<int:id>')

def eliminacionfisicaproducto(id):

        try:
            prod=Producto()
            prod.eliminar(id)
            flash('Producto eliminado')
        except:
            flash('Error al eliminar Producto')
        return redirect((url_for('consultarProductos')))

#Fin Cru de productos


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
