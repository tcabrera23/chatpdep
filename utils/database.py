"""
Manejo de base de datos SQLite para historial de conversaciones.
Implementa el almacenamiento local de conversaciones del usuario.
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import os


class ConversationDatabase:
    """
    Clase para manejar el historial de conversaciones en SQLite.
    """
    
    def __init__(self, db_path: str = "data/conversations.db"):
        """
        Inicializa la base de datos.
        
        Args:
            db_path: Ruta al archivo de base de datos SQLite
        """
        self.db_path = db_path
        
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Inicializar base de datos
        self._init_db()
    
    def _init_db(self):
        """Crea las tablas necesarias si no existen."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de conversaciones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                agent_name TEXT NOT NULL,
                model_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabla de mensajes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                has_attachment BOOLEAN DEFAULT 0,
                attachment_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id)
            )
        """)
        
        # Índices para mejorar performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_conv_id 
            ON messages(conversation_id)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_created_at 
            ON conversations(created_at DESC)
        """)
        
        conn.commit()
        conn.close()
    
    def create_conversation(
        self,
        conversation_id: str,
        title: str,
        agent_name: str,
        model_name: str
    ) -> bool:
        """
        Crea una nueva conversación.
        
        Args:
            conversation_id: ID único de la conversación
            title: Título de la conversación
            agent_name: Nombre del agente (Wollok, Haskell, Prolog)
            model_name: Modelo LLM usado
        
        Returns:
            True si se creó exitosamente
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO conversations (conversation_id, title, agent_name, model_name)
                VALUES (?, ?, ?, ?)
            """, (conversation_id, title, agent_name, model_name))
            
            conn.commit()
            conn.close()
            return True
        
        except sqlite3.IntegrityError:
            # La conversación ya existe
            return False
        except Exception as e:
            print(f"Error al crear conversación: {e}")
            return False
    
    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        has_attachment: bool = False,
        attachment_type: Optional[str] = None
    ) -> bool:
        """
        Añade un mensaje a una conversación.
        
        Args:
            conversation_id: ID de la conversación
            role: Rol del mensaje (user, assistant)
            content: Contenido del mensaje
            has_attachment: Si el mensaje tiene archivo adjunto
            attachment_type: Tipo de archivo (pdf, image)
        
        Returns:
            True si se añadió exitosamente
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO messages (conversation_id, role, content, has_attachment, attachment_type)
                VALUES (?, ?, ?, ?, ?)
            """, (conversation_id, role, content, has_attachment, attachment_type))
            
            # Actualizar timestamp de conversación
            cursor.execute("""
                UPDATE conversations 
                SET updated_at = CURRENT_TIMESTAMP 
                WHERE conversation_id = ?
            """, (conversation_id,))
            
            conn.commit()
            conn.close()
            return True
        
        except Exception as e:
            print(f"Error al añadir mensaje: {e}")
            return False
    
    def get_conversation_messages(self, conversation_id: str) -> List[Dict[str, str]]:
        """
        Obtiene todos los mensajes de una conversación.
        
        Args:
            conversation_id: ID de la conversación
        
        Returns:
            Lista de mensajes en formato [{"role": "user", "content": "..."}, ...]
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT role, content, has_attachment, attachment_type, created_at
                FROM messages
                WHERE conversation_id = ?
                ORDER BY created_at ASC
            """, (conversation_id,))
            
            messages = []
            for row in cursor.fetchall():
                message = {
                    "role": row[0],
                    "content": row[1]
                }
                if row[2]:  # has_attachment
                    message["attachment_type"] = row[3]
                messages.append(message)
            
            conn.close()
            return messages
        
        except Exception as e:
            print(f"Error al obtener mensajes: {e}")
            return []
    
    def get_all_conversations(self) -> List[Dict[str, any]]:
        """
        Obtiene todas las conversaciones ordenadas por fecha.
        
        Returns:
            Lista de conversaciones con metadata
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT conversation_id, title, agent_name, model_name, created_at, updated_at
                FROM conversations
                ORDER BY updated_at DESC
            """)
            
            conversations = []
            for row in cursor.fetchall():
                conversations.append({
                    "conversation_id": row[0],
                    "title": row[1],
                    "agent_name": row[2],
                    "model_name": row[3],
                    "created_at": row[4],
                    "updated_at": row[5]
                })
            
            conn.close()
            return conversations
        
        except Exception as e:
            print(f"Error al obtener conversaciones: {e}")
            return []
    
    def update_conversation_title(self, conversation_id: str, new_title: str) -> bool:
        """
        Actualiza el título de una conversación.
        
        Args:
            conversation_id: ID de la conversación
            new_title: Nuevo título
        
        Returns:
            True si se actualizó exitosamente
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE conversations 
                SET title = ?, updated_at = CURRENT_TIMESTAMP
                WHERE conversation_id = ?
            """, (new_title, conversation_id))
            
            conn.commit()
            conn.close()
            return True
        
        except Exception as e:
            print(f"Error al actualizar título: {e}")
            return False
    
    def delete_conversation(self, conversation_id: str) -> bool:
        """
        Elimina una conversación y todos sus mensajes.
        
        Args:
            conversation_id: ID de la conversación
        
        Returns:
            True si se eliminó exitosamente
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Eliminar mensajes
            cursor.execute("""
                DELETE FROM messages WHERE conversation_id = ?
            """, (conversation_id,))
            
            # Eliminar conversación
            cursor.execute("""
                DELETE FROM conversations WHERE conversation_id = ?
            """, (conversation_id,))
            
            conn.commit()
            conn.close()
            return True
        
        except Exception as e:
            print(f"Error al eliminar conversación: {e}")
            return False
    
    def get_conversation_info(self, conversation_id: str) -> Optional[Dict[str, any]]:
        """
        Obtiene información de una conversación específica.
        
        Args:
            conversation_id: ID de la conversación
        
        Returns:
            Diccionario con información de la conversación o None
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT conversation_id, title, agent_name, model_name, created_at, updated_at
                FROM conversations
                WHERE conversation_id = ?
            """, (conversation_id,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return {
                    "conversation_id": row[0],
                    "title": row[1],
                    "agent_name": row[2],
                    "model_name": row[3],
                    "created_at": row[4],
                    "updated_at": row[5]
                }
            return None
        
        except Exception as e:
            print(f"Error al obtener info de conversación: {e}")
            return None

