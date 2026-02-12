# 🚀 Cómo Ejecutar Tests en Windows

## ⚠️ Comandos Correctos para PowerShell

En PowerShell, debes usar `.\` antes del nombre del script:

### ✅ CORRECTO

```powershell
.\run_tests.ps1           # Ejecutar script PowerShell
.\run_tests.bat           # Ejecutar script batch
```

### ❌ INCORRECTO

```powershell
run_tests.ps1             # ❌ No funciona
run_tests.bat             # ❌ No funciona
run_tests.sh              # ❌ Script de Linux/Mac
```

---

## 🎯 Comandos Principales

### 1. Verificar Variables de Entorno

```powershell
.\venv\Scripts\python.exe check_env.py
```

**O si ya tienes el venv activado:**

```powershell
python check_env.py
```

### 2. Ejecutar Todos los Tests

**Opción A: Script PowerShell (Recomendado)**

```powershell
.\run_tests.ps1
```

**Opción B: Script Batch**

```powershell
.\run_tests.bat
```

**Opción C: pytest directo**

```powershell
pytest tests\ -v
```

### 3. Ejecutar Tests Específicos

```powershell
# Tests unitarios
.\run_tests.ps1 unit

# Tests de integración
.\run_tests.ps1 integration

# Tests con LLM-as-a-Judge
.\run_tests.ps1 judge

# Tests rápidos (sin LLM)
.\run_tests.ps1 quick

# Tests con cobertura
.\run_tests.ps1 coverage
```

---

## 🔧 Si PowerShell No Permite Ejecutar Scripts

### Error: "No se puede cargar porque la ejecución de scripts está deshabilitada"

**Solución:**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Luego intenta de nuevo:

```powershell
.\run_tests.ps1
```

---

## 📊 Tests por Archivo

### Ejecutar tests de un archivo específico

```powershell
# Tests de RAG
pytest tests\test_rag_tool.py -v

# Tests de base de datos
pytest tests\test_database.py -v

# Tests de configuración
pytest tests\test_agents_config.py -v

# Tests con LLM Judge
pytest tests\test_llm_judge.py -v
```

### Ejecutar un test específico

```powershell
pytest tests\test_rag_tool.py::TestSupabaseRAG::test_search_theory_wollok -v
```

---

## 🎭 Resultado Esperado

Al ejecutar `.\run_tests.ps1`, deberías ver:

```
🧪 ChatPdeP - Suite de Tests (PowerShell)
==========================================

📥 Cargando variables de entorno desde .env...
   ✅ OPENROUTER_API_KEY cargada
   ✅ SUPABASE_URL cargada
   ✅ SUPABASE_SERVICE_KEY cargada

📦 Activando entorno virtual...
📥 Verificando dependencias de testing...

==========================================

🚀 Ejecutando TODOS los tests...

tests\test_rag_tool.py::TestSupabaseRAG::test_rag_instance_creation PASSED [2%]
tests\test_rag_tool.py::TestSupabaseRAG::test_singleton_pattern PASSED [4%]
...
tests\test_llm_judge.py::TestWollokResponseQuality::test_wollok_basic_question PASSED [100%]

==========================================
✅ Tests completados exitosamente
==========================================
```

---

## 🐛 Troubleshooting

### Error: "Could not find platform independent libraries"

**Solución:** Este es solo un warning, puedes ignorarlo. Los tests funcionarán correctamente.

### Error: "Variables de entorno faltantes"

**Solución:**

```powershell
# 1. Verificar qué falta
.\venv\Scripts\python.exe check_env.py

# 2. Editar .env y agregar la variable faltante
# 3. Intentar de nuevo
.\run_tests.ps1
```

### Tests se saltan (SKIPPED)

**Causa:** Falta una variable de entorno requerida.

**Solución:** Configurar todas las variables en `.env`:

```env
OPENROUTER_API_KEY=sk-or-v1-...
SUPABASE_URL=https://...
SUPABASE_SERVICE_KEY=eyJ...
```

### Script no se encuentra

**Error:**
```
El término 'run_tests.ps1' no se reconoce como nombre de un cmdlet...
```

**Solución:** Usar `.\` al inicio:

```powershell
.\run_tests.ps1    # ✅ Correcto
```

---

## 📝 Resumen de Comandos

```powershell
# Verificar configuración
.\venv\Scripts\python.exe check_env.py

# Ejecutar tests
.\run_tests.ps1                # Todos los tests
.\run_tests.ps1 judge          # LLM-as-a-Judge
.\run_tests.ps1 quick          # Rápidos
pytest tests\ -v               # pytest directo

# Tests específicos
pytest tests\test_rag_tool.py -v
pytest tests\test_llm_judge.py -v
```

---

## ✨ Tips

1. **Siempre usa `.\` para scripts**: `.\run_tests.ps1`, no `run_tests.ps1`
2. **Usa barras invertidas en Windows**: `tests\` no `tests/`
3. **Activa el venv primero** (opcional):
   ```powershell
   .\venv\Scripts\Activate.ps1
   pytest tests\ -v
   ```

---

**¡Listo para ejecutar tests!** 🎉

