# 🔧 Solución: Tests en Windows - Variables de Entorno

## 🎯 Problema Identificado

Los tests se saltan porque falta la variable `OPENROUTER_API_KEY` en tu archivo `.env`.

---

## ✅ Solución Rápida

### Paso 1: Verificar Variables

Ejecuta este comando para ver qué variables faltan:

```powershell
.\venv\Scripts\python.exe check_env.py
```

**Resultado esperado:**
```
[OK] OPENROUTER_API_KEY  ✅
[OK] SUPABASE_URL        ✅
[OK] SUPABASE_SERVICE_KEY ✅
```

### Paso 2: Configurar Variable Faltante

Abre tu archivo `.env` y agrega la línea faltante:

```env
OPENROUTER_API_KEY=sk-or-v1-tu-clave-aqui
```

**Ubicación del archivo:** `C:\Users\tomas\OneDrive\Desktop\Apertura IA\ChatPdeP_web\agents_pdep\.env`

### Paso 3: Ejecutar Tests

Una vez configurada la variable, ejecuta los tests:

**Opción 1: PowerShell (Recomendado para Windows)** ✅

```powershell
.\run_tests.ps1
```

Este script:
- ✅ Carga explícitamente el archivo .env
- ✅ Activa el entorno virtual
- ✅ Ejecuta los tests

**Opciones de ejecución:**

```powershell
.\run_tests.ps1           # Todos los tests
.\run_tests.ps1 unit      # Solo unitarios
.\run_tests.ps1 judge     # LLM-as-a-Judge
.\run_tests.ps1 quick     # Rápidos (sin LLM)
.\run_tests.ps1 coverage  # Con cobertura
```

**Opción 2: CMD tradicional**

```cmd
run_tests.bat
```

**Opción 3: pytest directo**

```powershell
# Activar venv
.\venv\Scripts\Activate.ps1

# Ejecutar pytest
pytest tests\ -v
```

---

## 🔍 Diagnóstico del Problema

### ¿Por qué no funcionaba?

En Windows con PowerShell, `load_dotenv()` puede no cargar correctamente el `.env` si:

1. ❌ Se ejecuta desde un subdirectorio diferente
2. ❌ No se especifica la ruta explícita del `.env`
3. ❌ Faltan variables en el archivo

### ¿Qué se cambió?

1. **`conftest.py`** - Ahora carga el `.env` con ruta explícita:
   ```python
   env_path = project_root / ".env"
   load_dotenv(dotenv_path=env_path, override=True)
   ```

2. **`run_tests.ps1`** - Nuevo script PowerShell que:
   - Parsea manualmente el `.env`
   - Establece cada variable en el proceso
   - Ejecuta pytest con las variables cargadas

3. **`check_env.py`** - Script de verificación para diagnosticar problemas

---

## 📝 Estado Actual de tus Variables

Según la última verificación:

| Variable | Estado |
|----------|--------|
| `OPENROUTER_API_KEY` | ❌ **FALTA CONFIGURAR** |
| `SUPABASE_URL` | ✅ Configurada |
| `SUPABASE_SERVICE_KEY` | ✅ Configurada |

---

## 🚀 Siguientes Pasos

### 1. Configurar OPENROUTER_API_KEY

Obtén tu clave en: https://openrouter.ai/keys

Agrega al `.env`:
```env
OPENROUTER_API_KEY=sk-or-v1-xxxxx
```

### 2. Verificar que funciona

```powershell
.\venv\Scripts\python.exe check_env.py
```

Deberías ver:
```
[OK] Todas las variables estan configuradas correctamente!
```

### 3. Ejecutar tests

```powershell
.\run_tests.ps1
```

---

## 🎯 Tests por Ejecutar

### Tests Básicos (sin LLM)

Estos NO requieren OPENROUTER_API_KEY:

```powershell
# Tests de configuración
pytest tests\test_agents_config.py -v

# Tests de base de datos
pytest tests\test_database.py -v
```

### Tests Completos (con LLM)

Estos SÍ requieren OPENROUTER_API_KEY:

```powershell
# Tests de RAG
pytest tests\test_rag_tool.py -v

# Tests con LLM-as-a-Judge
pytest tests\test_llm_judge.py -v

# Tests de integración
pytest tests\test_integration.py -v
```

---

## 💡 Tips para Windows

### Ejecutar siempre desde la raíz

```powershell
# Asegúrate de estar en la raíz del proyecto
cd "C:\Users\tomas\OneDrive\Desktop\Apertura IA\ChatPdeP_web\agents_pdep"

# Luego ejecuta los scripts
.\run_tests.ps1
```

### Política de ejecución de PowerShell

Si ves error de política de ejecución:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Cargar variables manualmente (alternativa)

Si nada funciona, carga manualmente:

```powershell
$env:OPENROUTER_API_KEY="sk-or-v1-tu-clave"
$env:SUPABASE_URL="https://tu-url"
$env:SUPABASE_SERVICE_KEY="tu-service-key"

pytest tests\ -v
```

---

## 📊 Resultado Esperado

Una vez configurado todo, deberías ver:

```
tests\test_rag_tool.py::TestSupabaseRAG::test_rag_instance_creation PASSED [2%]
tests\test_rag_tool.py::TestSupabaseRAG::test_singleton_pattern PASSED [4%]
tests\test_rag_tool.py::TestSupabaseRAG::test_search_theory_wollok PASSED [6%]
...
tests\test_llm_judge.py::TestWollokResponseQuality::test_wollok_basic_question PASSED [100%]

===================== 39 passed in 125.43s ======================
✅ Tests completados exitosamente
```

---

## 🆘 Troubleshooting

### Problema: "SKIPPED - Variables de entorno faltantes"

**Solución:** Ejecuta `check_env.py` para ver cuál falta

### Problema: "UnicodeEncodeError" en la consola

**Solución:** Ya está solucionado en los scripts actualizados

### Problema: "Could not find platform independent libraries"

**Solución:** Esto es un warning, puedes ignorarlo si los scripts funcionan

### Problema: PowerShell no ejecuta scripts

**Solución:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📚 Archivos Creados para Windows

- ✅ `run_tests.ps1` - Script PowerShell que carga .env correctamente
- ✅ `check_env.py` - Verificador de variables de entorno
- ✅ `conftest.py` - Actualizado con carga explícita de .env
- ✅ `SOLUCION_TESTS_WINDOWS.md` - Esta guía

---

**¡Ahora sí deberías poder ejecutar los tests sin problemas!** 🚀

