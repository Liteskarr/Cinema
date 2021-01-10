from typing import List, Tuple

from PyQt5.QtGui import (QFont)
from PyQt5.QtWidgets import (QWidget,
                             QDialog,
                             QSpinBox,
                             QPushButton,
                             QGridLayout,
                             QLabel,
                             QSizePolicy)


class ChairMaskDialog(QDialog):
    def __init__(self, parent: QWidget, initial_mask: List = None):
        super().__init__(parent)
        self._mask = [] if initial_mask is None else initial_mask
        self._configure_ui()
        self._redraw_buttons()

    def _configure_ui(self):
        self.setWindowTitle('Маска кресел')
        self.setFont(QFont('Sans', 12))
        self.setModal(True)

        self.grid = QGridLayout(self)

        self.buttons_layout = QGridLayout(self)
        self.grid.addLayout(self.buttons_layout, 1, 1, 4, 4)

        self.width_label = QLabel(self)
        self.width_label.setText('Ширина маски:')
        self.grid.addWidget(self.width_label, 0, 0)

        self.width_spin = QSpinBox(self)
        self.width_spin.setMinimum(1)
        self.width_spin.setMaximum(40)
        self.width_spin.setValue(max(self._mask + [(0, 0)], key=lambda x: x[1])[1] + 1)
        self.width_spin.valueChanged.connect(self._handle_spin_value_changing)
        self.grid.addWidget(self.width_spin, 0, 1)

        self.height_label = QLabel(self)
        self.height_label.setText('Высота маски:')
        self.grid.addWidget(self.height_label, 0, 2)

        self.height_spin = QSpinBox(self)
        self.height_spin.setMinimum(1)
        self.height_spin.setMaximum(40)
        self.height_spin.setValue(max(self._mask + [(0, 0)], key=lambda x: x[0])[0] + 1)
        self.height_spin.valueChanged.connect(self._handle_spin_value_changing)
        self.grid.addWidget(self.height_spin, 0, 3)

        self.saving_button = QPushButton(self)
        self.saving_button.setText('Применить')
        self.saving_button.clicked.connect(self._handle_saving_button_click)
        self.grid.addWidget(self.saving_button, 0, 4)

        self.dropping_button = QPushButton(self)
        self.dropping_button.setText('Сбросить маску')
        self.dropping_button.clicked.connect(self._handle_mask_dropping)
        self.grid.addWidget(self.dropping_button, 0, 5)

    def _filter_mask(self):
        width = self.width_spin.value()
        height = self.height_spin.value()
        self._mask = list(filter(lambda p: 0 <= p[0] < height and 0 <= p[1] < width, self._mask))

    def _clear_buttons_layout(self):
        for i in reversed(range(self.buttons_layout.count())):
            self.buttons_layout.itemAt(i).widget().setParent(None)

    def _redraw_buttons(self):
        width = self.width_spin.value()
        height = self.height_spin.value()
        self._clear_buttons_layout()
        for i in range(height):
            row_label = QLabel(self)
            row_label.setText(str(i + 1))
            self.buttons_layout.addWidget(row_label, i, 0)
            for j in range(width):
                chair = QPushButton(self)
                chair.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                chair.setText(str(j + 1))
                if (i, j) in self._mask:
                    chair.setStyleSheet('background-color: yellow')
                else:
                    chair.setStyleSheet('background-color: white')
                chair.clicked.connect(self._factory_of_handler_of_chair_click(i, j, chair))
                self.buttons_layout.addWidget(chair, i, j + 1)

    def _factory_of_handler_of_chair_click(self, row: int, column: int, widget: QWidget):
        def func():
            if (row, column) in self._mask:
                widget.setStyleSheet('background-color: white')
                self._mask.remove((row, column))
            else:
                widget.setStyleSheet('background-color: yellow')
                self._mask.append((row, column))
            widget.setFont(QFont('Sans', 12))
        return func

    def _handle_spin_value_changing(self):
        self._redraw_buttons()
        self._filter_mask()

    def _handle_saving_button_click(self):
        self.close()

    def _handle_mask_dropping(self):
        self._mask = []
        self.close()

    def get_mask(self) -> List[Tuple[int, int]]:
        return self._mask
