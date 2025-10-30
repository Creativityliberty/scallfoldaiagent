from typing import Any, Dict, List
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum

class NodeStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class TraceEntry:
    timestamp: datetime
    node: str
    status: NodeStatus
    duration_ms: float
    data: Dict[str, Any] = field(default_factory=dict)

class Shared(dict):
    """
    Contract PocketFlow : Store partagé entre tous les nodes.
    Garantit la cohérence et la traçabilité du flow.
    """

    def __init__(self) -> None:
        super().__init__(
            context={},
            results={},
            trace=[],
            metadata={
                "flow_id": None,
                "user_id": None,
                "session_id": None,
                "start_time": datetime.now(),
            }
        )

    # Context methods
    def get_context(self, key: str, default: Any = None) -> Any:
        return self["context"].get(key, default)

    def set_context(self, key: str, value: Any) -> None:
        self["context"][key] = value

    def update_context(self, data: Dict[str, Any]) -> None:
        self["context"].update(data)

    # Results methods
    def get_result(self, node: str, key: str | None = None) -> Any:
        result = self["results"].get(node)
        if key and result:
            return result.get(key)
        return result

    def set_result(self, node: str, value: Any) -> None:
        self["results"][node] = value

    # Trace methods
    def add_trace(self, entry: TraceEntry) -> None:
        self["trace"].append(entry)

    def get_trace(self) -> List[TraceEntry]:
        return self["trace"]

    # Metadata
    def set_metadata(self, key: str, value: Any) -> None:
        self["metadata"][key] = value

    def get_metadata(self, key: str) -> Any:
        return self["metadata"].get(key)

    # Utilities
    def to_dict(self) -> Dict[str, Any]:
        return {
            "context": self["context"],
            "results": self["results"],
            "trace": [
                {
                    "timestamp": t.timestamp.isoformat(),
                    "node": t.node,
                    "status": t.status.value,
                    "duration_ms": t.duration_ms,
                    "data": t.data,
                }
                for t in self["trace"]
            ],
            "metadata": self["metadata"],
        }
