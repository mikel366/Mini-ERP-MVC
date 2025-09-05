@echo off
echo ================================================
echo     Mini ERP MVC - Instalador
echo ================================================
echo.

REM Crear carpeta en Archivos de Programa
set "INSTALL_DIR=%PROGRAMFILES%\MiniERP"
echo Creando directorio de instalacion: %INSTALL_DIR%
mkdir "%INSTALL_DIR%" 2>nul

REM Copiar ejecutable
echo Copiando archivos...
copy "dist\MiniERP.exe" "%INSTALL_DIR%\MiniERP.exe"

REM Crear acceso directo en el escritorio
echo Creando acceso directo en el escritorio...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\Mini ERP.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\MiniERP.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'Sistema Mini ERP MVC'; $Shortcut.Save()"

REM Crear acceso directo en el menú inicio
echo Creando acceso directo en el menu inicio...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\Mini ERP.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\MiniERP.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'Sistema Mini ERP MVC'; $Shortcut.Save()"

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
