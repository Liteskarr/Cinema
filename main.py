import sys
import sqlite3

from PyQt5.QtWidgets import (QApplication)

from src.context_data import ContextData
from src.context_locator import ContextLocator
from src.main_window import MainWindow
from src.main_menu_widget import MainMenuWidget


def enable_threads_exceptions() -> None:
    excepthook = sys.excepthook

    def exception_hook(exctype, value, traceback):
        excepthook(exctype, value, traceback)
        sys.exit(1)

    sys.excepthook = exception_hook


def enable_debug_mode() -> None:
    enable_threads_exceptions()


def main():
    enable_debug_mode()
    context_data = ContextData()
    context_data.connection = sqlite3.connect('res/data/database.db')
    ContextLocator.set_context(context_data)

    application = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.init_start_page(MainMenuWidget())
    main_window.show()
    sys.exit(application.exec())


if __name__ == '__main__':
    main()
