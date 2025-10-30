from typing import List, Dict, Any, Tuple
import numpy as np
from loguru import logger

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    logger.warning("FAISS not available, using simple similarity")

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    logger.warning("sentence-transformers not available, using dummy embeddings")

class VectorStore:
    """
    Store vectoriel pour recherche sémantique.
    Utilise FAISS + sentence-transformers pour les embeddings.
    """

    def __init__(self, dimension: int = 768):
        self.dimension = dimension
        self.documents: List[Dict[str, Any]] = []

        # Encoder pour les embeddings
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
            self.dimension = 384  # Dimension du modèle all-MiniLM-L6-v2
        else:
            self.encoder = None

        # Index FAISS
        if FAISS_AVAILABLE:
            self.index = faiss.IndexFlatL2(self.dimension)
        else:
            self.index = None
            self.vectors: List[np.ndarray] = []

        logger.info(f"VectorStore initialized (dim={self.dimension})")

    def _encode(self, text: str) -> np.ndarray:
        """Encode un texte en vecteur."""
        if self.encoder:
            return self.encoder.encode(text, convert_to_numpy=True)
        else:
            # Fallback: vecteur aléatoire (pour tests)
            return np.random.rand(self.dimension).astype('float32')

    def add(self, text: str, metadata: Dict[str, Any] | None = None) -> str:
        """Ajoute un document au store."""
        doc_id = f"doc_{len(self.documents)}"

        # Génère l'embedding
        vector = self._encode(text)

        # Stocke le document
        self.documents.append({
            "id": doc_id,
            "text": text,
            "metadata": metadata or {},
            "vector": vector
        })

        # Ajoute à l'index
        if self.index:
            self.index.add(vector.reshape(1, -1))
        else:
            self.vectors.append(vector)

        logger.debug(f"Added document {doc_id} to vector store")
        return doc_id

    def search(self, query: str, top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        """Recherche les documents les plus similaires."""
        if not self.documents:
            return []

        # Encode la query
        query_vector = self._encode(query)

        if self.index:
            # Recherche avec FAISS
            distances, indices = self.index.search(query_vector.reshape(1, -1), min(top_k, len(self.documents)))

            results = []
            for dist, idx in zip(distances[0], indices[0]):
                if idx < len(self.documents):
                    doc = self.documents[idx]
                    similarity = float(1.0 / (1.0 + dist))  # Convert distance to similarity
                    results.append((doc, similarity))

            return results
        else:
            # Fallback: calcul manuel de similarité cosine
            results = []
            for doc in self.documents:
                doc_vector = doc["vector"]
                similarity = self._cosine_similarity(query_vector, doc_vector)
                results.append((doc, float(similarity)))

            results.sort(key=lambda x: x[1], reverse=True)
            return results[:top_k]

    def _cosine_similarity(self, v1: np.ndarray, v2: np.ndarray) -> float:
        """Calcule la similarité cosine entre deux vecteurs."""
        dot = np.dot(v1, v2)
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot / (norm1 * norm2)

    def get_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques du store."""
        return {
            "total_documents": len(self.documents),
            "dimension": self.dimension,
            "faiss_available": FAISS_AVAILABLE,
            "encoder_available": SENTENCE_TRANSFORMERS_AVAILABLE
        }

    def clear(self) -> None:
        """Vide le store."""
        self.documents.clear()

        if self.index:
            self.index.reset()
        else:
            self.vectors.clear()

        logger.info("Vector store cleared")
