import sqlite3

from dataclasses import dataclass


@dataclass(init=False)
class ContextData:
    permission_lvl: int

    connection: sqlite3.Connection
