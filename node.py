from dataclasses import dataclass, astuple


@dataclass(frozen=True, order=True)
class Node:
    x: int
    y: int

    def get_coordinates(self) -> (int, int):
        """
        Public function used to return the node's x and y values as a tuple
        Returns:
        --------
        <value> : tuple
            tuple representation of the node's coordinates
        """
        return astuple(self)


if __name__ == '__main__':
    node = Node(0, 0)
    node1 = Node(0, 1)
    node2 = Node(0, 0)
    node4 = Node(1, 1)
    print(node1 < node4)
