# Changelog - Mini ERP MVC

## [2.0.0] - 2025-01-05

### 🎉 Nuevas Características
- **Sistema ERP Completo**: Implementación completa de módulos de Clientes, Productos, Pedidos y Ventas
- **Ejecutable Windows**: Script automático para generar .exe con PyInstaller
- **Botón de Reinicio**: Reinicia la aplicación sin cerrarla manualmente
- **Eliminación Masiva**: Botones "Eliminar Todos" en todas las vistas con doble confirmación
- **Gestión de Ventas**: Conversión de pedidos a ventas con cálculo automático de ganancias
- **Reversión de Ventas**: Convierte ventas de vuelta a pedidos cuando sea necesario

### ⚡ Mejoras
- **Actualización en Tiempo Real**: Los dropdowns de clientes y productos se actualizan automáticamente
- **Interfaz Mejorada**: Confirmaciones de seguridad y mensajes informativos
- **Validaciones Robustas**: Validación de entrada en todos los formularios
- **Manejo de Errores**: Captura y manejo robusto de excepciones
- **Base de Datos Mejorada**: Eliminación en cascada y transacciones atómicas

### 🔧 Cambios Técnicos
- Refactorización completa de la arquitectura MVC
- Implementación de callbacks para sincronización entre vistas
- Optimización de consultas de base de datos
- Mejora en la gestión de dependencias

### 📁 Archivos Nuevos
- `build_exe.py` - Script para generar ejecutables
- `README_EJECUTABLE.md` - Guía completa para ejecutables
- `CHANGELOG.md` - Registro de cambios
- `.gitignore` - Configuración para Git
- `instalar_MiniERP.bat` - Script de instalación automática

### 🐛 Correcciones
- Corregidos errores de nombres de métodos inconsistentes
- Solucionados problemas de actualización de interfaz
- Mejorada la sincronización entre pestañas
- Corregidos errores de validación de datos

---

## [1.0.0] - 2024-12-XX

### 🎉 Lanzamiento Inicial
- **Gestión de Clientes**: CRUD básico para clientes
- **Gestión de Productos**: Administración de inventario
- **Interfaz Tkinter**: Interfaz gráfica con pestañas
- **Base de Datos SQLite**: Almacenamiento local con Peewee ORM
- **Arquitectura MVC**: Separación clara de responsabilidades
