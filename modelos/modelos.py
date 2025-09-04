from peewee import *
import datetime
from .database import db

class BaseModel(Model):
    """Modelo base que heredan todos los modelos"""
    class Meta:
        database = db

class Estado(BaseModel):
    id = AutoField(primary_key=True)
    nombre = CharField(max_length=50, null=False, unique=True)
    
    class Meta:
        table_name = 'estados'

class Cliente(BaseModel):
    id = AutoField(primary_key=True)
    nombre = CharField(max_length=100, null=False)
    
    class Meta:
        table_name = 'clientes'
        constraints = [SQL('CHECK (id BETWEEN 1 AND 30)')]

class Producto(BaseModel):
    id = AutoField(primary_key=True)
    codigo = CharField(max_length=50, unique=True, null=False)
    precio = DecimalField(max_digits=10, decimal_places=2, null=False)
    pagina = IntegerField(null=True)
    
    class Meta:
        table_name = 'products'

class Pedido(BaseModel):
    id = AutoField(primary_key=True)
    cliente = ForeignKeyField(Cliente, backref='pedidos', null=False)
    monto_final = DecimalField(max_digits=12, decimal_places=2, null=False)
    estado = ForeignKeyField(Estado, backref='pedidos', null=False)
    ganancia_total = DecimalField(max_digits=12, decimal_places=2, default=0)
    fecha = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        table_name = 'pedidos'

class DetallePedido(BaseModel):
    id = AutoField(primary_key=True)
    pedido = ForeignKeyField(Pedido, backref='detalles', null=False)
    producto = ForeignKeyField(Producto, backref='detalles', null=False)
    cantidad = IntegerField(null=False, default=1)
    subtotal = DecimalField(max_digits=10, decimal_places=2, null=False)
    ganancia_per_detalle = DecimalField(max_digits=10, decimal_places=2, null=False)
    precio_venta = DecimalField(max_digits=10, decimal_places=2, null=False)
    
    class Meta:
        table_name = 'detalle_pedido'
        indexes = (
            (('pedido', 'producto'), True),
        )

class Venta(BaseModel):
    id = AutoField(primary_key=True)
    cliente_id = IntegerField(null=False)
    monto_final = DecimalField(max_digits=12, decimal_places=2, null=False)
    estado_id = IntegerField(null=False)
    ganancia_total = DecimalField(max_digits=12, decimal_places=2, default=0)
    fecha = DateTimeField(null=False)
    fecha_migracion = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        table_name = 'ventas'
        