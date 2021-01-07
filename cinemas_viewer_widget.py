from PyQt5.QtWidgets import (QMessageBox)

from context_locator import ContextLocator
from cinema_item_widget import CinemaItemWidget
from items_viewer_widget import ItemsViewerWidget
from empty_page_widget import EmptyPageWidget
from halls_viewer_widget import HallsViewerWidget
from cinema_editor_widget import CinemaEditorWidget


class CinemasViewerWidget(ItemsViewerWidget):
    def reload_items(self):
        self.widgets.clear()
        connection = ContextLocator.get_context().connection
        cursor = connection.cursor()
        for cinema, name in cursor.execute("SELECT * FROM cinemas;").fetchall():
            self.add_widget(CinemaItemWidget(cinema, name))

    def push_widget(self, widget: CinemaItemWidget):
        widget.opening_button_clicked.connect(self._handle_item_redirection)
        widget.editing_button_clicked.connect(self._handle_item_editing)
        widget.deleting_button_clicked.connect(self._handle_item_deleting)
        self._fast_push(widget)

    def _handle_item_adding(self):
        cinema_editor = CinemaEditorWidget(self)
        cinema_editor.exec()
        cinema, cinema_name, ok = cinema_editor.get_cinema()
        if ok:
            connection = ContextLocator.get_context().connection
            cursor = connection.cursor()
            if list(cursor.execute("SELECT id FROM cinemas WHERE name = ?;", (cinema_name, )).fetchall()):
                QMessageBox.information(self, 'Ошибка!', 'Кинотеатр с таким названием уже существует!')
                return
            else:
                cursor.execute("INSERT INTO cinemas(name) VALUES(?);", (cinema_name, ))
                connection.commit()
                self.reload_items()

    def _handle_item_redirection(self, cinema: int):
        ContextLocator.get_context().current_cinema = cinema
        self._new_page = HallsViewerWidget()
        self.opened_new_page.emit()
        self._new_page = EmptyPageWidget()

    def _handle_item_editing(self, cinema: int):
        connection = ContextLocator.get_context().connection
        cursor = connection.cursor()
        cinema_name, *_ = cursor.execute("SELECT name FROM cinemas WHERE id = ?;", (cinema, )).fetchone()
        cinema_editor = CinemaEditorWidget(self, cinema_name=cinema_name)
        cinema_editor.exec()
        _, cinema_name, ok = cinema_editor.get_cinema()
        if ok:
            cursor.execute("UPDATE cinemas SET name = ? WHERE id = ?;", (cinema_name, cinema))
            connection.commit()
            self.reload_items()

    def _handle_item_deleting(self, cinema: int):
        ok = QMessageBox.question(self, 'Вы уверены?', 'Это действие невозможно отменить!')
        if ok == QMessageBox.Yes:
            connection = ContextLocator.get_context().connection
            cursor = connection.cursor()
            cursor.execute("DELETE FROM cinemas WHERE id = ?;", (cinema, ))
            connection.commit()
            self.reload_items()
