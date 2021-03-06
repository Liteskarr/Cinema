from PyQt5.QtWidgets import (QInputDialog, QMessageBox, QWidget)


from src.context_locator import ContextLocator
from src.hall_item_widget import HallItemWidget
from src.items_viewer_widget import ItemsViewerWidget
from src.sessions_viewer_widget import SessionsViewerWidget
from src.empty_page_widget import EmptyPageWidget
from src.hall_editor_widget import HallEditorWidget


class HallsViewerWidget(ItemsViewerWidget):
    def _handle_item_adding(self, *args, **kwargs):
        hall_editor = HallEditorWidget(self)
        hall_editor.exec()
        _, hall_name, hall_width, hall_height, ok = hall_editor.get_hall()
        if ok:
            cinema = ContextLocator.get_context().current_cinema
            connection = ContextLocator.get_context().connection
            cursor = connection.cursor()
            cursor.execute("INSERT INTO halls(name, cinema, width, height) VALUES(?, ?, ?, ?);",
                           (hall_name, cinema, hall_width, hall_height))
            connection.commit()
            self.reload_items()

    def _handle_item_redirection(self, hall: int):
        ContextLocator.get_context().current_hall = hall
        self._new_page = SessionsViewerWidget()
        self.opened_new_page.emit()
        self._new_page = EmptyPageWidget()

    def _handle_item_editing(self, hall: int):
        connection = ContextLocator.get_context().connection
        cursor = connection.cursor()
        old_name = cursor.execute("SELECT name FROM halls WHERE id = ?;", (hall, )).fetchone()[0]
        name, ok = QInputDialog.getText(self, 'Переименование зала', 'Название:', text=old_name)
        if ok:
            if len(name) < 4:
                QMessageBox.information(self, 'Ошибка!', 'Длина названия должна быть больше 3 символов!')
                return
            cursor.execute("UPDATE halls SET name = ? WHERE id = ?;", (name, hall, ))
            connection.commit()
            self.reload_items()

    def _handle_item_deleting(self, hall: int):
        ok = QMessageBox.question(self, 'Вы уверены?', 'Это действие невозможно отменить!')
        if ok == QMessageBox.Yes:
            connection = ContextLocator.get_context().connection
            cursor = connection.cursor()
            cursor.execute("DELETE FROM halls WHERE id = ?;", (hall,))
            connection.commit()
            self.reload_items()

    def push_widget(self, widget: HallItemWidget):
        widget.opening_button_clicked.connect(self._handle_item_redirection)
        widget.editing_button_clicked.connect(self._handle_item_editing)
        widget.deleting_button_clicked.connect(self._handle_item_deleting)
        self._fast_push(widget)

    def reload_items(self):
        self.widgets.clear()
        connection = ContextLocator.get_context().connection
        cursor = connection.cursor()
        cinema = ContextLocator.get_context().current_cinema
        for hall, name, width, height in cursor.execute("SELECT id, name, width, height "
                                                        "FROM halls WHERE cinema = ?;", (cinema, )).fetchall():
            self.push_widget(HallItemWidget(hall, name, width, height))
