from flask import Flask ,jsonify ,request
from flask_cors import CORS   
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app=Flask(__name__)  # crear el objeto app de la clase Flask
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend


# configuro la base de datos, con el nombre el usuario y la clave
#app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://LuisEscobar:vivero123@LuisEscobar.mysql.pythonanywhere-services.com/LuisEscobar$lirios'
#app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://eduz14:MyNewPass@eduz14.mysql.pythonanywhere-services.com/eduz14$losliriosBD'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:MyNewPass@localhost/liriosDB'
# URI de la BBDD driver de la BD  user:clave@URLBBDD/nombreBBDD

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow



# defino la tabla
class Producto(db.Model):   # la clase Producto hereda de db.Model
    codigo=db.Column(db.Integer, primary_key=True, autoincrement=True )   #define los campos de la tabla
    nombre=db.Column(db.String(100))
    descripcion=db.Column(db.String(200))
    precio=db.Column(db.Integer)
    stock=db.Column(db.Integer)
    categoria=db.Column(db.Enum('lirios','frutales','herramientas'))
    imagen=db.Column(db.String(400))

    def __init__(self,nombre,descripcion,precio,stock,categoria,imagen):   #crea el  constructor de la clase
        self.nombre=nombre   # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.descripcion=descripcion
        self.precio=precio
        self.stock=stock
        self.categoria=categoria
        self.imagen=imagen
   

with app.app_context(): #se crea un contexto de la app, esto nos permite poder acceder a la base de datos usando el objeto db
    db.create_all()  # aqui crea todas las tablas
#  ************************************************************
class ProductoSchema(ma.Schema): #definimos como se muestran los datos en la tabla
    class Meta:
        fields=('codigo','nombre','descripcion','precio','stock','categoria','imagen')

producto_schema=ProductoSchema()            # El objeto producto_schema es para traer un producto, creamos una instancia
productos_schema=ProductoSchema(many=True)  # El objeto productos_schema es para traer multiples registros de producto

# crea los endpoint o rutas (json)
@app.route('/productos',methods=['GET'])
def get_Productos():
    all_productos=Producto.query.all()         # el metodo query.all() lo hereda de db.Model
    result=productos_schema.dump(all_productos)  # el metodo dump() lo hereda de ma.schema y
                                                 # trae todos los registros de la tabla
    return jsonify(result)                       # retorna un JSON de todos los registros de la tabla, dump realiza la cerializacion




@app.route('/producto/<codigo>',methods=['GET'])
def get_producto(codigo):
    producto=Producto.query.get(codigo) #buscamos un producto mediante su codigo y lo asignamos a la variable producto
    return producto_schema.jsonify(producto)   # retorna el JSON de un producto recibido como parametro




@app.route('/delete/<codigo>',methods=['DELETE'])
def delete_producto(codigo):
    producto=Producto.query.get(codigo) #buscamos un producto mediante su codigo y lo asignamos a la variable producto
    db.session.delete(producto)
    db.session.commit()#confirmamos la eliminacion
    return producto_schema.jsonify(producto)   # me devuelve un json con el registro eliminado


@app.route('/producto', methods=['POST']) # crea ruta o endpoint
def create_producto():
    #print(request.json)  # request.json contiene el json que envio el cliente con los valores para cada variable
    nombre=request.json['nombre']
    descripcion=request.json['descripcion']
    precio=request.json['precio']
    stock=request.json['stock']
    categoria=request.json['categoria']
    imagen=request.json['imagen']
    new_producto=Producto(nombre,descripcion,precio,stock,categoria,imagen) #se crea una instancia de un nuevo producto
    db.session.add(new_producto)#agregamos el producto
    db.session.commit()#confirmamos
    return producto_schema.jsonify(new_producto)


@app.route('/update/<codigo>' ,methods=['PUT'])
def update_producto(codigo):
    producto=Producto.query.get(codigo)  #obtenemos un producto mediante su codigo

    #actualizamos los atributos del objeto producto con los valores proporcionados por el json que se recibe en la solicitud
    producto.nombre=request.json['nombre']
    producto.descripcion=request.json['descripcion']
    producto.precio=request.json['precio']
    producto.stock=request.json['stock']
    producto.categoria=request.json['categoria']
    producto.imagen=request.json['imagen']

    db.session.commit()
    return producto_schema.jsonify(producto)



# programa principal *******************************
if __name__=='__main__':
    app.run(debug=True, port=5000)    # ejecuta el servidor Flask en el puerto 5000

    #debug=true nos permite poder inspeccionar los errores
