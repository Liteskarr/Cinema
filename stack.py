"""
Обертка обычного листа-стека в ООП-класс.
"""


import typing


T = typing.TypeVar('T')


class Stack(typing.Generic[T]):
    def __init__(self):
        self._data: typing.List[T] = []

    def __len__(self) -> int:
        return len(self._data)

    def top(self) -> T:
        return self._data[-1]

    def push(self, x: T) -> None:
        self._data.append(x)

    def pop(self) -> T:
        return self._data.pop(-1)
