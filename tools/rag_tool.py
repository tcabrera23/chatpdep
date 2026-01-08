"""
Tool para recuperar teoría desde Supabase usando RAG (Retrieval Augmented Generation).
Esta herramienta implementa la búsqueda semántica en las bases de datos vectoriales.
"""

import os
from typing import List, Dict, Any
from supabase import create_client, Client
from langchain_openai import OpenAIEmbeddings
from langchain_core.tools import tool


class SupabaseRAG:
    """
    Clase para manejar la recuperación de información desde Supabase.
    """
    
    def __init__(self):
        """Inicializa el cliente de Supabase y embeddings."""
        self.supabase_url = os.environ.get("SUPABASE_URL")
        # Usar ANON_KEY para operaciones de lectura RAG (más seguro que SERVICE_KEY)
        # Las políticas RLS permiten lectura pública en las tablas de teoría
        self.supabase_key = os.environ.get("SUPABASE_ANON_KEY") or os.environ.get("SUPABASE_SERVICE_KEY")
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError(
                "SUPABASE_URL y SUPABASE_ANON_KEY (o SUPABASE_SERVICE_KEY para retrocompatibilidad) "
                "deben estar configurados en las variables de entorno"
            )
        
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        
        # Embeddings usando OpenRouter (mismo modelo de OpenAI pero vía OpenRouter)
        # Model: openai/text-embedding-3-small (1536 dimensiones, $0.02/M tokens)
        openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")
        if not openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY debe estar configurado en las variables de entorno")
        
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=openrouter_api_key,  # OpenRouter usa el mismo formato
            model="openai/text-embedding-3-small",
            base_url="https://openrouter.ai/api/v1"
        )
    
    def search_theory(
        self,
        query: str,
        table_name: str,
        query_name: str,
        match_count: int = 5,
        filter_metadata: dict = None
    ) -> List[Dict[str, Any]]:
        """
        Busca teoría relevante en Supabase usando búsqueda semántica.
        
        Args:
            query: Pregunta o consulta del usuario
            table_name: Nombre de la tabla en Supabase (wollok, haskell, prolog)
            query_name: Nombre de la función RPC en Supabase (wollok_search, etc.)
            match_count: Número de resultados a retornar
            filter_metadata: Filtro opcional para metadata (jsonb)
        
        Returns:
            Lista de documentos relevantes con su contenido y metadata
        """
        try:
            # Generar embedding de la consulta
            query_embedding = self.embeddings.embed_query(query)
            
            # Preparar parámetros para la función RPC
            # Orden correcto: query_embedding, match_count, filter
            rpc_params = {
                "query_embedding": query_embedding,
                "match_count": match_count
            }
            
            # Agregar filter solo si se proporciona
            if filter_metadata:
                rpc_params["filter"] = filter_metadata
            
            # Realizar búsqueda en Supabase usando la función RPC
            response = self.supabase.rpc(query_name, rpc_params).execute()
            
            return response.data if response.data else []
        
        except Exception as e:
            print(f"Error en búsqueda RAG: {e}")
            return []
    
    def format_results(self, results: List[Dict[str, Any]]) -> str:
        """
        Formatea los resultados de la búsqueda para el agente.
        
        Args:
            results: Lista de resultados de Supabase
        
        Returns:
            String formateado con la información recuperada
        """
        if not results:
            return "No se encontró información relevante en la base de conocimientos."
        
        formatted = "# Teoría Recuperada\n\n"
        
        for i, doc in enumerate(results, 1):
            content = doc.get("content", "")
            similarity = doc.get("similarity", 0)
            metadata = doc.get("metadata", {})
            
            formatted += f"## Fragmento {i} (Similitud: {similarity:.3f})\n"
            
            # Agregar metadata si existe y es útil
            if metadata:
                source = metadata.get("source", "")
                if source:
                    formatted += f"**Fuente:** {source}\n\n"
            
            formatted += f"{content}\n\n"
            formatted += "---\n\n"
        
        return formatted


# Instancia global de SupabaseRAG
_rag_instance = None


def get_rag_instance() -> SupabaseRAG:
    """Obtiene o crea la instancia global de SupabaseRAG."""
    global _rag_instance
    if _rag_instance is None:
        _rag_instance = SupabaseRAG()
    return _rag_instance


@tool
def recuperar_teoria(query: str, agent_config: Dict[str, Any] = None) -> str:
    """
    Recupera teoría relevante desde la base de conocimientos usando búsqueda semántica.
    
    Esta herramienta busca en la base de datos vectorial de Supabase información
    relevante sobre conceptos, sintaxis, ejemplos y mejores prácticas del lenguaje
    de programación correspondiente (Wollok, Haskell o Prolog).
    
    Args:
        query: La pregunta o concepto a buscar (ej: "herencia en wollok", "listas en haskell")
        agent_config: Configuración del agente con tabla y query_name (opcional, se usa contexto si no se provee)
    
    Returns:
        String con la información recuperada formateada y lista para usar
    
    Ejemplos:
        - "objetos y clases en wollok"
        - "funciones de orden superior en haskell"
        - "unificación y backtracking en prolog"
    """
    try:
        rag = get_rag_instance()
        
        # Si no se provee configuración, usar valores por defecto (Wollok)
        if agent_config is None:
            table_name = "wollok"
            query_name = "wollok_search"
        else:
            table_name = agent_config.get("table", "wollok")
            query_name = agent_config.get("query_name", "wollok_search")
        
        # Realizar búsqueda
        results = rag.search_theory(
            query=query,
            table_name=table_name,
            query_name=query_name,
            match_count=5
        )
        
        # Formatear y retornar resultados
        return rag.format_results(results)
    
    except Exception as e:
        return f"Error al recuperar teoría: {str(e)}"


def create_recuperar_teoria_tool(agent_config: Dict[str, Any]):
    """
    Crea una instancia personalizada de la tool recuperar_teoria para un agente específico.
    
    Args:
        agent_config: Configuración del agente (incluye tabla y query_name)
    
    Returns:
        Tool configurada para el agente específico
    """
    from functools import partial
    
    # Crear una versión parcial de la función con la configuración del agente
    configured_tool = partial(recuperar_teoria, agent_config=agent_config)
    configured_tool.__name__ = "recuperar_teoria"
    configured_tool.__doc__ = recuperar_teoria.__doc__
    
    return tool(configured_tool)

