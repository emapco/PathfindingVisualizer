from dataclasses import dataclass, astuple


@dataclass(frozen=True, order=True)
class Node:
    x: int
    y: int

    """
    ##########################################################################
                                Public Functions
    ##########################################################################
    """
    def get_coordinates(self) -> (int, int):
        return astuple(self)


if __name__ == '__main__':
    node = Node(0, 0)
    node1 = Node(0, 1)
    node2 = Node(0, 0)
    node4 = Node(1, 1)
    print(node1 < node4)
