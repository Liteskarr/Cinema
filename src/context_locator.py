from src.singleton import Singleton
from src.context_data import ContextData


class ContextLocator(Singleton):
    _current_context: ContextData = None

    @staticmethod
    def get_context() -> ContextData:
        return ContextLocator._current_context

    @staticmethod
    def set_context(context: ContextData):
        ContextLocator._current_context = context
