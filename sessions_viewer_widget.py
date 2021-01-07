from datetime import datetime

from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtWidgets import QInputDialog, QDialog, QDialogButtonBox, QDateTimeEdit, QVBoxLayout, QMessageBox

from context_locator import ContextLocator
from items_viewer_widget import ItemsViewerWidget
from session_item_widget import SessionItemWidget
from tickets_viewer_widget import TicketsViewerWidget
from empty_page_widget import EmptyPageWidget


class DateDialog(QDialog):
    def __init__(self, parent=None):
        super(DateDialog, self).__init__(parent)

        layout = QVBoxLayout(self)

        self.datetime = QDateTimeEdit(self)
        self.datetime.setCalendarPopup(True)
        self.datetime.setDateTime(QDateTime.currentDateTime())
        layout.addWidget(self.datetime)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _get_datetime(self):
        return self.datetime.dateTime()

    @staticmethod
    def get_datetime(parent=None):
        dialog = DateDialog(parent)
        result = dialog.exec_()
        date = dialog._get_datetime()
        return date, result == QDialog.Accepted


class SessionsViewerWidget(ItemsViewerWidget):
    def _handle_item_adding(self, *args, **kwargs):
        connection = ContextLocator.get_context().connection
        cursor = connection.cursor()
        hall = ContextLocator.get_context().current_hall
        films = list(cursor.execute("SELECT * FROM films;").fetchall())
        film, film_ok = QInputDialog.getItem(self, 'Создание сеанса', 'Выберите фильм:',
                                             map(lambda x: x[1], films), editable=False)
        film, film_name, duration = films[list(map(lambda x: x[1], films)).index(film)]
        date, date_ok = DateDialog.get_datetime(self)
        date = date.toPyDateTime()
        cost, cost_ok = QInputDialog.getInt(self, 'Создание сеанса', 'Цена за билет: ', min=1)
        if film_ok and date_ok and cost_ok:
            # TODO: Test on collisions.
            if list(cursor.execute("").fetchall()):
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
        cursor.execute("DELETE FROM sessions WHERE id = ?;", (session, ))
        connection.commit()
        self.reload_items()

    def _handle_item_closing(self, session: int):
        connection = ContextLocator.get_context().connection
        cursor = connection.cursor()
        cursor.execute("UPDATE sessions "
                       "SET closed = 1 "
                       "WHERE id = ?;", (session, ))
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
        INNER JOIN films ON films.id = sessions.film; 
        """
        for session, film_name, duration, date, is_closed in cursor.execute(request).fetchall():
            if not is_closed:
                date = date[:date.index('.') - 3]
                date = datetime.strptime(date, ContextLocator.get_context().datetime_packing_format)
                self.push_widget(SessionItemWidget(session, film_name, duration, date))
