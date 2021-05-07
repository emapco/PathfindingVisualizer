import sys

from PyQt5.QtWidgets import QApplication

from package.MainWindow import MainWindow


q_app = QApplication(sys.argv)
window = MainWindow()
window.show()
window.setFixedSize(window.size())
q_app.exec_()
