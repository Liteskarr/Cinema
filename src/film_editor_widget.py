from typing import Tuple

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QWidget,
                             QDialog,
                             QGridLayout,
                             QPushButton,
                             QLineEdit,
                             QLabel,
                             QMessageBox, QSpinBox)


class FilmEditorWidget(QDialog):
    def __init__(self, parent: QWidget, film: int = -1, film_name: str = '', duration: int = -1):
        super().__init__(parent)
        self._film = film
        self._name = film_name
        self._duration = duration
        self._status = False
        self._configure_ui()

    def _configure_ui(self):
        self.setWindowTitle('Фильм')
        self.setModal(True)
        self.setFont(QFont('Sans', 12))

        self.grid = QGridLayout(self)

        self.name_label = QLabel(self)
        self.name_label.setText('Название:')
        self.grid.addWidget(self.name_label, 0, 0)

        self.name_edit = QLineEdit(self)
        self.name_edit.setText(self._name)
        self.grid.addWidget(self.name_edit, 0, 1)

        self.duration_label = QLabel(self)
        self.duration_label.setText('Продолжительность:')
        self.grid.addWidget(self.duration_label, 1, 0)

        self.duration_spin = QSpinBox(self)
        self.duration_spin.setMinimum(1)
        self.duration_spin.setMaximum(10000000)
        self.grid.addWidget(self.duration_spin, 1, 1)

        self.saving_button = QPushButton(self)
        self.saving_button.setText('Сохранить')
        self.saving_button.clicked.connect(self._handle_saving)
        self.grid.addWidget(self.saving_button, 2, 0, 1, 2)

    def _handle_saving(self):
        if len(self.name_edit.text()) < 4:
            QMessageBox.information(self,
                                    'Ошибка!',
                                    'Длина название кинотеатра должна быть больше 3 символов!')
            return
        self._name = self.name_edit.text()
        self._duration = self.duration_spin.value()
        self._status = True
        self.close()

    def get_film(self) -> Tuple[int, str, int, bool]:
        return self._film, self._name, self._duration, self._status
