"""

"""

import PyQt5.uic as uic
from PyQt5.QtWidgets import (QWidget, QListWidgetItem)

from ipage import IPage


class ItemsViewerWidget(QWidget, IPage):
    def __init__(self):
        super().__init__()
        self._new_page = None
        self._configure_ui()
        self.reload_items()

    def _configure_ui(self):
        uic.loadUi('res/uics/items_viewer.ui', self)
        self.adding_button.clicked.connect(self._handle_item_adding)

    def _fast_push(self, widget: QWidget):
        item = QListWidgetItem(self.widgets)
        item.setSizeHint(widget.sizeHint())
        self.widgets.setItemWidget(item, widget)

    def _handle_item_adding(self, *args, **kwargs):
        raise NotImplementedError()

    def push_widget(self, widget: QWidget):
        raise NotImplementedError('Call _fast_push after your implementation.')

    def reload_items(self):
        raise NotImplementedError()

    def add_widget(self, widget: QWidget):
        self.push_widget(widget)

    def get_new_page(self):
        return self._new_page
