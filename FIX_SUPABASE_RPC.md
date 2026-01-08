# 🔧 Fix: Corrección de Funciones RPC de Supabase

## 🐛 Problema Identificado

**Error original:**
```
Error en búsqueda RAG: {'message': 'Could not find the function public.wollok_search(match_count, match_threshold, query_embedding) in the schema cache', 'code': 'PGRST202'}
```

## 🔍 Diagnóstico

Usando el MCP de Supabase, se identificó que:

1. **Parámetros incorrectos**: El código intentaba usar `match_threshold` que no existe
2. **Orden incorrecto**: Los parámetros estaban en orden diferente
3. **Firma real de las funciones**:
   ```sql
   wollok_search(query_embedding vector, match_count integer, filter jsonb)
   ```

## ✅ Solución Implementada

### 1. Actualizado `tools/rag_tool.py`

#### Cambios en `search_theory()`

**Antes:**
```python
def search_theory(
    self,
    query: str,
    table_name: str,
    query_name: str,
    match_count: int = 5,
    match_threshold: float = 0.5  # ❌ No existe
) -> List[Dict[str, Any]]:
    # ...
    response = self.supabase.rpc(
        query_name,
        {
            "query_embedding": query_embedding,
            "match_count": match_count,
            "match_threshold": match_threshold  # ❌ Parámetro inválido
        }
    ).execute()
```

**Después:**
```python
def search_theory(
    self,
    query: str,
    table_name: str,
    query_name: str,
    match_count: int = 5,
    filter_metadata: dict = None  # ✅ Parámetro correcto
) -> List[Dict[str, Any]]:
    # ...
    rpc_params = {
        "query_embedding": query_embedding,
        "match_count": match_count
    }
    
    if filter_metadata:
        rpc_params["filter"] = filter_metadata
    
    response = self.supabase.rpc(query_name, rpc_params).execute()
```

#### Cambios en `format_results()`

**Mejoras:**
- Ahora incluye metadata en el formato
- Muestra fuente si está disponible
- Formato de similitud mejorado (3 decimales)

```python
def format_results(self, results: List[Dict[str, Any]]) -> str:
    # ...
    for i, doc in enumerate(results, 1):
        content = doc.get("content", "")
        similarity = doc.get("similarity", 0)
        metadata = doc.get("metadata", {})
        
        formatted += f"## Fragmento {i} (Similitud: {similarity:.3f})\n"
        
        if metadata:
            source = metadata.get("source", "")
            if source:
                formatted += f"**Fuente:** {source}\n\n"
        
        formatted += f"{content}\n\n"
```

### 2. Actualizado `README.md`

**Cambios:**
- Firma correcta de funciones RPC
- Parámetros actualizados
- Documentación de `filter` en lugar de `match_threshold`
- Agregado modelo de embedding: `text-embedding-3-small`

### 3. Actualizado `SETUP.md`

**Cambios:**
- Funciones SQL actualizadas con firma correcta
- Uso de `uuid` en lugar de `bigserial`
- Índices IVFFlat correctos
- Ejemplos actualizados

### 4. Creado `SUPABASE_FUNCTIONS.md`

**Nuevo archivo con:**
- Documentación completa de funciones RPC
- Ejemplos de uso desde Python
- Explicación de similitud de coseno
- Troubleshooting
- Optimizaciones

## 📊 Comparación: Antes vs Después

| Aspecto | Antes ❌ | Después ✅ |
|---------|---------|-----------|
| **Parámetros** | query_embedding, match_count, match_threshold | query_embedding, match_count, filter |
| **Retorno** | id, content, similarity | id, content, metadata, similarity |
| **Tipo ID** | bigint | uuid |
| **Filtrado** | Por threshold | Por metadata (JSONB) |
| **Modelo Embedding** | text-embedding-ada-002 | text-embedding-3-small |

## 🎯 Funciones Reales en Supabase

Según inspección con MCP de Supabase:

```sql
-- wollok_search
CREATE OR REPLACE FUNCTION public.wollok_search(
    query_embedding vector,
    match_count integer DEFAULT NULL::integer,
    filter jsonb DEFAULT '{}'::jsonb
)
RETURNS TABLE(
    id uuid,
    content text,
    metadata jsonb,
    similarity double precision
)
```

**Misma firma para:**
- `haskell_search`
- `prolog_search`

## 🚀 Testing

Para verificar que funciona:

```python
from tools.rag_tool import get_rag_instance

# Inicializar RAG
rag = get_rag_instance()

# Probar búsqueda
results = rag.search_theory(
    query="¿Qué es un objeto en Wollok?",
    table_name="wollok",
    query_name="wollok_search",
    match_count=5
)

# Ver resultados
print(rag.format_results(results))
```

**Resultado esperado:**
```
# Teoría Recuperada

## Fragmento 1 (Similitud: 0.876)
**Fuente:** Guía de Wollok - Capítulo 2

Un objeto en Wollok es una entidad que encapsula estado y comportamiento...

---

## Fragmento 2 (Similitud: 0.843)
...
```

## 📝 Archivos Modificados

1. ✅ `tools/rag_tool.py` - Lógica de búsqueda corregida
2. ✅ `README.md` - Documentación actualizada
3. ✅ `SETUP.md` - Guía de setup actualizada
4. ✅ `SUPABASE_FUNCTIONS.md` - Nueva documentación técnica
5. ✅ `FIX_SUPABASE_RPC.md` - Este documento

## 🎓 Lecciones Aprendidas

1. **Siempre verificar el schema real**: No asumir la firma de funciones
2. **Usar MCP de Supabase**: Herramienta invaluable para debugging
3. **Documentar bien**: Evita estos problemas en el futuro
4. **Metadata > Threshold**: Filtrado por metadata es más flexible

## 🔗 Referencias

- Ver `SUPABASE_FUNCTIONS.md` para documentación completa
- Ver `tools/rag_tool.py` para implementación
- Ver `README.md` para guía de uso

---

**Fix aplicado:** 2025-01-07  
**Status:** ✅ Resuelto  
**Impacto:** Crítico (bloqueaba funcionalidad RAG)

