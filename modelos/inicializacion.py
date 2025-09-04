from .database import *
from .modelos import Estado, Cliente, Producto, Pedido, DetallePedido, Venta

def inicializar_bd():
    """Inicializa la base de datos y crea las tablas"""
    from .database import conectar_db, cerrar_conexion
    
    try:
        # Conectar a la base de datos
        conectar_db()
        
        # Crear tablas
        with db:
            db.create_tables([Estado, Cliente, Producto, Pedido, DetallePedido, Venta])
        
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