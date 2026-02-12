# 🔒 Cambios de Seguridad y Mejoras - 08/01/2025

## ✅ Resumen Ejecutivo

Se implementó un sistema de seguridad mejorado usando **Row Level Security (RLS)** en Supabase, migrando de `SUPABASE_SERVICE_KEY` a `SUPABASE_ANON_KEY`. Esto hace que la aplicación sea más segura y permite compartir la configuración públicamente sin riesgos.

---

## 🎯 Cambios Principales

### 1. ✅ Configuración de RLS en Supabase

**Tablas actualizadas:**
- `wollok` - RLS habilitado con lectura pública
- `haskell` - RLS habilitado con lectura pública
- `prolog` - RLS habilitado con lectura pública
- `chatpdep_tokens` - RLS con inserción pública, lectura autenticada

**Políticas creadas:**

```sql
-- Lectura pública para búsquedas RAG
CREATE POLICY "Permitir lectura pública en wollok" ON wollok FOR SELECT USING (true);
CREATE POLICY "Permitir lectura pública en haskell" ON haskell FOR SELECT USING (true);
CREATE POLICY "Permitir lectura pública en prolog" ON prolog FOR SELECT USING (true);

-- Métricas: inserción pública, lectura restringida
CREATE POLICY "Permitir inserción pública en chatpdep_tokens" ON chatpdep_tokens FOR INSERT WITH CHECK (true);
CREATE POLICY "Permitir lectura autenticada en chatpdep_tokens" ON chatpdep_tokens FOR SELECT 
USING (auth.role() = 'authenticated' OR auth.role() = 'service_role');
```

### 2. ✅ Migración del Código

**Archivos modificados:**

#### `tools/rag_tool.py`
```python
# Antes
self.supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")

# Ahora
self.supabase_key = os.environ.get("SUPABASE_ANON_KEY") or os.environ.get("SUPABASE_SERVICE_KEY")
```

#### `utils/tracking.py` (NUEVO)
Sistema de tracking de métricas que usa ANON_KEY para insertar registros de uso.

#### `tests/conftest.py`
```python
# Ahora verifica SUPABASE_ANON_KEY en lugar de SERVICE_KEY
required_vars = [
    "OPENROUTER_API_KEY",
    "SUPABASE_URL",
    "SUPABASE_ANON_KEY"
]
```

### 3. ✅ Actualización de Documentación

**Archivos creados:**
- ✅ `SEGURIDAD_RLS.md` - Guía completa de seguridad RLS
- ✅ `utils/tracking.py` - Sistema de métricas
- ✅ `CAMBIOS_SEGURIDAD_2025-01-08.md` - Este archivo

**Archivos actualizados:**
- ✅ `README.md` - Menciona ANON_KEY y enlaza a documentación
- ✅ `check_env.py` - Verifica ANON_KEY en lugar de SERVICE_KEY
- ✅ `tests/conftest.py` - Usa ANON_KEY para tests

### 4. ✅ Posts de LinkedIn

**Archivo creado:**
- ✅ `linkedin_posts.md` - 6 posts para promoción del proyecto

**Contenido:**
- Post 1: Visión general y migración de N8N a Python
- Post 2: Explicación de RAG
- Post 3: Optimización de contexto y costos
- Post 4: Simplificación de despliegue
- Post 5: Llamado a UTN y replicación
- Post 6: Diferencias RAG vs cargar docs en otra IA

---

## 📊 Comparativa: Antes vs Ahora

| Aspecto | Antes (SERVICE_KEY) | Ahora (ANON_KEY) |
|---------|---------------------|------------------|
| **Seguridad** | ❌ Acceso total a DB | ✅ Acceso limitado por RLS |
| **Exposición** | ❌ No se puede compartir | ✅ Seguro para compartir |
| **Permisos** | ❌ Sin restricciones | ✅ Solo operaciones permitidas |
| **Auditoría** | ❌ Difícil de rastrear | ✅ Políticas claras |
| **Costo** | ✅ Ninguno | ✅ Ninguno |
| **Complejidad** | ✅ Simple | ✅ Simple |

---

## 🔑 Configuración Actualizada

### Variables de Entorno

```env
# REQUERIDAS
OPENROUTER_API_KEY=sk-or-v1-xxxxx
SUPABASE_URL=https://hpirunrgwsdzndmhtzgz.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# OPCIONAL (solo para retrocompatibilidad)
# SUPABASE_SERVICE_KEY=eyJ...
```

### Tu Configuración Actual

```env
SUPABASE_URL=https://hpirunrgwsdzndmhtzgz.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhwaXJ1bnJnd3Nkem5kbWh0emd6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDk1OTQzNTIsImV4cCI6MjA2NTE3MDM1Mn0.pGKPBpUb5BUseha_QvU9rfhItJc2akyObZTE0iuL9w8
```

---

## 🧪 Verificación

### Tests Actualizados

```bash
# Ejecutar tests con nueva configuración
.\venv\Scripts\pytest.exe tests\ -v
```

**Resultado esperado:** ✅ 42 tests PASSED

### Verificar Conexión

```bash
# Verificar variables
python check_env.py
```

**Resultado esperado:**
```
[OK] OPENROUTER_API_KEY
[OK] SUPABASE_URL
[OK] SUPABASE_ANON_KEY

[OK] Todas las variables estan configuradas correctamente!
```

---

## 📝 Pasos de Migración para Usuarios

Si alguien clona el repo, estos son los pasos:

### 1. Configurar Variables

```bash
cp .env.example .env
nano .env
```

### 2. Agregar Credenciales

```env
OPENROUTER_API_KEY=tu-clave-aqui
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_ANON_KEY=tu-anon-key-aqui
```

### 3. Verificar

```bash
python check_env.py
```

### 4. Ejecutar

```bash
streamlit run app.py
```

---

## 🛡️ Beneficios de Seguridad

### 1. Exposición Limitada

Con `ANON_KEY`:
- ✅ No da acceso total a la base de datos
- ✅ Solo permite operaciones definidas por RLS
- ✅ Se puede compartir públicamente en el repo

### 2. Control Granular

Con RLS puedes:
- ✅ Definir quién puede leer qué tablas
- ✅ Restringir operaciones de escritura
- ✅ Auditar accesos

### 3. Escalabilidad

Cuando agregues usuarios:
- ✅ Ya tienes RLS configurado
- ✅ Fácil agregar políticas por usuario
- ✅ No necesitas cambiar el código

---

## 🔄 Retrocompatibilidad

El código sigue funcionando con `SERVICE_KEY` para retrocompatibilidad:

```python
# Prioridad:
# 1. SUPABASE_ANON_KEY (recomendado)
# 2. SUPABASE_SERVICE_KEY (fallback)

self.supabase_key = os.environ.get("SUPABASE_ANON_KEY") or os.environ.get("SUPABASE_SERVICE_KEY")
```

**Recomendación:** Migrar a `ANON_KEY` en cuanto sea posible.

---

## 📚 Documentación Adicional

- [SEGURIDAD_RLS.md](SEGURIDAD_RLS.md) - Guía completa de RLS
- [README.md](README.md) - Instrucciones actualizadas
- [TESTING.md](TESTING.md) - Tests con ANON_KEY

---

## 🎉 Resultado Final

### Antes
```
❌ Usar SERVICE_KEY (riesgoso)
❌ No se puede compartir públicamente
❌ Acceso sin restricciones
```

### Ahora
```
✅ Usar ANON_KEY (seguro)
✅ Compartible públicamente
✅ Acceso controlado por RLS
✅ Sistema de tracking de métricas
✅ Posts de LinkedIn listos
✅ Documentación completa
```

---

**Fecha de implementación:** 08/01/2025  
**Proyecto:** hpirunrgwsdzndmhtzgz (Demos Apertura)  
**Estado:** ✅ Completado y Documentado  
**Próximos pasos:** Probar en producción y promocionar en LinkedIn

