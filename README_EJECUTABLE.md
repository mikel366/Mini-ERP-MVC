# 📦 Mini ERP MVC - Guía para Crear Ejecutable

## 🚀 Opción 1: Script Automático (RECOMENDADO)

### Paso 1: Ejecutar el script de construcción
```bash
python build_exe.py
```

Este script:
- ✅ Instala PyInstaller automáticamente
- ✅ Crea el ejecutable MiniERP.exe
- ✅ Genera script de instalación
- ✅ Limpia archivos temporales

### Paso 2: Distribuir
1. Copia `MiniERP.exe` y `instalar_MiniERP.bat` a cualquier PC
2. Ejecuta `instalar_MiniERP.bat` como administrador
3. ¡Listo! El ERP estará en el escritorio y menú inicio

---

## 🛠️ Opción 2: Manual con PyInstaller

### Instalar PyInstaller
```bash
pip install pyinstaller
```

### Crear ejecutable básico
```bash
pyinstaller --onefile --windowed --name=MiniERP main.py
```

### Crear ejecutable optimizado
```bash
pyinstaller --onefile --windowed --name=MiniERP --add-data="configuraciones;configuraciones" --add-data="controladores;controladores" --add-data="vistas;vistas" --hidden-import=peewee main.py
```

---

## 🎨 Opción 3: Auto-py-to-exe (Interfaz Gráfica)

### Instalar
```bash
pip install auto-py-to-exe
```

### Ejecutar
```bash
auto-py-to-exe
```

### Configuración recomendada:
- **Script Location**: main.py
- **Onefile**: One File
- **Console Window**: Window Based (hide the console)
- **Additional Files**: Agregar carpetas configuraciones, controladores, vistas
- **Output Directory**: dist

---

## 📋 Comparación de Opciones

| Método | Facilidad | Tamaño | Velocidad | Recomendado |
|--------|-----------|--------|-----------|-------------|
| **Script Automático** | ⭐⭐⭐⭐⭐ | ~15-25MB | Rápido | ✅ SÍ |
| **PyInstaller Manual** | ⭐⭐⭐⭐ | ~15-25MB | Rápido | ✅ SÍ |
| **Auto-py-to-exe** | ⭐⭐⭐⭐⭐ | ~15-25MB | Medio | ⚠️ Para principiantes |
| **cx_Freeze** | ⭐⭐⭐ | ~20-30MB | Medio | ❌ Más complejo |

---

## 🔧 Solución de Problemas

### Error: "No module named 'peewee'"
```bash
pip install peewee
```

### Error: "tkinter not found"
- En Ubuntu/Debian: `sudo apt-get install python3-tk`
- En Windows: Reinstalar Python con "tcl/tk and IDLE"

### Ejecutable muy grande
Usar `--exclude-module` para módulos no necesarios:
```bash
pyinstaller --onefile --windowed --exclude-module matplotlib --exclude-module numpy main.py
```

### Base de datos no funciona
Asegúrate de que la carpeta de la base de datos tenga permisos de escritura.

---

## 📁 Estructura Final

```
MiniERP/
├── MiniERP.exe                 # Ejecutable principal
├── instalar_MiniERP.bat       # Script de instalación
└── README_EJECUTABLE.md       # Esta guía
```

---

## 🎯 Ventajas del Ejecutable

- ✅ **Portabilidad**: Funciona en cualquier PC Windows sin Python
- ✅ **Profesional**: Acceso directo en escritorio y menú inicio
- ✅ **Independiente**: No requiere instalación de dependencias
- ✅ **Rápido**: Inicio inmediato de la aplicación
- ✅ **Seguro**: Base de datos SQLite local y privada

---

## 📞 Soporte

Si tienes problemas:
1. Verifica que Python esté instalado correctamente
2. Asegúrate de tener todas las dependencias: `pip install -r requirements.txt`
3. Ejecuta primero `python main.py` para verificar que funciona
4. Luego ejecuta `python build_exe.py`
