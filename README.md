
We are going to create a README.md file for the project. The project is a Mini ERP system with Tkinter for the GUI and SQLite as the database, using the MVC pattern.

Since the user mentioned they removed the PedidosController and its view and took it out of the main for now, we will focus on the existing structure.

The README should include:

Project title

Description

Features (based on what is currently implemented: Clients and Products)

Installation and setup

How to run

Project structure

License (if any)

Let's assume the project is in an early stage with only Client and Product management.

Note: The user is planning to integrate the Pedidos (Orders) later, so we don't need to mention it in detail.

Let's write the README accordingly.

Mini ERP MVC
Una aplicación de escritorio para la gestión de negocio desarrollada en Python con Tkinter, utilizando el patrón MVC (Modelo-Vista-Controlador) y SQLite como base de datos.

🚀 Características
Gestión de Clientes: CRUD completo para administrar clientes

Gestión de Productos: Administración de inventario con precios y códigos

Interfaz Intuitiva: Interfaz de usuario fácil de usar con pestañas

Base de Datos Local: Almacenamiento SQLite para datos locales

Arquitectura MVC: Código organizado y mantenible

🛠️ Tecnologías Utilizadas
Python 3.x: Lenguaje de programación

Tkinter: Biblioteca para la interfaz gráfica

Peewee ORM: Mapeo objeto-relacional para la base de datos

SQLite: Motor de base de datos embebida

📦 Instalación
Clona el repositorio:

bash
git clone [URL_DEL_REPOSITORIO]
cd mini-erp-mvc
Crea un entorno virtual (recomendado):

bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
Instala las dependencias:

bash
pip install -r requirements.txt
🚀 Uso
Ejecuta la aplicación con:

bash
python main.py
La aplicación se iniciará con las siguientes pestañas disponibles:

👥 Clientes: Gestión de información de clientes

📦 Productos: Administración de inventario de productos

📁 Estructura del Proyecto
text
app/
├── controladores/          # Lógica de negocio
│   ├── __init__.py
│   ├── clientes_controlador.py
│   └── producto_controlador.py
├── modelos/               # Modelos de datos y base de datos
│   ├── __init__.py
│   ├── modelos.py
│   ├── database.py
│   └── inicializacion.py
├── vistas/                # Interfaces de usuario
│   ├── __init__.py
│   ├── clientes_vistas.py
│   └── productos_vistas.py
├── main.py               # Punto de entrada de la aplicación
└── requirements.txt      # Dependencias del proyecto
🔧 Funcionalidades Actuales
Gestión de Clientes
Crear nuevos clientes

Listar todos los clientes

Editar información de clientes existentes

Eliminar clientes

Búsqueda de clientes

Gestión de Productos
Registrar nuevos productos

Actualizar información de productos

Listar productos con búsqueda

Eliminar productos

Control de inventario

📋 Próximas Funcionalidades
Módulo de Pedidos y Compras

Módulo de Ventas

Reportes y estadísticas

Sistema de usuarios y permisos

Backup de base de datos

🤝 Contribución
Las contribuciones son bienvenidas. Para contribuir:

Haz un fork del proyecto

Crea una rama para tu feature (git checkout -b feature/AmazingFeature)

Commit tus cambios (git commit -m 'Add some AmazingFeature')

Push a la rama (git push origin feature/AmazingFeature)

Abre un Pull Request

📄 Licencia
Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

📞 Contacto
Si tienes preguntas o sugerencias, no dudes en abrir un issue o contactar al desarrollador.

Nota: Esta es una versión inicial de la aplicación. Algunas funcionalidades como el módulo de pedidos están en desarrollo y se integrarán en futuras versiones.# Mini-ERP-MVC
# Mini-ERP-MVC
# Mini-ERP-MVC
