import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget

from graph import Graph, WeightedGraph
from node import Node
from UI.GridWidget import GridBoard
from UI.ParametersDialog import ParametersPopup


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pathfinding Algorithm Visualizer")
        self.layout = QVBoxLayout()
        self.buttons_layout = QHBoxLayout()
        self.grid = GridBoard()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setStyleSheet('background-color: white;')
        self.start_button = QPushButton('Start')
        self.reset_button = QPushButton('Reset grid')
        self.path_button = QPushButton('Clear path')
        self.change_button = QPushButton('Change parameters')
        self.buttons_layout.addWidget(self.start_button)
        self.buttons_layout.addWidget(self.reset_button)
        self.buttons_layout.addWidget(self.path_button)
        self.buttons_layout.addWidget(self.change_button)
        self.layout.addWidget(self.grid)
        self.layout.addLayout(self.buttons_layout)
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.reset_button.clicked.connect(self.clear_grid)
        self.change_button.clicked.connect(self.show_parameter_popup)
        self.start_button.clicked.connect(self.generate_path)
        self.path_button.clicked.connect(self.clear_path)

        self.parameters = ParametersPopup()
        self.parameters.buttonBox.accepted.connect(self.update_grid_with_parameters)

        self.graph = WeightedGraph(self.grid.columns, self.grid.rows)

    def closeEvent(self, event) -> None:
        sys.exit()

    def clear_grid(self) -> None:
        self.grid.clear_all_rectangles()

    def clear_path(self) -> None:
        self.grid.clear_path()

    def show_parameter_popup(self) -> None:
        self.parameters.raise_()
        self.parameters.show()

    def update_grid_with_parameters(self) -> None:
        start_row = self.parameters.start_row
        start_col = self.parameters.start_col
        end_row = self.parameters.end_row
        end_col = self.parameters.end_col
        self.grid.grid.startpoint_node = Node(start_col, start_row)
        self.grid.grid.endpoint_node = Node(end_col, end_row)
        self.grid.grid.visualize = self.parameters.visualize_checkBox.isChecked()
        self.grid.grid.desert_weight = self.parameters.desert_weight
        self.grid.grid.forest_weight = self.parameters.forest_weight

    def generate_path(self) -> None:
        self.grid.clear_path()
        self.graph.barrier_nodes = self.grid.grid.barrier_nodes
        self.graph.desert_nodes = self.grid.grid.desert_nodes
        self.graph.forest_nodes = self.grid.grid.forest_nodes
        path = []

        start = self.grid.grid.startpoint_node
        end = self.grid.grid.endpoint_node
        if self.parameters.a_star_radio.isChecked():
            path = self.graph.a_star(start, end, self.grid)
        elif self.parameters.dijkstra_radio.isChecked():
            path = self.graph.dijkstra(start, end, self.grid)
        elif self.parameters.bfs_radio.isChecked():
            path = self.graph.bfs(start, end, self.grid)

        self.grid.clear_path()
        for node in path:
            self.grid.grid.add_path_node(node)
            self.grid.redraw_rectangles()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.setFixedSize(window.size())
    app.exec_()
