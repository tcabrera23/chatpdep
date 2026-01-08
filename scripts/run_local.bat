@echo off
REM Script para ejecutar ChatPdeP localmente en Windows sin Docker

echo 🎓 ChatPdeP - Iniciando aplicación...
echo.

REM Verificar si existe el archivo .env
if not exist .env (
    echo ⚠️  No se encontró el archivo .env
    echo 📝 Creando .env desde .env.example...
    copy .env.example .env
    echo.
    echo ✅ Archivo .env creado. Por favor, edítalo con tus credenciales antes de continuar.
    echo    Necesitas configurar:
    echo    - OPENROUTER_API_KEY
    echo    - OPENAI_API_KEY
    echo    - SUPABASE_URL
    echo    - SUPABASE_SERVICE_KEY
    echo.
    pause
    exit /b 1
)

REM Verificar si existe el entorno virtual
if not exist venv (
    echo 📦 Creando entorno virtual...
    python -m venv venv
    echo ✅ Entorno virtual creado
    echo.
)

REM Activar entorno virtual
echo 🔧 Activando entorno virtual...
call venv\Scripts\activate.bat

REM Instalar/actualizar dependencias
echo 📥 Instalando dependencias...
pip install -r requirements.txt --quiet

REM Crear directorio de datos si no existe
if not exist data mkdir data

echo.
echo ✅ Todo listo!
echo 🚀 Iniciando Streamlit...
echo.

REM Ejecutar la aplicación
streamlit run app.py

