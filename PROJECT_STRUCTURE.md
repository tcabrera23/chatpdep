# 📁 Estructura del Proyecto ChatPdeP

## 🌳 Árbol de Directorios

```
agents_pdep/
│
├── 📄 app.py                           # Aplicación Streamlit principal (UI + lógica)
│
├── 📁 config/                          # Configuración de agentes
│   ├── __init__.py                     # Exports del módulo
│   └── agents.py                       # System prompts y config de 3 agentes
│
├── 📁 tools/                           # Herramientas del agente
│   ├── __init__.py                     # Exports del módulo
│   ├── rag_tool.py                     # Tool recuperar_teoria (RAG con Supabase)
│   └── file_extraction.py              # Extracción de PDFs e imágenes
│
├── 📁 utils/                           # Utilidades
│   ├── __init__.py                     # Exports del módulo
│   └── database.py                     # Gestión de SQLite para historial
│
├── 📁 data/                            # Datos persistentes (git-ignored)
│   ├── .gitkeep                        # Mantiene el directorio en Git
│   └── conversations.db                # Base de datos SQLite (auto-generada)
│
├── 📁 venv/                            # Entorno virtual Python (git-ignored)
│
├── 🐳 Dockerfile                       # Imagen Docker de la aplicación
├── 🐳 docker-compose.yml               # Orquestación Docker
├── 🚫 .dockerignore                    # Archivos excluidos de Docker build
│
├── 📦 requirements.txt                 # Dependencias Python
│
├── 🔧 .env.example                     # Plantilla de variables de entorno
├── 🚫 .gitignore                       # Archivos excluidos de Git
│
├── 🚀 run_local.sh                     # Script de inicio (Linux/Mac)
├── 🚀 run_local.bat                    # Script de inicio (Windows)
│
├── 📖 README.md                        # Documentación principal
├── 📖 SETUP.md                         # Guía de configuración detallada
├── 📖 MIGRATION_FROM_N8N.md            # Documentación de migración
├── 📖 CHANGELOG.md                     # Historial de cambios
└── 📖 PROJECT_STRUCTURE.md             # Este archivo
```

---

## 📂 Descripción de Archivos

### 🎯 Archivos Principales

#### `app.py` (Aplicación Principal)
**Líneas: ~350** | **Tipo: Python/Streamlit**

Interfaz de usuario y lógica principal del chat.

**Responsabilidades:**
- Configuración de Streamlit (título, layout, estilos)
- Sidebar con controles (API keys, selección de agente/modelo)
- Área de chat con historial de mensajes
- Input del usuario con soporte para archivos
- Invocación del agente con LangChain
- Gestión de estado de sesión
- Guardado de conversaciones en base de datos

**Componentes clave:**
- `st.chat_message()` - Mensajes del chat
- `st.chat_input()` - Input del usuario
- `st.file_uploader()` - Adjuntar archivos
- `AgentExecutor` - Ejecución del agente
- Session state management

---

### ⚙️ Módulo `config/`

#### `config/agents.py`
**Líneas: ~250** | **Tipo: Python**

Configuración de los 3 agentes (tutores).

**Contenido:**
- `AGENT_WOLLOK` - Configuración del tutor de Wollok (OOP)
- `AGENT_HASKELL` - Configuración del tutor de Haskell (Funcional)
- `AGENT_PROLOG` - Configuración del tutor de Prolog (Lógico)
- `AGENTS` - Diccionario con todos los agentes
- `get_agent_config()` - Función para obtener config de un agente

**Estructura de cada agente:**
```python
{
    "name": "Wollok",
    "table": "wollok",              # Tabla en Supabase
    "query_name": "wollok_search",  # Función RPC en Supabase
    "system_prompt": """..."""      # System prompt completo
}
```

**System Prompts:**
Cada prompt incluye:
- Rol y objetivo del tutor
- Alcance y límites (no alucinaciones)
- Instrucciones de uso de la tool `recuperar_teoria`
- Flujo de trabajo en 4 pasos
- Formato de respuesta
- Criterios de calidad
- Manejo de errores

#### `config/__init__.py`
**Líneas: ~10** | **Tipo: Python**

Exports del módulo para imports limpios.

---

### 🛠️ Módulo `tools/`

#### `tools/rag_tool.py`
**Líneas: ~150** | **Tipo: Python**

Herramienta RAG (Retrieval Augmented Generation).

**Clases:**
- `SupabaseRAG` - Cliente para búsqueda semántica en Supabase
  - `search_theory()` - Busca documentos relevantes
  - `format_results()` - Formatea resultados para el agente

**Functions:**
- `get_rag_instance()` - Singleton del cliente RAG
- `recuperar_teoria()` - Tool decorada con `@tool` para LangChain
- `create_recuperar_teoria_tool()` - Factory para crear tool personalizada

**Flujo:**
1. Recibe query del agente
2. Genera embedding con OpenAI
3. Ejecuta búsqueda en Supabase (RPC function)
4. Formatea resultados con scores de similitud
5. Retorna como string para el agente

#### `tools/file_extraction.py`
**Líneas: ~120** | **Tipo: Python**

Extracción de contenido de archivos adjuntos.

**Clases:**
- `FileExtractor` - Extractor de contenido
  - `extract_from_pdf()` - Extrae texto de PDFs (PyPDF2)
  - `extract_from_image()` - Analiza imágenes con LLM de visión
  - `extract_from_file()` - Detecta tipo y extrae automáticamente

**Functions:**
- `get_file_extractor()` - Singleton del extractor

**Formatos soportados:**
- PDFs: `.pdf`
- Imágenes: `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.webp`

**Para imágenes:**
- Usa modelo `gpt-4o-mini` con capacidad de visión
- Extrae texto, código, diagramas
- Describe contenido visual

#### `tools/__init__.py`
**Líneas: ~10** | **Tipo: Python**

Exports del módulo.

---

### 💾 Módulo `utils/`

#### `utils/database.py`
**Líneas: ~250** | **Tipo: Python**

Gestión de base de datos SQLite para historial.

**Clases:**
- `ConversationDatabase` - Gestor de base de datos
  - `create_conversation()` - Crea nueva conversación
  - `add_message()` - Añade mensaje a conversación
  - `get_conversation_messages()` - Obtiene historial de mensajes
  - `get_all_conversations()` - Lista todas las conversaciones
  - `update_conversation_title()` - Actualiza título
  - `delete_conversation()` - Elimina conversación
  - `get_conversation_info()` - Obtiene metadata de conversación

**Schema SQLite:**

```sql
-- Tabla conversations
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    agent_name TEXT NOT NULL,
    model_name TEXT NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Tabla messages
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id TEXT NOT NULL,
    role TEXT NOT NULL,  -- 'user' o 'assistant'
    content TEXT NOT NULL,
    has_attachment BOOLEAN,
    attachment_type TEXT,  -- 'pdf' o 'image'
    created_at TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations
);
```

**Índices:**
- `idx_conv_id` en `messages.conversation_id`
- `idx_created_at` en `conversations.created_at DESC`

#### `utils/__init__.py`
**Líneas: ~5** | **Tipo: Python**

Exports del módulo.

---

### 🐳 Docker

#### `Dockerfile`
**Líneas: ~30** | **Tipo: Dockerfile**

Imagen Docker de la aplicación.

**Características:**
- Base: `python:3.11-slim`
- Instala dependencias del sistema
- Copia `requirements.txt` y código
- Expone puerto 8501 (Streamlit)
- CMD: `streamlit run app.py`

#### `docker-compose.yml`
**Líneas: ~25** | **Tipo: YAML**

Orquestación de servicios.

**Configuración:**
- Servicio `chatpdep`
- Puerto: 8501:8501
- Volumen: `./data:/app/data` (persistencia)
- Variables de entorno desde `.env`
- Network: `chatpdep_network`
- Restart: `unless-stopped`

#### `.dockerignore`
**Líneas: ~30** | **Tipo: Text**

Archivos excluidos del build de Docker.

---

### 📦 Dependencias

#### `requirements.txt`
**Líneas: ~20** | **Tipo: Text**

Dependencias Python del proyecto.

**Principales:**
- `streamlit` - Framework UI
- `langchain` + `langchain-openai` - Framework LLM
- `openai` - Cliente OpenAI
- `supabase` - Cliente Supabase
- `PyPDF2` - Extracción de PDFs
- `Pillow` - Procesamiento de imágenes
- `python-dotenv` - Variables de entorno

---

### 🚀 Scripts de Inicio

#### `run_local.sh` (Linux/Mac)
**Líneas: ~35** | **Tipo: Bash**

Script para ejecutar la app localmente.

**Funciones:**
- Verifica existencia de `.env`
- Crea entorno virtual si no existe
- Instala/actualiza dependencias
- Ejecuta `streamlit run app.py`

#### `run_local.bat` (Windows)
**Líneas: ~40** | **Tipo: Batch**

Script para ejecutar la app en Windows.

**Funciones:**
- Mismas que `run_local.sh` pero para Windows
- Usa sintaxis de PowerShell/CMD

---

### 📖 Documentación

#### `README.md`
**Líneas: ~200** | **Tipo: Markdown**

Documentación principal del proyecto.

**Secciones:**
- Introducción y features
- Arquitectura del proyecto
- Instalación (3 opciones)
- Configuración de Supabase
- Personalización
- Tecnologías utilizadas
- Contribuciones

#### `SETUP.md`
**Líneas: ~400** | **Tipo: Markdown**

Guía detallada de configuración paso a paso.

**Secciones:**
- Requisitos previos
- Obtención de API keys (con capturas)
- Configuración de Supabase desde cero
- Configuración del proyecto
- Ejecución (3 métodos)
- Pruebas
- Troubleshooting
- Recursos adicionales

#### `MIGRATION_FROM_N8N.md`
**Líneas: ~350** | **Tipo: Markdown**

Documentación de la migración desde N8N.

**Secciones:**
- Comparación N8N vs Python
- Mapeo de componentes
- Mejoras implementadas
- Estructura del código
- Configuración de agentes
- Base de datos
- Performance
- Lecciones aprendidas

#### `CHANGELOG.md`
**Líneas: ~300** | **Tipo: Markdown**

Historial de cambios del proyecto.

**Secciones:**
- Version 2.0.0 (migración completa)
- Features nuevos
- Arquitectura
- Deployment
- Dependencias
- Configuración
- Testing
- Fixes y mejoras
- Roadmap futuro

#### `PROJECT_STRUCTURE.md` (este archivo)
**Líneas: ~400** | **Tipo: Markdown**

Documentación de la estructura del proyecto.

---

### 🔧 Configuración

#### `.env.example`
**Líneas: ~25** | **Tipo: Text**

Plantilla de variables de entorno.

**Variables:**
- `OPENROUTER_API_KEY` - API key de OpenRouter
- `OPENAI_API_KEY` - API key de OpenAI
- `SUPABASE_URL` - URL del proyecto Supabase
- `SUPABASE_SERVICE_KEY` - Service key de Supabase

#### `.gitignore`
**Líneas: ~50** | **Tipo: Text**

Archivos excluidos de Git.

**Categorías:**
- Python artifacts (`__pycache__`, `*.pyc`)
- Virtual environments (`venv/`, `env/`)
- Environment variables (`.env`)
- Database files (`*.db`, `data/`)
- IDE files (`.vscode/`, `.idea/`)
- OS files (`.DS_Store`, `Thumbs.db`)

---

## 📊 Estadísticas del Proyecto

### Líneas de Código (aproximadas)

| Archivo | Líneas | Complejidad |
|---------|--------|-------------|
| `app.py` | ~350 | Alta |
| `config/agents.py` | ~250 | Media |
| `tools/rag_tool.py` | ~150 | Media |
| `tools/file_extraction.py` | ~120 | Media |
| `utils/database.py` | ~250 | Media |
| **Total Código** | **~1120** | - |
| **Total con Docs** | **~2500** | - |

### Módulos

- **Módulos Python**: 3 (config, tools, utils)
- **Archivos Python**: 8 (incluyendo `__init__.py`)
- **Tests**: 0 (pendiente)

### Documentación

- **Archivos Markdown**: 5
- **Total líneas docs**: ~1400
- **Coverage**: Completo (100%)

---

## 🔄 Flujo de Ejecución

### 1. Inicio de la Aplicación

```
run_local.sh/bat
    ↓
Activar venv
    ↓
Instalar dependencies
    ↓
streamlit run app.py
    ↓
Inicializar Streamlit
    ↓
Cargar módulos (config, tools, utils)
    ↓
Renderizar UI
```

### 2. Interacción del Usuario

```
Usuario escribe pregunta [+ adjunta archivo opcional]
    ↓
app.py recibe input
    ↓
FileExtractor procesa archivo (si existe)
    ↓
Construir mensaje completo
    ↓
Obtener configuración del agente (config/agents.py)
    ↓
Crear LLM con OpenRouter
    ↓
Crear tool recuperar_teoria (tools/rag_tool.py)
    ↓
Crear AgentExecutor (LangChain)
    ↓
Invocar agente con mensaje + historial
    ↓
[Agente usa recuperar_teoria si necesita]
    ↓
Agente genera respuesta
    ↓
Mostrar respuesta en UI
    ↓
Guardar en SQLite (utils/database.py)
```

### 3. Tool: recuperar_teoria

```
Agente invoca recuperar_teoria("concepto X")
    ↓
SupabaseRAG.search_theory()
    ↓
Generar embedding con OpenAI
    ↓
Ejecutar RPC function en Supabase
    ↓
Recibir documentos relevantes
    ↓
Formatear resultados
    ↓
Retornar al agente
```

### 4. Extracción de Archivo

```
Usuario adjunta archivo
    ↓
FileExtractor.extract_from_file()
    ↓
Detectar tipo (PDF/imagen)
    ↓
Si PDF: PyPDF2.extract_text()
    ↓
Si imagen: GPT-4o-mini (visión)
    ↓
Retornar contenido extraído
    ↓
Agregar al mensaje del usuario
```

---

## 🎯 Puntos de Extensión

### Agregar Nuevo Agente

**Archivos a modificar:**
1. `config/agents.py` - Agregar `AGENT_NUEVO`
2. `app.py` - Actualizar lista de agentes (automático si usas `AGENTS.keys()`)

### Agregar Nueva Tool

**Archivos a modificar:**
1. Crear `tools/nueva_tool.py`
2. Implementar función decorada con `@tool`
3. Importar en `app.py`
4. Agregar al array `tools` del AgentExecutor

### Agregar Soporte para Nuevo Tipo de Archivo

**Archivos a modificar:**
1. `tools/file_extraction.py`
   - Agregar método `extract_from_X()`
   - Actualizar `extract_from_file()` para detectar nuevo tipo

### Cambiar Base de Datos

**Archivos a modificar:**
1. `utils/database.py` - Reemplazar SQLite por PostgreSQL/MySQL
2. `app.py` - Actualizar inicialización de DB
3. `docker-compose.yml` - Agregar servicio de DB

### Agregar Autenticación

**Archivos a modificar:**
1. Crear `utils/auth.py`
2. `app.py` - Agregar login/logout
3. `utils/database.py` - Agregar campo `user_id`

---

## 📝 Notas

### Archivos Auto-Generados

- `data/conversations.db` - Creado por `ConversationDatabase` al iniciar
- `venv/` - Creado por `python -m venv venv`

### Archivos Ignorados por Git

Ver `.gitignore` para lista completa. Los principales:
- `.env` (contiene secrets)
- `venv/` (entorno virtual)
- `data/` (base de datos local)
- `__pycache__/` (bytecode Python)

### Permisos de Archivos

Scripts de inicio necesitan permisos de ejecución:
```bash
chmod +x run_local.sh
```

---

## 🔗 Referencias

- **Streamlit**: [docs.streamlit.io](https://docs.streamlit.io)
- **LangChain**: [python.langchain.com](https://python.langchain.com)
- **Supabase**: [supabase.com/docs](https://supabase.com/docs)
- **SQLite**: [sqlite.org/docs](https://sqlite.org/docs.html)

---

**Última actualización**: 2026-01-07

