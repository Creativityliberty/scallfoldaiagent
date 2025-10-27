class GraphMemory:
    """Placeholder pour mémoire graphe."""
    def __init__(self):
        self.nodes = {}
        self.edges = []
    
    def add_relation(self, a: str, b: str, weight: float = 1.0):
        self.edges.append((a, b, weight))
