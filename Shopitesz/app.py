from datetime import timedelta

from flask import Flask,render_template,request,redirect,url_for,flash,session,abort
from flask_bootstrap import Bootstrap
from modelo.Dao import db,Categoria,Producto,Usuario
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

@app.route('/Usuarios/todos')
@login_required
def ConsultaUsuarios():
    if current_user.is_admin():
        usuario = Usuario()
        return render_template('usuarios/consultaGeneral.html', usuarios=usuario.consultaGeneral())
    else:
        abort(404)

@app.route('/Usuarios/verPerfil')
@login_required
def verperfil():
    return render_template('usuarios/VerPerfil.html')

@app.route('/Usuarios/Editar')
@login_required
def Editar():
    return render_template('usuarios/Editar.html')

@app.route('/Usuarios/editarPerfil')
@login_required
def editarPerfil():
    try:

        usuario = Usuario()
        usuario.direccion = request.form['direccion']
        usuario.telefono = request.form['telefono']
        usuario.email = request.form['correo']
        usuario.password = request.form['password']
        usuario.editar()
        flash('¡ Usuario modificado con exito !')
        redirect('/Usuarios/verPerfil')
    except:
        flash('¡ Error al modificar al usuario !')

@app.route('/Usuarios/cerrarSesion')
@login_required
def cerrarSesion():
    logout_user()
    return redirect('/validarSesion')

@app.route("/validarSesion")
def validarSesion():
    return render_template('usuarios/login.html')

@app.route("/compra")
def compra():
    return render_template('carrito/compra.html')


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

if __name__=='__main__':
    db.init_app(app)#Inicializar la BD - pasar la configuración de la url de la BD
    app.run(debug=True)