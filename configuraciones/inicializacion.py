from .database import db, conectar_db, cerrar_conexion
from .modelos import Estado, Cliente, Producto, Pedido, DetallePedido, Venta

def inicializar_bd():
    """Inicializa la base de datos y crea las tablas"""
    try:
        # Conectar a la base de datos
        conectar_db()
        
        # Crear tablas en el orden correcto (padres primero)
        db.create_tables([Estado, Cliente, Producto, Pedido, DetallePedido, Venta], safe=True)
        
        # Insertar estados predeterminados
        estados_predeterminados = [
            {'nombre': 'Pendiente'},
            {'nombre': 'Completado'},
            {'nombre': 'Cancelado'}
        ]
        for estado in estados_predeterminados:
            Estado.get_or_create(**estado)
        
        print("Base de datos inicializada correctamente")
        
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
    
    finally:
        # Cerrar conexión
        cerrar_conexion()
