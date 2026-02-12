# Posts para LinkedIn: Proyecto de IA con RAG y agentes (UTN)

Gracias por leer. Aquí tienes 6 posts breves pensados para LinkedIn para mostrar el proyecto, con ideas visuales (capturas, GIFs, videos) y llamados a la acción.

---

## Post 1 — Visión general y gancho
¿Qué voy a enseñar hoy? Migré un flujo de trabajo de N8N a Python para que cualquiera pueda ejecutar agentes IA de forma local con una simple API key. En el proyecto hay 3 agentes: Wollok, Haskell y Prolog, trabajando con RAG (búsqueda semántica en Supabase) y embeddings gestionados desde OpenRouter. Todo corre sin VPS, con una instalación sencilla.

Media sugerida:
- captura del repositorio y estructura
- diagrama corto de arquitectura
- GIF corto del flujo de consultas RAG

Llamado a la acción: clone el repo, configure el `.env` y prueben localmente.

---

## Post 2 — Qué es RAG y cómo funciona aquí
RAG = Retrieval Augmented Generation. Este proyecto:
- consulta una base de conocimiento mediante embeddings (Supabase + pgvector)
- recupera fragmentos relevantes y los alimenta al LLM
- genera respuestas precisas para Wollok/Haskell/Prolog

Media sugerida:
- captura de código de consulta y resultados de búsqueda
- video corto explicando el flujo (con voz o subtítulos)

Por qué importa: te da control total sobre qué información consulta tu agente.

---

## Post 3 — Optimización del contexto y costos
El tamaño de la ventana del modelo impacta en costos y rendimiento. Proponemos:
- resumen periódico de la conversación para conservar contexto clave
- limitar la memoria histórica sin perder calidad
- usar embeddings y RAG para recuperar solo lo necesario

Media sugerida:
- GIF mostrando el flujo de resumen automático
- captura de consola con conteo de tokens

Llamado a la acción: prueba con un conjunto de preguntas críticas y observa la diferencia de costos.

---

## Post 4 — De N8N a Python: simplificación de despliegue
Antes: N8N, VPS y múltiples claves. Ahora: Python puro, una API key y ejecución local. Menos complejidad, más reproducibilidad.
Ventajas:
- sin infra extra: solo API keys
- reproducibilidad entre máquinas
- comunidad de estudiantes puede adaptar el setup

Media sugerida:
- captura de commits/mensajes de migración
- diagrama “antes vs. después”

CTA: invita a la gente a intentar la migración en sus cursos.

---

## Post 5 — Llamado a UTN y replicación en otras materias
A la comunidad UTN: este proyecto es una base para replicar en física, química, informática, etc. El objetivo es mostrar cómo un agente RAG puede consultar documentación, guías y cursos completos para responder preguntas complejas.
Media sugerida:
- fotos de aula o campus
- video corto de una demo de QA entre el agente y la documentación

Contribuye: comparte adaptaciones para otras asignaturas.

---

## Post 6 — Diferencias clave: Rag vs cargar documentos en otras IA
En este proyecto:
- Rag controla la fuente: toda la documentación está integrada para consultas del agente
- ventana de contexto: límites claros y uso eficiente de tokens
- personalización: documentación lista para que los agentes consulten directamente
¿Qué te resulta más útil para tus proyectos?

Media sugerida:
- diagrama comparativo
- captura de resultados de una consulta a la base de conocimiento

CTA final: comparte tu implementación o pregunta dudas en los comentarios.

---

Notas:
- Captura, GIF y video deben estar listos para subir como media en LinkedIn.
- Mantén los posts concisos para lectura en ~1 minuto.
- Evita exponer claves/API keys; usa referencias generales.


en las slides pongo fotos

la primer foto es la interfaz de la app
la segunda es un gif tipo video de interaccion con la app
la tercer foto es la del repositorio
en los comentarios: quien quiera darle un vistazo, visita chatpdep.streamlit.com pone su apikey y ahi lo testea pero sin guardarse las conversaciones