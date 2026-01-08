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

# LangChain imports
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool

# Cargar variables de entorno
load_dotenv()

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
    st.session_state.current_model = "google/gemini-2.5-flash-lite"

# Flag para saber si es una conversación nueva
if "is_new_conversation" not in st.session_state:
    st.session_state.is_new_conversation = True

# =============================================================================
# SIDEBAR - CONFIGURACIÓN
# =============================================================================

with st.sidebar:
    st.markdown("## ⚙️ Configuración")
    
    # API Key de OpenRouter
    openrouter_key = st.text_input(
        "OpenRouter API Key",
        value=os.getenv("OPENROUTER_API_KEY", ""),
        type="password",
        help="Tu API key de OpenRouter para usar los modelos"
    )
    
    if openrouter_key:
        os.environ["OPENROUTER_API_KEY"] = openrouter_key
    
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
    
    # Información de modelos con costos (por 1M tokens)
    models_info = {
        "google/gemini-2.5-flash-lite": {
            "name": "Gemini 2.5 Flash Lite",
            "input": "$0.10",
            "output": "$0.40",
            "description": "Rápido y económico"
        },
        "openai/gpt-4.1-nano": {
            "name": "GPT-4.1 Nano",
            "input": "$0.15",
            "output": "$0.40",
            "description": "Equilibrado"
        },
        "x-ai/grok-4.1-fast": {
            "name": "Grok 4.1 Fast",
            "input": "$0.2",
            "output": "$0.5",
            "description": "Potente y rápido"
        },
        "qwen/qwen3-coder": {
            "name": "Qwen 3 Coder",
            "input": "$0.22",
            "output": "$0.95",
            "description": "Especializado en código"
        }
    }
    
    available_models = list(models_info.keys())
    
    selected_model = st.selectbox(
        "Selecciona el modelo",
        options=available_models,
        index=available_models.index(st.session_state.current_model) if st.session_state.current_model in available_models else 0,
        help="Modelo de lenguaje a utilizar",
        format_func=lambda x: models_info[x]["name"]
    )
    
    # Mostrar costos del modelo seleccionado
    model_info = models_info[selected_model]
    st.caption(f"**💰 Costo por 1M tokens:** Input: {model_info['input']} | Output: {model_info['output']}")
    st.caption(f"_{model_info['description']}_")
    
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
    st.info(f"**Modelo:** {selected_model.split('/')[-1]}")
with col3:
    st.info(f"**Contexto:** {context_window} msgs")

# Actualizar configuración si cambió
if selected_agent != st.session_state.current_agent or selected_model != st.session_state.current_model:
    st.session_state.current_agent = selected_agent
    st.session_state.current_model = selected_model
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
                
                # Crear LLM
                llm = ChatOpenAI(
                    model=selected_model,
                    base_url="https://openrouter.ai/api/v1",
                    api_key=os.getenv("OPENROUTER_API_KEY"),
                    temperature=0.5
                )
                
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
                        model_name=selected_model
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
