from dataclasses import dataclass

from abstract_data import AbstractData


@dataclass
class CinemaData(AbstractData):
    id: int
    name: str

    @staticmethod
    def from_tuple(sql_tuple: tuple):
        return CinemaData(*sql_tuple)
