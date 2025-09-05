from peewee import SqliteDatabase

# Configuración de la conexión a la base de datos
db = SqliteDatabase('mi_tienda.db')

def conectar_db():
    """Establece conexión con la base de datos"""
    db.connect()
    return db

def cerrar_conexion():
    """Cierra la conexión con la base de datos"""
    if not db.is_closed():
        db.close()