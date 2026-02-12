# 🔒 Configuración de Seguridad con RLS (Row Level Security)

## 📋 Resumen

Este proyecto ahora utiliza **Supabase ANON KEY** en lugar de SERVICE KEY para mayor seguridad. Esto es posible gracias a las políticas de Row Level Security (RLS) configuradas en las tablas.

---

## 🎯 ¿Por qué este cambio?

### Antes (❌ Menos seguro)

```env
SUPABASE_SERVICE_KEY=eyJ...  # Acceso total a la base de datos
```

**Problemas:**
- Service key tiene acceso completo a todas las tablas
- Si se expone, compromete toda la base de datos
- No se puede compartir públicamente

### Ahora (✅ Más seguro)

```env
SUPABASE_ANON_KEY=eyJ...  # Solo permisos definidos por RLS
```

**Ventajas:**
- Acceso limitado por políticas RLS
- Seguro para uso en cliente/frontend
- Puede compartirse en repositorios públicos
- Solo permite operaciones específicas

---

## 🛡️ Políticas RLS Configuradas

### 1. Tablas de Teoría (Lectura Pública)

Las tablas `wollok`, `haskell` y `prolog` tienen **lectura pública**:

```sql
-- Cualquiera puede leer (para búsquedas RAG)
CREATE POLICY "Permitir lectura pública en wollok"
ON wollok FOR SELECT
USING (true);
```

**Uso:** Búsquedas semánticas desde la app

### 2. Tabla de Métricas (Inserción Pública, Lectura Restringida)

La tabla `chatpdep_tokens` permite:
- ✅ **Inserción pública:** Registrar métricas de uso
- ❌ **Lectura solo autenticada:** Ver métricas requiere autenticación

```sql
-- Cualquiera puede insertar métricas
CREATE POLICY "Permitir inserción pública en chatpdep_tokens"
ON chatpdep_tokens FOR INSERT
WITH CHECK (true);

-- Solo usuarios autenticados pueden leer
CREATE POLICY "Permitir lectura autenticada en chatpdep_tokens"
ON chatpdep_tokens FOR SELECT
USING (auth.role() = 'authenticated' OR auth.role() = 'service_role');
```

---

## 📝 Configuración Requerida

### Variables de Entorno

```env
# URL de tu proyecto Supabase
SUPABASE_URL=https://tu-proyecto.supabase.co

# ANON KEY (recomendado) - Usar esta
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# SERVICE KEY (opcional, solo para retrocompatibilidad)
# SUPABASE_SERVICE_KEY=eyJ...
```

### Obtener tu ANON KEY

1. Ve a tu proyecto en [Supabase Dashboard](https://app.supabase.com)
2. Settings → API
3. Copia el **anon/public** key
4. Agrégalo a tu `.env` como `SUPABASE_ANON_KEY`

---

## 🔧 Cómo Funciona en el Código

### RAG Tool

```python
# tools/rag_tool.py
self.supabase_key = os.environ.get("SUPABASE_ANON_KEY") or os.environ.get("SUPABASE_SERVICE_KEY")
```

**Prioridad:**
1. Intenta usar `SUPABASE_ANON_KEY` (más seguro)
2. Si no existe, usa `SUPABASE_SERVICE_KEY` (retrocompatibilidad)

### Tracking de Métricas

```python
# utils/tracking.py
from utils.tracking import log_interaction

log_interaction(
    conversation_id="abc-123",
    user_input="¿Qué es un objeto?",
    agent_response="Un objeto...",
    tokens_in=50,
    tokens_out=200
)
```

**Usa ANON_KEY** para insertar en `chatpdep_tokens`

---

## 🧪 Tests

Los tests también usan ANON_KEY:

```python
# tests/conftest.py
required_vars = [
    "OPENROUTER_API_KEY",
    "SUPABASE_URL",
    "SUPABASE_ANON_KEY"  # Ahora usa ANON_KEY
]
```

---

## 📊 Permisos por Operación

| Tabla | Operación | ANON_KEY | SERVICE_KEY |
|-------|-----------|----------|-------------|
| `wollok` | SELECT | ✅ Sí | ✅ Sí |
| `wollok` | INSERT | ❌ No | ✅ Sí |
| `haskell` | SELECT | ✅ Sí | ✅ Sí |
| `prolog` | SELECT | ✅ Sí | ✅ Sí |
| `chatpdep_tokens` | INSERT | ✅ Sí | ✅ Sí |
| `chatpdep_tokens` | SELECT | ❌ No* | ✅ Sí |

\* Lectura solo para usuarios autenticados

---

## 🚀 Migración desde SERVICE_KEY

Si ya tienes el proyecto funcionando con `SUPABASE_SERVICE_KEY`:

### Paso 1: Agregar ANON_KEY

```bash
# Edita tu .env
nano .env
```

```env
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Paso 2: Verificar RLS

Las políticas RLS ya están aplicadas. Puedes verificar en:
- Supabase Dashboard → Table Editor → (tabla) → Policies

### Paso 3: Probar

```bash
# Ejecutar la app
streamlit run app.py
```

La app ahora usará `SUPABASE_ANON_KEY` automáticamente.

### Paso 4: (Opcional) Remover SERVICE_KEY

Una vez que todo funcione, puedes remover `SUPABASE_SERVICE_KEY` de tu `.env`:

```env
# Ya no es necesaria
# SUPABASE_SERVICE_KEY=eyJ...
```

---

## 🔍 Verificación de Seguridad

### Test 1: Verificar que RAG funciona con ANON_KEY

```bash
pytest tests/test_rag_tool.py -v
```

**Resultado esperado:** ✅ Todos los tests pasan

### Test 2: Verificar que tracking funciona

```bash
pytest tests/test_integration.py -v
```

**Resultado esperado:** ✅ Puede insertar métricas

### Test 3: Verificar permisos limitados

Intenta hacer algo que NO debería funcionar con ANON_KEY:

```python
from supabase import create_client
import os

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_ANON_KEY")
)

# Esto DEBE FALLAR (no tienes permisos de eliminación)
result = supabase.table("wollok").delete().eq("id", "some-id").execute()
```

**Resultado esperado:** ❌ Error de permisos (esto es bueno!)

---

## 📚 Más Información

- [Supabase RLS Documentation](https://supabase.com/docs/guides/auth/row-level-security)
- [Database Policies](https://supabase.com/docs/guides/database/postgres/row-level-security)
- [API Keys](https://supabase.com/docs/guides/api/api-keys)

---

## 🆘 Troubleshooting

### Error: "new row violates row-level security policy"

**Causa:** Intentas hacer una operación no permitida

**Solución:** Verifica que la política RLS permita esa operación

### Error: "SUPABASE_ANON_KEY debe estar configurado"

**Causa:** Falta la variable de entorno

**Solución:**
```bash
# Agregar a .env
SUPABASE_ANON_KEY=tu-anon-key-aquí
```

### Tests fallan con "permission denied"

**Causa:** Las políticas RLS no están aplicadas correctamente

**Solución:** Re-ejecutar la migración:
```sql
-- Ver SEGURIDAD_RLS.md sección "Políticas RLS"
```

---

**Cambio implementado:** 2025-01-08  
**Estado:** ✅ Activo  
**Seguridad:** 🛡️ Mejorada

