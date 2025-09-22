@echo off
echo Iniciando Jupyter Lab...
echo.

REM Ativar ambiente virtual
call .venv\Scripts\activate.bat

REM Iniciar Jupyter Lab
jupyter lab

pause
