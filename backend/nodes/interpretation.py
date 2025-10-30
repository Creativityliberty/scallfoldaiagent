from ..core.base_node import BaseNode
from ..core.shared import Shared
from typing import Dict, Any

class InterpretationNode(BaseNode):
    """
    Module 2: Interprétation
    Analyse l'intention et le type de tâche.
    """

    def __init__(self) -> None:
        super().__init__("interpretation")

    def prep(self, shared: Shared) -> Dict[str, Any]:
        """Récupère les données de perception."""
        perception = shared.get_result("perception")
        return {
            "clean_input": perception.get("clean_input", ""),
            "has_question": perception.get("has_question", False),
            "has_command": perception.get("has_command", False),
            "language": perception.get("language", "unknown")
        }

    async def exec(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Détermine l'intention et le type de tâche."""
        text = input_data.get("clean_input", "").lower()

        # Détection d'intention
        intent = self._detect_intent(text, input_data)

        # Détection du type de tâche
        task_type = self._detect_task_type(text, intent)

        # Extraction d'entités simples
        entities = self._extract_entities(text)

        # Analyse de sentiment
        sentiment = self._analyze_sentiment(text)

        return {
            "intent": intent,
            "task_type": task_type,
            "entities": entities,
            "sentiment": sentiment,
            "language": input_data.get("language", "unknown"),
            "complexity": self._estimate_complexity(text)
        }

    def _detect_intent(self, text: str, context: Dict[str, Any]) -> str:
        """Détecte l'intention principale."""
        if context.get("has_question"):
            if any(kw in text for kw in ["comment", "pourquoi", "quel", "quand", "où"]):
                return "information_seeking"
            return "question"

        if context.get("has_command"):
            if any(kw in text for kw in ["crée", "génère", "écris"]):
                return "creation"
            if any(kw in text for kw in ["analyse", "explique", "détaille"]):
                return "analysis"
            return "instruction"

        return "conversation"

    def _detect_task_type(self, text: str, intent: str) -> str:
        """Détermine le type de tâche."""
        if intent in ["information_seeking", "question"]:
            return "qa"
        elif intent == "creation":
            if any(kw in text for kw in ["code", "fonction", "script", "programme"]):
                return "code_generation"
            return "text_generation"
        elif intent == "analysis":
            return "reasoning"
        return "general"

    def _extract_entities(self, text: str) -> list[str]:
        """Extraction basique d'entités (à améliorer avec NER)."""
        # Pour l'instant, retourne les mots capitalisés
        import re
        entities = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        return list(set(entities))

    def _analyze_sentiment(self, text: str) -> str:
        """Analyse de sentiment basique."""
        positive_words = ['merci', 'super', 'excellent', 'génial', 'parfait', 'bien']
        negative_words = ['problème', 'erreur', 'bug', 'mauvais', 'nul', 'mal']

        pos_count = sum(1 for word in positive_words if word in text)
        neg_count = sum(1 for word in negative_words if word in text)

        if pos_count > neg_count:
            return "positive"
        elif neg_count > pos_count:
            return "negative"
        return "neutral"

    def _estimate_complexity(self, text: str) -> str:
        """Estime la complexité de la requête."""
        word_count = len(text.split())

        if word_count < 10:
            return "simple"
        elif word_count < 30:
            return "medium"
        return "complex"
