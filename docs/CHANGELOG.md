# 📝 Changelog - ChatPdeP

## [2.0.0] - 2026-01-07 - Migración Completa desde N8N

### 🎉 Nueva Implementación Python/Streamlit

Esta versión representa una reescritura completa del proyecto, migrando desde N8N a una aplicación Python standalone con Streamlit.

---

## ✨ Features Nuevos

### Agentes Múltiples
- ✅ **3 Agentes especializados**: Wollok, Haskell y Prolog
- ✅ System prompts dedicados y optimizados para cada paradigma
- ✅ Configuración centralizada en `config/agents.py`
- ✅ Fácil extensibilidad para agregar nuevos agentes

### Interfaz de Usuario
- ✅ Interfaz Streamlit moderna y responsive
- ✅ **Sidebar completo** con:
  - Configuración de API keys
  - Selector de agente (tutor)
  - Selector de modelo LLM
  - Control de ventana de contexto
  - Historial de conversaciones
- ✅ **Chat principal** con:
  - Formato mensaje por mensaje
  - Indicadores de archivos adjuntos
  - Respuestas del agente en tiempo real
  - Información de configuración actual

### Gestión de Archivos
- ✅ Soporte para **PDFs** (extracción de texto con PyPDF2)
- ✅ Soporte para **Imágenes** (análisis con modelo de visión)
- ✅ Detección automática de tipo de archivo
- ✅ Manejo robusto de errores

### Historial y Persistencia
- ✅ **Base de datos SQLite** local
- ✅ Almacenamiento de conversaciones con metadata:
  - ID único de conversación
  - Título editable
  - Agente utilizado
  - Modelo LLM usado
  - Timestamps de creación y actualización
- ✅ Historial completo de mensajes
- ✅ Indicadores de archivos adjuntos por mensaje
- ✅ Funciones de gestión:
  - Crear nueva conversación
  - Cargar conversación anterior
  - Eliminar conversación

### RAG (Retrieval Augmented Generation)
- ✅ Tool `recuperar_teoria` para búsqueda semántica
- ✅ Integración con Supabase (pgvector)
- ✅ **Configuración por agente**:
  - Wollok: tabla `wollok`, query `wollok_search`
  - Haskell: tabla `haskell`, query `haskell_search`
  - Prolog: tabla `prolog`, query `prolog_search`
- ✅ Embeddings OpenAI (1536 dimensiones)
- ✅ Resultados formateados con scores de similitud

### Modelos LLM
- ✅ Integración con OpenRouter
- ✅ Soporte para múltiples modelos:
  - Google Gemini 2.0 Flash (gratuito)
  - OpenAI GPT-4o-mini
  - X.AI Grok 2
- ✅ Selección dinámica desde la UI
- ✅ Configuración de temperatura y parámetros

### LangChain Integration
- ✅ AgentExecutor para manejo robusto del agente
- ✅ Tool calling nativo
- ✅ Chat history con MessagesPlaceholder
- ✅ Manejo de errores y reintentos
- ✅ Límite de iteraciones configurable

---

## 🏗️ Arquitectura

### Estructura del Proyecto
```
agents_pdep/
├── app.py                     # Aplicación Streamlit principal
├── config/
│   ├── __init__.py
│   └── agents.py             # Configuración de agentes y prompts
├── tools/
│   ├── __init__.py
│   ├── rag_tool.py           # Herramienta RAG (Supabase)
│   └── file_extraction.py    # Extracción de PDFs e imágenes
├── utils/
│   ├── __init__.py
│   └── database.py           # Gestión de SQLite
├── data/
│   └── conversations.db      # Base de datos (auto-generada)
├── requirements.txt          # Dependencias Python
├── Dockerfile                # Imagen Docker
├── docker-compose.yml        # Orquestación Docker
├── .env.example              # Plantilla de configuración
├── .gitignore                # Archivos ignorados por Git
├── README.md                 # Documentación principal
├── SETUP.md                  # Guía de configuración detallada
└── MIGRATION_FROM_N8N.md     # Documentación de migración
```

### Módulos Principales

#### `app.py`
- Interfaz Streamlit
- Lógica de chat
- Gestión de sesión
- Integración con LangChain

#### `config/agents.py`
- Diccionarios de configuración para cada agente
- System prompts especializados
- Mapping de tablas y queries de Supabase

#### `tools/rag_tool.py`
- Clase `SupabaseRAG` para búsqueda semántica
- Tool `recuperar_teoria` decorada con `@tool`
- Formateo de resultados

#### `tools/file_extraction.py`
- Clase `FileExtractor`
- Extracción de texto de PDFs
- Análisis de imágenes con modelos de visión

#### `utils/database.py`
- Clase `ConversationDatabase`
- CRUD completo para conversaciones
- Schema SQLite con índices optimizados

---

## 🚀 Deployment

### Opciones de Ejecución

#### 1. Docker (Recomendado)
```bash
docker-compose up --build
```

#### 2. Scripts de Inicio
```bash
# Linux/Mac
./run_local.sh

# Windows
run_local.bat
```

#### 3. Manual
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

#### 4. Streamlit Cloud
- Deploy con un clic desde GitHub
- Configurar secrets en el dashboard
- Sin historial persistente (SQLite en memoria)

---

## 📦 Dependencias Principales

- `streamlit>=1.32.0` - Framework de UI
- `langchain>=0.1.10` - Framework de LLM
- `langchain-openai>=0.0.8` - Integración OpenAI
- `openai>=1.12.0` - Cliente OpenAI
- `supabase>=2.3.4` - Cliente Supabase
- `PyPDF2>=3.0.1` - Extracción de PDFs
- `Pillow>=10.2.0` - Procesamiento de imágenes

Ver `requirements.txt` para la lista completa.

---

## 🔧 Configuración

### Variables de Entorno Requeridas

```env
OPENROUTER_API_KEY=sk-or-v1-...    # API key de OpenRouter
OPENAI_API_KEY=sk-...               # API key de OpenAI (embeddings)
SUPABASE_URL=https://....co         # URL del proyecto Supabase
SUPABASE_SERVICE_KEY=eyJ...         # Service key de Supabase
```

### Archivo `.env`
1. Copiar `.env.example` a `.env`
2. Completar con credenciales reales
3. **NUNCA** subir `.env` a Git

---

## 📚 Documentación

### Archivos de Documentación

- **`README.md`**: Documentación principal del proyecto
- **`SETUP.md`**: Guía detallada de configuración paso a paso
- **`MIGRATION_FROM_N8N.md`**: Explicación de la migración desde N8N
- **`CHANGELOG.md`**: Este archivo, historial de cambios

### Documentación en Código

Todos los módulos incluyen:
- Docstrings detallados
- Type hints
- Comentarios explicativos
- Ejemplos de uso

---

## 🧪 Testing

### Estado Actual
- ⚠️ Tests automatizados: **Pendiente**

### Tests Sugeridos para Futuro
- Unit tests para cada módulo
- Integration tests del workflow completo
- Tests de la tool `recuperar_teoria`
- Tests de extracción de archivos
- Tests de base de datos

---

## 🐛 Fixes y Mejoras

### Respecto a N8N
- ✅ Mejor manejo de errores
- ✅ Persistencia de datos (vs Redis volátil)
- ✅ Múltiples agentes (vs solo Wollok)
- ✅ Mejor UX con Streamlit
- ✅ Código versionable con Git
- ✅ Deployment más flexible

### Optimizaciones
- ✅ Índices en base de datos para queries rápidas
- ✅ Singleton pattern para RAG y FileExtractor
- ✅ Caché de sesión en Streamlit
- ✅ Ventana de contexto configurable

---

## 🎯 Roadmap Futuro

### Features Planeados

- [ ] **Streaming de respuestas**: Token por token
- [ ] **Tests automatizados**: Coverage completo
- [ ] **Métricas y analytics**: Dashboard de uso
- [ ] **Multi-usuario**: Autenticación y perfiles
- [ ] **Exportación de conversaciones**: PDF/Markdown
- [ ] **Temas visuales**: Light/Dark mode
- [ ] **Búsqueda en historial**: Full-text search
- [ ] **API REST**: Endpoints para integración
- [ ] **CLI**: Interfaz de línea de comandos

### Mejoras Técnicas

- [ ] Caché de embeddings (Redis/Memcached)
- [ ] Rate limiting y throttling
- [ ] Logging estructurado
- [ ] Monitoreo con Prometheus
- [ ] CI/CD con GitHub Actions
- [ ] Pre-commit hooks

---

## 🙏 Créditos

### Tecnologías Utilizadas
- [Streamlit](https://streamlit.io/) - Framework de UI
- [LangChain](https://python.langchain.com/) - Framework de LLM
- [Supabase](https://supabase.com/) - Base de datos vectorial
- [OpenRouter](https://openrouter.ai/) - Acceso a múltiples LLMs

### Inspiración
- Workflow original en N8N
- ChatGPT por OpenAI
- UTN FRBA - Paradigmas de Programación

---

## 📄 Licencia

MIT License - Ver archivo LICENSE para detalles

---

## 📞 Soporte

Para issues, preguntas o contribuciones:
- Abre un issue en GitHub
- Revisa la documentación en `SETUP.md`
- Consulta `MIGRATION_FROM_N8N.md` para detalles técnicos

---

**¡Gracias por usar ChatPdeP! 🎓**

