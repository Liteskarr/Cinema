from datetime import datetime, timedelta

import PyQt5.uic as uic
from PyQt5.QtCore import (pyqtSignal)
from PyQt5.QtWidgets import (QWidget)

from src.context_locator import ContextLocator


class SessionItemWidget(QWidget):
    opening_button_clicked = pyqtSignal(int)
    closing_button_clicked = pyqtSignal(int)
    deleting_button_clicked = pyqtSignal(int)

    def __init__(self, session: int, film_name: str, film_duration: int, date: datetime):
        super().__init__()
        self._session = session
        self._film_name = film_name
        self._duration = timedelta(minutes=film_duration)
        self._date = date
        self._configure_ui()

    def _configure_ui(self):
        uic.loadUi('res/uics/session_item.ui', self)
        self.film_title.setText(self._film_name)
        minutes = self._duration.seconds // 60
        datetime_format = ContextLocator.get_context().datetime_show_format
        self.time_label.setText(f'{self._date.strftime(datetime_format)} - '
                                f'{(self._date + self._duration).strftime(datetime_format)} '
                                f'({minutes // 60 :02d}:{minutes % 60: 02d})')
        self.closing_button.clicked.connect(lambda: self.closing_button_clicked.emit(self._session))
        self.deleting_button.clicked.connect(lambda: self.deleting_button_clicked.emit(self._session))
        self.opening_button.clicked.connect(lambda: self.opening_button_clicked.emit(self._session))
