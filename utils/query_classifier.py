"""
Clasificador de dificultad de consultas para optimizar selección de LLM.
Analiza el input del usuario y determina el modelo más apropiado según la complejidad.
"""

import re
from typing import Dict, Literal, Tuple
from dataclasses import dataclass

QueryType = Literal["theoretical", "coding", "debugging", "conceptual"]
Difficulty = Literal["simple", "medium", "complex"]


@dataclass
class QueryClassification:
    """Resultado de la clasificación de una consulta."""
    query_type: QueryType
    difficulty: Difficulty
    suggested_model_tier: str  # "economy", "balanced", "premium"
    confidence: float
    reasoning: str


class QueryClassifier:
    """
    Clasifica consultas del usuario para optimizar selección de modelo.
    
    Estrategia de optimización de costos:
    - Preguntas teóricas simples → Modelos económicos (Gemini Flash Lite)
    - Desarrollo de código → Modelos balanceados/premium (GPT Codex, Grok, Qwen)
    - Debugging complejo → Modelos premium (Claude Opus)
    """
    
    # Patrones para identificación de tipo de consulta
    THEORETICAL_PATTERNS = [
        r'\b(qu[eé] es|define|explica|concepto|teor[ií]a)\b',
        r'\b(diferencia entre|comparar|ventaja|desventaja)\b',
        r'\b(paradigma|principio|fundamento)\b',
    ]
    
    CODING_PATTERNS = [
        r'\b(escrib[ie]|implement[ae]|crea|codifica|programa)\b',
        r'\b(funci[oó]n|m[eé]todo|clase|objeto|predicado)\b',
        r'\b(c[oó]digo|soluci[oó]n|ejercicio|problema)\b',
        r'\b(resuelve|resolver|desarrolla|haz que)\b',
    ]
    
    DEBUGGING_PATTERNS = [
        r'\b(error|falla|bug|problema con|no funciona)\b',
        r'\b(debug|depura|corrige|arregla|fix)\b',
        r'\b(por qu[eé] no|c[oó]mo soluciono)\b',
    ]
    
    # Patrones de complejidad
    SIMPLE_INDICATORS = [
        r'\b(qu[eé] es|define|ejemplo simple)\b',
        r'^.{1,50}$',  # Consultas muy cortas
    ]
    
    COMPLEX_INDICATORS = [
        r'\b(implementar|desarrollar|optimizar|refactorizar)\b',
        r'\b(m[uú]ltiples|varios|diferentes|combinar)\b',
        r'\b(pattern|patr[oó]n|arquitectura|dise[ñn]o)\b',
        r'^.{200,}$',  # Consultas muy largas
    ]
    
    def __init__(self):
        """Inicializa el clasificador."""
        pass
    
    def classify(self, query: str, context: Dict = None) -> QueryClassification:
        """
        Clasifica una consulta de usuario.
        
        Args:
            query: Texto de la consulta del usuario
            context: Contexto adicional (archivos adjuntos, historial, etc.)
        
        Returns:
            QueryClassification con tipo, dificultad y modelo sugerido
        """
        query_lower = query.lower()
        
        # 1. Determinar tipo de consulta
        query_type, type_confidence = self._determine_query_type(query_lower)
        
        # 2. Determinar dificultad
        difficulty, diff_confidence = self._determine_difficulty(query_lower, context)
        
        # 3. Sugerir tier de modelo
        model_tier = self._suggest_model_tier(query_type, difficulty)
        
        # 4. Confidence global
        overall_confidence = (type_confidence + diff_confidence) / 2
        
        # 5. Razonamiento
        reasoning = self._build_reasoning(query_type, difficulty, model_tier)
        
        return QueryClassification(
            query_type=query_type,
            difficulty=difficulty,
            suggested_model_tier=model_tier,
            confidence=overall_confidence,
            reasoning=reasoning
        )
    
    def _determine_query_type(self, query: str) -> Tuple[QueryType, float]:
        """Determina el tipo de consulta."""
        scores = {
            "theoretical": self._count_pattern_matches(query, self.THEORETICAL_PATTERNS),
            "debugging": self._count_pattern_matches(query, self.DEBUGGING_PATTERNS),
            "coding": self._count_pattern_matches(query, self.CODING_PATTERNS),
        }
        
        # Si no hay matches claros, considerar conceptual
        if all(score == 0 for score in scores.values()):
            return "conceptual", 0.5
        
        # Retornar el tipo con mayor score
        max_type = max(scores, key=scores.get)
        max_score = scores[max_type]
        
        # Confidence basado en qué tan claro es el ganador
        total_score = sum(scores.values())
        confidence = max_score / total_score if total_score > 0 else 0.5
        
        return max_type, min(confidence, 1.0)
    
    def _determine_difficulty(self, query: str, context: Dict = None) -> Tuple[Difficulty, float]:
        """Determina la dificultad de la consulta."""
        simple_score = self._count_pattern_matches(query, self.SIMPLE_INDICATORS)
        complex_score = self._count_pattern_matches(query, self.COMPLEX_INDICATORS)
        
        # Factores adicionales
        has_attachment = context and context.get("has_attachment", False)
        query_length = len(query)
        
        # Scoring
        if has_attachment:
            complex_score += 1
        
        if query_length < 30:
            simple_score += 1
        elif query_length > 150:
            complex_score += 1
        
        # Decisión
        if simple_score > complex_score:
            difficulty = "simple"
            confidence = 0.8
        elif complex_score > simple_score * 1.5:
            difficulty = "complex"
            confidence = 0.9
        else:
            difficulty = "medium"
            confidence = 0.7
        
        return difficulty, confidence
    
    def _suggest_model_tier(self, query_type: QueryType, difficulty: Difficulty) -> str:
        """
        Sugiere tier de modelo según tipo y dificultad.
        
        Tiers:
        - economy: Gemini 2.5 Flash Lite ($0.1/$0.4 por 1M tokens)
        - balanced: GPT Codex Mini, Grok Fast, Qwen Coder
        - premium: Claude Opus ($5/$25 por 1M tokens)
        """
        # Matriz de decisión
        tier_matrix = {
            ("theoretical", "simple"): "economy",
            ("theoretical", "medium"): "economy",
            ("theoretical", "complex"): "balanced",
            ("conceptual", "simple"): "economy",
            ("conceptual", "medium"): "balanced",
            ("conceptual", "complex"): "balanced",
            ("coding", "simple"): "balanced",
            ("coding", "medium"): "balanced",
            ("coding", "complex"): "premium",
            ("debugging", "simple"): "balanced",
            ("debugging", "medium"): "balanced",
            ("debugging", "complex"): "premium",
        }
        
        return tier_matrix.get((query_type, difficulty), "balanced")
    
    def _count_pattern_matches(self, text: str, patterns: list) -> int:
        """Cuenta cuántos patrones coinciden en el texto."""
        count = 0
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                count += 1
        return count
    
    def _build_reasoning(self, query_type: QueryType, difficulty: Difficulty, tier: str) -> str:
        """Construye explicación de la clasificación."""
        type_desc = {
            "theoretical": "pregunta teórica",
            "coding": "desarrollo de código",
            "debugging": "depuración/debugging",
            "conceptual": "consulta conceptual"
        }
        
        diff_desc = {
            "simple": "simple",
            "medium": "moderada",
            "complex": "compleja"
        }
        
        tier_desc = {
            "economy": "modelo económico",
            "balanced": "modelo balanceado",
            "premium": "modelo premium"
        }
        
        return f"Clasificada como {type_desc[query_type]} de dificultad {diff_desc[difficulty]}. Sugerido: {tier_desc[tier]}."


# Singleton global
_classifier_instance = None

def get_classifier() -> QueryClassifier:
    """Obtiene instancia singleton del clasificador."""
    global _classifier_instance
    if _classifier_instance is None:
        _classifier_instance = QueryClassifier()
    return _classifier_instance
