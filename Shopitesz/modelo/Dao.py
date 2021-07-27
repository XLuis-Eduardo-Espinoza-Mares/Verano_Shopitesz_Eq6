from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer,String,BLOB,ForeignKey,Float,Date
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
db=SQLAlchemy()

class Categoria(db.Model):
    __tablename__='Categorias'
    idCategoria=Column(Integer,primary_key=True)
    nombre=Column(String,unique=True)
    estatus=Column(String,nullable=False)
    imagen=Column(BLOB)

    def consultaGeneral(self):
        return self.query.all()
        #return self.query.filter(Categoria.estatus=='Activa').all()

    def consultaIndividuall(self,id):
        return Categoria.query.get(id)

    def consultarImagen(self,id):
        return self.consultaIndividuall(id).imagen

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        cat=self.consultaIndividuall(id)
        db.session.delete(cat)
        db.session.commit()

    def eliminacionLogica(self,id):
        cat = self.consultaIndividuall(id)
        cat.estatus='Inactiva'
        cat.editar()

# class Producto(db.Model):
#     __tablename__='Productos'
#     idProducto=Column(Integer,primary_key=True)
#     idCategoria=Column(Integer,ForeignKey('Categorias.idCategoria'))
#     nombre=Column(String,nullable=False)
#     descripcion=Column(String,nullable=True)
#     precioVenta=Column(Float,nullable=False)
#     existencia=Column(Integer,nullable=False)
#     foto=Column(BLOB)
#     especificaciones=Column(BLOB)
#     estatus=Column(String,nullable=False)
#     categoria=relationship('Categoria',backref='productos',lazy='select')
#
#     def consultaGeneral(self):
#         return self.query.all()
#
# class Usuario(UserMixin,db.Model):
#     __tablename__='Usuarios'
#     idUsuario=Column(Integer,primary_key=True)
#     nombreCompleto=Column(String,nullable=False)
#     direccion=Column(String,nullable=False)
#     telefono=Column(String,nullable=False)
#     email=Column(String,unique=True)
#     password_hash=Column(String(128),nullable=False)
#     tipo=Column(String,nullable=False)
#     estatus=Column(String,nullable=False)
#     genero=Column(String,nullable=False)
#
#     @property #Implementa el metodo Get (para acceder a un valor)
#     def password(self):
#         raise AttributeError('El password no tiene acceso de lectura')
#
#     @password.setter #Definir el metodo set para el atributo password_hash
#     def password(self,password):#Se informa el password en formato plano para hacer el cifrado
#         self.password_hash=generate_password_hash(password)
#
#     def validarPassword(self,password):
#         return check_password_hash(self.password_hash,password)
#     #Definición de los métodos para el perfilamiento
#     def is_authenticated(self):
#         return True
#
#     def is_active(self):
#         if self.estatus=='Activo':
#             return True
#         else:
#             return False
#     def is_anonymous(self):
#         return False
#
#     def get_id(self):
#         return self.idUsuario
#
#     def is_admin(self):
#         if self.tipo=='Administrador':
#             return True
#         else:
#             return False
#     def is_vendedor(self):
#         if self.tipo=='Vendedor':
#             return True
#         else:
#             return False
#     def is_comprador(self):
#         if self.tipo=='Comprador':
#             return True
#         else:
#             return False
#     #Definir el método para la autenticacion
#     def validar(self,email,password):
#         usuario=Usuario.query.filter(Usuario.email==email).first()
#         if usuario!=None and usuario.validarPassword(password) and usuario.is_active():
#             return usuario
#         else:
#             return None
#     #Método para agregar una cuenta de usuario
#     def agregar(self):
#         db.session.add(self)
#         db.session.commit()
#
#
# class DetallePedidos(db.Model):
#     _tablename_ = 'DetallePedidos'
#     idDetalle = Column(Integer, primary_key=True)
#     idPedido = Column(Integer, ForeignKey('Pedidos.idPedidos'))
#     idProducto = Column(Integer, ForeignKey('Productos.idProductos'))
#     precio = Column(Float, nullable=False)
#     cantidadPedida = Column(String, nullable=False)
#     cantidadAceptada = Column(String, nullable=False)
#     cantidadRechazada = Column(String, nullable=False)
#     subtotal = Column(Float, nullable=False)
#     estatus = Column(String, nullable=False)
#     comentario = Column(String, nullable=False)
#
# class Tarjeta(db.Model):
#     _tablename_ = 'Tarjetas'
#     idTarjeta = Column(Integer, primary_key=True)
#     idUsuario = Column(Integer, ForeignKey('Usuarios.idUsuario'))
#     noTarjeta = Column(String, nullable=False)
#     saldo = Column(Float, nullable=False)
#     banco = Column(String, nullable=False)
#     estatus=Column(String, nullable=False)
#
# class Paqueteria(db.Model):
#     _tablename_ = 'PAQUETERIAS'
#     IDPAQUETERIA = Column(Integer, primary_key=True)
#     NOMBRE = Column(String, nullable=False)
#     PAGINAWEB = Column(String, nullable=False)
#     PRECIOGR = Column(Float, nullable=False)
#     TELEFONO = Column(Integer, nullable=False)
#     ESTATUS = Column(String, nullable=False)
#
# def consultaGeneral(self):
#         return self.query.all()
#
# class Pedido(db.Model):
#     tablename = 'Pedidos'
#     idPedido = Column(Integer, primary_key=True, nullable=False)
#     idComprador = Column(Integer, ForeignKey('Usuario.idUsuario'), nullable=False)
#     idVendedor = Column(Integer, ForeignKey('Usuario.idUsuario'), nullable=False)
#     idTarjeta = Column(String, ForeignKey('Tarjeta.idTarjeta'),nullable=False)
#     fechaRegistro = Column(String, nullable=False)
#     fechaAtencion = Column(String, nullable=False)
#     fechaRecepcion = Column(String, nullable=False)
#     fechaCierre = Column(String, nullable=False)
#     total = Column(Float, nullable=False)
#     estatus = Column(String, nullable=False)
#
# class Envios(db.Model):
#     __tablename__ = 'Envios'
#     idEnvio = Column(Integer, primary_key=True)
#     IDPEDIDO = Column(Integer, ForeignKey('Pedidos.idPedido'))
#     IDPAQUETERIA = Column(Integer, ForeignKey('Paqueterias.idPaqueteria'))
#     FECHAENVIO = Column(String, nullable=False)
#     FECHAENTREGA = Column(String, nullable=False)
#     NOGUIA = Column(String, nullable=False)
#     PESOPAQUETE = Column(Float, nullable=False)
#     PRECIOGR = Column(Float, nullable=False)
#     TOTALPAGAR = Column(Float, nullable=False)
#     ESTATUS = Column(String, nullable=False)
#
#     def consultaGeneral(self):
#         return self.query.all()