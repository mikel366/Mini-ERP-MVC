# build_exe.py - Script para crear ejecutable del ERP
"""
Script para generar ejecutable (.exe) del Mini ERP MVC
Utiliza PyInstaller para crear un ejecutable independiente
"""

import os
import sys
import subprocess
import shutil

def install_pyinstaller():
    """Instala PyInstaller si no está disponible"""
    try:
        import PyInstaller
        print("✓ PyInstaller ya está instalado")
        return True
    except ImportError:
        print("📦 Instalando PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✓ PyInstaller instalado exitosamente")
            return True
        except subprocess.CalledProcessError:
            print("❌ Error al instalar PyInstaller")
            return False

def create_executable():
    """Crea el ejecutable usando PyInstaller"""
    
    # Verificar que main.py existe
    if not os.path.exists("main.py"):
        print("❌ Error: No se encontró main.py en el directorio actual")
        return False
    
    # Comando PyInstaller con opciones optimizadas
    cmd = [
        "pyinstaller",
        "--onefile",                    # Crear un solo archivo ejecutable
        "--windowed",                   # Sin ventana de consola (para GUI)
        "--name=MiniERP",              # Nombre del ejecutable
        "--icon=icon.ico",             # Icono (opcional, si tienes uno)
        "--add-data=configuraciones;configuraciones",  # Incluir carpeta configuraciones
        "--add-data=controladores;controladores",      # Incluir carpeta controladores
        "--add-data=vistas;vistas",                    # Incluir carpeta vistas
        "--hidden-import=peewee",                      # Importación oculta para peewee
        "--hidden-import=tkinter",                     # Importación oculta para tkinter
        "--clean",                                     # Limpiar cache antes de construir
        "main.py"
    ]
    
    # Si no hay icono, remover esa opción
    if not os.path.exists("icon.ico"):
        cmd.remove("--icon=icon.ico")
        print("ℹ️  No se encontró icon.ico, continuando sin icono personalizado")
    
    print("🔨 Creando ejecutable...")
    print(f"Comando: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✓ Ejecutable creado exitosamente!")
        
        # Mostrar ubicación del ejecutable
        exe_path = os.path.join("dist", "MiniERP.exe")
        if os.path.exists(exe_path):
            print(f"📁 Ejecutable ubicado en: {os.path.abspath(exe_path)}")
            print(f"📊 Tamaño del archivo: {os.path.getsize(exe_path) / (1024*1024):.1f} MB")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al crear ejecutable: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def create_installer_script():
    """Crea un script batch para instalación fácil"""
    
    installer_content = '''@echo off
echo ================================================
echo     Mini ERP MVC - Instalador
echo ================================================
echo.

REM Crear carpeta en Archivos de Programa
set "INSTALL_DIR=%PROGRAMFILES%\\MiniERP"
echo Creando directorio de instalacion: %INSTALL_DIR%
mkdir "%INSTALL_DIR%" 2>nul

REM Copiar ejecutable
echo Copiando archivos...
copy "MiniERP.exe" "%INSTALL_DIR%\\MiniERP.exe"

REM Crear acceso directo en el escritorio
echo Creando acceso directo en el escritorio...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\Mini ERP.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\MiniERP.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'Sistema Mini ERP MVC'; $Shortcut.Save()"

REM Crear acceso directo en el menú inicio
echo Creando acceso directo en el menu inicio...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Mini ERP.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\MiniERP.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'Sistema Mini ERP MVC'; $Shortcut.Save()"

echo.
echo ================================================
echo     Instalacion completada exitosamente!
echo ================================================
echo.
echo El Mini ERP se ha instalado en: %INSTALL_DIR%
echo Se han creado accesos directos en:
echo - Escritorio
echo - Menu Inicio
echo.
echo Presiona cualquier tecla para salir...
pause >nul
'''
    
    with open("instalar_MiniERP.bat", "w", encoding="utf-8") as f:
        f.write(installer_content)
    
    print("✓ Script de instalación creado: instalar_MiniERP.bat")

def cleanup():
    """Limpia archivos temporales de PyInstaller"""
    dirs_to_clean = ["build", "__pycache__"]
    files_to_clean = ["MiniERP.spec"]
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🧹 Limpiado: {dir_name}/")
    
    for file_name in files_to_clean:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"🧹 Limpiado: {file_name}")

def main():
    """Función principal"""
    print("=" * 50)
    print("    MINI ERP MVC - GENERADOR DE EJECUTABLE")
    print("=" * 50)
    print()
    
    # Verificar e instalar PyInstaller
    if not install_pyinstaller():
        return
    
    print()
    
    # Crear ejecutable
    if create_executable():
        print()
        create_installer_script()
        print()
        
        # Preguntar si limpiar archivos temporales
        response = input("¿Desea limpiar archivos temporales? (s/n): ").lower()
        if response in ['s', 'si', 'sí', 'y', 'yes']:
            cleanup()
        
        print()
        print("=" * 50)
        print("           ¡PROCESO COMPLETADO!")
        print("=" * 50)
        print()
        print("📁 Archivos generados:")
        print("   - dist/MiniERP.exe (ejecutable principal)")
        print("   - instalar_MiniERP.bat (script de instalación)")
        print()
        print("📋 Instrucciones:")
        print("   1. Copia MiniERP.exe a cualquier PC")
        print("   2. Ejecuta instalar_MiniERP.bat como administrador")
        print("   3. ¡Listo! El ERP estará disponible desde el escritorio")
        
    else:
        print("❌ No se pudo crear el ejecutable")

if __name__ == "__main__":
    main()
