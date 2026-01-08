# 🗄️ Funciones de Supabase - Documentación Técnica

Este documento detalla las funciones RPC configuradas en Supabase para el proyecto ChatPdeP.

## 📊 Funciones Disponibles

Según la inspección del schema de Supabase, las siguientes funciones están disponibles:

| Función | Tabla | Parámetros | Retorna |
|---------|-------|------------|---------|
| `wollok_search` | wollok | query_embedding, match_count, filter | id, content, metadata, similarity |
| `haskell_search` | haskell | query_embedding, match_count, filter | id, content, metadata, similarity |
| `prolog_search` | prolog | query_embedding, match_count, filter | id, content, metadata, similarity |

## 🔧 Firma de las Funciones

### Parámetros de Entrada

```sql
CREATE OR REPLACE FUNCTION public.{table}_search(
    query_embedding vector,           -- Vector de embedding (1536 dimensiones)
    match_count integer DEFAULT NULL, -- Número de resultados (NULL = todos)
    filter jsonb DEFAULT '{}'         -- Filtro sobre metadata (opcional)
)
```

### Valores de Retorno

```sql
RETURNS TABLE(
    id uuid,                    -- ID único del documento
    content text,               -- Contenido del documento
    metadata jsonb,             -- Metadata adicional
    similarity double precision -- Score de similitud (0-1, mayor es mejor)
)
```

## 📝 Definición Completa

### wollok_search

```sql
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
LANGUAGE plpgsql
AS $function$
#variable_conflict use_column
BEGIN
    RETURN query
    SELECT
        id,
        content,
        metadata,
        1 - (wollok.embedding <=> query_embedding) AS similarity
    FROM
        public.wollok
    WHERE
        (filter = '{}' OR metadata @> filter)
    ORDER BY
        wollok.embedding <=> query_embedding
    LIMIT match_count;
END;
$function$;
```

### haskell_search

```sql
CREATE OR REPLACE FUNCTION public.haskell_search(
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
LANGUAGE plpgsql
AS $function$
#variable_conflict use_column
BEGIN
    RETURN query
    SELECT
        id,
        content,
        metadata,
        1 - (haskell.embedding <=> query_embedding) AS similarity
    FROM
        public.haskell
    WHERE
        (filter = '{}' OR metadata @> filter)
    ORDER BY
        haskell.embedding <=> query_embedding
    LIMIT match_count;
END;
$function$;
```

### prolog_search

```sql
CREATE OR REPLACE FUNCTION public.prolog_search(
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
LANGUAGE plpgsql
AS $function$
#variable_conflict use_column
BEGIN
    RETURN query
    SELECT
        id,
        content,
        metadata,
        1 - (prolog.embedding <=> query_embedding) AS similarity
    FROM
        public.prolog
    WHERE
        (filter = '{}' OR metadata @> filter)
    ORDER BY
        prolog.embedding <=> query_embedding
    LIMIT match_count;
END;
$function$;
```

## 🎯 Uso desde Python

### Ejemplo Básico

```python
from supabase import create_client
from langchain_openai import OpenAIEmbeddings

# Inicializar cliente
supabase = create_client(supabase_url, supabase_key)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Generar embedding de la query
query = "¿Qué es un objeto en Wollok?"
query_embedding = embeddings.embed_query(query)

# Llamar función RPC
response = supabase.rpc(
    "wollok_search",
    {
        "query_embedding": query_embedding,
        "match_count": 5
    }
).execute()

# Procesar resultados
for doc in response.data:
    print(f"Similitud: {doc['similarity']:.3f}")
    print(f"Contenido: {doc['content'][:100]}...")
    print(f"Metadata: {doc['metadata']}")
    print("---")
```

### Ejemplo con Filtro

```python
# Buscar solo documentos de un tipo específico
response = supabase.rpc(
    "wollok_search",
    {
        "query_embedding": query_embedding,
        "match_count": 5,
        "filter": {"type": "example"}  # Solo ejemplos
    }
).execute()
```

### Ejemplo sin Límite

```python
# Obtener todos los documentos relevantes (sin límite)
response = supabase.rpc(
    "wollok_search",
    {
        "query_embedding": query_embedding,
        "match_count": None  # Sin límite
    }
).execute()
```

## 🔍 Cómo Funciona

### 1. Similitud de Coseno

La función usa el operador `<=>` de pgvector que calcula la distancia de coseno:

```sql
1 - (embedding <=> query_embedding) AS similarity
```

- `<=>` retorna distancia (0 = idéntico, 2 = opuesto)
- `1 - distancia` convierte a similitud (1 = idéntico, -1 = opuesto)
- Valores típicos: 0.7-0.9 = muy relevante, 0.5-0.7 = relevante, <0.5 = poco relevante

### 2. Filtrado por Metadata

El operador `@>` verifica si el metadata contiene el filtro:

```sql
WHERE (filter = '{}' OR metadata @> filter)
```

Ejemplos de filtros válidos:
- `{"type": "example"}` - Solo ejemplos
- `{"difficulty": "basic"}` - Solo contenido básico
- `{"topic": "herencia", "type": "theory"}` - Teoría sobre herencia

### 3. Ordenamiento y Límite

```sql
ORDER BY embedding <=> query_embedding  -- Más similar primero
LIMIT match_count                       -- Limitar resultados
```

## 📊 Estructura de Tablas

### Schema de Tablas

```sql
CREATE TABLE wollok (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    content text NOT NULL,
    metadata jsonb DEFAULT '{}'::jsonb,
    embedding vector(1536)
);

CREATE INDEX ON wollok USING ivfflat (embedding vector_cosine_ops);
```

### Ejemplo de Metadata

```json
{
    "source": "Guía de Wollok - Capítulo 3",
    "type": "theory",
    "topic": "objetos",
    "difficulty": "intermediate",
    "language": "es",
    "created_at": "2025-01-07"
}
```

## 🚀 Optimizaciones

### Índice IVFFlat

Las tablas usan índice `ivfflat` para búsquedas rápidas:

```sql
CREATE INDEX ON wollok USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

**Ventajas:**
- Búsquedas ~10x más rápidas en tablas grandes
- Uso de memoria eficiente
- Precisión ~95% vs búsqueda exacta

**Configuración:**
- `lists`: Número de clusters (recomendado: rows/1000)
- Para 10K documentos: `lists = 100`
- Para 100K documentos: `lists = 1000`

### Caché de Queries

Para queries frecuentes, considera cachear resultados:

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_search(query: str, table: str, count: int):
    embedding = embeddings.embed_query(query)
    return supabase.rpc(f"{table}_search", {
        "query_embedding": embedding,
        "match_count": count
    }).execute()
```

## 🐛 Troubleshooting

### Error: "Could not find the function"

**Causa:** Parámetros incorrectos o en orden incorrecto.

**Solución:** Verificar que los parámetros sean:
1. `query_embedding` (vector)
2. `match_count` (integer, opcional)
3. `filter` (jsonb, opcional)

### Error: "Invalid vector dimensions"

**Causa:** El embedding tiene dimensiones incorrectas.

**Solución:** Usar `text-embedding-3-small` que genera 1536 dimensiones.

### Resultados Vacíos

**Causas posibles:**
1. Tabla vacía (sin documentos)
2. Filtro muy restrictivo
3. Query muy específica

**Solución:**
```python
# Verificar número de documentos
count = supabase.table("wollok").select("id", count="exact").execute()
print(f"Documentos en tabla: {count.count}")

# Probar sin filtro
response = supabase.rpc("wollok_search", {
    "query_embedding": embedding,
    "match_count": 10
}).execute()
```

## 📚 Referencias

- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [Supabase Vector Guide](https://supabase.com/docs/guides/ai/vector-columns)
- [PostgreSQL JSONB Operators](https://www.postgresql.org/docs/current/functions-json.html)

---

**Última actualización:** 2025-01-07  
**Proyecto:** ChatPdeP v2.0.0

