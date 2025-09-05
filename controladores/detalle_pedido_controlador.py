from typing import List
from configuraciones.modelos import DetallePedido, Producto
from configuraciones.database import db
from peewee import DoesNotExist

class DetallePedidoControlador:
    @staticmethod
    def obtener_un_detalle(detalle_pedido_id: int) -> DetallePedido:
        try:
            with db.atomic():
                detalle_pedido: DetallePedido = DetallePedido.get_by_id(detalle_pedido_id)
                return detalle_pedido
        except:
            return None
        
    @staticmethod
    def actualizar_detalle(detalle_pedido_id: int, cantidad: int) -> DetallePedido:
        try:
            with db.atomic():
                detalle_pedido: DetallePedido = DetallePedido.get_by_id(detalle_pedido_id)
                detalle_pedido.cantidad = cantidad
                detalle_pedido.subtotal = Producto.precio_venta*cantidad
                detalle_pedido.ganancia_per_detalle = (Producto.precio_venta - Producto.precio_compra)*cantidad
                detalle_pedido.save()
                return detalle_pedido
        except:
            return None
    
    @staticmethod
    def eliminar_detalle(detalle_pedido_id: int) -> bool:
        try:
            with db.atomic():
                detalle_pedido: DetallePedido = DetallePedido.get_by_id(detalle_pedido_id)
                detalle_pedido.delete_instance()
                return True
        except:
            return False
        
    @staticmethod
    def obtener_detalle_completo_pedido(pedido_id: int) -> List[DetallePedido]:
        try:
            with db.atomic():
                detalle_pedido: List[DetallePedido] = DetallePedido.select().where(DetallePedido.pedido_id == pedido_id)
                return detalle_pedido
        except:
            return None
        
    @staticmethod
    def eliminar_todos() -> bool:
        try:
            with db.atomic():
                DetallePedido.delete().execute()
                return True
        except:
            return False