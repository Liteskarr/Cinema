from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QLabel)

from ipage import IPage


class EmptyPageWidget(QLabel, IPage):
    def __init__(self):
        super().__init__()
        self._configure_ui()

    def _configure_ui(self):
        self.setText('404')
        self.setFont(QFont('Sans', 36))
        self.setAlignment(Qt.AlignCenter)
