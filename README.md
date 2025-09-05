# Mini ERP MVC v2.0 🚀

Una aplicación de escritorio completa para la gestión empresarial desarrollada en Python con Tkinter, utilizando el patrón MVC (Modelo-Vista-Controlador) y SQLite como base de datos.

## ✨ Novedades en v2.0

- 🎯 **Sistema completo de ERP**: Clientes, Productos, Pedidos y Ventas
- 🗑️ **Eliminación masiva**: Botones "Eliminar Todos" con confirmaciones de seguridad
- 🔄 **Actualización en tiempo real**: Los dropdowns se actualizan automáticamente
- 🔄 **Botón de reinicio**: Reinicia la aplicación sin cerrarla
- 💼 **Ejecutable Windows**: Genera .exe para distribución fácil
- 📊 **Gestión de ventas**: Conversión de pedidos a ventas con cálculo de ganancias
- ↩️ **Reversión de ventas**: Convierte ventas de vuelta a pedidos

## 🚀 Características

- **Gestión de Clientes**: CRUD completo para administrar clientes
- **Gestión de Productos**: Administración de inventario con precios y códigos
- **Gestión de Pedidos**: Creación y administración de pedidos con múltiples productos
- **Gestión de Ventas**: Conversión de pedidos a ventas con cálculo automático de ganancias
- **Interfaz Intuitiva**: Interfaz de usuario moderna con pestañas y confirmaciones
- **Base de Datos Local**: Almacenamiento SQLite seguro y local
- **Arquitectura MVC**: Código organizado y mantenible
- **Ejecutable Independiente**: Genera .exe para distribución sin Python

## 🛠️ Tecnologías Utilizadas

- **Python 3.x**: Lenguaje de programación
- **Tkinter**: Biblioteca para la interfaz gráfica
- **Peewee ORM**: Mapeo objeto-relacional para la base de datos
- **SQLite**: Motor de base de datos embebida
- **PyInstaller**: Generación de ejecutables

## 📦 Instalación

### Opción 1: Ejecutable (Recomendado)
1. Descarga `MiniERP.exe` desde [Releases](../../releases)
2. Ejecuta `instalar_MiniERP.bat` como administrador
3. ¡Listo! Acceso directo en escritorio y menú inicio

### Opción 2: Código Fuente
```bash
git clone https://github.com/mikel366/Mini-ERP-MVC.git
cd Mini-ERP-MVC
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## 🚀 Uso

### Ejecutar desde código:
```bash
python main.py
```

### Generar ejecutable:
```bash
python build_exe.py
```

## 📁 Estructura del Proyecto

```
app/
├── configuraciones/        # Configuración de BD y modelos
│   ├── __init__.py
│   ├── database.py
│   ├── inicializacion.py
│   └── modelos.py
├── controladores/          # Lógica de negocio
│   ├── __init__.py
│   ├── clientes_controlador.py
│   ├── producto_controlador.py
│   ├── pedido_controlador.py
│   ├── detalle_pedido_controlador.py
│   └── venta_controlador.py
├── vistas/                # Interfaces de usuario
│   ├── __init__.py
│   ├── clientes_vistas.py
│   ├── productos_vistas.py
│   ├── pedidos_vistas.py
│   └── ventas_vistas.py
├── dist/                  # Ejecutables generados
├── main.py               # Punto de entrada
├── build_exe.py          # Script para generar .exe
├── requirements.txt      # Dependencias
└── README_EJECUTABLE.md  # Guía de ejecutables
```

## 🔧 Funcionalidades Completas

### 👥 Gestión de Clientes
- ✅ Crear, editar, eliminar clientes
- ✅ Búsqueda y filtrado
- ✅ Eliminación masiva con confirmación
- ✅ Validaciones de entrada

### 📦 Gestión de Productos
- ✅ CRUD completo de productos
- ✅ Códigos únicos y precios
- ✅ Control de inventario
- ✅ Búsqueda avanzada

### 📋 Gestión de Pedidos
- ✅ Creación de pedidos por cliente
- ✅ Agregar múltiples productos
- ✅ Cálculo automático de totales
- ✅ Conversión a ventas

### 💰 Gestión de Ventas
- ✅ Conversión automática desde pedidos
- ✅ Cálculo de ganancias
- ✅ Estadísticas y reportes
- ✅ Reversión a pedidos
- ✅ Exportación de datos

## 🎯 Flujo de Trabajo

1. **Registrar Clientes y Productos**
2. **Crear Pedidos** → Seleccionar cliente y agregar productos
3. **Convertir a Ventas** → Genera ganancia automáticamente
4. **Gestionar Ventas** → Ver estadísticas, revertir si es necesario

## 📊 Características Técnicas

- **Base de datos relacional** con integridad referencial
- **Eliminación en cascada** para mantener consistencia
- **Transacciones atómicas** para operaciones seguras
- **Validaciones de entrada** en todos los formularios
- **Manejo de errores** robusto
- **Interfaz responsiva** con actualización automática

## 🔄 Versiones

### v2.0 (Actual)
- Sistema ERP completo
- Ejecutable Windows
- Eliminación masiva
- Gestión de ventas

### v1.0
- Gestión básica de clientes y productos

## 🤝 Contribución

1. Fork del proyecto
2. Crear rama: `git checkout -b feature/AmazingFeature`
3. Commit: `git commit -m 'Add AmazingFeature'`
4. Push: `git push origin feature/AmazingFeature`
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

## 📞 Soporte

- 🐛 [Reportar bugs](../../issues)
- 💡 [Solicitar features](../../issues)
- 📖 [Documentación completa](README_EJECUTABLE.md)
