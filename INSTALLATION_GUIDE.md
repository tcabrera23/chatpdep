# 📘 Guía de Instalación Completa - ChatPdeP v2.0

Esta guía te ayudará a instalar y configurar ChatPdeP en diferentes escenarios.

---

## 🎯 Elige tu Escenario

### Escenario 1: Desarrollo Local con Docker (Recomendado)
✅ Mejor para: Desarrollo, testing, uso personal  
✅ Incluye: Ollama local + Cloud API  
✅ Requiere: Docker Desktop

### Escenario 2: Solo Cloud (Sin Ollama)
✅ Mejor para: Producción, despliegue rápido  
✅ Incluye: Solo modelos cloud (OpenRouter)  
✅ Requiere: API Key de OpenRouter

### Escenario 3: Local Sin Docker
✅ Mejor para: Desarrollo sin Docker, personalización avanzada  
✅ Incluye: Python directo, configuración manual  
✅ Requiere: Python 3.11+

---

## 📦 Escenario 1: Docker Completo (Cloud + Local)

### Prerrequisitos

1. **Docker Desktop** instalado
   - [Windows/Mac](https://www.docker.com/products/docker-desktop)
   - Linux: `sudo apt install docker.io docker-compose`

2. **Git** instalado (opcional)

3. **Hardware recomendado para Ollama:**
   - **CPU**: 4+ cores
   - **RAM**: 8GB mínimo, 16GB recomendado
   - **Disco**: 10GB+ libres
   - **GPU** (opcional): NVIDIA con CUDA para mayor velocidad

### Instalación Paso a Paso

#### 1. Clonar o Descargar el Proyecto

```bash
# Opción A: Con Git
git clone <tu-repositorio>
cd agents_pdep

# Opción B: Descargar ZIP y extraer
# cd a la carpeta extraída
```

#### 2. Configurar Variables de Entorno

```bash
# Copiar el template
cp .env.example .env

# Editar .env con tu editor favorito
nano .env  # o notepad .env en Windows
```

**Configuración mínima del `.env`:**

```bash
# OpenRouter (opcional si solo usas Ollama)
OPENROUTER_API_KEY=sk-or-v1-tu-api-key-aqui

# Supabase (requerido)
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_ANON_KEY=tu-anon-key-aqui

# Ollama (se configura automáticamente en Docker)
OLLAMA_BASE_URL=http://ollama:11434
```

**¿Dónde obtener las keys?**
- **OpenRouter**: [https://openrouter.ai/keys](https://openrouter.ai/keys) (crea cuenta gratis)
- **Supabase**: [https://supabase.com](https://supabase.com) → Tu proyecto → Settings → API

#### 3. Elegir Configuración de Docker

**Opción A: Con GPU (NVIDIA)**

Si tienes GPU NVIDIA:

```bash
docker-compose up --build
```

**Opción B: Solo CPU (Sin GPU)**

Si NO tienes GPU o no es NVIDIA:

```bash
docker-compose -f docker-compose.cpu.yml up --build
```

#### 4. Esperar Instalación

**Primera ejecución (~3-5 minutos):**
1. Construye imagen de ChatPdeP (~1 min)
2. Descarga imagen de Ollama (~30 seg)
3. Descarga modelo phi4-mini (~2-3 min, 2.2GB)

**Verificar progreso:**
```bash
# En otra terminal
docker logs -f chatpdep_ollama
```

Deberías ver:
```
Instalando phi4-mini (puede tardar 2-3 minutos)...
pulling manifest
pulling 8c9...
...
phi4-mini instalado correctamente!
```

#### 5. Acceder a la Aplicación

Abre tu navegador en:
```
http://localhost:8501
```

¡Listo! ChatPdeP está corriendo con Ollama incluido.

### Instalar Modelos Adicionales

Una vez que la app está corriendo, puedes instalar más modelos:

```bash
# Qwen 3 4B (excelente para código)
docker exec -it chatpdep_ollama ollama pull qwen3-4b

# DeepSeek Coder 6.7B (especialista en programación)
docker exec -it chatpdep_ollama ollama pull deepseek-coder-6.7b

# Qwen 2.5 Coder 7B (muy potente)
docker exec -it chatpdep_ollama ollama pull qwen2.5-coder-7b

# Ver modelos instalados
docker exec -it chatpdep_ollama ollama list
```

**Modelos disponibles:**
- [Ver catálogo completo de Ollama](https://ollama.ai/library)

### Comandos Útiles

```bash
# Detener servicios
docker-compose down

# Reiniciar servicios
docker-compose restart

# Ver logs de ChatPdeP
docker logs -f chatpdep_app

# Ver logs de Ollama
docker logs -f chatpdep_ollama

# Limpiar todo (¡cuidado! borra modelos descargados)
docker-compose down -v
```

---

## ☁️ Escenario 2: Solo Cloud (Sin Ollama)

Si solo quieres usar modelos cloud y no necesitas Ollama local.

### Instalación Rápida

1. **Clonar proyecto**
   ```bash
   git clone <tu-repositorio>
   cd agents_pdep
   ```

2. **Crear `.env` solo con cloud**
   ```bash
   OPENROUTER_API_KEY=tu-api-key
   SUPABASE_URL=tu-url
   SUPABASE_ANON_KEY=tu-key
   ```

3. **Docker sin Ollama**
   
   Crea un `docker-compose.cloud.yml`:
   ```yaml
   version: '3.8'
   
   services:
     chatpdep:
       build: .
       container_name: chatpdep_app
       ports:
         - "8501:8501"
       volumes:
         - ./data:/app/data
       environment:
         - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
         - SUPABASE_URL=${SUPABASE_URL}
         - SUPABASE_SERVICE_KEY=${SUPABASE_ANON_KEY}
       env_file:
         - .env
       restart: unless-stopped
   ```

4. **Levantar**
   ```bash
   docker-compose -f docker-compose.cloud.yml up --build
   ```

5. **Usar**
   - Abre `http://localhost:8501`
   - En el sidebar, selecciona "☁️ Cloud (OpenRouter)"
   - ¡Listo!

---

## 🐍 Escenario 3: Local Sin Docker

Para desarrollo avanzado o sistemas sin Docker.

### Prerrequisitos

- Python 3.11 o superior
- pip
- Ollama instalado (opcional, para modelos locales)

### Instalación

#### 1. Instalar Python y Dependencias

```bash
# Clonar proyecto
git clone <tu-repositorio>
cd agents_pdep

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

#### 2. Instalar Ollama (Opcional)

**Windows/Mac:**
- Descargar desde [ollama.ai](https://ollama.ai/download)
- Instalar y ejecutar

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve
```

**Instalar modelos:**
```bash
ollama pull phi4-mini
ollama pull qwen3-4b
```

#### 3. Configurar `.env`

```bash
cp .env.example .env
# Editar .env con tus credenciales

# Si Ollama está local:
OLLAMA_BASE_URL=http://localhost:11434
```

#### 4. Ejecutar

```bash
streamlit run app.py
```

Abre: `http://localhost:8501`

---

## 🔧 Configuración de Supabase

ChatPdeP requiere Supabase para la base de datos vectorial (RAG).

### Setup Inicial

1. **Crear proyecto** en [Supabase](https://supabase.com)

2. **Crear tablas** para cada paradigma:
   - `wollok`
   - `haskell`
   - `prolog`

3. **Habilitar extensión pgvector**:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```

4. **Crear tabla** (ejemplo para Wollok):
   ```sql
   CREATE TABLE wollok (
       id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
       content TEXT NOT NULL,
       metadata JSONB,
       embedding VECTOR(1536)
   );
   
   CREATE INDEX ON wollok USING ivfflat (embedding vector_cosine_ops)
   WITH (lists = 100);
   ```

5. **Crear función RPC** para búsqueda:
   ```sql
   CREATE OR REPLACE FUNCTION wollok_search(
       query_embedding VECTOR,
       match_count INTEGER DEFAULT NULL,
       filter JSONB DEFAULT '{}'
   )
   RETURNS TABLE(
       id UUID,
       content TEXT,
       metadata JSONB,
       similarity DOUBLE PRECISION
   )
   LANGUAGE plpgsql
   AS $$
   BEGIN
       RETURN QUERY
       SELECT
           wollok.id,
           wollok.content,
           wollok.metadata,
           1 - (wollok.embedding <=> query_embedding) AS similarity
       FROM wollok
       WHERE (filter = '{}' OR metadata @> filter)
       ORDER BY wollok.embedding <=> query_embedding
       LIMIT match_count;
   END;
   $$;
   ```

6. **Repetir para `haskell` y `prolog`**

### Poblar Base de Conocimientos

Puedes usar el script de ingestion (si está disponible) o insertar manualmente:

```python
from tools.rag_tool import get_rag_instance

rag = get_rag_instance()

# Insertar teoría
rag.insert_theory(
    content="Wollok es un lenguaje orientado a objetos...",
    metadata={"topic": "introducción", "paradigm": "OOP"},
    table_name="wollok"
)
```

---

## 🐛 Solución de Problemas

### Docker no inicia

**Error: "Cannot connect to Docker daemon"**

Solución:
```bash
# Verificar que Docker Desktop esté corriendo
docker ps

# Si no, iniciar Docker Desktop manualmente
```

---

### Ollama no responde

**Error: "Connection refused to Ollama"**

Solución:
```bash
# Verificar que el contenedor esté corriendo
docker ps | grep ollama

# Ver logs
docker logs chatpdep_ollama

# Reiniciar
docker-compose restart ollama

# Verificar que el modelo esté instalado
docker exec -it chatpdep_ollama ollama list
```

---

### Error de API Key

**Error: "Invalid OpenRouter API Key"**

Solución:
1. Verifica que la key sea correcta en `.env`
2. Verifica que tenga créditos en OpenRouter
3. Prueba la key directamente:
   ```bash
   curl https://openrouter.ai/api/v1/models \
     -H "Authorization: Bearer $OPENROUTER_API_KEY"
   ```

---

### Modelo no encontrado

**Error: "Model not found in Ollama"**

Solución:
```bash
# Listar modelos instalados
docker exec -it chatpdep_ollama ollama list

# Si no está, instalar
docker exec -it chatpdep_ollama ollama pull phi4-mini
```

---

### Puerto 8501 ya en uso

**Error: "Port 8501 is already in use"**

Solución:
```bash
# Opción A: Detener el proceso que usa el puerto
# Windows:
netstat -ano | findstr :8501
taskkill /PID <pid> /F

# Linux/Mac:
lsof -i :8501
kill -9 <pid>

# Opción B: Cambiar puerto en docker-compose.yml
ports:
  - "8502:8501"  # Usar puerto 8502 en lugar de 8501
```

---

### Memoria insuficiente

**Error: Container killed (OOM)**

Solución:
1. Usar modelos más pequeños:
   - phi4-mini (3.8B) - Más ligero
   - En lugar de modelos 7B+

2. Aumentar memoria de Docker:
   - Docker Desktop → Settings → Resources → Memory
   - Asignar al menos 8GB

3. Usar solo cloud (sin Ollama):
   ```bash
   docker-compose -f docker-compose.cloud.yml up
   ```

---

### Base de datos Supabase no conecta

**Error: "Connection to Supabase failed"**

Solución:
1. Verifica URL y key en `.env`
2. Verifica que el proyecto Supabase esté activo
3. Verifica que las tablas existan:
   ```sql
   SELECT * FROM wollok LIMIT 1;
   ```
4. Verifica RLS (Row Level Security):
   - Supabase → Authentication → Policies
   - Asegúrate de tener políticas correctas

---

## 📊 Verificación de Instalación

### Checklist Completo

✅ **Docker:**
```bash
docker --version  # Debe mostrar versión
docker-compose --version
```

✅ **Servicios corriendo:**
```bash
docker ps
# Debe mostrar:
# - chatpdep_app
# - chatpdep_ollama (si usas Ollama)
```

✅ **App accesible:**
- Abrir `http://localhost:8501`
- Debe cargar interfaz de ChatPdeP

✅ **Ollama funcional:**
```bash
docker exec -it chatpdep_ollama ollama list
# Debe mostrar al menos phi4-mini
```

✅ **Supabase conectado:**
- En la app, hacer una pregunta
- No debe mostrar errores de conexión

✅ **OpenRouter funcional:**
- Configurar API key en sidebar
- Seleccionar modelo cloud
- Hacer pregunta
- Debe responder sin errores

---

## 🎓 Próximos Pasos

Una vez instalado:

1. **Lee el NEW_VERSION.md** para conocer todas las características
2. **Prueba los diferentes modos**:
   - Local (Ollama) con phi4-mini
   - Cloud con auto-clasificación
   - Modelos personalizados
3. **Explora los tutores**: Wollok, Haskell, Prolog
4. **Adjunta archivos**: PDFs e imágenes
5. **Revisa el historial**: Gestiona tus conversaciones

---

## 📞 Soporte

Si tienes problemas no cubiertos en esta guía:

1. Revisa los **logs**:
   ```bash
   docker logs chatpdep_app
   docker logs chatpdep_ollama
   ```

2. Busca el error en **GitHub Issues**

3. Crea un **nuevo issue** con:
   - Descripción del problema
   - Logs relevantes
   - Sistema operativo
   - Versión de Docker

---

**¡Disfruta de ChatPdeP v2.0!** 🎉
