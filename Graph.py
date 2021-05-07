from queue import Queue
import heapq
from typing import Dict
from math import inf

from PyQt5.QtWidgets import QWidget

from Node import Node

"""
Adapted from http://theory.stanford.edu/~amitp/GameProgramming/#pathfinding
"""


class Graph:
    def __init__(self, columns: int, rows: int):
        self.columns = columns
        self.rows = rows
        self.barriers = []
        self.weights = {}

    """
    ##########################################################################
                                Public Functions
    ##########################################################################
    """
    def in_bounds(self, node: Node) -> bool:
        return 0 <= node.x < self.columns and 0 <= node.y < self.rows

    def is_passable(self, node: Node) -> bool:
        return node not in self.barriers

    def neighbors(self, node: Node):
        x = node.x
        y = node.y
        neighbors_list = [Node(x + 1, y), Node(x - 1, y), Node(x, y + 1), Node(x, y - 1)]  # E W N S
        if (x + y) % 2 == 0: neighbors_list.reverse()  # S N W E
        results = filter(self.in_bounds, neighbors_list)
        results = filter(self.is_passable, results)
        return results

    # cost only accounts for weight from the to_node
    def cost(self, from_node: Node, to_node: Node) -> float:
        return self.weights.get(to_node, 1)

    def bfs(self, start: Node, end: Node, grid: QWidget) -> []:
        frontier = Queue()
        frontier.put(start)
        grid.add_frontier(start)
        came_from = dict()
        came_from[start] = None

        while not frontier.empty():
            current = frontier.get()
            grid.remove_frontier(current)

            if current == end:
                break

            for next in self.neighbors(current):
                if next not in came_from:
                    frontier.put(next)
                    came_from[next] = current

                    grid.add_frontier(next)
                    grid.repaint()

        return self.reconstruct_path(came_from, start, end)

    def a_star(self, start: Node, end: Node, grid: QWidget) -> []:
        frontier = PriorityQueue()
        frontier.put(start, 0)
        grid.add_frontier(start)
        came_from = dict()
        cost_so_far = dict()
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()
            grid.remove_frontier(current)

            if current == end:
                break

            for next in self.neighbors(current):
                new_cost = cost_so_far[current] + self.cost(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(next, end)
                    frontier.put(next, priority)
                    came_from[next] = current

                    grid.add_frontier(next)
                    grid.repaint()

        return self.reconstruct_path(came_from, start, end)

    def dijkstra(self, start: Node, end: Node, grid: QWidget) -> []:
        frontier = PriorityQueue()
        frontier.put(start, 0)
        grid.add_frontier(start)
        came_from = dict()
        cost_so_far = dict()
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()
            grid.remove_frontier(current)

            if current == end:
                break

            for next in self.neighbors(current):
                new_cost = cost_so_far[current] + self.cost(current, next)
                if new_cost < cost_so_far.get(next, inf):
                    cost_so_far[next] = new_cost
                    priority = new_cost
                    frontier.put(next, priority)
                    came_from[next] = current

                    grid.add_frontier(next)
                    grid.repaint()

        return self.reconstruct_path(came_from, start, end)

    """
    ##########################################################################
                                Static Functions
    ##########################################################################
    """
    @staticmethod
    def heuristic(n1: Node, n2: Node) -> float:
        (x1, y1) = n1.get_coordinates()
        (x2, y2) = n2.get_coordinates()
        return abs(x1 - x2) + abs(y1 - y2)

    @staticmethod
    def reconstruct_path(came_from: Dict[Node, Node], start: Node, end: Node) -> []:
        current = end
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.reverse()

        try:
            path.remove(end)
        except ValueError:
            pass

        return path


class PriorityQueue:
    def __init__(self):
        self.elements = []

    """
    ##########################################################################
                                Public Functions
    ##########################################################################
    """

    def empty(self) -> bool:
        return not self.elements

    def put(self, item, priority: float):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]
