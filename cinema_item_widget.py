import PyQt5.uic as uic
from PyQt5.QtCore import (pyqtSignal)
from PyQt5.QtWidgets import (QWidget)

from cinema_data import CinemaData


class CinemaItemWidget(QWidget):
    deleting_button_clicked = pyqtSignal(int)
    editing_button_clicked = pyqtSignal(int)
    opening_button_clicked = pyqtSignal(int)

    def __init__(self, data: CinemaData):
        super().__init__()
        self._data = data
        self._configure_ui()

    def _configure_ui(self):
        uic.loadUi('res/uics/cinema_item.ui', self)
        self.title_label.setText(self._data.name)
        self.deleting_button.clicked.connect(lambda: self.deleting_button_clicked.emit(self._data.id))
        self.editing_button.clicked.connect(lambda: self.editing_button_clicked.emit(self._data.id))
        self.opening_button.clicked.connect(lambda: self.opening_button_clicked.emit(self._data.id))
