# 🧪 Guía de Testing - ChatPdeP

## 📋 Resumen

ChatPdeP incluye una suite completa de tests que cubre:
- ✅ Tests unitarios de cada módulo
- ✅ Tests de integración del flujo completo
- ✅ Tests con LLM-as-a-Judge para evaluar calidad
- ✅ Tests de conexión a Supabase
- ✅ Tests de funcionalidades de la app

---

## 🚀 Quick Start

### Instalación de Dependencias

```bash
# Instalar dependencias de testing
pip install -r requirements-dev.txt
```

### Ejecutar Todos los Tests

```bash
# Linux/Mac
chmod +x run_tests.sh
./run_tests.sh

# Windows
run_tests.bat
```

---

## 📁 Estructura de Tests

```
tests/
├── __init__.py                  # Inicialización del paquete
├── conftest.py                  # Fixtures compartidos
├── test_rag_tool.py            # Tests de RAG/Supabase
├── test_file_extraction.py     # Tests de extracción de archivos
├── test_database.py            # Tests de SQLite
├── test_agents_config.py       # Tests de configuración de agentes
├── test_integration.py         # Tests de integración
└── test_llm_judge.py           # Tests con LLM-as-a-Judge ⭐
```

---

## 🎯 Tipos de Tests

### 1. Tests Unitarios

Tests rápidos que verifican componentes individuales:

```bash
# Ejecutar solo tests unitarios
./run_tests.sh unit
```

**Cobertura:**
- `test_rag_tool.py`: RAG y búsqueda semántica
- `test_file_extraction.py`: Extracción de PDFs e imágenes
- `test_database.py`: CRUD de conversaciones
- `test_agents_config.py`: Configuración de agentes

### 2. Tests de Integración

Tests que verifican el flujo completo:

```bash
# Ejecutar tests de integración
./run_tests.sh integration
```

**Cobertura:**
- Flujo completo RAG (buscar + formatear + usar)
- Integración LLM + RAG
- Conexión a Supabase
- Funciones RPC en Supabase

### 3. Tests con LLM-as-a-Judge ⭐

Tests que usan un LLM para evaluar la calidad de las respuestas:

```bash
# Ejecutar tests con juez LLM
./run_tests.sh judge
```

**Qué evalúa el juez:**
1. **Relevancia al Paradigma** (0-10): ¿Es específico del paradigma correcto?
2. **Corrección Técnica** (0-10): ¿La información es correcta?
3. **Claridad y Pedagogía** (0-10): ¿Es clara y útil?
4. **Completitud** (0-10): ¿Responde completamente?
5. **Uso del Contexto RAG** (0-10): ¿Usa bien la información recuperada?

**Ejemplo de evaluación:**

```json
{
  "relevancia_paradigma": 9,
  "correccion_tecnica": 8,
  "claridad_pedagogia": 9,
  "completitud": 8,
  "uso_contexto_rag": 9,
  "score_total": 8.6,
  "pasa_calidad": true,
  "paradigma_detectado": "Wollok",
  "paradigma_correcto": true,
  "analisis": "Respuesta excelente que explica objetos en Wollok con ejemplos claros.",
  "problemas_encontrados": []
}
```

---

## 🔧 Configuración

### Variables de Entorno Requeridas

Los tests necesitan las mismas variables que la app:

```env
OPENROUTER_API_KEY=sk-or-v1-...
SUPABASE_URL=https://...
SUPABASE_SERVICE_KEY=eyJ...
```

⚠️ **Sin estas variables**, los tests se saltarán automáticamente.

### ⚠️ Problema Común en Windows

Si los tests se saltan con "Variables de entorno faltantes" pero tienes el `.env` configurado:

**Solución 1: Verificar variables**

```bash
python check_env.py
```

Este script te mostrará si las variables se están cargando correctamente.

**Solución 2: Ejecutar desde la raíz del proyecto**

```bash
# Asegúrate de estar en la raíz del proyecto
cd "C:\Users\tomas\OneDrive\Desktop\Apertura IA\ChatPdeP_web\agents_pdep"

# Luego ejecuta los tests
run_tests.bat
```

**Solución 3: Cargar variables manualmente en PowerShell**

```powershell
# Cargar cada variable manualmente
$env:OPENROUTER_API_KEY="tu-clave-aqui"
$env:SUPABASE_URL="tu-url-aqui"
$env:SUPABASE_SERVICE_KEY="tu-clave-aqui"

# Luego ejecutar pytest directamente
pytest tests/ -v
```

**Solución 4: Usar pytest directamente con .env**

```bash
# Instalar pytest-dotenv
pip install pytest-dotenv

# Ejecutar tests
pytest tests/ -v
```

---

## 📊 Opciones de Ejecución

### Tests Rápidos (Excluye LLM Judge)

```bash
./run_tests.sh quick
```

### Tests con Coverage

```bash
./run_tests.sh coverage
# Genera reporte HTML en: htmlcov/index.html
```

### Tests Específicos

```bash
# Un archivo específico
pytest tests/test_rag_tool.py -v

# Un test específico
pytest tests/test_rag_tool.py::TestSupabaseRAG::test_search_theory_wollok -v

# Por marcador
pytest -m "rag" -v
```

---

## 🎭 Marcadores de Tests

Los tests están marcados para ejecutarlos selectivamente:

```python
@pytest.mark.unit          # Tests unitarios rápidos
@pytest.mark.integration   # Tests de integración
@pytest.mark.slow          # Tests lentos (con LLMs)
@pytest.mark.judge         # Tests con LLM-as-a-Judge
@pytest.mark.database      # Tests de base de datos
@pytest.mark.rag           # Tests de RAG/Supabase
```

**Ejemplos:**

```bash
# Solo tests de RAG
pytest -m rag -v

# Excluir tests lentos
pytest -m "not slow" -v

# Tests de integración y base de datos
pytest -m "integration or database" -v
```

---

## 📈 Interpretación de Resultados

### Salida Típica

```
================================ test session starts =================================
platform linux -- Python 3.11.0, pytest-7.4.0
collected 45 items

tests/test_rag_tool.py::TestSupabaseRAG::test_rag_instance_creation PASSED    [  2%]
tests/test_rag_tool.py::TestSupabaseRAG::test_singleton_pattern PASSED         [  4%]
tests/test_rag_tool.py::TestSupabaseRAG::test_search_theory_wollok PASSED      [  6%]
...
tests/test_llm_judge.py::TestWollokResponseQuality::test_wollok_basic_question PASSED [100%]

============================================================
PREGUNTA: ¿Qué es un objeto en Wollok?
RESPUESTA: Un objeto en Wollok es una entidad que...

EVALUACIÓN:
{
  "relevancia_paradigma": 9,
  "correccion_tecnica": 9,
  "claridad_pedagogia": 9,
  "completitud": 8,
  "uso_contexto_rag": 9,
  "score_total": 8.8,
  "pasa_calidad": true,
  "paradigma_correcto": true
}
============================================================

========================= 45 passed in 125.43s (0:02:05) =========================
```

### Interpretación de Scores

| Score | Interpretación |
|-------|---------------|
| 9-10  | Excelente ✅ |
| 7-8.9 | Bueno ✅ |
| 6-6.9 | Aceptable ⚠️ |
| <6    | Necesita mejora ❌ |

---

## 🐛 Troubleshooting

### Error: "Variables de entorno faltantes"

**Solución:** Configura las variables en `.env`:

```bash
cp .env.example .env
# Editar .env con tus credenciales
```

### Error: "Module not found"

**Solución:** Instala dependencias:

```bash
pip install -r requirements-dev.txt
```

### Tests de Supabase fallan

**Posibles causas:**
1. Credenciales incorrectas
2. Tablas vacías (sin datos)
3. Funciones RPC no creadas

**Verificar:**

```bash
# Test de conexión
pytest tests/test_integration.py::TestSupabaseConnection -v
```

### LLM Judge devuelve JSON inválido

**Solución:** El código ya maneja este caso, pero si persiste:
- Verificar que OPENROUTER_API_KEY sea válida
- El modelo GPT-4o-mini debería generar JSON consistente

---

## 📝 Escribir Nuevos Tests

### Template para Test Unitario

```python
# tests/test_nuevo_modulo.py

import pytest
from mi_modulo import mi_funcion


class TestMiModulo:
    """Tests para mi módulo."""
    
    def test_caso_basico(self):
        """Test: Caso básico de uso."""
        resultado = mi_funcion("input")
        
        assert resultado is not None
        assert isinstance(resultado, str)
```

### Template para Test con LLM Judge

```python
# tests/test_llm_judge.py

def test_nuevo_paradigma(self, llm_judge, openrouter_api_key):
    """Test: Evaluar nuevo paradigma."""
    question = "Mi pregunta..."
    agent_response = "Respuesta del agente..."
    
    evaluation = llm_judge.evaluate_response(
        question=question,
        agent_response=agent_response,
        expected_paradigm="MiParadigma"
    )
    
    assert evaluation["score_total"] >= 6.0
    assert evaluation["paradigma_correcto"] is True
```

---

## 🎯 Mejores Prácticas

### 1. Tests Independientes

✅ **Hacer:** Cada test debe poder ejecutarse solo
❌ **Evitar:** Dependencias entre tests

### 2. Usar Fixtures

✅ **Hacer:** Usar fixtures para setup/teardown
❌ **Evitar:** Código repetitivo en cada test

### 3. Tests Descriptivos

✅ **Hacer:** `test_search_theory_returns_correct_format`
❌ **Evitar:** `test1`, `test_func`

### 4. Assertions Claras

```python
# ✅ Bueno
assert len(results) == 3, f"Expected 3 results, got {len(results)}"

# ❌ Malo
assert len(results) == 3
```

### 5. Cleanup

```python
@pytest.fixture
def temp_db():
    db = create_db()
    yield db
    db.cleanup()  # ✅ Siempre cleanup
```

---

## 📊 Coverage Goal

**Objetivo:** >80% de cobertura de código

```bash
# Generar reporte
./run_tests.sh coverage

# Ver en navegador
open htmlcov/index.html  # Mac/Linux
start htmlcov/index.html # Windows
```

---

## 🔄 CI/CD Integration

### GitHub Actions (ejemplo)

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements-dev.txt
      - run: pytest tests/ -v
        env:
          OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}
          SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          SUPABASE_SERVICE_KEY: ${{ secrets.SUPABASE_SERVICE_KEY }}
```

---

## 📚 Referencias

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
- [LLM-as-a-Judge Pattern](https://arxiv.org/abs/2306.05685)

---

**Happy Testing! 🧪✨**

