from datetime import timedelta

from flask import Flask,render_template,request,redirect,url_for,flash,session,abort
from flask_bootstrap import Bootstrap
from modelo.Dao import db,Categoria,Producto,Usuario, Tarjeta
from flask_login import login_required,login_user,logout_user,current_user,LoginManager
import json
app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://user_shopitesz:Shopitesz.123@localhost/shopitesz'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='Cl4v3'

#Implementación de la gestion de usuarios con flask-login
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='validarSesion'
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

# CRUD Usuarios
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
            return redirect(url_for('validarSesion'))
    else:
        return redirect(url_for('validarSesion'))

@app.route('/Usuarios/todos')
@login_required
def ConsultaUsuarios():
    if current_user.is_admin():
        usuario = Usuario()
        return render_template('usuarios/consultaGeneral.html', usuarios=usuario.consultaGeneral())
    else:
        return redirect(url_for('validarSesion'))

@app.route('/Usuarios/verPerfil')
@login_required
def verperfil():
    return render_template('usuarios/VerPerfil.html')

@app.route('/Usuarios/<int:id>')
@login_required
def usuarioIndividual(id):
        usuario = Usuario()
        return render_template('usuarios/consultaIndividual.html',usuario=usuario.consultaIndividual(id))

@app.route('/Usuarios/Editar')
@login_required
def Editar():
    return render_template('usuarios/Editar.html')

@app.route('/Usuarios/editarPerfil',methods=['POST'])
@login_required
def editarPerfil():
    try:

        usuario = Usuario()
        usuario.idUsuario = current_user.idUsuario
        usuario.nombreCompleto = current_user.nombreCompleto
        usuario.direccion = request.form['direccion']
        usuario.telefono = request.form['telefono']
        usuario.email = current_user.email
        usuario.password = request.form['password']
        if current_user.is_admin():
            usuario.estatus = request.form['estatus']
            usuario.tipo = request.form['Tipo']
        else:
            usuario.estatus = current_user.estatus
            usuario.tipo = current_user.tipo
        usuario.editar()
        flash('¡ Usuario modificado con exito !')
        return render_template('usuarios/VerPerfil.html')
    except:
        flash('¡ Error al modificar al usuario !')
        return render_template('usuarios/VerPerfil.html')

@app.route('/Usuarios/eliminar/<int:id>')
@login_required
def eliminarPerfil(id):
    if current_user.is_authenticated and current_user.idUsuario == id:
        try:
            usuario = Usuario()
            usuario.eliminacionLogica(id)
            logout_user()
            flash('Usuario eliminado con exito')
        except:
            flash('Error al eliminar el usuario')
        return redirect(url_for('inicio'))
    else:
        abort(404)

@app.route('/Usuarios/cerrarSesion')
@login_required
def cerrarSesion():
    logout_user()
    return redirect('/validarSesion')
#FIN CRUD Usuarios

@app.route("/validarSesion")
def validarSesion():
    return render_template('usuarios/login.html')

@app.route("/compra")
def compra():
    return render_template('carrito/compra.html')


@app.route("/Registrarse")
def Registrarse():
    return render_template('usuarios/registrarCuenta.html')
#CRUD Productos
@app.route("/productos")
def consultarProductos():
    #return "Retorna la lista de productos"
    producto=Producto()
    cat = Categoria()
    return render_template("productos/consultaGeneral.html",productos=producto.consultaGeneral(),categorias=cat.consultaGeneral())

@app.route('/productos/consultarImagen/<int:id>')
def consultarImagenProductos(id):
    prod=Producto()
    return prod.consultarImagen(id)

@app.route('/productos/consultarPDF/<int:id>')
def consultarPDFProductos(id):
    prod=Producto()
    return prod.consultarPDF(id)

@app.route('/productos/<int:id>')
@login_required
def consultaProducto(id):
    if current_user.is_authenticated and current_user.is_admin and current_user.is_vendedor:
        prod=Producto()
        cat=Categoria()
        return render_template('productos/editarProductos.html',prod=prod.consultaIndividuall(id),categorias=cat.consultaGeneral())
    else:
        return redirect(url_for('validarSesion'))

@app.route('/productos/nuevo')
@login_required
def nuevoProducto():
    if current_user.is_authenticated and current_user.is_admin and current_user.is_vendedor:
        cate = Categoria()
        return render_template('productos/nuevoProducto.html',categorias=cate.consultaGeneral())
    else:
        return redirect(url_for('validarSesion'))

@app.route('/productos/comprador/<int:id>')
@login_required
def consultaProductoC(id):
    if current_user.is_authenticated and current_user.is_comprador:
        prod = Producto()
        cat = Categoria()
        return render_template('productos/consultaProducto.html', prod=prod.consultaIndividuall(id),categorias=cat.consultaGeneral())
    else:
        return redirect(url_for('validarSesion'))

@app.route('/productos/guardar',methods=['POST'])
@login_required
def guardarProducto():
    if current_user.is_authenticated and current_user.is_admin  and current_user.is_vendedor:
        try:
            prod=Producto()
            prod.idCategoria=request.form['categoria']
            prod.nombre=request.form['nombre']
            prod.descripcion = request.form['descripcion']
            prod.precioVenta = request.form['precio']
            prod.existencia = request.form['existencia']
            foto = request.files['foto'].stream.read()
            if foto:
                prod.foto = foto
            especificaciones = request.files['pdf'].stream.read()
            if especificaciones:
                prod.especificaciones = especificaciones
            prod.estatus = 'Sin Valor'
            prod.editar()
            flash('! Producto editado con éxito !')
            return redirect(url_for('consultarProductos'))
        except:
            flash('! Error al editar el producto !')
    else:
        return redirect(url_for('validarSesion'))

@app.route('/productos/editar',methods=['POST'])
@login_required
def editarProducto():
    if current_user.is_authenticated and current_user.is_admin  and current_user.is_vendedor:
        try:
            prod=Producto()
            prod.idProducto = request.form['id']
            prod.idCategoria=request.form['categoria']
            prod.nombre=request.form['nombre']
            prod.descripcion = request.form['descripcion']
            prod.precioVenta = request.form['precio']
            prod.existencia = request.form['existencia']
            foto = request.files['foto'].stream.read()
            if foto:
                prod.foto = foto
            especificaciones = request.files['pdf'].stream.read()
            if especificaciones:
                prod.especificaciones = especificaciones
            prod.estatus = request.values.get("estatus","Inactiva")
            prod.editar()
            flash('! Producto editado con éxito !')
            return redirect(url_for('consultarProductos'))
        except:
            flash('! Error al editar el producto !')
    else:
        return redirect(url_for('validarSesion'))

@app.route('/productos/eliminar/<int:id>')
@login_required
def eliminarProductos(id):
    if current_user.is_authenticated and current_user.is_admin:
        try:
            prod=Producto()
            prod.eliminacionLogica(id)
            flash('Producto eliminado con exito')
            return redirect(url_for('consultarProductos'))
        except:
            flash('Error al eliminar el producto')
    else:
        return redirect(url_for('validarSesion'))

#Fin Productos

@app.route("/tarjeta")
def tarjeta():
    return render_template('Tarjeta/Tarjeta.html')
#CRUD Tarjetas
@app.route("/Tarjetas/Agrega",methods=['post'])
@login_required
def subirtarjeta():
    try:

        tar=Tarjeta()
        tar.idUsuario=current_user.idUsuario
        tar.noTarjeta=request.form['noTarjeta']
        tar.saldo=request.form['saldos']
        tar.banco=request.form['NombreTarjeta']
        tar.mes=request.form["Mes"]
        tar.año=request.form['Año']
        tar.CCV=request.form['ccv']
        tar.nombrePersona=request.form['Nombre']
        tar.agregar()
        flash('!tarjeta agregada con exito¡')
        return render_template('principal.html')
    except:
        flash('! Error al agregar tarjeta¡')

@app.route('/Tarjeta/<int:id>')
@login_required
def EditarTarjetas(id):
    if current_user.is_authenticated():
        tar=Tarjeta()
        return render_template('tarjetas/Tarjetas.html', tar=tar.consulta(id))
    else:
        return redirect(url_for('mostrar_login'))

#Fin Tarjetas

@app.route("/ticket")
def ticket():
    return render_template('Tarjeta/Ticket.html')

# CRUD Categorías
@app.route('/Categorias')
def consultaCategorias():
    cat=Categoria()
    return render_template('categorias/consultaGeneral.html',categorias=cat.consultaGeneral())

@app.route('/Categorias/agregar',methods=['post'])
@login_required
def agregarCategoria():
    try:
        cat=Categoria()
        cat.nombre=request.form['nombre']
        cat.imagen=request.files['imagen'].stream.read()
        cat.estatus='Sin Valor'
        cat.agregar()
        flash('Categoria agregada con exito')
        return redirect(url_for('consultaCategorias'))
    except:
        flash('Error al agregar la categoria')
        return render_template('usuarios/login.html')

@app.route('/Categorias/nueva')
@login_required
def nuevaCategoria():
    return render_template('categorias/agregarCategoria.html')

@app.route('/Categorias/consultarImagen/<int:id>')
def consultarImagenCategoria(id):
    cat=Categoria()
    return cat.consultarImagen(id)

@app.route('/Categorias/<int:id>')
@login_required
def consultarCategoria(id):
    cat=Categoria()
    return render_template('categorias/editarCategoria.html',cat=cat.consultaIndividuall(id))

@app.route('/Categorias/editar',methods=['POST'])
@login_required
def editarCategoria():
        try:
            cat=Categoria()
            cat.idCategoria=request.form['id']
            cat.nombre=request.form['nombre']
            imagen=request.files['imagen'].stream.read()
            if imagen:
                cat.imagen=imagen
            cat.estatus=request.values.get("estatus","Inactiva")
            cat.editar()
            flash('¡ Categoria editada con exito !')
        except:
            flash('¡ Error al editar la categoria !')

        return redirect(url_for('consultaCategorias'))

@app.route('/Categorias/eliminar/<int:id>')
@login_required
def eliminarCategoria(id):
        try:
            categoria=Categoria()
            categoria.eliminacionLogica(id)
            flash('Categoria eliminada con exito')
        except:
            flash('Error al eliminar la categoria')
        return redirect(url_for('consultaCategorias'))
#FIN Categorías

if __name__=='__main__':
    db.init_app(app)#Inicializar la BD - pasar la configuración de la url de la BD
    app.run(debug=True)