from typing import Tuple

from PyQt5.QtWidgets import (QInputDialog, QMessageBox)

from context_locator import ContextLocator
from cinema_data import CinemaData
from cinema_item_widget import CinemaItemWidget
from items_viewer_widget import ItemsViewerWidget
from empty_page_widget import EmptyPageWidget
from halls_viewer_widget import HallsViewerWidget


class CinemasViewerWidget(ItemsViewerWidget):
    def reload_items(self):
        self.widgets.clear()
        connection = ContextLocator.get_context().connection
        cursor = connection.cursor()
        for cinema, name in cursor.execute("SELECT * FROM cinemas;").fetchall():
            self.add_widget(CinemaItemWidget(CinemaData(cinema, name)))

    def push_widget(self, widget: CinemaItemWidget):
        widget.opening_button_clicked.connect(self._handle_item_redirection)
        widget.editing_button_clicked.connect(self._handle_item_editing)
        widget.deleting_button_clicked.connect(self._handle_item_deleting)
        self._fast_push(widget)

    def _handle_item_adding(self):
        cinema_name, ok = QInputDialog.getText(self, 'Создание кинотеатра', 'Название:')
        if ok:
            if len(cinema_name) < 4:
                QMessageBox.information(self, 'Ошибка!', 'Длина названия должна быть больше 3 символов!')
                return
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
        name, ok = QInputDialog.getText(self, 'Переименование', 'Название:')
        if ok:
            if len(name) < 4:
                QMessageBox.information(self, 'Ошибка!', 'Длина названия должна быть больше 3 символов!')
                return
            connection = ContextLocator.get_context().connection
            cursor = connection.cursor()
            cursor.execute("UPDATE cinemas SET name = ? WHERE id = ?;", (name, cinema))
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
