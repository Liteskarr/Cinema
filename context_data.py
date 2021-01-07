import sqlite3

from dataclasses import dataclass


@dataclass(init=False)
class ContextData:
    permission_lvl: int
    current_cinema: int
    current_hall: int
    current_session: int

    connection: sqlite3.Connection

    datetime_show_format: str = "%d.%m.%Y %H:%M"
    datetime_packing_format: str = "%Y-%m-%d %H:%M"
