@echo off
echo Instalando dependencias de Biometrika...
echo.

REM Crear entorno virtual si no existe
if not exist "venv_biometrika" (
    echo Creando entorno virtual...
    python -m venv venv_biometrika
)

REM Activar entorno virtual
echo Activando entorno virtual...
call venv_biometrika\Scripts\activate

REM Actualizar pip
echo Actualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo ¡Instalación completada!
echo.
echo Para activar el entorno virtual ejecuta:
echo venv_biometrika\Scripts\activate
pause