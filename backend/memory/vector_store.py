import os
from typing import List, Dict, Tuple

class VectorStore:
    """Vector store with optional dependencies for compatibility."""

    def __init__(self, dim: int = 768):
        self.dim = dim
        self.docs: List[str] = []
        self._initialized = False

        # Check optional dependencies
        try:
            import faiss  # noqa
            import numpy as np  # noqa
            self._faiss_available = True
            self._numpy_available = True
        except ImportError:
            self._faiss_available = False
            self._numpy_available = False

        # Check sentence-transformers (now optional)
        try:
            import sentence_transformers  # noqa
            self._sentence_transformers_available = True
        except ImportError:
            self._sentence_transformers_available = False

    def add_texts(self, texts: List[str]) -> None:
        """Add texts to the store."""
        if not self._faiss_available:
            # Fallback: just store as simple list
            self.docs.extend(texts)
            return

        # TODO: Implement FAISS indexing when available
        self.docs.extend(texts)

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for similar texts."""
        if not self._faiss_available:
            # Fallback: return first few docs
            return [{"content": d, "score": 0.5} for d in self.docs[:top_k]]

        # TODO: Implement FAISS search when available
        return [{"content": d, "score": 0.5} for d in self.docs[:top_k]]

    def is_available(self) -> bool:
        """Check if advanced features are available."""
        return self._faiss_available

    def has_embeddings(self) -> bool:
        """Check if sentence-transformers is available for embeddings."""
        return self._sentence_transformers_available
