from dataclasses import dataclass


@dataclass
class AbstractData:
    @staticmethod
    def from_tuple(sql_tuple: tuple):
        raise NotImplementedError()
