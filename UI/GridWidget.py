from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QRectF, QEvent
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget
from qtpy import QtCore

from Node import Node, DESERT_WEIGHT, FOREST_WEIGHT


class Grid(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setMinimumSize(800, 600)
        self.columns = 40
        self.rows = 30

        self.barrier_rects = set()
        self.desert_rects = set()
        self.forest_rects = set()
        self.startpoint_rect = Node(0, 0)
        self.endpoint_rect = Node(39, 29)
        self.path_rects = set()
        self.frontier_rects = set()

    def resizeEvent(self, event):
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

    def paintEvent(self, event):
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

        # draw barrier rectangles
        self.paintRect(qp, Qt.black, self.barrier_rects)
        self.paintRect(qp, Qt.darkGreen, self.forest_rects)
        self.paintRect(qp, QColor(255, 140, 0), self.desert_rects)
        self.paintRect(qp, Qt.yellow, self.path_rects)
        self.paintRect(qp, Qt.blue, self.frontier_rects)
        self.paintRect(qp, Qt.green, (self.startpoint_rect,))
        self.paintRect(qp, Qt.red, (self.endpoint_rect,))

    def paintRect(self, qp, color, rects):
        # center the grid
        left = (self.width() - self.grid_width) / 2
        top = (self.height() - self.grid_height) / 2

        # create a smaller rectangle
        object_size = self.square_size * .95
        margin = 0
        object_rect = QRectF(margin, margin, object_size, object_size)

        qp.setBrush(color)
        for node in rects:
            qp.drawRect(object_rect.translated(
                left + node.x * self.square_size, top + node.y * self.square_size))

    def eventFilter(self, QObject, event):
        if event.type() == QEvent.MouseButtonPress or event.type() == QEvent.MouseMove:
            mouse_position = event.pos()
            col = int(event.x() // self.square_size)
            row = int(event.y() // self.square_size)

            self.add_node(col, row, mouse_position)

        if event.type() == QEvent.MouseButtonRelease:
            self.redraw_rectangles()

        return False

    def add_node(self, col, row, mouse_position):
        if self.rect().contains(mouse_position):
            modifiers = QtWidgets.QApplication.keyboardModifiers()
            if modifiers == QtCore.Qt.ControlModifier:
                self.remove_terrain_rect(col, row)
            elif modifiers == QtCore.Qt.ShiftModifier:
                self.desert_rects.add(Node(col, row))
            elif modifiers == QtCore.Qt.AltModifier:
                self.forest_rects.add(Node(col, row))
            else:
                self.barrier_rects.add(Node(col, row))

    def clear_all_rectangles(self):
        self.barrier_rects.clear()
        self.forest_rects.clear()
        self.desert_rects.clear()
        self.clear_path()

    def clear_path(self):
        self.path_rects.clear()
        self.frontier_rects.clear()
        self.update()

    def redraw_rectangles(self):
        self.update()

    def add_frontier(self, node: Node):
        self.frontier_rects.add(node)

    def remove_frontier(self, node: Node):
        self.frontier_rects.remove(node)

    def remove_terrain_rect(self, col, row):
        for terrain in self.barrier_rects, self.forest_rects, self.desert_rects:
            try:
                terrain.remove(Node(col, row))
            except KeyError:
                pass