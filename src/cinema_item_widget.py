import PyQt5.uic as uic
from PyQt5.QtCore import (pyqtSignal)
from PyQt5.QtWidgets import (QWidget)


class CinemaItemWidget(QWidget):
    deleting_button_clicked = pyqtSignal(int)
    editing_button_clicked = pyqtSignal(int)
    opening_button_clicked = pyqtSignal(int)

    def __init__(self, cinema: int, name: str):
        super().__init__()
        self._cinema = cinema
        self._name = name
        self._configure_ui()

    def _configure_ui(self):
        uic.loadUi('res/uics/cinema_item.ui', self)
        self.title_label.setText(self._name)
        self.deleting_button.clicked.connect(lambda: self.deleting_button_clicked.emit(self._cinema))
        self.editing_button.clicked.connect(lambda: self.editing_button_clicked.emit(self._cinema))
        self.opening_button.clicked.connect(lambda: self.opening_button_clicked.emit(self._cinema))
