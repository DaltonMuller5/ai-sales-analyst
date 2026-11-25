@echo off
echo.
echo  ╔════════════════════════════════════╗
echo  ║   AI Sales Analyst  v1.0.0        ║
echo  ╚════════════════════════════════════╝
echo.

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo  ERRO: Python nao encontrado. Instale em https://python.org
    pause
    exit /b 1
)

if not exist ".venv" (
    echo  Criando ambiente virtual...
    python -m venv .venv
)

call .venv\Scripts\activate.bat
echo  Instalando dependencias...
pip install -r requirements.txt -q

echo.
echo  Backend:  http://localhost:8000
echo  API Docs: http://localhost:8000/docs
echo  Frontend: abrir frontend/index.html no navegador
echo.

uvicorn api.index:app --host 0.0.0.0 --port 8000 --reload
pause
