from PyQt5.QtWidgets import QWidget, QMessageBox, QInputDialog

from context_locator import ContextLocator
from items_viewer_widget import ItemsViewerWidget
from film_item_widget import FilmItemWidget
from film_editor_widget import FilmEditorWidget


class FilmsViewerWidget(ItemsViewerWidget):
    def _handle_item_adding(self, *args, **kwargs):
        film_editor = FilmEditorWidget(self)
        film_editor.exec()
        _, film_name, film_duration, ok = film_editor.get_film()
        if ok:
            connection = ContextLocator.get_context().connection
            cursor = connection.cursor()
            cursor.execute("INSERT INTO films(name, duration) VALUES(?, ?);", (film_name, film_duration, ))
            connection.commit()
            self.reload_items()

    def _handle_item_deleting(self, film: int):
        connection = ContextLocator.get_context().connection
        cursor = connection.cursor()
        ok = QMessageBox.question(self,
                                  'Вы уверены?',
                                  'Это действие невозможно отменить! '
                                  'Все сеансы, использующии этот фильм, будут удалены.')
        if ok == QMessageBox.Yes:
            cursor.execute("DELETE FROM films WHERE id = ?;", (film,))
            cursor.execute("DELETE FROM tickets "
                           "WHERE session IN (SELECT id FROM sessions WHERE film = ?);", (film, ))
            cursor.execute("DELETE FROM sessions WHERE film = ?;", (film, ))
            connection.commit()
            self.reload_items()

    def push_widget(self, widget: FilmItemWidget):
        widget.deleting_button_clicked.connect(self._handle_item_deleting)
        self._fast_push(widget)

    def reload_items(self):
        self.widgets.clear()
        cursor = ContextLocator.get_context().connection.cursor()
        for film, name, duration in cursor.execute("SELECT * FROM films;").fetchall():
            self.push_widget(FilmItemWidget(film, name, duration))
