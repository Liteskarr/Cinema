from singleton import Singleton
from context_data import ContextData


class ContextLocator(Singleton):
    _current_context: ContextData = None

    def get_context(self) -> ContextData:
        return self._current_context

    def set_context(self, context: ContextData):
        self._current_context = context
