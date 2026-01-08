#!/bin/bash

# Script para ejecutar ChatPdeP localmente sin Docker

echo "🎓 ChatPdeP - Iniciando aplicación..."
echo ""

# Verificar si existe el archivo .env
if [ ! -f .env ]; then
    echo "⚠️  No se encontró el archivo .env"
    echo "📝 Creando .env desde .env.example..."
    cp .env.example .env
    echo ""
    echo "✅ Archivo .env creado. Por favor, edítalo con tus credenciales antes de continuar."
    echo "   Necesitas configurar:"
    echo "   - OPENROUTER_API_KEY"
    echo "   - OPENAI_API_KEY"
    echo "   - SUPABASE_URL"
    echo "   - SUPABASE_SERVICE_KEY"
    echo ""
    exit 1
fi

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python -m venv venv
    echo "✅ Entorno virtual creado"
    echo ""
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Instalar/actualizar dependencias
echo "📥 Instalando dependencias..."
pip install -r requirements.txt --quiet

# Crear directorio de datos si no existe
mkdir -p data

echo ""
echo "✅ Todo listo!"
echo "🚀 Iniciando Streamlit..."
echo ""

# Ejecutar la aplicación
streamlit run app.py

