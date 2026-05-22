import networkx as nx


class PathFinder:
    def shortest_path(self, edges: list[tuple[str, str]], source: str, target: str) -> list[str]:
        graph = nx.Graph()
        graph.add_edges_from(edges)
        return nx.shortest_path(graph, source=source, target=target)
