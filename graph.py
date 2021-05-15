from queue import Queue
import heapq
from random import random
from time import sleep
from typing import Dict
from math import inf

from node import Node

"""
Adapted from http://theory.stanford.edu/~amitp/GameProgramming/#pathfinding
"""


class Graph:
    def __init__(self, columns: int, rows: int):
        """
        Initiator

        Parameters:
        -----------
        columns: int
            The number of columns in the graph
        rows: int
            The number of rows in the graph
        """
        self.columns = columns
        self.rows = rows
        self.visualize_algorithm = True
        self.startpoint_node: Node = Node(0, 0)
        self.endpoint_node: Node = Node(39, 29)
        self.frontier_nodes: set = set()
        self.barrier_nodes: set = set()
        self.path_nodes: list = []

    """
    ##########################################################################
                                Public Functions
    ##########################################################################
    """
    def bfs(self, start: Node, end: Node) -> None:
        """
        Public function used to generate path from start to end using
        Breadth-First-Search algorithm.

        Parameters:
        -----------
        start : Node
            The node that the algorithm starts from
        end : Node
            The node that the algorithm ends at
        """
        self.clear_path_nodes()
        frontier = Queue()
        frontier.put(start)
        came_from = dict()
        came_from[start] = None
        self.frontier_nodes.add(start)

        while not frontier.empty():
            current = frontier.get()
            self.remove_frontier_node(current)

            if current == end:
                break

            for next in self._neighbors(current):
                if next not in came_from:
                    frontier.put(next)
                    came_from[next] = current

                    self.frontier_nodes.add(next)
                    self._sleep()

        self._reconstruct_path(came_from, start, end)

    def add_barrier_node(self, node: Node) -> None:
        self.barrier_nodes.add(node)

    def remove_frontier_node(self, node: Node) -> None:
        try:
            self.frontier_nodes.remove(node)
        except KeyError:
            pass

    def clear_path_nodes(self) -> None:
        self.path_nodes.clear()

    def clear_frontier_nodes(self) -> None:
        self.frontier_nodes.clear()

    """
    ##########################################################################
                                Private Functions
    ##########################################################################
    """
    def _neighbors(self, node: Node):
        """
        Private function used to filter which neighboring nodes are valid.
        """
        x = node.x
        y = node.y
        neighbors_list = [Node(x + 1, y), Node(x - 1, y), Node(x, y + 1), Node(x, y - 1)]  # E W N S
        if (x + y) % 2 == 0: neighbors_list.reverse()  # S N W E
        results = filter(self._in_bounds, neighbors_list)
        results = filter(self._is_passable, results)
        return results

    def _in_bounds(self, node: Node) -> bool:
        """
        Private function used to determine if node is in the bounds of the graph
        """
        return 0 <= node.x < self.columns and 0 <= node.y < self.rows

    def _is_passable(self, node: Node) -> bool:
        """
        Private function used to determine if node is accessible
        """
        return node not in self.barrier_nodes

    def _reconstruct_path(self, came_from: Dict[Node, Node], start: Node, end: Node) -> None:
        """
        Private function used to construct the path from a pathfinding algorithm output
        """
        self.clear_frontier_nodes()
        current = end
        try:
            while current != start:
                self.path_nodes.append(current)
                current = came_from[current]
            self.path_nodes.reverse()
        except KeyError:
            pass

        try:
            self.path_nodes.remove(end)
        except ValueError:
            pass

    def _sleep(self) -> None:
        """
        Private function used to halt the program so the UI can update
        """
        if self.visualize_algorithm:
            length = len(self.frontier_nodes)
            threshold = 0.80
            if length > 10:
                threshold = 0.91
            elif length > 20:
                threshold = 0.96

            if random() >= threshold:
                sleep(0.001)


class WeightedGraph(Graph):
    def __init__(self, columns: int, rows: int):
        """
        Initiator

        Parameters:
        -----------
        columns: int
            The number of columns in the graph
        rows: int
            The number of rows in the graph
        """
        super().__init__(columns, rows)
        self.forest_nodes = set()
        self.desert_nodes = set()
        self.default_weight: float = 1
        self.forest_weight: float = 2
        self.desert_weight: float = 3

    """
    ##########################################################################
                                Public Functions
    ##########################################################################
    """
    def a_star(self, start: Node, end: Node) -> None:
        """
        Public function used to generate path from start to end using
        A* algorithm.

        Parameters:
        -----------
        start : Node
            The node that the algorithm starts from
        end : Node
            The node that the algorithm ends at
        """
        self.clear_path_nodes()
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = dict()
        cost_so_far = dict()
        came_from[start] = None
        cost_so_far[start] = 0
        self.frontier_nodes.add(start)

        while not frontier.empty():
            current = frontier.get()
            self.remove_frontier_node(current)

            if current == end:
                break

            for next in self._neighbors(current):
                new_cost = cost_so_far[current] + self._cost(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self._heuristic(next, end)
                    frontier.put(next, priority)
                    came_from[next] = current

                    self.frontier_nodes.add(next)
                    self._sleep()

        self._reconstruct_path(came_from, start, end)

    def dijkstra(self, start: Node, end: Node) -> None:
        """
        Public function used to generate path from start to end using
        Dijkstra's algorithm.

        Parameters:
        -----------
        start : Node
            The node that the algorithm starts from
        end : Node
            The node that the algorithm ends at
        """
        self.clear_path_nodes()
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = dict()
        cost_so_far = dict()
        came_from[start] = None
        cost_so_far[start] = 0
        self.frontier_nodes.add(start)

        while not frontier.empty():
            current = frontier.get()
            self.remove_frontier_node(current)

            if current == end:
                break

            for next in self._neighbors(current):
                new_cost = cost_so_far[current] + self._cost(current, next)
                if new_cost < cost_so_far.get(next, inf):
                    cost_so_far[next] = new_cost
                    priority = new_cost
                    frontier.put(next, priority)
                    came_from[next] = current

                    self.frontier_nodes.add(next)
                    self._sleep()

        self._reconstruct_path(came_from, start, end)

    def add_forest_node(self, node: Node) -> None:
        self.forest_nodes.add(node)

    def add_desert_node(self, node: Node) -> None:
        self.desert_nodes.add(node)

    def remove_terrain_nodes(self, node: Node) -> None:
        for terrain in self.barrier_nodes, self.desert_nodes, self.forest_nodes:
            try:
                terrain.remove(node)
            except KeyError:
                pass

    def clear_terrain_nodes(self) -> None:
        for terrain in self.barrier_nodes, self.desert_nodes, self.forest_nodes:
            terrain.clear()

    """
    ##########################################################################
                                Private Functions
    ##########################################################################
    """
    def _cost(self, from_node: Node, to_node: Node) -> float:
        """
        Private function used to determine the cost from from_node to to_node.
        Currently only determined by the to_node.
        """
        weight = self.default_weight
        if to_node in self.forest_nodes:
            weight = self.forest_weight
        if to_node in self.desert_nodes:
            weight = self.desert_weight
        return weight

    """
    ##########################################################################
                                Static Functions
    ##########################################################################
    """
    @staticmethod
    def _heuristic(n1: Node, n2: Node) -> float:
        """
         Private static function used to calculate
         the (Manhattan distance, L1) heuristic cost.
         -----------
         n1 : Node
             The url the request is being made to
         n2 : Node
             The parameters you want to pass in
         Returns:
         --------
         <value> : float
             The heuristic cost
        """
        x1, y1 = n1.get_coordinates()
        x2, y2 = n2.get_coordinates()
        return abs(x1 - x2) + abs(y1 - y2)


class PriorityQueue:
    def __init__(self):
        self.elements: list = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item, priority: float) -> None:
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


if __name__ == "__main__":
    pq = PriorityQueue()
