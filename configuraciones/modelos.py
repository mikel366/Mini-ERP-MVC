from decimal import Decimal
from peewee import *
import datetime
from .database import db

class BaseModel(Model):
    class Meta:
        database = db

class Estado(BaseModel):
    id = AutoField()
    id: int
    nombre = CharField(max_length=50, null=False, unique=True)
    nombre: str

    class Meta:
        table_name = 'estados'

class Cliente(BaseModel):
    id = AutoField()
    id: int
    nombre = CharField(max_length=100, null=False)
    nombre: str

    class Meta:
        table_name = 'clientes'

class Producto(BaseModel):
    id = AutoField()
    id: int
    codigo = CharField(max_length=50, unique=True, null=False)
    codigo: str
    precio_compra = DecimalField(max_digits=10, decimal_places=2, null=False)
    precio_compra: Decimal
    precio_venta = DecimalField(max_digits=10, decimal_places=2, null=False)
    precio_venta: Decimal
    pagina = IntegerField(null=True)
    pagina: int

    class Meta:
        table_name = 'productos'

class Pedido(BaseModel):
    id = AutoField()
    id: int
    cliente = ForeignKeyField(Cliente, backref='pedidos', null=False)
    cliente: Cliente
    monto_final = DecimalField(max_digits=12, decimal_places=2, null=False)
    monto_final: Decimal
    estado = ForeignKeyField(Estado, backref='pedidos', null=False)
    estado: Estado
    ganancia_total = DecimalField(max_digits=12, decimal_places=2, default=0)
    ganancia_total: Decimal
    fecha = DateTimeField(default=datetime.datetime.now)
    fecha: datetime.datetime

    class Meta:
        table_name = 'pedidos'

class DetallePedido(BaseModel):
    id = AutoField()
    id: int
    pedido = ForeignKeyField(Pedido, backref='detalles', null=False)
    pedido: Pedido
    producto = ForeignKeyField(Producto, backref='detalles', null=False)
    producto: Producto
    cantidad = IntegerField(null=False, default=1)
    cantidad: int
    subtotal = DecimalField(max_digits=10, decimal_places=2, null=False)
    subtotal: Decimal
    ganancia_per_detalle = DecimalField(max_digits=10, decimal_places=2, null=False)
    ganancia_per_detalle: Decimal

    class Meta:
        table_name = 'detalle_pedido'
        indexes = ((('pedido_id', 'producto_id'), True),)

class Venta(BaseModel):
    id = AutoField()
    id: int
    pedido_id = IntegerField(null=False)  # ID del pedido original
    pedido_id: int
    cliente = ForeignKeyField(Cliente, backref='ventas', null=False)
    cliente: Cliente
    monto_final = DecimalField(max_digits=12, decimal_places=2, null=False)
    monto_final: Decimal
    estado_id = IntegerField(null=False)
    estado_id: int
    ganancia_total = DecimalField(max_digits=12, decimal_places=2, default=0)
    ganancia_total: Decimal
    fecha = DateTimeField(null=False)
    fecha: datetime.datetime

    class Meta:
        table_name = 'ventas'
