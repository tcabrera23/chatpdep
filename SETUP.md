# 🛠️ Guía de Configuración Detallada - ChatPdeP

Esta guía te ayudará a configurar paso a paso todo lo necesario para ejecutar ChatPdeP.

## 📋 Requisitos Previos

### Software Necesario

- **Python 3.11+** (Descargar: [python.org](https://www.python.org/downloads/))
- **Docker** (Opcional, para ejecución con contenedores)
- **Git** (Para clonar el repositorio)

### Cuentas y API Keys Necesarias

1. **OpenRouter** (para modelos LLM)
2. **OpenAI** (para embeddings)
3. **Supabase** (base de datos vectorial)

---

## 🔑 Paso 1: Obtener API Keys

### 1.1 OpenRouter API Key

1. Ve a [openrouter.ai](https://openrouter.ai)
2. Crea una cuenta o inicia sesión
3. Ve a [openrouter.ai/keys](https://openrouter.ai/keys)
4. Crea una nueva API key
5. Copia y guarda la key (comienza con `sk-or-v1-...`)

**Créditos Gratis**: OpenRouter ofrece $5 de crédito gratis al registrarte.

### 1.2 OpenAI API Key

1. Ve a [platform.openai.com](https://platform.openai.com)
2. Crea una cuenta o inicia sesión
3. Ve a [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
4. Crea una nueva API key
5. Copia y guarda la key (comienza con `sk-...`)

**Nota**: Necesitas agregar fondos a tu cuenta OpenAI. Los embeddings son muy económicos (~$0.0001 por 1K tokens).

### 1.3 Supabase Configuration

#### Opción A: Usar Base de Datos Existente (Recomendado si tienes acceso)

Si ya tienes acceso a la base de datos del proyecto:

1. Solicita las credenciales al administrador
2. Te proporcionarán:
   - `SUPABASE_URL`
   - `SUPABASE_SERVICE_KEY`

#### Opción B: Crear Tu Propia Base de Datos

Si deseas crear tu propia base de datos vectorial:

1. **Crear Proyecto en Supabase**
   - Ve a [supabase.com](https://supabase.com)
   - Crea una cuenta gratuita
   - Crea un nuevo proyecto
   - Guarda la contraseña de la base de datos

2. **Obtener Credenciales**
   - En tu proyecto, ve a **Settings** → **API**
   - Copia `URL` (será tu `SUPABASE_URL`)
   - Copia `service_role key` (será tu `SUPABASE_SERVICE_KEY`)

3. **Configurar pgvector**
   
   En el SQL Editor de Supabase, ejecuta:
   
   ```sql
   -- Habilitar extensión pgvector
   create extension if not exists vector;
   ```

4. **Crear Tablas y Funciones**

   Para cada paradigma (Wollok, Haskell, Prolog), ejecuta:

   ```sql
   -- Ejemplo para Wollok (repetir para haskell y prolog)
   
   -- Crear tabla
   CREATE TABLE wollok (
     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
     content text NOT NULL,
     metadata jsonb DEFAULT '{}'::jsonb,
     embedding vector(1536)
   );
   
   -- Crear índice para búsqueda rápida
   CREATE INDEX ON wollok USING ivfflat (embedding vector_cosine_ops);
   
   -- Crear función de búsqueda
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

5. **Poblar las Tablas con Contenido**

   Necesitarás agregar contenido educativo (apuntes, documentación, ejemplos) a las tablas.
   
   Puedes usar un script como este:
   
   ```python
   from langchain_openai import OpenAIEmbeddings
   from supabase import create_client
   import os
   
   # Configurar
   embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
   supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"])
   
   # Ejemplo de contenido
   documentos = [
       "Los objetos en Wollok son instancias que tienen estado y comportamiento...",
       "Una clase en Wollok define un tipo de objeto con atributos y métodos...",
       # Más contenido...
   ]
   
   # Insertar en Supabase
   for doc in documentos:
       embedding = embeddings.embed_query(doc)
       supabase.table("wollok").insert({
           "content": doc,
           "embedding": embedding
       }).execute()
   ```

---

## ⚙️ Paso 2: Configurar el Proyecto

### 2.1 Clonar el Repositorio

```bash
git clone <tu-repositorio>
cd agents_pdep
```

### 2.2 Crear Archivo .env

**En Linux/Mac:**
```bash
cp .env.example .env
```

**En Windows:**
```cmd
copy .env.example .env
```

### 2.3 Editar .env con tus Credenciales

Abre el archivo `.env` con tu editor favorito y completa:

```env
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_SERVICE_KEY=eyJxxxxxxxxxxxxx
```

⚠️ **IMPORTANTE**: Nunca compartas tu archivo `.env` ni lo subas a Git.

---

## 🚀 Paso 3: Ejecutar la Aplicación

### Opción A: Con Scripts de Inicio Rápido

**En Linux/Mac:**
```bash
chmod +x run_local.sh
./run_local.sh
```

**En Windows:**
```cmd
run_local.bat
```

### Opción B: Con Docker

```bash
docker-compose up --build
```

Luego abre: [http://localhost:8501](http://localhost:8501)

### Opción C: Manual

1. **Crear entorno virtual:**
   ```bash
   python -m venv venv
   ```

2. **Activar entorno virtual:**
   
   **Linux/Mac:**
   ```bash
   source venv/bin/activate
   ```
   
   **Windows:**
   ```cmd
   venv\Scripts\activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar:**
   ```bash
   streamlit run app.py
   ```

---

## 🧪 Paso 4: Probar la Aplicación

1. Abre tu navegador en `http://localhost:8501`

2. En el sidebar:
   - Verifica que tu API key esté configurada
   - Selecciona un tutor (Wollok, Haskell o Prolog)
   - Elige un modelo

3. Escribe una pregunta de prueba:
   - Para Wollok: "¿Qué es un objeto en Wollok?"
   - Para Haskell: "¿Cómo funcionan las funciones de orden superior?"
   - Para Prolog: "¿Qué es la unificación?"

4. Si obtienes una respuesta, ¡todo está funcionando! 🎉

---

## 🐛 Solución de Problemas

### Error: "Module not found"

```bash
pip install -r requirements.txt --force-reinstall
```

### Error: "Invalid API Key"

- Verifica que copiaste la key completa sin espacios
- Asegúrate de que la key no haya expirado
- Verifica que tienes fondos en OpenAI (para embeddings)

### Error: "Connection to Supabase failed"

- Verifica que `SUPABASE_URL` y `SUPABASE_SERVICE_KEY` sean correctos
- Asegúrate de tener conexión a internet
- Verifica que tu proyecto Supabase esté activo

### Error: "No se encontró información relevante"

- Tu base de datos vectorial está vacía
- Necesitas poblar las tablas con contenido educativo
- Ver sección "Poblar las Tablas" arriba

### La aplicación se ve mal o no carga

```bash
streamlit cache clear
streamlit run app.py
```

---

## 📞 Soporte

Si tienes problemas adicionales:

1. Revisa los logs en la terminal
2. Busca el error en los issues de GitHub
3. Crea un nuevo issue con:
   - Descripción del problema
   - Logs de error
   - Sistema operativo
   - Versión de Python

---

## 🎓 Recursos Adicionales

- [Documentación de Streamlit](https://docs.streamlit.io/)
- [Documentación de LangChain](https://python.langchain.com/)
- [Documentación de Supabase](https://supabase.com/docs)
- [OpenRouter Models](https://openrouter.ai/models)

---

¡Listo! Ahora deberías tener ChatPdeP funcionando correctamente. 🚀

