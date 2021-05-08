from dataclasses import dataclass
from typing import Union

DESERT_WEIGHT = 3
FOREST_WEIGHT = 2


class Node:
    def __init__(self, x: int, y: int, weight=1):
        self._x = x
        self._y = y
        self._weight = weight

    """
    ##########################################################################
                                Public Functions
    ##########################################################################
    """

    def get_coordinates(self) -> (int, int):
        return self._x, self._y

    """
    ##########################################################################
                                Properties
    ##########################################################################
    """

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def weight(self) -> int:
        return self._weight

    @weight.setter
    def weight(self, value):
        self._weight = value


    """
    ##########################################################################
                                Built-In Functions
    ##########################################################################
    """

    def __str__(self) -> str:
        return f'Node({self._x},{self._y})'

    def __repr__(self) -> str:
        return self.__str__()

    def __key(self) -> (int, int):
        return self._x, self._y

    def __hash__(self) -> hash:
        return hash(self.__key())

    def __eq__(self, other) -> Union[bool, type(NotImplemented)]:
        if isinstance(other, Node):
            return self.__key() == other.__key()
        return NotImplemented

    def __lt__(self, other) -> Union[bool, type(NotImplemented)]:
        if isinstance(other, Node):
            return sum(self.get_coordinates()) < sum(other.get_coordinates())
        return NotImplemented

    def __gt__(self, other) -> Union[bool, type(NotImplemented)]:
        if isinstance(other, Node):
            return sum(self.get_coordinates()) < sum(other.get_coordinates())
        return NotImplemented

    def __le__(self, other) -> Union[bool, type(NotImplemented)]:
        if isinstance(other, Node):
            return sum(self.get_coordinates()) <= sum(other.get_coordinates())
        return NotImplemented

    def __ge__(self, other) -> Union[bool, type(NotImplemented)]:
        if isinstance(other, Node):
            return sum(self.get_coordinates()) >= sum(other.get_coordinates())
        return NotImplemented
