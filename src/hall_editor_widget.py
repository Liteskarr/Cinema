from typing import Tuple

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QWidget,
                             QDialog,
                             QGridLayout,
                             QPushButton,
                             QLineEdit,
                             QLabel,
                             QMessageBox, QSpinBox)


class HallEditorWidget(QDialog):
    def __init__(self, parent: QWidget, hall: int = -1, name: str = '', width: int = 1, height: int = 1):
        super().__init__(parent)
        self._hall = hall
        self._name = name
        self._width = width
        self._height = height
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

        self.width_label = QLabel(self)
        self.width_label.setText('Количество мест в ряду:')
        self.grid.addWidget(self.width_label, 1, 0)

        self.width_spin = QSpinBox(self)
        self.width_spin.setMinimum(1)
        self.width_spin.setMaximum(40)
        self.width_spin.setValue(self._width)
        self.grid.addWidget(self.width_spin, 1, 1)

        self.height_label = QLabel(self)
        self.height_label.setText('Количество рядов:')
        self.grid.addWidget(self.height_label, 2, 0)

        self.height_spin = QSpinBox(self)
        self.height_spin.setMinimum(1)
        self.height_spin.setMaximum(40)
        self.height_spin.setValue(self._height)
        self.grid.addWidget(self.height_spin, 2, 1)

        self.saving_button = QPushButton(self)
        self.saving_button.setText('Сохранить')
        self.saving_button.clicked.connect(self._handle_saving)
        self.grid.addWidget(self.saving_button, 3, 0, 1, 2)

    def _handle_saving(self):
        if len(self.name_edit.text()) < 4:
            QMessageBox.information(self,
                                    'Ошибка!',
                                    'Длина название кинотеатра должна быть больше 3 символов!')
            return
        self._name = self.name_edit.text()
        self._width = self.width_spin.value()
        self._height = self.height_spin.value()
        self._status = True
        self.close()

    def get_hall(self) -> Tuple[int, str, int, int, bool]:
        return self._hall, self._name, self._width, self._height, self._status
