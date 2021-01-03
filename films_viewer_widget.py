from PyQt5.QtWidgets import QWidget, QMessageBox, QInputDialog

from context_locator import ContextLocator
from items_viewer_widget import ItemsViewerWidget
from film_item_widget import FilmItemWidget


class FilmsViewerWidget(ItemsViewerWidget):
    def _handle_item_adding(self, *args, **kwargs):
        film_name, ok_name = QInputDialog.getText(self, 'Создание фильма', 'Название:')
        film_duration, ok_duration = QInputDialog.getInt(self, 'Создание фильма', 'Продолжительность:', min=1)
        if ok_name and ok_duration:
            if len(film_name) < 4:
                QMessageBox.information(self, 'Ошибка!', 'Длина названия должна быть больше 3 символов!')
                return
            connection = ContextLocator.get_context().connection
            cursor = connection.cursor()
            cursor.execute("INSERT INTO films(name, duration) VALUES(?, ?);", (film_name, film_duration, ))
            connection.commit()
            self.reload_items()

    def _handle_item_deleting(self, film: int):
        connection = ContextLocator.get_context().connection
        cursor = connection.cursor()
        ok = QMessageBox.question(self, 'Вы уверены?', 'Это действие невозможно отменить!')
        if ok == QMessageBox.Yes:
            cursor.execute("DELETE FROM films WHERE id = ?;", (film,))
            connection.commit()
            self.reload_items()

    def push_widget(self, widget: FilmItemWidget):
        widget.film_deleting.connect(self._handle_item_deleting)
        self._fast_push(widget)

    def reload_items(self):
        self.widgets.clear()
        cursor = ContextLocator.get_context().connection.cursor()
        for film, name, duration in cursor.execute("SELECT * FROM films;").fetchall():
            self.push_widget(FilmItemWidget(film, name, duration))
