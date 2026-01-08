"""
Utilidad para tracking de métricas y uso de tokens en Supabase.
Usa ANON_KEY para mayor seguridad (RLS configurado para permitir inserción pública).
"""

import os
from typing import Optional
from datetime import datetime
from supabase import create_client, Client


class MetricsTracker:
    """
    Clase para registrar métricas de uso de la aplicación en Supabase.
    Usa el anon key para insertar registros (RLS permite inserción pública).
    """
    
    def __init__(self):
        """Inicializa el cliente de Supabase con anon key."""
        self.supabase_url = os.environ.get("SUPABASE_URL")
        # Usar ANON_KEY para tracking (más seguro)
        self.supabase_key = os.environ.get("SUPABASE_ANON_KEY") or os.environ.get("SUPABASE_SERVICE_KEY")
        
        if not self.supabase_url or not self.supabase_key:
            # No lanzar error, solo registrar warning
            self.supabase = None
            print("⚠️  SUPABASE_URL y SUPABASE_ANON_KEY no configurados. Tracking deshabilitado.")
        else:
            self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
    
    def log_interaction(
        self,
        conversation_id: str,
        user_input: str,
        agent_response: str,
        tokens_in: Optional[int] = None,
        tokens_out: Optional[int] = None,
        llm_latency_ms: Optional[int] = None,
        workflow_duration_ms: Optional[int] = None,
        agent_name: Optional[str] = None,
        model_name: Optional[str] = None
    ) -> bool:
        """
        Registra una interacción en la tabla chatpdep_tokens.
        
        Args:
            conversation_id: ID de la conversación
            user_input: Pregunta del usuario
            agent_response: Respuesta del agente
            tokens_in: Tokens de entrada
            tokens_out: Tokens de salida
            llm_latency_ms: Latencia del LLM en ms
            workflow_duration_ms: Duración total del flujo en ms
            agent_name: Nombre del agente (Wollok, Haskell, Prolog)
            model_name: Modelo LLM usado
        
        Returns:
            True si se registró correctamente, False si hubo error
        """
        if not self.supabase:
            return False
        
        try:
            tokens_total = None
            if tokens_in is not None and tokens_out is not None:
                tokens_total = tokens_in + tokens_out
            
            data = {
                "conversation_id": conversation_id,
                "user_input": user_input,
                "agent_response": agent_response,
                "tokens_in": tokens_in,
                "tokens_out": tokens_out,
                "tokens_total": tokens_total,
                "llm_api_latency_ms": llm_latency_ms,
                "workflow_duration_ms": workflow_duration_ms,
                "timestamp": datetime.utcnow().isoformat(),
                # Campos adicionales opcionales
                "n8n_workflow_name": agent_name,  # Reutilizar campo legacy
                "n8n_workflow_id": model_name      # Reutilizar campo legacy
            }
            
            # Insertar en Supabase (RLS permite inserción pública)
            result = self.supabase.table("chatpdep_tokens").insert(data).execute()
            
            return True
        
        except Exception as e:
            print(f"⚠️  Error al registrar métrica: {e}")
            return False


# Instancia global singleton
_tracker_instance = None


def get_tracker() -> MetricsTracker:
    """
    Retorna la instancia singleton del tracker.
    """
    global _tracker_instance
    if _tracker_instance is None:
        _tracker_instance = MetricsTracker()
    return _tracker_instance


def log_interaction(
    conversation_id: str,
    user_input: str,
    agent_response: str,
    **kwargs
) -> bool:
    """
    Función de conveniencia para registrar una interacción.
    
    Args:
        conversation_id: ID de la conversación
        user_input: Pregunta del usuario
        agent_response: Respuesta del agente
        **kwargs: Argumentos adicionales (tokens_in, tokens_out, etc.)
    
    Returns:
        True si se registró correctamente, False si hubo error
    """
    tracker = get_tracker()
    return tracker.log_interaction(
        conversation_id=conversation_id,
        user_input=user_input,
        agent_response=agent_response,
        **kwargs
    )

