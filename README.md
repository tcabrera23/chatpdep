# 🎓 ChatPdeP - Tutor de Paradigmas de Programación

Aplicación web interactiva que proporciona tutorías personalizadas para la materia "Paradigmas de Programación" de la UTN FRBA. Utiliza inteligencia artificial y RAG (Retrieval Augmented Generation) para asistir a estudiantes con tres paradigmas principales: **Wollok (OOP)**, **Haskell (Funcional)** y **Prolog (Lógico)**.

## 🆕 Versión 2.0 - Nuevas Características

- **⚡ Groq API gratuita** - Usa Llama 3.3 70B gratis (ideal para empezar)
- **☁️ Streamlit Cloud ready** - Publica tu app y compártela con el mundo
- **💻 Soporte para modelos locales** con Ollama (ejecución sin costo)
- **🎯 Clasificación automática** de consultas para optimizar costos
- **➕ Modelos personalizados** desde OpenRouter/Groq
- **🔄 Sistema de fallbacks** inteligente
- **📝 Summarización mejorada** con detección automática de límites

> 📖 **[Ver NEW_VERSION.md](NEW_VERSION.md)** para detalles completos de la versión 2.0
> 🚀 **[Ver STREAMLIT_CLOUD_DEPLOY.md](STREAMLIT_CLOUD_DEPLOY.md)** para publicar en cloud

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

### 🆕 Nuevas Funcionalidades v2.0

- **⚡ Groq API Gratuita**: 
  - Llama 3.3 70B gratis (70B parámetros)
  - Mixtral 8x7B gratis
  - Sin costo, ideal para estudiantes
  - Velocidad ultrarrápida
- **☁️ Streamlit Cloud Ready**:
  - Publica tu app en minutos
  - Comparte con link público
  - Sesiones por navegador (no requiere login)
  - **[Ver guía de deploy](STREAMLIT_CLOUD_DEPLOY.md)**
- **💻 Modelos Locales con Ollama**: Ejecuta LLMs en tu máquina sin costo
  - `phi4-mini` (3.8B) y `qwen3:4b` (4B) instalados por defecto
  - Soporte para `deepseek-coder:6.7b`, `qwen2.5-coder:7b`
- **🎯 Clasificación Automática**: Optimiza costos eligiendo el modelo según:
  - Tipo de consulta (teórica, código, debugging)
  - Dificultad (simple, media, compleja)
  - Tier sugerido (economy, balanced, premium)
- **➕ Modelos Personalizados**: Agrega cualquier modelo de OpenRouter/Groq copiando su ID
- **🔄 Fallbacks Inteligentes**: Si un modelo falla, usa Groq automáticamente
- **📝 Summarización Adaptativa**: Detecta límites de contexto por modelo

### 🎨 Interfaz de Usuario

**Sidebar:**
- **🌐 Selector de Proveedor**: Elige entre ⚡ Groq (gratis), ☁️ OpenRouter (pago) o 💻 Local (Ollama)
- Configuración de API Key de Groq (gratis, por defecto)
- Configuración de API Key de OpenRouter (solo si usas cloud pago)
- URL de Ollama configurable (solo local)
- **📦 Sugerencias de modelos** para instalar con Ollama
- Selector de Tutor (Wollok/Haskell/Prolog)
- **🎯 Auto-clasificación**: Habilita optimización automática de costos
- Selector de Modelo LLM (manual si auto-clasificación desactivada)
- **➕ Agregar Modelos Personalizados**: Expander para agregar modelos desde OpenRouter/Groq
- Control de ventana de contexto
- Historial de conversaciones con títulos editables
- Botón para nueva conversación

**Área Principal:**
- Chat interactivo con formato limpio
- Indicadores de configuración actual (tutor, modelo, contexto)
- **🎯 Notificaciones de clasificación** (cuando está activa)
- **🔄 Alertas de fallback** si un modelo falla
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
│   ├── database.py            # Gestión de SQLite para historial
│   ├── query_classifier.py    # 🆕 Clasificador de dificultad de consultas
│   └── model_manager.py       # 🆕 Gestor de modelos (cloud + local)
├── data/
│   └── conversations.db       # Base de datos SQLite (generada)
├── requirements.txt           # Dependencias Python (incluye ollama)
├── Dockerfile                 # Configuración Docker
├── docker-compose.yml         # 🆕 Orquestación Docker con Ollama
├── .env.example              # Plantilla de variables de entorno
├── NEW_VERSION.md            # 🆕 Documento de cambios v2.0
└── README.md                 # Este archivo
```

## 🚀 Instalación y Ejecución

### Opción 1: Ejecución Local con Docker (Recomendado) 🐳

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
- `GROQ_API_KEY`: Tu API key de [Groq](https://console.groq.com/keys) (gratis, recomendado)
- `OPENROUTER_API_KEY`: Tu API key de [OpenRouter](https://openrouter.ai/keys) (opcional si solo usas Groq o Ollama)
- `SUPABASE_URL`: URL de tu proyecto Supabase
- `SUPABASE_ANON_KEY`: Anon/public key de Supabase (Settings → API)
- `OLLAMA_BASE_URL`: URL de Ollama (por defecto: `http://ollama:11434` en Docker)

> 🔒 **Seguridad:** Usamos `ANON_KEY` con Row Level Security (RLS) en lugar de `SERVICE_KEY`. Ver [SEGURIDAD_RLS.md](SEGURIDAD_RLS.md)

3. **Levantar con Docker**
```bash
docker-compose up --build
```

**¿Qué se instala?**
- ✅ ChatPdeP en `http://localhost:8501`
- ✅ Ollama en `http://localhost:11434`
- ✅ Modelo `phi4-mini` (3.8B) y `qwen3:4b` (4B) instalados automáticamente

**Primera ejecución:**
- Tarda ~3-5 minutos en descargar los modelos (~2.2GB + ~3GB)
- Los logs muestran el progreso: `docker logs -f chatpdep_ollama`

4. **Acceder a la aplicación**
```
http://localhost:8501
```

5. **Instalar más modelos (opcional)**
```bash
# Modelos recomendados para código
docker exec -it chatpdep_ollama ollama pull deepseek-coder:6.7b
docker exec -it chatpdep_ollama ollama pull qwen2.5-coder:7b

# Ver modelos instalados
docker exec -it chatpdep_ollama ollama list
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

### Opción 3: Deploy en Streamlit Cloud ☁️

Publica ChatPdeP y compártelo con el mundo:

1. **Repositorio público en GitHub**
2. **Crear cuenta en [Streamlit Cloud](https://share.streamlit.io)** (gratis)
3. **Deploy en 3 clics**:
   - New app → Selecciona tu repo → Deploy
4. **Configurar Secrets**:
   - Settings → Secrets → Pegar configuración de `.streamlit/secrets.toml.example`

**📖 Guía completa:** [STREAMLIT_CLOUD_DEPLOY.md](STREAMLIT_CLOUD_DEPLOY.md)

**Funcionalidades en Cloud:**
- ✅ Groq gratis (Llama 3.3 70B)
- ✅ OpenRouter (modelos premium)
- ✅ Auto-clasificación
- ✅ RAG con Supabase
- ⚠️ Sin persistencia de conversaciones (solo durante sesión)
- ❌ Ollama no disponible (solo local)

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
- **Modelos Gratis**: [Groq](https://groq.com/) (Llama 3.3, Mixtral - **Gratis**)
- **Modelos Cloud**: [OpenRouter](https://openrouter.ai/) (Gemini, GPT-5, Grok, Claude)
- **Modelos Locales**: [Ollama](https://ollama.ai/) (Phi, Qwen, DeepSeek)
- **Embeddings**: OpenAI `text-embedding-3-small`
- **Base de Datos Vectorial**: [Supabase](https://supabase.com/) (pgvector)
- **Base de Datos Local**: SQLite / Session State (cloud)
- **File Processing**: PyPDF2, Pillow
- **Containerización**: Docker & Docker Compose
- **Hosting**: Streamlit Cloud (gratis)

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

## 🆕 Guía de Uso - Nuevas Características

### Usar Modelos Locales (Ollama)

1. **Inicia Docker** (si no está corriendo):
   ```bash
   docker-compose up -d
   ```

2. **En la app**, ve al sidebar:
   - Selecciona "💻 Local (Ollama)"
   - Elige un modelo (ej: "Phi 4 Mini")

3. **¡Listo!** Ahora usas modelos locales sin costo

**Ventajas:**
- ✅ $0 en costos de API
- ✅ Privacidad total
- ✅ Sin límites de tokens
- ✅ Funciona sin internet (después de instalar)

**Desventajas:**
- ❌ Requiere recursos locales (RAM, CPU/GPU)
- ❌ Modelos algo menos potentes que GPT-4 o Claude

---

### Optimizar Costos con Auto-Clasificación

1. **Activa en sidebar**: Marca "🎯 Auto-clasificar (optimizar costos)"

2. **Haz tu pregunta** normalmente

3. **El sistema analiza**:
   - "¿Qué es polimorfismo?" → Groq Llama 3.3 70B (Gratis)
   - "Resuelve este ejercicio de Wollok" → Groq Mixtral 8x7B (Gratis)
   - "Debug este error complejo" → Claude Opus ($5/$25)

4. **Resultados**:
   - Ahorro promedio: 60-80% en costos (¡o 100% con Groq!)
   - Calidad apropiada para cada tipo de consulta

**Ejemplo de ahorro:**

| Sin auto-clasificación | Con auto-clasificación | Ahorro |
|------------------------|------------------------|--------|
| 100 consultas con Opus | 60 teóricas (Groq Llama) + 30 código (Groq Mixtral) + 10 debug (Opus) | ~90% (¡o más!) |
| Costo: ~$50 | Costo: ~$5 | **$45** |

---

### Agregar Modelos Personalizados

1. **Encuentra tu modelo** en [OpenRouter](https://openrouter.ai/models) o [Groq Console](https://console.groq.com/keys)

2. **Copia el ID** (ej: `openai/gpt-4o`, `anthropic/claude-3.5-sonnet`, `llama-3.3-70b-versatile`)

3. **En el sidebar**, abre "➕ Agregar modelo personalizado"

4. **Completa**:
   - Proveedor: `OpenRouter` o `Groq`
   - ID: `openai/gpt-4o` (o el que copiaste)
   - Nombre: "GPT-4o Turbo" (o el que quieras)
   - Tier: Premium (o el adecuado)

5. **Agrega** y ya está disponible en el selector

**Casos de uso:**
- Quieres probar el último modelo experimental
- Necesitas un modelo específico para tu caso
- Comparar diferentes modelos

---

### Sistema de Fallbacks

**Funcionamiento automático:**

1. Seleccionas un modelo (ej: Opus)
2. Si falla (API caída, sin créditos, etc.)
3. Sistema usa Groq Llama 3.3 70B automáticamente
4. Te notifica del cambio
5. Tu conversación continúa sin interrupciones

**Notificaciones:**
- 🔄 "Modelo falló, usando fallback: Groq Llama 3.3 70B"
- 💡 "Razón: Rate limit exceeded"

**Casos especiales:**
- **Modelo local falla**: Te pide cambiar a cloud o verificar Ollama
- **No hay API Key**: Te pide configurarla

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.

## 👥 Autores

- UTN FRBA - Tomas Cabrera Roman - Estudiante

## 🙏 Agradecimientos

- A los estudiantes y profesores de la materia por su feedback
- A la comunidad de LangChain y Streamlit por sus excelentes herramientas


