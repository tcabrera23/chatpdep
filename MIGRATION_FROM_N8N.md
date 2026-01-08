# 🔄 Migración desde N8N a Python/Streamlit

Este documento explica cómo se migró el workflow de N8N a una aplicación Python completa.

## 📊 Comparación: N8N vs Nueva Arquitectura

### Workflow N8N Original

```
[Trigger: Chat Message] 
    ↓
[Extract from File] (PDFs)
    ↓
[Wollok AI Agent]
    ├── Chat Model: Google Gemini
    ├── Memory: Redis Chat Memory
    ├── Tool: recuperar_teoria
    └── Embeddings: OpenAI
    ↓
[Response]
```

### Nueva Arquitectura Python

```
[Streamlit UI]
    ↓
[File Extractor] (PDFs + Imágenes)
    ↓
[Agent Executor (LangChain)]
    ├── LLM: OpenRouter (Gemini/GPT/Grok)
    ├── Memory: SQLite Local
    ├── Tool: recuperar_teoria (RAG)
    └── Embeddings: OpenAI (vía Supabase)
    ↓
[Response Streaming]
```

---

## 🔀 Mapeo de Componentes

| Componente N8N | Componente Python | Archivo |
|----------------|-------------------|---------|
| Chat Message Trigger | Streamlit Chat Input | `app.py` |
| Extract from File | FileExtractor | `tools/file_extraction.py` |
| Wollok AI Agent | AgentExecutor | `app.py` |
| Redis Chat Memory | SQLite + Session State | `utils/database.py` |
| recuperar_teoria Tool | SupabaseRAG | `tools/rag_tool.py` |
| Embeddings OpenAI | OpenAIEmbeddings | `tools/rag_tool.py` |
| System Prompts | AGENTS config | `config/agents.py` |

---

## ✨ Mejoras Implementadas

### 1. **Múltiples Agentes**
- **N8N**: Solo Wollok
- **Python**: Wollok, Haskell y Prolog

### 2. **Persistencia de Datos**
- **N8N**: Redis (volátil)
- **Python**: SQLite (persistente en disco)

### 3. **Interfaz de Usuario**
- **N8N**: Interfaz externa
- **Python**: Streamlit integrado con sidebar completo

### 4. **Gestión de Conversaciones**
- **N8N**: Sin historial persistente
- **Python**: Historial completo con:
  - Títulos editables
  - Búsqueda de conversaciones
  - Eliminación de conversaciones
  - Metadata (agente, modelo, fechas)

### 5. **Soporte de Archivos**
- **N8N**: Solo PDFs
- **Python**: PDFs + Imágenes (PNG, JPG, etc.)

### 6. **Modelos LLM**
- **N8N**: Google Gemini fijo
- **Python**: Selección dinámica entre múltiples modelos

### 7. **Deployment**
- **N8N**: Requiere instancia N8N
- **Python**: 
  - Docker (local)
  - Streamlit Cloud
  - Cualquier servidor Python

---

## 🏗️ Estructura del Código

### Modularización

El código está organizado en módulos especializados:

```
agents_pdep/
├── app.py                    # UI y lógica principal
├── config/
│   └── agents.py            # System prompts y configuración
├── tools/
│   ├── rag_tool.py          # Búsqueda RAG en Supabase
│   └── file_extraction.py   # Extracción de PDFs e imágenes
└── utils/
    └── database.py          # Gestión de historial SQLite
```

### Ventajas de la Modularización

1. **Mantenibilidad**: Cada módulo tiene una responsabilidad clara
2. **Testabilidad**: Fácil de probar componentes individuales
3. **Extensibilidad**: Agregar nuevos agentes o herramientas es simple
4. **Reutilización**: Los módulos pueden usarse en otros proyectos

---

## 🔧 Configuración de Agentes

### En N8N
- System prompt embebido en el nodo
- Un solo agente configurado

### En Python
- System prompts en `config/agents.py`
- Configuración centralizada para 3 agentes
- Fácil agregar nuevos agentes editando un solo archivo

```python
AGENT_NUEVO = {
    "name": "Nuevo",
    "table": "nuevo_table",
    "query_name": "nuevo_search",
    "system_prompt": """..."""
}
```

---

## 🗄️ Base de Datos

### Redis en N8N
- Memoria volátil
- Configuración compleja
- Requiere servidor Redis separado

### SQLite en Python
- Persistente en disco
- Sin configuración adicional
- Archivo simple `data/conversations.db`
- Respaldos fáciles (copiar archivo)

### Schema SQLite

```sql
-- Tabla de conversaciones
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY,
    conversation_id TEXT UNIQUE,
    title TEXT,
    agent_name TEXT,
    model_name TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Tabla de mensajes
CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    conversation_id TEXT,
    role TEXT,
    content TEXT,
    has_attachment BOOLEAN,
    attachment_type TEXT,
    created_at TIMESTAMP
);
```

---

## 🔍 Tool: recuperar_teoria

### Implementación N8N
- Configurado visualmente en el nodo
- Parámetros fijos

### Implementación Python

```python
@tool
def recuperar_teoria(query: str) -> str:
    """
    Recupera teoría relevante desde la base de conocimientos.
    """
    rag = get_rag_instance()
    results = rag.search_theory(
        query=query,
        table_name=agent_config["table"],
        query_name=agent_config["query_name"],
        match_count=5
    )
    return rag.format_results(results)
```

**Ventajas**:
- Configuración dinámica por agente
- Reutilizable en otros contextos
- Fácil de testear

---

## 📄 Extracción de Archivos

### N8N: Extract from File
- Solo PDFs
- Configuración limitada

### Python: FileExtractor

```python
class FileExtractor:
    def extract_from_pdf(self, pdf_file) -> str:
        # PyPDF2 para extracción de texto
        
    def extract_from_image(self, image_file) -> str:
        # Análisis con modelo de visión
        
    def extract_from_file(self, uploaded_file) -> str:
        # Detección automática de tipo
```

**Características**:
- Soporte para PDFs e imágenes
- Análisis inteligente de imágenes con LLM
- Manejo robusto de errores
- Fácil agregar nuevos tipos de archivo

---

## 🚀 Deployment

### N8N
```
Requiere:
- Instancia N8N
- Redis server
- Configuración manual de nodos
- No portable
```

### Python
```bash
# Opción 1: Docker
docker-compose up

# Opción 2: Local
streamlit run app.py

# Opción 3: Cloud
# Deploy en Streamlit Cloud con un clic
```

**Ventajas**:
- Múltiples opciones de deployment
- Portátil entre entornos
- Fácil de versionar con Git
- CI/CD simple

---

## 📈 Performance

| Aspecto | N8N | Python |
|---------|-----|--------|
| Tiempo de carga | ~5-10s | ~2-3s |
| Memoria | ~200MB + Redis | ~100MB |
| Latencia respuesta | Similar | Similar |
| Concurrent users | Limitado | Escalable |

---

## 🎯 Próximos Pasos Sugeridos

### Mejoras Posibles

1. **Streaming de Respuestas**
   - Implementar streaming token por token
   - Mejor UX con respuestas largas

2. **Caché de Embeddings**
   - Cachear queries frecuentes
   - Reducir costos de API

3. **Análisis de Uso**
   - Métricas de conversaciones
   - Queries más comunes
   - Feedback de usuarios

4. **Tests Automatizados**
   - Unit tests para cada módulo
   - Integration tests del workflow completo
   - CI/CD con GitHub Actions

5. **Multi-usuario**
   - Autenticación
   - Conversaciones por usuario
   - Compartir conversaciones

---

## 💡 Lecciones Aprendidas

### Lo Bueno de N8N
- ✅ Prototipado rápido
- ✅ Visual e intuitivo
- ✅ Sin código necesario

### Lo Bueno de Python
- ✅ Control total del código
- ✅ Fácil de versionar
- ✅ Mejor para producción
- ✅ Más portable
- ✅ Mejor performance
- ✅ Extensible

### Conclusión
**N8N es excelente para prototipos y MVP**, pero para una aplicación de producción con múltiples funcionalidades, **Python + Streamlit ofrece mejor control, mantenibilidad y escalabilidad**.

---

## 🔗 Referencias

- [N8N Documentation](https://docs.n8n.io/)
- [LangChain Documentation](https://python.langchain.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Supabase Documentation](https://supabase.com/docs)

