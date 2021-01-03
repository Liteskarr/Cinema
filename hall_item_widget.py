import PyQt5.uic as uic
from PyQt5.QtCore import (pyqtSignal)
from PyQt5.QtWidgets import (QWidget)


class HallItemWidget(QWidget):
    deleting_button_clicked = pyqtSignal(int)
    editing_button_clicked = pyqtSignal(int)
    opening_button_clicked = pyqtSignal(int)

    def __init__(self, hall: int, name: str, width: int, height: int):
        super().__init__()
        self._hall = hall
        self._name = name
        self._width = width
        self._height = height
        self._configure_ui()

    def _configure_ui(self):
        uic.loadUi('res/uics/hall_item.ui', self)
        self.title_label.setText(self._name)
        self.size_label.setText(f'({self._height}x{self._width})')
        self.deleting_button.clicked.connect(lambda: self.deleting_button_clicked.emit(self._hall))
        self.editing_button.clicked.connect(lambda: self.editing_button_clicked.emit(self._hall))
        self.opening_button.clicked.connect(lambda: self.opening_button_clicked.emit(self._hall))
