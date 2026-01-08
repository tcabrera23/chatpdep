@echo off
REM Script para ejecutar tests de ChatPdeP en Windows

echo 🧪 ChatPdeP - Suite de Tests
echo ==============================
echo.

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Activar entorno virtual si existe
if exist venv (
    echo 📦 Activando entorno virtual...
    call venv\Scripts\activate.bat
)

REM Instalar dependencias de testing
echo 📥 Verificando dependencias de testing...
pip install -q -r requirements-dev.txt

REM Verificar que el archivo .env existe
if not exist .env (
    echo ⚠️  ADVERTENCIA: Archivo .env no encontrado
    echo    Copia .env.example a .env y configura tus variables
    echo.
)

REM Verificar variables de entorno
echo.
echo 🔍 Verificando configuración...
if "%OPENROUTER_API_KEY%"=="" (
    echo ⚠️  OPENROUTER_API_KEY no configurada
)
if "%SUPABASE_URL%"=="" (
    echo ⚠️  SUPABASE_URL no configurada
)
if "%SUPABASE_SERVICE_KEY%"=="" (
    echo ⚠️  SUPABASE_SERVICE_KEY no configurada
)

echo.
echo ================================
echo.

REM Determinar qué tests ejecutar
if "%1"=="unit" (
    echo 🧪 Ejecutando tests unitarios...
    pytest tests/ -m unit -v
) else if "%1"=="integration" (
    echo 🔗 Ejecutando tests de integración...
    pytest tests/ -m integration -v
) else if "%1"=="judge" (
    echo ⚖️  Ejecutando tests con LLM-as-a-Judge...
    pytest tests/test_llm_judge.py -v
) else if "%1"=="quick" (
    echo ⚡ Ejecutando tests rápidos...
    pytest tests/ -m "not slow" -v
) else if "%1"=="coverage" (
    echo 📊 Ejecutando tests con coverage...
    pytest tests/ --cov=. --cov-report=html --cov-report=term
    echo.
    echo 📈 Reporte HTML generado en: htmlcov\index.html
) else (
    echo 🚀 Ejecutando TODOS los tests...
    pytest tests/ -v
)

REM Capturar código de salida
set EXIT_CODE=%ERRORLEVEL%

echo.
echo ================================
if %EXIT_CODE%==0 (
    echo ✅ Tests completados exitosamente
) else (
    echo ❌ Algunos tests fallaron (código: %EXIT_CODE%
)
echo ================================

exit /b %EXIT_CODE%

