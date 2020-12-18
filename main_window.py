import PyQt5.uic as uic
from PyQt5.QtWidgets import (QMainWindow)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def _configure_ui(self):
        uic.loadUi('res/uics/main_window.ui', self)
