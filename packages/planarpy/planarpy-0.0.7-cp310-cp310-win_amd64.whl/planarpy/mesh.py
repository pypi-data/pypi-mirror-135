from typing import List, Tuple, NamedTuple, Dict, Set, Callable
from math import nan


def lines(nodes):
    [n0, n1, n2] = nodes
    return (n0, n1), (n0, n2), (n1, n2)


class Edge(NamedTuple):
    pow: int
    adj_list: Set[int]


class Cell(NamedTuple):
    nodes: List[int]
    pow: Tuple[int, int]


class Group:
    id: int
    nodes: Set[int]
    edges: Set[Tuple[int, int]]
    cells: Set[int]

    def __init__(self, id, nodes, edges, cells):
        self.id, self.nodes, self.edges, self.cells = id, nodes, edges, cells

    def plot_group(self, mesh) -> Tuple[List[float], List[float], List[float]]:
        x, y, z = [], [], []
        for [n0, n1] in self.edges:
            [x0, y0], [x1, y1] = mesh.pts[n0], mesh.pts[n1]
            x.extend([x0, x1, nan])
            y.extend([y0, y1, nan])
            z.extend([0., 0., nan])
        return x, y, z


class Mesh:
    pts: List[Tuple[float, float]]
    edges: Dict[Tuple[int, int], Edge]
    cells: List[Cell]
    groups: int

    def __init__(self, pts: List[Tuple[float, float]], triangles: List[List[int]], pow: int, rcm: bool = False):
        if rcm:
            graph = rcm_graph(len(pts), triangles)
            pts = [pts[node] for node in graph]
            triangles = [[graph[n0], graph[n1], graph[n2]] for n0, n1, n2 in triangles]
        cells = []
        edges = {}
        for idx, nodes in enumerate(triangles):
            nodes.sort()
            for line in lines(nodes):
                if line not in edges:
                    edges[line] = Edge(pow, set())
                edges[line].adj_list.add(idx)
            cells.append(Cell(nodes, (pow, pow)))
        cells.sort(key=lambda cell: cell[0])
        self.pts, self.edges, self.cells, self.groups = pts, edges, cells, 0

    def def_group(self, cond: Callable[[float, float], bool]):
        self.groups += 1
        id, nodes, edges, cells = self.groups, set(), set(), set()
        for ver, [x, y] in enumerate(self.pts):
            if cond(x, y):
                nodes.add(ver)
        for (n0, n1) in self.edges:
            if n0 in nodes and n1 in nodes:
                edges.add((n0, n1))
        for idx, ((n0, n1, n2), _) in enumerate(self.cells):
            if n0 in nodes and n1 in nodes and n2 in nodes:
                cells.add(idx)
        return Group(id, nodes, edges, cells)

    def adapt_p(self, group: Group, pow: int):
        limit = {}
        for idx in group.cells:
            nodes = self.cells[idx].nodes
            for line in lines(nodes):
                if line not in limit:
                    limit[line] = set()
                limit[line].add(idx)
        limit = {nodes: elems.pop() for nodes, elems in limit.items() if len(elems) < 2}
        limit = {elem: nodes for nodes, elem in limit.items() if len(self.edges[nodes].adj_list) > 1}
        for idx, (n0, n1) in limit.items():
            nodes, (_, trans) = self.cells[idx]
            nodes = [n0, n1, (set(nodes) - {n0, n1}).pop()]
            self.cells[idx] = Cell(nodes, (pow, trans))
        for idx in group.cells - limit.keys():
            nodes = self.cells[idx].nodes
            self.cells[idx] = Cell(nodes, (pow, pow))
        for edge in group.edges - {edge for _, edge in limit.items()}:
            adj_list = self.edges[edge].adj_list
            self.edges[edge] = Edge(pow, adj_list)

    def plot_sys(self) -> Dict[int, Tuple[List[float], List[float], List[float]]]:
        pows = {}
        for (n0, n1), (pow, _) in self.edges.items():
            [x0, y0], [x1, y1] = self.pts[n0], self.pts[n1]
            if pow not in pows:
                pows[pow] = [], [], []
            pows[pow][0].extend([x0, x1, nan])
            pows[pow][1].extend([y0, y1, nan])
            pows[pow][2].extend([0., 0., nan])
        return pows


def rcm_graph(size: int, cells: List[List[int]]) -> Dict[int, int]:
    adj_list = {}
    for nodes in cells:
        for node in nodes:
            if node not in adj_list:
                adj_list[node] = set()
            for adj_node in nodes:
                if adj_node != node:
                    adj_list[node].add(adj_node)
    start = min([(len(adj_nodes), node) for node, adj_nodes in adj_list.items()])[1]
    graph = [start]
    used = {start}
    for idx in range(0, size):
        node = graph[idx]
        next_nodes = [(len(adj_list[n]), n) for n in adj_list[node]]
        next_nodes.sort()
        for (_, n) in next_nodes:
            if n not in used:
                graph.append(n)
                used.add(n)
    graph.reverse()
    return {node: idx for idx, node in enumerate(graph)}
