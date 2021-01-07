from datetime import datetime
from typing import Tuple

from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QWidget,
                             QDialog,
                             QGridLayout,
                             QPushButton,
                             QLabel,
                             QComboBox,
                             QDateTimeEdit, QSpinBox)

from context_locator import ContextLocator


class SessionEditorWidget(QDialog):
    def __init__(self,
                 parent: QWidget,
                 session: int = -1,
                 film: int = 0,
                 date: datetime = datetime.now(),
                 cost: int = 1):
        super().__init__(parent)
        self._session = session
        self._film = film
        self._date = date
        self._cost = cost
        self._status = False
        connection = ContextLocator.get_context().connection
        cursor = connection.cursor()
        self._raw_films = list(cursor.execute("SELECT * FROM films;").fetchall())
        self._films = list(map(lambda films: f'{films[1]} ({films[2] // 60:02d}:{films[2] % 60:02d})',
                               self._raw_films))
        self._configure_ui()

    def _configure_ui(self):
        self.setWindowTitle('Сеанс')
        self.setModal(True)
        self.setFont(QFont('Sans', 12))

        self.grid = QGridLayout(self)

        self.film_label = QLabel(self)
        self.film_label.setText('Фильм:')
        self.grid.addWidget(self.film_label, 0, 0)

        self.film_combobox = QComboBox(self)
        self.film_combobox.addItems(self._films)
        self.film_combobox.setCurrentIndex(self._film)
        self.grid.addWidget(self.film_combobox, 0, 1)

        self.datetime_label = QLabel(self)
        self.datetime_label.setText('Время сеанса:')
        self.grid.addWidget(self.datetime_label, 1, 0)

        self.datetime_edit = QDateTimeEdit(self)
        self.datetime_edit.setDateTime(QDateTime(self._date.year,
                                                 self._date.month,
                                                 self._date.day,
                                                 self._date.hour,
                                                 self._date.minute))
        self.grid.addWidget(self.datetime_edit, 1, 1)

        self.cost_label = QLabel(self)
        self.cost_label.setText('Цена за билет:')
        self.grid.addWidget(self.cost_label, 2, 0)

        self.cost_spin = QSpinBox(self)
        self.cost_spin.setMinimum(1)
        self.cost_spin.setMaximum(1000000)
        self.grid.addWidget(self.cost_spin, 2, 1)

        self.saving_button = QPushButton(self)
        self.saving_button.setText('Сохранить')
        self.saving_button.clicked.connect(self._handle_saving)
        self.grid.addWidget(self.saving_button, 3, 0, 1, 2)

    def _handle_saving(self):
        self._film = self.film_combobox.currentIndex()
        self._date = self.datetime_edit.dateTime().toPyDateTime()
        self._cost = self.cost_spin.value()
        self._status = True
        self.close()

    def get_session(self) -> Tuple[int, int, datetime, int, bool]:
        return self._session, self._raw_films[self._film][0], self._date, self._cost, self._status
