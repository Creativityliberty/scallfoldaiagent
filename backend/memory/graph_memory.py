from typing import Dict, List, Any, Tuple
import networkx as nx
from loguru import logger
from datetime import datetime

class GraphMemory:
    """
    Graphe morphique de mémoire.
    Stocke les relations pondérées entre concepts/entités.
    """

    def __init__(self):
        self.graph = nx.DiGraph()
        logger.info("GraphMemory initialized")

    def add_node(self, node_id: str, node_type: str, data: Dict[str, Any] | None = None) -> None:
        """Ajoute un nœud au graphe."""
        self.graph.add_node(
            node_id,
            type=node_type,
            data=data or {},
            created_at=datetime.now().isoformat()
        )
        logger.debug(f"Added node: {node_id} (type={node_type})")

    def add_edge(
        self,
        source: str,
        target: str,
        relation: str,
        weight: float = 1.0,
        metadata: Dict[str, Any] | None = None
    ) -> None:
        """Ajoute une arête entre deux nœuds."""
        # Crée les nœuds s'ils n'existent pas
        if not self.graph.has_node(source):
            self.add_node(source, "unknown")
        if not self.graph.has_node(target):
            self.add_node(target, "unknown")

        self.graph.add_edge(
            source,
            target,
            relation=relation,
            weight=weight,
            metadata=metadata or {},
            created_at=datetime.now().isoformat()
        )
        logger.debug(f"Added edge: {source} --[{relation}]--> {target} (weight={weight})")

    def strengthen_edge(self, source: str, target: str, delta: float = 0.1) -> None:
        """Renforce une relation existante (apprentissage morphique)."""
        if self.graph.has_edge(source, target):
            current_weight = self.graph[source][target].get("weight", 1.0)
            new_weight = min(current_weight + delta, 1.0)
            self.graph[source][target]["weight"] = new_weight
            logger.debug(f"Strengthened edge {source}->{target}: {current_weight:.2f} -> {new_weight:.2f}")

    def get_neighbors(self, node_id: str, relation: str | None = None) -> List[Tuple[str, Dict[str, Any]]]:
        """Récupère les voisins d'un nœud."""
        if not self.graph.has_node(node_id):
            return []

        neighbors = []
        for neighbor in self.graph.successors(node_id):
            edge_data = self.graph[node_id][neighbor]

            if relation is None or edge_data.get("relation") == relation:
                neighbors.append((neighbor, edge_data))

        # Trie par poids décroissant
        neighbors.sort(key=lambda x: x[1].get("weight", 0), reverse=True)
        return neighbors

    def find_path(self, source: str, target: str) -> List[str] | None:
        """Trouve le chemin le plus court entre deux nœuds."""
        try:
            path = nx.shortest_path(self.graph, source, target)
            return path
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return None

    def get_related_concepts(self, node_id: str, max_depth: int = 2) -> List[Dict[str, Any]]:
        """Récupère les concepts liés à un nœud (BFS)."""
        if not self.graph.has_node(node_id):
            return []

        visited = set()
        queue = [(node_id, 0)]
        results = []

        while queue:
            current, depth = queue.pop(0)

            if current in visited or depth > max_depth:
                continue

            visited.add(current)

            if current != node_id:
                node_data = self.graph.nodes[current]
                results.append({
                    "node_id": current,
                    "type": node_data.get("type", "unknown"),
                    "depth": depth,
                    "data": node_data.get("data", {})
                })

            # Ajoute les voisins à la queue
            for neighbor in self.graph.successors(current):
                if neighbor not in visited:
                    queue.append((neighbor, depth + 1))

        return results

    def get_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques du graphe."""
        return {
            "nodes": self.graph.number_of_nodes(),
            "edges": self.graph.number_of_edges(),
            "density": nx.density(self.graph) if self.graph.number_of_nodes() > 0 else 0,
            "is_connected": nx.is_weakly_connected(self.graph) if self.graph.number_of_nodes() > 0 else False
        }

    def export_graphml(self, filepath: str) -> None:
        """Exporte le graphe au format GraphML."""
        nx.write_graphml(self.graph, filepath)
        logger.info(f"Graph exported to {filepath}")

    def clear(self) -> None:
        """Vide le graphe."""
        self.graph.clear()
        logger.info("Graph memory cleared")
