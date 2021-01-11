import PyQt5.uic as uic
from PyQt5.QtWidgets import (QWidget)

from src.ipage import IPage
from src.empty_page_widget import EmptyPageWidget
from src.cinemas_viewer_widget import CinemasViewerWidget
from src.films_viewer_widget import FilmsViewerWidget
from src.searching_widget import SearchingWidget
from src.statistics_widget import StatisticsWidget


class MainMenuWidget(QWidget, IPage):
    def __init__(self):
        super().__init__()
        self._new_page = EmptyPageWidget()
        self._configure_ui()

    def _configure_ui(self):
        uic.loadUi('res/uics/main_menu.ui', self)
        self.cinemas_button.clicked.connect(self._handle_cinemas_button_click)
        self.statistic_button.clicked.connect(self._handle_statistic_button_click)
        self.searching_button.clicked.connect(self._handle_searching_button_click)
        self.films_button.clicked.connect(self._handle_films_button_click)

    def _handle_cinemas_button_click(self):
        self._new_page = CinemasViewerWidget()
        self.opened_new_page.emit()
        self._new_page = EmptyPageWidget()

    def _handle_films_button_click(self):
        self._new_page = FilmsViewerWidget()
        self.opened_new_page.emit()
        self._new_page = EmptyPageWidget()

    def _handle_searching_button_click(self):
        self._new_page = SearchingWidget()
        self.opened_new_page.emit()
        self._new_page = EmptyPageWidget()

    def _handle_statistic_button_click(self):
        self._new_page = StatisticsWidget()
        self.opened_new_page.emit()
        self._new_page = EmptyPageWidget()

    def get_new_page(self):
        return self._new_page
