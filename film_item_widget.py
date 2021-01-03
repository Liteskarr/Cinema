import PyQt5.uic as uic
from PyQt5.QtCore import (pyqtSignal)
from PyQt5.QtWidgets import (QWidget)


class FilmItemWidget(QWidget):
    film_deleting = pyqtSignal(int)

    def __init__(self, film: int, name: str, duration: int):
        super().__init__()
        self._film = film
        self._name = name
        self._duration = duration
        self._configure_ui()

    def _configure_ui(self):
        uic.loadUi('res/uics/film_item.ui', self)
        self.title_label.setText(self._name)
        self.duration_label.setText(f'({self._duration // 60 :02d}:{self._duration % 60 :02d})')
        self.deleting_button.clicked.connect(lambda: self.film_deleting.emit(self._film))
