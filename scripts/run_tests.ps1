# Script PowerShell para ejecutar tests de ChatPdeP
# Este script carga explícitamente las variables de entorno del .env

Write-Host "🧪 ChatPdeP - Suite de Tests (PowerShell)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Cambiar al directorio del script
Set-Location $PSScriptRoot

# Verificar que existe el archivo .env
if (-Not (Test-Path ".env")) {
    Write-Host "❌ Archivo .env no encontrado" -ForegroundColor Red
    Write-Host "   Copia .env.example a .env y configura tus variables" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

Write-Host "📥 Cargando variables de entorno desde .env..." -ForegroundColor Green

# Leer el archivo .env y cargar las variables
Get-Content ".env" | ForEach-Object {
    # Ignorar líneas vacías y comentarios
    if ($_ -match '^\s*$' -or $_ -match '^\s*#') {
        return
    }
    
    # Parsear la línea (formato: KEY=VALUE)
    if ($_ -match '^([^=]+)=(.*)$') {
        $key = $matches[1].Trim()
        $value = $matches[2].Trim()
        
        # Remover comillas si existen
        $value = $value -replace '^[''"]|[''"]$', ''
        
        # Establecer variable de entorno
        [Environment]::SetEnvironmentVariable($key, $value, "Process")
        Write-Host "   ✅ $key cargada" -ForegroundColor Gray
    }
}

Write-Host ""

# Activar entorno virtual si existe
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "📦 Activando entorno virtual..." -ForegroundColor Green
    & "venv\Scripts\Activate.ps1"
}

# Instalar dependencias de testing
Write-Host "📥 Verificando dependencias de testing..." -ForegroundColor Green
pip install -q -r requirements-dev.txt

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Determinar qué tests ejecutar según el parámetro
$testType = $args[0]

switch ($testType) {
    "unit" {
        Write-Host "🧪 Ejecutando tests unitarios..." -ForegroundColor Yellow
        pytest tests/ -m unit -v
    }
    "integration" {
        Write-Host "🔗 Ejecutando tests de integración..." -ForegroundColor Yellow
        pytest tests/ -m integration -v
    }
    "judge" {
        Write-Host "⚖️  Ejecutando tests con LLM-as-a-Judge..." -ForegroundColor Yellow
        pytest tests/test_llm_judge.py -v
    }
    "quick" {
        Write-Host "⚡ Ejecutando tests rápidos..." -ForegroundColor Yellow
        pytest tests/ -m "not slow" -v
    }
    "coverage" {
        Write-Host "📊 Ejecutando tests con coverage..." -ForegroundColor Yellow
        pytest tests/ --cov=. --cov-report=html --cov-report=term
        Write-Host ""
        Write-Host "📈 Reporte HTML generado en: htmlcov\index.html" -ForegroundColor Green
    }
    default {
        Write-Host "🚀 Ejecutando TODOS los tests..." -ForegroundColor Yellow
        pytest tests/ -v
    }
}

$exitCode = $LASTEXITCODE

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan

if ($exitCode -eq 0) {
    Write-Host "✅ Tests completados exitosamente" -ForegroundColor Green
} else {
    Write-Host "❌ Algunos tests fallaron (código: $exitCode)" -ForegroundColor Red
}

Write-Host "==========================================" -ForegroundColor Cyan

exit $exitCode

