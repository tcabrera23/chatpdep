# 🧪 Pruebas Rápidas - ChatPdeP v2.0

Guía para probar todas las nuevas características de la V2.

---

## ✅ Checklist de Pruebas

### 1. ⚡ Groq (API Gratuita)

**Setup:**
```bash
# Obtener API Key
# 1. Ve a https://console.groq.com
# 2. Crea cuenta gratis
# 3. API Keys → Create API Key
# 4. Copia la key
```

**Configurar:**
```bash
# En .env
GROQ_API_KEY=gsk_tu_key_aqui
```

**Probar:**
- [ ] Abrir app
- [ ] Sidebar → Proveedor: "⚡ Groq (Gratis)"
- [ ] Pegar API Key
- [ ] Modelo: "Llama 3.3 70B Versatile"
- [ ] Hacer pregunta: "¿Qué es programación orientada a objetos?"
- [ ] ✅ Debe responder en ~2-3 segundos

**Verificar:**
- [ ] Respuesta coherente y detallada
- [ ] Sin errores de API
- [ ] Info de modelo muestra "Llama 3.3"

---

### 2. 🎯 Auto-clasificación

**Probar:**
- [ ] Activar checkbox: "🎯 Auto-clasificar (optimizar costos)"
- [ ] Pregunta teórica: "¿Qué es polimorfismo?"
  - Debería sugerir modelo economy (Groq/Gemini)
- [ ] Pregunta de código: "Crea una clase Persona en Wollok"
  - Debería sugerir modelo balanced (Groq Mixtral/Grok)
- [ ] Pregunta compleja con archivo adjunto
  - Debería sugerir modelo premium

**Verificar:**
- [ ] Notificación de clasificación aparece
- [ ] Modelo cambia automáticamente
- [ ] Razonamiento es correcto

---

### 3. ➕ Modelos Personalizados

**Probar (Groq):**
- [ ] Sidebar → "➕ Agregar modelo personalizado"
- [ ] Proveedor: Groq
- [ ] ID: `gemma2-9b-it`
- [ ] Nombre: "Gemma 2 9B"
- [ ] Tier: Economy
- [ ] Click "➕ Agregar Modelo"

**Verificar:**
- [ ] Mensaje de éxito
- [ ] Modelo aparece en selector
- [ ] Funciona al seleccionarlo

**Probar (OpenRouter):**
- [ ] ID: `openai/gpt-4o-mini`
- [ ] Debe agregarse correctamente

---

### 4. 🔄 Sistema de Fallbacks

**Probar fallo intencional:**
- [ ] Agregar modelo con ID inválido: "modelo-que-no-existe"
- [ ] Intentar usarlo
- [ ] Debe mostrar error
- [ ] Debe usar fallback automático (Groq o Gemini)
- [ ] Notificación de fallback aparece

**Verificar:**
- [ ] No crashea la app
- [ ] Mensaje de error claro
- [ ] Continúa funcionando con fallback

---

### 5. 💻 Ollama Local (Solo Local)

**Setup (Docker):**
```bash
docker-compose up --build
# Esperar ~3 minutos para que descargue phi4-mini
```

**Verificar instalación:**
```bash
docker logs chatpdep_ollama
# Debe mostrar: "phi4-mini instalado correctamente!"
```

**Probar:**
- [ ] Sidebar → Proveedor: "💻 Local (Ollama)"
- [ ] Modelo: "Phi 4 Mini (3.8B)"
- [ ] Pregunta simple: "¿Qué es una variable?"
- [ ] ✅ Debe responder (puede tardar 10-30 seg primera vez)

**Instalar más modelos:**
```bash
docker exec -it chatpdep_ollama ollama pull qwen3-4b
```

**Verificar:**
- [ ] Modelo se descarga correctamente
- [ ] Aparece en selector después de refrescar
- [ ] Funciona al usarlo

---

### 6. 📝 Summarización Mejorada

**Probar:**
- [ ] Hacer 10+ preguntas y respuestas
- [ ] Observar cuando se acerca al límite de contexto
- [ ] Debe aparecer: "📝 Resumiendo conversación anterior..."
- [ ] Conversación continúa sin problemas

**Verificar:**
- [ ] No pierde el contexto importante
- [ ] Mantiene últimos 4 mensajes sin resumir
- [ ] Tokens aproximados se reducen

---

### 7. 📎 Archivos Adjuntos

**Probar PDF:**
- [ ] Subir PDF con teoría o ejercicio
- [ ] Pregunta: "Resume este PDF"
- [ ] Debe extraer texto y procesar

**Probar Imagen:**
- [ ] Subir imagen con código o diagrama
- [ ] Pregunta: "¿Qué muestra esta imagen?"
- [ ] Debe analizar (requiere modelo con visión)

**Verificar:**
- [ ] Extracción funciona
- [ ] Contenido se incluye en consulta
- [ ] Indicador de adjunto aparece

---

### 8. 📚 Historial (Solo Local)

**Probar:**
- [ ] Hacer varias consultas
- [ ] Cerrar y reabrir navegador
- [ ] Historial debe mantener conversaciones
- [ ] Click en conversación antigua
- [ ] Debe cargar mensajes correctamente

**Verificar:**
- [ ] SQLite guarda correctamente
- [ ] Títulos son descriptivos
- [ ] Borrar funciona

---

### 9. 🌐 Streamlit Cloud

**Setup:**
```bash
# 1. Subir a GitHub (público)
git add .
git commit -m "Deploy v2.0"
git push origin main

# 2. Ir a share.streamlit.io
# 3. New app → Selecciona repo → Deploy
# 4. Settings → Secrets → Pegar:
GROQ_API_KEY = "tu_key"
SUPABASE_URL = "tu_url"
SUPABASE_ANON_KEY = "tu_key"
```

**Probar:**
- [ ] App se despliega sin errores
- [ ] URL funciona: `tu-app.streamlit.app`
- [ ] Groq funciona
- [ ] OpenRouter funciona (si configuraste)
- [ ] Auto-clasificación funciona
- [ ] RAG recupera teoría

**Verificar limitaciones cloud:**
- [ ] Ollama NO aparece como opción (esperado)
- [ ] Historial no persiste al refrescar (esperado)
- [ ] Funciona durante la sesión del navegador
- [ ] Mensaje de advertencia cloud aparece (si lo agregaste)

---

## 🚨 Errores Comunes y Soluciones

### "GROQ_API_KEY not configured"

**Solución:**
- Verifica que la key esté en `.env` o en sidebar
- Verifica que sea válida en console.groq.com
- Recarga la app

### "Connection to Ollama failed"

**Solución:**
```bash
# Verificar que Ollama esté corriendo
docker ps | grep ollama

# Ver logs
docker logs chatpdep_ollama

# Reiniciar
docker-compose restart ollama
```

### "Model not found"

**Solución:**
- Verifica el ID del modelo
- Para Ollama, instálalo primero: `ollama pull modelo`
- Para Groq/OpenRouter, verifica que exista en su plataforma

### "Rate limit exceeded" (Groq)

**Esperado en tier gratuito**

**Solución:**
- Espera 1 minuto
- Usa otro proveedor temporalmente
- O upgrade a Groq Pro

### App muy lenta en Streamlit Cloud

**Normal en tier gratuito**

**Solución:**
- Usa modelos más rápidos (Groq es el más rápido)
- Reduce ventana de contexto
- O hostea en tu propio servidor

---

## 📊 Métricas de Éxito

### Groq
- ✅ Respuesta en < 5 segundos
- ✅ Sin errores de API
- ✅ Calidad similar a GPT-3.5

### Auto-clasificación
- ✅ 80%+ de precisión en tipo
- ✅ Selecciona tier correcto
- ✅ Notificaciones claras

### Ollama Local
- ✅ Primera respuesta en < 30 seg
- ✅ Siguientes en < 10 seg
- ✅ Calidad aceptable para uso local

### Streamlit Cloud
- ✅ Deploy exitoso en < 5 min
- ✅ Link público accesible
- ✅ Funciona para demos

---

## 🎯 Prueba Completa End-to-End

### Escenario: Estudiante usando la app por primera vez

1. **Setup inicial (5 min)**
   - [ ] Obtiene API key de Groq (2 min)
   - [ ] Clona repo (1 min)
   - [ ] Configura .env (1 min)
   - [ ] Levanta Docker (1 min)

2. **Primera consulta (2 min)**
   - [ ] Abre app en navegador
   - [ ] Selecciona agente Wollok
   - [ ] Activa auto-clasificación
   - [ ] Pregunta: "¿Qué es un objeto en Wollok?"
   - [ ] Recibe respuesta de Groq

3. **Consulta de código (5 min)**
   - [ ] Pregunta: "Crea una clase Guerrero con ataque"
   - [ ] Auto-clasificación selecciona modelo adecuado
   - [ ] Recibe código completo en Wollok
   - [ ] Código es correcto y funcional

4. **Adjuntar archivo (3 min)**
   - [ ] Sube PDF con ejercicio
   - [ ] Pregunta: "Resuelve el ejercicio 3"
   - [ ] App extrae contenido
   - [ ] Genera solución basada en PDF

5. **Cambiar a Ollama local (2 min)**
   - [ ] Cambia a proveedor Ollama
   - [ ] Selecciona phi4-mini
   - [ ] Hace pregunta simple
   - [ ] Funciona sin costo

6. **Publicar en cloud (10 min)**
   - [ ] Sube a GitHub
   - [ ] Despliega en Streamlit Cloud
   - [ ] Configura secrets
   - [ ] Comparte link con amigo
   - [ ] Amigo puede usarlo

**Tiempo total:** ~30 minutos
**Resultado:** App funcional, publicada y gratis

---

## ✅ Resultado Esperado

Si todas las pruebas pasan:

✅ **ChatPdeP v2.0 está 100% funcional**
✅ **Listo para uso personal**
✅ **Listo para publicar en cloud**
✅ **Listo para compartir en portafolio**

---

## 📝 Reporte de Bugs

Si encuentras problemas:

1. **Revisa logs:**
   ```bash
   docker logs chatpdep_app
   docker logs chatpdep_ollama
   ```

2. **Verifica configuración:**
   - API keys correctas
   - Supabase conectado
   - Modelos instalados

3. **Crea issue en GitHub:**
   - Describe el problema
   - Incluye logs relevantes
   - Menciona tu sistema operativo

---

**¡Disfruta probando ChatPdeP v2.0!** 🚀
