#!/bin/bash

# Script para ejecutar tests de ChatPdeP

echo "🧪 ChatPdeP - Suite de Tests"
echo "=============================="
echo ""

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    echo "📦 Activando entorno virtual..."
    source venv/bin/activate
fi

# Instalar dependencias de testing si no están
echo "📥 Verificando dependencias de testing..."
pip install -q -r requirements-dev.txt

# Verificar variables de entorno
echo ""
echo "🔍 Verificando configuración..."
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "⚠️  OPENROUTER_API_KEY no configurada"
fi
if [ -z "$SUPABASE_URL" ]; then
    echo "⚠️  SUPABASE_URL no configurada"
fi
if [ -z "$SUPABASE_SERVICE_KEY" ]; then
    echo "⚠️  SUPABASE_SERVICE_KEY no configurada"
fi

echo ""
echo "================================"
echo ""

# Opción de tests a ejecutar
case "$1" in
    "unit")
        echo "🧪 Ejecutando tests unitarios..."
        pytest tests/ -m unit -v
        ;;
    "integration")
        echo "🔗 Ejecutando tests de integración..."
        pytest tests/ -m integration -v
        ;;
    "judge")
        echo "⚖️  Ejecutando tests con LLM-as-a-Judge..."
        pytest tests/test_llm_judge.py -v
        ;;
    "quick")
        echo "⚡ Ejecutando tests rápidos..."
        pytest tests/ -m "not slow" -v
        ;;
    "coverage")
        echo "📊 Ejecutando tests con coverage..."
        pytest tests/ --cov=. --cov-report=html --cov-report=term
        echo ""
        echo "📈 Reporte HTML generado en: htmlcov/index.html"
        ;;
    "all"|"")
        echo "🚀 Ejecutando TODOS los tests..."
        pytest tests/ -v
        ;;
    *)
        echo "❓ Uso: $0 [unit|integration|judge|quick|coverage|all]"
        echo ""
        echo "Opciones:"
        echo "  unit        - Solo tests unitarios"
        echo "  integration - Tests de integración"
        echo "  judge       - Tests con LLM-as-a-Judge"
        echo "  quick       - Tests rápidos (excluye lentos)"
        echo "  coverage    - Tests con reporte de cobertura"
        echo "  all         - Todos los tests (por defecto)"
        exit 1
        ;;
esac

# Capturar código de salida
EXIT_CODE=$?

echo ""
echo "================================"
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Tests completados exitosamente"
else
    echo "❌ Algunos tests fallaron (código: $EXIT_CODE)"
fi
echo "================================"

exit $EXIT_CODE

