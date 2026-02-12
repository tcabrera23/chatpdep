# 🚀 Quick Start - ChatPdeP v2.0

Guía rápida para empezar a usar ChatPdeP en 5 minutos.

---

## ⚡ Instalación Rápida (Docker)

### Requisitos
- Docker Desktop instalado

### 3 Comandos para Empezar

```bash
# 1. Clonar y entrar
git clone <tu-repo> && cd agents_pdep

# 2. Configurar (crear .env con tus keys)
cp .env.example .env
# Editar .env con tus credenciales

# 3. Levantar
docker-compose up --build
```

**¡Listo!** Abre `http://localhost:8501`

---

## 🎯 Primeros Pasos

### 1. Elegir Modo

En el **sidebar**, selecciona:

**Opción A: Local (Gratis)**
- Proveedor: `💻 Local (Ollama)`
- Modelo: `Phi 4 Mini (3.8B)`
- ✅ $0 en costos

**Opción B: Cloud (Potente)**
- Proveedor: `☁️ Cloud (OpenRouter)`
- Configura tu API Key
- Activa: `🎯 Auto-clasificar`
- ✅ Optimiza costos automáticamente

### 2. Elegir Tutor

Selecciona según lo que necesites:
- **Wollok**: Programación Orientada a Objetos
- **Haskell**: Programación Funcional
- **Prolog**: Programación Lógica

### 3. Hacer tu Primera Pregunta

Ejemplos:

**Pregunta Teórica:**
```
¿Qué es polimorfismo en Wollok?
```
→ Usa Gemini Flash Lite (económico)

**Desarrollo de Código:**
```
Crea una clase Personaje en Wollok con nombre y energía
```
→ Usa Grok o Codex (balanceado)

**Debugging Complejo:**
```
Tengo este error [pega código], ¿cómo lo soluciono?
```
→ Usa Claude Opus (premium)

---

## 💡 Características Principales

### 🎯 Auto-Clasificación (Optimizar Costos)

1. Activa en sidebar: `🎯 Auto-clasificar`
2. Haz tu pregunta
3. El sistema elige el mejor modelo
4. **Ahorro:** 60-80% en costos

### 📎 Adjuntar Archivos

Puedes adjuntar:
- **PDFs**: Enunciados, teoría
- **Imágenes**: Diagramas, código

Ejemplo:
1. Haz clic en "📎 Adjuntar archivo"
2. Sube tu PDF con el ejercicio
3. Pregunta: "Resuelve el ejercicio del PDF"

### 📚 Historial

En el **sidebar**, sección "Historial":
- Ver conversaciones previas
- Cargar conversación
- Eliminar conversación

---

## 🔧 Configuración Avanzada

### Agregar Modelo Personalizado

1. Ve a [OpenRouter Models](https://openrouter.ai/models)
2. Busca el modelo que quieres
3. Copia su ID (ej: `openai/gpt-4o`)
4. En sidebar → "➕ Agregar modelo personalizado"
5. Pega el ID
6. Configura tier y nombre
7. ¡Listo!

### Instalar Más Modelos Locales

```bash
# Modelos recomendados
docker exec -it chatpdep_ollama ollama pull qwen3-4b
docker exec -it chatpdep_ollama ollama pull deepseek-coder-6.7b

# Ver instalados
docker exec -it chatpdep_ollama ollama list
```

### Ajustar Ventana de Contexto

En sidebar:
- Slider: "Ventana de contexto"
- Rango: 4-20 mensajes
- Recomendado: 8 mensajes

---

## 🆘 Solución Rápida de Problemas

### Ollama no responde
```bash
docker logs chatpdep_ollama
docker-compose restart ollama
```

### API Key inválida
1. Verifica en `.env`
2. Verifica créditos en OpenRouter
3. Reconfigura en sidebar

### Puerto ocupado
```bash
# Cambiar puerto en docker-compose.yml
ports:
  - "8502:8501"
```

---

## 📖 Documentación Completa

- **NEW_VERSION.md**: Todas las nuevas características
- **INSTALLATION_GUIDE.md**: Guía detallada de instalación
- **README.md**: Documentación técnica completa
- **CHANGELOG.md**: Historial de cambios

---

## 💬 Ejemplos de Uso

### Ejemplo 1: Pregunta Teórica Simple
```
Usuario: ¿Qué es un objeto en Wollok?
Sistema: 🎯 Clasificada como teórica simple
Modelo: Gemini 2.5 Flash Lite
Respuesta: [Explicación clara y concisa]
```

### Ejemplo 2: Ejercicio de Código
```
Usuario: Implementa la clase Guerrero con ataque y defensa
Sistema: 🎯 Clasificada como código media
Modelo: Grok 4.1 Fast
Respuesta: [Código completo en Wollok con explicación]
```

### Ejemplo 3: Debugging Complejo
```
Usuario: [Adjunta imagen con error] ¿Por qué falla este código?
Sistema: 🎯 Clasificada como debugging complejo
Modelo: Claude Opus 4.6
Respuesta: [Análisis detallado del error y solución]
```

---

## 🎓 Tips y Trucos

### Optimizar Costos
- ✅ Activa auto-clasificación
- ✅ Usa Ollama local para preguntas simples
- ✅ Reserva Claude Opus para problemas complejos

### Mejores Respuestas
- ✅ Sé específico en tus preguntas
- ✅ Adjunta archivos cuando sea relevante
- ✅ Usa el tutor correcto (Wollok/Haskell/Prolog)
- ✅ Proporciona contexto si es necesario

### Gestión de Conversaciones
- ✅ Crea nueva conversación para temas diferentes
- ✅ Revisa el historial antes de preguntar lo mismo
- ✅ Borra conversaciones antiguas para orden

---

## ⚙️ Configuración Recomendada

### Para Estudiantes
```
Proveedor: Local (Ollama)
Modelo: phi4-mini
Auto-clasificar: Desactivado
Ventana: 8 mensajes
```
**Por qué:** Gratis, suficiente para aprender

### Para Desarrollo Serio
```
Proveedor: Cloud (OpenRouter)
Auto-clasificar: Activado
Ventana: 12 mensajes
API Key: Configurada
```
**Por qué:** Mejor calidad, optimiza costos

### Para Exámenes/Parciales
```
Proveedor: Cloud
Modelo manual: Claude Opus
Auto-clasificar: Desactivado
Ventana: 16 mensajes
```
**Por qué:** Máxima calidad, sin riesgo de fallos

---

**¡Listo para empezar!** 🎉

Si tienes problemas, consulta la [Guía de Instalación](INSTALLATION_GUIDE.md).
