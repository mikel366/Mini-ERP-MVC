# app/controladores/usuario_controlador.py
from typing import List
from configuraciones.modelos import Cliente, Pedido
from peewee import DoesNotExist

class ClientesControlador:
    @staticmethod
    def registrar_cliente(nombre: str):
        try:
            # Validar que el nombre no esté vacío
            if not nombre or not nombre.strip():
                return False, "El nombre no puede estar vacío"
            
            # Validar que no se exceda el límite de 30 clientes
            if Cliente.select().count() >= 30:
                return False, "Límite máximo de 30 clientes alcanzado"
            
            # Crear el nuevo cliente
            Cliente.create(nombre=nombre.strip())
            return True, "Cliente registrado exitosamente"
            
        except Exception as e:
            print(f"Error al registrar usuario: {e}")
            return False, f"Error al registrar usuario: {e}"
        
    @staticmethod
    def listar_clientes(busqueda: str = None) -> List[Cliente]:
        try:
            query: List[Cliente] = Cliente.select()
            if busqueda:
                query = query.where(Cliente.nombre.contains(busqueda))
            return [(cliente.id, cliente.nombre) for cliente in query]
        except Exception as e:
            print(f"Error al listar clientes: {e}")
            return []
    
    @staticmethod
    def obtener_cliente(id: int) -> Cliente:
        try:
            return Cliente.get_by_id(id)
        except DoesNotExist:
            return None
        except Exception as e:
            print(f"Error al obtener cliente: {e}")
            return None
        
    @staticmethod
    def editar_cliente(id: int, nombre: str):
        try:
            # Validar que el nombre no esté vacío
            if not nombre or not nombre.strip():
                return False, "El nombre no puede estar vacío"
            
            cliente: Cliente = Cliente.get_by_id(id)
            cliente.nombre = nombre.strip()
            cliente.save()
            return True, "Cliente actualizado exitosamente"
        except DoesNotExist:
            return False, "Cliente no encontrado"
        except Exception as e:
            print(f"Error al editar cliente: {e}")
            return False, f"Error al editar cliente: {e}"
        
    @staticmethod
    def eliminar_cliente(id: int):
        try:
            cliente: Cliente = Cliente.get_by_id(id)
            
            # Verificar si el cliente tiene pedidos asociados
            if cliente.pedidos.count() > 0:
                return False, "No se puede eliminar el cliente porque tiene pedidos asociados"
            
            cliente.delete_instance()
            return True, "Cliente eliminado exitosamente"
        except DoesNotExist:
            return False, "Cliente no encontrado"
        except Exception as e:
            print(f"Error al eliminar cliente: {e}")
            return False, f"Error al eliminar cliente: {e}"

    @staticmethod
    def eliminar_todos() -> bool:
        try:
            from configuraciones.database import db
            with db.atomic():
                # Eliminar en orden correcto para respetar las relaciones
                from configuraciones.modelos import DetallePedido, Pedido, Venta
                DetallePedido.delete().execute()
                Venta.delete().execute()
                Pedido.delete().execute()
                Cliente.delete().execute()
                return True
        except Exception as e:
            print(f"Error al eliminar todos los clientes: {e}")
            return False