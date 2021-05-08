from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QButtonGroup


class ParametersPopup(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedHeight(160)
        self.setFixedWidth(320)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setAttribute(Qt.WA_QuitOnClose, True)
        self.setObjectName("Parameters")
        self.bfs_radio = QtWidgets.QRadioButton(self)
        self.bfs_radio.setGeometry(QtCore.QRect(250, 70, 82, 17))
        self.bfs_radio.setObjectName("bfs_radio")
        self.a_star_radio = QtWidgets.QRadioButton(self)
        self.a_star_radio.setGeometry(QtCore.QRect(250, 10, 82, 17))
        self.a_star_radio.setObjectName("a_star_radio")
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(0, 130, 311, 23))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.end_textbox = QtWidgets.QPlainTextEdit(self)
        self.end_textbox.setGeometry(QtCore.QRect(70, 50, 50, 21))
        self.end_textbox.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.end_textbox.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.end_textbox.setObjectName("end_textbox")
        self.start_textbox = QtWidgets.QPlainTextEdit(self)
        self.start_textbox.setGeometry(QtCore.QRect(70, 10, 50, 21))
        self.start_textbox.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.start_textbox.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.start_textbox.setObjectName("start_textbox")
        self.start_label = QtWidgets.QLabel(self)
        self.start_label.setGeometry(QtCore.QRect(10, 10, 61, 16))
        self.start_label.setObjectName("start_label")
        self.algorithm_label = QtWidgets.QLabel(self)
        self.algorithm_label.setGeometry(QtCore.QRect(140, 10, 101, 16))
        self.algorithm_label.setObjectName("algorithm_label")
        self.end_label = QtWidgets.QLabel(self)
        self.end_label.setGeometry(QtCore.QRect(10, 50, 47, 13))
        self.end_label.setObjectName("end_label")
        self.dijkstra_radio = QtWidgets.QRadioButton(self)
        self.dijkstra_radio.setGeometry(QtCore.QRect(250, 40, 82, 16))
        self.dijkstra_radio.setObjectName("dijkstra_radio")
        self.visualize_checkBox = QtWidgets.QCheckBox(self)
        self.visualize_checkBox.setGeometry(QtCore.QRect(10, 100, 121, 17))
        self.visualize_checkBox.setObjectName("visualize_checkBox")

        QtCore.QMetaObject.connectSlotsByName(self)

        self.setWindowTitle("Parameters")
        self.bfs_radio.setText("BFS")
        self.a_star_radio.setText("A*")
        self.start_label.setText("Start point:")
        self.algorithm_label.setText("Select an algorithm:")
        self.end_label.setText("End point:")
        self.dijkstra_radio.setText("Dijkstra")
        self.start_textbox.setPlainText("0, 0")
        self.end_textbox.setPlainText("39, 29")
        self.visualize_checkBox.setText("visualize algorithm")
        self.visualize_checkBox.setChecked(True)
        self.bfs_radio.setChecked(True)

        # set start/end row&col values using default text
        self.set_start_end_points()

        # variables in case values are changed but user presses cancel button
        self.set_previous_variables()

        self.group = QButtonGroup()
        self.group.addButton(self.a_star_radio)
        self.group.addButton(self.bfs_radio)
        self.group.addButton(self.dijkstra_radio)

        self.buttonBox.buttons()[0].clicked.connect(self.ok_button)  # ok button
        self.buttonBox.buttons()[1].clicked.connect(self.cancel_button)  # cancel button

    def closeEvent(self, event):
        self.cancel_button()

    def set_previous_variables(self):
        self.previous_start_text = self.start_textbox.toPlainText()
        self.previous_end_text = self.end_textbox.toPlainText()
        self.previous_visualize = self.visualize_checkBox.isChecked()
        self.previous_a_star_radio_state = self.a_star_radio.isChecked()
        self.previous_bfs_radio_state = self.bfs_radio.isChecked()
        self.previous_dijkstra_radio_state = self.dijkstra_radio.isChecked()

    def set_start_end_points(self):
        try:
            start_point_values = self.start_textbox.toPlainText().strip().split(",", maxsplit=1)
            end_point_values = self.end_textbox.toPlainText().split(",", maxsplit=1)
            self.start_col = int(start_point_values[0].strip())
            self.start_row = int(start_point_values[1].strip())
            self.end_col = int(end_point_values[0].strip())
            self.end_row = int(end_point_values[1].strip())
            return True
        except (ValueError, IndexError) as e:
            return False

    def ok_button(self):
        valid_values = self.set_start_end_points()  # test whether input is valid

        if valid_values:
            self.set_previous_variables()  # changes are valid and confirmed so update previous variables
            self.close()

    def cancel_button(self):
        self.start_textbox.setPlainText(self.previous_start_text)  # user cancelled so restore previous values
        self.end_textbox.setPlainText(self.previous_end_text)
        self.visualize_checkBox.setChecked(self.previous_visualize)

        # set setExclusive to False so radio states can be reset to previous state
        # otherwise radio buttons cannot be set to False individually
        self.group.setExclusive(False)
        self.a_star_radio.setChecked(self.previous_a_star_radio_state)
        self.bfs_radio.setChecked(self.previous_bfs_radio_state)
        self.dijkstra_radio.setChecked(self.previous_dijkstra_radio_state)
        self.group.setExclusive(True)

        self.close()
