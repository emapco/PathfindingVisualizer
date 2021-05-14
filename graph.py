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
        self._columns = columns
        self._rows = rows
        self._startpoint_node: Node = Node(0, 0)
        self._endpoint_node: Node = Node(39, 29)
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

    def bfs(self, start: Node, end: Node) -> None:
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

            for next in self.neighbors(current):
                if next not in came_from:
                    frontier.put(next)
                    came_from[next] = current

                    self.frontier_nodes.add(next)
                    self._sleep()

        self._reconstruct_path(came_from, start, end)
        self.clear_frontier_nodes()

    def add_barrier_node(self, node) -> None:
        self.barrier_nodes.add(node)

    def remove_frontier_node(self, node) -> None:
        try:
            self.frontier_nodes.remove(node)
        except KeyError:
            pass

    def clear_path_nodes(self) -> None:
        self.path_nodes.clear()

    def clear_frontier_nodes(self) -> None:
        self.frontier_nodes.clear()

    def _reconstruct_path(self, came_from: Dict[Node, Node], start: Node, end: Node) -> None:
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

    @staticmethod
    def _sleep():
        n = random()
        if n >= 0.90:
            sleep(0.001)
    """
    ##########################################################################
                                PROPERTIES
    ##########################################################################
    """
    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, value: int):
        self._columns = value

    @property
    def rows(self):
        return self._rows

    @rows.setter
    def rows(self, value: int):
        self._rows = value

    @property
    def startpoint_node(self):
        return self._startpoint_node

    @startpoint_node.setter
    def startpoint_node(self, value: Node):
        self._startpoint_node = value

    @property
    def endpoint_node(self):
        return self._endpoint_node

    @endpoint_node.setter
    def endpoint_node(self, value: Node):
        self._endpoint_node = value


class WeightedGraph(Graph):
    def __init__(self, columns: int, rows: int):
        super().__init__(columns, rows)
        self.forest_nodes = set()
        self.desert_nodes = set()
        self._default_weight: float = 1
        self._forest_weight: float = 2
        self._desert_weight: float = 3

    """
    ##########################################################################
                                Public Functions
    ##########################################################################
    """

    def a_star(self, start: Node, end: Node) -> []:
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

            for next in self.neighbors(current):
                new_cost = cost_so_far[current] + self._cost(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self._heuristic(next, end)
                    frontier.put(next, priority)
                    came_from[next] = current

                    self.frontier_nodes.add(next)
                    self._sleep()


        self._reconstruct_path(came_from, start, end)
        self.clear_frontier_nodes()

    def dijkstra(self, start: Node, end: Node) -> []:
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

            for next in self.neighbors(current):
                new_cost = cost_so_far[current] + self._cost(current, next)
                if new_cost < cost_so_far.get(next, inf):
                    cost_so_far[next] = new_cost
                    priority = new_cost
                    frontier.put(next, priority)
                    came_from[next] = current

                    self.frontier_nodes.add(next)
                    self._sleep()

        self._reconstruct_path(came_from, start, end)
        self.clear_frontier_nodes()

    # cost only accounts for weight from the to_node
    def _cost(self, from_node: Node, to_node: Node) -> float:
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
                                PROPERTIES
    ##########################################################################
    """
    @property
    def default_weight(self):
        return self._default_weight

    @default_weight.setter
    def default_weight(self, value: float):
        self._default_weight = value

    @property
    def forest_weight(self):
        return self._forest_weight

    @forest_weight.setter
    def forest_weight(self, value: float):
        self._forest_weight = value

    @property
    def desert_weight(self):
        return self._desert_weight

    @desert_weight.setter
    def desert_weight(self, value: float):
        self._desert_weight = value

    """
    ##########################################################################
                                Static Functions
    ##########################################################################
    """
    @staticmethod
    def _heuristic(n1: Node, n2: Node) -> float:
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
