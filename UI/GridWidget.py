from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QRectF, QEvent, QPoint
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore

from node import Node


class GridUI(QWidget):
    def __init__(self, graph, columns, rows, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setMinimumSize(800, 600)
        self.columns = columns
        self.rows = rows
        self.graph = graph
        self.visualize_algorithm = True

    def resizeEvent(self, event) -> None:
        # compute the square size based on the aspect ratio, assuming that the
        # column and row numbers are fixed
        reference = self.width() * self.rows / self.columns
        if reference > self.height():
            # the window is larger than the aspect ratio
            # use the height as a reference (minus 1 pixel)
            self.square_size = (self.height() - 1) / self.rows
        else:
            # the opposite
            self.square_size = (self.width() - 1) / self.columns
        self.grid_width = self.square_size * self.columns
        self.grid_height = self.square_size * self.rows

    def paintEvent(self, event) -> None:
        qp = QPainter(self)
        qp.translate(.5, .5)  # translate the painter by half a pixel to ensure correct line painting
        qp.setRenderHints(qp.Antialiasing)

        # center the grid
        left = (self.width() - self.grid_width) / 2
        top = (self.height() - self.grid_height) / 2
        x, y = left, top
        # we need to add 1 to draw the topmost right/bottom lines too
        for row in range(self.rows + 1):
            qp.drawLine(left, y, left + self.grid_width, y)
            y += self.square_size
        for column in range(self.columns + 1):
            qp.drawLine(x, top, x, top + self.grid_height)
            x += self.square_size

        self.paint_rectangles(qp, Qt.black, self.graph.barrier_nodes)
        self.paint_rectangles(qp, Qt.darkGreen, self.graph.forest_nodes)
        self.paint_rectangles(qp, QColor(255, 140, 0), self.graph.desert_nodes)
        self.paint_rectangles(qp, Qt.yellow, self.graph.path_nodes)
        self.paint_rectangles(qp, Qt.blue, self.graph.frontier_nodes)
        self.paint_rectangles(qp, Qt.green, (self.graph.startpoint_node,))
        self.paint_rectangles(qp, Qt.red, (self.graph.endpoint_node,))

    def eventFilter(self, QObject, event) -> bool:
        if event.type() == QEvent.MouseButtonPress or event.type() == QEvent.MouseMove:
            mouse_position = event.pos()
            col = int(event.x() // self.square_size)
            row = int(event.y() // self.square_size)

            self.add_node(col, row, mouse_position)
        return False

    def paint_rectangles(self, qp: QPainter, color: QColor, nodes) -> None:
        left = (self.width() - self.grid_width) / 2
        top = (self.height() - self.grid_height) / 2

        # create a smaller rectangle
        object_size = self.square_size * .95
        margin = 0
        object_rect = QRectF(margin, margin, object_size, object_size)

        qp.setBrush(color)
        for node in nodes:
            qp.drawRect(object_rect.translated(
                left + node.x * self.square_size, top + node.y * self.square_size))

    def add_node(self, col: int, row: int, mouse_position) -> None:
        if self.rect().contains(mouse_position):
            node = Node(col, row)
            modifiers = QtWidgets.QApplication.keyboardModifiers()
            if modifiers == QtCore.Qt.ControlModifier:
                self.graph.remove_terrain_nodes(node)
            elif modifiers == QtCore.Qt.ShiftModifier:
                self.graph.add_desert_node(node)
            elif modifiers == QtCore.Qt.AltModifier:
                self.graph.add_forest_node(node)
            else:
                self.graph.add_barrier_node(node)
