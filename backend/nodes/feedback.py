from ..core.base_node import BaseNode
from ..core.shared import Shared
from typing import Dict, Any
from loguru import logger

class FeedbackNode(BaseNode):
    """
    Module 7: Feedback
    Collecte et analyse le feedback pour l'amélioration continue.
    """

    def __init__(self) -> None:
        super().__init__("feedback")
        self.feedback_log: list[Dict[str, Any]] = []

    async def exec(self, input_data: Any) -> Dict[str, Any]:
        """Traite le feedback utilisateur."""
        # Pour l'instant, pas de feedback actif dans le flow principal
        return {
            "feedback_collected": False,
            "total_feedback": len(self.feedback_log)
        }

    def collect_feedback(
        self,
        flow_id: str,
        rating: int,
        comment: str = ""
    ) -> None:
        """Collecte le feedback utilisateur."""
        feedback = {
            "flow_id": flow_id,
            "rating": rating,
            "comment": comment,
            "timestamp": None  # Ajouter timestamp
        }

        self.feedback_log.append(feedback)
        logger.info(f"Feedback collected for flow {flow_id}: {rating}/5")

    def get_statistics(self) -> Dict[str, Any]:
        """Statistiques sur le feedback."""
        if not self.feedback_log:
            return {"total": 0, "average_rating": 0}

        total = len(self.feedback_log)
        avg_rating = sum(f["rating"] for f in self.feedback_log) / total

        return {
            "total": total,
            "average_rating": avg_rating,
            "distribution": self._rating_distribution()
        }

    def _rating_distribution(self) -> Dict[int, int]:
        """Distribution des ratings."""
        distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

        for feedback in self.feedback_log:
            rating = feedback.get("rating", 0)
            if rating in distribution:
                distribution[rating] += 1

        return distribution
