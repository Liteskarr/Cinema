from datetime import datetime
from typing import Tuple, List

from PyQt5.QtGui import (QFont)
from PyQt5.QtWidgets import (QWidget,
                             QGridLayout,
                             QComboBox,
                             QPushButton,
                             QListWidget,
                             QListWidgetItem)

from src.ipage import IPage
from src.context_locator import ContextLocator
from src.searched_session_item_widget import SearchedSessionItemWidget
from src.empty_page_widget import EmptyPageWidget
from src.tickets_viewer_widget import TicketsViewerWidget
from src.chair_mask_dialog import ChairMaskDialog


ANY_ITEM = 'ВСЕ'


def test_mask(booked: List[Tuple[int, int]], mask: List[Tuple[int, int]], width: int, height: int) -> bool:
    for r in range(height):
        for c in range(width):
            if (r, c) in booked:
                continue
            if all([(r + dr, c + dc) not in booked and r + dr < height and c + dc < width
                    for dr, dc in mask]) or not mask:
                return True
    return not booked


class SearchingWidget(QWidget, IPage):
    def __init__(self):
        super().__init__()
        self._new_page = EmptyPageWidget()
        self._current_mask = []
        self._configure_ui()
        self._reload_comboboxes()
        self._search()

    def _configure_ui(self):
        self.setFont(QFont('Sans', 10))

        self.grid = QGridLayout(self)

        self.cinemas_combobox = QComboBox(self)
        self.cinemas_combobox.currentIndexChanged.connect(self._handle_cinemas_combobox_changing)
        self.cinemas_combobox.currentIndexChanged.connect(self._search)
        self.grid.addWidget(self.cinemas_combobox, 0, 0)

        self.halls_combobox = QComboBox(self)
        self.halls_combobox.currentIndexChanged.connect(self._search)
        self.grid.addWidget(self.halls_combobox, 0, 1)

        self.films_combobox = QComboBox(self)
        self.films_combobox.currentIndexChanged.connect(self._search)
        self.grid.addWidget(self.films_combobox, 0, 2)

        self.chair_mask_changer = QPushButton(self)
        self.chair_mask_changer.setText('Маска кресел')
        self.chair_mask_changer.clicked.connect(self._handle_chair_mask_changing)
        self.grid.addWidget(self.chair_mask_changer, 0, 3)

        self.sessions = QListWidget(self)
        self.grid.addWidget(self.sessions, 1, 0, 4, 4)

    def _reload_comboboxes(self):
        connection = ContextLocator.get_context().connection
        cursor = connection.cursor()

        self._cinemas_list = list(cursor.execute("SELECT * FROM cinemas;"))
        self._films_list = list(cursor.execute("SELECT * FROM films;"))
        self._halls_lists = {}
        for cinema, *_ in self._cinemas_list:
            self._halls_lists[cinema] = list(cursor.execute("SELECT * FROM halls WHERE cinema = ?;",
                                                            (cinema, )))

        self.cinemas_combobox.clear()
        self.cinemas_combobox.addItem(ANY_ITEM)
        self.cinemas_combobox.addItems(map(lambda x: x[1], self._cinemas_list))

        self.films_combobox.clear()
        self.films_combobox.addItem(ANY_ITEM)
        self.films_combobox.addItems(map(lambda x: f'{x[1]} ({x[2] // 60:02d}:{x[2] % 60:02d})',
                                         self._films_list))

    def _handle_chair_mask_changing(self):
        chair_mask_dialog = ChairMaskDialog(self, self._current_mask)
        chair_mask_dialog.exec()
        self._current_mask = chair_mask_dialog.get_mask()
        self._search()

    def _handle_cinemas_combobox_changing(self):
        if self.cinemas_combobox.currentText() == ANY_ITEM:
            self.halls_combobox.clear()
            self.halls_combobox.addItem(ANY_ITEM)
            self.halls_combobox.setEnabled(False)
        else:
            self.halls_combobox.clear()
            self.halls_combobox.addItem(ANY_ITEM)
            cinema = self._cinemas_list[self.cinemas_combobox.currentIndex() - 1][0]
            self.halls_combobox.addItems(map(lambda x: x[1], self._halls_lists[cinema]))
            self.halls_combobox.setEnabled(True)

    def _handle_item_redirection(self, session: int):
        connection = ContextLocator.get_context().connection
        cursor = connection.cursor()
        request = """
        SELECT halls.id, cinemas.id FROM sessions 
        INNER JOIN halls ON halls.id = sessions.hall
        INNER JOIN cinemas ON cinemas.id = halls.cinema
        WHERE
            sessions.id = ?;
        """
        hall, cinema, *_ = cursor.execute(request, (session, )).fetchone()
        ContextLocator.get_context().current_cinema = cinema
        ContextLocator.get_context().current_hall = hall
        ContextLocator.get_context().current_session = session
        tickets_viewer = TicketsViewerWidget()
        self._new_page = tickets_viewer
        self.opened_new_page.emit()
        self._new_page = EmptyPageWidget()

    def _handle_item_closing(self, session: int):
        connection = ContextLocator.get_context().connection
        cursor = connection.cursor()
        cursor.execute("UPDATE sessions "
                       "SET closed = 1 "
                       "WHERE id = ?;", (session,))
        connection.commit()
        self._search()

    def _get_filters(self) -> str:
        result = ['sessions.closed = 0']
        if self.cinemas_combobox.currentIndex() > 0:
            cinema = self.cinemas_combobox.currentIndex() - 1
            result.append(f'cinemas.id = {self._cinemas_list[cinema][0]}')
            cinema_id = self._cinemas_list[cinema][0]
            if self.halls_combobox.currentIndex() > 0:
                result.append(f'halls.id = '
                              f'{self._halls_lists[cinema_id][self.halls_combobox.currentIndex() - 1][0]}')
        if self.films_combobox.currentIndex() > 0:
            result.append(f'films.id = {self._films_list[self.films_combobox.currentIndex() - 1][0]}')
        return ' AND '.join(result)

    def _search(self):
        self.sessions.clear()
        connection = ContextLocator.get_context().connection
        cursor = connection.cursor()
        request_filters = self._get_filters()
        request = f"""
        SELECT 
            sessions.id, films.name, films.duration, 
            sessions.datetime, halls.name, cinemas.name,
            halls.width, halls.height
        FROM sessions
        INNER JOIN films ON sessions.film = films.id
        INNER JOIN halls ON sessions.hall = halls.id
        INNER JOIN cinemas ON halls.cinema = cinemas.id
        {"WHERE " + request_filters if request_filters else ''}
        ORDER BY sessions.datetime;
        """
        for session, film, duration, date, hall, cinema, width, height in cursor.execute(request).fetchall():
            booked = list(cursor.execute("SELECT row, column FROM tickets WHERE session = ?;",
                                         (session, )).fetchall())
            if test_mask(booked, self._current_mask, width, height):
                date = datetime.strptime(date[:-3], ContextLocator.get_context().datetime_packing_format)
                self._push_widget(session, film, duration, date, hall, cinema)

    def _push_widget(self, session: int, film: str, duration: int, date: datetime, hall: str, cinema: str):
        session_widget = SearchedSessionItemWidget(session, film, duration, date, hall, cinema)
        session_widget.opening_button_clicked.connect(self._handle_item_redirection)
        session_widget.closing_button_clicked.connect(self._handle_item_closing)
        self._fast_push(session_widget)

    def _fast_push(self, widget: QWidget):
        item = QListWidgetItem(self.sessions)
        item.setSizeHint(widget.sizeHint())
        self.sessions.setItemWidget(item, widget)

    def get_new_page(self):
        return self._new_page
