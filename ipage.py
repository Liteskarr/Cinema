"""
Этот интерфейс позволяет разделить ответственность между несколькими подвиджетами одного приложения.
"""


from PyQt5.QtCore import (pyqtSignal)


class IPage:
    opened_new_page = pyqtSignal()

    def get_new_page(self):
        raise NotImplementedError()

    def exit_with_safing(self) -> bool:
        """
        Возвращает True, если было совершено закрытие страницы.
        Иначе False. Требует для контроля, например, за сохранением пользователем изменений.
        Переопределяется в классах-наследниках.
        """
        return True
