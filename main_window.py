import PyQt5.uic as uic
from PyQt5.QtWidgets import (QMainWindow,
                             QWidget)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._configure_ui()

    def _configure_ui(self):
        uic.loadUi('res/uics/main_window.ui', self)

        self.backward.setShortcut('Ctrl+B')
        self.backward.triggered.connect(self._pop_widget)
        self.drop_stack.setShortcut('Ctrl+M')
        self.drop_stack.triggered.connect(self._return_to_start_page)

    def _stack_size(self):
        return self.widgets.count()

    def _get_top_widget(self):
        return self.widgets.widget(self._stack_size() - 1)

    def _display_top(self):
        self.widgets.setCurrentIndex(self._stack_size() - 1)

    def _push_widget(self, widget: QWidget):
        self.widgets.addWidget(widget)
        self._display_top()

    def _pop_widget(self):
        if self._stack_size() > 1:
            if not self._get_top_widget().exit_with_safing():
                return
            self.widgets.removeWidget(self._get_top_widget())
            self._display_top()

    def _return_to_start_page(self):
        while self._stack_size() > 1:
            if not self._get_top_widget().exit_with_safing():
                return
            self._pop_widget()

    def _handle_page_opening(self):
        page = self._get_top_widget().get_new_page()
        page.opened_new_page.connect(self._handle_page_opening)
        self._push_widget(page)

    def init_start_page(self, widget: QWidget):
        widget.opened_new_page.connect(self._handle_page_opening)
        self.widgets.addWidget(widget)
        self._display_top()
