from flask import Flask
app = Flask(__name__)

@app.route("/")
def inicio():
    return "Hola mundo"

@app.route("/login")
def login():
    return "otra ruta de prueba"

@app.route("/productos")
def consultarProductos():
    return "Retorna la lista de productos"

@app.route("/productos/agregar")
def agregarProducto():
    return "agregando un producto"

@app.route("/productos/actualizar")
def actualizarProducto():
    return "actualizando un producto"
@app.route("/cesta")
def consultarCesta():
    return "consultando la cesta de compra"

@app.route("/productos/categoria/<int:id>")
def consultarProductosCategoria(id):
    return "consultando los productos de la cetogoria: "+str(id)

@app.route("/clientes/<string:nombre>")
def consultarCliente(nombre):
    return "consultando al cliente:"+nombre

@app.route("/productos/<float:precio>")
def consultarPorductosPorPrecio(precio):
    return "Hola"+str(precio)

if __name__=='__main__':
    app.run(debug=True)

