@echo off
echo Instalando dependencias do projeto...
echo.

REM Ativar ambiente virtual
call .venv\Scripts\activate.bat

REM Instalar dependencias
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo Instalacao concluida!
echo Para ativar o ambiente virtual, execute: .venv\Scripts\activate.bat
pause
