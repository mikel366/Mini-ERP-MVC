from typing import List
from configuraciones.modelos import Venta, Pedido, Cliente, DetallePedido
from configuraciones.database import db
from peewee import DoesNotExist

class VentaControlador:
    @staticmethod
    def obtener_venta(venta_id: int) -> Venta:
        try:
            with db.atomic():
                venta: Venta = Venta.get_by_id(venta_id)
                return venta
        except:
            return None
    @staticmethod
    def listar_ventas(busqueda: str = None) -> List[Venta]:
        try:
            with db.atomic():
                ventas = Venta.select().order_by(Venta.id.desc())
                if busqueda:
                    ventas = ventas.join(Cliente).where(
                        (Cliente.nombre.contains(busqueda)) |
                        (Venta.fecha.contains(busqueda))
                    )
                return list(ventas)
        except Exception as e:
            print(f"Error en listar_ventas: {e}")
            return []
        
    @staticmethod
    def cambiar_estado(venta_id: int) -> Pedido:
        try:
            with db.atomic():
                # Obtener la venta
                venta: Venta = Venta.get_by_id(venta_id)
                
                # Verificar si el pedido original aún existe
                try:
                    pedido_original = Pedido.get_by_id(venta.pedido_id)
                    # Si existe, cambiar su estado de vuelta a pendiente (estado = 1)
                    from configuraciones.modelos import Estado
                    estado_pendiente = Estado.get_by_id(1)  # Asumiendo que 1 es pendiente
                    pedido_original.estado = estado_pendiente
                    pedido_original.save()
                    
                    # Eliminar la venta
                    venta.delete_instance()
                    return pedido_original
                    
                except DoesNotExist:
                    # Si el pedido original no existe, crear uno nuevo con sus detalles
                    from configuraciones.modelos import Estado
                    estado_pendiente = Estado.get_by_id(1)  # Estado pendiente
                    
                    pedido_nuevo = Pedido.create(
                        cliente=venta.cliente,
                        monto_final=venta.monto_final,
                        estado=estado_pendiente,
                        ganancia_total=venta.ganancia_total,
                        fecha=venta.fecha
                    )
                    
                    # Copiar los detalles del pedido original si existen
                    try:
                        detalles_originales = DetallePedido.select().where(DetallePedido.pedido_id == venta.pedido_id)
                        for detalle in detalles_originales:
                            # Verificar si ya existe este detalle para evitar duplicados
                            existing = DetallePedido.select().where(
                                (DetallePedido.pedido == pedido_nuevo) & 
                                (DetallePedido.producto == detalle.producto)
                            ).exists()
                            
                            if not existing:
                                DetallePedido.create(
                                    pedido=pedido_nuevo,
                                    producto=detalle.producto,
                                    cantidad=detalle.cantidad,
                                    subtotal=detalle.subtotal,
                                    ganancia_per_detalle=detalle.ganancia_per_detalle
                                )
                    except Exception as e:
                        print(f"No se pudieron copiar los detalles: {e}")
                    
                    # Eliminar la venta
                    venta.delete_instance()
                    return pedido_nuevo
                    
        except Exception as e:
            print(f"Error en cambiar_estado: {e}")
            return None
    @staticmethod
    def eliminar_venta(venta_id: int) -> bool:
        try:
            with db.atomic():
                venta: Venta = Venta.get_by_id(venta_id)
                venta.delete_instance()
                return True
        except:
            return False
        
    @staticmethod
    def eliminar_todas() -> bool:
        try:
            with db.atomic():
                Venta.delete().execute()
                return True
        except:
            return False