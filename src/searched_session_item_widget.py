from datetime import datetime

from PyQt5.QtCore import (pyqtSignal)
from PyQt5.QtGui import (QFont)
from PyQt5.QtWidgets import (QWidget,
                             QGridLayout, QLabel)

from src.session_item_widget import SessionItemWidget


class SearchedSessionItemWidget(QWidget):
    opening_button_clicked = pyqtSignal(int)
    closing_button_clicked = pyqtSignal(int)

    def __init__(self,
                 session: int,
                 film_name: str,
                 film_duration: int,
                 date: datetime,
                 hall_name: str,
                 cinema_name: str):
        super().__init__()
        self._session = session
        self._film_name = film_name
        self._film_duration = film_duration
        self._date = date
        self._hall_name = hall_name
        self._cinema_name = cinema_name
        self._configure_ui()

    def _configure_ui(self):
        self.setFont(QFont('Sans', 14))
        self.grid = QGridLayout(self)
        self.setContentsMargins(0, 0, 0, 0)

        self.cinema_label = QLabel(self)
        self.cinema_label.setText(f'Кинотеатр: {self._cinema_name}')
        self.grid.addWidget(self.cinema_label, 0, 0)

        self.hall_label = QLabel(self)
        self.hall_label.setText(f'Зал: {self._hall_name}')
        self.grid.addWidget(self.hall_label, 1, 0)

        self.session_item_widget = SessionItemWidget(self._session,
                                                     self._film_name,
                                                     self._film_duration,
                                                     self._date)
        self.session_item_widget.setFont(QFont('Sans', 12))
        self.session_item_widget.deleting_button.hide()
        self.session_item_widget.opening_button.clicked.connect(lambda: self.opening_button_clicked.emit(self._session))
        self.session_item_widget.closing_button_clicked.connect(lambda: self.closing_button_clicked.emit(self._session))
        self.grid.addWidget(self.session_item_widget, 2, 0)
