import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget

from Graph import Graph
from Node import Node
from package.GridWidget import Grid
from package.ParametersDialog import ParametersPopup


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pathfinding Algorithm Visualizer")
        self.layout = QVBoxLayout()
        self.buttons_layout = QHBoxLayout()
        self.grid = Grid()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setStyleSheet('background-color: white;')
        self.start_button = QPushButton('Start animation')
        self.reset_button = QPushButton('Reset grid')
        self.change_button = QPushButton('Change parameters')
        self.buttons_layout.addWidget(self.start_button)
        self.buttons_layout.addWidget(self.reset_button)
        self.buttons_layout.addWidget(self.change_button)
        self.layout.addWidget(self.grid)
        self.layout.addLayout(self.buttons_layout)
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.reset_button.clicked.connect(self.clear_grid)
        self.change_button.clicked.connect(self.show_parameter_popup)
        self.start_button.clicked.connect(self.generate_path)

        self.parameters = ParametersPopup()
        self.parameters.buttonBox.buttons()[0].clicked.connect(self.update_end_point_rects)

        self.graph = Graph(self.grid.columns, self.grid.rows)

    def closeEvent(self, event) -> None:
        sys.exit()

    def clear_grid(self):
        self.grid.clear_all_rectangles()

    def show_parameter_popup(self):
        self.parameters.raise_()
        self.parameters.show()

    def update_end_point_rects(self):
        start_row = self.parameters.start_row
        start_col = self.parameters.start_col
        end_row = self.parameters.end_row
        end_col = self.parameters.end_col
        self.grid.startpoint_rect = Node(start_col, start_row)
        self.grid.endpoint_rect = Node(end_col, end_row)

    def generate_path(self):
        self.grid.clear_path()
        self.graph.barriers = self.grid.barrier_rects
        path = []

        start = self.grid.startpoint_rect
        end = self.grid.endpoint_rect
        if self.parameters.a_star_radio.isChecked():
            path = self.graph.a_star(start, end, self.grid)
        elif self.parameters.dijkstra_radio.isChecked():
            path = self.graph.dijkstra(start, end, self.grid)
        elif self.parameters.bfs_radio.isChecked():
            path = self.graph.bfs(start, end, self.grid)

        self.grid.clear_path()
        for node in path:
            self.grid.path_rects.add(node)
            self.grid.redraw_rectangles()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.setFixedSize(window.size())
    app.exec_()
