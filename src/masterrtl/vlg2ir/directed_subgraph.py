from collections import defaultdict

from .directed_graph_subnode import DirectedGraphSubNode as SubNode


class subGraph:
    def __init__(self, name, children, type, width=None, delay=0):
        self.graph = defaultdict(list)
        self.node_dict = {}
        self.start = name
        self.end_set = set()
        self.add_decl_node(name, type, width, delay)
        for c in children:
            self.add_edge(name, c)

    def add_decl_node(self, name, type, width=None, delay=0):
        node = SubNode(name, type, width, delay)
        self.node_dict[name] = node

    def add_edge(self, u, v):
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append(v)
