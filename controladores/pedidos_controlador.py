from typing import List
from configuraciones.modelos import Pedido, DetallePedido, Producto, Venta, Cliente, Estado
from configuraciones.database import db
from datetime import datetime
from peewee import DoesNotExist

class PedidoControlador:
    @staticmethod
    def abrir_pedido(cliente_id) -> Pedido:
        try:
            with db.atomic():
                cliente = Cliente.get_by_id(cliente_id)
                estado = Estado.get_by_id(1)  # Estado pendiente
                pedido: Pedido = Pedido.create(
                    cliente=cliente,
                    monto_final=0,
                    estado=estado,
                    ganancia_total=0,
                    fecha=datetime.now(),
                )
                pedido.save()
                return pedido
        except Exception as e:
            print(f"Error en abrir_pedido: {e}")
            return None
        
    @staticmethod
    def crear_detalle_pedido(pedido_id:int, producto_id:int, cantidad:int=0) -> DetallePedido:
        try:
            with db.atomic():
                # Obtener el pedido y producto para calcular precios
                pedido = Pedido.get_by_id(pedido_id)
                producto = Producto.get_by_id(producto_id)
                subtotal = producto.precio_venta * cantidad
                ganancia = (producto.precio_venta - producto.precio_compra) * cantidad
                
                detalle: DetallePedido = DetallePedido.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=cantidad,
                    subtotal=subtotal,
                    ganancia_per_detalle=ganancia,
                )
                detalle.save()
                return detalle
        except Exception as e:
            print(f"Error creating detalle pedido: {e}")
            return None
        
    @staticmethod
    def crear_pedido(pedido_id: int, detalle: List[DetallePedido]) -> Pedido:
        try:
            with db.atomic():
                pedido: Pedido = Pedido.get_by_id(pedido_id)
                for d in detalle:
                    d.save()
                pedido.monto_final = sum([d.subtotal for d in detalle])
                pedido.ganancia_total = sum([d.ganancia_per_detalle for d in detalle])
                pedido.save()
                return pedido
        except:
            return None
        
    # actualizacion y migracion de datos a tabla ventas
    @staticmethod
    def actualizar_estado(pedido_id: int) -> Venta:
        try:
            with db.atomic():
                pedido: Pedido = Pedido.get_by_id(pedido_id)
                venta: Venta = Venta.create(
                    pedido_id=pedido.id,
                    cliente=pedido.cliente,
                    monto_final=pedido.monto_final,
                    estado_id=2,  # Estado completado para ventas
                    ganancia_total=pedido.ganancia_total,
                    fecha=datetime.now(),  # Fecha actual de la venta
                )
                venta.save()
                # eliminacion de pedido
                pedido.delete_instance()
                return venta
        except Exception as e:
            print(f"Error en actualizar_estado: {e}")
            return None
        
    @staticmethod
    def obtener_pedido(pedido_id: int) -> Pedido:
        try:
            with db.atomic():
                pedido: Pedido = Pedido.get_by_id(pedido_id)
                return pedido
        except:
            return None
        
    @staticmethod
    def eliminar_pedido(pedido_id: int) -> bool:
        try:
            with db.atomic():
                pedido: Pedido = Pedido.get_by_id(pedido_id)
                pedido.delete_instance()
                DetallePedido.delete().where(DetallePedido.pedido_id == pedido_id).execute()
                return True
        except:
            return False

    @staticmethod
    def eliminar_todos() -> bool:
        try:
            with db.atomic():
                Pedido.delete().execute()
                return True
        except:
            return False
        
    @staticmethod
    def listar_pedidos(busqueda: str = None) -> List[Pedido]:
        try:
            with db.atomic():
                pedidos = Pedido.select().order_by(Pedido.id.desc())
                if busqueda:
                    pedidos = pedidos.join(Cliente).where(
                        (Cliente.nombre.contains(busqueda)) |
                        (Pedido.fecha.contains(busqueda))
                    )
                return list(pedidos)
        except Exception as e:
            print(f"Error en listar_pedidos: {e}")
            return []