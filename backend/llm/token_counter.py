from typing import Dict

def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)

def cost_estimate(text: str, price_per_1k: float = 0.0) -> Dict[str, float]:
    tokens = estimate_tokens(text)
    return {"tokens": tokens, "usd": (tokens / 1000) * price_per_1k}
