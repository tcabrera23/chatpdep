# 🎉 Nueva Versión - ChatPdeP v2.0

## ¿Qué hay de nuevo?

¡Hemos actualizado ChatPdeP con características increíbles! Ahora puedes usar **Groq gratis**, publicar tu app en **Streamlit Cloud**, optimizar costos y mucho más. Aquí te contamos todo lo nuevo:

---

## 🚀 Características Principales

### 1. ⚡ **Groq API Gratuita** ⭐ NUEVO

¡La mejor forma de empezar con ChatPdeP sin gastar un centavo!

**¿Qué es Groq?**
- API **completamente gratuita** para modelos de IA
- Llama 3.3 70B (70 mil millones de parámetros)
- Mixtral 8x7B y otros modelos potentes
- **Velocidad ultrarrápida** (más rápido que GPT-4)
- Sin límites estrictos en tier gratuito

**¿Por qué Groq?**
- ✅ $0 de costo (perfecto para estudiantes)
- ✅ Sin tarjeta de crédito requerida
- ✅ Calidad comparable a modelos premium
- ✅ Ideal para producción y demo
- ✅ Ahora es el **proveedor por defecto**

**Cómo obtener tu API Key (2 minutos):**
1. Ve a [console.groq.com](https://console.groq.com)
2. Crea cuenta (email + contraseña)
3. API Keys → Create API Key
4. Copia y pega en ChatPdeP
5. ¡Listo! Usa Llama 3.3 70B gratis

**Modelos disponibles en Groq:**
| Modelo | Parámetros | Contexto | Uso Recomendado |
|--------|-----------|----------|-----------------|
| Llama 3.3 70B Versatile | 70B | 128K | Propósito general, desarrollo |
| Llama 3.1 70B Versatile | 70B | 128K | Propósito general |
| Mixtral 8x7B | 8x7B | 32K | Código especializado |
| Gemma 2 9B | 9B | 8K | Consultas rápidas |

---

### 2. ☁️ **Streamlit Cloud Ready** ⭐ NUEVO

¡Publica ChatPdeP y compártelo con el mundo en minutos!

**¿Qué es Streamlit Cloud?**
- Hosting gratuito para apps de Streamlit
- Sin configuración de servidor
- Deploy automático desde GitHub
- SSL y dominio incluidos

**Características:**
- ✅ **100% gratis** para proyectos públicos
- ✅ **Link público** para compartir (ej: `chatpdep-tu-nombre.streamlit.app`)
- ✅ **Deploy en 3 clics** desde GitHub
- ✅ **Sesiones por navegador** (no requiere login por ahora)
- ✅ **Auto-actualizaciones** desde Git

**Lo que funciona en Cloud:**
- ✅ Groq (gratis)
- ✅ OpenRouter (modelos premium)
- ✅ Auto-clasificación de consultas
- ✅ RAG con Supabase
- ✅ Todos los 3 agentes (Wollok/Haskell/Prolog)
- ✅ Archivos adjuntos (durante sesión)

**Limitaciones en Cloud:**
- ⚠️ Conversaciones no persisten entre sesiones (solo en navegador actual)
- ❌ Ollama no disponible (solo funciona local con Docker)
- ⚠️ App se duerme después de 7 días sin uso

**Cómo publicar:**
1. Sube tu repo a GitHub (público)
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. New app → Selecciona tu repo
4. Configura secrets (Groq API Key, Supabase)
5. Deploy

**📖 Guía completa:** [STREAMLIT_CLOUD_DEPLOY.md](STREAMLIT_CLOUD_DEPLOY.md)

---

### 3. 💻 **Soporte para Modelos Locales con Ollama**

¡Ahora puedes ejecutar modelos de IA directamente en tu computadora sin gastar en APIs!

**¿Qué es Ollama?**
- Es una herramienta que te permite correr modelos de lenguaje localmente
- **Costo: $0** (no pagas por tokens)
- Privacidad total: tus conversaciones no salen de tu máquina
- Perfecto para desarrollo y pruebas

**Modelos incluidos:**
- **phi4-mini (3.8B)**: Instalado por defecto, rápido y ligero
- **qwen3-4b**: Excelente para código, balanceado
- **deepseek-coder-6.7b**: Especialista en programación
- **qwen2.5-coder-7b**: Muy potente para desarrollo

**¿Cómo funciona?**
1. Levanta Docker con `docker-compose up`
2. El contenedor de Ollama se instala automáticamente con phi4-mini
3. Selecciona "Local (Ollama)" en el sidebar
4. ¡Listo! Usa modelos locales gratis

---

### 4. ☁️ **Selector Flexible: Groq / OpenRouter / Local**

Ahora puedes elegir entre tres modos:

| Modo | Descripción | Ventajas |
|------|-------------|----------|
| **⚡ Groq (Gratis)** | API gratuita en la nube | Gratis, potente (70B), rápido, sin instalación |
| **☁️ OpenRouter (Pago)** | Modelos premium (API) | Acceso a todos los modelos (GPT-4, Claude) |
| **💻 Local (Ollama)** | Modelos en tu PC | Privacidad total, sin límites, offline |

**Cambio dinámico**: Puedes cambiar de proveedor en cualquier momento desde el sidebar.

---

### 5. 🎯 **Clasificación Automática de Consultas (Optimización de Costos)**

¡El sistema ahora es inteligente y elige el modelo adecuado según tu pregunta!

**¿Cómo funciona?**
El clasificador analiza tu consulta y determina:
- **Tipo**: ¿Es teórica, código, debugging o conceptual?
- **Dificultad**: ¿Simple, media o compleja?
- **Modelo sugerido**: Economy, Balanced o Premium

**Ejemplos:**

| Tu pregunta | Clasificación | Modelo sugerido | Razón |
|------------|---------------|-----------------|-------|
| "¿Qué es un paradigma?" | Teórica Simple | Groq Llama 3.3 | Consulta simple, modelo gratis |
| "Resuelve este ejercicio de Wollok" | Código Media | Groq Mixtral / Grok | Desarrollo de código, rápido |
| "Debug este error complejo" | Debugging Complejo | Claude Opus | Máxima calidad para debugging |

**Ahorro estimado**: 60-80% en costos de tokens usando modelos apropiados

**Activación:**
- Marca "🎯 Auto-clasificar (optimizar costos)" en el sidebar
- El sistema selecciona el modelo automáticamente
- Puedes desactivarlo y elegir manualmente

---

### 6. ➕ **Modelos Personalizados desde OpenRouter/Groq**

¿Quieres usar un modelo específico de OpenRouter? ¡Ahora puedes!

**Cómo agregar un modelo:**
1. Ve a [OpenRouter](https://openrouter.ai/models)
2. Busca el modelo que quieres (ej: `openai/gpt-4o`, `google/gemini-exp-1206`)
3. Copia el ID del modelo
4. En el sidebar, abre "➕ Agregar modelo personalizado"
5. Pega el ID, dale un nombre y selecciona el tier
6. ¡Listo! Ya lo puedes usar

**Ejemplo:**
- ID: `openai/gpt-4o`
- Nombre: "GPT-4o Turbo"
- Tier: Premium
- ✅ Agregado exitosamente

---

### 5. 🔄 **Sistema de Fallbacks Inteligente**

¿Qué pasa si un modelo falla? No te preocupes, ahora hay respaldo automático.

**Funcionamiento:**
1. Si el modelo seleccionado falla (error de API, modelo no disponible, etc.)
2. El sistema automáticamente usa **Gemini 2.5 Flash Lite** como respaldo
3. Te notifica que hubo un problema y qué modelo se usó
4. Tu conversación continúa sin interrupciones

**Casos especiales:**
- **Modelo local falla**: Te pide que selecciones un modelo cloud o verifiques Ollama
- **Modelo cloud falla**: Usa Gemini Flash Lite automáticamente
- **Ambos fallan**: Te muestra un error claro con instrucciones

---

### 8. 📝 **Summarización Mejorada del Chat**

Ahora el sistema es más inteligente con el context window de cada modelo.

**Mejoras:**
- ✅ Detecta automáticamente el límite de contexto de cada modelo
- ✅ Usa 80% del límite para seguridad
- ✅ Resume la conversación cuando se acerca al límite
- ✅ Mantiene los últimos 4 mensajes sin resumir
- ✅ Funciona con modelos personalizados y locales

**Ejemplo:**
- Modelo: Gemini 2.5 Flash Lite (1M tokens de contexto)
- Límite seguro: 800K tokens
- Si excedes: Resume conversación anterior automáticamente
- Resultado: Nunca pierdes el contexto

---

## 🐳 Docker Actualizado

### Nuevo Servicio de Ollama

El `docker-compose.yml` ahora incluye:
- **Servicio `chatpdep`**: Tu aplicación Streamlit
- **Servicio `ollama`**: Servidor de modelos locales
- **Volumen `ollama_models`**: Persiste modelos descargados

**Instalación automática:**
```bash
docker-compose up --build
```

Esto instalará:
1. ChatPdeP en `http://localhost:8501`
2. Ollama en `http://localhost:11434`
3. Modelo `phi4-mini` (3.8B) por defecto

**Instalar más modelos:**
```bash
docker exec -it chatpdep_ollama ollama pull qwen3-4b
docker exec -it chatpdep_ollama ollama pull deepseek-coder-6.7b
```

---

## 💡 Casos de Uso

### Caso 1: Estudiante con presupuesto limitado
**Problema**: Gastar mucho en APIs para estudiar
**Solución**: Usa Ollama local con phi4-mini para preguntas teóricas y de código simple
**Ahorro**: 100% (gratis)

### Caso 2: Desarrollador optimizando costos
**Problema**: Usar Claude Opus para todo (caro)
**Solución**: Activa auto-clasificación. Usa Gemini para teoría, Grok/Codex para código, Opus solo para debugging complejo
**Ahorro**: 60-80% en costos

### Caso 3: Uso profesional con modelos específicos
**Problema**: Quiero usar el último GPT-4o de OpenRouter
**Solución**: Agrega el modelo personalizado con ID `openai/gpt-4o`
**Resultado**: Acceso a cualquier modelo de OpenRouter

### Caso 4: Desarrollo sin internet
**Problema**: Trabajar en zona sin conexión
**Solución**: Usa Ollama local, corre phi4-mini o qwen3 sin internet
**Resultado**: Productividad sin depender de APIs

---

## 🎓 Comparativa de Modelos

### Cloud (OpenRouter)

| Modelo | Tier | Costo Input | Costo Output | Mejor Para |
|--------|------|-------------|--------------|-----------|
| Gemini 2.5 Flash Lite | Economy | $0.10 | $0.40 | Preguntas teóricas, conceptos simples |
| GPT 5 Codex Mini | Balanced | $0.25 | $2.00 | Desarrollo de código general |
| Grok 4.1 Fast | Balanced | $0.20 | $0.50 | Código rápido, explicaciones |
| Qwen 3 Coder | Balanced | $0.22 | $0.95 | Código especializado |
| Claude Opus 4.6 | Premium | $5.00 | $25.00 | Debugging complejo, arquitectura |

### Local (Ollama)

| Modelo | Tamaño | Costo | RAM Recomendada | Mejor Para |
|--------|--------|-------|-----------------|-----------|
| phi4-mini | 3.8B | $0 | 4GB | Consultas rápidas, teoría |
| qwen3-4b | 4B | $0 | 8GB | Código balanceado |
| deepseek-coder-6.7b | 6.7B | $0 | 16GB | Código especializado |
| qwen2.5-coder-7b | 7B | $0 | 16GB | Desarrollo avanzado |

---

## 🔧 Configuración Técnica

### Variables de Entorno

Actualiza tu `.env`:

```bash
# Cloud (OpenRouter)
OPENROUTER_API_KEY=tu_api_key

# Supabase
SUPABASE_URL=tu_url
SUPABASE_ANON_KEY=tu_key

# Ollama (opcional, Docker lo configura automáticamente)
OLLAMA_BASE_URL=http://localhost:11434
```

### Requisitos de Sistema

**Para usar Ollama local:**
- **CPU**: Recomendado 4+ cores
- **RAM**: Mínimo 8GB, recomendado 16GB
- **Disco**: 10GB+ para modelos
- **GPU** (opcional): NVIDIA con CUDA para velocidad

**Sin Ollama (solo cloud):**
- Cualquier máquina que corra Docker

---

## 📊 Estadísticas de Mejora

| Métrica | Antes | Después | Mejora |
|---------|-------|---------|--------|
| Opciones de modelos | 5 cloud | 5 cloud + 4+ local + infinitos custom | +180% |
| Costo mínimo por consulta | $0.001 | $0 (local) | 100% ahorro |
| Flexibilidad de proveedor | Solo cloud | Cloud + Local | +100% |
| Optimización automática | ❌ No | ✅ Sí (auto-clasificación) | ∞ |
| Fallbacks | ❌ No | ✅ Automático a Gemini | +100% confiabilidad |
| Context window inteligente | Manual | Automático por modelo | +100% |

---

## 🛠️ Guía Rápida de Uso

### Para empezar con Local (Ollama):

1. **Levantar Docker:**
   ```bash
   docker-compose up --build
   ```

2. **Esperar instalación** (primera vez, ~2-3 min)

3. **Abrir app:** `http://localhost:8501`

4. **Seleccionar en sidebar:**
   - Proveedor: "💻 Local (Ollama)"
   - Modelo: "Phi 4 Mini (3.8B)"

5. **¡Listo!** Pregunta lo que quieras gratis

### Para usar Cloud (OpenRouter):

1. **Obtener API Key:** [OpenRouter Keys](https://openrouter.ai/keys)

2. **Configurar en sidebar:**
   - Proveedor: "☁️ Cloud (OpenRouter)"
   - Pegar API Key

3. **Activar auto-clasificación:**
   - Marcar "🎯 Auto-clasificar (optimizar costos)"

4. **¡Listo!** El sistema elegirá el mejor modelo

---

## 🐛 Solución de Problemas

### "Modelo local no responde"
**Solución:**
1. Verifica que Docker esté corriendo: `docker ps`
2. Verifica Ollama: `docker logs chatpdep_ollama`
3. Reinicia: `docker-compose restart ollama`

### "Error con modelo personalizado"
**Solución:**
1. Verifica que el ID sea correcto en OpenRouter
2. Verifica tu API Key
3. Prueba con otro modelo para confirmar

### "Memoria insuficiente para modelo local"
**Solución:**
1. Usa phi4-mini (más liviano)
2. Cierra otras aplicaciones
3. O usa modelos cloud

---

## 🙏 Créditos y Agradecimientos

Esta actualización fue posible gracias a:
- **Ollama**: Por democratizar el acceso a LLMs locales
- **OpenRouter**: Por la API unificada de modelos
- **Comunidad de ChatPdeP**: Por el feedback y sugerencias

---

## 📝 Próximas Mejoras (Roadmap)

🔮 En desarrollo:
- [ ] Comparación side-by-side de modelos
- [ ] Métricas de costo por conversación
- [ ] Soporte para más proveedores (HuggingFace, Together AI)
- [ ] Fine-tuning de modelos locales

---

## 📖 Documentación Completa

Para más detalles técnicos, consulta el [README.md](README.md) actualizado.

---

**Versión**: 2.0  
**Fecha**: Febrero 2026  
**Autor**: Tomas Cabrera Roman - UTN FRBA  

---

¡Disfruta de la nueva versión de ChatPdeP! 🎓🚀
