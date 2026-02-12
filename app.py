"""
Interfaz Streamlit para ChatPdeP - Tutor de Paradigmas de Programación.
Aplicación principal con sidebar, chat y manejo de archivos adjuntos.
"""

import streamlit as st
import os
import uuid
import time
from datetime import datetime
from dotenv import load_dotenv

# Importaciones locales
from config.agents import AGENTS, get_agent_config
from tools.rag_tool import get_rag_instance, recuperar_teoria
from tools.file_extraction import get_file_extractor
from utils.database import ConversationDatabase
from utils.query_classifier import get_classifier
from utils.model_manager import get_model_manager

# LangChain imports
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool

# Cargar variables de entorno
load_dotenv()

# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def count_tokens_approximate(messages: list) -> int:
    """
    Estima el número de tokens en una lista de mensajes.
    Aproximación: 1 token ≈ 4 caracteres en español.
    """
    total_chars = sum(len(msg.content) if hasattr(msg, 'content') else len(str(msg)) for msg in messages)
    return total_chars // 4


def summarize_conversation(llm: ChatOpenAI, messages: list, keep_last: int = 4) -> list:
    """
    Resume conversaciones largas manteniendo los mensajes más recientes.
    
    Args:
        llm: Modelo de lenguaje para generar el resumen
        messages: Lista de mensajes a resumir
        keep_last: Número de mensajes recientes a mantener sin resumir
    
    Returns:
        Lista de mensajes con historial resumido
    """
    if len(messages) <= keep_last + 2:  # Si hay pocos mensajes, no resumir
        return messages
    
    # Separar mensajes a resumir y mensajes recientes
    messages_to_summarize = messages[1:-keep_last]  # Excluir system prompt y últimos mensajes
    recent_messages = messages[-keep_last:]
    system_prompt = messages[0] if isinstance(messages[0], SystemMessage) else None
    
    if not messages_to_summarize:
        return messages
    
    # Crear prompt de resumen
    conversation_text = "\n".join([
        f"{msg.__class__.__name__}: {msg.content}" 
        for msg in messages_to_summarize
    ])
    
    summary_prompt = f"""Resume la siguiente conversación de manera concisa, preservando:
- Conceptos clave discutidos
- Código o ejemplos importantes mencionados
- Conclusiones o decisiones tomadas

Conversación:
{conversation_text}

Resumen:"""
    
    # Generar resumen
    summary_response = llm.invoke([HumanMessage(content=summary_prompt)])
    summary_message = SystemMessage(content=f"Resumen de conversación previa: {summary_response.content}")
    
    # Construir nueva lista de mensajes
    result = []
    if system_prompt:
        result.append(system_prompt)
    result.append(summary_message)
    result.extend(recent_messages)
    
    return result

# =============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# =============================================================================

st.set_page_config(
    page_title="ChatPdeP - Tutor de Paradigmas",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# ESTILOS PERSONALIZADOS
# =============================================================================

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .sidebar .element-container {
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# INICIALIZACIÓN DE ESTADO
# =============================================================================

# Inicializar base de datos
if "db" not in st.session_state:
    st.session_state.db = ConversationDatabase()

# Inicializar extractor de archivos
if "file_extractor" not in st.session_state:
    st.session_state.file_extractor = get_file_extractor()

# Inicializar gestor de modelos
if "model_manager" not in st.session_state:
    st.session_state.model_manager = get_model_manager()

# Inicializar clasificador de queries
if "query_classifier" not in st.session_state:
    st.session_state.query_classifier = get_classifier()

# Conversación actual
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = f"conv_{uuid.uuid4().hex[:8]}_{int(time.time())}"

# Mensajes de la conversación actual
if "messages" not in st.session_state:
    st.session_state.messages = []

# Configuración del agente seleccionado
if "current_agent" not in st.session_state:
    st.session_state.current_agent = "Wollok"

if "current_model" not in st.session_state:
    st.session_state.current_model = "groq/compound"

# Proveedor de modelo (groq/openrouter/ollama)
if "model_provider" not in st.session_state:
    st.session_state.model_provider = "groq"  # Groq por defecto (gratis)

# Auto-clasificación habilitada
if "auto_classify" not in st.session_state:
    st.session_state.auto_classify = True

# Modelos personalizados
if "custom_models" not in st.session_state:
    st.session_state.custom_models = {}

# Flag para saber si es una conversación nueva
if "is_new_conversation" not in st.session_state:
    st.session_state.is_new_conversation = True

# =============================================================================
# SIDEBAR - CONFIGURACIÓN
# =============================================================================

with st.sidebar:
    st.markdown("## ⚙️ Configuración")
    
    # Selector de proveedor
    st.markdown("### 🌐 Proveedor de Modelo")
    
    provider_options = ["groq", "openrouter", "ollama"]
    provider_labels = {
        "groq": "⚡ Groq (Gratis)",
        "openrouter": "☁️ OpenRouter (Pago)",
        "ollama": "💻 Local (Ollama)"
    }
    
    # Determinar índice actual
    # Si el proveedor guardado en sesión no es 'groq', lo seteamos a 0 para que 'groq' sea el default.
    # Esto asegura que Groq sea el proveedor por defecto al iniciar o refrescar.
    current_index = 0
    if st.session_state.model_provider != "groq":
        st.session_state.model_provider = "groq" # Forzar Groq como default si no fue seteado o es inválido
        current_index = 0 # Asegurar que Groq sea el seleccionado por defecto en el radio button
    
    provider = st.radio(
        "Selecciona el proveedor",
        options=provider_options,
        format_func=lambda x: provider_labels[x],
        index=current_index,
        help="Groq: API gratuita ideal para empezar | OpenRouter: Acceso a todos los modelos | Ollama: Modelos locales sin costo"
    )
    st.session_state.model_provider = provider
    
    # Configuración según proveedor
    if provider == "groq":
        # API Key de Groq (gratis)
        groq_key = st.text_input(
            "Groq API Key (Gratis)",
            value="", # No mostrar el valor por defecto
            type="password",
            help="Obtén tu API key gratis en https://console.groq.com/keys"
        )
        
        if groq_key:
            os.environ["GROQ_API_KEY"] = groq_key
        
        st.info("💡 **¡Groq es gratis!** Obtén tu API key en [console.groq.com](https://console.groq.com)")
    
    elif provider == "openrouter":
        # API Key de OpenRouter (pago)
        openrouter_key = st.text_input(
            "OpenRouter API Key",
            value="", # No mostrar el valor por defecto
            type="password",
            help="Tu API key de OpenRouter para usar los modelos"
        )
        
        if openrouter_key:
            os.environ["OPENROUTER_API_KEY"] = openrouter_key
    
    else:  # ollama
        # URL de Ollama (local)
        ollama_url = st.text_input(
            "Ollama Base URL",
            value=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            help="URL del servidor Ollama (ej: http://localhost:11434)"
        )
        os.environ["OLLAMA_BASE_URL"] = ollama_url
        
        # Sugerencias de modelos para instalar
        with st.expander("📦 Modelos sugeridos para Ollama"):
            st.markdown("""
            Instala estos modelos con Docker o manualmente:
            
            **Por defecto en Docker:**
            ```bash
            phi4-mini (3.8B) - Rápido y ligero
            ```
            
            **Recomendados (vía comando):**
            ```bash
            ollama pull qwen3-4b
            ollama pull deepseek-coder-6.7b
            ollama pull qwen2.5-coder-7b
            ```
            """)
    
    st.markdown("---")
    
    # Selección de Agente (Tutor)
    st.markdown("### 🎓 Tutor")
    selected_agent = st.selectbox(
        "Selecciona el paradigma",
        options=list(AGENTS.keys()),
        index=list(AGENTS.keys()).index(st.session_state.current_agent),
        help="Elige el lenguaje de programación sobre el que necesitas ayuda"
    )
    
    # Selección de Modelo
    st.markdown("### 🤖 Modelo LLM")
    
    # Auto-clasificación
    auto_classify = st.checkbox(
        "🎯 Auto-clasificar (optimizar costos)",
        value=st.session_state.auto_classify,
        help="Clasifica automáticamente la consulta y selecciona el modelo más apropiado según dificultad"
    )
    st.session_state.auto_classify = auto_classify
    
    # Obtener modelos según proveedor
    model_manager = st.session_state.model_manager
    available_models = model_manager.get_models_by_provider(provider)
    
    # Crear opciones para el selector
    model_options = {model.id: model for model in available_models}
    
    # Si no hay modelos disponibles
    if not model_options:
        st.warning(f"⚠️ No hay modelos disponibles para {provider}")
        st.stop()
    
    # Selector de modelo
    selected_model_id = st.selectbox(
        "Modelo manual (si auto-clasificar desactivado)",
        options=list(model_options.keys()),
        index=list(model_options.keys()).index(st.session_state.current_model) if st.session_state.current_model in model_options else 0,
        help="Modelo de lenguaje a utilizar",
        format_func=lambda x: model_options[x].name,
        disabled=auto_classify
    )
    
    # Mostrar info del modelo seleccionado
    selected_model_config = model_options[selected_model_id]
    st.caption(f"**💰 Costo:** Input: {selected_model_config.input_cost} | Output: {selected_model_config.output_cost}")
    st.caption(f"_{selected_model_config.description}_")
    st.caption(f"**🔧 Tier:** {selected_model_config.tier.upper()}")
    
    # Sección para agregar modelos personalizados
    with st.expander("➕ Agregar modelo personalizado"):
        st.markdown("Agrega un modelo desde OpenRouter o Ollama:")
        
        custom_provider = st.radio(
            "Proveedor del modelo personalizado",
            options=["groq", "openrouter", "ollama"],
            format_func=lambda x: "Groq" if x == "groq" else ("OpenRouter" if x == "openrouter" else "Ollama"),
            key="custom_provider"
        )
        
        # Placeholder según proveedor
        placeholder_map = {
            "groq": "llama-3.3-70b-versatile",
            "openrouter": "openai/gpt-4o",
            "ollama": "llama3"
        }
        
        custom_model_id = st.text_input(
            "ID del modelo",
            placeholder=placeholder_map.get(custom_provider, "model-id"),
            help="Copia el ID desde la documentación del proveedor",
            key="custom_model_id"
        )
        
        custom_model_name = st.text_input(
            "Nombre descriptivo (opcional)",
            placeholder="GPT-4o",
            key="custom_model_name"
        )
        
        custom_tier = st.selectbox(
            "Tier",
            options=["economy", "balanced", "premium"],
            index=1,
            key="custom_tier"
        )
        
        if st.button("➕ Agregar Modelo", key="add_custom_model"):
            if custom_model_id:
                try:
                    model_manager.add_custom_model(
                        model_id=custom_model_id,
                        provider=custom_provider,
                        name=custom_model_name if custom_model_name else None,
                        tier=custom_tier
                    )
                    st.success(f"✅ Modelo {custom_model_id} agregado exitosamente!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error al agregar modelo: {str(e)}")
            else:
                st.warning("⚠️ Por favor ingresa el ID del modelo")
    
    # Ventana de contexto
    context_window = st.slider(
        "Ventana de contexto (mensajes)",
        min_value=4,
        max_value=20,
        value=8,
        step=2,
        help="Número de mensajes previos a mantener en memoria"
    )
    
    st.markdown("---")
    
    # Botón para nueva conversación
    if st.button("➕ Nueva Conversación", use_container_width=True):
        st.session_state.conversation_id = f"conv_{uuid.uuid4().hex[:8]}_{int(time.time())}"
        st.session_state.messages = []
        st.session_state.is_new_conversation = True
        st.rerun()
    
    # Historial de conversaciones
    st.markdown("### 📚 Historial")
    
    conversations = st.session_state.db.get_all_conversations()
    
    if conversations:
        for conv in conversations[:10]:  # Mostrar últimas 10
            col1, col2 = st.columns([4, 1])
            
            # Verificar si es la conversación actual
            is_current = conv['conversation_id'] == st.session_state.conversation_id
            
            with col1:
                # Botón para cargar conversación
                button_label = f"{'✅' if is_current else '💬'} {conv['title'][:30]}..."
                if st.button(
                    button_label,
                    key=f"load_{conv['conversation_id']}",
                    use_container_width=True,
                    type="primary" if is_current else "secondary"
                ):
                    # Cargar mensajes de la conversación
                    loaded_messages = st.session_state.db.get_conversation_messages(conv['conversation_id'])
                    
                    # Actualizar estado de sesión
                    st.session_state.conversation_id = conv['conversation_id']
                    st.session_state.messages = loaded_messages
                    st.session_state.current_agent = conv['agent_name']
                    st.session_state.current_model = conv['model_name']
                    st.session_state.is_new_conversation = False
                    
                    # Debug: Verificar que se cargaron mensajes
                    print(f"Cargando conversación {conv['conversation_id']}")
                    print(f"Mensajes cargados: {len(loaded_messages)}")
                    
                    st.rerun()
            
            with col2:
                # Botón para eliminar
                if st.button("🗑️", key=f"del_{conv['conversation_id']}"):
                    st.session_state.db.delete_conversation(conv['conversation_id'])
                    st.rerun()
    else:
        st.info("No hay conversaciones previas")

# =============================================================================
# ÁREA PRINCIPAL - CHAT
# =============================================================================

st.markdown('<div class="main-header">🎓 ChatPdeP</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Tu tutor de Paradigmas de Programación - UTN FRBA</div>', unsafe_allow_html=True)

# Mostrar configuración actual
col1, col2, col3 = st.columns(3)
with col1:
    st.info(f"**Tutor:** {selected_agent}")
with col2:
    if st.session_state.auto_classify:
        st.info(f"**Modelo:** 🎯 Auto (optimizando)")
    else:
        st.info(f"**Modelo:** {selected_model_id.split('/')[-1]}")
with col3:
    st.info(f"**Contexto:** {context_window} msgs")

# Actualizar configuración si cambió
if selected_agent != st.session_state.current_agent or selected_model_id != st.session_state.current_model:
    st.session_state.current_agent = selected_agent
    st.session_state.current_model = selected_model_id
    # Si hay mensajes, crear nueva conversación
    if st.session_state.messages:
        st.session_state.conversation_id = f"conv_{uuid.uuid4().hex[:8]}_{int(time.time())}"
        st.session_state.messages = []
        st.session_state.is_new_conversation = True

st.markdown("---")

# =============================================================================
# MOSTRAR MENSAJES DEL CHAT
# =============================================================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Mostrar indicador si hay archivo adjunto
        if message.get("attachment_type"):
            st.caption(f"📎 Archivo adjunto: {message['attachment_type']}")

# =============================================================================
# INPUT DEL USUARIO
# =============================================================================

# Columna para archivo adjunto
uploaded_file = st.file_uploader(
    "📎 Adjuntar archivo (opcional)",
    type=['pdf', 'png', 'jpg', 'jpeg'],
    help="Puedes adjuntar un PDF o imagen con tu pregunta"
)

# Input de chat
if prompt := st.chat_input("Escribe tu pregunta sobre " + selected_agent + "..."):
    
    # Verificar API Key
    if not os.getenv("OPENROUTER_API_KEY"):
        st.error("⚠️ Por favor, configura tu OpenRouter API Key en el sidebar")
        st.stop()
    
    # Procesar archivo adjunto si existe
    extracted_content = None
    attachment_type = None
    
    if uploaded_file is not None:
        with st.spinner("📄 Procesando archivo adjunto..."):
            extracted_content = st.session_state.file_extractor.extract_from_file(uploaded_file)
            attachment_type = "pdf" if uploaded_file.name.endswith('.pdf') else "image"
    
    # Construir mensaje completo
    full_message = prompt
    if extracted_content:
        full_message += f"\n\n--- Contenido del archivo adjunto ---\n{extracted_content}"
    
    # Añadir mensaje del usuario al chat
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "attachment_type": attachment_type
    })
    
    # Mostrar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(prompt)
        if attachment_type:
            st.caption(f"📎 Archivo adjunto: {attachment_type}")
    
    # Generar respuesta del agente
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            with st.spinner("🤔 Pensando..."):
                # Obtener configuración del agente
                agent_config = get_agent_config(selected_agent)
                
                # Clasificar consulta si auto-clasificación está habilitada
                final_model_id = selected_model_id
                classification_info = None
                
                if st.session_state.auto_classify:
                    with st.spinner("🎯 Clasificando consulta..."):
                        classifier = st.session_state.query_classifier
                        classification = classifier.classify(
                            prompt,
                            context={"has_attachment": attachment_type is not None}
                        )
                        classification_info = classification
                        
                        # Sugerir modelo según tier
                        suggested_model = model_manager.suggest_model_by_tier(
                            tier=classification.suggested_model_tier,
                            provider=provider
                        )
                        
                        final_model_id = suggested_model.id
                        
                        # Mostrar clasificación
                        st.info(f"🎯 **Clasificación:** {classification.reasoning}")
                        st.info(f"🤖 **Modelo seleccionado:** {suggested_model.name}")
                
                # Crear herramienta personalizada para este agente
                @tool
                def recuperar_teoria_agent(query: str) -> str:
                    """
                    Recupera teoría relevante sobre el lenguaje de programación.
                    Usa esta herramienta para buscar conceptos, sintaxis, ejemplos y mejores prácticas.
                    """
                    rag = get_rag_instance()
                    results = rag.search_theory(
                        query=query,
                        table_name=agent_config["table"],
                        query_name=agent_config["query_name"],
                        match_count=5
                    )
                    return rag.format_results(results)
                
                # Crear LLM con fallback
                llm, is_fallback, fallback_reason = model_manager.create_llm_with_fallback(
                    model_id=final_model_id,
                    temperature=0.5
                )
                
                # Notificar si se usó fallback
                if is_fallback:
                    fallback_config = model_manager.get_fallback_model()
                    
                    if provider == "ollama":
                        st.error(f"⚠️ **Error en modelo local:** {fallback_reason}")
                        st.warning(f"🔄 Por favor selecciona un modelo cloud desde el sidebar o verifica que Ollama esté corriendo.")
                        st.info(f"💡 Usando fallback: {fallback_config.name}")
                    else:
                        st.warning(f"⚠️ Modelo seleccionado falló. Usando fallback: {fallback_config.name}")
                        st.caption(f"Razón: {fallback_reason}")
                
                # Preparar mensajes con system prompt
                messages = [SystemMessage(content=agent_config["system_prompt"])]
                
                # Agregar historial reciente
                recent_messages = st.session_state.messages[-context_window:] if len(st.session_state.messages) > context_window else st.session_state.messages[:-1]
                
                for msg in recent_messages:
                    if msg["role"] == "user":
                        messages.append(HumanMessage(content=msg["content"]))
                    else:
                        messages.append(AIMessage(content=msg["content"]))
                
                # Primero, buscar teoría relevante automáticamente
                with st.spinner("🔍 Buscando teoría relevante..."):
                    theory_context = recuperar_teoria_agent.invoke({"query": full_message})
                
                # Construir mensaje enriquecido con contexto
                enriched_message = f"""Usuario: {full_message}

--- Contexto de la base de conocimientos ---
{theory_context}

Usa la información anterior para responder de manera precisa y fundamentada."""
                
                messages.append(HumanMessage(content=enriched_message))
                
                # ✅ MIDDLEWARE DE SUMMARIZATION
                # Verificar si necesitamos resumir la conversación
                estimated_tokens = count_tokens_approximate(messages)
                
                # Obtener límite de contexto del modelo actual
                current_model_config = model_manager.get_model(final_model_id)
                if current_model_config:
                    # Usar 80% del contexto para seguridad
                    safe_limit = int(current_model_config.context_window * 0.8)
                else:
                    # Fallback conservador
                    safe_limit = 25_000
                
                # Si excedemos el límite, resumir conversación
                if estimated_tokens > safe_limit:
                    with st.spinner("📝 Resumiendo conversación anterior..."):
                        messages = summarize_conversation(llm, messages, keep_last=4)
                        st.info(f"💡 Conversación resumida ({estimated_tokens} → {count_tokens_approximate(messages)} tokens aprox.)")
                
                # Invocar LLM con contexto
                response = llm.invoke(messages)
                
                # Obtener respuesta
                assistant_message = response.content
                
                # Mostrar respuesta
                message_placeholder.markdown(assistant_message)
                
                # Añadir respuesta al historial
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_message
                })
                
                # Guardar en base de datos
                # Si es conversación nueva, crearla primero
                if st.session_state.is_new_conversation:
                    # Generar título basado en primera pregunta
                    title = prompt[:50] if len(prompt) <= 50 else prompt[:47] + "..."
                    
                    st.session_state.db.create_conversation(
                        conversation_id=st.session_state.conversation_id,
                        title=title,
                        agent_name=selected_agent,
                        model_name=final_model_id
                    )
                    st.session_state.is_new_conversation = False
                
                # Guardar mensajes
                st.session_state.db.add_message(
                    conversation_id=st.session_state.conversation_id,
                    role="user",
                    content=full_message,
                    has_attachment=attachment_type is not None,
                    attachment_type=attachment_type
                )
                
                st.session_state.db.add_message(
                    conversation_id=st.session_state.conversation_id,
                    role="assistant",
                    content=assistant_message
                )
        
        except Exception as e:
            error_message = f"❌ Error al generar respuesta: {str(e)}"
            message_placeholder.error(error_message)
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_message
            })

# =============================================================================
