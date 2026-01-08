# ⚡ Quick Start - ChatPdeP

Guía rápida para levantar ChatPdeP en 5 minutos.

## 🚀 Opción 1: Docker (La Más Rápida)

### Requisitos
- Docker y Docker Compose instalados
- API keys (ver abajo)

### Pasos

1. **Clonar repositorio**
```bash
git clone <tu-repositorio>
cd agents_pdep
```

2. **Crear archivo .env**
```bash
# Linux/Mac
cp .env.example .env

# Windows
copy .env.example .env
```

3. **Editar .env con tus API keys**
```env
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_SERVICE_KEY=eyJxxxxxxxxxxxxx
```

4. **Levantar aplicación**
```bash
docker-compose up --build
```

5. **Abrir en navegador**
```
http://localhost:8501
```

✅ **¡Listo!** Ya puedes usar ChatPdeP.

---

## 🖥️ Opción 2: Local Sin Docker

### Requisitos
- Python 3.11 o superior
- pip instalado
- API keys (ver abajo)

### Pasos

**Linux/Mac:**
```bash
# 1. Clonar repo
git clone <tu-repositorio>
cd agents_pdep

# 2. Ejecutar script
chmod +x run_local.sh
./run_local.sh
```

**Windows:**
```cmd
REM 1. Clonar repo
git clone <tu-repositorio>
cd agents_pdep

REM 2. Ejecutar script
run_local.bat
```

El script automáticamente:
- Crea entorno virtual
- Instala dependencias
- Ejecuta Streamlit

---

## 🔑 Obtener API Keys (5 minutos)

### 1. OpenRouter (GRATIS con créditos)

1. Ve a [openrouter.ai](https://openrouter.ai)
2. Registrate/Login
3. Ve a [openrouter.ai/keys](https://openrouter.ai/keys)
4. Crea key → Copia (empieza con `sk-or-v1-`)

💰 **$5 de crédito gratis** al registrarte

### 2. OpenAI (Para embeddings)

1. Ve a [platform.openai.com](https://platform.openai.com)
2. Registrate/Login
3. Ve a [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
4. Crea key → Copia (empieza con `sk-`)

💵 Agrega $5-10 a tu cuenta (embeddings son muy baratos)

### 3. Supabase

**Opción A:** Usar base de datos existente del proyecto
- Solicita credenciales al admin

**Opción B:** Crear tu propia base de datos
- Ve a [supabase.com](https://supabase.com)
- Crea proyecto gratis
- Settings → API → Copia URL y service_role key
- ⚠️ Necesitarás configurar las tablas (ver SETUP.md)

---

## 🎮 Uso Básico

### 1. Seleccionar Tutor

En el sidebar, elige:
- **Wollok** (Programación Orientada a Objetos)
- **Haskell** (Programación Funcional)
- **Prolog** (Programación Lógica)

### 2. Seleccionar Modelo

Recomendados:
- `gemini-2.0-flash-exp:free` (gratis, rápido)
- `gpt-4o-mini` (muy bueno, económico)
- `grok-2-1212` (potente, más caro)

### 3. Hacer una Pregunta

Ejemplos:

**Wollok:**
```
¿Cómo implemento herencia en Wollok?
```

**Haskell:**
```
¿Qué son las funciones de orden superior?
```

**Prolog:**
```
Explícame la unificación con ejemplos
```

### 4. Adjuntar Archivos (Opcional)

- Click en "📎 Adjuntar archivo"
- Soporta: PDFs e Imágenes
- El agente analizará el contenido

---

## 💡 Tips

### Mejores Prácticas

✅ **Sé específico en tus preguntas**
```
❌ "ayuda con objetos"
✅ "¿Cómo defino atributos privados en una clase Wollok?"
```

✅ **Usa el contexto**
```
"En el código que te pasé en el PDF, ¿cómo puedo mejorar el método calcular()?"
```

✅ **Pide código completo**
```
"Dame el código completo de una clase Punto con x e y"
```

### Ajustar Ventana de Contexto

- **4-6 mensajes**: Respuestas rápidas, menor contexto
- **8-12 mensajes**: Balanceado (recomendado)
- **14-20 mensajes**: Conversaciones largas, más contexto

### Cambiar de Agente

Si cambias de Wollok a Haskell:
- Se creará una nueva conversación automáticamente
- El historial anterior se guarda

---

## 🐛 Problemas Comunes

### "Invalid API Key"
- Verifica que copiaste la key completa
- Asegúrate de tener fondos (OpenAI)

### "Connection to Supabase failed"
- Verifica URL y key en `.env`
- Asegúrate de tener internet

### "Module not found"
```bash
pip install -r requirements.txt --force-reinstall
```

### La app no se ve bien
```bash
streamlit cache clear
streamlit run app.py
```

---

## 📚 Más Información

- **Guía completa**: Ver `SETUP.md`
- **Documentación**: Ver `README.md`
- **Estructura**: Ver `PROJECT_STRUCTURE.md`
- **Migración N8N**: Ver `MIGRATION_FROM_N8N.md`

---

## 🎓 Primeros Pasos Recomendados

### 1. Prueba Básica
```
Usuario: "¿Qué es Wollok?"
```
Verifica que el agente responde correctamente.

### 2. Prueba con RAG
```
Usuario: "Dame ejemplos de clases en Wollok"
```
El agente debería usar `recuperar_teoria` para buscar info.

### 3. Prueba con Archivo
- Adjunta un PDF con código
- Pregunta sobre ese código

### 4. Prueba Historial
- Haz varias preguntas
- Click en "➕ Nueva Conversación"
- Verifica que puedes volver a la anterior

---

## ⚙️ Configuración Avanzada

### Cambiar Puerto

**Docker:**
```yaml
# docker-compose.yml
ports:
  - "8502:8501"  # Usar puerto 8502
```

**Local:**
```bash
streamlit run app.py --server.port 8502
```

### Cambiar Ubicación de DB

```bash
# .env
DB_PATH=custom/path/conversations.db
```

### Variables de Entorno Adicionales

```env
# .env
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

---

## 🚀 Deploy en Cloud

### Streamlit Cloud (GRATIS)

1. Push código a GitHub
2. Ve a [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect repositorio
4. Agregar secrets:
   ```
   OPENROUTER_API_KEY = "sk-or-..."
   OPENAI_API_KEY = "sk-..."
   SUPABASE_URL = "https://..."
   SUPABASE_SERVICE_KEY = "eyJ..."
   ```
5. Deploy!

⚠️ **Nota**: El historial no se persistirá en Streamlit Cloud (SQLite en memoria)

---

## 🎉 ¡Listo!

Ya estás usando ChatPdeP. Algunas ideas:

- 📝 Resuelve ejercicios de la facultad
- 🧪 Experimenta con diferentes paradigmas
- 📚 Aprende nuevos conceptos
- 💬 Pregunta sobre errores en tu código

**¿Problemas?** Revisa `SETUP.md` o abre un issue.

**¡Feliz aprendizaje! 🎓**

