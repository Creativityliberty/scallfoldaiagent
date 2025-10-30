from ..core.base_node import BaseNode
from ..core.shared import Shared
from typing import Dict, Any, List

class MemoryNode(BaseNode):
    """
    Module 4: Mémoire
    Gère la recherche et le stockage en mémoire.
    (Implémentation simplifiée - à enrichir avec vector store)
    """

    def __init__(self) -> None:
        super().__init__("memory")
        self.short_term_memory: List[Dict[str, Any]] = []
        self.max_memory_size = 10

    def prep(self, shared: Shared) -> Dict[str, Any]:
        """Récupère le contexte pour la recherche mémoire."""
        return {
            "query": shared.get_result("perception", "clean_input"),
            "intent": shared.get_result("interpretation", "intent")
        }

    async def exec(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Recherche dans la mémoire."""
        query = input_data.get("query", "")

        # Recherche simple (à améliorer avec embedding similarity)
        relevant_memories = self._search(query)

        return {
            "relevant_contexts": relevant_memories,
            "memory_size": len(self.short_term_memory),
            "search_query": query
        }

    def post(self, shared: Shared, prep_result: Any, exec_result: Any) -> str | None:
        """Stocke l'interaction en mémoire."""
        super().post(shared, prep_result, exec_result)

        # Ajoute à la mémoire court terme
        interaction = {
            "query": prep_result.get("query", ""),
            "intent": prep_result.get("intent", ""),
            "timestamp": shared.get_metadata("start_time")
        }

        self.short_term_memory.append(interaction)

        # Limite la taille
        if len(self.short_term_memory) > self.max_memory_size:
            self.short_term_memory = self.short_term_memory[-self.max_memory_size:]

        # Met à jour le contexte partagé
        shared.set_context("memory_snapshot", self.short_term_memory)

        return None

    def _search(self, query: str) -> List[Dict[str, Any]]:
        """Recherche basique par mots-clés."""
        if not query:
            return []

        query_lower = query.lower()
        results = []

        for memory in self.short_term_memory:
            memory_query = memory.get("query", "").lower()
            if any(word in memory_query for word in query_lower.split()):
                results.append(memory)

        return results[-3:]  # Top 3 plus récents
