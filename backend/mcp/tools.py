from typing import List, Dict, Any
from loguru import logger
import asyncio

# === MEMORY TOOLS ===

async def search_memory(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Recherche sémantique dans la mémoire de l'agent.

    Args:
        query: Requête de recherche
        top_k: Nombre de résultats à retourner

    Returns:
        Liste de résultats avec scores
    """
    logger.info(f"Searching memory for: {query} (top_k={top_k})")

    # Simulation - à remplacer par une vraie recherche vectorielle
    await asyncio.sleep(0.1)  # Simule une latence

    return [
        {
            "content": f"Résultat {i+1} pour: {query}",
            "score": 0.95 - (i * 0.1),
            "timestamp": "2025-10-28T12:00:00Z",
            "source": "conversation"
        }
        for i in range(min(top_k, 3))
    ]

async def store_memory(content: str, metadata: Dict[str, Any] | None = None) -> Dict[str, str]:
    """
    Stocke un élément en mémoire.

    Args:
        content: Contenu à stocker
        metadata: Métadonnées optionnelles

    Returns:
        Confirmation avec ID
    """
    logger.info(f"Storing memory: {content[:50]}...")

    memory_id = f"mem_{hash(content) % 100000}"

    return {
        "status": "stored",
        "memory_id": memory_id,
        "content_length": len(content)
    }

# === ANALYSIS TOOLS ===

async def analyze_sentiment(text: str) -> Dict[str, Any]:
    """
    Analyse le sentiment d'un texte.

    Args:
        text: Texte à analyser

    Returns:
        Résultats d'analyse de sentiment
    """
    logger.info(f"Analyzing sentiment for text length: {len(text)}")

    # Analyse basique
    positive_words = ['bon', 'excellent', 'super', 'génial', 'parfait', 'merci']
    negative_words = ['mauvais', 'nul', 'problème', 'erreur', 'bug']

    text_lower = text.lower()
    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)

    total = pos_count + neg_count
    if total == 0:
        sentiment = "neutral"
        score = 0.5
    elif pos_count > neg_count:
        sentiment = "positive"
        score = 0.5 + (pos_count / (total * 2))
    else:
        sentiment = "negative"
        score = 0.5 - (neg_count / (total * 2))

    return {
        "sentiment": sentiment,
        "score": score,
        "confidence": 0.75,
        "details": {
            "positive_indicators": pos_count,
            "negative_indicators": neg_count
        }
    }

async def extract_keywords(text: str, max_keywords: int = 10) -> List[Dict[str, Any]]:
    """
    Extrait les mots-clés importants d'un texte.

    Args:
        text: Texte à analyser
        max_keywords: Nombre maximum de mots-clés

    Returns:
        Liste de mots-clés avec scores
    """
    logger.info(f"Extracting keywords from text length: {len(text)}")

    # Extraction basique par fréquence (à améliorer avec TF-IDF)
    import re
    from collections import Counter

    # Nettoie et tokenize
    words = re.findall(r'\b\w{4,}\b', text.lower())

    # Stop words français basiques
    stop_words = {'dans', 'avec', 'pour', 'cette', 'mais', 'sont', 'était', 'fait', 'plus'}
    words = [w for w in words if w not in stop_words]

    # Compte les occurrences
    word_counts = Counter(words)

    keywords = [
        {"keyword": word, "frequency": count, "score": count / len(words)}
        for word, count in word_counts.most_common(max_keywords)
    ]

    return keywords

# === UTILITY TOOLS ===

async def calculate(expression: str) -> Dict[str, Any]:
    """
    Évalue une expression mathématique.

    Args:
        expression: Expression mathématique à évaluer

    Returns:
        Résultat du calcul
    """
    logger.info(f"Calculating: {expression}")

    try:
        # Sécurité: whitelist des opérations autorisées
        import ast
        import operator

        ops = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.USub: operator.neg,
        }

        def eval_expr(node: Any) -> float:
            if isinstance(node, ast.Num):
                return float(node.n)
            elif isinstance(node, ast.BinOp):
                return ops[type(node.op)](eval_expr(node.left), eval_expr(node.right))
            elif isinstance(node, ast.UnaryOp):
                return ops[type(node.op)](eval_expr(node.operand))
            else:
                raise ValueError(f"Unsupported operation: {type(node)}")

        tree = ast.parse(expression, mode='eval')
        result = eval_expr(tree.body)

        return {
            "expression": expression,
            "result": result,
            "success": True
        }

    except Exception as e:
        return {
            "expression": expression,
            "error": str(e),
            "success": False
        }

async def get_current_context() -> Dict[str, Any]:
    """
    Récupère le contexte actuel de l'agent.

    Returns:
        Informations sur le contexte
    """
    logger.info("Getting current context")

    return {
        "status": "active",
        "memory_size": 10,
        "conversation_turns": 5,
        "capabilities": [
            "text_generation",
            "reasoning",
            "memory_search",
            "sentiment_analysis"
        ]
    }
