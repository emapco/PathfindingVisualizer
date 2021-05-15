import sys

from PyQt5.QtCore import QThread, pyqtSignal, QObject, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget

from graph import WeightedGraph
from node import Node
from UI.GridWidget import GridUI
from UI.ParametersDialog import ParametersPopup


class UIQObj(QObject):
    start = pyqtSignal()
    update = pyqtSignal()

    def __init__(self):
        super(UIQObj, self).__init__()

    @pyqtSlot()
    def run(self):
        while True:
            QThread.usleep(50)
            self.update.emit()


class PathQObj(QObject):
    start = pyqtSignal(WeightedGraph, str, Node, Node)

    def __init__(self):
        super(PathQObj, self).__init__()

    @pyqtSlot(WeightedGraph, str, Node, Node)
    def run(self, graph, option, start, end):
        if option == 'a':
            graph.a_star(start, end)
        elif option == "d":
            graph.dijkstra(start, end)
        else:
            graph.bfs(start, end)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pathfinding Algorithm Visualizer")
        self.layout = QVBoxLayout()

        columns = 40
        rows = 30
        self.graph = WeightedGraph(columns, rows)
        self.grid_ui = GridUI(self.graph, columns, rows)
        self.grid_ui.setContentsMargins(0, 0, 0, 0)
        self.grid_ui.setStyleSheet('background-color: white;')

        self.buttons_layout = QHBoxLayout()
        self.start_button = QPushButton('Start')
        self.reset_button = QPushButton('Reset grid')
        self.path_button = QPushButton('Clear path')
        self.change_button = QPushButton('Change parameters')
        self.buttons_layout.addWidget(self.start_button)
        self.buttons_layout.addWidget(self.reset_button)
        self.buttons_layout.addWidget(self.path_button)
        self.buttons_layout.addWidget(self.change_button)
        self.layout.addWidget(self.grid_ui)
        self.layout.addLayout(self.buttons_layout)
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.reset_button.clicked.connect(self.clear_grid)
        self.change_button.clicked.connect(self.show_parameter_popup)
        self.start_button.clicked.connect(self.generate_path)
        self.path_button.clicked.connect(self.clear_path)

        self.parameters = ParametersPopup()
        self.parameters.buttonBox.accepted.connect(self.update_graph_with_parameters)

        self.ui_thread = QThread()
        self.ui_thread.start()
        self.ui_QObj = UIQObj()
        self.ui_QObj.moveToThread(self.ui_thread)
        self.ui_QObj.update.connect(self.handle_ui_update)
        self.ui_QObj.start.connect(self.ui_QObj.run)
        self.ui_QObj.start.emit()

        self.path_thread = QThread()
        self.path_thread.start()
        self.path_QObj = PathQObj()
        self.path_QObj.moveToThread(self.path_thread)
        self.path_QObj.start.connect(self.path_QObj.run)

    def closeEvent(self, event) -> None:
        sys.exit()

    def clear_grid(self) -> None:
        self.graph.clear_terrain_nodes()
        self.clear_path()

    def clear_path(self) -> None:
        self.graph.clear_path_nodes()
        self.graph.clear_frontier_nodes()

    def show_parameter_popup(self) -> None:
        self.parameters.raise_()
        self.parameters.show()

    def update_graph_with_parameters(self) -> None:
        start_row = self.parameters.start_row
        start_col = self.parameters.start_col
        end_row = self.parameters.end_row
        end_col = self.parameters.end_col
        self.graph.startpoint_node = Node(start_col, start_row)
        self.graph.endpoint_node = Node(end_col, end_row)
        self.graph.desert_weight = self.parameters.desert_weight
        self.graph.forest_weight = self.parameters.forest_weight
        self.graph.visualize_algorithm = self.parameters.visualize_checkBox.isChecked()

    def generate_path(self) -> None:
        start = self.graph.startpoint_node
        end = self.graph.endpoint_node
        option = "b"
        if self.parameters.a_star_radio.isChecked():
            option = "a"
        elif self.parameters.dijkstra_radio.isChecked():
            option = "d"

        self.path_QObj.start.emit(self.graph, option, start, end)

    @pyqtSlot()
    def handle_ui_update(self):
        self.grid_ui.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.setFixedSize(window.size())
    app.exec_()
