from datetime import timedelta
from flask import Flask,render_template,request,redirect,url_for,flash,session,abort
from flask_bootstrap import Bootstrap
from modelo.Dao import db,Categoria,Producto,Usuario,Tarjeta
from flask_login import login_required,login_user,logout_user,current_user,LoginManager
import json
app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://user_shopitesz:JoseKun@localhost/shopitesz'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='Cl4v3'

#Implementación de la gestion de usuarios con flask-login
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='mostrar_login'
login_manager.login_message='¡ Tu sesión expiró !'
login_manager.login_message_category="info"
#Implementación de la gestion de usuarios con flask-login
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='mostrar_login'
login_manager.login_message='¡ Tu sesión expiró !'
login_manager.login_message_category="info"

@app.before_request
def before_request():
    session.permanent=True
    app.permanent_session_lifetime=timedelta(minutes=10)

@app.route("/")
def inicio():
    #return "Bienvenido a la tienda en linea Shopitesz"
    return render_template('principal.html')

@login_manager.user_loader
def cargar_usuario(id):
    return Usuario.query.get(int(id))

@app.route('/Usuarios/agregar',methods=['post'])
def agregarUsuario():
    try:

        usuario = Usuario()
        usuario.nombreCompleto = request.form['nombres']
        usuario.telefono = request.form['telefono']
        usuario.direccion = request.form['direccion']
        usuario.email = request.form['correo']
        usuario.password = request.form['password']
        usuario.tipo = request.form['Tipo']
        usuario.estatus = 'Activo'
        usuario.agregar()
        flash('¡ Usuario registrado con éxito !')
        return render_template('usuarios/registrarCuenta.html')
    except:
        flash('¡ Error al agregar al usuario !')

@app.route("/Usuarios/validarSesion",methods=['POST'])
def login():
    if not current_user.is_authenticated:
        correo = request.form['correo']
        password = request.form['password']
        usuario = Usuario()
        user = usuario.validar(correo, password)
        if user != None:
            login_user(user)
            if current_user.is_active():
                return render_template('principal.html')
            else:
                logout_user()
                flash('Cuenta inactiva')
                return redirect(url_for('mostrar_login'))
        else:
            flash('Nombre de usuario o contraseña incorrectos')
            return render_template('usuarios/login.html')
    else:
        abort(404)


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

@app.route("/productos/Insertar")
def InsertarProductos():
    producto=Producto()

    return render_template("productos/Insertar.html", productos=producto.agregar())



#CRUD Tarjetas

@app.route("/tarjeta")
def tarjeta():
    return render_template('Tarjeta/Tarjeta.html')

@app.route('/Usuarios/verTarjetas/<int:id>')
@login_required
def verTarjetas(id):
    tar=Tarjeta()
    return render_template("/tarjetas/tarjetaregistrada.html",Tarjetas=tar.consultaGeneral(id))
@app.route('/usuarios/agregarNuevaTarjeta/<int:id>')
@login_required
def agregarTarjeta(id):
    if current_user.is_authenticated :
        return render_template("/tarjetas/tarjetas.html")
@app.route("/tarjetas/agregar/<int:id>",methods=['post'])
@login_required
def subirtarjeta(id):
    try:
        if current_user.is_authenticated:
                try:
                    tar = Tarjeta()
                    tar.idUsuario = request.form['ID']
                    tar.noTarjeta = request.form['noTarjeta']
                    tar.saldo = request.form['Saldo']
                    tar.banco = request.form['Banco']
                    tar.año = request.form['año']
                    tar.mes = request.form['mes']
                    tar.CCV = request.form['CCV']
                    tar.agregar()
                    flash('!tarjeta agregada con exito¡')
                except:
                    flash('! Error al agregar tarjeta¡')
                return render_template("/tarjetas/tarjetaregistrada.html",Tarjetas=tar.consultaGeneral(id))
        else:
            return redirect(url_for('mostrar_login'))
    except:
        #abort(500)
        return render_template("/")
@app.route('/Tarjeta/<int:id>')
@login_required
def EditarTarjetas(id):
    if current_user.is_authenticated():
        tar=Tarjeta()
        return render_template('tarjetas/editar.html', tar=tar.consulta(id))
    else:
        return redirect(url_for('mostrar_login'))
@app.route('/tarjeta/editar/<int:id>',methods=['POST'])
@login_required
def editandoTarjeta(id):
    if current_user.is_authenticated:
        try:
            tar = Tarjeta()
            tar.idUsuario = request.form['ID']
            tar.noTarjeta = request.form['noTarjeta']
            tar.saldo = request.form['Saldo']
            tar.banco = request.form['Banco']
            tar.año = request.form['año']
            tar.mes = request.form['mes']
            tar.CCV = request.form['CCV']
            tar.editar()
            flash('! Tarjeta editada con exito')
        except:
            flash('! Error al editar el producto')
        return render_template("/tarjetas/tarjetaregistrada.html",Tarjetas=tar.consultaGeneral(id))
    else:
        return redirect(url_for('mostrar_login'))
@app.route('/tarjeta/eliminar/<int:id>')
@login_required
def eliminarTarjeta(id):
    if  current_user.is_authenticated():
        try:
            tar=Tarjeta()
            tar.eliminar(id)
            flash('Tarjeta Eliminada')
        except:
            flash('Error al eliminar tarjeta')
        return redirect((url_for('verperfil')))
    else:
        return redirect(url_for('mostrar_login'))

@app.route('/tarjeta/saldo')
@login_required
def saldoTarjeta():
    if current_user.is_authenticated and current_user.is_comprador():
        tarjeta = Tarjeta()
        tarjeta = tarjeta.consultaGeneral(current_user.idUsuario)
        for t in tarjeta:
            dict_tarjeta = {"idTarjeta": t.idTarjeta, "saldo": t.saldo}
        return json.dumps(dict_tarjeta)
    else:
        msg = {"estatus": "error", "mensaje": "Debes iniciar sesion"}
        return json.dumps(msg)
#Fin CRUD Tarjetas


@app.route("/ticket")
def ticket():
    return render_template('Tarjeta/Ticket.html')

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


#incio de CRUD DE PRODUCTOS
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

@app.route('/productos/consultarprecioVenta/<int:id>')
def consultarprecioVenta(id):
    prod=Producto()
    return prod.consultarprecioVenta(id)

@app.route('/productos/consultarexistencia/<int:id>')
def consultarexistencia(id):
    prod=Producto()
    return prod.consultarexistencia(id)

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

if __name__=='__main__':
    db.init_app(app)#Inicializar la BD - pasar la configuración de la url de la BD
    app.run(debug=True)