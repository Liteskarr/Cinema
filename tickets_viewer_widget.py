from PyQt5.QtCore import (Qt)
from PyQt5.QtGui import (QFont)
from PyQt5.QtWidgets import (QWidget,
                             QGridLayout,
                             QPushButton,
                             QLabel,
                             QSizePolicy)

from ipage import IPage
from context_locator import ContextLocator
from empty_page_widget import EmptyPageWidget


class TicketsViewerWidget(QWidget, IPage):
    def __init__(self):
        super().__init__()
        self.connection = ContextLocator.get_context().connection
        self.cursor = self.connection.cursor()
        self.hall = ContextLocator.get_context().current_hall
        self.session = ContextLocator.get_context().current_session
        self.width, self.height = self.cursor.execute("SELECT width, height FROM halls WHERE id = ?;",
                                                      (self.hall, )).fetchone()
        self._configure_ui()

    def _configure_ui(self):
        self.setFont(QFont('Sans', 12))
        self.grid = QGridLayout(self)

        self.buttons = {}
        for y in range(self.height):
            for x in range(self.width):
                button = QPushButton(self)
                if list(self.cursor.execute("SELECT * FROM tickets "
                                            "WHERE session = ? AND row = ? AND column = ?;",
                                            (self.session, y, x)).fetchall()):
                    button.setStyleSheet('background-color: yellow')
                else:
                    button.setStyleSheet('background-color: white')
                button.setText(str(x + 1))
                button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                button.clicked.connect(self._handlers_factory(y, x))
                self.buttons[y, x] = button
                self.grid.addWidget(button, y + 1, x + 1)

        self.screen_label = QLabel(self)
        self.screen_label.setFont(QFont('Sans', 24))
        self.screen_label.setText('Экран')
        self.screen_label.setAlignment(Qt.AlignCenter)
        self.screen_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.grid.addWidget(self.screen_label, 0, 1, 1, self.width)

        for i in range(1, self.height + 1):
            label = QLabel(self)
            label.setText(str(i))
            label.setAlignment(Qt.AlignCenter)
            self.grid.addWidget(label, i, 0)

    def _handlers_factory(self, row: int, column: int):
        def f():
            self._handle_button_click(row, column)
        return f

    def _handle_button_click(self, row: int, column: int):
        if list(self.cursor.execute("SELECT session FROM tickets "
                                    "WHERE session = ? AND row = ? AND column = ?;",
                                    (self.session, row, column)).fetchall()):
            self.cursor.execute("DELETE FROM tickets WHERE session = ? AND row = ? AND column = ?;",
                                (self.session, row, column))
            self.buttons[row, column].setStyleSheet('background-color: white')
        else:
            self.cursor.execute("INSERT INTO tickets VALUES(?, ?, ?);", (self.session, row, column))
            self.buttons[row, column].setStyleSheet('background-color: yellow')
        self.buttons[row, column].setFont(QFont('Sans', 12))
        self.connection.commit()

    def get_new_page(self):
        return EmptyPageWidget()
