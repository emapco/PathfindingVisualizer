from queue import Queue
import heapq
from typing import Dict
from math import inf

from PyQt5.QtWidgets import QWidget

from node import Node

"""
Adapted from http://theory.stanford.edu/~amitp/GameProgramming/#pathfinding
"""


class Graph:
    def __init__(self, columns: int, rows: int):
        self.columns = columns
        self.rows = rows
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

    def neighbors(self, node: Node):
        x = node.x
        y = node.y
        neighbors_list = [Node(x + 1, y), Node(x - 1, y), Node(x, y + 1), Node(x, y - 1)]  # E W N S
        if (x + y) % 2 == 0: neighbors_list.reverse()  # S N W E
        results = filter(self.in_bounds, neighbors_list)
        results = filter(self.is_passable, results)
        return results

    def in_bounds(self, node: Node) -> bool:
        return 0 <= node.x < self.columns and 0 <= node.y < self.rows

    def is_passable(self, node: Node) -> bool:
        return node not in self.barrier_nodes

    def bfs(self, start: Node, end: Node, grid: QWidget) -> []:
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

            for next in self.neighbors(current):
                if next not in came_from:
                    frontier.put(next)
                    came_from[next] = current

                    self.frontier_nodes.add(next)
                    grid.repaint_grid()

        return self.reconstruct_path(came_from, start, end)

    def add_barrier_node(self, node) -> None:
        self.barrier_nodes.add(node)

    def remove_frontier_node(self, node) -> None:
        try:
            self.frontier_nodes.remove(node)
        except KeyError:
            pass

    def clear_path_nodes(self):
        self.path_nodes.clear()

    def clear_frontier_nodes(self):
        self.frontier_nodes.clear()

    def reconstruct_path(self, came_from: Dict[Node, Node], start: Node, end: Node) -> None:
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


class WeightedGraph(Graph):
    def __init__(self, columns: int, rows: int):
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

    def a_star(self, start: Node, end: Node, grid: QWidget) -> []:
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

            for next in self.neighbors(current):
                new_cost = cost_so_far[current] + self.cost(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(next, end)
                    frontier.put(next, priority)
                    came_from[next] = current

                    self.frontier_nodes.add(next)
                    grid.repaint_grid()

        return self.reconstruct_path(came_from, start, end)

    def dijkstra(self, start: Node, end: Node, grid: QWidget) -> []:
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

            for next in self.neighbors(current):
                new_cost = cost_so_far[current] + self.cost(current, next)
                if new_cost < cost_so_far.get(next, inf):
                    cost_so_far[next] = new_cost
                    priority = new_cost
                    frontier.put(next, priority)
                    came_from[next] = current

                    self.frontier_nodes.add(next)
                    grid.repaint_grid()

        return self.reconstruct_path(came_from, start, end)

    # cost only accounts for weight from the to_node
    def cost(self, from_node: Node, to_node: Node) -> float:
        weight = self.default_weight
        if to_node in self.forest_nodes:
            weight = self.forest_weight
        if to_node in self.desert_nodes:
            weight = self.desert_weight
        return weight

    def add_forest_node(self, node: Node) -> None:
        self.forest_nodes.add(node)

    def add_desert_node(self, node) -> None:
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
                                Static Functions
    ##########################################################################
    """
    @staticmethod
    def heuristic(n1: Node, n2: Node) -> float:
        x1, y1 = n1.get_coordinates()
        x2, y2 = n2.get_coordinates()
        return abs(x1 - x2) + abs(y1 - y2)


class PriorityQueue:
    def __init__(self):
        self.elements: list = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item, priority: float):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


if __name__ == "__main__":
    pq = PriorityQueue()
