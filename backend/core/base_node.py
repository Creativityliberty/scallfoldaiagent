from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple
from .shared import Shared, TraceEntry, NodeStatus
from datetime import datetime
import time

class BaseNode(ABC):
    """
    Interface PocketFlow pour tous les nodes.
    Implémente le pattern prep -> exec -> post.
    """

    def __init__(self, name: str):
        self.name = name

    def prep(self, shared: Shared) -> Any:
        """Phase de préparation : lecture du contexte partagé."""
        return None

    @abstractmethod
    async def exec(self, input_data: Any) -> Any:
        """Phase d'exécution : logique métier du node."""
        pass

    def post(self, shared: Shared, prep_result: Any, exec_result: Any) -> str | None:
        """Phase post-exécution : écriture dans shared, routage."""
        shared.set_result(self.name, exec_result)
        return None  # Pas de routage spécial

    async def run(self, shared: Shared, input_data: Any = None) -> Tuple[Any, str | None]:
        """Execute le cycle complet prep -> exec -> post avec traçabilité."""
        start = time.perf_counter()

        try:
            # Prep
            prep_result = self.prep(shared)

            # Exec
            if input_data is None:
                input_data = prep_result
            exec_result = await self.exec(input_data)

            # Post
            next_route = self.post(shared, prep_result, exec_result)

            # Trace success
            duration = (time.perf_counter() - start) * 1000
            shared.add_trace(TraceEntry(
                timestamp=datetime.now(),
                node=self.name,
                status=NodeStatus.SUCCESS,
                duration_ms=duration,
                data={"has_result": exec_result is not None}
            ))

            return exec_result, next_route

        except Exception as e:
            duration = (time.perf_counter() - start) * 1000
            shared.add_trace(TraceEntry(
                timestamp=datetime.now(),
                node=self.name,
                status=NodeStatus.FAILED,
                duration_ms=duration,
                data={"error": str(e)}
            ))
            raise
