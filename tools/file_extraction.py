"""
Herramientas para extraer texto de archivos PDF e imágenes.
Implementa la extracción de contenido de archivos adjuntos por los usuarios.
"""

import os
import base64
from typing import Optional
from io import BytesIO
import PyPDF2
from PIL import Image
from langchain_openai import ChatOpenAI


class FileExtractor:
    """
    Clase para extraer texto de PDFs e imágenes.
    """
    
    def __init__(self):
        """Inicializa el extractor con un modelo simple para análisis de imágenes."""
        openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")
        
        if openrouter_api_key:
            # Modelo ligero para análisis de imágenes
            self.vision_model = ChatOpenAI(
                model="openai/gpt-4o-mini",
                base_url="https://openrouter.ai/api/v1",
                api_key=openrouter_api_key,
                temperature=0.3
            )
        else:
            self.vision_model = None
    
    def extract_from_pdf(self, pdf_file) -> str:
        """
        Extrae texto de un archivo PDF.
        
        Args:
            pdf_file: Archivo PDF (UploadedFile de Streamlit o bytes)
        
        Returns:
            Texto extraído del PDF
        """
        try:
            # Resetear puntero del archivo al inicio
            pdf_file.seek(0)
            
            # Leer el PDF
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Extraer texto de todas las páginas
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += f"\n--- Página {page_num + 1} ---\n"
                text += page.extract_text()
            
            if not text.strip():
                return "⚠️ El PDF no contiene texto extraíble (puede ser una imagen escaneada)."
            
            return text.strip()
        
        except Exception as e:
            return f"❌ Error al extraer texto del PDF: {str(e)}"
    
    def extract_from_image(self, image_file) -> str:
        """
        Analiza una imagen usando un modelo de visión y extrae texto/información.
        
        Args:
            image_file: Archivo de imagen (UploadedFile de Streamlit o bytes)
        
        Returns:
            Descripción y texto extraído de la imagen
        """
        try:
            if self.vision_model is None:
                return "⚠️ Análisis de imágenes no disponible. Configure OPENROUTER_API_KEY."
            
            # Resetear puntero del archivo al inicio
            image_file.seek(0)
            
            # Abrir imagen con PIL
            image = Image.open(image_file)
            
            # Convertir a RGB si es necesario
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convertir a base64
            buffered = BytesIO()
            image.save(buffered, format="JPEG", quality=85)
            img_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            # Analizar con modelo de visión
            prompt = """Analiza esta imagen y extrae toda la información relevante:
            - Si contiene código, transcríbelo exactamente
            - Si contiene texto, extráelo completamente
            - Si es un diagrama o gráfico, descríbelo en detalle
            - Si contiene ejercicios o problemas, transcríbelos fielmente
            
            Responde en español de manera clara y estructurada."""
            
            # Crear mensaje con imagen usando OpenAI format
            from langchain_core.messages import HumanMessage
            
            message = HumanMessage(
                content=[
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{img_base64}",
                            "detail": "high"
                        }
                    }
                ]
            )
            
            response = self.vision_model.invoke([message])
            return response.content
        
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Error detallado al analizar imagen: {error_details}")
            return f"❌ Error al analizar la imagen: {str(e)}"
    
    def extract_from_file(self, uploaded_file) -> Optional[str]:
        """
        Extrae contenido de un archivo (detecta tipo automáticamente).
        
        Args:
            uploaded_file: Archivo subido por el usuario
        
        Returns:
            Texto extraído o None si no se pudo procesar
        """
        if uploaded_file is None:
            return None
        
        # Obtener extensión del archivo
        file_name = uploaded_file.name.lower()
        
        if file_name.endswith('.pdf'):
            return self.extract_from_pdf(uploaded_file)
        
        elif file_name.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
            return self.extract_from_image(uploaded_file)
        
        else:
            return f"⚠️ Tipo de archivo no soportado: {file_name}"


# Instancia global
_extractor_instance = None


def get_file_extractor() -> FileExtractor:
    """Obtiene o crea la instancia global de FileExtractor."""
    global _extractor_instance
    if _extractor_instance is None:
        _extractor_instance = FileExtractor()
    return _extractor_instance

