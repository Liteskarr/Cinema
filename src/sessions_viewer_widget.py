from datetime import datetime, timedelta

from PyQt5.QtWidgets import QMessageBox

from src.context_locator import ContextLocator
from src.empty_page_widget import EmptyPageWidget
from src.items_viewer_widget import ItemsViewerWidget
from src.session_editor_widget import SessionEditorWidget
from src.session_item_widget import SessionItemWidget
from src.tickets_viewer_widget import TicketsViewerWidget


def test_on_collisions(date: datetime, duration: int, hall: int) -> bool:
    duration = timedelta(minutes=duration)
    connection = ContextLocator.get_context().connection
    cursor = connection.cursor()
    for sdate, sduration in cursor.execute("SELECT sessions.datetime, films.duration FROM sessions "
                                           "INNER JOIN films ON films.id = sessions.film "
                                           "WHERE hall = ? AND closed = 0;", (hall, )).fetchall():
        sdate = datetime.strptime(sdate[:-3], ContextLocator.get_context().datetime_packing_format)
        sduration = timedelta(minutes=sduration)
        if (date <= sdate <= date + duration) or \
                (date <= sdate + duration <= date + duration) or \
                (sdate <= date and date + duration <= sdate + sduration):
            return True
    return False


class SessionsViewerWidget(ItemsViewerWidget):
    def _handle_item_adding(self, *args, **kwargs):
        connection = ContextLocator.get_context().connection
        cursor = connection.cursor()
        hall = ContextLocator.get_context().current_hall
        session_editor = SessionEditorWidget(self)
        session_editor.exec()
        _, film, date, cost, ok = session_editor.get_session()
        duration, *_ = cursor.execute("SELECT duration FROM films WHERE id = ?;", (film,)).fetchone()
        if ok:
            if test_on_collisions(date, duration, hall):
                QMessageBox.information(self, 'Ошибка!', 'Данный сеанс пересекается с уже существующим!')
                return
            cursor.execute("INSERT INTO sessions(hall, film, datetime, cost, closed) "
                           "VALUES(?, ?, ?, ?, ?)", (hall, film, date, cost, False))
            connection.commit()
            self.reload_items()

    def _handle_item_redirection(self, session: int):
        ContextLocator.get_context().current_session = session
        self._new_page = TicketsViewerWidget()
        self.opened_new_page.emit()
        self._new_page = EmptyPageWidget()

    def _handle_item_deleting(self, session: int):
        connection = ContextLocator.get_context().connection
        cursor = connection.cursor()
        cursor.execute("DELETE FROM sessions WHERE id = ?;", (session,))
        connection.commit()
        self.reload_items()

    def _handle_item_closing(self, session: int):
        connection = ContextLocator.get_context().connection
        cursor = connection.cursor()
        cursor.execute("UPDATE sessions "
                       "SET closed = 1 "
                       "WHERE id = ?;", (session,))
        connection.commit()
        self.reload_items()

    def push_widget(self, widget: SessionItemWidget):
        widget.closing_button_clicked.connect(self._handle_item_closing)
        widget.deleting_button_clicked.connect(self._handle_item_deleting)
        widget.opening_button_clicked.connect(self._handle_item_redirection)
        self._fast_push(widget)

    def reload_items(self):
        self.widgets.clear()
        connection = ContextLocator.get_context().connection
        cursor = connection.cursor()
        request = """
        SELECT sessions.id, films.name, films.duration, sessions.datetime, sessions.closed FROM sessions
        INNER JOIN films ON films.id = sessions.film
        WHERE
            sessions.hall = ?; 
        """
        hall = ContextLocator.get_context().current_hall
        for session, film_name, duration, date, is_closed in cursor.execute(request, (hall, )).fetchall():
            if not is_closed:
                date = date[:-3]
                date = datetime.strptime(date, ContextLocator.get_context().datetime_packing_format)
                self.push_widget(SessionItemWidget(session, film_name, duration, date))
