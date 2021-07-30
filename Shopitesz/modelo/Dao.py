from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer,String,BLOB,ForeignKey,Float,Date
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
db=SQLAlchemy()

class Categoria(db.Model):
    __tablename__='categorias'
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

class Producto(db.Model):
    __tablename__='Productos'
    idProducto=Column(Integer,primary_key=True)
    idCategoria=Column(Integer,ForeignKey('categorias.idCategoria'))
    nombre=Column(String,nullable=False)
    descripcion=Column(String,nullable=True)
    precioVenta=Column(Float,nullable=False)
    existencia=Column(Integer,nullable=False)
    foto=Column(BLOB)
    especificaciones=Column(BLOB)
    estatus=Column(String,nullable=False)
    categoria=relationship('Categoria',backref='productos',lazy='select')

    def consultaGeneral(self):
        return self.query.all()

    def consultaIndividuall(self, id):
        return Producto.query.get(id)

    def consultarImagen(self, id):
        return self.consultaIndividuall(id).foto

    def consultarPDF(self, id):
        return self.consultaIndividuall(id).especificaciones

    def consultarNombre(self, id):
        return self.consultaIndividuall(id).nombre

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        prod=self.consultaIndividuall(id)
        db.session.delete(prod)
        db.session.commit()

    def eliminacionLogica(self,id):
        prod = self.consultaIndividuall(id)
        prod.estatus = 'Inactivo'
        prod.editar()


class Usuario(UserMixin,db.Model):
    __tablename__='Usuarios'
    idUsuario=Column(Integer,primary_key=True)
    nombreCompleto=Column(String,nullable=False)
    direccion=Column(String,nullable=False)
    telefono=Column(String,nullable=False)
    email=Column(String,unique=True)
    password_hash=Column(String(128),nullable=False)
    tipo=Column(String,nullable=False)
    estatus=Column(String,nullable=False)

    @property #Implementa el metodo Get (para acceder a un valor)
    def password(self):
        raise AttributeError('El password no tiene acceso de lectura')\

    @password.setter #Definir el metodo set para el atributo password_hash
    def password(self,password):#Se informa el password en formato plano para hacer el cifrado
        self.password_hash=generate_password_hash(password)

    def validarPassword(self,password):
        return check_password_hash(self.password_hash,password)
    #Definición de los métodos para el perfilamiento
    def is_authenticated(self):
        return True

    def is_active(self):
        if self.estatus=='Activo':
            return True
        else:
            return False
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.idUsuario

    def is_admin(self):
        if self.tipo=='Administrador':
            return True
        else:
            return False
    def is_vendedor(self):
        if self.tipo=='Vendedor':
            return True
        else:
            return False
    def is_comprador(self):
        if self.tipo=='Comprador':
            return True
        else:
            return False
    #Definir el método para la autenticacion
    def validar(self,email,password):
        usuario=Usuario.query.filter(Usuario.email==email).first()
        if usuario!=None and usuario.validarPassword(password):
            return usuario
        else:
            return None
    #Método para agregar una cuenta de usuario
    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def consultaGeneral(self):
        return self.query.all()

    def consultaIndividual(self,id):
        return self.query.get(id)

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminacionLogica(self,id):
        usuario = self.consultaIndividual(id)
        usuario.estatus = 'Inactivo'
        usuario.editar()

class Tarjeta(db.Model):
    __tablename__ = 'Tarjetas'
    idTarjeta = Column(Integer, primary_key=True)
    idUsuario = Column(Integer, ForeignKey('Usuarios.idUsuario'))
    noTarjeta = Column(String, nullable=False)
    saldo = Column(Float, nullable=False)
    banco = Column(String, nullable=False)
    mes=Column(Integer, nullable=False)
    año = Column(Integer, nullable=False)
    CCV = Column(Integer, nullable=False)
    nombrePersona = Column(String, nullable=False)

    def consultaGeneral(self,id):
        return self.query.filter(Tarjeta.idUsuario==id).all()

    def agregar(self):
        db.session.add(self)
        db.session.commit()
    def consulta(self, id):
        return Tarjeta.query.get(id)

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        tar = self.consulta(id)
        db.session.delete(tar)
        db.session.commit()

class Carrito(db.Model):
    __tablename__ ='Carrito'
    idCarrito = Column(Integer, primary_key=True)
    idUsuario = Column(Integer, ForeignKey('Usuarios.idUsuario'))
    idProducto = Column(Integer, ForeignKey ('Productos.idProducto'))
    fecha = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False)
    estatus = Column(String, nullable=False)

    def consultaGeneral(self,id):
        return self.query.filter(Carrito.idUsuario==id).all()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def consultaIndividual(self,id):
        return self.query.get(id)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def consulta(self, id):
        return Carrito.query.get(id)

    def eliminar(self, id):
        carrito = self.consulta(id)
        db.session.delete(carrito)
        db.session.commit()


class Pedido(db.Model):
    __tablename__ = 'Pedidos'
    idPedido = Column(Integer, primary_key=True, nullable=False)
    idComprador = Column(Integer, ForeignKey('Usuarios.idUsuario'), nullable=False)
    idVendedor = Column(Integer, ForeignKey('Usuarios.idUsuario'), nullable=False)
    idTarjeta = Column(Integer, ForeignKey('Tarjetas.idTarjeta'),nullable=False)
    fechaRegistro = Column(String, nullable=False)
    fechaAtencion = Column(String, nullable=False)
    fechaRecepcion = Column(String, nullable=False)
    fechaCierre = Column(String, nullable=False)
    total = Column(Float, nullable=False)
    estatus = Column(String, nullable=False)

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return self.query.get(id)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def consultaGeneral(self, id):
        return self.query.filter(Pedido.idComprador== id and Pedido.idVendedor==id).all()

class Paqueteria(db.Model):
    __tablename__='PAQUETERIAS'
    IDPAQUETERIA = Column(Integer, primary_key=True)
    NOMBRE = Column(String, nullable=False)
    PAGINAWEB = Column(String, nullable=False)
    PRECIOGR = Column(Float, nullable=False)
    TELEFONO = Column(Integer, nullable=False)
    ESTATUS = Column(String, nullable=False)

    def consultaGeneral(self):
        return self.query.all()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def consultaIndividual(self,id):
        return self.query.get(id)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

class Envio(db.Model):
    __tablename__='ENVIOS'
    IDENVIO = Column(Integer, primary_key=True)
    IDPEDIDO = Column(Integer, ForeignKey('Pedidos.idPedido'), nullable=False)
    IDPAQUETERIA = Column(Integer, ForeignKey('PAQUETERIAS.IDPAQUETERIA'), nullable=False)
    FECHAENVIO = Column(String)
    FECHAENTREGA = Column(String)
    NOGUIA = Column(String)
    PESOPAQUETE = Column(Float)
    PRECIOGR = Column(Float)
    TOTALPAGAR = Column(Float)
    ESTATUS = Column(String)

    def consultaGeneral(self):
        return self.query.all()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def consultaIndividual(self,id):
        return self.query.get(id)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

class DetallePedidos(db.Model):
    __tablename__ = 'DetallePedidos'
    idDetalle = Column(Integer, primary_key=True)
    idPedido = Column(Integer, ForeignKey('Pedidos.idPedido'))
    idProducto = Column(Integer, ForeignKey('Productos.idProducto'))
    precio = Column(Float, nullable=False)
    cantidadPedida = Column(Integer, nullable=False)
    cantidadEnviada = Column(Integer, nullable=False)
    cantidadAceptada = Column(Integer, nullable=False)
    cantidadRechazada = Column(Integer, nullable=False)
    subtotal = Column(Float, nullable=False)
    estatus = Column(String, nullable=False)
    comentario = Column(String, nullable=False)

    def consultaGeneral(self, id):
        return self.query.filter(DetallePedidos.idPedido== id).all()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return self.query.get(id)
