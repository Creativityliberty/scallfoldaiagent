from typing import Dict, Any
import tiktoken

class TokenCounter:
    """Gestionnaire de comptage de tokens et estimation de coûts."""

    def __init__(self, model: str = "gpt-4"):
        """
        Note: Gemini utilise un tokenizer différent, mais tiktoken donne
        une estimation raisonnable. Pour production, utiliser l'API Gemini officielle.
        """
        try:
            self.encoder = tiktoken.encoding_for_model(model)
        except KeyError:
            self.encoder = tiktoken.get_encoding("cl100k_base")

        # Prix approximatifs (à ajuster selon les tarifs réels Gemini)
        self.pricing = {
            "gemini-1.5-flash": {"input": 0.00035 / 1000, "output": 0.00105 / 1000},
            "gemini-1.5-pro": {"input": 0.0035 / 1000, "output": 0.0105 / 1000},
        }

    def count_tokens(self, text: str) -> int:
        """Compte le nombre de tokens dans un texte."""
        return len(self.encoder.encode(text))

    def estimate_cost(
        self,
        input_text: str,
        output_text: str,
        model: str = "gemini-1.5-flash"
    ) -> Dict[str, Any]:
        """Estime le coût d'une génération."""
        input_tokens = self.count_tokens(input_text)
        output_tokens = self.count_tokens(output_text)

        pricing = self.pricing.get(model, self.pricing["gemini-1.5-flash"])

        input_cost = input_tokens * pricing["input"]
        output_cost = output_tokens * pricing["output"]
        total_cost = input_cost + output_cost

        return {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "input_cost_usd": input_cost,
            "output_cost_usd": output_cost,
            "total_cost_usd": total_cost,
            "model": model,
        }

    def format_cost_report(self, cost_data: Dict[str, Any]) -> str:
        """Formate un rapport de coût lisible."""
        return f"""
Token Usage Report
==================
Model: {cost_data['model']}
Input tokens: {cost_data['input_tokens']:,}
Output tokens: {cost_data['output_tokens']:,}
Total tokens: {cost_data['total_tokens']:,}

Cost Breakdown
--------------
Input:  ${cost_data['input_cost_usd']:.6f}
Output: ${cost_data['output_cost_usd']:.6f}
Total:  ${cost_data['total_cost_usd']:.6f}
"""
