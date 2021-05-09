from node import Node


class Grid:
    def __init__(self):
        self.visualize = True
        self.default_weight = 1
        self.forest_weight = 2
        self.desert_weight = 3
        self.barrier_nodes = set()
        self.desert_nodes = set()
        self.forest_nodes = set()
        self.startpoint_node = Node(0, 0)
        self.endpoint_node = Node(39, 29)
        self.path_nodes = set()
        self.frontier_nodes = set()

    def add_forest_node(self, node: Node) -> None:
        self.forest_nodes.add(node)

    def add_desert_node(self, node) -> None:
        self.desert_nodes.add(node)

    def add_barrier_node(self, node) -> None:
        self.barrier_nodes.add(node)

    def add_path_node(self, node) -> None:
        self.path_nodes.add(node)

    def add_frontier_node(self, node: Node):
        self.frontier_nodes.add(node)

    def remove_frontier_node(self, node: Node):
        self.frontier_nodes.remove(node)

    def remove_terrain_nodes(self, node: Node):
        for terrain in self.barrier_nodes, self.desert_nodes, self.forest_nodes:
            try:
                terrain.remove(node)
            except KeyError:
                pass

    def clear_terrain_nodes(self):
        for terrain in self.barrier_nodes, self.desert_nodes, self.forest_nodes:
            terrain.clear()
