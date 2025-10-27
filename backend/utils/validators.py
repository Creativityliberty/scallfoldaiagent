from ..core.shared import Shared

def validate_shared(shared: Shared) -> bool:
    return isinstance(shared, Shared) and "context" in shared and "results" in shared
