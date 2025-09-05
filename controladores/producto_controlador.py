# app/controladores/producto_controlador.py
from configuraciones.modelos import Producto
from peewee import DoesNotExist

class ProductoControlador:
    @staticmethod
    def registrar_producto(codigo, precio_compra, precio_venta, pagina):
        try:
            # Validar que el código no esté vacío
            if not codigo or not codigo.strip():
                return False, "El código no puede estar vacío"
            
            # Validar que la página sea un entero válido
            try:
                pagina_int = int(pagina)
                if pagina_int <= 0:
                    return False, "La página debe ser un número positivo"
            except ValueError:
                return False, "La página debe ser un número entero válido"
            
            # Validar que el precio sea un número válido
            try:
                precio_compra_float = float(precio_compra)
                if precio_compra_float <= 0:
                    return False, "El precio debe ser mayor a cero"
            except ValueError:
                return False, "El precio debe ser a número válido"
            
            # Validar que el precio de venta sea mayor al de compra
            try:
                precio_venta_float = float(precio_venta)
                if precio_venta_float <= precio_compra_float:
                    return False, "El precio de venta debe ser mayor al de compra"
            except ValueError:
                return False, "El precio de venta debe ser un número válido"
            
            
            # Validar que no se exceda el límite de 30 productos
            if Producto.select().count() >= 30:
                return False, "Límite máximo de 30 productos alcanzado"
            
            # Validar que el código no exista ya
            if Producto.select().where(Producto.codigo == codigo.strip()).exists():
                return False, "Ya existe un producto con este código"
            
            # Crear el nuevo producto
            Producto.create(codigo=codigo.strip(), precio_compra=precio_compra_float, precio_venta=precio_venta_float, pagina=pagina_int)
            return True, "Producto registrado exitosamente"
            
        except Exception as e:
            print(f"Error al registrar producto: {e}")
            return False, f"Error al registrar producto: {e}"
        
    @staticmethod
    def listar_productos(busqueda=None):
        try:
            query = Producto.select()
            if busqueda:
                query = query.where(
                    (Producto.codigo.contains(busqueda)) |
                    (Producto.pagina.contains(busqueda))
                )
            return [(producto.id, producto.pagina, producto.codigo, producto.precio_compra, producto.precio_venta) for producto in query]
        except Exception as e:
            print(f"Error al listar productos: {e}")
            return []
    
    @staticmethod
    def obtener_producto(id):
        try:
            return Producto.get(Producto.id == id)
        except DoesNotExist:
            return None
        except Exception as e:
            print(f"Error al obtener producto: {e}")
            return None
    
    @staticmethod
    def actualizar_producto(id, codigo, precio_compra, precio_venta, pagina):
        try:
            # Validar que la página sea un entero válido
            try:
                pagina_int = int(pagina)
                if pagina_int <= 0:
                    return False, "La página debe ser un número positivo"
            except ValueError:
                return False, "La página debe ser un número entero válido"
            
            # Validar que el código no esté vacío
            if not codigo or not codigo.strip():
                return False, "El código no puede estar vacío"
            
            # Validar que el precio sea un número válido
            try:
                precio_compra_float = float(precio_compra)
                if precio_compra_float <= 0:
                    return False, "El precio debe ser mayor a cero"
            except ValueError:
                return False, "El precio debe ser un número válido"
            
            # Validar que el precio de venta sea mayor al de compra
            try:
                precio_venta_float = float(precio_venta)
                if precio_venta_float <= precio_compra_float:
                    return False, "El precio de venta debe ser mayor al de compra"
            except ValueError:
                return False, "El precio de venta debe ser un número válido"
            
            producto = Producto.get(Producto.id == id)
            
            # Verificar si otro producto tiene el mismo código
            existing = Producto.select().where(
                (Producto.codigo == codigo.strip()) & 
                (Producto.id != id)
            )
            if existing.exists():
                return False, "Ya existe otro producto con este código"
            
            # Actualizar el producto
            producto.codigo = codigo.strip()
            producto.precio_compra = precio_compra_float
            producto.precio_venta = precio_venta_float
            producto.pagina = pagina_int
            producto.save()
            
            return True, "Producto actualizado exitosamente"
        except DoesNotExist:
            return False, "Producto no encontrado"
        except Exception as e:
            print(f"Error al actualizar producto: {e}")
            return False, f"Error al actualizar producto: {e}"
    
    @staticmethod
    def eliminar_producto(id):
        try:
            producto = Producto.get(Producto.id == id)
            producto.delete_instance()
            return True, "Producto eliminado exitosamente"
        except DoesNotExist:
            return False, "Producto no encontrado"
        except Exception as e:
            print(f"Error al eliminar producto: {e}")
            return False, f"Error al eliminar producto: {e}"
        
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
                Producto.delete().execute()
                return True
        except Exception as e:
            print(f"Error al eliminar todos los productos: {e}")
            return False