# 🎓 ChatPdeP - Tutor de Paradigmas de Programación

Aplicación web interactiva que proporciona tutorías personalizadas para la materia "Paradigmas de Programación" de la UTN FRBA. Utiliza inteligencia artificial y RAG (Retrieval Augmented Generation) para asistir a estudiantes con tres paradigmas principales: **Wollok (OOP)**, **Haskell (Funcional)** y **Prolog (Lógico)**.

## 🌟 Características

### 🤖 Tres Agentes Especializados
- **Wollok**: Tutor de Programación Orientada a Objetos
- **Haskell**: Tutor de Programación Funcional
- **Prolog**: Tutor de Programación Lógica

Cada agente utiliza RAG para recuperar información específica de su base de conocimientos en Supabase.

### 💡 Funcionalidades Principales

- **Chat Interactivo**: Interfaz similar a ChatGPT
- **Archivos Adjuntos**: Soporte para PDFs e imágenes
  - Extracción automática de texto de PDFs
  - Análisis de imágenes con modelos de visión
- **Historial Persistente**: Base de datos SQLite local para guardar conversaciones
- **Ventana de Contexto Configurable**: Ajusta cuántos mensajes mantener en memoria (4-20 mensajes)
- **Gestión de Conversaciones**: Crea, carga y elimina conversaciones anteriores

### 🎨 Interfaz de Usuario

**Sidebar:**
- Configuración de API Key de OpenRouter
- Selector de Tutor (Wollok/Haskell/Prolog)
- Selector de Modelo LLM
- Control de ventana de contexto
- Historial de conversaciones con títulos editables
- Botón para nueva conversación

**Área Principal:**
- Chat interactivo con formato limpio
- Indicadores de configuración actual
- Soporte para archivos adjuntos
- Respuestas con streaming

## 🏗️ Arquitectura del Proyecto

```
agents_pdep/
├── app.py                      # Aplicación principal Streamlit
├── config/
│   ├── __init__.py
│   └── agents.py              # Configuración de los 3 agentes y system prompts
├── tools/
│   ├── __init__.py
│   ├── rag_tool.py            # Herramienta RAG para Supabase
│   └── file_extraction.py     # Extracción de PDFs e imágenes
├── utils/
│   ├── __init__.py
│   └── database.py            # Gestión de SQLite para historial
├── data/
│   └── conversations.db       # Base de datos SQLite (generada)
├── requirements.txt           # Dependencias Python
├── Dockerfile                 # Configuración Docker
├── docker-compose.yml         # Orquestación Docker
├── .env.example              # Plantilla de variables de entorno
└── README.md                 # Este archivo
```

## 🚀 Instalación y Ejecución

### Opción 1: Ejecución Local con Docker (Recomendado)

1. **Clonar el repositorio**
```bash
git clone <tu-repositorio>
cd agents_pdep
```

2. **Configurar variables de entorno**
```bash
cp .env.example .env
```

Edita el archivo `.env` con tus credenciales:
- `OPENROUTER_API_KEY`: Tu API key de [OpenRouter](https://openrouter.ai/keys)
- `SUPABASE_URL`: URL de tu proyecto Supabase
- `SUPABASE_ANON_KEY`: Anon/public key de Supabase (Settings → API)

> 🔒 **Seguridad:** Usamos `ANON_KEY` con Row Level Security (RLS) en lugar de `SERVICE_KEY`. Ver [SEGURIDAD_RLS.md](SEGURIDAD_RLS.md)

3. **Levantar con Docker**
```bash
docker-compose up --build
```

4. **Acceder a la aplicación**
```
http://localhost:8501
```

### Opción 2: Ejecución Local sin Docker

1. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

4. **Ejecutar la aplicación**
```bash
streamlit run app.py
```

### Opción 3: Deploy en Streamlit Cloud

1. **Fork del repositorio** en GitHub
2. **Crear app en [Streamlit Cloud](https://streamlit.io/cloud)**
3. **Configurar Secrets** en el dashboard de Streamlit:
   - Agregar todas las variables del `.env.example` como secrets
4. **Nota**: El historial no se persistirá entre sesiones en Streamlit Cloud

## 🗄️ Configuración de Supabase

### Base de Datos Vectorial

El proyecto utiliza tres tablas en Supabase, cada una con su función RPC correspondiente:

| Agente   | Tabla      | Query RPC       | Modelo Embedding | Costo | Dimensiones |
|----------|------------|-----------------|------------------|-------|-------------|
| Wollok   | `wollok`   | `wollok_search` | openai/text-embedding-3-small (via OpenRouter) | $0.02/M tokens | 1536 |
| Haskell  | `haskell`  | `haskell_search`| openai/text-embedding-3-small (via OpenRouter) | $0.02/M tokens | 1536 |
| Prolog   | `prolog`   | `prolog_search` | openai/text-embedding-3-small (via OpenRouter) | $0.02/M tokens | 1536 |

### Configuración de las Funciones RPC

Cada tabla debe tener una función RPC para búsqueda semántica. Ejemplo para `wollok_search`:

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

**Parámetros:**
- `query_embedding`: Vector de embedding (1536 dimensiones con text-embedding-3-small)
- `match_count`: Número de resultados a retornar (default: NULL para todos)
- `filter`: Filtro opcional sobre metadata en formato JSONB (default: '{}' sin filtro)

Replica esta función para `haskell_search` y `prolog_search` cambiando el nombre de la tabla.

## 🔧 Personalización

### Agregar un Nuevo Agente

1. **Editar `config/agents.py`**:
```python
AGENT_NUEVO = {
    "name": "Nuevo",
    "table": "nuevo_table",
    "query_name": "nuevo_search",
    "system_prompt": """..."""
}

AGENTS = {
    "Wollok": AGENT_WOLLOK,
    "Haskell": AGENT_HASKELL,
    "Prolog": AGENT_PROLOG,
    "Nuevo": AGENT_NUEVO  # Agregar aquí
}
```

2. **Crear tabla y función en Supabase** siguiendo el patrón de las existentes

### Modificar System Prompts

Los system prompts de cada agente están en `config/agents.py`. Puedes editarlos para ajustar el comportamiento del tutor.

## 📚 Tecnologías Utilizadas

- **Frontend**: [Streamlit](https://streamlit.io/)
- **LLM Framework**: [LangChain](https://python.langchain.com/)
- **Modelos**: [OpenRouter](https://openrouter.ai/) (Gemini, GPT-4, Grok)
- **Embeddings**: OpenAI `text-embedding-ada-002`
- **Base de Datos Vectorial**: [Supabase](https://supabase.com/) (pgvector)
- **Base de Datos Local**: SQLite
- **File Processing**: PyPDF2, Pillow
- **Containerización**: Docker & Docker Compose

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 🧪 Testing

ChatPdeP incluye una suite completa de tests con **LLM-as-a-Judge** para garantizar calidad.

### Ejecutar Tests

```bash
# Todos los tests
./run_tests.sh        # Linux/Mac
run_tests.bat         # Windows

# Tests específicos
./run_tests.sh unit           # Tests unitarios
./run_tests.sh integration    # Tests de integración
./run_tests.sh judge          # Tests con LLM-as-a-Judge
./run_tests.sh coverage       # Tests con cobertura
```

### LLM-as-a-Judge

Los tests usan GPT-4o-mini como juez para evaluar:
- ✅ Relevancia al paradigma correcto
- ✅ Corrección técnica
- ✅ Claridad pedagógica
- ✅ Completitud de respuestas
- ✅ Uso apropiado del contexto RAG

**Score mínimo requerido:** 7.0/10

Ver [TESTING.md](TESTING.md) para documentación completa.

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.

## 👥 Autores

- UTN FRBA - Tomas Cabrera Roman - Estudiante

## 🙏 Agradecimientos

- A los estudiantes y profesores de la materia por su feedback
- A la comunidad de LangChain y Streamlit por sus excelentes herramientas


