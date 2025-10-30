from typing import Dict, Any, List

class PromptBuilder:
    """Constructeur de prompts pour RRLA et autres patterns."""

    @staticmethod
    def build_rrla_decompose(context: Dict[str, Any]) -> str:
        """Construit un prompt pour la décomposition (R1)."""
        return f"""Tu es un agent de raisonnement expert. Décompose cette requête en étapes logiques claires et actionnables.

Requête utilisateur: {context.get('clean_input', '')}
Type de tâche: {context.get('task_type', 'general')}
Intention détectée: {context.get('intent', 'unknown')}

Contexte additionnel:
{context.get('memory_context', 'Aucun contexte historique')}

Réponds UNIQUEMENT en JSON avec cette structure exacte:
{{
    "steps": [
        {{"id": 1, "action": "description de l'action", "rationale": "pourquoi cette étape"}},
        {{"id": 2, "action": "description de l'action", "rationale": "pourquoi cette étape"}}
    ]
}}

Sois concis et pragmatique. Maximum 5 étapes."""

    @staticmethod
    def build_rrla_reflect(steps: List[Dict[str, Any]], context: Dict[str, Any]) -> str:
        """Construit un prompt pour la réflexion (R2)."""
        steps_str = "\n".join([f"{s['id']}. {s['action']}" for s in steps])
        return f"""Évalue la faisabilité et la pertinence de ces étapes:

{steps_str}

Contexte: {context.get('clean_input', '')}

Pour chaque étape, fournis:
- feasibility (0.0 à 1.0): probabilité de succès
- priority (1-5): importance
- risks: risques potentiels

Réponds en JSON:
{{
    "evaluations": [
        {{"step_id": 1, "feasibility": 0.9, "priority": 5, "risks": ["risque1"]}},
        ...
    ]
}}"""

    @staticmethod
    def build_synthesis(reasoning_result: Dict[str, Any], input_text: str) -> str:
        """Construit un prompt pour la synthèse finale."""
        steps = reasoning_result.get("steps", [])
        steps_summary = "\n".join([f"- {s.get('action', '')}" for s in steps])

        return f"""Tu es un agent de synthèse. Génère une réponse claire et complète.

Question originale: {input_text}

Raisonnement effectué:
{steps_summary}

Décision prise: {reasoning_result.get('decision', {})}
Confiance: {reasoning_result.get('confidence', 0.0)*100:.0f}%

Génère une réponse:
1. Naturelle et conversationnelle
2. Qui intègre le raisonnement
3. Qui répond directement à la question
4. Avec des exemples si pertinent

Réponds directement sans métadonnées ni JSON."""

    @staticmethod
    def build_system_prompt() -> str:
        """Prompt système général pour l'agent."""
        return """Tu es un agent IA avancé utilisant l'architecture RRLA (Raisonnement, Réflexion, Logique, Action).

Tes principes:
- Raisonner avant d'agir
- Être précis et factuel
- Citer tes sources quand disponibles
- Admettre tes limites
- Privilégier la clarté à la verbosité

Tu as accès à des outils via MCP (Model Context Protocol) pour étendre tes capacités."""
