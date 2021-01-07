from typing import Tuple

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QWidget,
                             QDialog,
                             QGridLayout,
                             QPushButton,
                             QLineEdit,
                             QLabel,
                             QMessageBox)


class CinemaEditorWidget(QDialog):
    def __init__(self, parent: QWidget, cinema: int = -1, cinema_name: str = ''):
        super().__init__(parent)
        self._cinema = cinema
        self._name = cinema_name
        self._status = False
        self._configure_ui()

    def _configure_ui(self):
        self.setWindowTitle('Кинотеатр')
        self.setModal(True)
        self.setFont(QFont('Sans', 12))

        self.grid = QGridLayout(self)

        self.name_label = QLabel(self)
        self.name_label.setText('Название:')
        self.grid.addWidget(self.name_label, 0, 0)

        self.name_edit = QLineEdit(self)
        self.name_edit.setText(self._name)
        self.grid.addWidget(self.name_edit, 0, 1)

        self.saving_button = QPushButton(self)
        self.saving_button.setText('Сохранить')
        self.saving_button.clicked.connect(self._handle_saving)
        self.grid.addWidget(self.saving_button, 1, 0, 1, 2)

    def _handle_saving(self):
        if len(self.name_edit.text()) < 4:
            QMessageBox.information(self,
                                    'Ошибка!',
                                    'Длина название кинотеатра должна быть больше 3 символов!')
            return
        self._name = self.name_edit.text()
        self._status = True
        self.close()

    def get_cinema(self) -> Tuple[int, str, bool]:
        return self._cinema, self._name, self._status
